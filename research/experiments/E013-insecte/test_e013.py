"""E013 -- tests : jeux, encodages, disjonction entrainement/test, decodage, reprise."""
import json
import os
import shutil
import subprocess
import sys
import unittest

import numpy as np

import donnees as D

ICI = os.path.dirname(os.path.abspath(__file__))


class Jeux(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test = D.jeux_test()
        cls.val = D.jeu_val()

    def test_tailles_et_longueurs(self):
        for L, it in self.val["VAL-OOD"].items():
            self.assertEqual(len(it), 500)
            self.assertTrue(all(len(str(a)) == L == len(str(b)) for a, b in it))
        for L, it in self.test["T-LONG"].items():
            self.assertEqual(len(it), 200 if L == 1000 else 500)
            self.assertTrue(all(len(str(a)) == L == len(str(b)) for a, b in it))
        for L in D.ADV_LENS:
            self.assertEqual(len(self.test["ADV-CASCADE"][L]), 103)
            self.assertEqual(len(self.test["ADV-ZEROS"][L]), 101)
            self.assertEqual(len(self.test["ADV-ASYM"][L]), 101)

    def test_cascade_retenue_partout(self):
        for L, it in self.test["ADV-CASCADE"].items():
            for a, b in it[3:13]:
                self.assertEqual(D.e008.chaine_retenue(a, b), L)
            self.assertEqual(it[0], (int("9" * L), 1))

    def test_asym(self):
        for L, it in self.test["ADV-ASYM"].items():
            for a, b in it:
                self.assertEqual(sorted([len(str(a)), len(str(b))])[1], L)
                self.assertLessEqual(min(len(str(a)), len(str(b))), 5)

    def test_disjoint_du_flux(self):
        tous = set()
        for jeux in (self.val, self.test):
            for par_l in jeux.values():
                for it in par_l.values():
                    tous.update(it)
                    tous.update((b, a) for a, b in it)
        for g in (0, 1, 5):
            for t in range(0, 6000, 97):
                self.assertFalse(tous & set(D.paires_flux(g, t)))

    def test_deterministe(self):
        self.assertEqual(D.jeux_test()["ADV-ZEROS"][16], self.test["ADV-ZEROS"][16])


class Encodage(unittest.TestCase):
    def test_aligne(self):
        A, B, Y, M = D.encode_aligne([(95, 7), (1, 2)])
        self.assertEqual(A[0].tolist(), [5, 9, 10])
        self.assertEqual(B[0].tolist(), [7, 10, 10])
        self.assertEqual(Y[0].tolist(), [2, 0, 1])   # 102
        self.assertEqual(M[1].tolist(), [1, 1, 0])
        self.assertEqual(Y[1].tolist(), [3, 0, 0])

    def test_decode_un_seul_zero(self):
        self.assertEqual(D.decode([3, 0]), "3")
        self.assertEqual(D.decode([2, 0, 1]), "102")
        self.assertEqual(D.decode([0, 0]), "0")
        self.assertEqual(D.decode([3, 0, 0]), "03")  # un seul 0 retire : faux ensuite

    def test_plat(self):
        S = D.encode_plat([(12, 3)])
        self.assertEqual(S[0].tolist(), [D.DEBUT, 1, 2, 10, 3, 11])

    def test_jeu_fixe_unique(self):
        j = D.jeu_fixe(1, 1000)
        self.assertEqual(len(set(j)), 1000)
        self.assertEqual(j[:5], D.jeu_fixe(1, 5))


class Modeles(unittest.TestCase):
    def test_oracle_i1_par_construction(self):
        """Controle positif : un I1 dont les poids codent la retenue a la main passe a 1000
        chiffres -> l'architecture peut representer la regle (H = 1)."""
        import mlx.core as mx
        from modeles import I1
        from systemes import systeme
        m = I1(1)
        # t = a_t + b_t + h (h ~ 0,995 si retenue, 0 sinon) ; z_k = relu(t - k + 1), k = 0..20
        # u_k = z_k - z_{k+1} = 1 ssi t >= k ; retenue = u_10 ; chiffre c = u_c - u_{c+1} + u_{c+10} - u_{c+11}
        W1 = np.zeros((32, 23), np.float32)
        b1 = np.zeros(32, np.float32)
        for k in range(21):
            for d in range(10):
                W1[k, d] = d
                W1[k, 11 + d] = d      # ABSENT (indice 10) -> 0
            W1[k, 22] = 1.0
            b1[k] = 1.0 - k
        U = np.zeros((21, 32), np.float32)
        for k in range(20):
            U[k, k], U[k, k + 1] = 1, -1
        Wh = (3 * U[10])[None, :]
        bh = np.zeros(1, np.float32)
        Wo = np.stack([30 * (U[c] - U[c + 1] + U[c + 10] - U[c + 11]) for c in range(10)])
        m.cell.l1.weight = mx.array(W1)
        m.cell.l1.bias = mx.array(b1)
        m.cell.lh.weight = mx.array(Wh)
        m.cell.lh.bias = mx.array(bh)
        m.cell.lo.weight = mx.array(Wo)
        m.cell.lo.bias = mx.zeros(10)
        rng = np.random.default_rng(0)
        paires = [(D.e008.tire_nombre(rng, 1000), D.e008.tire_nombre(rng, 1000)) for _ in range(5)]
        paires += [(int("9" * 1000), 1), (10 ** 999, 999), (7, 5), (0, 0)]
        out = systeme(m)(paires)
        self.assertEqual([r for r, _ in out], [str(a + b) for a, b in paires])

    def test_i2_forme(self):
        import mlx.core as mx
        from modeles import I2
        m = I2(8)
        S = mx.array(D.encode_plat([(12, 345), (9, 9)]))
        self.assertEqual(m(S, 4).shape, (2, 4, 10))


class Reprise(unittest.TestCase):
    def test_reprise_identique(self):
        """Un run coupe puis repris finit au meme etat que le run d'un seul tenant."""
        py = sys.executable
        base = os.path.join(ICI, "runs")
        for tag in ("tA", "tB"):
            shutil.rmtree(os.path.join(base, f"I1-H2-s7-{tag}"), ignore_errors=True)
        cmd = [py, "entraine.py", "--configs", "I1-H2", "--graines", "7", "--lr", "1e-2",
               "--pas", "500", "--cpu"]
        subprocess.run(cmd + ["--tag", "tA"], cwd=ICI, check=True, capture_output=True)
        # tB : budget nul -> s'arrete au premier point de sauvegarde (250), puis reprend
        r = subprocess.run(cmd + ["--tag", "tB", "--budget-min", "0"], cwd=ICI, check=True,
                           capture_output=True, text=True)
        self.assertIn("BUDGET", r.stdout)
        subprocess.run(cmd + ["--tag", "tB"], cwd=ICI, check=True, capture_output=True)
        ea = json.load(open(os.path.join(base, "I1-H2-s7-tA", "etat.json")))
        eb = json.load(open(os.path.join(base, "I1-H2-s7-tB", "etat.json")))
        self.assertTrue(ea["fini"] and eb["fini"])
        self.assertEqual([v[0] for v in ea["val"]], [v[0] for v in eb["val"]])
        self.assertAlmostEqual(ea["val"][-1][1], eb["val"][-1][1], places=4)
        self.assertEqual(ea["exemples_uniques_vus"], eb["exemples_uniques_vus"])
        for tag in ("tA", "tB"):
            shutil.rmtree(os.path.join(base, f"I1-H2-s7-{tag}"))


class AdvPropag(unittest.TestCase):
    """ADV-PROPAG (post hoc, R010) : rang 0 genere la retenue, tous les autres la propagent."""

    def test_propagation_pure(self):
        import adv_propag as P
        jeu = P.jeu_propag()
        self.assertEqual(jeu, P.jeu_propag())  # deterministe
        for L, it in jeu.items():
            self.assertEqual(len(it), 2 + P.N_PROPAG)
            self.assertEqual(len(set(it)), len(it))
            self.assertEqual(it[0], (int("9" * L), 1))
            for a, b in it[2:]:
                self.assertEqual(a + b, 10 ** L)
                self.assertTrue(len(str(a)) == L == len(str(b)))
                da, db = D.chiffres_lsb(a), D.chiffres_lsb(b)
                self.assertEqual(da[0] + db[0], 10)
                self.assertTrue(all(x + y == 9 for x, y in zip(da[1:], db[1:])))
                self.assertEqual(D.e008.chaine_retenue(a, b), L)

    def test_part_propagation(self):
        import adv_propag as P
        self.assertEqual(P.rangs_propagation([(45, 55)]), (1, 2))
        self.assertEqual(P.rangs_propagation([(17, 1)]), (0, 1))


if __name__ == "__main__":
    unittest.main()
