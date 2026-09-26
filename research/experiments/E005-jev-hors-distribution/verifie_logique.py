#!/usr/bin/env python3
"""Recalcule mecaniquement les attentes logiques (F4, F5) de cases.json, sans Jev (stdlib).

Parse les faits « X > Y » et « incompatible(X, Y) » de chaque state, ferme par transitivite
(regle 1), puis derive statut (contradiction / coherent / indetermine) et les questions
« Peut-on deduire X > Y ». Sort en code 1 si une attente preenregistree differe.
"""
import json
import re
import sys
from pathlib import Path

cases = json.loads((Path(__file__).resolve().parent / "cases.json").read_text(encoding="utf-8"))["cases"]
bad = 0
for c in cases:
    if not c["id"].startswith(("F4", "F5-01")):
        continue
    faits = c["state"].split("Regle")[0]
    rel = set(re.findall(r"\b([A-Z]) > ([A-Z])\b", faits))
    inc = re.findall(r"incompatible\(([A-Z]), ([A-Z])\)", faits)
    while True:
        new = {(a, d) for a, b in rel for x, d in rel if b == x} - rel
        if not new:
            break
        rel |= new
    calc = {}
    for qid, q in c["questions"].items():
        if qid == "statut":
            if "Aucune regle ne definit ce que signifie incompatible" in c["state"]:
                calc[qid] = "indetermine"
            elif "Regle 2" in c["state"] and any((x, y) in rel or (y, x) in rel for x, y in inc):
                calc[qid] = "contradiction"
            else:
                calc[qid] = "coherent"
        else:
            x, y = re.search(r"deduire ([A-Z]) > ([A-Z])", q["instructions"]).groups()
            calc[qid] = (x, y) in rel
    ok = calc == c["attendu"]
    bad += not ok
    print("{} calcule {} attendu {} -> {}".format(c["id"], calc, c["attendu"], "OK" if ok else "ECART"))
sys.exit(1 if bad else 0)
