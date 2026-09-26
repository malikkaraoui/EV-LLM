import copy
import glob
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import unittest

ICI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ICI)

import chemin  # noqa: E402,F401

from a0 import (A0, A0SansMemoire, A0VerifieJamais, A0VerifieToujours, CONFIGURATIONS,  # noqa: E402
                apprendre, decision, etat_initial, gain_perte, revelations, valeurs_options)
from etalons_bis import premisses  # noqa: E402
from evaluer import evaluer_monde  # noqa: E402
from evaluer_a0 import pire  # noqa: E402
from interface import Environnement  # noqa: E402
from monde import generer_monde  # noqa: E402
from raisonneur import DEDUIT  # noqa: E402

NOM = re.compile(r"\bR\d\b|\bo\d{3}\b")


def _suite(systeme, graines):
    for g in graines:
        _, corr = evaluer_monde(systeme, generer_monde(g))
        systeme.fin_monde(corr)
    return systeme


class _Enregistreur(A0):
    """A0 qui garde, pour le test de renommage, ce qu'il passe à `apprendre`."""

    def fin_monde(self, correction):
        surs, rv = revelations(self.vue["questions"], correction)
        surs.update(self.req)
        self.capture = (copy.deepcopy(self.trace()), dict(surs), set(rv))
        super().fin_monde(correction)


def _renommer(x, table):
    if isinstance(x, str):
        if x in table:
            return table[x]
        if ":" in x:
            return ":".join(table.get(p, p) for p in x.split(":"))
        return x
    if isinstance(x, tuple):
        return tuple(_renommer(v, table) for v in x)
    if isinstance(x, list):
        return [_renommer(v, table) for v in x]
    if isinstance(x, set):
        return {_renommer(v, table) for v in x}
    if isinstance(x, dict):
        return {_renommer(k, table): _renommer(v, table) for k, v in x.items()}
    return x


class MemoireSansNom(unittest.TestCase):
    def test_aucun_nom_dans_l_etat(self):
        s = _suite(A0(), range(1, 8))
        texte = json.dumps(s.etat, sort_keys=True)
        self.assertIsNone(NOM.search(texte), texte[:300])
        self.assertEqual(set(s.etat), set(etat_initial()))
        self.assertEqual(len(s.etat["profils"]), 7)

    def test_renommage_ne_change_rien(self):
        for g in (1, 7, 14):
            s = _Enregistreur()
            s.etat = copy.deepcopy(_suite(A0(), range(1, 4)).etat) if g != 1 else etat_initial()
            depart = copy.deepcopy(s.etat)
            _suite(s, [g])
            trace, surs, rv = s.capture
            rels = trace["relations"]
            table = {r: n for r, n in zip(rels, ["R%d" % i for i in (3, 5, 1, 4, 2)])}
            ents = trace["entites"]
            table.update({e: "o%03d" % (997 - 7 * i) for i, e in enumerate(ents)})
            e1, e2 = copy.deepcopy(depart), copy.deepcopy(depart)
            apprendre(e1, trace, surs, rv, True)
            tr2 = _renommer(trace, table)
            tr2["relations"], tr2["entites"] = sorted(tr2["relations"]), sorted(tr2["entites"])  # comme une vue
            self.assertNotEqual([table[r] for r in rels], tr2["relations"])  # l'ordre change vraiment
            apprendre(e2, tr2, _renommer(surs, table), _renommer(rv, table), True)
            self.assertEqual(json.dumps(e1, sort_keys=True), json.dumps(e2, sort_keys=True), g)


