"""E009-bis -- tests : flux avec curriculum, controles de curriculum et d'arret, reprise, verrous.

  python -m unittest -v test_e009bis
"""
import os
import shutil
import tempfile
import unittest
from unittest import mock

import mlx.core as mx

import curric as C
import entraine_bis as E

EX = C.d8.paires_exclues()
HP = {"lot": 32, "plafond_pas": 20, "lr_min": 1e-5, "montee": 4, "wd": 0.01,
      "betas": [0.9, 0.98], "clip": 1.0}


class TestFlux(unittest.TestCase):
    def test_niveau5_identique_au_flux_e008(self):
        for g, t in [(1, 0), (2, 17), (5, 19_999)]:
            self.assertEqual(C.paires_du_pas(g, t, EX, 5), C.d8.paires_du_pas(g, t, EX))

    def test_longueurs_bornees_par_le_niveau(self):
        for niv in (2, 3, 4):
            ls = [max(len(str(a)), len(str(b))) for t in range(20)
                  for a, b in C.paires_du_pas(1, t, EX, niv)]
            self.assertEqual(max(ls), niv)
            self.assertTrue(all(p not in EX for p in C.paires_du_pas(1, 3, EX, niv)))

    def test_niveau_au_pas_et_uniques(self):
        tr = [[500, 3], [1500, 4], [2000, 5]]
        self.assertEqual([C.niveau_au_pas(tr, p) for p in (0, 499, 500, 1999, 2000, 9999)],
                         [2, 2, 3, 4, 5, 5])
        _, c = C.uniques(1, 40, [[20, 5]], points=(20, 40), batch=64)
        self.assertLess(c[20], c[40])
        self.assertLess(c[40], 40 * 64 + 1)

    def test_fabrique_largeur(self):
        from archis import nb_parametres
        for s in ("A1", "A2-L", "A3", "A3-T"):
            self.assertLess(nb_parametres(C.fabrique(s, 64)), nb_parametres(C.fabrique(s, 128)))


class TestControles(unittest.TestCase):
    def _etat(self, niv, pas):
        return {"niveau": niv, "pas": pas, "transitions": []}

    def test_curriculum_monte_d_un_niveau_au_seuil(self):
        e = self._etat(2, 500)
        with mock.patch.object(C, "mesure", return_value={"T-ID|2": 0.90}) as m:
            E.controle_curriculum(None, "A1", e)
        self.assertEqual((e["niveau"], e["transitions"]), (3, [[500, 3]]))
        self.assertEqual(list(m.call_args[0][2]["T-ID"]), [2])  # longueurs 2..niveau
        e = self._etat(3, 1000)
        with mock.patch.object(C, "mesure", return_value={"a": 1.0, "b": 0.79}):
            E.controle_curriculum(None, "A1", e)
        self.assertEqual((e["niveau"], e["transitions"]), (3, []))

    def test_arret_seulement_a_95(self):
        tmp = tempfile.mkdtemp()
        try:
            modele = C.fabrique("A1", 16)
            e = self._etat(5, 1000)
            with mock.patch.object(C, "mesure", return_value={"a": 0.95, "b": 0.94}):
                self.assertFalse(E.controle_arret(modele, "A1", e, tmp))
            with mock.patch.object(C, "mesure", return_value={"a": 0.95, "b": 0.95}) as m:
                self.assertTrue(E.controle_arret(modele, "A1", e, tmp))
            self.assertEqual(sorted(m.call_args[0][2]["T-ID"]), [2, 3, 4, 5])
            self.assertEqual(len(m.call_args[0][2]["T-ID"][5]), 200)
            self.assertTrue(e["appris"] and e["pas_appris"] == 1000)
            self.assertTrue(os.path.exists(os.path.join(tmp, "meilleur.safetensors")))
        finally:
            shutil.rmtree(tmp)


class TestEntrainement(unittest.TestCase):
    def test_reprise_equivaut_a_un_trait(self):
        tmp = tempfile.mkdtemp()
        try:
            for s in ("A2-L", "A3"):
                d1, d2 = os.path.join(tmp, s + "1"), os.path.join(tmp, s + "2")
                kw = dict(log=lambda *_: None, avec_controles=False)
                E.entrainer(s, 7, 32, 1e-3, d1, HP, 1e9, 12, **kw)
                E.entrainer(s, 7, 32, 1e-3, d2, HP, 1e9, 5, **kw)
                e = C.b9.lire_json(os.path.join(d2, "etat.json"))
                e["fini"], e["pas_max"] = False, 12
                C.b9.ecrire_json(e, os.path.join(d2, "etat.json"))
                e = E.entrainer(s, 7, 32, 1e-3, d2, HP, 1e9, 12, **kw)
                self.assertEqual((e["pas"], e["invocations"], e["fini"]), (12, 2, True))
                w1 = mx.load(os.path.join(d1, "poids.safetensors"))
                w2 = mx.load(os.path.join(d2, "poids.safetensors"))
                self.assertLess(max(float(mx.abs(w1[k] - w2[k]).max()) for k in w1), 1e-3, s)
        finally:
            shutil.rmtree(tmp)

    def test_curriculum_en_boucle_et_arret(self):
        """Controles branches dans la boucle : niveau monte, puis arret a 95 % (mesure simulee)."""
        tmp = tempfile.mkdtemp()
        try:
            vals = iter([{"x": 0.95}, {"x": 0.95}, {"x": 0.95}, {"x": 0.5}, {"x": 0.99}])
            niveaux, vrai_lot = [], C.lot

            def lot_espion(g, pas, ex, lmax, *a):
                niveaux.append(lmax)
                return vrai_lot(g, pas, ex, lmax, *a)
            with mock.patch.object(C, "PERIODE_CURR", 2), \
                    mock.patch.object(C, "PERIODE_ARRET", 4), \
                    mock.patch.object(C, "lot", side_effect=lot_espion), \
                    mock.patch.object(C, "mesure", side_effect=lambda *a: next(vals)):
                e = E.entrainer("A1", 3, 16, 1e-3, tmp, HP, 1e9, 20, log=lambda *_: None)
            self.assertEqual(niveaux, [2, 2, 3, 3, 4, 4] + [5] * 6)  # le flux suit le niveau
            self.assertEqual(e["transitions"], [[2, 3], [4, 4], [6, 5]])
            # pas 8 : arret a 0.5 (non) ; pas 12 : 0.99 -> appris
            self.assertEqual((e["appris"], e["pas_appris"], e["pas"], e["fini"]), (True, 12, 12, True))
        finally:
            shutil.rmtree(tmp)


class TestVerrous(unittest.TestCase):
    def test_eval_refusee_si_non_appris(self):
        import subprocess
        import sys
        tmp = os.path.join(E.ICI, "runs", "_test-nonappris")
        os.makedirs(tmp, exist_ok=True)
        try:
            C.b9.ecrire_json({"fini": True, "appris": False, "graine": 1, "pas": 20000,
                              "systeme": "A1", "w": 16}, os.path.join(tmp, "etat.json"))
            for ph in ("val", "final"):
                r = subprocess.run([sys.executable, "evalue_bis.py", "--run", "_test-nonappris",
                                    "--phase", ph], cwd=E.ICI, capture_output=True, text=True)
                self.assertIn("distribution non apprise", r.stderr + r.stdout)
        finally:
            shutil.rmtree(tmp)


if __name__ == "__main__":
    unittest.main()
