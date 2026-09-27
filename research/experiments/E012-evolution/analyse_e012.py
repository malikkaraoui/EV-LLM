"""E012 -- agregation : resultats/resultats.json, summary.md, circuits.md.

Usage : python analyse_e012.py
"""
import glob
import os

import numpy as np

from jeux import EXPERIENCES, ICI, ecrire_json, lire_json


def exacte(res):
    """Graine 'a trouve la regle exacte' : 100 % sur tout le test et tous les adverses (+ preuve)."""
    ok = all(c["exact"] == 1.0 for k, c in res["par_jeu"].items() if not k.startswith("V-"))
    return ok and res["preuve"][0] in ("PROUVE", "SANS_OBJET", "NON_PROUVABLE", "NON_BORNE")


def main():
    out, lignes, circuits = {}, [], ["# E012 -- circuits rendus (MDL-minimaux)\n"]
    for exp in EXPERIENCES:
        runs = []
        for d in sorted(glob.glob(os.path.join(ICI, "runs", f"{exp}-s[1-5]"))):
            if os.path.exists(os.path.join(d, "resume.json")):
                runs.append((lire_json(os.path.join(d, "run.json")),
                             lire_json(os.path.join(d, "resume.json"))))
        if not runs:
            continue
        cles = sorted(runs[0][1]["par_jeu"], key=lambda k: (k.split("|")[0], int(k.split("|")[1])))
        par_jeu = {}
        for k in cles:
            v = np.array([res["par_jeu"][k]["exact"] for _, res in runs])
            fs = int(sum(res["par_jeu"][k]["faux_surs"] for _, res in runs))
            par_jeu[k] = {"moy": float(v.mean()), "ecart": float(v.std()), "min": float(v.min()),
                          "faux_surs_total": fs}
        graines = []
        for run, res in runs:
            h = run["histo"][-1] if run["histo"] else {}
            graines.append({
                "graine": run["graine"], "exacte": exacte(res), "preuve": res["preuve"],
                "cachees": res["cachees"], "connexions": res["connexions"], "biais": res["biais"],
                "G_bits": res["G_bits"], "DG_bits": h.get("DG"), "gen": run["gen"],
                "enfants": run["enfants"], "evaluations": run["evaluations"],
                "secondes": run["secondes"], "raison": run["raison"],
                "decouverte": run["decouverte"], "circuit": res["circuit"],
                "t16": res["par_jeu"].get("T-OOD|16", {}).get("exact")})
            circuits.append(f"## {exp} graine {run['graine']} -- preuve {res['preuve'][0]}\n")
            circuits.append("```\n" + "\n".join(res["circuit"]) + "\n```\n")
        n_ex = sum(g["exacte"] for g in graines)
        n16 = sum((g["t16"] or 0) >= 0.9 for g in graines)
        verdict = "decouvre" if n_ex >= 3 else ("parfois" if n_ex >= 1 else "non")
        out[exp] = {"graines": graines, "par_jeu": par_jeu, "n_exactes": n_ex, "n_ge90_16": n16,
                    "verdict": verdict, "exemples_uniques": EXPERIENCES[exp]["n_train"]}
        dec = [g["decouverte"]["evaluations"] for g in graines if g["decouverte"]]
        lignes.append(f"## {exp} ({EXPERIENCES[exp]}) -- {n_ex}/{len(graines)} graines exactes, "
                      f"{n16} >= 90 % a 16, verdict : {verdict}\n")
        lignes.append("| graine | exacte | preuve | cachees | connexions | biais | \\|G\\| | \\|D:G\\| "
                      "| generations | enfants | evaluations | 1re decouverte (evaluations) | s | arret |")
        lignes.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
        for g in graines:
            d = g["decouverte"]["evaluations"] if g["decouverte"] else "-"
            lignes.append(f"| {g['graine']} | {'oui' if g['exacte'] else 'non'} | {g['preuve'][0]} | "
                          f"{g['cachees']} | {g['connexions']} | {g['biais']} | {g['G_bits']} | "
                          f"{(g['DG_bits'] or 0):.1f} | {g['gen']} | {g['enfants']} | "
                          f"{g['evaluations']} | {d} | {g['secondes']:.0f} | {g['raison']} |")
        lignes.append(f"\nEvaluations jusqu'a la decouverte : {dec}\n")
        lignes.append("| jeu | moyenne | ecart | min | faux surs (total) |\n|---|---|---|---|---|")
        for k, c in par_jeu.items():
            lignes.append(f"| {k} | {100 * c['moy']:.1f} % | {100 * c['ecart']:.1f} | "
                          f"{100 * c['min']:.1f} % | {c['faux_surs_total']} |")
        lignes.append("")
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    ecrire_json(out, os.path.join(ICI, "resultats", "resultats.json"))
    with open(os.path.join(ICI, "resultats", "summary.md"), "w") as f:
        f.write("# E012 -- resume des resultats (test final, graines 1-5)\n\n" + "\n".join(lignes))
    with open(os.path.join(ICI, "resultats", "circuits.md"), "w") as f:
        f.write("\n".join(circuits))
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
