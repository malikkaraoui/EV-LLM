"""E015 -- tests (python -m unittest test_e015)."""
import unittest

import numpy as np

import circuits as C
import d15
import programmes as PG
from d15 import ABS, EGAL, MOINS, PLUS

ID = np.array(list(range(10)) + [0, 0, 0, 10])
COMPL = np.array([9 - d for d in range(10)] + [0, 0, 0, 9])


def _lib():
    if not hasattr(_lib, "L"):
        _lib.L = []
        for t, k in [("M-SOMME", 2), ("M-SUCC", 1)]:
            P = C.vie(C.init_poids(np.random.default_rng(1), k, 4, 32), t, 0, 600, 1e-2)
            _lib.L.append({"poids": P, "ports": k, "niche": t})
    return _lib.L


def prog_n1():
    return {"ins": [{"op": "DEC", "r": [0], "v": PLUS}, {"op": "DEC", "r": [2], "v": EGAL},
                    {"op": "INV", "r": [1]}, {"op": "INV", "r": [3]},
                    {"op": "CH", "c": 0, "r": [5, 6], "A": [ID, ID]},
                    {"op": "INV", "r": [7]}], "sortie": 8}


def prog_n3():
    return {"ins": [{"op": "DEC", "r": [0], "v": MOINS}, {"op": "DEC", "r": [2], "v": EGAL},
                    {"op": "INV", "r": [1]}, {"op": "INV", "r": [3]},
                    {"op": "CH", "c": 0, "r": [5, 6], "A": [ID, COMPL]},
                    {"op": "CH", "c": 1, "r": [7], "A": [ID]}, {"op": "TRQ", "r": [8]},
                    {"op": "INV", "r": [9]}], "sortie": 10}


class Donnees(unittest.TestCase):
    def test_oracle_partout(self):
        for t in d15.TACHES:
            for jeux in (d15.jeu_val(t), d15.jeux_test(t)):
                for par in jeux.values():
                    for its in par.values():
                        for it in its:
                            self.assertEqual(d15.oracle(t, it), d15.reference(t, it))

    def test_oracle_mutant_tue(self):
        # une retenue oubliee doit etre vue par la comparaison
        self.assertNotEqual(d15.oracle_somme((999, 1)).replace("1", "0", 1),
                            d15.reference("N1", (999, 1)))

    def test_disjonction_flux(self):
        for t in d15.TACHES:
            train = set()
            for g in range(30):
                train.update(d15.lot_train(t, 1, g))
            for nom, par in dict(d15.jeu_val(t), **d15.jeux_test(t)).items():
                for its in par.values():
                    self.assertFalse(train & set(its), (t, nom))
            self.assertTrue(all(max(len(str(x)) for x in it) <= 5 for it in train))

    def test_generateurs_adverses(self):
        for L in (10, 100):
            T1 = d15.jeux_test("N1")
            self.assertTrue(all(a + b == 10 ** L for a, b in T1["ADV-PROPAG"][L][2:]))
            T2 = d15.jeux_test("N2")
            self.assertTrue(all(sum(it) == 10 ** L for it in T2["ADV-PROPAG3"][L]))
            T3 = d15.jeux_test("N3")
            self.assertTrue(all(a == b for a, b in T3["ADV-EGAUX"][L]))
            self.assertTrue(all(a >= b for jeu in T3.values() for its in jeu.values()
                                for a, b in its))

    def test_mini_taches(self):
        self.assertEqual(d15.cible_mini("M-SOMME", (95, 7)), [2, 0, 1])
        self.assertEqual(d15.cible_mini("M-DIFF", (12, 5)), [7, 1, 0])
        self.assertEqual(d15.cible_mini("M-COMPL", (30,)), [9, 6, 0])
        self.assertEqual(d15.cible_mini("M-SUCC", (99,)), [0, 0, 1])


class Programmes(unittest.TestCase):
    def test_decode(self):
        self.assertEqual(PG.decode(np.array([0, 0, 1, 2])), "12")
        self.assertEqual(PG.decode(np.array([0, 0])), "0")
        self.assertIsNone(PG.decode(np.array([1, EGAL])))
        self.assertIsNone(PG.decode(np.array([], dtype=np.int64)))

    def test_programmes_main_existent(self):
        """Controle positif : l'assemblage est atteignable avec la bibliotheque (N1, N3)."""
        lib = _lib()
        for t, p in (("N1", prog_n1()), ("N3", prog_n3())):
            its = d15.jeux_test(t)["T-LONG"][32][:100]
            reps, _, _ = PG.executer(p, lib, its, t)
            ok = np.mean([r == d15.reference(t, it) for r, it in zip(reps, its)])
            self.assertGreaterEqual(ok, 0.99, t)

    def test_adaptateur_mutant_tue(self):
        lib = _lib()
        p = prog_n1()
        p["ins"][4]["A"][1] = ID.copy()
        p["ins"][4]["A"][1][3] = 4
        its = d15.lot_train("N1", 1, 0, 64)
        s, ex = PG.score(PG.executer(p, lib, its, "N1")[0], its, "N1")
        self.assertLess(ex, 0.9)

    def test_net_equivalent_et_aleatoires_executables(self):
        lib = _lib()
        rng = np.random.default_rng(0)
        its = d15.lot_train("N2", 1, 0, 32)
        for _ in range(300):
            p = PG.prog_alea(rng, lib)
            for _ in range(3):
                p = PG.mute(rng, p, lib)
            a = PG.executer(p, lib, its, "N2")[0]
            b = PG.executer(PG.net(p), lib, its, "N2")[0]
            self.assertEqual(a, b)

    def test_juge_compte(self):
        lib = _lib()
        J = PG.Juge(lib, "N1")
        its = d15.lot_train("N1", 1, 0, 64)
        s, ex, _ = J(prog_n1(), its)
        self.assertEqual((J.essais, ex), (1, 1.0))
        self.assertAlmostEqual(s, 1.1)

    def test_vie_ameliore(self):
        lib = _lib()
        rng = np.random.default_rng(3)
        p = prog_n1()
        p["ins"][4]["A"][0] = ID.copy()
        p["ins"][4]["A"][0][7] = 2
        J = PG.Juge(lib, "N1")
        its = d15.lot_train("N1", 1, 0, 64)
        s0, _, _ = J(p, its)
        p2, s1, ex1 = PG.vie(rng, PG.copie(p), J, its, 400)
        self.assertGreaterEqual(s1, s0)
        self.assertEqual(ex1, 1.0)


if __name__ == "__main__":
    unittest.main()
