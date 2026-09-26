import glob
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ICI)

import chemin  # noqa: E402,F401

from a0bis import A0Bis  # noqa: E402
from acquereur_oracle import (OracleAcquereur, OracleAmnesique, OracleExact, connaissance,  # noqa: E402
                              enregistrer_mondes, placer, regles_vraies)
from evaluer import evaluer_monde  # noqa: E402
from evaluer_oracle import verdict_mission1  # noqa: E402
from monde import generer_monde  # noqa: E402

NOM = re.compile(r"\bR\d\b|\bo\d{3}\b")
MONDES = {}


def monde(g):
    if g not in MONDES:
        MONDES[g] = generer_monde(g)
        enregistrer_mondes([MONDES[g]])
    return MONDES[g]


def _suite(systeme, graines):
    lignes = []
    for g in graines:
        l, corr = evaluer_monde(systeme, monde(g))
        systeme.fin_monde(corr)
        lignes.append(l)
    return systeme, lignes


def _sans_crues(l):
    return {k: v for k, v in l.items() if k != "proprietes_crues"}


class Espion(OracleAcquereur):
    """Journalise, à chaque phase, ce que l'oracle sait (sans rien changer)."""
    nom = "espion"

    def __init__(self):
        super().__init__()
        self.vu = []
        self.utilisees_vues = []

    def phase(self, p, observations, demander):
        reps = super().phase(p, observations, demander)
        self.vu.append((_monde_graine(self), p, self.regles_oracle is not None, sorted(self.connaissances)))
        self.utilisees_vues.append((_monde_graine(self), list(self.utilisees), self.regles_oracle))
        return reps


def _monde_graine(s):
    from acquereur_oracle import _monde
    return _monde(s.vue)["graine"]


class Temporalite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.espion, cls.lignes = _suite(Espion(), [1, 2, 6])

    def test_rien_pendant_le_premier_monde(self):
        g1 = [v for v in self.espion.vu if v[0] == 1]
        self.assertEqual([(p, o, k) for _, p, o, k in g1], [(1, False, []), (2, False, [])])

    def test_connaissance_apres_le_premier_monde(self):
        g2 = [v for v in self.espion.vu if v[0] == 2]
        self.assertEqual([(p, o, k) for _, p, o, k in g2], [(1, True, [0]), (2, True, [0])])

    def test_nouvelle_famille_sans_connaissance(self):
        g6 = [v for v in self.espion.vu if v[0] == 6]
        self.assertEqual([(p, o, k) for _, p, o, k in g6], [(1, False, [0]), (2, False, [0])])
        self.assertEqual(sorted(self.espion.connaissances), [0, 1])

    def test_canal_journalise(self):
        self.assertEqual(self.espion.acces_canal, [("fin_monde", 1, True), ("debut_monde", 2, True),
                                                    ("fin_monde", 2, True), ("debut_monde", 6, False),
                                                    ("fin_monde", 6, True)])

    def test_regles_utilisees_sont_celles_de_l_oracle(self):
        for g, utilisees, oracle in self.espion.utilisees_vues:
            if g == 2:
                self.assertEqual(utilisees, oracle)
            else:
                self.assertIsNone(oracle)

    def test_regles_oracle_utilisees_sans_test(self):
        self.assertEqual(self.lignes[1]["proprietes_crues"]["regles_oracle"], 5)   # g2 : 4 propriétés + 1 composition
        self.assertIsNone(self.lignes[0]["proprietes_crues"]["regles_oracle"])


class EgalA0BisAuPremierMonde(unittest.TestCase):
    def test_graine_1(self):
        _, lo = _suite(OracleAcquereur(), [1])
        _, lb = _suite(A0Bis(), [1])
        self.assertEqual(_sans_crues(lo[0]), _sans_crues(lb[0]))


