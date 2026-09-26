#!/usr/bin/env python3
"""Genere cases.json (E006) -- corpus preenregistre, meme schema qu'E001/E005. Stdlib.

Groupes (champ `groupe`) et nombre cible de reponses HTTP 200 par cas (champ `cible`) :
- R  replication : les 6 cas « faux et sur » d'E005, recopies a l'identique (assertion) ;
- C  contamination (E004) : 4 paires minimales avec / sans contradiction independante ;
- L  frontiere : chaine transitive de 2 a 6 pas ; T1-A avec 0, 1, 2 distracteurs
     (le point a 3 distracteurs est R-F4-01, etat identique -- assertion) ;
- P  paires minimales : forme correcte en regard de F1-04 / F1-05 / F1-08.
L'ordre des cas dans le fichier est l'ordre d'appel (R, C, L, P), fixe avant tout appel.
"""
import json
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
E001 = HERE.parent / "E001-jev-sonde" / "cases.json"
E005 = HERE.parent / "E005-jev-hors-distribution" / "cases.json"

R1 = "Regle 1 : si X > Y et Y > Z alors X > Z."
R2 = "Regle 2 : si incompatible(X, Y) alors ni X > Y ni Y > X."
R3 = "Regle 3 : si couleur(X, bleu) alors X > D."


def boolq(txt):
    return {"type": "boolean",
            "instructions": "Peut-on deduire {} uniquement a partir des faits et regles donnes ?".format(txt)}


def load(path):
    return {c["id"]: c for c in json.loads(path.read_text(encoding="utf-8"))["cases"]}


e001, e005 = load(E001), load(E005)
cases = []

# --- R : replication, a l'identique -------------------------------------------------------
for src in ("F1-04", "F1-05", "F1-08", "F3-02", "F4-01", "F4-04"):
    o = e005[src]
    c = {"id": "R-" + src, "famille": "R-replication", "groupe": "R", "cible": 5,
         "state": o["state"], "questions": o["questions"], "attendu": o["attendu"],
         "justification": o["justification"], "source": "E005/cases.json:" + src}
    for k in ("state", "questions", "attendu", "justification"):
        assert c[k] == o[k], (src, k)
    if src == "F3-02":
        c["note"] = "Attente a confirmer (doublage R004) ; recopiee sans modification."
    cases.append(c)

# --- C : contamination, paires minimales (une lettre change) -------------------------------
BLOC_AVEC = "A > B. B > C. incompatible(A, C)."   # A > C deduit en 1 pas : R2 violee
BLOC_SANS = "A > B. B > C. incompatible(A, D)."   # D n'apparait nulle part ailleurs
DIRECT_AVEC = "A > B. incompatible(A, B)."         # violation directe d'un fait
DIRECT_SANS = "A > B. incompatible(A, C)."
PAIRES = [
    # (id, faits de la deduction, question, bloc avec, bloc sans, bloc avant ?, justification)
    ("C1", "P > Q. Q > R.", "P > R", BLOC_AVEC, BLOC_SANS, False,
     "P > R en 1 pas, sous-graphe disjoint ; contradiction deduite (A > C) apres la deduction"),
    ("C2", "P > Q. Q > R. R > S.", "P > S", BLOC_AVEC, BLOC_SANS, False,
     "P > S en 2 pas, sous-graphe disjoint ; contradiction deduite (A > C) apres la deduction"),
    ("C3", "P > Q. Q > R.", "P > R", DIRECT_AVEC, DIRECT_SANS, False,
     "P > R en 1 pas, sous-graphe disjoint ; contradiction directe (A > B et incompatible(A, B))"),
    ("C4", "P > Q. Q > R. R > S.", "P > S", BLOC_AVEC, BLOC_SANS, True,
     "P > S en 2 pas, sous-graphe disjoint ; contradiction deduite placee avant la deduction"),
]
for pid, deduc, q, avec, sans, avant, why in PAIRES:
    for membre, bloc in (("avec", avec), ("sans", sans)):
        faits = "{} {}".format(bloc, deduc) if avant else "{} {}".format(deduc, bloc)
        cases.append({
            "id": "{}-{}".format(pid, membre), "famille": "C-contamination", "groupe": "C",
            "cible": 5, "paire": pid, "membre": membre,
            "state": "Faits : {} {} {}".format(faits, R1, R2),
            "questions": {"deduction": boolq(q)}, "attendu": {"deduction": True},
            "justification": "{} ; membre {} ({}).".format(
                why, membre, "R2 violee ailleurs" if membre == "avec" else "aucune regle violee")})

