"""E012 -- evaluation finale UNIQUE (validation + test + adverses) des runs officiels (graines 1-5).

Evaluateur E008 (evaluer / resume) importe tel quel. A lancer une seule fois, apres toutes les recherches.
Usage : python evaluation_e012.py   -> runs/<exp>-s<g>/resume.json
"""
import glob
import os

from jeux import EXPERIENCES, ICI, ecrire_json, encodeur, lire_json
from evaluate import evaluer, resume  # E008
from recherche import depuis_json
from reseau import longueur_G, lisible, preuve_aligne, systeme, taille
from verifs import tous_les_jeux


def main():
    n = 0
    for chemin in sorted(glob.glob(os.path.join(ICI, "runs", "*-s[1-5]", "run.json"))):
        r = lire_json(chemin)
        exp, cfg = r["exp"], EXPERIENCES[r["exp"]]
        g = depuis_json(r["genome"])
        jeux = tous_les_jeux(cfg["base"])
        res = resume(evaluer(systeme(g, cfg, encodeur(exp)), jeux, exp))
        preuve = (preuve_aligne(g, cfg["base"]) if cfg["format"] == "aligne"
                  else ("SANS_OBJET", "format plat"))
        res.update({"exp": exp, "graine": r["graine"], "G_bits": longueur_G(g), **taille(g),
                    "preuve": preuve, "circuit": lisible(g)})
        ecrire_json(res, os.path.join(os.path.dirname(chemin), "resume.json"))
        n += 1
        print(exp, r["graine"], preuve[0], taille(g))
    print(f"{n} runs evalues")


if __name__ == "__main__":
    main()
