"""E010 -- agregation : resultats/resultats.json, summary.md, courbe.csv.

  python analyse.py
"""
import csv
import glob
import json
import os
from collections import defaultdict

import numpy as np

from donnees import ecrire_json, lire_json

ICI = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(ICI, "resultats")


def charge(fichier):
    out = []
    for f in sorted(glob.glob(os.path.join(ICI, "runs", "*", fichier))):
        if "_lr" in f or "-s0" in f:
            continue  # pilote exclu
        out.append(lire_json(f))
    return out


def cle_tri(k):
    j, L = k.split("|")
    return (j, int(L))


def agrege(runs):
    par_cond = defaultdict(list)
    for r in runs:
        par_cond[f"{r['format']}-{r['positions']}"].append(r)
    out = {}
    for cond, rs in sorted(par_cond.items()):
        rs = sorted(rs, key=lambda r: r["graine"])
        jeux = sorted(rs[0]["par_jeu"], key=cle_tri)
        d = {"graines": [r["graine"] for r in rs], "par_jeu": {}}
        for k in jeux:
            v = [r["par_jeu"][k]["exact"] for r in rs]
            faux = sum(r["par_jeu"][k]["faux"] for r in rs)
            d["par_jeu"][k] = {
                "moy": float(np.mean(v)), "ecart": float(np.std(v, ddof=1)) if len(v) > 1 else 0.0,
                "par_graine": v, "faux": faux,
                "faux_surs": sum(r["par_jeu"][k]["faux_surs"] for r in rs),
                "abstentions": sum(r["par_jeu"][k]["abstentions"] for r in rs),
                "traces_justes": sum(r["par_jeu"][k]["traces_justes"] for r in rs),
                "coherents": sum(r["par_jeu"][k]["coherents"] for r in rs),
                "n": sum(r["par_jeu"][k]["n"] for r in rs)}
        t16 = [r["par_jeu"].get("T-FIN|16", {}).get("exact") for r in rs]
        d["graines_reussies_16"] = sum(1 for x in t16 if x is not None and x >= 0.9)
        out[cond] = d
    return out


def main():
    os.makedirs(RES, exist_ok=True)
    finals = charge("final.json")
    cribles = charge("crible.json")
    etats = charge("etat.json")
    calcul = sum(e["calcul_s"] for e in etats)
    pilote = sum(v["calcul_s"] for v in lire_json(os.path.join(RES, "pilote.json")).values())

    # courbe d'efficacite (criblage, graine 1, T-ID 200/L + V-OOD 200/L)
    lignes = []
    for r in cribles:
        if r["graine"] != 1 or r["format"] not in ("F0", "F1"):
            continue
        tid = np.mean([r["par_jeu"][f"T-ID|{L}"]["exact"] for L in (2, 3, 4, 5)])
        lignes.append({"condition": f"{r['format']}-{r['positions']}", "N": r["N"],
                       "uniques_vus": r["uniques_vus"], "pas": r["pas"], "T-ID_moy": tid,
                       **{f"V-OOD{L}": r["par_jeu"][f"V-OOD|{L}"]["exact"] for L in (6, 7, 8)}})
    lignes.sort(key=lambda x: (x["condition"], x["N"]))
    with open(os.path.join(RES, "courbe.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(lignes[0]))
        w.writeheader()
        for l in lignes:
            w.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in l.items()})
    besoin = {}
    for cond in sorted({l["condition"] for l in lignes}):
        ok = [l["N"] for l in lignes if l["condition"] == cond and l["T-ID_moy"] >= 0.95]
        besoin[cond] = min(ok) if ok else "> 256000"

    res = {"final": agrege(finals), "crible": agrege(cribles), "courbe": lignes,
           "exemples_pour_95": besoin,
           "calcul_s": {"entrainement_officiel": round(calcul, 1), "pilote": round(pilote, 1),
                        "eval_final": round(sum(r["duree_eval_s"] for r in finals), 1)}}
    ecrire_json(res, os.path.join(RES, "resultats.json"))

    # summary.md : tous les jeux, valeurs par graine
    L_ = ["# E010 — résumé brut (généré par analyse.py)", "",
          f"Calcul : entraînement officiel {calcul / 60:.1f} min, pilote {pilote / 60:.1f} min, "
          f"test final {res['calcul_s']['eval_final'] / 60:.1f} min.", "",
          "## Test final (T-ID 500/L, V-OOD 500/L, T-FIN 200/L, T-ADV 20/L)", ""]
    for cond, d in res["final"].items():
        L_ += [f"### {cond} — graines {d['graines']} — graines réussies à 16 chiffres : "
               f"{d['graines_reussies_16']}/{len(d['graines'])}", "",
               "| jeu | moy ± écart | par graine | faux sûrs / faux | abstentions | traces justes | cohérents |",
               "|---|---|---|---|---|---|---|"]
        for k, c in d["par_jeu"].items():
            L_.append(f"| {k} | {100 * c['moy']:.1f} ± {100 * c['ecart']:.1f} | "
                      f"{' / '.join(f'{100 * v:.1f}' for v in c['par_graine'])} | "
                      f"{c['faux_surs']} / {c['faux']} | {c['abstentions']} | "
                      f"{c['traces_justes']}/{c['n']} | {c['coherents']}/{c['n']} |")
        L_.append("")
    L_ += ["## Courbe d'efficacité (graine 1, criblage 200/L)", "",
           "| condition | N uniques | T-ID moy | V-OOD 6 | 7 | 8 |", "|---|---|---|---|---|---|"]
    for l in lignes:
        L_.append(f"| {l['condition']} | {l['N']} | {100 * l['T-ID_moy']:.1f} | "
                  f"{100 * l['V-OOD6']:.1f} | {100 * l['V-OOD7']:.1f} | {100 * l['V-OOD8']:.1f} |")
    L_ += ["", "Exemples uniques nécessaires pour T-ID moyen ≥ 95 % : " +
           ", ".join(f"{k} : {v}" for k, v in besoin.items()), ""]
    with open(os.path.join(RES, "summary.md"), "w") as f:
        f.write("\n".join(L_))
    print("\n".join(L_[:4]))
    print(json.dumps(besoin))


if __name__ == "__main__":
    main()
