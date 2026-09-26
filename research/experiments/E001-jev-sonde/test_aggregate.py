"""Tests de aggregate.py -- donnees synthetiques, zero reseau.

  python3 -m unittest test_aggregate
"""

import json
import tempfile
import unittest
from pathlib import Path

import aggregate

CASE_F = {"id": "X-1", "famille": "synth", "state": "phrase fausse",
          "questions": {"correcte": {"type": "boolean", "instructions": "ok ?"}},
          "attendu": {"correcte": False}}
CASE_T = {"id": "X-2", "famille": "synth", "state": "phrase juste",
          "questions": {"correcte": {"type": "boolean", "instructions": "ok ?"}},
          "attendu": {"correcte": True}}
CASE_C = {"id": "X-3", "famille": "synth", "state": "choix",
          "questions": {"statut": {"type": "choice", "instructions": "?",
                                   "criteria": {"a": "A", "b": "B"}}},
          "attendu": {"statut": "a"}}


def rec(case, rep, status, answers=None, lat=100.0, headers=True):
    body = {"model": "typesafe-ai/jev", "state": case["state"], "questions": case["questions"]}
    text = json.dumps({"answers": answers}) if answers is not None else '{"error":{}}'
    r = {"case_id": case["id"], "rep": rep, "ts": "t", "http_status": status,
         "latency_ms": lat, "request_body": body, "response_body_text": text}
    if headers:
        r["response_headers"] = {"X-Test": "1"}
    return r


def boolean(p):
    return {"correcte": {"type": "boolean", "probability": p}}


class AggregateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def run_dir(self, name, records, fname="raw.jsonl"):
        d = self.root / name
        d.mkdir()
        (d / fname).write_text("".join(json.dumps(r) + "\n" for r in records), encoding="utf-8")
        return d

    def rows(self, cases, dirs):
        rows, meta = aggregate.aggregate(cases, dirs)
        return {r["case_id"]: r for r in rows}, meta

    def test_ne_garde_que_les_200(self):
        a = self.run_dir("a", [rec(CASE_F, 1, 200, boolean(0.9)), rec(CASE_F, 2, 429)])
        b = self.run_dir("b", [rec(CASE_F, 1, 503), rec(CASE_F, 1, 200, boolean(0.7))])
        rows, meta = self.rows([CASE_F], [a, b])
        r = rows["X-1"]
        self.assertEqual(r["n_appels"], 2)          # seulement les 200
        self.assertEqual(r["stabilite"], [0.7, 0.9])
        self.assertAlmostEqual(r["p"], 0.8)
        self.assertEqual(meta["n_appels"], 4)
        self.assertEqual(meta["n_http_200"], 2)
        self.assertEqual(meta["sources"][0]["statuts_http"], {"200": 1, "429": 1})
        self.assertEqual(meta["sources"][1]["statuts_http"], {"503": 1, "200": 1})

    def test_faux_et_sur_et_conforme(self):
        # attendu false, P mediane 0.9 -> non conforme, faux et sur
        # attendu true, P mediane 0.1 -> non conforme, faux et sur
        a = self.run_dir("a", [rec(CASE_F, 1, 200, boolean(0.9)),
                               rec(CASE_T, 1, 200, boolean(0.1))])
        b = self.run_dir("b", [rec(CASE_F, 1, 200, boolean(0.85)),
                               rec(CASE_T, 1, 200, boolean(0.15))])
        rows, _ = self.rows([CASE_F, CASE_T], [a, b])
        for cid in ("X-1", "X-2"):
            self.assertIs(rows[cid]["conforme"], False)
            self.assertIs(rows[cid]["faux_et_sur"], True)

    def test_non_conforme_mais_pas_sur(self):
        a = self.run_dir("a", [rec(CASE_F, 1, 200, boolean(0.6)),
                               rec(CASE_T, 1, 200, boolean(0.3))])
        rows, _ = self.rows([CASE_F, CASE_T], [a])
        for cid in ("X-1", "X-2"):
            self.assertIs(rows[cid]["conforme"], False)
            self.assertIs(rows[cid]["faux_et_sur"], False)

    def test_conforme_aux_seuils(self):
        # frontieres de la regle : 0.5 compte comme true
        a = self.run_dir("a", [rec(CASE_F, 1, 200, boolean(0.49)),
                               rec(CASE_T, 1, 200, boolean(0.5))])
        rows, _ = self.rows([CASE_F, CASE_T], [a])
        self.assertIs(rows["X-1"]["conforme"], True)
        self.assertIs(rows["X-2"]["conforme"], True)

    def test_aucun_200_donne_non_parse(self):
        a = self.run_dir("a", [rec(CASE_F, 1, 429)])
        rows, _ = self.rows([CASE_F], [a])
        self.assertEqual(rows["X-1"]["obtenu"], "NON_PARSE")
        self.assertIsNone(rows["X-1"]["conforme"])

    def test_choice(self):
        ans = {"statut": {"type": "choice", "choice": "b", "probabilities": {"a": 0.1, "b": 0.9}}}
        a = self.run_dir("a", [rec(CASE_C, 1, 200, ans)])
        rows, _ = self.rows([CASE_C], [a])
        self.assertEqual(rows["X-3"]["obtenu"], "b")
        self.assertIs(rows["X-3"]["faux_et_sur"], True)

    def test_prefere_raw_public(self):
        d = self.run_dir("a", [rec(CASE_F, 1, 200, boolean(0.1), headers=False)],
                         fname="raw.public.jsonl")
        (d / "raw.jsonl").write_text(json.dumps(rec(CASE_F, 1, 200, boolean(0.9))) + "\n")
        rows, meta = self.rows([CASE_F], [d])
        self.assertEqual(meta["sources"][0]["fichier"], "raw.public.jsonl")
        self.assertAlmostEqual(rows["X-1"]["p"], 0.1)

    def test_refuse_requete_differente_du_cas(self):
        r = rec(CASE_F, 1, 200, boolean(0.1))
        r["request_body"]["state"] = "autre etat"
        a = self.run_dir("a", [r])
        with self.assertRaises(ValueError):
            aggregate.aggregate([CASE_F], [a])

    def test_dossier_sans_raw(self):
        d = self.root / "vide"
        d.mkdir()
        with self.assertRaises(FileNotFoundError):
            aggregate.aggregate([CASE_F], [d])

    def test_main_ecrit_summary_au_format_run(self):
        a = self.run_dir("a", [rec(CASE_F, 1, 200, boolean(0.2))])
        cases = self.root / "cases.json"
        cases.write_text(json.dumps({"cases": [CASE_F]}), encoding="utf-8")
        out = self.root / "out"
        rc = aggregate.main(["--cases", str(cases), "--out-root", str(out), str(a)])
        self.assertEqual(rc, 0)
        (d,) = list(out.iterdir())
        self.assertTrue(d.name.startswith("agregat-"))
        md = (d / "summary.md").read_text(encoding="utf-8")
        self.assertIn("| cas | question | attendu (préenregistré) | obtenu (médiane des "
                      "répétitions) | P ou confiance | stabilité (min–max) | latence médiane "
                      "(ms) | conforme | faux et sûr |", md)
        self.assertIn("| X-1 | correcte | false | false | 0.20 |", md)
        js = json.loads((d / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(js["meta"]["n_http_200"], 1)
        self.assertNotIn("response_headers", (d / "summary.json").read_text())

    def test_main_rc2_si_incoherent(self):
        r = rec(CASE_F, 1, 200, boolean(0.1))
        r["request_body"]["questions"] = {}
        a = self.run_dir("a", [r])
        cases = self.root / "cases.json"
        cases.write_text(json.dumps({"cases": [CASE_F]}), encoding="utf-8")
        rc = aggregate.main(["--cases", str(cases), "--out-root", str(self.root / "o"), str(a)])
        self.assertEqual(rc, 2)
        self.assertFalse((self.root / "o").exists())


if __name__ == "__main__":
    unittest.main()
