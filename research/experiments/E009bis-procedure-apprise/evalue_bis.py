"""E009-bis -- evaluation par l'evaluateur UNIQUE d'E008, seulement si la distribution est apprise.

  python evalue_bis.py --run A1-s1 --phase val     # VAL 6-8 (300 / L) + T-ID (200 / L)
  python evalue_bis.py --run A1-s1 --phase final   # TEST + ADV-* : une seule fois, a la fin
  python evalue_bis.py --run pilote-A1-w64-lr0.001 --phase pilote  # T-ID + VAL (100 / L)
  python evalue_bis.py --run A1-s1 --phase tid     # T-ID (200 / L) des poids finaux, tout run
"""
import argparse
import json
import os
import time
from collections import Counter, defaultdict

import numpy as np

import curric as C
from bande import ecrire_json, jeux_final, jeux_id, lire_json, sous_val  # E009
from evaluate import evaluer, resume  # E008
from evalue import systeme_appris  # E009

ICI = os.path.dirname(os.path.abspath(__file__))


def charge(etat, dossier, fichier):
    import mlx.core as mx
    m = C.fabrique(etat["systeme"], etat["w"])
    m.load_weights(os.path.join(dossier, fichier))
    mx.eval(m.parameters())
    m.eval()
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--phase", required=True, choices=["pilote", "tid", "val", "final"])
    args = ap.parse_args()
    dossier = os.path.join(ICI, "runs", args.run)
    etat = lire_json(os.path.join(dossier, "etat.json"))
    if not etat.get("fini"):
        raise SystemExit(f"entrainement inacheve : {etat['pas']}")
    if args.phase == "pilote":
        if etat["graine"] != 0:
            raise SystemExit("phase pilote reservee a la graine 0")
        jeux, fichier = {**C.t_id(range(2, 6), 100), **sous_val(100)}, "poids.safetensors"
    elif args.phase == "tid":  # dans la distribution seulement : permis pour tout run officiel
        if etat["graine"] == 0:
            raise SystemExit("graine 0 = pilote, exclue")
        jeux, fichier = C.t_id(range(2, 6), 200), "poids.safetensors"
    else:
        if etat["graine"] == 0:
            raise SystemExit("graine 0 = pilote, exclue")
        if not etat.get("appris"):
            raise SystemExit("distribution non apprise : pas d'evaluation hors distribution "
                             "(PREREGISTREMENT-bis 2.3)")
        fichier = "meilleur.safetensors"
        if args.phase == "val":
            jeux = {**b9_val(), **jeux_id()}
        else:
            if os.path.exists(os.path.join(dossier, "resume_final.json")):
                raise SystemExit("test final deja evalue pour ce run : une seule fois")
            if not os.path.exists(os.path.join(ICI, "resultats", "FINAL_OUVERT")):
                raise SystemExit("test final verrouille : resultats/FINAL_OUVERT absent")
            jeux = jeux_final()
    sortie = os.path.join(dossier, f"resume_{args.phase}.json")
    t0 = time.time()
    m = charge(etat, dossier, fichier)
    iters = defaultdict(list)
    f = systeme_appris(m, C.regle(etat["systeme"]), True, iters)
    recs = evaluer(f, jeux, etat["systeme"])
    with open(os.path.join(dossier, f"eval_{args.phase}.jsonl"), "w") as fh:
        for r in recs:
            fh.write(json.dumps({**r, "a": str(r["a"]), "b": str(r["b"])}) + "\n")
    res = resume(recs)
    nr = defaultdict(lambda: [0, 0])  # non-reponses (abstentions) parmi les faux
    for r in recs:
        if not r["juste"]:
            k = f"{r['jeu']}|{r['L']}"
            nr[k][0] += r["rep"] is None
            nr[k][1] += 1
    res["non_reponses_parmi_faux"] = dict(nr)
    res["iterations_retenues"] = {str(k): {"min": min(v), "med": float(np.median(v)),
                                           "max": max(v), "top": Counter(v).most_common(3)}
                                  for k, v in sorted(iters.items())}
    res.update({"run": args.run, "systeme": etat["systeme"], "graine": etat["graine"],
                "w": etat["w"], "lr": etat["lr"], "pas": etat["pas"], "niveau": etat["niveau"],
                "duree_eval_s": round(time.time() - t0, 1)})
    ecrire_json(res, sortie)
    print(f"{args.run} {args.phase} : {res['duree_eval_s']} s (pas {etat['pas']}, "
          f"niveau {etat['niveau']})")
    for k, c in sorted(res["par_jeu"].items()):
        print(f"  {k:16s} exact {c['exact']:.3f}  faux_surs {c['faux_surs']}/{c['faux']}")


def b9_val():
    from bande import jeux_val  # E009 : VAL 6-8, 300 / L
    return jeux_val()


if __name__ == "__main__":
    main()
