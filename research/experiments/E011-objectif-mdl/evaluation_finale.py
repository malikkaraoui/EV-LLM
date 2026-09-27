"""E011 -- evaluation finale UNIQUE (test + adverses + validation) de tous les runs officiels.

Evaluateur E008 (evaluer / resume) importe tel quel. A lancer une seule fois, apres tous les runs.
Usage : python evaluation_finale.py   -> runs/<run>/resume.json
"""
import glob
import os

import numpy as np

from controles import tous_les_jeux
from donnees import ICI, ecrire_json, encode, lire_json
from evaluate import evaluer, resume  # E008
from rnn import predit


def main():
    jeux = tous_les_jeux()
    n = 0
    for chemin in sorted(glob.glob(os.path.join(ICI, "runs", "*-s[1-5]", "run.json"))):
        r = lire_json(chemin)
        th = np.array(r["theta_final"])
        res = resume(evaluer(lambda p: predit(th, p, encode), jeux, r["config"]))
        res.update({"config": r["config"], "graine": r["graine"]})
        ecrire_json(res, os.path.join(os.path.dirname(chemin), "resume.json"))
        n += 1
    print(f"{n} runs evalues")


if __name__ == "__main__":
    main()
