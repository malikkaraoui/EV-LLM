"""E013 -- entrainement avec reprise, file de runs, budget par invocation.

  python entraine.py --configs I1-H1 I1-H4 --graines 1 2 3 4 5     # hyperparametres.json
  python entraine.py --configs I1-H4 --graines 0 --lr 3e-3 --pas 3000 --tag pilote

S'arrete de lui-meme apres --budget-min minutes (defaut 8,5) en sauvegardant ; relancer la meme
commande reprend. Checkpoint retenu = meilleur exact-match moyen VAL-OOD (egalite : le plus tardif).
"""
import argparse
import json
import os
import time

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
import numpy as np
from mlx.utils import tree_flatten, tree_unflatten

import donnees as D
from modeles import I2, nb_parametres, perte
from systemes import cree, systeme

ICI = os.path.dirname(os.path.abspath(__file__))
EVAL_TOUS = 250
T_TRAIN = 6          # max(l) + 1 avec l <= 5
P_TRAIN = 13         # DEBUT + 5 + '+' + 5 + '='


def val_exact(m):
    from evaluate import evaluer, resume  # evaluateur E008
    r = resume(evaluer(systeme(m), D.jeu_val(), "val"))["par_jeu"]
    return float(np.mean([c["exact"] for c in r.values()]))


def lot(config, graine, pas, jeu_fixe):
    paires = (D.paires_fixes(jeu_fixe, graine, pas) if jeu_fixe is not None
              else D.paires_flux(graine, pas))
    A, B, Y, M = D.encode_aligne(paires, T_TRAIN)
    if config == "I2":
        entree = (mx.array(D.encode_plat(paires, P_TRAIN)),)
    else:
        entree = (mx.array(A), mx.array(B))
    return entree, mx.array(Y), mx.array(M)


def uniques_vus(config, graine, pas_total, jeu_fixe):
    vus = set()
    for t in range(pas_total):
        vus.update(D.paires_fixes(jeu_fixe, graine, t) if jeu_fixe is not None
                   else D.paires_flux(graine, t))
    return len(vus)


def un_run(config, graine, lr, pas_total, dossier, t_fin):
    os.makedirs(dossier, exist_ok=True)
    f_etat = os.path.join(dossier, "etat.json")
    etat = json.load(open(f_etat)) if os.path.exists(f_etat) else None
    if etat and etat["fini"]:
        return True
    mx.random.seed(graine)
    m = cree(config)
    opt = optim.Adam(learning_rate=lr)
    if etat:
        m.load_weights(os.path.join(dossier, "poids.safetensors"))
        opt.init(m.trainable_parameters())
        opt.state = tree_unflatten(list(mx.load(os.path.join(dossier, "opt.safetensors")).items()))
    else:
        etat = {"config": config, "graine": graine, "lr": lr, "pas_total": pas_total, "pas": 0,
                "lot": D.LOT, "params": nb_parametres(m), "val": [], "meilleur_pas": None,
                "meilleur_val": -1.0, "duree_s": 0.0, "fini": False}
    jeu_fixe = (D.jeu_fixe(graine, int(config[4:])) if config.startswith("I3-N") else None)
    T = T_TRAIN
    vg = nn.value_and_grad(m, lambda mm, e, y, mk: perte(mm, e, y, mk, T))
    t0 = time.time()

    def sauve():
        m.save_weights(os.path.join(dossier, "poids.safetensors"))
        mx.save_safetensors(os.path.join(dossier, "opt.safetensors"),
                            dict(tree_flatten(opt.state)))
        etat["duree_s"] = round(etat["duree_s"] + time.time() - t0, 1)
        json.dump(etat, open(f_etat, "w"), indent=1)

    while etat["pas"] < pas_total:
        e, y, mk = lot(config, graine, etat["pas"], jeu_fixe)
        l, g = vg(m, e, y, mk)
        g, _ = optim.clip_grad_norm(g, 1.0)
        opt.update(m, g)
        mx.eval(m.parameters(), opt.state, l)
        etat["pas"] += 1
        if etat["pas"] % EVAL_TOUS == 0 or etat["pas"] == pas_total:
            v = val_exact(m)
            etat["val"].append([etat["pas"], round(float(l), 5), v])
            if v >= etat["meilleur_val"]:
                etat["meilleur_val"], etat["meilleur_pas"] = v, etat["pas"]
                m.save_weights(os.path.join(dossier, "meilleur.safetensors"))
            if etat["pas"] == pas_total:
                etat["exemples_vus"] = pas_total * min(D.LOT, len(jeu_fixe) if jeu_fixe else D.LOT)
                etat["exemples_uniques_vus"] = uniques_vus(config, graine, pas_total, jeu_fixe)
                etat["fini"] = True
            sauve()
            t0 = time.time()
            print(f"{config} s{graine} pas {etat['pas']} perte {float(l):.4f} val {v:.3f}",
                  flush=True)
            if time.time() > t_fin and not etat["fini"]:
                return False
    return etat["fini"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--configs", nargs="+", required=True)
    ap.add_argument("--graines", nargs="+", type=int, required=True)
    ap.add_argument("--lr", type=float)
    ap.add_argument("--pas", type=int)
    ap.add_argument("--tag", default="")
    ap.add_argument("--budget-min", type=float, default=8.5)
    ap.add_argument("--cpu", action="store_true")
    a = ap.parse_args()
    if a.cpu:
        mx.set_default_device(mx.cpu)
    t_fin = time.time() + 60 * a.budget_min
    hp = json.load(open(os.path.join(ICI, "hyperparametres.json"))) if a.lr is None else None
    for c in a.configs:
        for g in a.graines:
            if hp:
                cle = "I2" if c == "I2" else "I1"
                lr, pas = hp[cle]["lr"], hp[cle]["pas"]
            else:
                lr, pas = a.lr, (a.pas * (2 if c == "I2" else 1))
            nom = f"{c}-s{g}" + (f"-{a.tag}" if a.tag else "")
            fini = un_run(c, g, lr, pas, os.path.join(ICI, "runs", nom), t_fin)
            if not fini or time.time() > t_fin:
                print("BUDGET atteint : relancer la meme commande")
                return
    print("FILE TERMINEE")


if __name__ == "__main__":
    main()
