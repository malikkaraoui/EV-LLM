"""E008 -- entrainement B-STD / B-REF avec reprise sur checkpoint.

Chaque invocation s'arrete d'elle-meme apres --budget-min minutes de calcul (defaut 8.5)
et sauvegarde ; relancer la meme commande reprend au pas suivant. Enchainer au premier plan.

  python train.py --systeme B-STD --graine 1
"""
import argparse
import csv
import json
import os
import time
from functools import partial

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
from mlx.utils import tree_flatten, tree_unflatten

from data import ecrire_json, jeux_de_test, lire_json, lot, paires_exclues
from model import Additionneur, lr_schedule, nb_parametres, perte

ICI = os.path.dirname(os.path.abspath(__file__))


def sous_jeux_jalon(jeux):
    """100 premiers items de T-ID (L=2..5) et T-OOD (L=6, 8) -- PREREGISTREMENT section 4."""
    return {"T-ID": {L: v[:100] for L, v in jeux["T-ID"].items()},
            "T-OOD": {L: jeux["T-OOD"][L][:100] for L in (6, 8)}}


def entrainer(systeme, graine, dossier, hp, budget_s, jalons=True, modele_kw=None, log=print):
    os.makedirs(dossier, exist_ok=True)
    inverse = systeme == "B-REF"
    f_etat = os.path.join(dossier, "etat.json")

    mx.random.seed(graine)
    modele = Additionneur(positions=not inverse, **(modele_kw or {}))
    sched = lr_schedule(hp["lr_max"], hp["montee"], hp["pas"], hp["lr_min"])
    opt = optim.AdamW(learning_rate=sched, betas=hp["betas"], weight_decay=hp["wd"])
    opt.init(modele.trainable_parameters())

    etat = {"pas": 0, "calcul_s": 0.0, "invocations": 0, "params": nb_parametres(modele)}
    if os.path.exists(f_etat):
        etat = lire_json(f_etat)
        modele.load_weights(os.path.join(dossier, "poids.safetensors"))
        opt.state = tree_unflatten(list(mx.load(os.path.join(dossier, "opt.safetensors")).items()))
    mx.eval(modele.parameters(), opt.state)
    etat["invocations"] += 1

    ex = paires_exclues()
    loss_and_grad = nn.value_and_grad(modele, perte)
    st = [modele.state, opt.state]

    @partial(mx.compile, inputs=st, outputs=st)
    def pas_opt(x, y, m):
        l, g = loss_and_grad(modele, x, y, m)
        g, _ = optim.clip_grad_norm(g, hp["clip"])
        opt.update(modele, g)
        return l

    jeux_j = sous_jeux_jalon(jeux_de_test()) if jalons else None
    t0 = time.time()
    somme, n = 0.0, 0
    while etat["pas"] < hp["pas"] and time.time() - t0 < budget_s:
        x, y, m = (mx.array(v) for v in lot(graine, etat["pas"], ex, inverse, hp["lot"]))
        l = pas_opt(x, y, m)
        mx.eval(st)
        etat["pas"] += 1
        somme += l.item()
        n += 1
        if etat["pas"] % 500 == 0:
            log(f"{systeme} s{graine} pas {etat['pas']} perte {somme / n:.4f}")
            with open(os.path.join(dossier, "journal.csv"), "a") as f:
                f.write(f"{etat['pas']},{somme / n:.6f}\n")
            somme, n = 0.0, 0
        if jalons and (etat["pas"] in hp["jalons"] or etat["pas"] == hp["pas"]):
            jalon(modele, inverse, jeux_j, etat["pas"], hp["lot"], dossier)
    etat["calcul_s"] += time.time() - t0
    etat["fini"] = etat["pas"] >= hp["pas"]
    modele.save_weights(os.path.join(dossier, "poids.safetensors"))
    mx.save_safetensors(os.path.join(dossier, "opt.safetensors"), dict(tree_flatten(opt.state)))
    ecrire_json(etat, f_etat)
    return etat


def jalon(modele, inverse, jeux_j, pas, taille_lot, dossier):
    from evaluate import evaluer, resume, systeme_modele
    modele.eval()
    r = resume(evaluer(systeme_modele(modele, inverse), jeux_j, "jalon"))["par_jeu"]
    modele.train()
    f = os.path.join(dossier, "courbe.csv")
    neuf = not os.path.exists(f)
    with open(f, "a", newline="") as fh:
        w = csv.writer(fh)
        if neuf:
            w.writerow(["pas", "exemples_vus", "jeu", "L", "exact"])
        for k, c in sorted(r.items()):
            jeu, L = k.split("|")
            w.writerow([pas, pas * taille_lot, jeu, L, f"{c['exact']:.4f}"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systeme", required=True, choices=["B-STD", "B-REF"])
    ap.add_argument("--graine", type=int, required=True)
    ap.add_argument("--budget-min", type=float, default=8.5)
    args = ap.parse_args()
    if args.budget_min > 9:
        raise SystemExit("budget par invocation plafonne a 9 min (mandat)")
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    dossier = os.path.join(ICI, "runs", f"{args.systeme}-s{args.graine}")
    etat = entrainer(args.systeme, args.graine, dossier, hp, args.budget_min * 60)
    print(json.dumps(etat))


if __name__ == "__main__":
    main()