class Declencheur(unittest.TestCase):
    def test_gain_perte_a_la_main(self):
        # p_ref = 0.25, ε = 1/64 : G = 2 − log2(64/63) ; L = 6 − log2(4/3)
        g, l = gain_perte(0.25, True)
        self.assertAlmostEqual(g, 2 - math.log2(64 / 63), places=9)
        self.assertAlmostEqual(l, 6 - math.log2(4 / 3), places=9)
        g, l = gain_perte(0.25, False)
        self.assertAlmostEqual(g, math.log2(4 / 3) - math.log2(64 / 63), places=9)
        self.assertAlmostEqual(l, 6 - 2, places=9)

    def test_regle_de_cout_a_la_main(self):
        C = 9.32
        # p = 0.1, ΣG = 20, ΣL = 110 : conclure 18 − 11 = 7 ; vérifier 18 − 9.32 = 8.68 → vérifier
        v = valeurs_options(0.1, 20, 110, C)
        self.assertAlmostEqual(v["conclure"], 7.0)
        self.assertAlmostEqual(v["verifier"], 8.68)
        self.assertEqual(decision(0.1, 20, 110, C), "verifier")
        # ΣL = 90 : p·ΣL = 9 < 9.32 → conclure (9 > 8.68)
        self.assertEqual(decision(0.1, 20, 90, C), "conclure")
        # κ = 1.25 : p·κ·ΣL = 11.25 > 9.32 → vérifier
        self.assertEqual(decision(0.1, 20, 90, C, kappa=1.25), "verifier")
        # p = 0.5, ΣG = 2, ΣL = 10 : conclure −4, vérifier −8.32 → INDÉTERMINÉ
        self.assertEqual(decision(0.5, 2, 10, C), "indetermine")
        # frontière exacte p·ΣL = C : conclure et vérifier à égalité → conclure
        self.assertEqual(decision(0.1, 20, 93.2, C), "conclure")

    def test_verifie_toujours_demande_toute_premisse(self):
        for g in (1, 6, 11, 16):
            m = generer_monde(g)
            env, s = Environnement(m), A0VerifieToujours()
            s.debut_monde(env.vue_publique())
            for p in (1, 2):
                reps = s.phase(p, env.ouvrir_phase(p), env.demander)
            demandes = {a for _, a, _ in env.requetes}
            self.assertTrue(premisses(reps) <= demandes, g)

    def test_verifie_jamais_ne_verifie_aucune_premisse(self):
        for g in (1, 6, 11, 16):
            m = generer_monde(g)
            env, s = Environnement(m), A0VerifieJamais()
            s.debut_monde(env.vue_publique())
            s.phase(1, env.ouvrir_phase(1), env.demander)
            s.phase(2, env.ouvrir_phase(2), env.demander)
            obs = {tuple(o["atome"]) for o in m["observations"]}
            self.assertFalse([a for _, a, _ in env.requetes if a in obs], g)


# --- autodiagnostic sur erreurs injectées --------------------------------------

ENTS = ["a", "b", "c", "d"]


def _trace(obs, req, reponse, cat=None):
    q = {"id": "A:R1:a:c", "type": "atome", "atome": ["R1", "a", "c"]}
    return {"relations": ["R1", "R2"], "entites": ENTS, "obs": obs, "req": req, "cat": cat or {},
            "reponses": {q["id"]: reponse}, "questions": [q], "compositions": []}


def _deduit_vrai(premisses_):
    return {"etiquette": DEDUIT, "valeur": True,
            "preuve": {"premisses": premisses_, "regles": [["transitive", "R1"]]}}


def _diff(a, b):
    return {k for k in a if json.dumps(a[k], sort_keys=True) != json.dumps(b[k], sort_keys=True)}


