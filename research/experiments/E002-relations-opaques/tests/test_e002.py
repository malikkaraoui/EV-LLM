"""Tests E002 : générateur, oracle (cas écrits à la main), interface, R, étalons."""

import itertools
import math
import os
import random
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etalons import Aleatoire, DecouvreurNaif, OracleProprietes  # noqa: E402
from evaluer import acceleration, evaluer_monde  # noqa: E402
from interface import Environnement  # noqa: E402
from monde import (BRUIT_MAX, BRUIT_MIN, N_OBS, generer_monde, regles_du_monde,  # noqa: E402
                   vers_json)
from oracle import C_ATOME, attendus, bits_economises, juste  # noqa: E402
from raisonneur import (CONTRADICTION, DEDUIT, INDETERMINE, Fermeture,  # noqa: E402
                        Raisonneur, verifier_preuve)

ENT = ["A", "B", "C", "D", "E"]
CHAINE = {("G", "A", "B"): True, ("G", "B", "C"): True, ("G", "C", "D"): True, ("G", "E", "A"): True}
ORDRE = [("transitive", "G"), ("antisymetrique", "G")]


class Generateur(unittest.TestCase):
    def test_deterministe(self):
        self.assertEqual(vers_json(generer_monde(7)), vers_json(generer_monde(7)))
        self.assertNotEqual(vers_json(generer_monde(7)), vers_json(generer_monde(8)))

    def test_contraintes_preenregistrees(self):
        for g in range(1, 21):
            m = generer_monde(g)
            non_trans = sum(1 for r in m["relations"] if not m["proprietes"][r]["transitive"])
            self.assertGreaterEqual(non_trans / len(m["relations"]), 0.30)
            nb = sum(o["bruit"] for o in m["observations"])
            self.assertEqual(nb, round(m["taux_bruit"] * N_OBS))
            self.assertTrue(BRUIT_MIN <= m["taux_bruit"] <= BRUIT_MAX)
            obs = {tuple(o["atome"]) for o in m["observations"]}
            tenus = {tuple(a) for a in m["tenus_a_l_ecart"]}
            self.assertFalse(obs & tenus)
            self.assertEqual(len(m["questions"]), 60 + 20 + 3)
            self.assertEqual(m["semantique"]["variante"], "A" if m["famille"] in (0, 2) else "B")
            cible = [o for o in m["observations"] if o["cible"]]
            self.assertEqual(len(cible), 1)
            self.assertEqual(cible[0]["phase"], 2)

    def test_meme_profil_dans_une_famille(self):
        for f in range(4):
            profils = {str(generer_monde(5 * f + i)["profil"]) for i in range(1, 6)}
            self.assertEqual(len(profils), 1)

    def test_verite_coherente_et_proprietes(self):
        for g in range(1, 21):
            m = generer_monde(g)
            vrai = {(r, a, b): True for r, ps in m["verite"].items() for a, b in ps}
            rais = Raisonneur(vrai, regles_du_monde(m), m["exclusions"], m["entites"])
            self.assertTrue(rais.coherent(), g)
            # la fermeture de la vérité sous les vraies règles n'ajoute rien de faux
            self.assertEqual(set(rais.ferm.just), set(vrai), g)
            for r, t in m["types"].items():
                p = m["proprietes"][r]
                if t in ("ORDRE", "ORDRE_LARGE"):
                    self.assertTrue(p["transitive"] and p["antisymetrique"])
                if t == "EQUIVALENCE":
                    self.assertTrue(p["transitive"] and p["symetrique"] and p["reflexive"])
                if t.endswith("PIEGE"):
                    self.assertFalse(p["transitive"])
                if t == "SYM_PIEGE":
                    self.assertTrue(p["symetrique"] and not p["reflexive"])
                if t == "CYCLE_PIEGE":
                    self.assertTrue(p["antisymetrique"] and not p["symetrique"])
                if t == "AUCUNE_PIEGE":
                    self.assertFalse(any(p.values()))


