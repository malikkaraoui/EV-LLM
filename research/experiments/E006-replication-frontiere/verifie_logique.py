#!/usr/bin/env python3
"""Recalcule mecaniquement les attentes logiques (R-F4, C, L) de cases.json, sans Jev (stdlib).

Meme algorithme que E005/verifie_logique.py (fermeture transitive par la regle 1, R2 violee si
un couple incompatible est ordonne). Sort en code 1 si une attente preenregistree differe.
"""
import json
import re
import sys
from pathlib import Path

cases = json.loads((Path(__file__).resolve().parent / "cases.json").read_text(encoding="utf-8"))["cases"]
bad = n = 0
for c in cases:
    if c["groupe"] not in "CL" and not c["id"].startswith("R-F4"):
        continue
    n += 1
    faits = c["state"].split("Regle")[0]
    rel = set(re.findall(r"\b([A-Z]) > ([A-Z])\b", faits))
    inc = re.findall(r"incompatible\(([A-Z]), ([A-Z])\)", faits)
    while True:
        new = {(a, d) for a, b in rel for x, d in rel if b == x} - rel
        if not new:
            break
        rel |= new
    viole = "Regle 2" in c["state"] and any((x, y) in rel or (y, x) in rel for x, y in inc)
    calc = {}
    for qid, q in c["questions"].items():
        if qid == "statut":
            calc[qid] = "contradiction" if viole else "coherent"
        else:
            x, y = re.search(r"deduire ([A-Z]) > ([A-Z])", q["instructions"]).groups()
            calc[qid] = (x, y) in rel
    # paires C : le membre « avec » doit violer R2, le membre « sans » non
    if c["groupe"] == "C" and viole != (c["membre"] == "avec"):
        calc["_membre"] = "viole={} incoherent avec membre={}".format(viole, c["membre"])
    ok = calc == c["attendu"]
    bad += not ok
    print("{} calcule {} attendu {} -> {}".format(c["id"], calc, c["attendu"], "OK" if ok else "ECART"))
print("{} cas logiques verifies, {} ecart(s)".format(n, bad))
sys.exit(1 if bad else 0)