class Autodiagnostic(unittest.TestCase):
    def _deux(self, trace, surs):
        avec, sans = etat_initial(), etat_initial()
        d = apprendre(avec, trace, surs, set(), True)
        apprendre(sans, copy.deepcopy(trace), dict(surs), set(), False)
        return avec, sans, d

    def test_propriete_mal_acceptee(self):
        # R1(a,b) et R1(b,c) vrais et SÛRS (demandés), R1(a,c) faux : transitive réfutée.
        req = {("R1", "a", "b"): True, ("R1", "b", "c"): True}
        tr = _trace({}, req, _deduit_vrai([["R1", "a", "b", True], ["R1", "b", "c", True]]))
        surs = dict(req)
        surs[("R1", "a", "c")] = False
        avec, sans, d = self._deux(tr, surs)
        self.assertEqual(d, [["A:R1:a:c", "propriete"]])
        self.assertEqual(_diff(avec, sans), {"delta"})
        self.assertEqual(avec["delta"]["transitive"], 0.5)
        self.assertEqual(sum(avec["delta"].values()), 0.5)
        self.assertEqual(avec["kappa"], 1.0)

    def test_premisse_bruitee_non_verifiee(self):
        # R1(a,b) observé vrai en phase 2, jamais demandé, faux en vérité.
        obs = {("R1", "a", "b"): (True, 2), ("R1", "b", "c"): (True, 1)}
        tr = _trace(obs, {}, _deduit_vrai([["R1", "a", "b", True], ["R1", "b", "c", True]]))
        surs = {("R1", "a", "c"): False, ("R1", "a", "b"): False}
        avec, sans, d = self._deux(tr, surs)
        self.assertEqual(d, [["A:R1:a:c", "premisse"]])
        self.assertEqual(_diff(avec, sans), {"bruit"})
        self.assertEqual(avec["bruit"]["phase2"][0] - sans["bruit"]["phase2"][0], 2)
        self.assertEqual(avec["bruit"]["phase2"][1] - sans["bruit"]["phase2"][1], 2)
        self.assertEqual(avec["bruit"]["phase1"], sans["bruit"]["phase1"])

    def test_categorie_violation(self):
        obs = {("R1", "a", "b"): (True, 1), ("R1", "b", "c"): (True, 1)}
        tr = _trace(obs, {}, _deduit_vrai([["R1", "a", "b", True], ["R1", "b", "c", True]]),
                    cat={("R1", "a", "b"): "violation"})
        surs = {("R1", "a", "c"): False, ("R1", "a", "b"): False}
        avec, sans, _ = self._deux(tr, surs)
        self.assertEqual(avec["bruit"]["violation"][0] - sans["bruit"]["violation"][0], 2)

    def test_seuil_quand_rien_n_est_etabli(self):
        # Prémisses observées, vérité non révélée : ni propriété ni prémisse établie.
        obs = {("R1", "a", "b"): (True, 1), ("R1", "b", "c"): (True, 1)}
        tr = _trace(obs, {}, _deduit_vrai([["R1", "a", "b", True], ["R1", "b", "c", True]]))
        avec, sans, d = self._deux(tr, {("R1", "a", "c"): False})
        self.assertEqual(d, [["A:R1:a:c", "seuil"]])
        self.assertEqual(_diff(avec, sans), {"kappa"})
        self.assertAlmostEqual(avec["kappa"], 1.1)

    def test_reponse_juste_rien_ne_bouge(self):
        obs = {("R1", "a", "b"): (True, 1), ("R1", "b", "c"): (True, 1)}
        tr = _trace(obs, {}, _deduit_vrai([["R1", "a", "b", True], ["R1", "b", "c", True]]))
        avec, sans, d = self._deux(tr, {("R1", "a", "c"): True})
        self.assertEqual(d, [])
        self.assertEqual(_diff(avec, sans), set())


class Configurations(unittest.TestCase):
    def test_sans_memoire_repart_de_zero(self):
        s = _suite(A0SansMemoire(), [1, 2])
        s.debut_monde(Environnement(generer_monde(3)).vue_publique())
        self.assertEqual(s.etat, etat_initial())

    def test_memoire_conservee(self):
        s = _suite(A0(), [1, 2])
        s.debut_monde(Environnement(generer_monde(3)).vue_publique())
        self.assertEqual(len(s.etat["profils"]), 2)

    def test_noms_uniques(self):
        self.assertEqual(len({c.nom for c in CONFIGURATIONS}), 5)

    def test_pire_et_verdict(self):
        ref = {"M1": (0.01, +1), "M4": (2.0, -1)}
        self.assertEqual(pire({"M1": (0.0, +1), "M4": (2.0, -1)}, ref), ["M1"])
        self.assertEqual(pire({"M1": (0.01, +1), "M4": (3.0, -1)}, ref), ["M4"])
        self.assertEqual(pire({"M1": (0.02, +1), "M4": (1.0, -1)}, ref), [])


class Determinisme(unittest.TestCase):
    def test_deux_processus_identiques(self):
        script = os.path.join(ICI, "evaluer_a0.py")
        sorties = []
        with tempfile.TemporaryDirectory() as d:
            for h in ("1", "2"):
                sub = os.path.join(d, h)
                subprocess.run([sys.executable, script, "--graines", "1-10", "--sortie", sub], check=True,
                               stdout=subprocess.DEVNULL, env=dict(os.environ, PYTHONHASHSEED=h))
                with open(glob.glob(os.path.join(sub, "*", "resultats.json"))[0], encoding="utf-8") as fh:
                    sorties.append(fh.read())
        self.assertEqual(sorties[0], sorties[1])


if __name__ == "__main__":
    unittest.main()