# --- L : frontiere en nombre de pas (faits melanges, ordre fixe par graine = k) -----------
LETTRES = "ABCDEFGH"
for k in range(2, 7):
    noeuds = LETTRES[:k + 2]                      # k pas de regle 1 = k + 1 faits
    faits = ["{} > {}".format(a, b) for a, b in zip(noeuds, noeuds[1:])]
    random.Random(k).shuffle(faits)
    if k == 4:
        # paire minimale avec R-F4-04 : meme ordre des faits, sans incompatible(A, F) ni R2
        faits = [f for f in e005["F4-04"]["state"][len("Faits : "):].split(" Regle")[0].split(". ")
                 if " > " in f]
    cases.append({
        "id": "L-PAS{}".format(k), "famille": "L-frontiere-pas", "groupe": "L", "cible": 3,
        "pas": k,
        "state": "Faits : {}. {}".format(". ".join(faits), R1),
        "questions": {"deduction": boolq("{} > {}".format(noeuds[0], noeuds[-1]))},
        "attendu": {"deduction": True},
        "justification": "Chaine de {} faits melanges, {} > {} en {} applications de R1, sans R2.".format(
            k + 1, noeuds[0], noeuds[-1], k)})
    if k == 4:
        assert cases[-1]["state"] == e005["F4-04"]["state"].replace(" incompatible(A, F).", "").replace(" " + R2, "")

# --- L : frontiere en nombre de distracteurs autour de T1-A (E001) --------------------------
t1a = e001["T1-A"]
DISTRACTEURS = [
    t1a["state"],
    t1a["state"].replace("E > A. ", "E > A. A > C. "),
    t1a["state"].replace("E > A. ", "E > A. A > C. ") + " " + R3,
]
d3 = t1a["state"].replace("E > A. ", "E > A. A > C. couleur(A, rouge). ") + " " + R3
assert d3 == e005["F4-01"]["state"], "le point a 3 distracteurs doit etre F4-01"
assert e005["F4-01"]["questions"] == t1a["questions"] and e005["F4-01"]["attendu"] == t1a["attendu"]
POURQUOI = ["T1-A d'E001 a l'identique (0 distracteur).",
            "T1-A + fait redondant A > C (1 distracteur).",
            "T1-A + A > C + regle 3 non pertinente (aucune couleur) (2 distracteurs)."]
for d, st in enumerate(DISTRACTEURS):
    cases.append({"id": "L-DIS{}".format(d), "famille": "L-frontiere-distracteurs", "groupe": "L",
                  "cible": 3, "distracteurs": d, "state": st, "questions": t1a["questions"],
                  "attendu": t1a["attendu"],
                  "justification": POURQUOI[d] + " E > D deduit, R2 violee."})
assert cases[-3]["state"] == t1a["state"]

# --- P : paires minimales, forme correcte ---------------------------------------------------
for pid, src, phrase, why in [
        ("P-F1-04", "F1-03", None, "Forme correcte de F1-04 (= F1-03 d'E005) : « se » COI, PP invariable."),
        ("P-F1-05", None, "Ils se sont parlé pendant des heures.",
         "Forme correcte de F1-05 : parler a quelqu'un, « se » COI, PP invariable."),
        ("P-F1-08", "F1-07", None, "Forme correcte de F1-08 (= F1-07 d'E005) : « fait » + infinitif invariable.")]:
    base = e005["F1-04"]
    state = e005[src]["state"] if src else "Phrase ecrite par un eleve : « {} »".format(phrase)
    cases.append({"id": pid, "famille": "P-paire-minimale", "groupe": "P", "cible": 3,
                  "paire_de": "R-" + pid[2:], "state": state, "questions": base["questions"],
                  "attendu": {"correcte": True}, "justification": why})
    if src:
        assert e005[src]["attendu"] == {"correcte": True} and e005[src]["questions"] == base["questions"]

ids = [c["id"] for c in cases]
assert len(ids) == len(set(ids))
out = {"preregistre_le": "2026-09-26",
       "note": ("Corpus E006 preenregistre (M0011). Attentes fixees avant tout appel ; "
                "R recopie E005 a l'identique ; L-DIS3 = R-F4-01 (etat identique)."),
       "cases": cases}
(HERE / "cases.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(cases), "cas,", sum(len(c["questions"]) for c in cases), "questions,",
      sum(c["cible"] for c in cases), "reponses 200 visees")
