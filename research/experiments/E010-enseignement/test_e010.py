"""E010 -- tests unitaires.   python -m unittest -v test_e010"""
import random
import unittest

import numpy as np

import donnees as D
from data import chaine_retenue  # E008


class TestFormats(unittest.TestCase):
    def test_longueurs_entrainement(self):
        self.assertEqual({f: D.seq_train(f) for f in D.FORMATS},
                         {"F0": 18, "F1": 49, "F2": 34, "F3": 49})
        self.assertEqual(D.VOCAB, 30)
        self.assertEqual(len(D.REGLE), 16)

    def test_oracle_trace_relu(self):
        rnd = random.Random(0)
        paires = [(99999, 1), (1, 99999), (0, 0), (5, 5), (10 ** 99, 7), (123, 98765)]
        paires += [(rnd.randrange(10 ** rnd.randint(1, 40)), rnd.randrange(10 ** rnd.randint(1, 40)))
                   for _ in range(300)]
        for a, b in paires:
            for f in D.FORMATS:
                self.assertEqual(D.lit_sortie(D.cible(a, b, f), f)[0], str(a + b), (a, b, f))

    def test_trace_sans_position(self):
        tr = D.trace(47, 385)  # colonnes : 7+5, 4+8+1, 0+3+1
        self.assertEqual(tr, [7, 5, 0, 2, 1, D.SEP, 4, 8, 1, 3, 1, D.SEP, 0, 3, 1, 4, 0, D.SEP])
        self.assertTrue(all(t <= D.SEP for t in tr))

    def test_lit_sortie_invalide(self):
        self.assertEqual(D.lit_sortie([1, 2, 3], "F0")[0], None)          # pas de fin
        self.assertEqual(D.lit_sortie([1, D.FIN], "F1")[0], None)         # pas de #
        self.assertEqual(D.lit_sortie([D.FIN], "F0")[0], None)            # reponse vide
        self.assertEqual(D.lit_sortie([1, D.PLUS, D.FIN], "F0")[0], None) # symbole
        self.assertEqual(D.lit_sortie([3, 2, 1, D.FIN], "F0")[0], "321")

    def test_generation_suffisante(self):
        for a, b in [(10 ** 99, 10 ** 99), (int("9" * 100), 1), (123, int("9" * 64))]:
            for f in D.FORMATS:
                self.assertLessEqual(len(D.cible(a, b, f)),
                                     D.n_gen_max(len(str(a)), len(str(b)), f))


class TestReserve(unittest.TestCase):
    def test_emboitee_unique_disjointe(self):
        D._CACHE.clear()
        petite = D.reserve(1, 1000)
        D._CACHE.clear()
        grande = D.reserve(1, 20_000)
        self.assertEqual(petite, grande[:1000])
        self.assertEqual(len(set(grande)), len(grande))
        ex = D.paires_exclues()
        self.assertFalse(any(p in ex for p in grande))
        self.assertTrue(all(1 <= len(str(a)) <= 5 and 1 <= len(str(b)) <= 5 for a, b in grande))

    def test_epoques(self):
        vus = []
        for pas in range(4):
            vus += D.indices_du_pas(1, 1000, pas)
        self.assertEqual(sorted(vus[:1000]), list(range(1000)))
        self.assertEqual(D.uniques_vus(1000, 1500), 1000)
        self.assertEqual(D.uniques_vus(384_000, 1500), 384_000)

    def test_lot_masque(self):
        for f in D.FORMATS:
            x, y, m = D.lot(2, 1000, 3, f, batch=8)
            paires = D.paires_du_pas(2, 1000, 3, batch=8)
            for i, (a, b) in enumerate(paires):
                self.assertEqual(y[i][m[i] == 1].tolist(), D.cible(a, b, f))

    def test_jeux_disjoints_et_adverses(self):
        j = D.jeux_e010(final=True)
        table = set(D.reserve(1, 50_000))
        for nom in ("T-ID", "V-OOD", "T-FIN", "ADV-CASCADE", "ADV-ZEROS", "ADV-ASYM"):
            for L, items in j[nom].items():
                self.assertFalse(any(p in table or p[::-1] in table for p in items), (nom, L))
                self.assertEqual(len(set(items)), len(items))
        for L, items in j["ADV-CASCADE"].items():
            for a, b in items:
                self.assertEqual(len(str(a + b)), L + 1)
                self.assertGreaterEqual(chaine_retenue(a, b), L - 3)
        for L, items in j["ADV-ASYM"].items():
            for a, b in items:
                self.assertEqual(sorted((len(str(a)), len(str(b)))), [3, L])
        self.assertIn((10 ** 9 + 2, 10 ** 9 + 3), j["ADV-ZEROS"][10])
        self.assertEqual([len(j["T-FIN"][L]) for L in D.FIN_LENS], [200] * 5)


class TestModele(unittest.TestCase):
    def test_cache_egal_sans_cache(self):
        import mlx.core as mx
        from modele import Additionneur, Cache
        for pos in (True, False):
            mx.random.seed(0)
            m = Additionneur(positions=pos)
            m.eval()
            seq = mx.array(np.random.default_rng(0).integers(0, 16, (3, 300)).astype(np.int32))
            plein = m(seq)
            caches = [Cache() for _ in m.blocs]
            morceaux = [m(seq[:, :40], caches, 0)]
            for t in range(40, 300):
                morceaux.append(m(seq[:, t:t + 1], caches, t))
            inc = mx.concatenate(morceaux, axis=1)
            self.assertLess(float(mx.abs(inc - plein).max()), 1e-3, pos)


if __name__ == "__main__":
    unittest.main()
