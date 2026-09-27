"""E012 -- recherche evolutive en iles, selection MDL (PREREGISTREMENT section 4).

Une graine = un processus ; reprise sur checkpoint (runs/<exp>-s<g>/etat.pkl).
Usage : python recherche.py --exp X1 --graines 1 2 3 4 5 --minutes 8.5
"""
import argparse
import os
import pickle
import time
from multiprocessing import Pool

import numpy as np

from jeux import (EXPERIENCES, ICI, ecrire_json, encodeur, jeu_entrainement, jeu_validation,
                  lire_json, n_entrees)
from reseau import cle, evalue, longueur_G, mute, taille, vide

TAILLE_MEMO = 200_000


def charge_hp():
    return lire_json(os.path.join(ICI, "hyperparametres.json"))


class Recherche:
    def __init__(self, exp, graine, hp):
        self.exp, self.graine, self.hp = exp, graine, hp
        self.cfg = EXPERIENCES[exp]
        enc = encodeur(exp)
        self.train = enc(jeu_entrainement(exp, graine))
        self.val = enc([p for ps in jeu_validation(self.cfg["base"])["V-OOD"].values() for p in ps])
        self.memo = {}
        self.manques = 0

    # ------------------------------------------------------------ evaluation
    def note(self, g):
        k = cle(g)
        r = self.memo.get(k)
        if r is None:
            dg, faux, ex, n = evalue(g, self.train, self.cfg["base"])
            hg = longueur_G(g)
            r = (hg + dg, hg, dg, ex == n)
            if len(self.memo) >= TAILLE_MEMO:
                self.memo.clear()
            self.memo[k] = r
            self.manques += 1
        return r

    def exact_val(self, g):
        _, _, ex, n = evalue(g, self.val, self.cfg["base"])
        return ex / n

    # ------------------------------------------------------------ etat
    def init(self):
        rng = np.random.default_rng([50_000 + self.graine, hash_exp(self.exp)])
        iles = []
        nin = n_entrees(self.exp)
        for _ in range(self.hp["iles"]):
            pop = []
            for _ in range(self.hp["pop"]):
                g = vide(nin)
                for _ in range(int(rng.integers(0, 3))):
                    g = mute_ajout_avant(g, rng)
                pop.append((self.note(g)[0], g))
            pop.sort(key=lambda t: t[0])
            iles.append(pop)
        return {"gen": 0, "enfants": 0, "iles": iles, "rng": rng.bit_generator.state,
                "histo": [], "decouverte": None, "meilleur_depuis": 0, "mdl_meilleur": None,
                "fini": False, "raison": None, "manques": 0, "secondes": 0.0}

    def generation(self, etat, rng):
        P = self.hp["pop"]
        nouv = []
        for pop in etat["iles"]:
            enfants = []
            for _ in range(P):
                i, j = rng.integers(0, P, 2)
                parent = pop[min(i, j)][1]  # pop triee : le plus petit indice a le plus petit MDL
                g = parent
                for _ in range(1 + int(rng.poisson(self.hp.get("lambda_mut", 0.5)))):
                    g = mute(g, rng)
                enfants.append((self.note(g)[0], g))
            if self.hp.get("remplacement", "troncature") == "troncature":
                regroupe = enfants + pop[:2]
                regroupe.sort(key=lambda t: t[0])
                nouv.append(regroupe[:P])
            else:  # generationnel : les 2 meilleurs parents remplacent les 2 pires enfants
                enfants.sort(key=lambda t: t[0])
                regroupe = pop[:2] + enfants[:P - 2]
                regroupe.sort(key=lambda t: t[0])
                nouv.append(regroupe)
        etat["iles"] = nouv
        etat["gen"] += 1
        etat["enfants"] += P * len(nouv)
        if etat["gen"] % self.hp["migration"] == 0:
            meilleurs = [pop[0] for pop in nouv]
            for k, pop in enumerate(nouv):
                pop[-1] = meilleurs[k - 1]
                pop.sort(key=lambda t: t[0])

    def suivi(self, etat):
        best = min((pop[0] for pop in etat["iles"]), key=lambda t: t[0])
        mdl, g = best
        _, hg, dg, ok_train = self.note(g)
        val = self.exact_val(g)
        etat["histo"].append({"gen": etat["gen"], "enfants": etat["enfants"],
                              "evaluations": etat["manques"] + self.manques, "mdl": mdl,
                              "G": hg, "DG": dg, "train_exact": ok_train, "val_exact": val,
                              **taille(g)})
        if ok_train and val == 1.0 and etat["decouverte"] is None:
            etat["decouverte"] = dict(etat["histo"][-1])
        if etat["mdl_meilleur"] is None or mdl < etat["mdl_meilleur"] - 1e-9:
            etat["mdl_meilleur"], etat["meilleur_depuis"] = mdl, etat["gen"]
        if ok_train and val == 1.0 and etat["gen"] - etat["meilleur_depuis"] >= self.hp["patience"]:
            etat["fini"], etat["raison"] = True, "arret anticipe (exact train+val, MDL stable)"
        if etat["gen"] >= self.hp["generations"]:
            etat["fini"], etat["raison"] = True, "budget de generations"
        return best


