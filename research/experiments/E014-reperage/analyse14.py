"""E014 -- agregats (resultats/resultats.json, summary.md), autodiagnostic, predictions P1-P7.

  python analyse14.py      (lit runs/*/resume.json et eval.jsonl ; aucun modele recharge)
"""
import json
import os
from collections import defaultdict

import numpy as np

import d14 as D

ICI = os.path.dirname(os.path.abspath(__file__))
CONFIGS = ["R0a", "R0b", "R1G", "R1J", "R2"]
GRAINES = [1, 2, 3, 4, 5]
SEUIL = 0.9
LONGS = D.LONG_LENS + [1000]


def lire(nom, f):
    return json.load(open(os.path.join(ICI, "runs", nom, f)))


def items(nom):
    with open(os.path.join(ICI, "runs", nom, "eval.jsonl")) as f:
        return [json.loads(l) for l in f]


def med(xs):
    return float(np.median(xs)) if len(xs) else None


def main():
    res = {"par_config": {}, "par_graine": {}, "autodiag": {}, "lecture": {}, "predictions": {}}
    for c in CONFIGS:
        par_cle, meta = defaultdict(list), defaultdict(list)
        fs = defaultdict(lambda: [0, 0, 0])
        for g in GRAINES:
            nom = f"{c}-s{g}"
            r = lire(nom, "resume.json")
            res["par_graine"][nom] = {k: v["exact"] for k, v in r["par_jeu"].items()}
            for k, v in r["par_jeu"].items():
                par_cle[k].append(v["exact"])
                fs[k][0] += v["faux"]
                fs[k][1] += v["faux_surs"]
                fs[k][2] += v["n"]
            for k in ("params", "exemples_vus", "exemples_uniques_vus", "meilleur_pas",
                      "meilleur_val", "duree_s", "duree_eval_s"):
                meta[k].append(r.get(k))
            meta["tau"].append(r["abstention"]["tau"])
            if r.get("lecture_exacte"):
                res["lecture"][nom] = r["lecture_exacte"]
        res["par_config"][c] = {
            **{f"reussies_{L}": sum(x >= SEUIL for x in par_cle[f"T-LONG|{L}"]) for L in LONGS},
            "exact": {k: {"moy": float(np.mean(v)), "ecart": float(np.std(v)), "graines": v}
                      for k, v in sorted(par_cle.items())},
            "faux_et_surs": {k: {"faux": v[0], "faux_surs": v[1], "n": v[2]} for k, v in fs.items()},
            "meta": dict(meta),
        }
        # autodiagnostic : p_min (confiance preenregistree) et produit, justes vs faux ; abstention
        tout = [x for g in GRAINES for x in items(f"{c}-s{g}") if x["jeu"] != "T-ID"]
        ok = [x for x in tout if x["juste"]]
        ko = [x for x in tout if not x["juste"]]
        taus = {g: lire(f"{c}-s{g}", "resume.json")["abstention"]["tau"] for g in GRAINES}
        ab = {"abst_faux": 0, "faux": 0, "abst_justes": 0, "justes": 0}
        for g in GRAINES:
            for k, v in lire(f"{c}-s{g}", "resume.json")["abstention"]["par_jeu"].items():
                if not k.startswith("T-ID"):
                    for f in ab:
                        ab[f] += v[f]
        res["autodiag"][c] = {
            "n": len(tout), "faux": len(ko),
            "faux_surs_pmin": sum(x["pmin"] >= 0.8 for x in ko),
            "faux_surs_prod": sum(x["prod"] >= 0.8 for x in ko),
            "pmin_med_justes": med([x["pmin"] for x in ok]),
            "pmin_med_faux": med([x["pmin"] for x in ko]),
            "taus": taus, "abstention": ab,
            "abst_quand_faux": ab["abst_faux"] / ab["faux"] if ab["faux"] else None,
            "abst_quand_juste": ab["abst_justes"] / ab["justes"] if ab["justes"] else None,
        }
        if c in ("R1G", "R1J"):
            lu_ko = [x for x in tout if x["lu_ok"] is False]
            add_ko_lu_ok = [x for x in ko if x["lu_ok"]]
            res["autodiag"][c].update({
                "faux_avec_lecture_juste": len(add_ko_lu_ok),
                "lectures_fausses": len(lu_ko),
                "pmin_lu_med_lecture_juste": med([x["pmin_lu"] for x in tout if x["lu_ok"]]),
                "pmin_lu_med_lecture_fausse": med([x["pmin_lu"] for x in lu_ko]),
            })
    # predictions
    pc = res["par_config"]
    res["predictions"]["P1"] = pc["R0a"]["reussies_16"] <= 1
    res["predictions"]["P2"] = pc["R0b"]["reussies_16"] <= 1
    lu16 = [res["lecture"][f"R1G-s{g}"]["T-LONG|16"] for g in GRAINES]
    res["predictions"]["P3"] = {"lecture_16": lu16, "ok": sum(x >= SEUIL for x in lu16) >= 3}
    p4 = {}
    for g in GRAINES:
        nom = f"R1G-s{g}"
        p4[nom] = {L: [res["par_graine"][nom][f"T-LONG|{L}"], res["lecture"][nom][f"T-LONG|{L}"]]
                   for L in LONGS}
    res["predictions"]["P4"] = {"addition_vs_lecture": p4,
                                "ok": all(a >= l - 0.02 for d in p4.values() for a, l in d.values())}
    m100 = lambda c: pc[c]["exact"]["T-LONG|100"]["moy"]
    res["predictions"]["P5"] = {"R1G_100": m100("R1G"), "R1J_100": m100("R1J"),
                                "ok": m100("R1J") >= m100("R1G") - 0.05}
    res["predictions"]["P6"] = pc["R2"]["reussies_16"] > pc["R0a"]["reussies_16"]
    p7 = {}
    for c in CONFIGS:
        a = res["autodiag"][c]
        if a["faux"] >= 20 and a["n"] - a["faux"] > 0:
            p7[c] = a["pmin_med_faux"] < a["pmin_med_justes"]
    res["predictions"]["P7"] = {"par_config": p7, "ok": all(p7.values())}
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    json.dump(res, open(os.path.join(ICI, "resultats", "resultats.json"), "w"), indent=1)

    # summary.md
    L_ = []
    L_.append("| système | graines ≥ 90 % à 16 / 100 / 1 000 | T-ID 5 | T-LONG 10 | 16 | 32 | 64 | "
              "100 | 1 000 |")
    L_.append("|---|---|---|---|---|---|---|---|---|")
    for c in CONFIGS:
        p, e = pc[c], pc[c]["exact"]
        cel = [f"{100 * e[f'T-LONG|{L}']['moy']:.1f} ± {100 * e[f'T-LONG|{L}']['ecart']:.1f}"
               for L in LONGS]
        L_.append(f"| {c} | {p['reussies_16']}/5 / {p['reussies_100']}/5 / {p['reussies_1000']}/5 | "
                  f"{100 * e['T-ID|5']['moy']:.1f} | " + " | ".join(cel) + " |")
    L_.append("")
    L_.append("Adverses (exact-match moyen %, L = 10 / 16 / 32 / 64 / 100 / 1 000) :")
    L_.append("")
    L_.append("| système | ADV-CASCADE | ADV-ZEROS | ADV-ASYM |")
    L_.append("|---|---|---|---|")
    for c in CONFIGS:
        e = pc[c]["exact"]
        L_.append(f"| {c} | " + " | ".join(" / ".join(f"{100 * e[f'{j}|{L}']['moy']:.1f}"
                                                   for L in D.ADV_LENS)
                                         for j in ("ADV-CASCADE", "ADV-ZEROS", "ADV-ASYM")) + " |")
    L_.append("")
    L_.append("Par graine (exact-match %, T-LONG 16 / 100 / 1 000) :")
    L_.append("")
    for c in CONFIGS:
        L_.append(f"- {c} : " + "; ".join(
            f"s{g} " + "/".join(f"{100 * res['par_graine'][f'{c}-s{g}'][f'T-LONG|{L}']:.1f}"
                                for L in (16, 100, 1000)) for g in GRAINES))
    L_.append("")
    L_.append("R1 : addition composée gelée (R1G) vs lecture exacte du lecteur, T-LONG "
              "10 / 16 / 32 / 64 / 100 / 1 000 (%) :")
    L_.append("")
    for nom, d in p4.items():
        L_.append(f"- {nom} : addition " + "/".join(f"{100 * d[L][0]:.1f}" for L in LONGS)
                  + " ; lecture " + "/".join(f"{100 * d[L][1]:.1f}" for L in LONGS))
    L_.append("")
    L_.append("Autodiagnostic (TEST hors T-ID, 5 graines ; confiance = p_min) :")
    L_.append("")
    L_.append("| système | faux / n | faux et sûrs (p_min ≥ 0,8) | faux et sûrs (produit) | "
              "p_min méd. justes / faux | τ par graine | abstention quand faux / quand juste |")
    L_.append("|---|---|---|---|---|---|---|")
    for c in CONFIGS:
        a = res["autodiag"][c]
        f2 = lambda x: "—" if x is None else f"{x:.3f}"
        pct = lambda x: "—" if x is None else f"{100 * x:.1f} %"
        L_.append(f"| {c} | {a['faux']} / {a['n']} | {a['faux_surs_pmin']} | {a['faux_surs_prod']} | "
                  f"{f2(a['pmin_med_justes'])} / {f2(a['pmin_med_faux'])} | "
                  f"{', '.join(str(t) for t in a['taus'].values())} | "
                  f"{pct(a['abst_quand_faux'])} / {pct(a['abst_quand_juste'])} |")
    L_.append("")
    L_.append("Prédictions : " + ", ".join(
        f"{k} {'✅' if (v if isinstance(v, bool) else v['ok']) else '❌'}"
        for k, v in res["predictions"].items()))
    open(os.path.join(ICI, "resultats", "summary.md"), "w").write("\n".join(L_) + "\n")
    print("\n".join(L_))
    for c in ("R1G", "R1J"):
        print(c, {k: v for k, v in res["autodiag"][c].items() if "lu" in k or "lecture" in k})
    print("meta", {c: {k: pc[c]["meta"][k] for k in ("exemples_uniques_vus", "meilleur_pas",
                                                     "duree_s")} for c in CONFIGS})


if __name__ == "__main__":
    main()
