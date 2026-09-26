"""Tests de run_paced.py -- horloge et appels simules, zero reseau.

  python3 -m unittest test_run_paced
"""
import json
import tempfile
import unittest
from pathlib import Path

import run_paced

KEY = "cle-de-test-XYZ"


def mk(cid, groupe, cible):
    return {"id": cid, "famille": "synth", "groupe": groupe, "cible": cible,
            "state": "etat " + cid,
            "questions": {"q": {"type": "boolean", "instructions": "ok ?"}},
            "attendu": {"q": True}}


class Horloge:
    """now() avance de la duree des sleep() et de `latence` a chaque appel HTTP simule."""

    def __init__(self, t=1_790_000_000.0):
        self.t, self.sleeps = t, []

    def now(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(s)
        self.t += s


class Appels:
    def __init__(self, horloge, statuts=None, corps=None, latence=2.0):
        self.h, self.statuts, self.corps, self.lat = horloge, list(statuts or []), corps, latence
        self.faits = []

    def __call__(self, key, body):
        self.faits.append(body)
        self.h.t += self.lat
        status = self.statuts.pop(0) if self.statuts else 200
        text = self.corps or json.dumps({"answers": {"q": {"probability": 0.9}}})
        return status, self.lat * 1000, {"x-secret-header": "h"}, text, None


class TestRunPaced(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        self.cases = [mk("P-1", "P", 1), mk("R-1", "R", 2), mk("R-2", "R", 2), mk("C-1", "C", 1)]
        self.cf = self.d / "cases.json"
        self.cf.write_text(json.dumps({"cases": self.cases}), encoding="utf-8")
        self.res = self.d / "results"
        self.h = Horloge()

    def tearDown(self):
        self.tmp.cleanup()

    def lancer(self, appels, *extra):
        argv = ["--cases", str(self.cf), "--results", str(self.res), *extra]
        return run_paced.main(argv, call=appels, now=self.h.now, sleep=self.h.sleep,
                              load_key=lambda _: KEY)

    def records(self, fichier="raw.jsonl"):
        out = []
        for d in sorted(self.res.glob("2026-*")):
            out += [json.loads(l) for l in (d / fichier).read_text().splitlines()]
        return out

    def test_ordre_R_puis_C_puis_P_et_round_robin(self):
        a = Appels(self.h)
        self.assertEqual(self.lancer(a), 0)
        ids = [r["case_id"] for r in self.records()]
        self.assertEqual(ids, ["R-1", "R-2", "R-1", "R-2", "C-1", "P-1"])

    def test_intervalle_minimal_respecte_dans_et_entre_invocations(self):
        a = Appels(self.h)
        self.lancer(a, "--max-calls", "3")
        self.h.t += 5  # invocation suivante lancee 5 s apres la fin de la precedente
        self.lancer(a, "--max-calls", "3")
        recs = self.records()
        self.assertEqual(len(recs), 6)
        departs = [r["t_epoch"] for r in recs]
        ecarts = [b - a for a, b in zip(departs, departs[1:])]
        self.assertTrue(all(e >= 26 for e in ecarts), ecarts)
        self.assertIsNone(recs[0]["intervalle_s"])
        self.assertEqual([r["intervalle_s"] for r in recs[1:]], [round(e, 1) for e in ecarts])
        self.assertEqual(len(self.h.sleeps), 5)  # une attente avant chaque appel sauf le premier

    def test_refus_intervalle_et_max_calls_hors_bornes(self):
        a = Appels(self.h)
        self.assertEqual(self.lancer(a, "--min-interval", "25"), 2)
        self.assertEqual(self.lancer(a, "--max-calls", "9"), 2)
        self.assertEqual(a.faits, [])

    def test_max_calls(self):
        a = Appels(self.h)
        self.lancer(a, "--max-calls", "2")
        self.assertEqual(len(a.faits), 2)

    def test_budget_total_compte_tous_les_statuts(self):
        a = Appels(self.h, statuts=[429, 200])
        self.lancer(a, "--budget", "2")
        self.assertEqual(len(a.faits), 2)
        self.assertEqual(self.lancer(a, "--budget", "2"), 5)
        self.assertEqual(len(a.faits), 2)

    def test_non_200_ne_compte_pas_vers_la_cible(self):
        a = Appels(self.h, statuts=[503])
        self.lancer(a, "--max-calls", "5")
        ids = [r["case_id"] for r in self.records()]
        self.assertEqual(ids, ["R-1", "R-1", "R-2", "R-1", "R-2"])

    def test_stop_sur_401(self):
        a = Appels(self.h, statuts=[200, 401])
        self.assertEqual(self.lancer(a), 4)
        self.assertEqual(len(a.faits), 2)

    def test_stop_apres_echecs_consecutifs(self):
        a = Appels(self.h, statuts=[429, 429, 429, 200])
        self.assertEqual(self.lancer(a), 1)
        self.assertEqual(len(a.faits), 3)

    def test_rien_a_faire(self):
        a = Appels(self.h)
        self.lancer(a)
        self.assertEqual(self.lancer(a), 5)

    def test_public_sans_entetes_et_equivalent(self):
        self.lancer(Appels(self.h), "--max-calls", "2")
        raw, pub = self.records(), self.records("raw.public.jsonl")
        self.assertTrue(all("response_headers" in r for r in raw))
        self.assertEqual(pub, [{k: v for k, v in r.items() if k != "response_headers"} for r in raw])

    def test_corps_de_requete_identique_au_cas(self):
        a = Appels(self.h)
        self.lancer(a, "--max-calls", "1")
        self.assertEqual(a.faits[0], {"model": "typesafe-ai/jev", "state": "etat R-1",
                                      "questions": self.cases[1]["questions"]})

    def test_garde_anti_fuite(self):
        a = Appels(self.h, corps='{"echo": "' + KEY + '"}')
        self.assertEqual(self.lancer(a, "--max-calls", "1"), 3)
        for f in next(self.res.glob("2026-*")).iterdir():
            self.assertEqual(f.read_text(), "FUITE DETECTEE\n")


if __name__ == "__main__":
    unittest.main()
