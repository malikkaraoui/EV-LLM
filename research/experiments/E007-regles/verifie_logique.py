#!/usr/bin/env python3
"""Recalcule mecaniquement les attentes logiques (groupes A, B, D logiques) de cases.json, sans Jev.

Chaque phrase « Regle n : ... » est reconnue par son texte exact ; une phrase non reconnue (hors
sujet) n'a aucun effet. Semantique :
- R1      : X > Y et Y > Z  =>  X > Z          (fermeture)
- R1 inv. : X > Y et Y > Z  =>  Z > X          (fermeture)
- R2      : violee si un couple incompatible est ordonne (dans un sens ou l'autre)
- R2 inv. : violee si un couple incompatible n'est ordonne dans aucun sens
- R3      : couleur(X, bleu) => X > D
statut = contradiction si une regle est violee, sinon coherent. Question « deduire X > Y » : vrai
ssi (X, Y) est dans la fermeture. Sort en code 1 si une attente preenregistree differe.
`--mutation` : inverse une attente en memoire et verifie que l'ecart est detecte.
"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gen_cases as G  # noqa: E402  (textes des regles ; import sans reecriture de cases.json)

REGLES_CONNUES = {G.R1: "R1", G.R1_INV: "R1_INV", G.R2: "R2", G.R2_INV: "R2_INV", G.R3: "R3"}


def calcule(case):
    st = case["state"]
    faits = st.split("Regle")[0]
    regles = {nom for txt, nom in REGLES_CONNUES.items() if txt in st}
    rel = set(re.findall(r"\b([A-Z]) > ([A-Z])\b", faits))
    inc = re.findall(r"incompatible\(([A-Z]), ([A-Z])\)", faits)
    if "R3" in regles:
        rel |= {(x, "D") for x in re.findall(r"couleur\(([A-Z]), bleu\)", faits)}
    while True:
        new = set()
        if "R1" in regles:
            new |= {(a, d) for a, b in rel for x, d in rel if b == x}
        if "R1_INV" in regles:
            new |= {(d, a) for a, b in rel for x, d in rel if b == x}
        new -= rel
        if not new:
            break
        rel |= new
    ordonne = [(x, y) in rel or (y, x) in rel for x, y in inc]
    viole = ("R2" in regles and any(ordonne)) or ("R2_INV" in regles and not all(ordonne))
    calc = {}
    for qid, q in case["questions"].items():
        if qid == "statut":
            calc[qid] = "contradiction" if viole else "coherent"
        else:
            x, y = re.search(r"deduire ([A-Z]) > ([A-Z])", q["instructions"]).groups()
            calc[qid] = (x, y) in rel
    return calc


def main(argv):
    cases = json.loads((HERE / "cases.json").read_text(encoding="utf-8"))["cases"]
    logiques = [c for c in cases if c["state"].startswith("Faits : ")]
    if "--mutation" in argv:
        c = logiques[0]
        q = next(iter(c["attendu"]))
        v = c["attendu"][q]
        c["attendu"][q] = (not v) if isinstance(v, bool) else ("coherent" if v != "coherent" else "contradiction")
    bad = 0
    for c in logiques:
        calc = calcule(c)
        ok = calc == c["attendu"]
        bad += not ok
        print("{} calcule {} attendu {} -> {}".format(c["id"], calc, c["attendu"], "OK" if ok else "ECART"))
    print("{} cas logiques verifies, {} ecart(s)".format(len(logiques), bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
