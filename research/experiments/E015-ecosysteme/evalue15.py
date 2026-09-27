"""E015 -- TEST final (une seule fois par run) + VAL-OOD (pour le seuil d'abstention).

  python evalue15.py --runs EVO-N1-s1 ...
Refuse de reevaluer un run deja evalue (runs/<run>/test.jsonl existe).
"""
import argparse
import json
import os
import time
from multiprocessing import Pool

from compose import charge_lib, json_prog, systeme
from d15 import evaluer, exact_par_jeu, jeu_val, jeux_test, resume

ICI = os.path.dirname(os.path.abspath(__file__))
TAUS = [0.99, 0.9, 0.8, 0.7, 0.6, 0.5]


def tau_val(recs_val):
    justes = [r["conf"] for r in recs_val if r["juste"]]
    if not justes:
        return None
    for t in TAUS:  # plus grand seuil laissant <= 5 % des justes sous tau
        if sum(c < t for c in justes) <= 0.05 * len(justes):
            return t
    return None


def un_run(run):
    dos = os.path.join(ICI, "runs", run)
    if os.path.exists(os.path.join(dos, "test.jsonl")):
        return run, "deja evalue (TEST lu une seule fois)"
    res = json.load(open(os.path.join(dos, "resultat.json")))
    lib = charge_lib(res["graine"])
    prog = json_prog(os.path.join(dos, "resultat.json"))
    t0 = time.time()
    f = systeme(prog, lib, res["tache"])
    rv = evaluer(f, jeu_val(res["tache"]), run, res["tache"])
    tau = tau_val(rv)
    rt = evaluer(f, jeux_test(res["tache"]), run, res["tache"])
    with open(os.path.join(dos, "test.jsonl"), "w") as fo:
        for r in rt:
            fo.write(json.dumps(r) + "\n")
    faux = [r for r in rt if not r["juste"] and r["jeu"] != "T-ID"]
    justes = [r for r in rt if r["juste"] and r["jeu"] != "T-ID"]
    out = {"run": run, "exact": exact_par_jeu(rt), "val_exact": exact_par_jeu(rv),
           "resume_e008": resume(rt)["par_jeu"], "tau": tau,
           "faux_hors_tid": len(faux), "justes_hors_tid": len(justes),
           "faux_surs": sum(r["conf"] >= 0.8 for r in faux),
           "abstention_quand_faux": (sum(r["conf"] < tau for r in faux) / len(faux)
                                     if tau and faux else None),
           "abstention_quand_juste": (sum(r["conf"] < tau for r in justes) / len(justes)
                                      if tau and justes else None),
           "duree_s": round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(dos, "test.json"), "w"), indent=1)
    return run, f"T-LONG 16 = {out['exact']['T-LONG|16']:.3f} ({out['duree_s']} s)"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True)
    a = ap.parse_args()
    with Pool(min(6, len(a.runs))) as p:
        for run, msg in p.imap_unordered(un_run, a.runs):
            print(f"{run:16s} {msg}", flush=True)


if __name__ == "__main__":
    main()