def hash_exp(exp):
    return sum(ord(c) * 31 ** i for i, c in enumerate(exp)) % 1_000_003


def mute_ajout_avant(g, rng):
    from reseau import _rationnel
    s = int(rng.integers(0, g["nin"]))
    d = g["nin"]
    if not any(c[0] == s and c[1] == d and not c[2] for c in g["conns"]):
        n, q = _rationnel(rng)
        g["conns"].append((s, d, False, n, q))
    return g


def travaille(args):
    exp, graine, minutes, tag, surcharge = args
    hp = charge_hp()
    hp.update(surcharge)
    if isinstance(hp["generations"], dict):
        hp["generations"] = hp["generations"][exp]
    dossier = os.path.join(ICI, "runs", f"{tag}{exp}-s{graine}")
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, "etat.pkl")
    R = Recherche(exp, graine, hp)
    t0 = time.time()
    if os.path.exists(chemin):
        with open(chemin, "rb") as f:
            etat = pickle.load(f)
    else:
        etat = R.init()
    rng = np.random.default_rng()
    rng.bit_generator.state = etat["rng"]
    marque = dernier_ckpt = time.time()
    budget = hp.get("budget_mur_min", {}).get(exp, 1e9) * 60
    while not etat["fini"] and time.time() - t0 < minutes * 60:
        if etat["secondes"] + (time.time() - marque) >= budget:  # plafond mur (hyperparametres)
            R.suivi(etat)
            etat["fini"], etat["raison"] = True, "budget mur"
            break
        R.generation(etat, rng)
        if etat["gen"] % hp["suivi"] == 0 or etat["gen"] >= hp["generations"]:
            R.suivi(etat)
        if time.time() - dernier_ckpt > 240:
            marque = _sauve(etat, rng, R, chemin, marque)
            dernier_ckpt = time.time()
    _sauve(etat, rng, R, chemin, marque)
    best = min((pop[0] for pop in etat["iles"]), key=lambda t: t[0])
    if etat["fini"]:
        ecrire_json({"exp": exp, "graine": graine, "genome": _jsonable(best[1]),
                     "raison": etat["raison"], "gen": etat["gen"], "enfants": etat["enfants"],
                     "evaluations": etat["manques"], "secondes": round(etat["secondes"], 1),
                     "decouverte": etat["decouverte"], "histo": etat["histo"],
                     "exemples_uniques": EXPERIENCES[exp]["n_train"], "hp": hp},
                    os.path.join(dossier, "run.json"))
    h = etat["histo"][-1] if etat["histo"] else {}
    return (f"{exp} s{graine} gen={etat['gen']} enfants={etat['enfants']} "
            f"mdl={best[0]:.1f} G={h.get('G', 0):.0f} DG={h.get('DG', 0):.1f} "
            f"train={h.get('train_exact')} val={h.get('val_exact', 0):.3f} "
            f"cach={h.get('cachees')} conn={h.get('connexions')} fini={etat['fini']} "
            f"decouverte_gen={(etat['decouverte'] or {}).get('gen')} t={etat['secondes']:.0f}s")


def _sauve(etat, rng, R, chemin, marque):
    maintenant = time.time()
    etat["rng"] = rng.bit_generator.state
    etat["manques"] += R.manques
    R.manques = 0
    etat["secondes"] += maintenant - marque
    tmp = chemin + ".tmp"
    with open(tmp, "wb") as f:
        pickle.dump(etat, f)
    os.replace(tmp, chemin)
    return maintenant


def _jsonable(g):
    return {"nin": g["nin"], "cach": g["cach"], "act": {str(k): v for k, v in g["act"].items()},
            "conns": [list(c) for c in g["conns"]],
            "biais": {str(k): list(v) for k, v in g["biais"].items()}, "suiv": g["suiv"]}


def depuis_json(d):
    return {"nin": d["nin"], "cach": list(d["cach"]), "act": {int(k): v for k, v in d["act"].items()},
            "conns": [tuple(c) for c in d["conns"]],
            "biais": {int(k): tuple(v) for k, v in d["biais"].items()}, "suiv": d["suiv"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--exp", required=True, choices=list(EXPERIENCES))
    ap.add_argument("--graines", type=int, nargs="+", required=True)
    ap.add_argument("--minutes", type=float, default=8.5)
    ap.add_argument("--tag", default="", help="prefixe du dossier (pilotes)")
    ap.add_argument("--hp", default="{}", help="surcharge JSON des hyperparametres (pilotes)")
    a = ap.parse_args()
    import json
    with Pool(len(a.graines)) as pool:
        for ligne in pool.imap(travaille, [(a.exp, g, a.minutes, a.tag, json.loads(a.hp))
                                           for g in a.graines]):
            print(ligne, flush=True)


if __name__ == "__main__":
    main()
