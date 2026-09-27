"""E016 -- agregation : resultats/resultats.json + resultats/summary.md (PREREGISTREMENT section 5).

  python analyse16.py
"""
import json
import os

import numpy as np

from evalue16 import SUR, seuil_abstention
from m16 import D, K

ICI = os.path.dirname(os.path.abspath(__file__))
CONDS = ["DONNE", "COLL", "IND", "COUPE"]
GRAINES = [1, 2, 3, 4, 5]
PAIRES = [f"A{i}B{j}" for i in (1, 2, 3) for j in (1, 2, 3)]
LONG = ["T-ID|5", "T-LONG|10", "T-LONG|16", "T-LONG|32", "T-LONG|64", "T-LONG|100", "T-LONG|1000"]
ADV = [f"{j}|{L}" for j in ("ADV-CASCADE", "ADV-ZEROS", "ADV-ASYM") for L in D.ADV_LENS]


def charge(c, g):
    return json.load(open(os.path.join(ICI, "resultats", "eval", f"{c}-s{g}.json")))


def ex(r, p, k):
    return float(np.mean(r["paires"][p][k]["juste"]))


def lexique(r):
    """Symboles partages entre emetteurs, et recepteurs qui comprennent plusieurs A."""
    lex = r["lexique"]
    part = {f"A{a + 1}-A{b + 1}": sum(lex[a][d] == lex[b][d] for d in range(K))
            for a in range(3) for b in range(a + 1, 3)}
    return dict(C=r["C"], partages_par_paire_A=part, lexique=lex)


def unique_vus(c, g):
    """Problemes neufs consommes : les n_neufs premiers du flux concatene de chaque pas."""
    e = json.load(open(os.path.join(ICI, "runs", f"{c}-s{g}", "etat.json")))
    vus, total = set(), 0
    for pas, _, _, _, n in e["journal"]:
        if n:
            neufs = [p for r in range(3) for p in D.paires_flux(g, 3 * pas + r)][:n]
            vus.update(neufs)
            total += n
    return len(vus), total


def dynamique(c, g):
    """VAL par paire aux checkpoints : paires >= 90 % a la fin de la phase 1 (pas 2000) et a 4000 ;
    premier pas (resolution 250) ou chaque paire apprise passe 90 % ; stabilite du lexique."""
    e = json.load(open(os.path.join(ICI, "runs", f"{c}-s{g}", "etat.json")))
    val = {v["pas"]: v for v in e["val"]}
    appr = lambda v: [PAIRES[3 * i + j] for i in range(3) for j in range(3) if v["mat"][i][j] >= 0.9]
    premier = {}
    for p in sorted(val):
        for k in appr(val[p]):
            premier.setdefault(k, p)
    fin = val[max(val)]["lex"]
    change = sum(val[p]["lex"] != fin for p in val if p >= max(val) - 1000)
    j = np.array(e["journal"])
    return dict(paires_fin_phase1=appr(val[2000]), paires_fin=appr(val[max(val)]),
                premier_pas_90=premier, lexique_change_1000_derniers_pas=int(change),
                tours_reussis_phase1_fin=float(j[1750:2000, 2].mean()),
                tours_reussis_phase2=float(j[2000:, 2].mean()),
                items_justes_phase2=float(j[2000:, 3].mean()),
                meilleur=e["meilleur"])


def autodiag(r):
    val_j = [cf for p in PAIRES for L in D.VAL_LENS
             for ok, cf in zip(r["paires"][p][f"VAL-OOD|{L}"]["juste"], r["paires"][p][f"VAL-OOD|{L}"]["conf"]) if ok]
    tau = seuil_abstention(val_j)
    J, F = [], []
    for p in PAIRES:
        for k, v in r["paires"][p].items():
            if k.startswith(("VAL", "T-ID")):
                continue
            for ok, cf in zip(v["juste"], v["conf"]):
                (J if ok else F).append(cf)
    J, F = np.array(J), np.array(F)
    return dict(n=len(J) + len(F), faux=len(F), faux_surs=int((F >= SUR).sum()),
                conf_med_justes=float(np.median(J)) if len(J) else None,
                conf_med_faux=float(np.median(F)) if len(F) else None, tau=tau,
                abst_faux=float((F < tau).mean()) if tau and len(F) else 0.0,
                abst_justes=float((J < tau).mean()) if tau and len(J) else 0.0)


