"""E009 -- tests : bande, jeux, disjonction, C-BANDE, pertes, arret, reprise.

  python -m unittest -v test_e009
"""
import os
import shutil
import tempfile
import unittest

import mlx.core as mx
import mlx.nn as nn
import numpy as np

from archis import M_ENTRAINEMENT, SYSTEMES, norme_spectrale
from bande import (EGAL, FIN, PAD, PLUS, SLOT, bande_entree, bandes, cible_cases, d8,
                   decode_cases, jeux_final, jeux_id, jeux_val, lot)
from boucle import perte_progressive, perte_tn, predire, tirage_progressif
from controles import systeme_oracle  # E008
from evaluate import evaluer, resume  # E008
from evalue import systeme_appris

EX = d8.paires_exclues()


class FauxModele:
    """Renvoie la bande cible exacte (decalee de `decalage` cases) : sert a C-BANDE."""

    def __init__(self, inverse, decalage=0):
        self.inverse, self.decalage = inverse, decalage

    def etat0(self, x):
        return x[..., None].astype(mx.float32), None

    def iterer(self, h, ctx):
        return h

    def lire(self, h):
        xs = np.array(h)[..., 0].astype(np.int64)
        B, L = xs.shape
        n = L // 2
        out = np.full((B, L, 15), -20.0, dtype=np.float32)
        for i in range(B):
            toks = list(xs[i, :n])
            p = toks.index(PLUS)
            a = int("".join(map(str, toks[:p])))
            b = int("".join(map(str, toks[p + 1: n - 1])))
            cib = cible_cases(a, b, self.inverse)
            cib = cib[self.decalage:] + [PAD] * self.decalage if self.decalage else cib
            for j, t in enumerate(cib):
                out[i, n + j, t] = 20.0
        return mx.array(out)


class TestBande(unittest.TestCase):
    def test_format(self):
        self.assertEqual(bande_entree(12, 345), [1, 2, PLUS, 3, 4, 5, EGAL] + [SLOT] * 7)
        self.assertEqual(cible_cases(12, 345, True), [7, 5, 3, FIN, PAD, PAD, PAD])
        self.assertEqual(cible_cases(12, 345, False), [3, 5, 7, FIN, PAD, PAD, PAD])
        self.assertEqual(cible_cases(9, 1, True), [0, 1, FIN, PAD])

    def test_lot_suit_le_flux_e008(self):
        for g, t in [(1, 0), (2, 17), (5, 5999)]:
            x, y, m, t_n = lot(g, t, EX, True)
            paires = d8.paires_du_pas(g, t, EX, 256)
            for i in (0, 100, 255):
                a, b = paires[i]
                n = len(d8.encode_prompt(a, b))
                self.assertEqual(list(x[i, :2 * n]), bande_entree(a, b))
                self.assertTrue((x[i, 2 * n:] == PAD).all())
                self.assertEqual(list(y[i, n:2 * n]), cible_cases(a, b, True))
                self.assertEqual(m[i].sum(), n)
                self.assertEqual(m[i, :n].sum(), 0)
                self.assertEqual(t_n[i], max(len(str(a)), len(str(b))) + 1)
            self.assertLessEqual(x.shape[1], 24)

    def test_decodage(self):
        self.assertEqual(decode_cases([7, 5, 3, FIN, PAD], np.ones(5), True), ("357", 1.0))
        self.assertEqual(decode_cases([3, 5, 7, FIN, 5], [0.5] * 5, False), ("357", 0.5 ** 4))
        self.assertEqual(decode_cases([3, 5, 7, 7], [1] * 4, False)[0], None)
        self.assertEqual(decode_cases([3, SLOT, FIN], [1] * 3, False)[0], "3_")


