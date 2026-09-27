"""E011 -- agregation : resultats/resultats.json, resultats/summary.md, resultats/trajectoires.csv."""
import glob
import os
from collections import defaultdict

import numpy as np

from donnees import ICI, TEST_LENS, ecrire_json, lire_json
from objectifs import longueur_H

GRAINES = [1, 2, 3, 4, 5]
JEUX_FINAUX = ["T-OOD", "A-CASCADE", "A-ZEROS", "A-ASYM"]


def verdict(n_exactes):
    return "garde la regle" if n_exactes == 5 else ("s'en eloigne" if n_exactes <= 2 else "instable")


def main():
    par_cfg = defaultdict(dict)
    for d in sorted(glob.glob(os.path.join(ICI, "runs", "*-s[1-5]"))):
        r = lire_json(os.path.join(d, "run.json"))
        s = lire_json(os.path.join(d, "resume.json"))
        par_cfg[r["config"]][r["graine"]] = (r, s)
    out, lignes_csv = {}, ["config,graine,pas,ce_train_bits,objectif,dist_golden,norme,val_exact"]
    for cfg, runs in par_cfg.items():
        assert sorted(runs) == GRAINES, (cfg, sorted(runs))
        cles = sorted(next(iter(runs.values()))[1]["par_jeu"])
        acc = {k: [runs[g][1]["par_jeu"][k]["exact"] for g in GRAINES] for k in cles}
        faux_surs = {k: sum(runs[g][1]["par_jeu"][k]["faux_surs"] for g in GRAINES) for k in cles}
        faux = {k: sum(runs[g][1]["par_jeu"][k]["faux"] for g in GRAINES) for k in cles}
        exactes = [g for g in GRAINES
                   if all(runs[g][1]["par_jeu"][k]["exact"] == 1.0 for k in cles
                          if k.split("|")[0] in JEUX_FINAUX)]
        seize = [g for g in GRAINES if runs[g][1]["par_jeu"]["T-OOD|16"]["exact"] >= 0.9]
        fins = [runs[g][0]["trajectoire"][-1] for g in GRAINES]
        out[cfg] = {
            "graines_exactes": exactes, "n_exactes": len(exactes), "verdict": verdict(len(exactes)),
            "graines_>=90%_a_16": len(seize),
            "exact_moy": {k: float(np.mean(v)) for k, v in acc.items()},
            "exact_ecart": {k: float(np.std(v)) for k, v in acc.items()},
            "exact_par_graine": acc, "faux": faux, "faux_surs": faux_surs,
            "premiere_perte_val": [runs[g][0]["premiere_perte_val"] for g in GRAINES],
            "dist_golden_fin": [f["dist_golden"] for f in fins],
            "norme_fin": [f["norme"] for f in fins],
            "ce_train_fin": [f["ce_train_bits"] for f in fins],
            "H_bits_fin": [longueur_H(np.array(runs[g][0]["theta_final"])) for g in GRAINES],
            "exemples_uniques": [runs[g][0]["exemples_uniques"] for g in GRAINES],
            "acceptees": [runs[g][0].get("propositions_acceptees") for g in GRAINES],
        }
        for g in GRAINES:
            for t in runs[g][0]["trajectoire"]:
                lignes_csv.append(",".join(str(x) for x in [cfg, g, t["pas"], t["ce_train_bits"],
                                  t["objectif"], t["dist_golden"], t["norme"], t["val_exact"]]))
    rd = os.path.join(ICI, "resultats")
    os.makedirs(rd, exist_ok=True)
    ecrire_json(out, os.path.join(rd, "resultats.json"))
    with open(os.path.join(rd, "trajectoires.csv"), "w") as f:
        f.write("\n".join(lignes_csv) + "\n")

    ordre = ["a", "b-lam0.01", "b-lam0.1", "b-lam1", "c-lam0.01", "c-lam0.1", "c-lam1", "e",
             "d", "d-CE", "d-L2"]
    ordre = [c for c in ordre if c in out]
    md = ["# E011 partie 1 -- resume (genere par analyse.py)", "",
          "| config | graines exactes /5 | verdict | 1re perte val (pas) | dist. golden fin | "
          "\\|H\\| fin (bits) | CE train fin (bits) |", "|---|---|---|---|---|---|---|"]
    for c in ordre:
        o = out[c]
        md.append(f"| {c} | {o['n_exactes']} | {o['verdict']} | {o['premiere_perte_val']} | "
                  + " ".join(f"{x:.2f}" for x in o["dist_golden_fin"]) + " | "
                  + " ".join(str(x) for x in o["H_bits_fin"]) + " | "
                  + " ".join(f"{x:.3g}" for x in o["ce_train_fin"]) + " |")
    md += ["", "Exact-match (%) moyenne +- ecart sur 5 graines (faux surs cumules entre crochets)", ""]
    cols = [f"V-OOD|{L}" for L in (6, 7, 8)] + [f"T-OOD|{L}" for L in TEST_LENS] + \
        [f"{j}|{L}" for j in ("A-CASCADE", "A-ZEROS", "A-ASYM") for L in (100, 1000)]
    md.append("| config | " + " | ".join(cols) + " |")
    md.append("|---" * (len(cols) + 1) + "|")
    for c in ordre:
        o = out[c]
        md.append(f"| {c} | " + " | ".join(
            f"{100 * o['exact_moy'][k]:.1f} ± {100 * o['exact_ecart'][k]:.1f} [{o['faux_surs'][k]}]"
            for k in cols) + " |")
    with open(os.path.join(rd, "summary.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
