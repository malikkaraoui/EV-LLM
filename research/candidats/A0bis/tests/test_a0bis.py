import copy
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

from a0 import revelations  # noqa: E402
from a0bis import (A0Bis, A0BisSansBruitMLE, A0BisSansCoutMarginal, A0BisSansMemoireFamille,  # noqa: E402
                   CONFIGURATIONS, apprendre_bis, augmente_r, cout_marginal, distance_profils, eta_global_mle,
                   memoire_initiale, p_bruit_mle, ranger, rentable, voi_instance, voi_premisse)
from evaluer import evaluer_monde  # noqa: E402
from evaluer_a0bis import attribution  # noqa: E402
from interface import Environnement  # noqa: E402
from monde import generer_monde  # noqa: E402
from oracle import C_ATOME  # noqa: E402
from raisonneur import DEDUIT  # noqa: E402

NOM = re.compile(r"\bR\d\b|\bo\d{3}\b")


def _suite(systeme, graines):
    lignes = []
    for g in graines:
        l, corr = evaluer_monde(systeme, generer_monde(g))
        systeme.fin_monde(corr)
        lignes.append(l)
    return systeme, lignes


# --- (a) coût marginal ----------------------------------------------------------

class CoutMarginal(unittest.TestCase):
    def test_derivation_a_la_main(self):
        # E = 10, B = 1000, C = 9.32 : R·C = 0.0932.
        e, b, c = 10.0, 1000.0, 9.32
        self.assertAlmostEqual(cout_marginal(e / b, c), 0.0932)
        self.assertTrue(augmente_r(e, b, 0.1, c))       # 10.1 / 1009.32 = 0.010007 > 0.01
        self.assertFalse(augmente_r(e, b, 0.09, c))     # 10.09 / 1009.32 = 0.009997 < 0.01
        self.assertAlmostEqual(10.1 / 1009.32, 0.0100067, places=6)
        # La règle de requête coïncide avec le calcul direct de part et d'autre de R·C.
        for d in (0.05, 0.0931, 0.0933, 0.5, 5.0):
            self.assertEqual(rentable(d, cout_marginal(e / b, c)), augmente_r(e, b, d, c), d)

    def test_pas_de_dilution(self):
        # R < 0 : une requête de gain nul augmente R (dilution) mais n'est pas faite.
        self.assertTrue(augmente_r(-10.0, 1000.0, 0.0))
        self.assertEqual(cout_marginal(-0.01), 0.0)
        self.assertFalse(rentable(0.0, cout_marginal(-0.01)))
        self.assertTrue(rentable(0.01, cout_marginal(-0.01)))

    def test_voi_instance_a_la_main(self):
        # b = 0.5, ΣG = 10, ΣL = 20, q = 0.5, m = 0 (antécédents sûrs) :
        # U(b) = max(0, 5 + 0.5·(5 − 10)) = 2.5 ; P_c = 0.75, b_c = 2/3, U(b_c) = 20/3 − 5/3 = 5 ;
        # P_v = 0.25, b_v = 0, U(0) = max(0, −5) = 0 ; VOI = 0.75·5 − 2.5 = 1.25.
        self.assertAlmostEqual(voi_instance(0.5, 10, 20, 0.5, 0.1, 0), 1.25)
        # m = 1, η = 0.1 : η_m = 0.1 ; P_c = 0.45 + 0.25 = 0.7 ; b_c = 0.45/0.7 ; b_v = 0.05/0.3.
        bc, bv = 0.45 / 0.7, 0.05 / 0.3
        u = lambda b: max(0.0, b * 10 + (1 - b) * (5 - 10))  # noqa: E731
        self.assertAlmostEqual(voi_instance(0.5, 10, 20, 0.5, 0.1, 1), 0.7 * u(bc) + 0.3 * u(bv) - 2.5)
        # q = 0.2 (q ≠ 1 − q) : U(b) = max(0, 5 + 0.5·(2 − 16)) = 0 ; P_c = 0.5 + 0.1 = 0.6, b_c = 5/6,
        # U(b_c) = 50/6 + (2 − 16)/6 = 6 ; b_v = 0 ; VOI = 0.6·6 = 3.6.
        self.assertAlmostEqual(voi_instance(0.5, 10, 20, 0.2, 0.1, 0), 3.6)
        # Information inutile : une règle sûre n'a aucune valeur de test.
        self.assertAlmostEqual(voi_instance(1.0, 10, 20, 0.5, 0.1, 0), 0.0)

    def test_voi_premisse_a_la_main(self):
        # p = 0.1, ΣG = 10, ΣL = 30 : min(p·ΣL, (1−p)·ΣG) = min(3, 9) = 3 ; κ = 2 → min(6, 9) = 6.
        self.assertAlmostEqual(voi_premisse(0.1, 10, 30), 3.0)
        self.assertAlmostEqual(voi_premisse(0.1, 10, 30, kappa=2.0), 6.0)
        # p = 0.5, ΣG = 2, ΣL = 10 : conclure < 0, donc VOI = (1−p)·ΣG = 1.
        self.assertAlmostEqual(voi_premisse(0.5, 2, 10), 1.0)

    def test_requetes_selon_le_cout(self):
        # Premier monde, R̂ = 0 : a0bis demande ; en coût absolu (règle d'A0) il ne demande rien.
        _, l1 = _suite(A0Bis(), [1])
        _, l2 = _suite(A0BisSansCoutMarginal(), [1])
        self.assertGreater(l1[0]["requetes"], 0)
        self.assertEqual(l2[0]["requetes"], 0)
        self.assertEqual(l1[0]["proprietes_crues"]["cout_marginal"], 0.0)
        self.assertAlmostEqual(l2[0]["proprietes_crues"]["cout_marginal"], C_ATOME)

    def test_r_realise_egale_r_du_banc(self):
        s, lignes = _suite(A0Bis(), [1, 6, 11])
        for l, j in zip(lignes, s.journal):
            self.assertAlmostEqual(l["R"], j["r_realise"], places=12)

    def test_r_chapeau_fige_pour_le_monde(self):
        s, _ = _suite(A0Bis(), [1, 2])
        env = Environnement(generer_monde(3))
        s.debut_monde(env.vue_publique())
        self.assertIsNone(s.r_chapeau)
        s.r_chapeau = 0.123
        for p in (1, 2):
            s.phase(p, env.ouvrir_phase(p), env.demander)
        self.assertEqual(s.r_chapeau, 0.123)
        self.assertAlmostEqual(s.proprietes_crues()["cout_marginal"], 0.123 * C_ATOME)

    def test_r_chapeau_moyenne_des_mondes_passes(self):
        s, _ = _suite(A0BisSansMemoireFamille(), [1, 2, 3])
        rs = [j["r_realise"] for j in s.journal]
        self.assertEqual(s.journal[0]["r_chapeau"], 0.0)
        self.assertAlmostEqual(s.journal[2]["r_chapeau"], (rs[0] + rs[1]) / 2)


