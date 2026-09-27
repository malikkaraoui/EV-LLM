"""E012 -- tests unitaires (python -m unittest -v test_e012)."""
import unittest

import numpy as np

from jeux import EXPERIENCES, encode_aligne, encode_plat, encodeur, jeu_entrainement
from recherche import depuis_json, _jsonable
from reseau import (circuit_main, cle, copie, evalue, longueur_G, mute, preuve_aligne, systeme,
                    vide)
from verifs import addition_listes


class T(unittest.TestCase):
    def test_circuit_binaire_et_decimal_exacts_sur_train(self):
        for exp in ("X1", "X2-100", "X2-1000"):
            base = EXPERIENCES[exp]["base"]
            lots = encodeur(exp)(jeu_entrainement(exp, 1))
            dg, faux, ex, n = evalue(circuit_main(base), lots, base)
            self.assertEqual((dg, faux, ex), (0.0, 0, n), exp)

    def test_systeme_circuit_long(self):
        sysd = systeme(circuit_main(10), EXPERIENCES["X2-100"], encodeur("X2-100"))
        a, b = int("9" * 300), 1
        self.assertEqual(sysd([(a, b), (123, 98765)])[0][0], str(a + b))
        self.assertEqual(sysd([(123, 98765)])[0][0], str(123 + 98765))
        sysb = systeme(circuit_main(2), EXPERIENCES["X1"], encodeur("X1"))
        self.assertEqual(sysb([(2 ** 999 - 1, 1)])[0][0], str(2 ** 999))

    def test_preuve(self):
        self.assertEqual(preuve_aligne(circuit_main(10), 10)[0], "PROUVE")
        self.assertEqual(preuve_aligne(circuit_main(2), 2)[0], "PROUVE")
        g = circuit_main(10)
        g["conns"] = [c for c in g["conns"] if not c[2]]  # sans retenue recurrente
        self.assertEqual(preuve_aligne(g, 10)[0], "FAUX")
        g = circuit_main(10)
        g["act"][3] = "sig"
        self.assertEqual(preuve_aligne(g, 10)[0], "NON_PROUVABLE")

    def test_encodage_plat(self):
        lots = encode_plat([(12, 345), (99, 1)])
        tot = sum(len(l[3]) for l in lots)
        self.assertEqual(tot, 2)
        for X, Y, M, idx in lots:
            for j, i in enumerate(idx):
                a, b = [(12, 345), (99, 1)][i]
                cible = [int(c) for c in str(a + b).rjust(max(len(str(a)), len(str(b))) + 1, "0")]
                self.assertEqual(list(Y[j][M[j] > 0]), cible)

    def test_oracle_algo(self):
        rng = np.random.default_rng(0)
        for _ in range(200):
            a, b = int(rng.integers(0, 10 ** 9)), int(rng.integers(0, 10 ** 9))
            self.assertEqual(addition_listes(a, b, 10), str(a + b))
            self.assertEqual(addition_listes(a, b, 2), str(a + b))

    def test_mutations_valides_et_json(self):
        rng = np.random.default_rng(1)
        lots = encode_aligne(jeu_entrainement("X2-100", 1), 10)
        g = vide(2)
        for _ in range(3000):
            g2 = mute(g, rng)
            # connexions avant acycliques selon l'ordre
            pos = {u: k for k, u in enumerate(g2["cach"] + [2])}
            for s, d, r, n, q in g2["conns"]:
                self.assertNotEqual(n, 0)
                self.assertGreaterEqual(q, 1)
                if not r and s >= 2:
                    self.assertLess(pos[s], pos[d])
            evalue(g2, lots, 10)
            longueur_G(g2)
            self.assertEqual(cle(depuis_json(_jsonable(g2))), cle(g2))
            g = g2 if rng.random() < 0.7 else g
        self.assertEqual(cle(copie(g)), cle(g))

    def test_mdl_circuit_plus_court_que_par_coeur(self):
        # sanity : le circuit main a |D:G| = 0 et |G| raisonnable
        self.assertLess(longueur_G(circuit_main(10)), 200)


if __name__ == "__main__":
    unittest.main()
