"""E016 -- evaluation finale (TEST lu une seule fois) des 9 paires de chaque (condition, graine).

  python evalue16.py --conds DONNE COLL IND COUPE --graines 1 2 3 4 5

Un fichier par (condition, graine) dans resultats/eval/ : relancer reprend la ou l'on s'est arrete
(budget par invocation). DONNE = interface exacte, aucun entrainement (codes prives de la graine).
Confiance = min des probabilites des choix argmax (symbole, jeton, chiffre d'I1).
"""
import argparse
import json
import os
import time

import numpy as np

from m16 import D, Population

ICI = os.path.dirname(os.path.abspath(__file__))
TAUS = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
SUR = 0.8


def seuil_abstention(conf_justes):
    """Plus grand tau tel que <= 5 % des reponses justes aient conf < tau (regle E014)."""
    x = np.asarray(conf_justes)
    ok = [t for t in TAUS if len(x) and np.mean(x < t) <= 0.05]
    return max(ok) if ok else None


def evalue_paire(pop, i, j, jeux):
    f = pop.systeme(i, j)
    out = {}
    for jeu, par_l in jeux.items():
        for L, paires in sorted(par_l.items()):
            r = f(paires)
            out[f"{jeu}|{L}"] = dict(juste=[x == str(a + b) for (a, b), (x, _) in zip(paires, r)],
                                     conf=[round(c, 5) for _, c in r])
    return out


def un_systeme(cond, g, t_fin):
    dossier = os.path.join(ICI, "resultats", "eval")
    os.makedirs(dossier, exist_ok=True)
    f = os.path.join(dossier, f"{cond}-s{g}.json")
    res = json.load(open(f)) if os.path.exists(f) else {"paires": {}}
    if res.get("fini"):
        return True
    pop = Population(g, coupe=(cond == "COUPE"))
    if cond == "DONNE":
        pop.interface_donnee()
    else:
        pop.t.load_weights(os.path.join(ICI, "runs", f"{cond}-s{g}", "meilleur.safetensors"))
    res["C"] = pop.indice_commun()
    res["lexique"], dec = pop.lexique()
    res["decodage"] = dec
    jeux = dict(D.jeu_val(), **D.jeux_test())
    for i in range(3):
        for j in range(3):
            k = f"A{i + 1}B{j + 1}"
            if k in res["paires"]:
                continue
            t0 = time.time()
            res["paires"][k] = evalue_paire(pop, i, j, jeux)
            json.dump(res, open(f, "w"))
            print(f"  {cond} s{g} {k} : T-LONG|16 {np.mean(res['paires'][k]['T-LONG|16']['juste']):.3f} "
                  f"|100 {np.mean(res['paires'][k]['T-LONG|100']['juste']):.3f} ({time.time() - t0:.0f} s)",
                  flush=True)
            if time.time() > t_fin:
                return False
    res["fini"] = True
    json.dump(res, open(f, "w"))
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conds", nargs="+", required=True)
    ap.add_argument("--graines", nargs="+", type=int, required=True)
    ap.add_argument("--budget-min", type=float, default=8.5)
    a = ap.parse_args()
    t_fin = time.time() + 60 * a.budget_min
    for cond in a.conds:
        for g in a.graines:
            if not un_systeme(cond, g, t_fin):
                print("ARRET (budget), relancer pour reprendre", flush=True)
                return
    print("TERMINE", flush=True)


if __name__ == "__main__":
    main()
