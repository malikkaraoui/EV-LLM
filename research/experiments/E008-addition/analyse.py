"""E008 -- agregation : resultats/resultats.json, resultats/summary.md, resultats/courbe.csv.

Refuse de lire les modeles si resultats/controles.json n'est pas VALIDE (PREREGISTREMENT 6).
  python analyse.py
"""
import csv
import os
from collections import defaultdict

import numpy as np

from data import lire_json, ecrire_json

ICI = os.path.dirname(os.path.abspath(__file__))
SYSTEMES = ["B-STD", "B-REF"]
GRAINES = [1, 2, 3]
ORDRE_JEUX = ["T-ID1", "T-ID", "T-OOD", "T-CARRY"]


def cle_tri(k):
    jeu, L = k.split("|")
    return ORDRE_JEUX.index(jeu), int(L)


def lire_csv(chemin):
    with open(chemin, newline="") as f:
        return list(csv.DictReader(f))


def moy_ec(v):
    v = np.asarray(v, dtype=float)
    return float(v.mean()), float(v.std(ddof=1)) if len(v) > 1 else 0.0


def pct(x):
    return f"{100 * x:.1f}"


def main():
    ctl = lire_json(os.path.join(ICI, "resultats", "controles.json"))
    if ctl["verdict"] != "VALIDE":
        raise SystemExit("test NON VALIDE : aucune lecture des modeles appris")
    runs = {}
    for s in SYSTEMES:
        for g in GRAINES:
            d = os.path.join(ICI, "runs", f"{s}-s{g}")
            runs[(s, g)] = {"resume": lire_json(os.path.join(d, "resume.json")),
                            "etat": lire_json(os.path.join(d, "etat.json")),
                            "courbe": lire_csv(os.path.join(d, "courbe.csv"))}

    cles = sorted(runs[("B-STD", 1)]["resume"]["par_jeu"], key=cle_tri)
    exact, surs = {}, {}
    for s in SYSTEMES:
        exact[s], surs[s] = {}, {}
        for k in cles:
            cs = [runs[(s, g)]["resume"]["par_jeu"][k] for g in GRAINES]
            m, e = moy_ec([c["exact"] for c in cs])
            faux = sum(c["faux"] for c in cs)
            fs = sum(c["faux_surs"] for c in cs)
            n = sum(c["n"] for c in cs)
            exact[s][k] = {"moy": m, "ec": e, "par_graine": [c["exact"] for c in cs]}
            surs[s][k] = {"faux": faux, "faux_surs": fs, "n": n,
                          "parmi_faux": fs / faux if faux else None, "parmi_tous": fs / n}

    chaines = {}
    for s in SYSTEMES:
        acc = defaultdict(list)
        for g in GRAINES:
            for ch, c in runs[(s, g)]["resume"]["par_chaine"].items():
                acc[int(ch)].append((c["justes"], c["n"]))
        chaines[s] = {ch: {"exact_moy": float(np.mean([j / n for j, n in v])),
                           "n_par_graine": v[0][1]} for ch, v in sorted(acc.items())}

    courbe = defaultdict(list)
    for s in SYSTEMES:
        for g in GRAINES:
            for r in runs[(s, g)]["courbe"]:
                courbe[(s, int(r["pas"]), int(r["exemples_vus"]), r["jeu"], int(r["L"]))].append(
                    float(r["exact"]))
    with open(os.path.join(ICI, "resultats", "courbe.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["systeme", "pas", "exemples_vus", "jeu", "L", "exact_moy", "exact_ec",
                    "g1", "g2", "g3"])
        for (s, p, ex, jeu, L), v in sorted(courbe.items()):
            m, e = moy_ec(v)
            w.writerow([s, p, ex, jeu, L, f"{m:.4f}", f"{e:.4f}"] + [f"{x:.4f}" for x in v])

    def ex(s, k):
        return exact[s][k]["moy"]

    preds = {
        "P1 B-STD T-ID >= 95 % a chaque L": all(ex("B-STD", f"T-ID|{L}") >= 0.95 for L in (2, 3, 4, 5)),
        "P2 B-STD T-OOD L=8 <= 10 %": ex("B-STD", "T-OOD|8") <= 0.10,
        "P3 B-REF T-ID >= 95 % a chaque L": all(ex("B-REF", f"T-ID|{L}") >= 0.95 for L in (2, 3, 4, 5)),
        "P4 B-REF T-OOD L=6 >= B-STD + 10 pts": ex("B-REF", "T-OOD|6") >= ex("B-STD", "T-OOD|6") + 0.10,
        "P5 T-CARRY < T-ID a chaque L=2..5 (les deux modeles)": all(
            ex(s, f"T-CARRY|{L}") < ex(s, f"T-ID|{L}") for s in SYSTEMES for L in (2, 3, 4, 5)),
    }
    durees = {f"{s}-s{g}": {"calcul_s": round(runs[(s, g)]["etat"]["calcul_s"], 1),
                            "invocations": runs[(s, g)]["etat"]["invocations"],
                            "params": runs[(s, g)]["etat"]["params"],
                            "eval_s": runs[(s, g)]["resume"]["duree_eval_s"]}
              for s in SYSTEMES for g in GRAINES}
    out = {"controles": {k: ctl[k] for k in ("verdict", "oracle_100_partout",
                                              "parcoeur_max_T-ID_T-OOD", "table_parcoeur")},
           "exact": exact, "faux_et_surs": surs, "par_chaine": chaines,
           "predictions": preds, "durees": durees}
    ecrire_json(out, os.path.join(ICI, "resultats", "resultats.json"))

    L_ = []
    L_.append("# E008 -- resultats (genere par analyse.py)\n")
    L_.append(f"Test : **{ctl['verdict']}** (C-ORACLE 100 % partout : {ctl['oracle_100_partout']} ; "
              f"C-PARCOEUR max T-ID/T-OOD : {pct(ctl['parcoeur_max_T-ID_T-OOD'])} %).\n")
    L_.append("## Exact-match (%) par jeu x longueur -- moyenne +- ecart-type sur graines 1, 2, 3\n")
    L_.append("| jeu | L | n | C-ORACLE | C-PARCOEUR | B-STD | B-REF | B-STD (g1/g2/g3) | B-REF (g1/g2/g3) |")
    L_.append("|---|---|---|---|---|---|---|---|---|")
    for k in cles:
        jeu, Lk = k.split("|")
        fmt = lambda s: f"{pct(exact[s][k]['moy'])} +- {pct(exact[s][k]['ec'])}"
        pg = lambda s: "/".join(pct(x) for x in exact[s][k]["par_graine"])
        L_.append(f"| {jeu} | {Lk} | {ctl['C-ORACLE'][k]['n']} | {pct(ctl['C-ORACLE'][k]['exact'])} | "
                  f"{pct(ctl['C-PARCOEUR'][k]['exact'])} | {fmt('B-STD')} | {fmt('B-REF')} | "
                  f"{pg('B-STD')} | {pg('B-REF')} |")
    L_.append("\n## « Faux et sur » (reponse fausse, confiance >= 0,8), 3 graines cumulees\n")
    L_.append("| jeu | L | B-STD faux | B-STD surs / faux | B-REF faux | B-REF surs / faux |")
    L_.append("|---|---|---|---|---|---|")
    for k in cles:
        jeu, Lk = k.split("|")
        cell = lambda s: (f"{surs[s][k]['faux']}", "-" if surs[s][k]["parmi_faux"] is None
                          else f"{surs[s][k]['faux_surs']} ({pct(surs[s][k]['parmi_faux'])} %)")
        a, b = cell("B-STD"), cell("B-REF")
        L_.append(f"| {jeu} | {Lk} | {a[0]} | {a[1]} | {b[0]} | {b[1]} |")
    L_.append("\n## Exact-match (%) par longueur de chaine de retenue (T-ID, T-OOD, T-CARRY)\n")
    L_.append("| chaine | n / graine | B-STD | B-REF |")
    L_.append("|---|---|---|---|")
    for ch in sorted(set(chaines["B-STD"]) | set(chaines["B-REF"])):
        L_.append(f"| {ch} | {chaines['B-STD'][ch]['n_par_graine']} | "
                  f"{pct(chaines['B-STD'][ch]['exact_moy'])} | {pct(chaines['B-REF'][ch]['exact_moy'])} |")
    L_.append("\n## Predictions preenregistrees\n")
    for p, v in preds.items():
        L_.append(f"- {p} : **{'CONFIRMEE' if v else 'INFIRMEE'}**")
    L_.append("\n## Durees\n")
    L_.append("| run | params | calcul (s) | invocations | evaluation (s) |")
    L_.append("|---|---|---|---|---|")
    for r, d in durees.items():
        L_.append(f"| {r} | {d['params']} | {d['calcul_s']} | {d['invocations']} | {d['eval_s']} |")
    L_.append("\nCourbe d'efficacite : `courbe.csv`.")
    with open(os.path.join(ICI, "resultats", "summary.md"), "w") as f:
        f.write("\n".join(L_) + "\n")
    print("\n".join(L_))


if __name__ == "__main__":
    main()
