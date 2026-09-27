"""E014 -- entrainement avec reprise, file de runs, budget par invocation.

  python entraine14.py --configs R0a R2 --graines 1 2 3 4 5          # hyperparametres.json
  python entraine14.py --configs R2 --graines 0 --lr 3e-3 --pas 12000 --tag pilote-lr3e-3

S'arrete de lui-meme apres --budget-min minutes (defaut 8,5) en sauvegardant ; relancer la meme
commande reprend. Checkpoint = meilleur VAL-OOD (egalite : le plus tardif). R1L : exactitude de
LECTURE sur VAL-OOD (aucune somme). R1J : part de la composition gelee R1L-s<g> + I1 E013 s<g>,
pas 0 compris dans les candidats.
"""
import argparse
import json
import os
import time

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
from mlx.utils import tree_flatten, tree_unflatten

import d14 as D
from m14 import perte_addition, perte_lecture
from modeles import nb_parametres
from s14 import composition_gelee, cree, lecture_exacte, val_exact

ICI = os.path.dirname(os.path.abspath(__file__))
EVAL_TOUS = 250


def paires_du_lot(config, graine, pas, pas_total):
    if config == "R0b":
        return D.paires_curriculum(graine, pas, pas_total)
    return D.paires_flux(graine, pas)


def lot(config, graine, pas, pas_total):
    paires = paires_du_lot(config, graine, pas, pas_total)
    A, B, Y, M = D.encode_aligne(paires, D.T_TRAIN)
    S = mx.array(D.encode_plat(paires, D.P_TRAIN))
    if config == "R1L":
        return (S, mx.array(A), mx.array(B), mx.array(M))
    return (S, mx.array(Y), mx.array(M))


def valide(config, m):
    return lecture_exacte(m, D.jeu_val()) if config == "R1L" else val_exact(m)


def un_run(config, graine, lr, pas_total, dossier, t_fin, tag=""):
    os.makedirs(dossier, exist_ok=True)
    f_etat = os.path.join(dossier, "etat.json")
    etat = json.load(open(f_etat)) if os.path.exists(f_etat) else None
    if etat and etat["fini"]:
        return True
    mx.random.seed(graine)
    if config == "R1J":
        m = composition_gelee(graine, os.path.join(ICI, "runs", f"R1L-s{graine}" + (f"-{tag}" if tag else ""),
                                                   "meilleur.safetensors"))
    else:
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
        if config == "R1J":  # candidat pas 0 = composition gelee
            v = valide(config, m)
            etat["val"].append([0, None, v])
            etat["meilleur_val"], etat["meilleur_pas"] = v, 0
            m.save_weights(os.path.join(dossier, "meilleur.safetensors"))
    T = D.T_TRAIN
    if config == "R1L":
        vg = nn.value_and_grad(m, lambda mm, S, A, B, M: perte_lecture(mm, S, A, B, M, T))
    else:
        vg = nn.value_and_grad(m, lambda mm, S, Y, M: perte_addition(mm, S, Y, M, T))
    t0 = time.time()

    def sauve():
        m.save_weights(os.path.join(dossier, "poids.safetensors"))
        mx.save_safetensors(os.path.join(dossier, "opt.safetensors"),
                            dict(tree_flatten(opt.state)))
        etat["duree_s"] = round(etat["duree_s"] + time.time() - t0, 1)
        json.dump(etat, open(f_etat, "w"), indent=1)

    while etat["pas"] < pas_total:
        l, g = vg(m, *lot(config, graine, etat["pas"], pas_total))
        g, _ = optim.clip_grad_norm(g, 1.0)
        opt.update(m, g)
        mx.eval(m.parameters(), opt.state, l)
        etat["pas"] += 1
        if etat["pas"] % EVAL_TOUS == 0 or etat["pas"] == pas_total:
            v = valide(config, m)
            etat["val"].append([etat["pas"], round(float(l), 5), v])
            if v >= etat["meilleur_val"]:
                etat["meilleur_val"], etat["meilleur_pas"] = v, etat["pas"]
                m.save_weights(os.path.join(dossier, "meilleur.safetensors"))
            if etat["pas"] == pas_total:
                vus = set()
                for t in range(pas_total):
                    vus.update(paires_du_lot(config, graine, t, pas_total))
                etat["exemples_vus"] = pas_total * D.LOT
                etat["exemples_uniques_vus"] = len(vus)
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
    a = ap.parse_args()
    t_fin = time.time() + 60 * a.budget_min
    hp = json.load(open(os.path.join(ICI, "hyperparametres.json"))) if a.lr is None else None
    for c in a.configs:
        for g in a.graines:
            lr, pas = (hp[c]["lr"], hp[c]["pas"]) if hp else (a.lr, a.pas)
            nom = f"{c}-s{g}" + (f"-{a.tag}" if a.tag else "")
            fini = un_run(c, g, lr, pas, os.path.join(ICI, "runs", nom), t_fin, a.tag)
            if not fini or time.time() > t_fin:
                print("BUDGET atteint : relancer la meme commande")
                return
    print("FILE TERMINEE")


if __name__ == "__main__":
    main()