class TestJeux(unittest.TestCase):
    def setUp(self):
        self.jeux = {**jeux_val(), **jeux_final(), **jeux_id()}

    def test_tailles_et_unicite(self):
        for nom, attendu in [("VAL", 300), ("TEST", 200), ("ADV-RET", 102), ("ADV-ZERO", 101),
                             ("ADV-ASYM", 50), ("T-ID", 200)]:
            for L, items in self.jeux[nom].items():
                self.assertEqual(len(items), attendu, (nom, L))
                self.assertEqual(len(set(items)), len(items), (nom, L))

    def test_longueurs(self):
        for nom in ("VAL", "TEST", "ADV-RET", "ADV-ZERO"):
            for L, items in self.jeux[nom].items():
                for a, b in items:
                    if nom == "ADV-RET" and 1 in (a, b):
                        self.assertEqual(max(a, b), int("9" * L))
                        continue
                    self.assertEqual((len(str(a)), len(str(b))), (L, L))
        for k, items in self.jeux["ADV-ASYM"].items():
            la, lb = map(int, k.split("+"))
            for a, b in items:
                self.assertEqual((len(str(a)), len(str(b))), (la, lb))

    def test_adverses(self):
        for L, items in self.jeux["ADV-RET"].items():
            self.assertTrue(all(d8.chaine_retenue(a, b) == L for a, b in items))
        for L, items in self.jeux["ADV-ZERO"].items():
            self.assertEqual(items[0], (10 ** (L - 1) + 2, 10 ** (L - 1) + 3))
            zeros = sum(str(a)[1:].count("0") for a, _ in items[1:]) / (100 * (L - 1))
            self.assertGreater(zeros, 0.85)

    def test_disjonction_entrainement(self):
        """Les jeux nouveaux ont un operande >= 6 chiffres ; le flux n'en tire jamais."""
        for nom in ("VAL", "TEST", "ADV-RET", "ADV-ZERO", "ADV-ASYM"):
            for items in self.jeux[nom].values():
                self.assertTrue(all(max(len(str(a)), len(str(b))) >= 6 for a, b in items))
        for g in (1, 2, 3, 4, 5):
            for t in list(range(0, 50)) + [5999]:
                for a, b in d8.paires_du_pas(g, t, EX, 256):
                    self.assertLessEqual(max(len(str(a)), len(str(b))), 5)

    def test_oracle(self):
        r = resume(evaluer(systeme_oracle, self.jeux, "C-ORACLE"))["par_jeu"]
        self.assertTrue(all(c["exact"] == 1.0 for c in r.values()))


class TestCBande(unittest.TestCase):
    """C-BANDE : cible exacte -> 100 % ; cible decalee d'une case -> ~0 %."""

    def _exact(self, modele, regle, inverse):
        jeux = {"VAL": {6: jeux_val()["VAL"][6][:50]},
                "ADV-ASYM": {k: v[:10] for k, v in jeux_final()["ADV-ASYM"].items()
                             if k in ("100+3", "1+64")}}
        r = resume(evaluer(systeme_appris(modele, regle, inverse, plafond=3), jeux, "f"))
        return [c["exact"] for c in r["par_jeu"].values()]

    def test_parfait(self):
        for inverse in (True, False):
            for regle in ("bande", "confiance", "t_n"):
                self.assertEqual(self._exact(FauxModele(inverse), regle, inverse), [1.0] * 3)

    def test_decale(self):
        for inverse in (True, False):
            self.assertTrue(all(v <= 0.05 for v in
                                self._exact(FauxModele(inverse, 1), "confiance", inverse)))

    def test_mauvais_format(self):
        """Une bande standard lue comme inversee echoue (le format compte)."""
        self.assertTrue(all(v <= 0.2 for v in self._exact(FauxModele(False), "bande", True)))


class Compteur(nn.Module):
    """iterer ajoute 1 : l'etat au tour t vaut t."""

    def etat0(self, x):
        return mx.zeros((x.shape[0], x.shape[1], 1)), None

    def iterer(self, h, ctx):
        return h + 1

    def lire(self, h):
        return -((mx.arange(15) - h) ** 2)  # argmax = numero du tour


