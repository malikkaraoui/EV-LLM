"""E008 -- tests (unittest).  python -m unittest -v test_e008"""
import os
import shutil
import tempfile
import unittest
from collections import Counter

import numpy as np

import data
from controles import addition_retenue, systeme_oracle, systeme_parcoeur, table_parcoeur, cle
from evaluate import evaluer, resume, systeme_modele


class TestGenerateur(unittest.TestCase):
    def test_equilibre_par_longueur(self):
        ex = data.paires_exclues()
        la, lb = Counter(), Counter()
        for t in range(200):
            for a, b in data.paires_du_pas(1, t, ex):
                la[len(str(a))] += 1
                lb[len(str(b))] += 1
        n = 200 * data.BATCH
        for c in (la, lb):
            self.assertEqual(sorted(c), [1, 2, 3, 4, 5])
            for k in c:
                self.assertAlmostEqual(c[k] / n, 0.2, delta=0.01)

    def test_premier_chiffre(self):
        rng = np.random.default_rng(0)
        for lg in range(1, 17):
            for _ in range(200):
                self.assertEqual(len(str(data.tire_nombre(rng, lg))), lg)

    def test_deterministe_et_reprise(self):
        ex = data.paires_exclues()
        self.assertEqual(data.paires_du_pas(2, 77, ex), data.paires_du_pas(2, 77, ex))
        self.assertNotEqual(data.paires_du_pas(2, 77, ex), data.paires_du_pas(3, 77, ex))

    def test_lot_masque(self):
        x, y, m = data.lot(1, 0, data.paires_exclues(), inverse=False, batch=8)
        for i in range(8):
            cibles = [data.CARS[t] for t, k in zip(y[i], m[i]) if k]
            entree = "".join(data.CARS[t] for t in x[i] if t != data.PAD)
            a, b = entree.split("=")[0].split("+")
            self.assertEqual("".join(cibles), str(int(a) + int(b)) + "$")
        x, y, m = data.lot(1, 0, data.paires_exclues(), inverse=True, batch=8)
        for i in range(8):
            cibles = "".join(data.CARS[t] for t, k in zip(y[i], m[i]) if k)
            entree = "".join(data.CARS[t] for t in x[i] if t != data.PAD)
            a, b = entree.split("=")[0].split("+")
            self.assertEqual(cibles, str(int(a) + int(b))[::-1] + "$")