class OracleCasAlaMain(unittest.TestCase):
    """§29 v2.1 : A>B>C>D, E>A ; variantes A/B de « exclut »."""

    def test_variante_A_contradiction(self):
        rais = Raisonneur(CHAINE, ORDRE + [("exclusion_A", "G")], [("D", "E")], ENT)
        rep = rais.exclusion("D", "E")
        self.assertEqual(rep["etiquette"], CONTRADICTION)
        self.assertEqual(rep["regle_violee"], ["exclusion_A", "G"])
        prem = {tuple(p[:3]) for p in rep["preuve"]["premisses"]}
        self.assertEqual(prem, set(CHAINE))  # preuve E>A>B>C>D
        self.assertEqual(rais.atome(("G", "E", "D"))["etiquette"], CONTRADICTION)
        self.assertFalse(rais.coherent())

    def test_variante_B_indetermine(self):
        rais = Raisonneur(CHAINE, ORDRE, [("D", "E")], ENT)
        rep = rais.exclusion("D", "E")
        self.assertEqual(rep["etiquette"], INDETERMINE)
        self.assertIn("exclut", rep["manque"])
        self.assertEqual((rais.atome(("G", "E", "D"))["etiquette"], rais.atome(("G", "E", "D"))["valeur"]),
                         (DEDUIT, True))
        self.assertTrue(rais.coherent())

    def test_A_et_B_different(self):
        a = Raisonneur(CHAINE, ORDRE + [("exclusion_A", "G")], [("D", "E")], ENT).exclusion("D", "E")
        b = Raisonneur(CHAINE, ORDRE, [("D", "E")], ENT).exclusion("D", "E")
        self.assertNotEqual(a["etiquette"], b["etiquette"])

    def test_exclusion_A_sans_conflit(self):
        faits = {("G", "A", "B"): True, ("G", "C", "D"): True}
        rais = Raisonneur(faits, ORDRE + [("exclusion_A", "G")], [("A", "D")], ENT)
        self.assertEqual(rais.exclusion("A", "D")["etiquette"], DEDUIT)
        self.assertEqual(rais.atome(("G", "A", "D"))["valeur"], False)  # interdit par la règle

    def test_deductions_ordre(self):
        rais = Raisonneur(CHAINE, ORDRE, [], ENT)
        self.assertEqual(rais.atome(("G", "A", "C"))["valeur"], True)
        self.assertEqual(rais.atome(("G", "E", "D"))["valeur"], True)
        r = rais.atome(("G", "C", "A"))  # antisymétrie
        self.assertEqual((r["etiquette"], r["valeur"]), (DEDUIT, False))
        self.assertEqual(rais.atome(("G", "B", "E"))["etiquette"], DEDUIT)  # E>B donc pas B>E
        self.assertEqual(rais.atome(("H", "A", "B"))["etiquette"], INDETERMINE)

    def test_sans_transitivite_rien_ne_se_deduit(self):
        rais = Raisonneur(CHAINE, [], [], ENT)
        self.assertEqual(rais.atome(("G", "A", "C"))["etiquette"], INDETERMINE)
        self.assertEqual(rais.atome(("G", "A", "B"))["etiquette"], DEDUIT)  # fait connu

    def test_observation_negative_contredite(self):
        faits = dict(CHAINE)
        faits[("G", "A", "D")] = False
        rais = Raisonneur(faits, ORDRE, [], ENT)
        self.assertEqual(rais.atome(("G", "A", "D"))["etiquette"], CONTRADICTION)
        self.assertEqual(rais.atome(("G", "A", "D"))["regle_violee"], ["fait-negatif"])
        # base incohérente : une contradiction ailleurs ne rend pas tout « DÉDUIT faux »
        self.assertEqual(rais.atome(("H", "A", "B"))["etiquette"], INDETERMINE)

    def test_symetrie_reflexivite_composition(self):
        faits = {("S", "A", "B"): True, ("P", "B", "C"): True}
        regles = [("symetrique", "S"), ("reflexive", "S"), ("composition", "S", "P", "Q")]
        rais = Raisonneur(faits, regles, [], ENT)
        self.assertEqual(rais.atome(("S", "B", "A"))["valeur"], True)
        self.assertEqual(rais.atome(("S", "E", "E"))["valeur"], True)
        self.assertEqual(rais.atome(("Q", "A", "C"))["valeur"], True)
        self.assertEqual(rais.atome(("Q", "B", "C"))["etiquette"], DEDUIT)  # S(B,B) ∘ P(B,C)

    def test_verificateur_de_preuve(self):
        rais = Raisonneur(CHAINE, ORDRE, [], ENT)
        q = {"type": "atome", "atome": ["G", "A", "D"]}
        rep = rais.atome(q["atome"])
        self.assertTrue(verifier_preuve(rep, q, CHAINE, ORDRE, [], ENT))
        # règle citée fausse dans le monde (ici G n'y est pas transitive)
        self.assertFalse(verifier_preuve(rep, q, CHAINE, [("antisymetrique", "G")], [], ENT))
        # prémisse inconnue du système
        faux = dict(rep, preuve={"premisses": [["G", "A", "D", True]], "regles": []})
        self.assertFalse(verifier_preuve(faux, q, CHAINE, ORDRE, [], ENT))
        # preuve qui n'entraîne pas la conclusion
        court = dict(rep, preuve={"premisses": [["G", "A", "B", True]], "regles": [["transitive", "G"]]})
        self.assertFalse(verifier_preuve(court, q, CHAINE, ORDRE, [], ENT))


