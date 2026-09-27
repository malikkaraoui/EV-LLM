"""E014 -- evaluation finale (TEST, une seule fois) du checkpoint retenu par VAL-OOD.

  python evalue14.py --runs R0a-s1 R1G-s1 R1J-s1 ...

R1G-s<g> = composition gelee (lecteur R1L-s<g> + I1 H = 4 d'E013 s<g>), sans entrainement.
Seuil d'abstention tau fixe sur VAL-OOD (section 5) AVANT de lire TEST.
Evaluateur E008 (`evaluate.evaluer` / `resume`) importe tel quel ; confiance = p_min.
"""
import argparse
import json
import os
import time
from collections import defaultdict

import d14 as D
from evaluate import evaluer, resume  # noqa: E402  (E008)
from s14 import charge, composition_gelee, seuil_abstention, systeme

ICI = os.path.dirname(os.path.abspath(__file__))
SUR = 0.8


def modele_du_run(nom):
    dossier = os.path.join(ICI, "runs", nom)
    config, g = nom.split("-s")[0], int(nom.split("-s")[1])
    if config == "R1G":
        src = json.load(open(os.path.join(ICI, "runs", f"R1L-s{g}", "etat.json")))
        if not src["fini"]:
            raise SystemExit(f"R1L-s{g} : entrainement inacheve")
        os.makedirs(dossier, exist_ok=True)
        etat = {k: src[k] for k in ("lr", "pas_total", "meilleur_pas", "meilleur_val", "params",
                                     "exemples_vus", "exemples_uniques_vus", "duree_s")}
        etat.update(config="R1G", graine=g, fini=True, note="lecteur R1L gele + I1 E013 gele")
        json.dump(etat, open(os.path.join(dossier, "etat.json"), "w"), indent=1)
        return composition_gelee(g, os.path.join(ICI, "runs", f"R1L-s{g}", "meilleur.safetensors")), etat
    etat = json.load(open(os.path.join(dossier, "etat.json")))
    if not etat["fini"]:
        raise SystemExit(f"{nom} : entrainement inacheve")
    return charge(config, os.path.join(dossier, "meilleur.safetensors")), etat


def evalue_run(nom, jeux):
    dossier = os.path.join(ICI, "runs", nom)
    if os.path.exists(os.path.join(dossier, "resume.json")):
        print(f"{nom} : deja evalue (TEST lu une seule fois)")
        return
    t0 = time.time()
    m, etat = modele_du_run(nom)
    # 1. seuil d'abstention sur VAL-OOD seul
    jv = []
    rv = evaluer(systeme(m, jv), D.jeu_val(), nom)
    tau = seuil_abstention([d["pmin"] for r, d in zip(rv, jv) if r["juste"]])
    # 2. TEST, une seule fois
    jt = []
    recs = evaluer(systeme(m, jt), jeux, nom)
    ab = defaultdict(lambda: {"justes": 0, "faux": 0, "abst_justes": 0, "abst_faux": 0,
                              "faux_surs_prod": 0, "lu_ok": 0, "n": 0})
    with open(os.path.join(dossier, "eval.jsonl"), "w") as f:
        for r, d in zip(recs, jt):
            k = f"{r['jeu']}|{r['L']}"
            c = ab[k]
            c["n"] += 1
            abst = tau is not None and d["pmin"] < tau
            if r["juste"]:
                c["justes"] += 1
                c["abst_justes"] += abst
            else:
                c["faux"] += 1
                c["abst_faux"] += abst
                c["faux_surs_prod"] += d["prod"] >= SUR
            c["lu_ok"] += d.get("lu_ok", False)
            r.update(pmin=d["pmin"], prod=d["prod"], lu_ok=d.get("lu_ok"),
                     pmin_lu=d.get("pmin_lu"))
            if r["L"] >= 100:  # items longs : on ne garde pas les operandes (poids)
                r["a"], r["b"], r["attendu"] = len(str(r["a"])), len(str(r["b"])), None
                r["rep"] = None if r["juste"] else (r["rep"][:40] if r["rep"] else None)
            f.write(json.dumps(r) + "\n")
    res = resume(recs)
    res["abstention"] = {"tau": tau, "par_jeu": dict(ab)}
    res["lecture_exacte"] = ({k: c["lu_ok"] / c["n"] for k, c in ab.items()}
                             if "lu_ok" in jt[0] else None)
    res.update({k: etat.get(k) for k in ("config", "graine", "lr", "pas_total", "meilleur_pas",
                                          "meilleur_val", "params", "exemples_vus",
                                          "exemples_uniques_vus", "duree_s")})
    res["duree_eval_s"] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(dossier, "resume.json"), "w"), indent=1)
    pj = res["par_jeu"]
    print(f"{nom} : T-LONG 16 = {pj['T-LONG|16']['exact']:.3f}, 100 = {pj['T-LONG|100']['exact']:.3f}"
          f", 1000 = {pj['T-LONG|1000']['exact']:.3f} ; tau {tau} ({res['duree_eval_s']} s)",
          flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True)
    a = ap.parse_args()
    jeux = D.jeux_test()
    for nom in a.runs:
        evalue_run(nom, jeux)


if __name__ == "__main__":
    main()
