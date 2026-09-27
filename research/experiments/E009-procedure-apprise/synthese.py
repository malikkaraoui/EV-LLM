"""E009 -- agregation : resultats/resultats.json + resultats/summary.md + resultats/courbe.csv.

Lit runs/*/etat.json, resume_val.json, resume_final.json (graines officielles >= 1 seulement),
les chiffres E008 (B-STD, B-REF) et recompte les exemples uniques du flux aux jalons.
"""
import csv
import glob
import json
import os
import statistics as st
from collections import defaultdict

from bande import ecrire_json, lire_json
from entraine import jalons
from verifie import uniques

ICI = os.path.dirname(os.path.abspath(__file__))
SYSTEMES = ["A1", "A2", "A2-L", "A3", "A3-T"]
SEUIL_GRAINE = 0.9  # graine reussie : >= 90 % a TEST|16


def cle_tri(k):
    jeu, L = k.split("|")
    a = [int(x) for x in L.split("+")]
    return (jeu, max(a), a[0])


def runs():
    out = defaultdict(dict)  # (systeme, fmt) -> {graine: dossier}
    for d in glob.glob(os.path.join(ICI, "runs", "*-s*")):
        e = lire_json(os.path.join(d, "etat.json"))
        if e["graine"] >= 1:
            out[(e["systeme"], e["fmt"])][e["graine"]] = d
    return out


def agrege(dossiers, phase):
    par_k = defaultdict(lambda: {"exact": [], "faux": 0, "faux_surs": 0, "n": 0, "nr": 0})
    iters = {}
    for g, d in sorted(dossiers.items()):
        f = os.path.join(d, f"resume_{phase}.json")
        if not os.path.exists(f):
            continue
        r = lire_json(f)
        for k, c in r["par_jeu"].items():
            a = par_k[k]
            a["exact"].append(c["exact"])
            a["faux"] += c["faux"]
            a["faux_surs"] += c["faux_surs"]
            a["n"] += c["n"]
            a["nr"] += r["non_reponses_parmi_faux"].get(k, [0, 0])[0]
        iters[g] = r.get("iterations_retenues")
    res = {}
    for k in sorted(par_k, key=cle_tri):
        a = par_k[k]
        ex = a["exact"]
        res[k] = {"moy": st.mean(ex), "ec": st.stdev(ex) if len(ex) > 1 else 0.0,
                  "par_graine": ex, "faux": a["faux"], "faux_surs": a["faux_surs"],
                  "non_reponses": a["nr"], "n": a["n"]}
    return res, iters


def main():
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    rs = runs()
    out = {"controles": lire_json(os.path.join(ICI, "resultats", "controles.json"))["verdict"],
           "systemes": {}}
    for (s, fmt), dossiers in sorted(rs.items()):
        etats = {g: lire_json(os.path.join(d, "etat.json")) for g, d in dossiers.items()}
        val, it_val = agrege(dossiers, "val")
        fin, it_fin = agrege(dossiers, "final")
        pertes = {}
        for g, d in dossiers.items():
            with open(os.path.join(d, "journal.csv")) as f:
                pertes[g] = float(list(csv.reader(f))[-1][1])
        reussies = None
        if "TEST|16" in fin:
            reussies = sum(v >= SEUIL_GRAINE for v in fin["TEST|16"]["par_graine"])
        out["systemes"][f"{s}-{fmt}"] = {
            "graines": sorted(dossiers), "params": etats[min(etats)]["params"],
            "pas": {g: e["pas"] for g, e in etats.items()},
            "calcul_s": {g: round(e["calcul_s"], 1) for g, e in etats.items()},
            "checkpoint_retenu": {g: e.get("meilleur") for g, e in etats.items()},
            "perte_finale": pertes, "val": val, "final": fin,
            "iterations_retenues_final": it_fin, "graines_reussies_16": reussies}
    # exemples uniques vus aux jalons (flux deterministe, graines 1 et 2)
    js = jalons(hp["pas"])
    out["exemples_uniques"] = {g: uniques(g, hp["pas"], js)[1] for g in (1, 2)}
    e8 = lire_json(os.path.join(ICI, "..", "E008-addition", "resultats", "resultats.json"))
    out["E008"] = {s: {k: v["moy"] for k, v in e8["exact"][s].items()} for s in ("B-STD", "B-REF")}
    ecrire_json(out, os.path.join(ICI, "resultats", "resultats.json"))

    # courbes VAL (100 / L) aux jalons, tous runs
    with open(os.path.join(ICI, "resultats", "courbe.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["systeme", "fmt", "graine", "pas", "exemples_vus", "exemples_uniques", "L",
                    "exact"])
        for (s, fmt), dossiers in sorted(rs.items()):
            for g, d in sorted(dossiers.items()):
                with open(os.path.join(d, "courbe.csv")) as f:
                    for row in list(csv.DictReader(f)):
                        u = out["exemples_uniques"].get(g, {}).get(int(row["pas"]), "")
                        w.writerow([s, fmt, g, row["pas"], row["exemples_vus"], u, row["L"],
                                    row["exact"]])

    # summary.md
    L = ["# E009 -- resume (genere par synthese.py)", ""]
    for nom, d in out["systemes"].items():
        L.append(f"## {nom} -- graines {d['graines']}, {d['params']} parametres")
        L.append(f"- calcul (s) : {d['calcul_s']} ; perte finale : "
                 f"{ {g: round(v, 3) for g, v in d['perte_finale'].items()} }")
        L.append(f"- checkpoint retenu : {d['checkpoint_retenu']}")
        L.append(f"- graines reussies (TEST|16 >= 90 %) : {d['graines_reussies_16']}")
        L.append("")
        L.append("| jeu | moy % | ec | par graine | faux surs / faux | non-reponses |")
        L.append("|---|---|---|---|---|---|")
        for part in ("val", "final"):
            for k, c in d[part].items():
                L.append(f"| {k} | {100 * c['moy']:.1f} | {100 * c['ec']:.1f} | "
                         f"{[round(100 * v, 1) for v in c['par_graine']]} | "
                         f"{c['faux_surs']} / {c['faux']} | {c['non_reponses']} |")
        L.append("")
    L.append(f"Exemples uniques aux jalons : {out['exemples_uniques']}")
    with open(os.path.join(ICI, "resultats", "summary.md"), "w") as f:
        f.write("\n".join(L) + "\n")
    print("\n".join(L[:60]))


if __name__ == "__main__":
    main()
