"""E014 -- tests : jeux, curriculum, boucle = I2, pointeurs durs, interface de composition."""
import os
import unittest

import mlx.core as mx
import mlx.nn as nn
import numpy as np

import d14 as D
import donnees as D13
from m14 import R2, Lecteur, accumule, boucle, perte_addition, perte_lecture
from modeles import I1, I2
from s14 import seuil_abstention

ICI = os.path.dirname(os.path.abspath(__file__))


def lecture_parfaite(paires, T=None):
    """Logits d'un lecteur parfait : 30 sur la bonne classe (probabilite ~1)."""
    A, B, _, _ = D.encode_aligne(paires, T)
    return mx.array(30.0 * np.concatenate([np.eye(11)[A], np.eye(11)[B]], axis=-1))


class Jeux(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test, cls.val = D.jeux_test(), D.jeu_val()

    def test_tailles(self):
        for L, it in self.val["VAL-OOD"].items():
            self.assertEqual(len(it), 500)
            self.assertTrue(all(len(str(a)) == L == len(str(b)) for a, b in it))
        for L, it in self.test["T-LONG"].items():
            self.assertEqual(len(it), 200 if L == 1000 else 500)
        for L in D.ADV_LENS:
            self.assertEqual(len(self.test["ADV-CASCADE"][L]), 103)
            self.assertEqual(len(self.test["ADV-ASYM"][L]), 101)

    def test_graines_nouvelles(self):
        t13 = D13.jeux_test()
        self.assertNotEqual(t13["T-LONG"][16], self.test["T-LONG"][16])
        self.assertNotEqual(D13.jeu_val()["VAL-OOD"][6], self.val["VAL-OOD"][6])

    def test_disjoint_des_flux(self):
        tous = set()
        for jeux in (self.val, {k: v for k, v in self.test.items() if k != "T-ID"}):
            for par_l in jeux.values():
                for it in par_l.values():
                    tous.update(it)
                    tous.update((b, a) for a, b in it)
        for t in range(0, 12000, 211):
            self.assertFalse(tous & set(D.paires_flux(1, t)))
            self.assertFalse(tous & set(D.paires_curriculum(1, t, 12000)))

    def test_curriculum(self):
        self.assertEqual([D.lmax_curriculum(t, 12000) for t in (0, 2999, 3000, 6000, 9000, 11999)],
                         [2, 2, 3, 4, 5, 5])
        for t, lm in ((10, 2), (5000, 3), (11000, 5)):
            p = D.paires_curriculum(2, t, 12000)
            self.assertEqual(len(p), D.LOT)
            self.assertTrue(all(len(str(x)) <= lm for a, b in p for x in (a, b)))
        self.assertEqual(max(len(str(a)) for t in range(9000, 9020)
                             for a, _ in D.paires_curriculum(2, t, 12000)), 5)


class Modeles(unittest.TestCase):
    def test_boucle_egale_I2(self):
        mx.random.seed(3)
        m = I2(8)
        S = mx.array(D.encode_plat(D.paires_flux(1, 0)[:32]))
        self.assertEqual(float(mx.abs(m(S, 6) - boucle(m, S, 6, 10)).max()), 0.0)

    def test_pointeurs_durs_entiers_et_gradient(self):
        mx.random.seed(4)
        m = R2(8)
        p = D.paires_flux(1, 3)[:32]
        S = mx.array(D.encode_plat(p))
        _, pos = boucle(m, S, 6, 10, dur=True, garder_pos=True)
        pos = np.array(pos).astype(np.int64)  # argmax MLX = uint32
        self.assertTrue(np.all(np.abs(np.diff(pos, axis=1)) <= 1))  # pas relatifs -1/0/+1
        A, B, Y, M = D.encode_aligne(p, 6)
        _, g = nn.value_and_grad(m, lambda mm: perte_addition(mm, S, mx.array(Y), mx.array(M), 6))(m)
        self.assertGreater(float(mx.abs(g["q"]).sum()), 0.0)   # le depart apprend
        self.assertGreater(float(mx.abs(g["cell"]["lo"]["weight"][10:]).sum()), 0.0)  # decalages

    def test_lecteur_sorties(self):
        mx.random.seed(5)
        m = Lecteur(8)
        p = D.paires_flux(1, 3)[:8]
        S = mx.array(D.encode_plat(p))
        self.assertEqual(m(S, 6).shape, (8, 6, 22))
        A, B, _, M = D.encode_aligne(p, 6)
        l = perte_lecture(m, S, mx.array(A), mx.array(B), mx.array(M), 6)
        self.assertTrue(np.isfinite(float(l)))


class Composition(unittest.TestCase):
    """Controle positif de l'interface : lecture parfaite + I1 E013 gele = addition exacte."""

    def _exact(self, i1, paires):
        n = max(D.n_pas(a, b) for a, b in paires)
        tok = np.array(mx.argmax(accumule(i1, lecture_parfaite(paires, n), 64), -1))
        return np.mean([D.decode(tok[j, :D.n_pas(a, b)]) == str(a + b)
                        for j, (a, b) in enumerate(paires)])

    def test_lecture_parfaite_plus_i1_gele(self):
        t = D.jeux_test()
        for g in range(1, 6):
            i1 = I1(4)
            i1.load_weights(os.path.join(ICI, "i1_e013", f"I1-H4-s{g}.safetensors"))
            for jeu in ("ADV-CASCADE", "ADV-ZEROS", "ADV-ASYM"):
                for L in (16, 100):
                    paires = [p for p in t[jeu][L] if D.n_pas(*p) == L + 1]
                    self.assertEqual(self._exact(i1, paires), 1.0, (g, jeu, L))

    def test_i1_aleatoire_echoue(self):  # mutant : I1 non entraine
        mx.random.seed(0)
        self.assertLess(self._exact(I1(4), D.jeux_test()["T-LONG"][16]), 0.05)


class Abstention(unittest.TestCase):
    def test_seuil(self):
        self.assertEqual(seuil_abstention([0.999] * 100), 0.99)
        self.assertEqual(seuil_abstention([0.999] * 94 + [0.55] * 6), 0.5)
        self.assertEqual(seuil_abstention([0.1] * 10), None)


if __name__ == "__main__":
    unittest.main()
