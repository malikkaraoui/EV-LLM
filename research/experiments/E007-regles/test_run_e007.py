"""Tests de run_e007.py -- horloge et appels simules (ceux de test_run_paced d'E006), zero reseau.

  python3 -m unittest test_run_e007
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "E006-replication-frontiere"))
import run_e007  # noqa: E402
from test_run_paced import KEY, Appels, Horloge, mk  # noqa: E402


class TestRunE007(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.d = Path(self.tmp.name)
        cases = [mk("B-1", "B", 1), mk("A-1", "A", 1), mk("C-1", "C", 2), mk("D-1", "D", 1)]
        self.cf = self.d / "cases.json"
        self.cf.write_text(json.dumps({"cases": cases}), encoding="utf-8")
        self.res = self.d / "results"
        self.h = Horloge()

    def tearDown(self):
        self.tmp.cleanup()

    def lancer(self, appels, *extra):
        return run_e007.main(["--cases", str(self.cf), "--results", str(self.res), *extra],
                             call=appels, now=self.h.now, sleep=self.h.sleep, load_key=lambda _: KEY)

    def ids(self):
        out = []
        for d in sorted(self.res.glob("2026-*")):
            out += [json.loads(l)["case_id"] for l in (d / "raw.jsonl").read_text().splitlines()]
        return out

    def test_ordre_D_C_A_B(self):
        self.assertEqual(self.lancer(Appels(self.h)), 0)
        self.assertEqual(self.ids(), ["D-1", "C-1", "C-1", "A-1", "B-1"])

    def test_budget_100_par_defaut_et_plafond(self):
        a = Appels(self.h)
        self.assertEqual(self.lancer(a, "--budget", "101"), 2)
        self.assertEqual(a.faits, [])
        self.assertEqual(run_e007.BUDGET, 100)

    def test_intervalle_et_max_calls_herites(self):
        a = Appels(self.h)
        self.assertEqual(self.lancer(a, "--min-interval", "15"), 2)  # run_paced exige >= 26
        self.assertEqual(self.lancer(a, "--max-calls", "9"), 2)
        self.assertEqual(a.faits, [])
        self.lancer(a, "--max-calls", "3")
        self.h.t += 1
        self.lancer(a)
        departs = []
        for d in sorted(self.res.glob("2026-*")):
            departs += [json.loads(l)["t_epoch"] for l in (d / "raw.jsonl").read_text().splitlines()]
        self.assertTrue(all(b - x >= 26 for x, b in zip(departs, departs[1:])))

    def test_vrai_corpus_ordre_et_budget(self):
        cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]
        self.assertLessEqual(sum(c["cible"] for c in cases), run_e007.BUDGET)
        self.assertEqual(set(c["groupe"] for c in cases), set("DCAB"))
        n200, ordre = {}, []
        run_e007.run_paced.ORDRE_GROUPES = run_e007.ORDRE_GROUPES
        while True:
            c = run_e007.run_paced.prochain_cas(cases, n200)
            if c is None:
                break
            ordre.append(c["groupe"])
            n200[c["id"]] = n200.get(c["id"], 0) + 1
        self.assertEqual("".join(dict.fromkeys(ordre)), "DCAB")
        self.assertEqual(len(ordre), 90)


if __name__ == "__main__":
    unittest.main()