class ConnaissanceDuPremierMonde(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.acq, cls.la = _suite(OracleAcquereur(), [1, 2, 3, 4])
        cls.exa, cls.le = _suite(OracleExact(), [1, 2, 3, 4])

    def test_graine_4_regles_du_premier_monde(self):
        self.assertFalse(any(r[0] == "reflexive" for r in self.acq.regles_oracle))
        self.assertTrue(any(r[0] == "reflexive" for r in self.exa.regles_oracle))
        self.assertEqual(self.exa.regles_oracle, regles_vraies(monde(4)))
        self.assertNotEqual(self.acq.regles_oracle, self.exa.regles_oracle)

    def test_egalite_a_la_verite_hors_graine_4(self):
        self.assertEqual([l["proprietes_crues"]["k_egale_verite"] for l in self.la], [None, True, True, False])
        self.assertEqual([l["proprietes_crues"]["k_egale_verite"] for l in self.le], [None, True, True, True])

    def test_connaissance_sans_nom(self):
        self.assertIsNone(NOM.search(json.dumps(self.acq.connaissances)))
        self.assertEqual(self.acq.connaissances[0], connaissance(monde(1)))


class Placement(unittest.TestCase):
    def test_bijection_retrouvee_a_la_main(self):
        # K : emplacement 0 transitif+antisymétrique, 1 symétrique, 2 rien ; composition 1∘2 = 0.
        k = {"vecteurs": [[0, 0, 1, 1], [0, 1, 0, 0], [0, 0, 0, 0]], "compositions": [[1, 2, 0]]}
        P = ("reflexive", "symetrique", "antisymetrique", "transitive")
        props = {"Rc": [0, 0, 1, 1], "Ra": [0, 1, 0, 0], "Rb": [0, 0, 0, 0]}
        m = {"relations": ["Ra", "Rb", "Rc"], "proprietes": {r: dict(zip(P, v)) for r, v in props.items()},
             "compositions": [["Ra", "Rb", "Rc"]]}
        self.assertEqual(placer(k, m), sorted([("antisymetrique", "Rc"), ("transitive", "Rc"),
                                               ("symetrique", "Ra"), ("composition", "Ra", "Rb", "Rc")]))

    def test_composition_departage(self):
        # Deux emplacements identiques : seule la composition fixe lequel est lequel.
        k = {"vecteurs": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], "compositions": [[0, 1, 2]]}
        P = ("reflexive", "symetrique", "antisymetrique", "transitive")
        m = {"relations": ["Ra", "Rb", "Rc"], "proprietes": {r: dict(zip(P, [0] * 4)) for r in "Ra Rb Rc".split()},
             "compositions": [["Rc", "Ra", "Rb"]]}
        self.assertEqual(placer(k, m), [("composition", "Rc", "Ra", "Rb")])


class Amnesique(unittest.TestCase):
    def test_aucune_memoire_entre_mondes(self):
        s, l12 = _suite(OracleAmnesique(), [1, 2])
        _, l2 = _suite(OracleAmnesique(), [2])
        self.assertEqual(_sans_crues(l12[1]), _sans_crues(l2[0]))
        self.assertEqual(l12[1]["proprietes_crues"], l2[0]["proprietes_crues"])
        self.assertIsNone(l12[1]["proprietes_crues"]["regles_oracle"])


class Verdict(unittest.TestCase):
    def _res(self, n_acq, n_amn):
        def bloc(n):
            return {"mondes": [{"R_diff": 0.0, "requetes": 0, "deduits_faux_en_verite": 0}],
                    "familles": {"0": {"gain": 0.0, "serie": [0.0] * 5, "hausses": 0, "acceleration": False}},
                    "critere_acquerir": {"familles_accelerees": n, "verdict": "REUSSITE" if n >= 3 else "ECHEC"}}
        res = {n: bloc(0) for n in ("a0bis", "oracle_exact", "aleatoire", "oracle_proprietes",
                                    "plafond_verificateur", "decouvreur_naif")}
        res["oracle_acquereur"], res["oracle_amnesique"] = bloc(n_acq), bloc(n_amn)
        for n in ("oracle_acquereur", "oracle_exact"):
            res[n]["mondes"][0].update({"graine": 1, "proprietes_crues": {"k_egale_verite": None, "regles_oracle": None}})
        return res

    def test_seuils(self):
        self.assertEqual(verdict_mission1(self._res(3, 1))["verdict"], "ATTEIGNABLE_ET_DISCRIMINANT")
        self.assertEqual(verdict_mission1(self._res(2, 1))["verdict"], "NON_ATTEIGNABLE")
        self.assertEqual(verdict_mission1(self._res(4, 2))["verdict"], "TROP_PERMISSIF")
        self.assertEqual(verdict_mission1(self._res(2, 2))["verdict"], "NON_ATTEIGNABLE_ET_TROP_PERMISSIF")
        self.assertTrue(verdict_mission1(self._res(3, 1))["mission2"])
        self.assertFalse(verdict_mission1(self._res(3, 2))["mission2"])


class Determinisme(unittest.TestCase):
    def test_deux_processus_identiques(self):
        script = os.path.join(ICI, "evaluer_oracle.py")
        sorties = []
        with tempfile.TemporaryDirectory() as d:
            for h in ("1", "2"):
                sub = os.path.join(d, h)
                subprocess.run([sys.executable, script, "--graines", "1-6", "--sortie", sub], check=True,
                               stdout=subprocess.DEVNULL, env=dict(os.environ, PYTHONHASHSEED=h))
                with open(glob.glob(os.path.join(sub, "*", "resultats.json"))[0], encoding="utf-8") as fh:
                    sorties.append(fh.read())
        self.assertEqual(sorties[0], sorties[1])


if __name__ == "__main__":
    unittest.main()
