import glob
import json
import os
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chemin_e002  # noqa: E402,F401

from diagnostic_sans_bruit import sans_bruit  # noqa: E402
from etalons import OracleProprietes  # noqa: E402
from etalons_bis import ETALONS_BIS, PlafondVerificateur, premisses  # noqa: E402
from evaluer import evaluer_monde  # noqa: E402
from evaluer_bis import acceleration_diff, evaluer_suite, r_diff, verdict_mesure  # noqa: E402
from interface import Environnement  # noqa: E402
from monde import generer_monde, regles_du_monde  # noqa: E402

GRAINES = range(1, 21)


class RDiffALaMain(unittest.TestCase):
    def test_r_diff(self):
        # R système −0.0603303 (exemple à la main d'E002) ; R plafond +0.0125
        # → R̂_diff = −0.0603303 − 0.0125 = −0.0728303 ; le quotient serait −4.83.
        self.assertAlmostEqual(r_diff(-0.0603303, 0.0125), -0.0728303, places=7)
        # Défini même quand le plafond vaut 0 ou est négatif (cas indéfini d'E002).
        self.assertAlmostEqual(r_diff(0.01, 0.0), 0.01)
        self.assertAlmostEqual(r_diff(-0.014, -0.003), -0.011)

    def test_acceleration(self):
        # gain 0.006 ≥ 0.005, hausses 3/4 → oui
        self.assertTrue(acceleration_diff([-0.010, -0.008, -0.009, -0.006, -0.004])["acceleration"])
        # 4 hausses mais gain 0.004 < 0.005 → non
        self.assertFalse(acceleration_diff([-0.010, -0.009, -0.008, -0.007, -0.006])["acceleration"])
        # gain 0.02 mais 2 hausses → non
        self.assertFalse(acceleration_diff([-0.03, -0.01, -0.02, -0.005, -0.01])["acceleration"])
        # plafond contre lui-même : R̂_diff ≡ 0 → non
        self.assertFalse(acceleration_diff([0.0] * 5)["acceleration"])

    def test_verdict_mesure(self):
        self.assertEqual(verdict_mesure([0.01] * 16 + [0.0, -0.01, 0.0, -0.1])["verdict"], "REPAREE")
        self.assertEqual(verdict_mesure([0.01] * 15 + [0.0] * 5)["verdict"], "NON_REPAREE")


class PlafondVerificateurProcessus(unittest.TestCase):
    def test_jamais_pire_sans_bruit(self):
        for g in GRAINES:
            m = sans_bruit(generer_monde(g))
            lo, _ = evaluer_monde(OracleProprietes(), m)
            lv, _ = evaluer_monde(PlafondVerificateur(), m)
            self.assertGreaterEqual(lv["bits_economises"], lo["bits_economises"] - 1e-9, g)
            self.assertEqual(lv["exactitude"], lo["exactitude"], g)

    def test_reponses_identiques_sans_bruit(self):
        for g in GRAINES:
            m = sans_bruit(generer_monde(g))
            reps = []
            for cls in (OracleProprietes, PlafondVerificateur):
                env, s = Environnement(m), cls()
                s.recevoir_proprietes(regles_du_monde(m))
                s.debut_monde(env.vue_publique())
                for p in (1, 2):
                    r = s.phase(p, env.ouvrir_phase(p), env.demander)
                reps.append(r)
            self.assertEqual(reps[0], reps[1], g)

    def test_toute_premisse_est_demandee(self):
        for g in GRAINES:
            m = generer_monde(g)
            env, s = Environnement(m), PlafondVerificateur()
            s.recevoir_proprietes(regles_du_monde(m))
            s.debut_monde(env.vue_publique())
            for p in (1, 2):
                reps = s.phase(p, env.ouvrir_phase(p), env.demander)
            demandes = {a for _, a, _ in env.requetes}
            self.assertTrue(premisses(reps) <= demandes, g)
            self.assertEqual(env.refus, [], g)

    def test_zero_deduit_faux_en_verite(self):
        for g in GRAINES:
            ligne, _ = evaluer_monde(PlafondVerificateur(), generer_monde(g))
            self.assertEqual(ligne["deduits_faux_en_verite"], 0, g)
            self.assertEqual(ligne["exactitude"], 1.0, g)


class Determinisme(unittest.TestCase):
    def test_deux_executions_identiques(self):
        g = [generer_monde(x) for x in (1, 6, 11, 16)]
        a = json.dumps(evaluer_suite(ETALONS_BIS, g), sort_keys=True, ensure_ascii=False)
        b = json.dumps(evaluer_suite(ETALONS_BIS, [generer_monde(x) for x in (1, 6, 11, 16)]),
                       sort_keys=True, ensure_ascii=False)
        self.assertEqual(a, b)

    def test_deux_processus_identiques(self):
        """Garantie entre processus, quel que soit PYTHONHASHSEED ambiant."""
        script = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evaluer_bis.py")
        sorties = []
        with tempfile.TemporaryDirectory() as d:
            for h in ("1", "2"):
                sub = os.path.join(d, h)
                subprocess.run([sys.executable, script, "--graines", "6-10", "--sortie", sub], check=True,
                               stdout=subprocess.DEVNULL, env=dict(os.environ, PYTHONHASHSEED=h))
                with open(glob.glob(os.path.join(sub, "*", "resultats.json"))[0], encoding="utf-8") as fh:
                    sorties.append(fh.read())
        self.assertEqual(sorties[0], sorties[1])


if __name__ == "__main__":
    unittest.main()
