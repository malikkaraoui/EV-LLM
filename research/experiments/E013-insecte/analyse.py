"""E013 -- agregats (resultats/resultats.json, summary.md) + autodiagnostic + inspection du circuit.

  python analyse.py
"""
import json
import os
from collections import defaultdict

import mlx.core as mx
import numpy as np

import donnees as D
from systemes import charge

ICI = os.path.dirname(os.path.abspath(__file__))
CONFIGS = ["I1-H1", "I1-H2", "I1-H4", "I1-H8", "I2", "I3-N10", "I3-N100", "I3-N1000", "I3-N10000"]
GRAINES = [1, 2, 3, 4, 5]
SEUIL = 0.9


def lire(nom, f):
    return json.load(open(os.path.join(ICI, "runs", nom, f)))


def items(nom):
    with open(os.path.join(ICI, "runs", nom, "eval.jsonl")) as f:
        return [json.loads(l) for l in f]


def circuit(nom, H, paires):
    """Correlation de chaque unite avec la vraie retenue sortante ; marge de separation."""
    m = charge(lire(nom, "etat.json")["config"], os.path.join(ICI, "runs", nom, "meilleur.safetensors"))
    A, B, _, M = D.encode_aligne(paires)
    _, h = m(mx.array(A), mx.array(B), garder_etats=True, eval_tous=64)
    h = np.array(h)
    ret = np.zeros(A.shape, dtype=np.int8)
    for i, (a, b) in enumerate(paires):
        da, db, r = D.chiffres_lsb(a), D.chiffres_lsb(b), 0
        for t in range(D.n_pas(a, b)):
            s = (da[t] if t < len(da) else 0) + (db[t] if t < len(db) else 0) + r
            r = int(s >= 10)
            ret[i, t] = r
    v = M.astype(bool)
    y = ret[v].astype(float)
    out = []
    for u in range(H):
        x = h[..., u][v]
        c = float(np.corrcoef(x, y)[0, 1]) if x.std() > 0 else 0.0
        x0, x1 = x[y == 0], x[y == 1]
        marge = float(x1.min() - x0.max()) if c > 0 else float(x0.min() - x1.max())
        out.append({"unite": u, "corr": round(c, 4), "moy_r0": round(float(x0.mean()), 4),
                    "moy_r1": round(float(x1.mean()), 4), "marge": round(marge, 4)})
    port = max(out, key=lambda o: abs(o["corr"]))
    return {"unites": out, "porteuse": port["unite"], "corr_porteuse": port["corr"],
            "marge_porteuse": port["marge"]}


def derive_h1():
    """I1 H = 1 : etat apres (1,1) puis k paires (0,0) sans retenue (k = 0..40), et apres (9,1)."""
    out = {}
    for g in GRAINES:
        m = charge("I1-H1", os.path.join(ICI, "runs", f"I1-H1-s{g}", "meilleur.safetensors"))
        A = np.array([[1] + [0] * 40])
        _, h = m(mx.array(A), mx.array(A), garder_etats=True)
        h = np.array(h)[0, :, 0]
        _, h2 = m(mx.array(np.array([[9, 0]])), mx.array(np.array([[1, 0]])), garder_etats=True)
        out[f"s{g}"] = {"h_sans_retenue_k0_1_5_10_20_40": [round(float(h[k]), 3)
                                                            for k in (0, 1, 5, 10, 20, 40)],
                        "h_apres_retenue": round(float(np.array(h2)[0, 0, 0]), 3)}
    return out