class FermetureIndependante(unittest.TestCase):
    """Le chaînage avant égale un point fixe naïf écrit autrement."""

    def naif(self, faits, regles, ent):
        m = set(faits)
        for t in regles:
            if t[0] == "reflexive":
                m |= {(t[1], x, x) for x in ent}
        while True:
            neuf = set()
            for t in regles:
                for (r1, x, y), (r2, y2, z) in itertools.product(m, m):
                    if t[0] == "transitive" and r1 == r2 == t[1] and y == y2:
                        neuf.add((r1, x, z))
                    if t[0] == "composition" and (r1, r2) == (t[1], t[2]) and y == y2:
                        neuf.add((t[3], x, z))
                for (r, x, y) in m:
                    if t[0] == "symetrique" and r == t[1]:
                        neuf.add((r, y, x))
            if neuf <= m:
                return m
            m |= neuf

    def test_aleatoire(self):
        rng = random.Random(3)
        ent = ["a", "b", "c", "d"]
        rels = ["P", "Q", "S"]
        for _ in range(60):
            faits = {(rng.choice(rels), rng.choice(ent), rng.choice(ent)) for _ in range(6)}
            regles = []
            for r in rels:
                for p in ("reflexive", "symetrique", "transitive"):
                    if rng.random() < 0.3:
                        regles.append((p, r))
            if rng.random() < 0.5:
                regles.append(("composition",) + tuple(rng.sample(rels, 3)))
            self.assertEqual(set(Fermeture(faits, regles, ent).just), self.naif(faits, regles, ent))


class InterfaceEtR(unittest.TestCase):
    def mini_monde(self):
        return {
            "relations": ["R1"], "entites": ["a", "b", "c"],
            "verite": {"R1": [["a", "b"], ["b", "b"], ["c", "a"]]},
            "semantique": {"variante": "B", "relation": None, "texte": ""},
            "exclusions": [], "questions": [],
            "tenus_a_l_ecart": [["R1", "a", "b"], ["R1", "b", "a"], ["R1", "c", "a"], ["R1", "a", "c"],
                                ["R1", "c", "b"]],
            "observations": [{"atome": ["R1", "b", "b"], "valeur": True, "phase": 1},
                             {"atome": ["R1", "a", "a"], "valeur": False, "phase": 1},
                             {"atome": ["R1", "b", "c"], "valeur": True, "phase": 1}],  # bruitée
        }

    def test_requete_refusee_et_requete_prime(self):
        env = Environnement(self.mini_monde())
        env.ouvrir_phase(1)
        self.assertIsNone(env.demander("R1", "a", "b"))          # tenu à l'écart
        self.assertEqual(env.bits_experience()["requetes"], 0)  # non facturé
        self.assertIs(env.demander("R1", "b", "c"), False)      # le monde corrige le bruit
        self.assertIs(env.connus(1)[("R1", "b", "c")], False)
        self.assertAlmostEqual(env.bits_experience()["requetes"], C_ATOME)

    def test_R_calcule_a_la_main(self):
        # p_ref(R1) = (2 positifs + 1) / (3 obs + 2) = 0.6 ; C_ATOME = log2 5 + 7 = 9.3219281
        # a,b vrai   DÉDUIT vrai   : 0.7369656 − 0.0227201 = +0.7142455
        # b,a faux   DÉDUIT vrai   : 1.3219281 − 6         = −4.6780719
        # c,a vrai   DÉDUIT vrai   : +0.7142455
        # a,c faux   HYPOTHÈSE 0.2 : 1.3219281 − 0.3219281 = +1.0000000
        # c,b faux   INDÉTERMINÉ   : 0
        # total −2.2495809 ; expérience 3 obs + 1 requête = 37.2877124 bits ; R = −0.0603303
        env = Environnement(self.mini_monde())
        env.ouvrir_phase(1)
        env.demander("R1", "c", "c")
        self.assertAlmostEqual(env.p_ref()["R1"], 0.6)
        reps = {("R1", "a", "b"): {"etiquette": DEDUIT, "valeur": True},
                ("R1", "b", "a"): {"etiquette": DEDUIT, "valeur": True},
                ("R1", "c", "a"): {"etiquette": DEDUIT, "valeur": True},
                ("R1", "c", "b"): {"etiquette": INDETERMINE},
                ("R1", "a", "c"): {"etiquette": "HYPOTHÈSE", "valeur": False, "p_vrai": 0.2}}
        m = self.mini_monde()
        verites = {tuple(a): [a[1], a[2]] in m["verite"]["R1"] for a in m["tenus_a_l_ecart"]}
        eco = bits_economises(reps, m["tenus_a_l_ecart"], verites, env.p_ref())
        self.assertAlmostEqual(eco, -2.2495809, places=6)
        bits_exp = sum(env.bits_experience().values())
        self.assertAlmostEqual(bits_exp, 37.2877124, places=6)
        self.assertAlmostEqual(eco / bits_exp, -0.0603303, places=6)
        self.assertAlmostEqual(C_ATOME, math.log2(5) + 7)


