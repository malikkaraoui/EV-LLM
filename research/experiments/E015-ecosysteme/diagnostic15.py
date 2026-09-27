"""E015 -- diagnostic POST HOC (non preenregistre), sur des lots d'entrainement neufs (pas TEST).

Lecon L-E012-2 : avant d'accuser l'objectif, calculer sa valeur sur la solution connue.
Pour chaque run N1 : score du juge (lot de 1 024 items neufs) du programme rendu, et de la solution
ecrite a la main (cablage ECH0 + meilleur champion M-SOMME de la bibliotheque, adaptateurs identite).
Sortie : resultats/diagnostic.json
"""
import json
import os

import numpy as np

import programmes as PG
from compose import charge_lib, json_prog
from d15 import EGAL, PLUS, lot_train

ICI = os.path.dirname(os.path.abspath(__file__))
ID = np.array(list(range(10)) + [0, 0, 0, 10])


def solution(lib):
    somme = [i for i, c in enumerate(lib) if c["niche"].startswith("M-SOMME")]
    c = max(somme, key=lambda i: lib[i]["val"])
    return {"ins": [{"op": "DEC", "r": [0], "v": PLUS}, {"op": "DEC", "r": [2], "v": EGAL},
                    {"op": "INV", "r": [1]}, {"op": "INV", "r": [3]},
                    {"op": "CH", "c": c, "r": [5, 6], "A": [ID, ID]},
                    {"op": "INV", "r": [7]}], "sortie": 8}


def main():
    out = {}
    for cond in ["EVO", "ALEA", "SANSVIE", "ECH0", "ECH1", "ECH2"]:
        for g in range(1, 6):
            run = f"{cond}-N1-s{g}"
            lib = charge_lib(g)
            items = lot_train("N1", g, 7_000_000, 1024)
            rendu = json_prog(os.path.join(ICI, "runs", run, "resultat.json"))
            s_r, e_r = PG.score(PG.executer(rendu, lib, items, "N1")[0], items, "N1")
            s_s, e_s = PG.score(PG.executer(solution(lib), lib, items, "N1")[0], items, "N1")
            out[run] = {"score_rendu": round(s_r, 4), "exact_rendu": e_r,
                        "score_solution": round(s_s, 4), "exact_solution": e_s}
            print(f"{run:14s} rendu {s_r:.3f} (exact {e_r:.3f}) | solution connue {s_s:.3f} "
                  f"(exact {e_s:.3f})")
    # reutilisation : programme ECH0-N1 retenu, applique tel quel a N2 / N3 ; solutions connues
    from d15 import MOINS
    copie_a = {"ins": [{"op": "DEC", "r": [0], "v": PLUS}], "sortie": 1}
    for g in range(1, 6):
        lib = charge_lib(g)
        src = json_prog(os.path.join(ICI, "runs", f"ECH0-N1-s{g}", "resultat.json"))
        sol = solution(lib)
        c_succ = max([i for i, c in enumerate(lib) if c["niche"].startswith("M-SUCC")],
                     key=lambda i: lib[i]["val"])
        compl = np.array([9 - d for d in range(10)] + [0, 0, 0, 9])
        sol3 = PG.copie(sol)
        sol3["ins"][0]["v"] = MOINS
        sol3["ins"][4]["A"][1] = compl
        sol3["ins"] = sol3["ins"][:5] + [{"op": "CH", "c": c_succ, "r": [7], "A": [ID]},
                                         {"op": "TRQ", "r": [8]}, {"op": "INV", "r": [9]}]
        sol3["sortie"] = 10
        n1_v3 = PG.copie(src)
        n1_v3["ins"][0]["v"] = MOINS
        cs = sol["ins"][4]["c"]
        sol2 = {"ins": [{"op": "DEC", "r": [0], "v": PLUS}, {"op": "DEC", "r": [2], "v": PLUS},
                        {"op": "DEC", "r": [4], "v": EGAL}, {"op": "INV", "r": [1]},
                        {"op": "INV", "r": [3]}, {"op": "INV", "r": [5]},
                        {"op": "CH", "c": cs, "r": [7, 8], "A": [ID, ID]},
                        {"op": "CH", "c": cs, "r": [10, 9], "A": [ID, ID]},
                        {"op": "INV", "r": [11]}], "sortie": 12}
        for t, progs in (("N2", {"n1_tel_quel": src, "copie_a": copie_a, "solution_connue": sol2}),
                         ("N3", {"n1_tel_quel": src, "n1_coupe_moins": n1_v3,
                                 "copie_a": dict(copie_a, ins=[dict(copie_a["ins"][0], v=MOINS)]),
                                 "solution_connue": sol3})):
            items = lot_train(t, g, 7_000_000, 1024)
            for nom, p in progs.items():
                s_, e_ = PG.score(PG.executer(p, lib, items, t)[0], items, t)
                out[f"reutil-{t}-s{g}-{nom}"] = {"score": round(s_, 4), "exact": e_}
                print(f"{t} s{g} {nom:16s} score {s_:.3f} exact {e_:.3f}")
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    json.dump(out, open(os.path.join(ICI, "resultats", "diagnostic.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