def main():
    res = {"par_config": {}, "circuit": {}, "autodiag": {}, "par_graine": {}}
    jeux = D.jeux_test()
    lignes = []
    for c in CONFIGS:
        par_cle = defaultdict(list)
        fs = defaultdict(lambda: [0, 0])
        meta = defaultdict(list)
        for g in GRAINES:
            nom = f"{c}-s{g}"
            r = lire(nom, "resume.json")
            res["par_graine"][nom] = {k: v["exact"] for k, v in r["par_jeu"].items()}
            for k, v in r["par_jeu"].items():
                par_cle[k].append(v["exact"])
                fs[k][0] += v["faux"]
                fs[k][1] += v["faux_surs"]
            for k in ("params", "exemples_vus", "exemples_uniques_vus", "meilleur_pas",
                      "duree_s"):
                meta[k].append(r[k])
        l16 = par_cle["T-LONG|16"]
        res["par_config"][c] = {
            "reussies_16": sum(x >= SEUIL for x in l16),
            "reussies_1000": sum(x >= SEUIL for x in par_cle["T-LONG|1000"]),
            "exact": {k: {"moy": float(np.mean(v)), "ecart": float(np.std(v)), "graines": v}
                      for k, v in sorted(par_cle.items())},
            "faux_et_surs": {k: {"faux": v[0], "faux_surs": v[1]} for k, v in fs.items()},
            "meta": dict(meta),
        }
        # autodiagnostic : ADV-CASCADE et T-LONG, confiance des justes vs des faux
        ad = {}
        for jeu in ("ADV-CASCADE", "T-LONG", "ADV-ZEROS", "ADV-ASYM"):
            j = [x for g in GRAINES for x in items(f"{c}-s{g}") if x["jeu"] == jeu]
            ok = [x for x in j if x["juste"]]
            ko = [x for x in j if not x["juste"]]
            med = lambda xs, f: float(np.median([x[f] for x in xs])) if xs else None
            ad[jeu] = {"n": len(j), "faux": len(ko),
                       "faux_surs": sum(x["conf"] >= 0.8 for x in ko),
                       "conf_med_justes": med(ok, "conf"), "conf_med_faux": med(ko, "conf"),
                       "pmin_med_justes": med(ok, "pmin"), "pmin_med_faux": med(ko, "pmin"),
                       "abstention": 0.0}
        res["autodiag"][c] = ad
    # circuit : I1 (toutes graines reussies) sur T-LONG L = 100
    p100 = jeux["T-LONG"][100]
    for c in ["I1-H1", "I1-H2", "I1-H4", "I1-H8", "I3-N1000", "I3-N10000"]:
        H = 4 if c.startswith("I3") else int(c[4:])
        for g in GRAINES:
            nom = f"{c}-s{g}"
            if res["par_graine"][nom]["T-LONG|16"] >= SEUIL:
                res["circuit"][nom] = circuit(nom, H, p100)
    res["derive_h1"] = derive_h1()
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    json.dump(res, open(os.path.join(ICI, "resultats", "resultats.json"), "w"), indent=1)

    # summary.md
    cles = ["T-ID|2", "T-ID|5", "VAL"] + [f"T-LONG|{L}" for L in D.LONG_LENS + [1000]]
    lignes.append("| config | params | uniques vus | graines ≥ 90 % à 16 | "
                  + " | ".join(k.replace("|", " ") for k in cles if k != "VAL") + " |")
    lignes.append("|" + "---|" * (4 + len(cles) - 1))
    for c in CONFIGS:
        pc = res["par_config"][c]
        cel = []
        for k in cles:
            if k == "VAL":
                continue
            e = pc["exact"][k]
            cel.append(f"{100 * e['moy']:.1f} ± {100 * e['ecart']:.1f}")
        u = pc["meta"]["exemples_uniques_vus"]
        lignes.append(f"| {c} | {pc['meta']['params'][0]} | {min(u)}–{max(u)} | "
                      f"{pc['reussies_16']}/5 | " + " | ".join(cel) + " |")
    lignes.append("")
    lignes.append("Adverses (exact-match moyen %, par L = 10 / 16 / 32 / 64 / 100 / 1000) :")
    lignes.append("")
    for jeu in ("ADV-CASCADE", "ADV-ZEROS", "ADV-ASYM"):
        lignes.append(f"| config | {jeu} |")
        lignes.append("|---|---|")
        for c in CONFIGS:
            e = res["par_config"][c]["exact"]
            lignes.append(f"| {c} | " + " / ".join(
                f"{100 * e[f'{jeu}|{L}']['moy']:.1f}" for L in D.ADV_LENS) + " |")
        lignes.append("")
    lignes.append("Par graine (exact-match %, T-LONG 16 / 100 / 1000) :")
    lignes.append("")
    for c in CONFIGS:
        s = "; ".join(
            f"s{g} {100 * res['par_graine'][f'{c}-s{g}']['T-LONG|16']:.1f}/"
            f"{100 * res['par_graine'][f'{c}-s{g}']['T-LONG|100']:.1f}/"
            f"{100 * res['par_graine'][f'{c}-s{g}']['T-LONG|1000']:.1f}" for g in GRAINES)
        lignes.append(f"- {c} : {s}")
    open(os.path.join(ICI, "resultats", "summary.md"), "w").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))
    print("\nAUTODIAG", json.dumps(res["autodiag"], indent=0)[:6000])
    print("\nDERIVE H1", json.dumps(res["derive_h1"]))
    print("\nCIRCUIT")
    for nom, ci in res["circuit"].items():
        print(nom, "porteuse", ci["porteuse"], "corr", ci["corr_porteuse"], "marge",
              ci["marge_porteuse"])


if __name__ == "__main__":
    main()