# --- (b) mémoire par famille, sans nom ------------------------------------------

class MemoireSansNom(unittest.TestCase):
    def test_aucun_nom_dans_la_memoire(self):
        s, _ = _suite(A0Bis(), range(1, 8))
        texte = json.dumps(s.memoire, sort_keys=True)
        self.assertIsNone(NOM.search(texte), texte[:300])
        self.assertEqual(len(s.memoire["globale"]["profils"]), 7)
        self.assertGreaterEqual(len(s.memoire["familles"]), 1)

    def test_renommage_ne_change_rien(self):
        base, _ = _suite(A0Bis(), [1, 2, 6])
        for g in (3, 7, 14):
            s = copy.deepcopy(base)
            _suite(s, [g])
            j = s.journal[-1]
            # rejoue la mise à jour de fin de monde sur une copie renommée des entrées
            s2 = copy.deepcopy(base)
            env = Environnement(generer_monde(g))
            l, corr = evaluer_monde(s2, generer_monde(g))
            surs, rv = revelations(s2.vue["questions"], corr)
            surs.update(s2.req)
            trace = s2.trace()
            rels, ents = trace["relations"], trace["entites"]
            table = {r: n for r, n in zip(rels, ["R%d" % i for i in (3, 5, 1, 4, 2)])}
            table.update({e: "o%03d" % (997 - 7 * i) for i, e in enumerate(ents)})
            m1, m2 = copy.deepcopy(s2.memoire), copy.deepcopy(s2.memoire)
            var = env.vue_publique()["semantique"]["variante"]
            apprendre_bis(m1, s2.k_ident, trace, surs, rv, var, j["r_realise"], eta_=s2._eta())
            tr2 = _renommer(trace, table)
            tr2["relations"], tr2["entites"] = sorted(tr2["relations"]), sorted(tr2["entites"])
            self.assertNotEqual([table[r] for r in rels], tr2["relations"])
            apprendre_bis(m2, s2.k_ident, tr2, _renommer(surs, table), _renommer(rv, table), var,
                          j["r_realise"], eta_=s2._eta())
            self.assertEqual(json.dumps(m1, sort_keys=True), json.dumps(m2, sort_keys=True), g)
            self.assertEqual(json.dumps(m1, sort_keys=True), json.dumps(s.memoire, sort_keys=True), g)

    def test_familles(self):
        p = [[0, 1, 0, 0], [0, 0, 0, 0], [1, 1, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]
        d2 = [[1, 1, 0, 0], [0, 0, 0, 0], [1, 1, 0, 1], [0, 0, 1, 1], [0, 1, 0, 0]]
        d3 = [[0, 1, 0, 0], [1, 0, 1, 1], [1, 1, 0, 1], [0, 0, 1, 0], [0, 1, 0, 0]]
        self.assertEqual(distance_profils(sorted(p), sorted(reversed(p))), 0)
        self.assertEqual(distance_profils(sorted(p), sorted(d2)), 2)
        self.assertEqual(distance_profils(sorted(p), sorted(d3)), 3)
        fam = [{"variante": "B", "representant": sorted(p)}]
        self.assertEqual(ranger(fam, "B", sorted(d2)), 0)
        self.assertIsNone(ranger(fam, "B", sorted(d3)))
        self.assertIsNone(ranger(fam, "A", sorted(p)))

    def test_sans_memoire_famille_n_identifie_jamais(self):
        s, lignes = _suite(A0BisSansMemoireFamille(), [1, 2, 3])
        self.assertEqual(s.memoire["familles"], [])
        self.assertTrue(all(l["proprietes_crues"]["famille_identifiee"] is None for l in lignes))

    def test_identification_dans_la_meme_famille(self):
        s, lignes = _suite(A0Bis(), [6, 7, 8])
        self.assertTrue(any(l["proprietes_crues"]["famille_identifiee"] is not None for l in lignes[1:]))


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


# --- (c) bruit MLE ---------------------------------------------------------------

ENTS = ["a", "b", "c", "d"]


def _trace_premisse_fautive():
    q = {"id": "A:R1:a:c", "type": "atome", "atome": ["R1", "a", "c"]}
    rep = {"etiquette": DEDUIT, "valeur": True,
           "preuve": {"premisses": [["R1", "a", "b", True], ["R1", "b", "c", True]],
                      "regles": [["transitive", "R1"]]}}
    obs = {("R1", "a", "b"): (True, 2), ("R1", "b", "c"): (True, 1)}
    trace = {"relations": ["R1", "R2"], "entites": ENTS, "obs": obs, "req": {}, "cat": {},
             "reponses": {q["id"]: rep}, "questions": [q], "compositions": []}
    return trace, {("R1", "a", "c"): False, ("R1", "a", "b"): False}


class BruitMLE(unittest.TestCase):
    def test_mle_sur_donnees_connues(self):
        v = {"phase1": [3, 40], "phase2": [0, 0], "violation": [2, 4]}
        self.assertAlmostEqual(p_bruit_mle(v, "phase1"), 0.075)
        self.assertAlmostEqual(p_bruit_mle(v, "phase2"), 5 / 44)     # n < 5 : repli sur les trois catégories
        self.assertAlmostEqual(p_bruit_mle(v, "violation"), 5 / 44)
        self.assertAlmostEqual(eta_global_mle(v), 0.075)
        v2 = {"phase1": [7, 70], "phase2": [3, 30], "violation": [0, 0]}
        self.assertAlmostEqual(eta_global_mle(v2), 0.1)

    def test_repli_sous_cinq_verifications(self):
        v = {"phase1": [1, 2], "phase2": [0, 1], "violation": [0, 1]}
        self.assertAlmostEqual(p_bruit_mle(v, "phase1"), 0.1)
        self.assertAlmostEqual(p_bruit_mle(v, "violation"), 0.5)
        self.assertAlmostEqual(eta_global_mle(v), 0.1)

    def test_bornes(self):
        self.assertAlmostEqual(p_bruit_mle({"phase1": [0, 50], "phase2": [0, 0], "violation": [0, 0]}, "phase1"), 0.01)
        self.assertAlmostEqual(p_bruit_mle({"phase1": [40, 50], "phase2": [0, 0], "violation": [0, 0]}, "phase1"), 0.5)

    def test_fautes_attribuees_ne_touchent_pas_le_bruit(self):
        trace, surs = _trace_premisse_fautive()
        mem = memoire_initiale()
        avant = copy.deepcopy(mem["verifs"])
        out = apprendre_bis(mem, None, trace, surs, set(), "B", 0.0, bruit_mle=True, eta_=0.1)
        self.assertEqual(out["diagnostic"], [["A:R1:a:c", "premisse"]])
        self.assertEqual(mem["verifs"], avant)
        self.assertEqual(mem["bruit_a0"], memoire_initiale()["bruit_a0"])
        # ablation −bruit-MLE : compteurs d'A0, révélation + 2 erreurs attribuées
        mem2 = memoire_initiale()
        apprendre_bis(mem2, None, copy.deepcopy(trace), dict(surs), set(), "B", 0.0, bruit_mle=False, eta_=0.1)
        self.assertEqual(mem2["bruit_a0"]["phase2"], [1 + 2, 1 + 2])

    def test_verifications_comptees_en_direct(self):
        # Une vérification est la requête d'un fait DÉJÀ observé (pas d'un atome observé plus tard).
        for g in (1, 6):
            m = generer_monde(g)
            env, s = Environnement(m), A0Bis()
            s.debut_monde(env.vue_publique())
            for p in (1, 2):
                s.phase(p, env.ouvrir_phase(p), env.demander)
            ph = {tuple(o["atome"]): o["phase"] for o in m["observations"]}
            fausses = {tuple(o["atome"]): o["valeur"] for o in m["observations"]}
            verifs = [(a, v) for p, a, v in env.requetes if a in ph and ph[a] <= p]
            self.assertGreater(len(verifs), 0, g)
            self.assertEqual(sum(v[1] for v in s.memoire["verifs"].values()), len(verifs), g)
            self.assertEqual(sum(v[0] for v in s.memoire["verifs"].values()),
                             sum(fausses[a] != v for a, v in verifs), g)


class Configurations(unittest.TestCase):
    def test_noms_uniques(self):
        self.assertEqual(len({c.nom for c in CONFIGURATIONS}), 4)

    def test_ablations_un_seul_drapeau(self):
        ref = (A0Bis.COUT_MARGINAL, A0Bis.MEMOIRE_FAMILLE, A0Bis.BRUIT_MLE)
        self.assertEqual(ref, (True, True, True))
        for c in CONFIGURATIONS[1:]:
            self.assertEqual(sum(a != b for a, b in zip(ref, (c.COUT_MARGINAL, c.MEMOIRE_FAMILLE, c.BRUIT_MLE))), 1)
        self.assertFalse(A0BisSansBruitMLE.BRUIT_MLE)

    def test_attribution(self):
        ref = {"M1_R_diff_moyen": (0.0, 1), "M2_familles_accelerees": (2, 1)}
        self.assertEqual(attribution({"M1_R_diff_moyen": (-0.01, 1), "M2_familles_accelerees": (3, 1)}, ref), "porte")
        self.assertEqual(attribution({"M1_R_diff_moyen": (0.0, 1), "M2_familles_accelerees": (2, 1)}, ref),
                         "ne_porte_pas")
        self.assertEqual(attribution({"M1_R_diff_moyen": (0.01, 1), "M2_familles_accelerees": (1, 1)}, ref),
                         "indetermine")


class Determinisme(unittest.TestCase):
    def test_deux_processus_identiques(self):
        script = os.path.join(ICI, "evaluer_a0bis.py")
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
