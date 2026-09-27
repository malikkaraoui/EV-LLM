"""E009 -- evaluation des systemes appris par l'evaluateur UNIQUE d'E008 (evaluer / resume).

  python evalue.py --systeme A2 --graine 1 --phase val      # VAL 6-8 (300 / L) + T-ID
  python evalue.py --systeme A2 --graine 1 --phase final    # TEST + ADV-* : une seule fois
"""
import argparse
import json
import os
import time
from collections import Counter, defaultdict

import numpy as np

from bande import bandes, decode_cases, ecrire_json, jeux_final, jeux_id, jeux_val, lire_json
from evaluate import evaluer, resume  # E008, non modifie

ICI = os.path.dirname(os.path.abspath(__file__))


def systeme_appris(modele, regle, inverse, iters_log=None, plafond=None):
    """Fonction (paires) -> [(reponse | None, confiance)] ; journalise l'iteration retenue."""
    from boucle import PLAFOND_TEST, predire
    plafond = plafond or PLAFOND_TEST

    def f(paires):
        out = [None] * len(paires)
        groupes = defaultdict(list)
        for i, (a, b) in enumerate(paires):
            groupes[len(str(a)) + len(str(b)) + 2].append(i)
        for n, idx in sorted(groupes.items()):
            taille = min(500, max(25, 20_000 // (2 * n)))
            for k in range(0, len(idx), taille):
                sous = idx[k: k + taille]
                x, _, _, t_n = bandes([paires[i] for i in sous], inverse)
                tok, pm, t = predire(modele, regle, x, t_n, plafond)
                for j, i in enumerate(sous):
                    out[i] = decode_cases(tok[j], pm[j], inverse)
                if iters_log is not None:
                    iters_log[2 * n].extend(int(v) for v in t)
        return out

    return f


def charge(systeme, dossier, fichier="meilleur.safetensors"):
    import mlx.core as mx
    from archis import SYSTEMES
    m = SYSTEMES[systeme]["fabrique"]()
    m.load_weights(os.path.join(dossier, fichier))
    mx.eval(m.parameters())
    m.eval()
    return m


def nom_run(systeme, graine, fmt):
    return f"{systeme}-{fmt}-s{graine}"


def main():
    from archis import SYSTEMES
    ap = argparse.ArgumentParser()
    ap.add_argument("--systeme", required=True, choices=list(SYSTEMES))
    ap.add_argument("--graine", type=int, required=True)
    ap.add_argument("--fmt", default="inv", choices=["inv", "std"])
    ap.add_argument("--phase", required=True, choices=["val", "final"])
    args = ap.parse_args()
    dossier = os.path.join(ICI, "runs", nom_run(args.systeme, args.graine, args.fmt))
    etat = lire_json(os.path.join(dossier, "etat.json"))
    if not etat.get("fini"):
        raise SystemExit(f"entrainement inacheve : {etat['pas']}")
    sortie = os.path.join(dossier, f"resume_{args.phase}.json")
    if args.phase == "final" and os.path.exists(sortie):
        raise SystemExit("test final deja evalue pour ce run : une seule fois (PREREGISTREMENT 5)")
    if args.phase == "final" and not os.path.exists(os.path.join(ICI, "resultats", "FINAL_OUVERT")):
        raise SystemExit("test final verrouille : resultats/FINAL_OUVERT absent (fin du deroule)")
    jeux = {**jeux_val(), **jeux_id()} if args.phase == "val" else jeux_final()
    t0 = time.time()
    m = charge(args.systeme, dossier)
    iters = defaultdict(list)
    f = systeme_appris(m, SYSTEMES[args.systeme]["regle"], args.fmt == "inv", iters)
    recs = evaluer(f, jeux, args.systeme)
    with open(os.path.join(dossier, f"eval_{args.phase}.jsonl"), "w") as fh:
        for r in recs:
            fh.write(json.dumps({**r, "a": str(r["a"]), "b": str(r["b"])}) + "\n")
    res = resume(recs)
    nr = defaultdict(lambda: [0, 0])  # non-reponses parmi les faux
    for r in recs:
        if not r["juste"]:
            k = f"{r['jeu']}|{r['L']}"
            nr[k][0] += r["rep"] is None
            nr[k][1] += 1
    res["non_reponses_parmi_faux"] = {k: v for k, v in nr.items()}
    res["iterations_retenues"] = {str(k): {"min": min(v), "med": float(np.median(v)),
                                           "max": max(v), "top": Counter(v).most_common(3)}
                                  for k, v in sorted(iters.items())}
    res.update({"systeme": args.systeme, "graine": args.graine, "fmt": args.fmt,
                "checkpoint_pas": etat.get("meilleur", {}).get("pas"),
                "duree_eval_s": round(time.time() - t0, 1)})
    ecrire_json(res, sortie)
    print(f"{nom_run(args.systeme, args.graine, args.fmt)} {args.phase} : "
          f"{res['duree_eval_s']} s")
    for k, c in sorted(res["par_jeu"].items()):
        print(f"  {k:16s} exact {c['exact']:.3f}  faux_surs {c['faux_surs']}/{c['faux']}")


if __name__ == "__main__":
    main()