class TestJeux(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.jeux = data.jeux_de_test()

    def test_tailles_et_longueurs(self):
        j = self.jeux
        self.assertEqual(len(j["T-ID1"][1]), 100)
        for nom, lens, n in (("T-ID", data.ID_LENS, 500), ("T-OOD", data.OOD_LENS, 500)):
            self.assertEqual(sorted(j[nom]), lens)
            for L in lens:
                self.assertEqual(len(set(j[nom][L])), n)
                for a, b in j[nom][L]:
                    self.assertEqual((len(str(a)), len(str(b))), (L, L))
        for L in data.CARRY_LENS:
            self.assertEqual(len(set(j["T-CARRY"][L])), 502)

    def test_disjonction_id_entrainement(self):
        """Aucune paire de test (T-ID, T-OOD, T-CARRY), dans un ordre ou l'autre, dans le flux."""
        ex = data.paires_exclues(self.jeux)
        test = set()
        for nom in ("T-ID", "T-OOD", "T-CARRY"):
            for items in self.jeux[nom].values():
                for a, b in items:
                    test.add((a, b))
                    test.add((b, a))
        self.assertEqual(ex, test)
        for g in (1, 2, 3):
            for t in list(range(300)) + [19_999]:
                for a, b in data.paires_du_pas(g, t, ex):
                    self.assertNotIn((a, b), test)

    def test_exclusion_mordante(self):
        """L'exclusion retire vraiment quelque chose : sans elle, des paires T-ID apparaissent."""
        tid = {p for items in self.jeux["T-ID"].values() for p in items if len(str(p[0])) == 2}
        vus = set()
        for t in range(400):
            vus.update(data.paires_du_pas(1, t, set()))
        self.assertTrue(tid & vus)

    def test_hard_carry(self):
        for L, items in self.jeux["T-CARRY"].items():
            for a, b in items[:-2]:
                self.assertEqual(data.chaine_retenue(a, b), L)
                self.assertEqual(len(str(a + b)), L + 1)
            neuf = int("9" * L)
            self.assertEqual(items[-2:], [(neuf, 1), (1, neuf)])
            self.assertEqual(data.chaine_retenue(neuf, 1), L)

    def test_chaine_retenue(self):
        self.assertEqual(data.chaine_retenue(0, 0), 0)
        self.assertEqual(data.chaine_retenue(5, 5), 1)
        self.assertEqual(data.chaine_retenue(19, 81), 2)
        self.assertEqual(data.chaine_retenue(909, 191), 3)
        self.assertEqual(data.chaine_retenue(505, 505), 1)


class TestControles(unittest.TestCase):
    def test_oracle_100(self):
        jeux = data.jeux_de_test()
        r = resume(evaluer(systeme_oracle, jeux, "C-ORACLE"))
        for k, c in r["par_jeu"].items():
            self.assertEqual(c["exact"], 1.0, k)

    def test_addition_retenue_aleatoire(self):
        rng = np.random.default_rng(5)
        for _ in range(5000):
            a, b = (data.tire_nombre(rng, int(rng.integers(1, 20))) for _ in range(2))
            self.assertEqual(addition_retenue(a, b), str(a + b))

    def test_parcoeur(self):
        table = table_parcoeur(1, 50, 64)
        vus = data.paires_du_pas(1, 3, data.paires_exclues(), 64)
        r = systeme_parcoeur(table)(vus + [(123456, 654321)])
        self.assertTrue(all(x[0] == str(a + b) for x, (a, b) in zip(r, vus)))
        self.assertIsNone(r[-1][0])
        self.assertIn(cle(*vus[0]), table)


class TestEvaluateur(unittest.TestCase):
    def test_exact_match(self):
        jeux = {"X": {3: [(100, 20), (999, 1), (5, 5), (12, 30)]}}
        rep = [("120", 0.9), ("01000", 0.99), (None, 0.95), ("42", 0.1)]
        recs = evaluer(lambda p: rep, jeux, "faux")
        self.assertEqual([r["juste"] for r in recs], [True, False, False, True])
        c = resume(recs)["par_jeu"]["X|3"]
        self.assertEqual((c["justes"], c["faux"], c["faux_surs"]), (2, 2, 2))

    def _modele_parfait(self, inverse):
        """Faux modele MLX : predit toujours le bon token suivant (teste decodage/inversion)."""
        import mlx.core as mx

        def f(x):
            xs = np.array(x)
            B, T = xs.shape
            logits = np.full((B, T, data.VOCAB), -10.0, dtype=np.float32)
            for i in range(B):
                s = "".join(data.CARS[t] for t in xs[i])
                gauche, gen = s.split("=")
                a, b = gauche.split("+")
                cible = data.reponse(int(a), int(b), inverse) + "$"
                c = cible[len(gen)] if len(gen) < len(cible) else "$"  # deja fini
                logits[i, -1, data.CARS.index(c)] = 10.0
            return mx.array(logits)
        return f

    def test_decodage_modele(self):
        jeux = {"X": {2: [(12, 34), (99, 1), (1, 99), (50, 50)], 6: [(123456, 999999)]}}
        for inverse in (False, True):
            recs = evaluer(systeme_modele(self._modele_parfait(inverse), inverse), jeux, "p")
            self.assertTrue(all(r["juste"] for r in recs), inverse)
            self.assertTrue(all(r["conf"] > 0.99 for r in recs))
        # mauvais sens d'inversion -> faux sur les sommes non palindromes
        recs = evaluer(systeme_modele(self._modele_parfait(True), False), jeux, "p")
        self.assertFalse(recs[0]["juste"])


class TestDeterminisme(unittest.TestCase):
    HP = {"lot": 32, "pas": 20, "lr_max": 1e-3, "lr_min": 1e-5, "montee": 5, "wd": 0.01,
          "betas": [0.9, 0.98], "clip": 1.0, "jalons": []}
    KW = {"d": 32, "couches": 1, "tetes": 2, "ffn": 64}

    def _poids(self, dossier):
        import mlx.core as mx
        return {k: np.array(v) for k, v in mx.load(os.path.join(dossier, "poids.safetensors")).items()}

    def test_deux_executions_et_reprise(self):
        from train import entrainer
        tmp = tempfile.mkdtemp()
        try:
            for systeme in ("B-STD", "B-REF"):
                d1, d2, d3 = (os.path.join(tmp, f"{systeme}-{i}") for i in range(3))
                q = lambda *a, **k: None
                entrainer(systeme, 7, d1, self.HP, 1e9, jalons=False, modele_kw=self.KW, log=q)
                entrainer(systeme, 7, d2, self.HP, 1e9, jalons=False, modele_kw=self.KW, log=q)
                hp10 = dict(self.HP)
                # reprise : 10 pas, arret, puis 10 pas -- meme resultat que 20 d'un trait
                import train
                orig = train.time.time
                compteur = {"n": 0}

                def horloge():
                    compteur["n"] += 1
                    return 0.0 if compteur["n"] <= 11 else 1e12
                train.time.time = horloge
                try:
                    e = entrainer(systeme, 7, d3, hp10, 1.0, jalons=False, modele_kw=self.KW, log=q)
                finally:
                    train.time.time = orig
                self.assertEqual(e["pas"], 10)
                e = entrainer(systeme, 7, d3, hp10, 1e9, jalons=False, modele_kw=self.KW, log=q)
                self.assertEqual(e["pas"], 20)
                p1, p2, p3 = self._poids(d1), self._poids(d2), self._poids(d3)
                # [VERIFIE 26/09] le GPU MLX n'est pas bit-a-bit reproductible (ecarts ~3e-8
                # apres 20 pas) : determinisme exige a 1e-6 pres, pas au bit.
                for k in p1:
                    np.testing.assert_allclose(p1[k], p2[k], rtol=0, atol=1e-6)
                    np.testing.assert_allclose(p1[k], p3[k], rtol=0, atol=1e-6)
                # et la graine compte vraiment
                d4 = os.path.join(tmp, f"{systeme}-autre")
                entrainer(systeme, 8, d4, self.HP, 1e9, jalons=False, modele_kw=self.KW, log=q)
                p4 = self._poids(d4)
                self.assertTrue(any(np.abs(p1[k] - p4[k]).max() > 1e-3 for k in p1))
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
