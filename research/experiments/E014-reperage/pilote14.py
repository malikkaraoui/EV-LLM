"""E014 -- bilan du pilote (graine 0, exclue) : VAL-OOD (selection) et VAL-ID (en distribution).

  python pilote14.py  -> resultats/pilote.json
"""
import glob
import json
import os

import numpy as np

import d14 as D
from evaluate import evaluer, resume
from s14 import charge, lecture_exacte, systeme

ICI = os.path.dirname(os.path.abspath(__file__))


def main():
    out = {}
    for d in sorted(glob.glob(os.path.join(ICI, "runs", "*-s0-pilote-*"))):
        e = json.load(open(os.path.join(d, "etat.json")))
        m = charge(e["config"], os.path.join(d, "meilleur.safetensors"))
        if e["config"] == "R1L":
            vid = lecture_exacte(m, D.jeu_val_id())
        else:
            r = resume(evaluer(systeme(m), D.jeu_val_id(), "vid"))["par_jeu"]
            vid = float(np.mean([c["exact"] for c in r.values()]))
        out[os.path.basename(d)] = {"lr": e["lr"], "pas": e["pas_total"],
                                    "val_ood": e["meilleur_val"], "meilleur_pas": e["meilleur_pas"],
                                    "val_id": vid, "duree_s": e["duree_s"]}
        print(os.path.basename(d), out[os.path.basename(d)])
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    json.dump(out, open(os.path.join(ICI, "resultats", "pilote.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