class TestBoucle(unittest.TestCase):
    def test_tirage_progressif(self):
        for g in (0, 1, 5):
            for t in range(300):
                n, k = tirage_progressif(g, t)
                self.assertTrue(0 <= n < M_ENTRAINEMENT and 1 <= k <= M_ENTRAINEMENT - n)

    def test_t_n_selectionne_le_bon_tour(self):
        x = mx.zeros((3, 8), dtype=mx.int32)
        tok, pm, T = predire(Compteur(), "t_n", np.zeros((3, 8), np.int32), [2, 5, 3])
        self.assertEqual(list(T), [2, 5, 3])
        self.assertEqual([list(r) for r in tok], [[2] * 4, [5] * 4, [3] * 4])
        tok, _, T = predire(Compteur(), "bande", np.zeros((2, 10), np.int32), None)
        self.assertEqual((list(T), tok[0, 0], tok[1, 4]), ([10, 10], 10, 10))
        seen = []
        import boucle
        old = boucle.ce
        boucle.ce = lambda logits, y, m: mx.argmax(logits[:, 0, :], axis=-1)
        try:
            v = perte_tn(Compteur(), x, None, None, mx.array([2, 5, 3]), 5)
            seen = list(np.array(v))
        finally:
            boucle.ce = old
        self.assertEqual(seen, [2, 5, 3])

    def test_arret_confiance_max_et_plafond(self):
        class Pic(Compteur):  # confiance maximale au tour 4
            def lire(self, h):
                return mx.concatenate([8 - 2 * mx.abs(h - 4)] + [mx.zeros_like(h)] * 14, -1)
        x0 = np.zeros((2, 8), np.int32)
        self.assertEqual(list(predire(Pic(), "confiance", x0, None, plafond=9)[2]), [4, 4])
        self.assertEqual(list(predire(Pic(), "confiance", x0, None, plafond=3)[2]), [3, 3])
        self.assertEqual(list(predire(Pic(), "confiance", x0, None, plafond=9)[0][0]), [0] * 4)

    def test_pertes_finies_et_gradients(self):
        x, y, m, t_n = (mx.array(v) for v in lot(1, 0, EX, True, 16))
        for s, d in SYSTEMES.items():
            mo = d["fabrique"]()
            fn = {"bande": lambda mo_: __import__("boucle").perte_bande(mo_, x, y, m),
                  "confiance": lambda mo_: perte_progressive(mo_, x, y, m, 3, 4),
                  "t_n": lambda mo_: perte_tn(mo_, x, y, m, t_n, int(t_n.max().item()))}[d["regle"]]
            l, g = nn.value_and_grad(mo, fn)(mo)
            from mlx.utils import tree_flatten
            gn = sum(float((v * v).sum()) for _, v in tree_flatten(g))
            self.assertTrue(np.isfinite(l.item()) and 0 < gn < 1e6, s)

    def test_norme_spectrale(self):
        w = nn.Conv1d(128, 128, 3).weight * 3
        vrai = np.linalg.norm(np.array(w).reshape(128, -1), 2)
        self.assertAlmostEqual(float(norme_spectrale(w)) / vrai, 1.0, delta=0.06)


class TestReprise(unittest.TestCase):
    def test_reprise_equivaut_a_un_trait(self):
        from entraine import entrainer
        hp = {"lot": 32, "pas": 12, "lr_max": 1e-3, "lr_min": 1e-5, "montee": 4, "wd": 0.01,
              "betas": [0.9, 0.98], "clip": 1.0}
        tmp = tempfile.mkdtemp()
        try:
            for s in ("A2-L", "A3-T"):
                d1, d2 = os.path.join(tmp, s + "1"), os.path.join(tmp, s + "2")
                entrainer(s, 7, "inv", d1, hp, 1e9, log=lambda *_: None, avec_jalons=False)
                entrainer(s, 7, "inv", d2, hp, 1e9, log=lambda *_: None, avec_jalons=False,
                          arret_pas=5)
                e = entrainer(s, 7, "inv", d2, hp, 1e9, log=lambda *_: None, avec_jalons=False)
                self.assertEqual((e["pas"], e["invocations"], e["fini"]), (12, 2, True))
                w1 = mx.load(os.path.join(d1, "poids.safetensors"))
                w2 = mx.load(os.path.join(d2, "poids.safetensors"))
                ecart = max(float(mx.abs(w1[k] - w2[k]).max()) for k in w1)
                self.assertLess(ecart, 1e-3, s)  # GPU MLX non deterministe au bit (E008)
                d3 = os.path.join(tmp, s + "3")  # controle negatif : autre graine
                entrainer(s, 8, "inv", d3, hp, 1e9, log=lambda *_: None, avec_jalons=False)
                w3 = mx.load(os.path.join(d3, "poids.safetensors"))
                self.assertGreater(max(float(mx.abs(w1[k] - w3[k]).max()) for k in w1), 1e-2)
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
