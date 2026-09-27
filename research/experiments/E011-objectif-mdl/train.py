"""E011 -- partie 1 : on continue l'entrainement depuis le reseau golden (PREREGISTREMENT s. 4).

Usage :
  python train.py --graines 0            # pilote (exclu)
  python train.py --graines 1 2 3 4 5    # runs officiels (reprend : saute les runs finis)
Sortie : runs/<config>-s<g>/run.json (trajectoire, theta final). Aucun acces au test final.
"""
import argparse
import os
import time

import numpy as np

from donnees import (ICI, ecrire_json, encode, jeu_entrainement, jeu_validation, lire_json)
from objectifs import modele_evalue, objectif_grad, objectif_local
from rnn import forward, golden, sig

JALONS = [0, 10, 30, 100, 300, 1000, 3000, 10000, 20000]


def configs(hp):
    out = [("a", None)]
    out += [("b", lam) for lam in hp["lambdas"]]
    out += [("c", lam) for lam in hp["lambdas"]]
    out += [("e", None), ("d", None), ("d-CE", None), ("d-L2", None)]
    return out


def nom(code, lam):
    return code if lam is None else f"{code}-lam{lam:g}"


class Validation:
    def __init__(self):
        paires = [p for items in jeu_validation()["V-OOD"].values() for p in items]
        self.X, self.Y, self.M = encode(paires)

    def exact(self, theta):
        z, _ = forward(theta, self.X)
        ok = ((sig(z) > 0.5) == (self.Y > 0.5)) | (self.M == 0)
        return float(ok.all(axis=1).mean())


def run(code, lam, graine, hp, val, theta0):
    rng = np.random.default_rng([40_000 + graine, sum(map(ord, code))])
    paires = jeu_entrainement(graine)
    X, Y, M = encode(paires)
    th = theta0.copy()
    pas_total, tous = hp["pas"], hp["controle_val_tous"]
    traj, premiere_perte = [], None
    local = code.startswith("d")
    if local:
        f = objectif_local(code)
        cur = f(th, X, Y, M)
        acceptes = 0
    else:
        f = objectif_grad(code, lam)
        m1 = np.zeros_like(th); m2 = np.zeros_like(th)
        b1, b2, eps = hp["betas"][0], hp["betas"][1], 1e-8
        ordre = []

    def note(pas):
        mod = modele_evalue(code, th)
        from rnn import ce_bits
        ce = ce_bits(forward(mod, X)[0], Y, M)
        obj = cur if local else f(th, X, Y, M)[0]
        traj.append({"pas": pas, "ce_train_bits": ce, "objectif": float(obj),
                     "dist_golden": float(np.linalg.norm(th - theta0)),
                     "norme": float(np.linalg.norm(th)), "val_exact": val.exact(mod)})

    note(0)
    for pas in range(1, pas_total + 1):
        if local:
            i = int(rng.integers(0, th.size))
            d = (1.0 if rng.random() < 0.5 else -1.0) / 2 ** int(rng.integers(0, 4))
            prop = th.copy(); prop[i] += d
            v = f(prop, X, Y, M)
            if v <= cur:
                th, cur = prop, v
                acceptes += 1
        else:
            if not ordre:
                ordre = list(rng.permutation(len(paires)).reshape(-1, hp["lot"]))
            idx = ordre.pop()
            _, _, g = f(th, X[idx], Y[idx], M[idx])
            m1 = b1 * m1 + (1 - b1) * g
            m2 = b2 * m2 + (1 - b2) * g * g
            mh = m1 / (1 - b1 ** pas); vh = m2 / (1 - b2 ** pas)
            th = th - hp["lr"] * mh / (np.sqrt(vh) + eps)
        if not np.all(np.isfinite(th)):
            raise FloatingPointError(f"{code} s{graine} : NaN au pas {pas}")
        if premiere_perte is None and pas % tous == 0:
            if val.exact(modele_evalue(code, th)) < 1.0:
                premiere_perte = pas
        if pas in JALONS:
            note(pas)
    out = {"config": nom(code, lam), "code": code, "lambda": lam, "graine": graine,
           "pas": pas_total, "exemples_uniques": len(paires),
           "premiere_perte_val": premiere_perte, "resolution_perte": tous,
           "trajectoire": traj, "theta_final": modele_evalue(code, th).tolist(),
           "theta_brut": th.tolist()}
    if local:
        out["propositions_acceptees"] = acceptes
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graines", type=int, nargs="+", required=True)
    ap.add_argument("--budget-s", type=float, default=510.0)
    args = ap.parse_args()
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    val = Validation()
    theta0 = golden(hp["k"], hp["k"])
    t0 = time.time()
    for g in args.graines:
        for code, lam in configs(hp):
            d = os.path.join(ICI, "runs", f"{nom(code, lam)}-s{g}")
            if os.path.exists(os.path.join(d, "run.json")):
                continue
            if time.time() - t0 > args.budget_s:
                print("budget d'invocation atteint : relancer"); return
            t1 = time.time()
            r = run(code, lam, g, hp, val, theta0)
            r["duree_s"] = round(time.time() - t1, 1)
            os.makedirs(d, exist_ok=True)
            ecrire_json(r, os.path.join(d, "run.json"))
            fin = r["trajectoire"][-1]
            print(f"{r['config']:12s} s{g} {r['duree_s']:6.1f}s val={fin['val_exact']:.3f} "
                  f"perte@{r['premiere_perte_val']} dist={fin['dist_golden']:.2f} "
                  f"ce={fin['ce_train_bits']:.3g}", flush=True)
    print("FINI")


if __name__ == "__main__":
    main()
