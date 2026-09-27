"""E009-bis -- agregation : resultats/resultats.json + resultats/summary.md.

Lit runs/<systeme>-s<g>/ (graines officielles >= 1) : etat.json, resume_tid.json, resume_val.json,
resume_final.json ; recompte les exemples uniques du flux reconstruit (curriculum compris).
"""
import glob
import json
import os
import statistics as st

import curric as C
from bande import ecrire_json, lire_json  # E009

ICI = os.path.dirname(os.path.abspath(__file__))
B_REF = {"VAL|6": 0.912, "VAL|7": 0.079, "VAL|8": 0.001}  # E008, chiffres existants


def charge(d, phase):
    f = os.path.join(d, f"resume_{phase}.json")
    return lire_json(f) if os.path.exists(f) else None


def main():
    runs = {}
    for d in sorted(glob.glob(os.path.join(ICI, "runs", "A*-s*"))):
        e = lire_json(os.path.join(d, "etat.json"))
        if e["graine"] < 1:
            continue
        _, uniq = C.uniques(e["graine"], e["pas"], e["transitions"], points=(e["pas"],))
        perte = open(os.path.join(d, "journal.csv")).read().split()[-1].split(",")[-1]
        r = {"systeme": e["systeme"], "graine": e["graine"], "w": e["w"], "lr": e["lr"],
             "params": e["params"], "pas": e["pas"], "appris": e["appris"],
             "pas_appris": e.get("pas_appris"), "niveau_final": e["niveau"],
             "transitions": e["transitions"], "exemples_vus": e["pas"] * 256,
             "exemples_uniques": uniq[e["pas"]], "perte_finale": float(perte),
             "calcul_s": round(e["calcul_s"], 1), "controles_curr": e.get("controles_curr"),
             "controles_arret": e.get("controles_arret")}
        for ph in ("tid", "val", "final"):
            res = charge(d, ph)
            if res:
                r[ph] = {k: {"exact": c["exact"], "faux": c["faux"], "faux_surs": c["faux_surs"],
                             "n": c["n"],
                             "abstentions_parmi_faux": res["non_reponses_parmi_faux"].get(k, [0, 0])[0]}
                         for k, c in res["par_jeu"].items()}
                r[ph + "_iterations"] = res.get("iterations_retenues")
                r[ph + "_duree_s"] = res.get("duree_eval_s")
        runs[os.path.basename(d)] = r
    par_sys = {}
    for s in ("A1", "A2-L", "A3", "A3-T"):
        rs = [r for r in runs.values() if r["systeme"] == s]
        if not rs:
            continue
        v8 = [r["val"]["VAL|8"]["exact"] for r in rs if "val" in r]
        t16 = [r["final"]["TEST|16"]["exact"] for r in rs if "final" in r]
        par_sys[s] = {"graines": sorted(r["graine"] for r in rs),
                      "graines_apprises": sorted(r["graine"] for r in rs if r["appris"]),
                      "val8_moy_apprises": st.mean(v8) if v8 else None,
                      "confirmation_5_graines": bool(v8) and st.mean(v8) >= 0.5,
                      "graines_reussies_test16": sum(x >= 0.9 for x in t16)}
    out = {"runs": runs, "systemes": par_sys, "B-REF_E008": B_REF,
           "calcul_runs_officiels_s": round(sum(r["calcul_s"] for r in runs.values()), 1)}
    ecrire_json(out, os.path.join(ICI, "resultats", "resultats.json"))
    lignes = ["# E009-bis -- resume (genere par synthese_bis.py)", "",
              "| run | appris | pas (arret ou plafond) | niveau | T-ID 2/3/4/5 % | ex. uniques | perte |",
              "|---|---|---|---|---|---|---|"]
    for k, r in runs.items():
        t = r.get("tid") or {}
        tid = "/".join(f"{100 * t[f'T-ID|{L}']['exact']:.1f}" for L in (2, 3, 4, 5)) if t else "-"
        lignes.append(f"| {k} | {'oui' if r['appris'] else 'non'} | "
                      f"{r['pas_appris'] or r['pas']} | {r['niveau_final']} | {tid} | "
                      f"{r['exemples_uniques']} | {r['perte_finale']:.3f} |")
    for k, r in runs.items():
        for ph in ("val", "final"):
            if ph in r:
                lignes += ["", f"## {k} -- {ph}", "",
                           "| jeu | exact % | faux surs / faux | abstentions parmi faux |",
                           "|---|---|---|---|"]
                for j, c in sorted(r[ph].items()):
                    lignes.append(f"| {j} | {100 * c['exact']:.1f} | {c['faux_surs']} / "
                                  f"{c['faux']} | {c['abstentions_parmi_faux']} |")
    lignes += ["", f"Systemes : `{json.dumps(par_sys)}`",
               f"Calcul runs officiels : {out['calcul_runs_officiels_s']} s"]
    with open(os.path.join(ICI, "resultats", "summary.md"), "w") as f:
        f.write("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
