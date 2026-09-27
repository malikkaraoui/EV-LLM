"""E010 -- entrainement avec reprise sur checkpoint, par file de runs.

Un run = format x positions x reserve N x graine. Chaque invocation s'arrete d'elle-meme
apres --budget-min minutes (<= 9) et sauvegarde ; relancer la meme commande reprend.

  python entrainer.py --plan crible          # file officielle (voir PLANS)
  python entrainer.py --run F1 nope 384000 0 # un run isole (pilote)
"""
import argparse
import json
import os
import time
from functools import partial

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim
from mlx.utils import tree_flatten, tree_unflatten

from donnees import BATCH, FORMATS, ecrire_json, lire_json, lot, uniques_vus
from modele import Additionneur, lr_schedule, nb_parametres, perte

ICI = os.path.dirname(os.path.abspath(__file__))


def nom_run(fmt, pos, n, graine):
    return f"{fmt}-{pos}-N{n}-s{graine}"


def plans(hp):
    nmax = hp["pas"] * BATCH
    crible = [(f, p, nmax, g) for g in (1, 2) for f in FORMATS for p in ("abs", "nope")]
    courbe = [(f, p, n, 1) for n in (1_000, 10_000, 100_000) for f in ("F0", "F1")
              for p in ("abs", "nope")]
    return {"crible": crible, "courbe": courbe}


def entrainer(fmt, pos, n, graine, hp, budget_s, log=print):
    nom = nom_run(fmt, pos, n, graine)
    dossier = os.path.join(ICI, "runs", nom)
    os.makedirs(dossier, exist_ok=True)
    f_etat = os.path.join(dossier, "etat.json")
    if os.path.exists(f_etat) and lire_json(f_etat).get("fini"):
        return lire_json(f_etat)

    mx.random.seed(graine)
    modele = Additionneur(positions=(pos == "abs"))
    sched = lr_schedule(hp["lr_max"], hp["montee"], hp["pas"], hp["lr_min"])
    opt = optim.AdamW(learning_rate=sched, betas=hp["betas"], weight_decay=hp["wd"])
    opt.init(modele.trainable_parameters())
    etat = {"run": nom, "format": fmt, "positions": pos, "N": n, "graine": graine, "pas": 0,
            "calcul_s": 0.0, "invocations": 0, "params": nb_parametres(modele), "hp": hp}
    if os.path.exists(f_etat):
        etat = lire_json(f_etat)
        modele.load_weights(os.path.join(dossier, "poids.safetensors"))
        opt.state = tree_unflatten(list(mx.load(os.path.join(dossier, "opt.safetensors")).items()))
    mx.eval(modele.parameters(), opt.state)
    etat["invocations"] += 1

    loss_and_grad = nn.value_and_grad(modele, perte)
    st = [modele.state, opt.state]

    @partial(mx.compile, inputs=st, outputs=st)
    def pas_opt(x, y, m):
        l, g = loss_and_grad(modele, x, y, m)
        g, _ = optim.clip_grad_norm(g, hp["clip"])
        opt.update(modele, g)
        return l

    t0 = time.time()
    somme, k = 0.0, 0
    while etat["pas"] < hp["pas"] and time.time() - t0 < budget_s:
        x, y, m = (mx.array(v) for v in lot(graine, n, etat["pas"], fmt, BATCH))
        l = pas_opt(x, y, m)
        mx.eval(st)
        etat["pas"] += 1
        somme += l.item()
        k += 1
        if etat["pas"] % 250 == 0:
            log(f"{nom} pas {etat['pas']} perte {somme / k:.4f}")
            with open(os.path.join(dossier, "journal.csv"), "a") as fh:
                fh.write(f"{etat['pas']},{somme / k:.6f}\n")
            somme, k = 0.0, 0
    etat["calcul_s"] += time.time() - t0
    etat["fini"] = etat["pas"] >= hp["pas"]
    etat["uniques_vus"] = uniques_vus(n, etat["pas"])
    modele.save_weights(os.path.join(dossier, "poids.safetensors"))
    mx.save_safetensors(os.path.join(dossier, "opt.safetensors"), dict(tree_flatten(opt.state)))
    ecrire_json(etat, f_etat)
    return etat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", choices=["crible", "courbe", "graines"])
    ap.add_argument("--run", nargs=4, metavar=("FMT", "POS", "N", "GRAINE"))
    ap.add_argument("--conditions", nargs="*", default=[],
                    help="plan graines : conditions FMT-POS a porter aux graines 3, 4, 5")
    ap.add_argument("--budget-min", type=float, default=8.5)
    ap.add_argument("--hp", default="hyperparametres.json")
    args = ap.parse_args()
    if args.budget_min > 9:
        raise SystemExit("budget par invocation plafonne a 9 min (mandat)")
    hp = lire_json(os.path.join(ICI, args.hp))
    if args.run:
        f, p, n, g = args.run
        file = [(f, p, int(n), int(g))]
    elif args.plan == "graines":
        nmax = hp["pas"] * BATCH
        file = [(c.split("-")[0], c.split("-")[1], nmax, g) for g in (3, 4, 5)
                for c in args.conditions]
    else:
        file = plans(hp)[args.plan]
    t0 = time.time()
    for f, p, n, g in file:
        reste = args.budget_min * 60 - (time.time() - t0)
        if reste < 20:
            break
        etat = entrainer(f, p, n, g, hp, reste)
        if not etat.get("fini"):
            break
    faits = [nom_run(*r) for r in file
             if os.path.exists(os.path.join(ICI, "runs", nom_run(*r), "etat.json"))
             and lire_json(os.path.join(ICI, "runs", nom_run(*r), "etat.json")).get("fini")]
    print(json.dumps({"finis": len(faits), "total": len(file),
                      "invocation_s": round(time.time() - t0, 1)}))


if __name__ == "__main__":
    main()