def main():
    out = {}
    for c in CONDS:
        oc = out[c] = {"graines": {}}
        for g in GRAINES:
            r = charge(c, g)
            og = dict(par_paire={p: {k: ex(r, p, k) for k in LONG + ADV} for p in PAIRES},
                      lexique=lexique(r), autodiag=autodiag(r))
            og["paires_90_a_16"] = [p for p in PAIRES if og["par_paire"][p]["T-LONG|16"] >= 0.9]
            og["paires_90_a_100"] = [p for p in PAIRES if og["par_paire"][p]["T-LONG|100"] >= 0.9]
            og["reussie"] = len(og["paires_90_a_16"]) == 9
            if c != "DONNE":
                og["dynamique"] = dynamique(c, g)
                if c in ("COLL", "IND"):
                    og["uniques_vus"], og["problemes_consommes"] = unique_vus(c, g)
            oc["graines"][g] = og
        G = oc["graines"]
        oc["graines_reussies"] = sum(G[g]["reussie"] for g in GRAINES)
        oc["moyenne_9_paires"] = {k: [float(np.mean([np.mean([G[g]["par_paire"][p][k] for p in PAIRES]) for g in GRAINES])),
                                      float(np.std([np.mean([G[g]["par_paire"][p][k] for p in PAIRES]) for g in GRAINES]))]
                                  for k in LONG}
        appr = [(g, p) for g in GRAINES for p in G[g]["paires_90_a_16"]]
        oc["paires_apprises"] = len(appr)
        oc["paires_apprises_moyenne"] = {k: float(np.mean([G[g]["par_paire"][p][k] for g, p in appr])) if appr else None
                                         for k in LONG + ADV}
    json.dump(out, open(os.path.join(ICI, "resultats", "resultats.json"), "w"), indent=1)
    ecrit_summary(out)


def f(x):
    return "—" if x is None else f"{100 * x:.1f}"


def ecrit_summary(out):
    L = ["# E016 — résumé (généré par analyse16.py)", ""]
    L += ["| cond. | graines réussies (9 paires ≥ 90 % à 16) | paires ≥ 90 % à 16 par graine | moyenne 9 paires T-LONG 16 | 100 | 1 000 |",
          "|---|---|---|---|---|---|"]
    for c, oc in out.items():
        G = oc["graines"]
        L.append(f"| {c} | {oc['graines_reussies']}/5 | {' ; '.join(str(len(G[g]['paires_90_a_16'])) for g in GRAINES)} | "
                 f"{f(oc['moyenne_9_paires']['T-LONG|16'][0])} ± {f(oc['moyenne_9_paires']['T-LONG|16'][1])} | "
                 f"{f(oc['moyenne_9_paires']['T-LONG|100'][0])} | {f(oc['moyenne_9_paires']['T-LONG|1000'][0])} |")
    L += ["", "## Paires apprises (≥ 90 % à 16), exact moyen %", "",
          "| cond. | n paires | T-ID 5 | 10 | 16 | 32 | 64 | 100 | 1 000 | CASCADE 100 / 1 000 | ZEROS 100 / 1 000 | ASYM 100 / 1 000 |",
          "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for c, oc in out.items():
        m = oc["paires_apprises_moyenne"]
        if oc["paires_apprises"]:
            L.append(f"| {c} | {oc['paires_apprises']} | " + " | ".join(f(m[k]) for k in LONG) + " | " +
                     " | ".join(f"{f(m[f'{j}|100'])} / {f(m[f'{j}|1000'])}" for j in ("ADV-CASCADE", "ADV-ZEROS", "ADV-ASYM")) + " |")
        else:
            L.append(f"| {c} | 0 | " + " | ".join("—" for _ in range(10)) + " |")
    L += ["", "## Par graine : paires apprises, lexique, dynamique", "",
          "| cond. | g | paires ≥ 90 % à 16 (à 100) | fin phase 1 → fin | C | symboles partagés A1-A2 / A1-A3 / A2-A3 | tours réussis fin ph. 1 / ph. 2 | uniques vus |",
          "|---|---|---|---|---|---|---|---|"]
    for c in ("COLL", "IND", "COUPE"):
        for g in GRAINES:
            o = out[c]["graines"][g]
            d = o["dynamique"]
            part = " / ".join(str(v) for v in o["lexique"]["partages_par_paire_A"].values())
            L.append(f"| {c} | {g} | {', '.join(o['paires_90_a_16']) or '—'} ({len(o['paires_90_a_100'])}) | "
                     f"{len(d['paires_fin_phase1'])} → {len(d['paires_fin'])} | {o['lexique']['C']}/11 | {part} | "
                     f"{f(d['tours_reussis_phase1_fin'])} / {f(d['tours_reussis_phase2'])} | {o.get('uniques_vus', '—')} |")
    L += ["", "## Autodiagnostic (TEST hors T-ID, 9 paires × 5 graines)", "",
          "| cond. | faux | faux et sûrs (≥ 0,8) | conf. médiane justes / faux | τ par graine | abstention quand faux / quand juste |",
          "|---|---|---|---|---|---|"]
    for c, oc in out.items():
        A = [oc["graines"][g]["autodiag"] for g in GRAINES]
        mj = [a["conf_med_justes"] for a in A if a["conf_med_justes"] is not None]
        mf = [a["conf_med_faux"] for a in A if a["conf_med_faux"] is not None]
        L.append(f"| {c} | {sum(a['faux'] for a in A)} / {sum(a['n'] for a in A)} | {sum(a['faux_surs'] for a in A)} | "
                 f"{np.median(mj) if mj else float('nan'):.3f} / {np.median(mf) if mf else float('nan'):.3f} | "
                 f"{', '.join(str(a['tau']) if a['tau'] else '—' for a in A)} | "
                 f"{f(np.mean([a['abst_faux'] for a in A]))} % / {f(np.mean([a['abst_justes'] for a in A]))} % |")
    open(os.path.join(ICI, "resultats", "summary.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()
