"""E015 -- agregats (resultats/resultats.json + resultats.md). Lit runs/*/resultat.json et test.json.

Ecart-type : ddof = 0 (numpy par defaut), declare.
"""
import json
import os

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
GRAINES = [1, 2, 3, 4, 5]
CONDS = [("EVO", "N1"), ("ALEA", "N1"), ("SANSVIE", "N1"), ("ECH0", "N1"), ("ECH1", "N1"),
         ("ECH2", "N1"), ("FROID", "N2"), ("CHAUD", "N2"),
         ("FROID", "N3"), ("CHAUD", "N3")]
LONGS = [10, 16, 32, 64, 100, 1000]
ADV = {"N1": ["ADV-CASCADE", "ADV-ZEROS", "ADV-ASYM", "ADV-PROPAG"],
       "N2": ["ADV-CASCADE3", "ADV-PROPAG3", "ADV-ASYM3"],
       "N3": ["ADV-EMPRUNT", "ADV-EGAUX", "ADV-ASYM"]}


def lire(run, f):
    p = os.path.join(ICI, "runs", run, f)
    return json.load(open(p)) if os.path.exists(p) else None


def ms(v):
    v = [x for x in v if x is not None]
    return f"{100 * np.mean(v):.1f} ± {100 * np.std(v):.1f}" if v else "—"


def med(v):
    v = [x for x in v if x is not None]
    return (f"{int(np.median(v))} ({len(v)}/5)" if v else "— (0/5)")


def reutilisation(n1, n):
    """Part des lignes du programme net EVO-N1 retrouvees telles quelles dans le programme net."""
    if not n1 or not n:
        return None
    a = set(n1["lisible"][:-1])
    return len(a & set(n["lisible"][:-1])) / max(1, len(a))


def main():
    out, md = {}, ["# E015 — résultats agrégés (5 graines, TEST lu une fois)", ""]
    md += ["| condition | graines ≥ 90 % à 16 | T-ID 5 | T-LONG " + " | ".join(map(str, LONGS))
           + " | VAL-OOD retenue | candidats (médiane) | essais → 1er candidat (médiane, n) "
           "| essais → 1er candidat VAL ≥ 0,99 | exemples uniques (moy.) |",
           "|---|---|---|" + "---|" * len(LONGS) + "---|---|---|---|---|"]
    detail = []
    for cond, t in CONDS:
        nom = f"{cond}-{t}"
        R = [lire(f"{nom}-s{g}", "resultat.json") for g in GRAINES]
        T = [lire(f"{nom}-s{g}", "test.json") for g in GRAINES]
        if not all(R) or not all(T):
            md.append(f"| {nom} | incomplet |")
            continue
        ok = [x["exact"]["T-LONG|16"] >= 0.9 for x in T]
        tid5 = [x["exact"].get("T-ID|5") for x in T]
        ligne = [f"| {nom} | **{sum(ok)}/5** | {ms(tid5)} "]
        for L in LONGS:
            ligne.append(ms([x["exact"][f"T-LONG|{L}"] for x in T]))
        ligne += [ms([r["choix"]["val"] for r in R]),
                  f"{int(np.median([r['n_candidats'] for r in R]))}",
                  med([r["essais_premier_candidat"] for r in R]),
                  med([r["essais_premier_candidat_val99"] for r in R]),
                  f"{int(np.mean([r['exemples_uniques'] for r in R]))}"]
        md.append(" | ".join(ligne) + " |")
        n1 = [lire(f"ECH0-N1-s{g}", "resultat.json") for g in GRAINES]
        out[nom] = {
            "graines_reussies": int(sum(ok)),
            "par_graine": {g: {"T-LONG": {L: T[i]["exact"][f"T-LONG|{L}"] for L in LONGS},
                               "adv": {a: {L: T[i]["exact"][f"{a}|{L}"] for L in
                                           [10, 16, 32, 64, 100, 1000]} for a in ADV[t]},
                               "val": R[i]["choix"]["val"], "essais": R[i]["essais"],
                               "n_candidats": R[i]["n_candidats"],
                               "essais_premier_candidat": R[i]["essais_premier_candidat"],
                               "essais_premier_candidat_val99":
                                   R[i]["essais_premier_candidat_val99"],
                               "exemples_uniques": R[i]["exemples_uniques"],
                               "faux_hors_tid": T[i]["faux_hors_tid"],
                               "faux_surs": T[i]["faux_surs"], "tau": T[i]["tau"],
                               "abst_faux": T[i]["abstention_quand_faux"],
                               "abst_juste": T[i]["abstention_quand_juste"],
                               "triche": R[i]["triche"],
                               "reutilisation_N1": (reutilisation(n1[i], R[i])
                                                    if cond == "CHAUD" else None),
                               "lisible": R[i]["lisible"]}
                           for i, g in enumerate(GRAINES)}}
        detail.append((nom, t, out[nom]))
    md += ["", "## Adverses (moyenne 5 graines, %, L = 10 / 16 / 32 / 64 / 100 / 1 000)", "",
           "| condition | jeu | exact |", "|---|---|---|"]
    for nom, t, d in detail:
        for a in ADV[t]:
            v = [" / ".join(f"{100 * np.mean([d['par_graine'][g]['adv'][a][L] for g in GRAINES]):.1f}"
                            for L in [10, 16, 32, 64, 100, 1000])]
            md.append(f"| {nom} | {a} | {v[0]} |")
    md += ["", "## Par graine", ""]
    for nom, t, d in detail:
        md.append(f"### {nom}")
        for g in GRAINES:
            x = d["par_graine"][g]
            md.append(f"- s{g} : T-LONG 16 / 100 / 1 000 = "
                      f"{100 * x['T-LONG'][16]:.1f} / {100 * x['T-LONG'][100]:.1f} / "
                      f"{100 * x['T-LONG'][1000]:.1f} ; VAL {100 * x['val']:.1f} ; "
                      f"candidats {x['n_candidats']} ; 1er candidat {x['essais_premier_candidat']}"
                      f" ; faux {x['faux_hors_tid']}, faux et sûrs {x['faux_surs']} ; "
                      f"τ {x['tau']} ; abst. faux/juste {x['abst_faux']}/{x['abst_juste']}"
                      + (f" ; réutilisation N1 {x['reutilisation_N1']}"
                         if x["reutilisation_N1"] is not None else "")
                      + f" ; raccourcis {x['triche']['raccourcis_val_lt_0.1']}, sans champion "
                        f"score>0 {x['triche']['sans_champion_score_pos']['n']}")
            md.append("  ```")
            md += [f"  {li}" for li in x["lisible"]]
            md.append("  ```")
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    json.dump(out, open(os.path.join(ICI, "resultats", "resultats.json"), "w"), indent=1)
    open(os.path.join(ICI, "resultats", "resultats.md"), "w").write("\n".join(md) + "\n")
    print("\n".join(md[:14]))


if __name__ == "__main__":
    main()
