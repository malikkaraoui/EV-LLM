"""E009-bis -- DIAGNOSTIC HORS PROTOCOLE (apres le test final, ne sert a aucun choix).

Systemes a arret par confiance (A2-L, A3) : T-ID (2-5, 200 / L) et VAL 6 (100) avec un nombre
d'iterations FIXE t (au lieu de l'arret par confiance maximale, plafond 512). Separe
« le reseau ne sait pas » de « la regle d'arret choisit la mauvaise iteration ».
"""
import os

import numpy as np

import curric as C
from bande import ecrire_json, lire_json, sous_val  # E009
from evaluate import evaluer, resume  # E008
from evalue import systeme_appris  # E009
from evalue_bis import charge

ICI = os.path.dirname(os.path.abspath(__file__))


def fixe(modele, t):
    import boucle
    f = systeme_appris(modele, "t_n", True)

    def g(paires):  # A3-T-like : meme bande, t iterations pour tous
        vieux = C.b9.t_de_n
        C.b9.t_de_n = lambda a, b: t
        try:
            return f(paires)
        finally:
            C.b9.t_de_n = vieux
    return g


out = {}
jeux = {**C.t_id(range(2, 6), 200), "VAL": {6: sous_val(100)["VAL"][6]}}
for run in ("A2-L-s1", "A3-s1", "A3-s2"):
    d = os.path.join(ICI, "runs", run)
    e = lire_json(os.path.join(d, "etat.json"))
    m = charge(e, d, "meilleur.safetensors" if e["appris"] else "poids.safetensors")
    for t in (8, 16, 24, 32):
        r = resume(evaluer(fixe(m, t), jeux, run))["par_jeu"]
        out[f"{run}|t={t}"] = {k: c["exact"] for k, c in r.items()}
        print(run, f"t={t:2d}", " ".join(f"{k}={c['exact']:.3f}" for k, c in sorted(r.items())))
ecrire_json(out, os.path.join(ICI, "resultats", "diagnostic_iterations.json"))
