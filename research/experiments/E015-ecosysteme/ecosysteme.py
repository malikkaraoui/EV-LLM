"""E015 -- phase A : ecosysteme (evolution + vie) sur 5 mini-taches, archive MAP-Elites -> bibliotheque.

  python ecosysteme.py --graines 0            # pilote
  python ecosysteme.py --graines 1 2 3 4 5    # un processus par graine
Sortie : runs/lib-s<g>/bibliotheque.pkl (poids numpy + meta) et journal.json.
"""
import argparse
import json
import os
import pickle
import time
from multiprocessing import Pool

import numpy as np

from circuits import exact_mini, init_poids, vie
from d15 import MINI, PORTS, val_mini

ICI = os.path.dirname(os.path.abspath(__file__))
HS, FS = [1, 2, 3, 4, 6, 8], [8, 16, 32]


def hp():
    return json.load(open(os.path.join(ICI, "hyperparametres.json")))["ecosysteme"]


def niche(tache, H):
    return f"{tache}|{'petit' if H <= 2 else 'grand'}"


def mute(rng, g):
    g = dict(g)
    quoi = rng.integers(0, 3)
    if quoi == 0:
        g["H"] = int(rng.choice(HS))
    elif quoi == 1:
        g["F"] = int(rng.choice(FS))
    else:
        g["loglr"] = float(np.clip(g["loglr"] + rng.normal(0, 0.3), -3, -1.5))
    return g


def une_graine(graine):
    H = hp()
    t0 = time.time()
    rng = np.random.default_rng([80_000 + graine])
    archive, journal, n_vie = {}, [], 0
    for tache in MINI:
        val = val_mini(tache)
        k = PORTS[tache]
        pop = []
        for _ in range(H["population"]):
            g = {"H": int(rng.choice(HS)), "F": int(rng.choice(FS)),
                 "loglr": float(rng.uniform(-3, -1.5))}
            pop.append((g, None))
        evalues = []
        for gen in range(H["generations"]):
            nouveaux = []
            for g, P_parent in pop:
                P0 = (P_parent if P_parent is not None
                      else init_poids(np.random.default_rng([90_000 + graine, n_vie]), k,
                                      g["H"], g["F"]))
                P = vie(P0, tache, graine, H["pas_vie"], 10 ** g["loglr"],
                        decalage=n_vie * H["pas_vie"])
                n_vie += 1
                s = exact_mini(P, tache, val)
                nouveaux.append((s, g, P))
                journal.append({"tache": tache, "gen": gen, "genome": g, "val": s})
                nk = niche(tache, g["H"])
                if nk not in archive or s > archive[nk]["val"]:
                    archive[nk] = {"val": s, "genome": g, "poids": P, "tache": tache,
                                   "ports": k}
            evalues = sorted(evalues + nouveaux, key=lambda x: -x[0])[: H["garder"]]
            pop = []
            for j in range(H["population"] - H["garder"]):
                s, g, P = evalues[j % len(evalues)]
                g2 = mute(rng, g)
                pop.append((g2, P if (g2["H"], g2["F"]) == (g["H"], g["F"]) else None))
    lib = [dict(v, niche=k) for k, v in sorted(archive.items())]
    dos = os.path.join(ICI, "runs", f"lib-s{graine}")
    os.makedirs(dos, exist_ok=True)
    pickle.dump(lib, open(os.path.join(dos, "bibliotheque.pkl"), "wb"))
    meta = {"graine": graine, "vies": n_vie, "duree_s": round(time.time() - t0, 1),
            "bibliotheque": [{"niche": c["niche"], "val": c["val"], "genome": c["genome"]}
                             for c in lib],
            "journal": journal}
    json.dump(meta, open(os.path.join(dos, "journal.json"), "w"), indent=1)
    return graine, meta["duree_s"], [(c["niche"], c["val"]) for c in lib]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graines", type=int, nargs="+", required=True)
    a = ap.parse_args()
    with Pool(len(a.graines)) as p:
        for g, d, lib in p.imap_unordered(une_graine, a.graines):
            print(f"graine {g} : {d} s")
            for nk, v in lib:
                print(f"  {nk:18s} VAL {v:.3f}")


if __name__ == "__main__":
    main()
