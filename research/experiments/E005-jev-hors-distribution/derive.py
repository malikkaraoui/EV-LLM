#!/usr/bin/env python3
"""Derive mecaniquement un sous-corpus de cases.json : cas recopies tels quels.

Usage : python3 derive.py <sortie.json> <id> [<id> ...]
Aucune attente n'est modifiee ; aggregate.py (E001) reverifie state/questions.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
src_bytes = (HERE / "cases.json").read_bytes()
src = json.loads(src_bytes)
ids = sys.argv[2:]
by_id = {c["id"]: c for c in src["cases"]}
sub = [dict(by_id[i], derive_de="cases.json@" + hashlib.sha256(src_bytes).hexdigest()[:12]) for i in ids]
for s in sub:
    o = by_id[s["id"]]
    assert all(s[k] == o[k] for k in o), s["id"]
Path(sys.argv[1]).write_text(json.dumps({"preregistre_le": src["preregistre_le"],
                                         "note": "Sous-corpus derive mecaniquement de cases.json.",
                                         "cases": sub}, ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")
print(len(sub), "cas ->", sys.argv[1])
