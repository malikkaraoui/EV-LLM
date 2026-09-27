"""E013 -- evaluation finale (TEST, une seule fois) du checkpoint retenu par VAL-OOD.

  python evalue.py --runs I1-H1-s1 I1-H1-s2 ...     # runs/<nom>/meilleur.safetensors

Evaluateur E008 (`evaluate.evaluer` / `resume`) importe tel quel ; en plus : p_min par item.
"""
import argparse
import json
import os
import time

import donnees as D
from systemes import charge, details
from evaluate import evaluer, resume  # noqa: E402  (E008, via donnees)

ICI = os.path.dirname(os.path.abspath(__file__))


def evalue_run(nom, jeux):
    dossier = os.path.join(ICI, "runs", nom)
    etat = json.load(open(os.path.join(dossier, "etat.json")))
    if not etat["fini"]:
        raise SystemExit(f"{nom} : entrainement inacheve")
    if os.path.exists(os.path.join(dossier, "resume.json")):
        print(f"{nom} : deja evalue (TEST lu une seule fois)")
        return
    t0 = time.time()
    m = charge(etat["config"], os.path.join(dossier, "meilleur.safetensors"))
    pmins = []

    def sys_(paires):
        d = details(m, paires)
        pmins.extend(x[2] for x in d)
        return [(r, c) for r, c, _ in d]

    recs = evaluer(sys_, jeux, nom)
    with open(os.path.join(dossier, "eval.jsonl"), "w") as f:
        for r, pm in zip(recs, pmins):
            r["pmin"] = pm
            if r["L"] >= 100:  # items longs : on ne garde pas les operandes (poids)
                r["a"], r["b"], r["attendu"] = len(str(r["a"])), len(str(r["b"])), None
                r["rep_ok_longueur"] = r["rep"] is not None
                r["rep"] = None if r["juste"] else (r["rep"][:40] if r["rep"] else None)
            f.write(json.dumps(r) + "\n")
    res = resume(recs)
    res.update({k: etat[k] for k in ("config", "graine", "lr", "pas_total", "meilleur_pas",
                                      "meilleur_val", "params", "exemples_vus",
                                      "exemples_uniques_vus", "duree_s")})
    res["duree_eval_s"] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(dossier, "resume.json"), "w"), indent=1)
    l16 = res["par_jeu"]["T-LONG|16"]["exact"]
    l1k = res["par_jeu"]["T-LONG|1000"]["exact"]
    print(f"{nom} : T-LONG 16 = {l16:.3f}, 1000 = {l1k:.3f} ({res['duree_eval_s']} s)", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True)
    a = ap.parse_args()
    jeux = D.jeux_test()
    for nom in a.runs:
        evalue_run(nom, jeux)


if __name__ == "__main__":
    main()
