#!/usr/bin/env python3
"""Genere cases.json (E007) -- corpus preenregistre, meme schema qu'E001/E005/E006. Stdlib.

Question : Jev lit-il les regles ecrites, ou juge-t-il la plausibilite de surface de l'etat ?

Groupes (champ `groupe`) et nombre cible de reponses HTTP 200 par cas (champ `cible`) :
- D  controles triviaux (logique et grammaire), en premier pour detecter une passerelle en panne ;
- C  grammaire avec regle d'accord explicite : les 3 paires minimales d'E006 (forme fautive,
     forme correcte), la regle d'accord ecrite dans l'etat ; + rappel des formes correctes SANS
     regle (etat identique a E006, derive au cours du temps) ;
- A  ablation de regle (logique) : meme etat, variante (i) regle presente, (ii) retiree,
     (iii) inversee, (iv) remplacee par une phrase hors sujet de meme longueur (meme position),
     (v) regle presente + phrase hors sujet ajoutee ;
- B  distracteur neutre vs pertinent autour de T1-A : fait redondant seul, autre fait
     redondant seul, regle non pertinente seule, fait non pertinent seul (reference : A1-i = T1-A).
L'ordre des cas dans le fichier est l'ordre d'appel dans un groupe ; ordre des groupes : D, C, A, B.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
E001 = HERE.parent / "E001-jev-sonde" / "cases.json"
E006 = HERE.parent / "E006-replication-frontiere" / "cases.json"

R1 = "Regle 1 : si X > Y et Y > Z alors X > Z."
R1_INV = "Regle 1 : si X > Y et Y > Z alors Z > X."
R1_HS = "Regle 1 : la gare ferme chaque dimanche."
R2 = "Regle 2 : si incompatible(X, Y) alors ni X > Y ni Y > X."
R2_INV = "Regle 2 : si incompatible(X, Y) alors X > Y ou Y > X."
R2_HS = "Regle 2 : le marche du hameau ouvre chaque samedi matin."
R3 = "Regle 3 : si couleur(X, bleu) alors X > D."
R3_HS = "Regle 3 : le marche du hameau ouvre chaque samedi matin."
assert len(R1_HS) == len(R1) and len(R2_HS) == len(R2)


def boolq(txt):
    return {"type": "boolean",
            "instructions": "Peut-on deduire {} uniquement a partir des faits et regles donnes ?".format(txt)}


def load(path):
    return {c["id"]: c for c in json.loads(path.read_text(encoding="utf-8"))["cases"]}


e001, e006 = load(E001), load(E006)
t1a = e001["T1-A"]
assert t1a["state"] == e006["L-DIS0"]["state"]
Q_GRAM = e006["R-F1-04"]["questions"]
cases = []

# --- D : controles triviaux ------------------------------------------------------------------
BASE_D = "Faits : A > B. B > C. " + R1
for cid, state, q, att, why in [
        ("D-LOG-VRAI", BASE_D, {"deduction": boolq("A > C")}, {"deduction": True},
         "A > C en 1 application de R1."),
        ("D-LOG-FAUX", BASE_D, {"deduction": boolq("C > A")}, {"deduction": False},
         "C > A ne se deduit pas (R1 ne produit que A > C)."),
        ("D-GRAM-FAUX", "Phrase ecrite par un eleve : « Les enfants mange du pain. »", Q_GRAM,
         {"correcte": False}, "Accord sujet-verbe : « Les enfants mangent »."),
        ("D-GRAM-OK", "Phrase ecrite par un eleve : « Le chat dort sur le canapé. »", Q_GRAM,
         {"correcte": True}, "Phrase simple sans difficulte d'accord.")]:
    cases.append({"id": cid, "famille": "D-controle", "groupe": "D", "cible": 3,
                  "state": state, "questions": q, "attendu": att, "justification": why})

# --- C : grammaire, regle d'accord ecrite dans l'etat -----------------------------------------
# Sources des regles (accord du participe passe) : Grevisse & Goosse, « Le Bon Usage » (accord
# du participe passe des verbes pronominaux ; participe passe suivi d'un infinitif) ;
# Bescherelle, « La grammaire pour tous ». Numeros de paragraphe non cites (non verifies ici).
REGLES = {
    "F1-04": ("Règle d'accord : quand un verbe pronominal a un complément d'objet direct placé "
              "après lui (ex. « se laver les mains »), « se » est complément indirect et le "
              "participe passé ne s'accorde pas."),
    "F1-05": ("Règle d'accord : dans « se parler » (parler à quelqu'un), « se » est complément "
              "indirect et le participe passé reste invariable."),
    "F1-08": ("Règle d'accord : le participe passé « fait » suivi d'un infinitif est toujours "
              "invariable."),
}
SOURCE = ("Regle standard d'accord du participe passe (Grevisse & Goosse, Le Bon Usage ; "
          "Bescherelle, La grammaire pour tous).")
for src, regle in REGLES.items():
    for forme, orig in (("fautive", "R-" + src), ("correcte", "P-" + src)):
        o = e006[orig]
        assert o["state"].startswith("Phrase ecrite par un eleve : « ") and o["questions"] == Q_GRAM
        cases.append({"id": "C-{}-{}".format(src, forme), "famille": "C-regle-explicite",
                      "groupe": "C", "cible": 5, "paire": src, "forme": forme, "regle": True,
                      "sans_regle_e006": orig,
                      "state": "{} {}".format(regle, o["state"]), "questions": Q_GRAM,
                      "attendu": o["attendu"],
                      "justification": "{} + regle d'accord ecrite avant la phrase. {} Source : {}".format(
                          orig, o["justification"], SOURCE)})
for src in REGLES:
    o = e006["P-" + src]
    cases.append({"id": "C0-{}-correcte".format(src), "famille": "C-rappel-sans-regle",
                  "groupe": "C", "cible": 2, "paire": src, "forme": "correcte", "regle": False,
                  "sans_regle_e006": "P-" + src, "state": o["state"], "questions": o["questions"],
                  "attendu": o["attendu"],
                  "justification": "Rappel de P-{} d'E006 (etat identique, sans regle) : derive dans le temps.".format(src)})

# --- A : ablation de regle -------------------------------------------------------------------
# A1 : T1-A, on manipule R2 (la regle qui cree la contradiction).
# A2 : chaine A > B > C > D, on manipule R1 (la regle qui cree la deduction).
A1_FAITS = "Faits : A > B. B > C. C > D. E > A. incompatible(D, E)."
assert "{} {} {}".format(A1_FAITS, R1, R2) == t1a["state"]
A2_FAITS = "Faits : A > B. B > C. C > D."
VARIANTES = [
    # (suffixe, description, A1 regles, A1 attendu statut, A2 regles, A2 attendu)
    ("i", "regle presente", [R1, R2], "contradiction", [R1], True),
    ("ii", "regle retiree", [R1], "coherent", [], False),
    ("iii", "regle inversee", [R1, R2_INV], "coherent", [R1_INV], False),
    ("iv", "regle remplacee par une phrase hors sujet de meme longueur", [R1, R2_HS], "coherent", [R1_HS], False),
    ("v", "regle presente + phrase hors sujet ajoutee", [R1, R2, R3_HS], "contradiction", [R1, R2_HS], True),
]
for suf, desc, r_a1, st_a1, r_a2, att_a2 in VARIANTES:
    cases.append({"id": "A1-" + suf, "famille": "A-ablation", "groupe": "A", "cible": 3,
                  "base": "A1", "variante": suf, "regle_manipulee": "R2",
                  "state": " ".join([A1_FAITS] + r_a1), "questions": t1a["questions"],
                  "attendu": {"statut": st_a1, "e_sup_d": True},
                  "justification": ("T1-A, R2 : {}. E > D se deduit par R1 dans toutes les variantes. "
                                    "Statut attendu {}.").format(desc, st_a1)})
    cases.append({"id": "A2-" + suf, "famille": "A-ablation", "groupe": "A", "cible": 3,
                  "base": "A2", "variante": suf, "regle_manipulee": "R1",
                  "state": " ".join([A2_FAITS] + r_a2), "questions": {"deduction": boolq("A > D")},
                  "attendu": {"deduction": att_a2},
                  "justification": "Chaine A > B > C > D, R1 : {}. A > D {}.".format(
                      desc, "se deduit (2 pas)" if att_a2 else "ne se deduit pas des regles donnees")})
# A2-v : R1 presente + phrase hors sujet ajoutee (numerotee Regle 2, aucune autre regle 2 dans A2)
assert [c for c in cases if c["id"] == "A2-v"][0]["state"] == "{} {} {}".format(A2_FAITS, R1, R2_HS)
assert [c for c in cases if c["id"] == "A1-i"][0]["state"] == t1a["state"]

# --- B : distracteur neutre vs pertinent (reference : A1-i = T1-A) -----------------------------
BLOCS = [
    ("B-FAIT", "E > A. A > C. ", None, "fait redondant A > C (deductible), sans regle (= L-DIS1 d'E006)"),
    ("B-FAIT2", "E > A. B > D. ", None, "autre fait redondant B > D (deductible), sans regle"),
    ("B-REGLE", "E > A. ", R3, "regle 3 non pertinente (aucune couleur), sans fait"),
    ("B-NEUTRE", "E > A. couleur(A, rouge). ", None, "fait non pertinent couleur(A, rouge), sans regle"),
]
for cid, rempl, regle, why in BLOCS:
    st = t1a["state"].replace("E > A. ", rempl)
    if regle:
        st += " " + regle
    cases.append({"id": cid, "famille": "B-distracteur", "groupe": "B", "cible": 3,
                  "state": st, "questions": t1a["questions"], "attendu": t1a["attendu"],
                  "justification": "T1-A + {}. E > D deduit, R2 violee.".format(why)})
assert cases[-4]["state"] == e006["L-DIS1"]["state"]

ids = [c["id"] for c in cases]
assert len(ids) == len(set(ids))
out = {"preregistre_le": "2026-09-26",
       "note": ("Corpus E007 preenregistre (M0017). Attentes fixees avant tout appel ; "
                "A1-i = T1-A d'E001 ; B-FAIT = L-DIS1 d'E006 ; C reprend les etats d'E006 + regle."),
       "cases": cases}
if __name__ == "__main__":
    (HERE / "cases.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(len(cases), "cas,", sum(len(c["questions"]) for c in cases), "questions,",
          sum(c["cible"] for c in cases), "reponses 200 visees")
