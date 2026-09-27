"""E011 -- tests unitaires : gradient, golden, oracle, codage MDL, jeux."""
import unittest

import numpy as np

from controles import addition_bits
from donnees import encode, jeu_entrainement, jeux_test
from objectifs import bits_entier, bits_poids, objectif_grad, quantifie
from rnn import N_PARAMS, ce_et_grad, golden, predit


class T(unittest.TestCase):
    def test_gradient_numerique(self):
        rng = np.random.default_rng(0)
        th = golden(2.0, 2.0) + rng.normal(0, 0.3, N_PARAMS)
        X, Y, M = encode(jeu_entrainement(1)[:20])
        _, g = ce_et_grad(th, X, Y, M)
        for i in range(N_PARAMS):
            e = np.zeros(N_PARAMS); e[i] = 1e-6
            num = (ce_et_grad(th + e, X, Y, M)[0] - ce_et_grad(th - e, X, Y, M)[0]) / 2e-6
            self.assertAlmostEqual(num, g[i], delta=1e-5 * max(1.0, abs(num)))

    def test_gradient_regularises(self):
        th = golden(3.0, 3.0) + 0.1
        X, Y, M = encode(jeu_entrainement(2)[:10])
        for code, lam in (("b", 0.1), ("c", 0.1)):
            f = objectif_grad(code, lam)
            _, _, g = f(th, X, Y, M)
            e = np.zeros(N_PARAMS); e[4] = 1e-6
            num = (f(th + e, X, Y, M)[0] - f(th - e, X, Y, M)[0]) / 2e-6
            self.assertAlmostEqual(num, g[4], delta=1e-5)

    def test_golden_exact_long(self):
        th = golden()
        paires = [(2 ** 1000 - 1, 1), (12345678901234567890, 98765432109876543210)]
        paires += jeux_test()["A-ASYM"][1000][:5]
        for (a, b), (rep, _) in zip(paires, predit(th, paires, encode)):
            self.assertEqual(rep, str(a + b))

    def test_oracle(self):
        rng = np.random.default_rng(1)
        for _ in range(500):
            a, b = int(rng.integers(0, 2 ** 40)), int(rng.integers(0, 2 ** 40))
            self.assertEqual(addition_bits(a, b), str(a + b))
        self.assertEqual(addition_bits(0, 0), "0")

    def test_encodage(self):
        X, Y, M = encode([(5, 3)])  # 101 + 011 = 1000
        self.assertEqual(M.sum(), 4)
        self.assertEqual(list(Y[0]), [0, 0, 0, 1])

    def test_codage_mdl(self):
        self.assertEqual(bits_entier(0), 1)
        self.assertEqual(bits_entier(1), 3)
        self.assertEqual(bits_poids(10.0), 1 + bits_entier(10) + bits_entier(1))
        self.assertLess(bits_poids(0.5), bits_poids(0.37))
        self.assertTrue(np.all(quantifie(golden()) == golden()))

    def test_entrainement(self):
        p = jeu_entrainement(3)
        self.assertEqual(len(set(p)), 100)
        self.assertTrue(all(max(a, b).bit_length() <= 5 for a, b in p))
        self.assertNotEqual(p, jeu_entrainement(4))


if __name__ == "__main__":
    unittest.main()