class Etalons(unittest.TestCase):
    def test_plafond_egale_l_attendu(self):
        for g in (1, 6):
            m = generer_monde(g)
            ligne, corr = evaluer_monde(OracleProprietes(), m)
            self.assertEqual(ligne["exactitude"], 1.0)
            self.assertEqual(ligne["requetes"], 0)
            self.assertEqual(ligne["preuves_valides"], 1.0)

    def test_decouvreur_respecte_les_regles_du_banc(self):
        m = generer_monde(3)
        s = DecouvreurNaif()
        ligne, _ = evaluer_monde(s, m)
        self.assertLessEqual(ligne["requetes"], DecouvreurNaif.BUDGET)
        tenus = {tuple(a) for a in m["tenus_a_l_ecart"]}
        self.assertFalse(set(s.req) & tenus)
        # rien n'est gardé : même monde, même résultat, quel que soit l'historique
        s2 = DecouvreurNaif()
        evaluer_monde(s2, generer_monde(9))
        self.assertEqual(evaluer_monde(s2, m)[0]["R"], ligne["R"])

    def test_aleatoire_deterministe(self):
        m = generer_monde(2)
        self.assertEqual(evaluer_monde(Aleatoire(), m)[0]["R"], evaluer_monde(Aleatoire(), m)[0]["R"])

    def test_juste_hypothese_sur_indetermine(self):
        self.assertTrue(juste({"etiquette": "HYPOTHÈSE"}, {"etiquette": INDETERMINE}))
        self.assertFalse(juste({"etiquette": "HYPOTHÈSE"}, {"etiquette": DEDUIT, "valeur": True}))

    def test_attendus_couvrent_toutes_les_questions(self):
        m = generer_monde(4)
        env = Environnement(m)
        env.ouvrir_phase(1)
        env.ouvrir_phase(2)
        self.assertEqual(set(attendus(m, env.connus(2))), {q["id"] for q in m["questions"]})


class Acceleration(unittest.TestCase):
    def test_critere(self):
        self.assertTrue(acceleration([0.1, 0.2, 0.3, 0.25, 0.4])["acceleration"])
        self.assertFalse(acceleration([0.1, 0.2, 0.3, 0.4, 0.12])["acceleration"])  # gain < 0.05
        self.assertFalse(acceleration([0.1, 0.5, 0.2, 0.1, 0.4])["acceleration"])   # 2 hausses
        self.assertFalse(acceleration([0.1, None, 0.3, 0.4, 0.5])["acceleration"])


if __name__ == "__main__":
    unittest.main()
