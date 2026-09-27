"""E009 -- entrainement A1 / A2 / A2-L / A3 / A3-T avec reprise sur checkpoint.

Chaque invocation s'arrete d'elle-meme apres --budget-min minutes (defaut 8.5, plafond 9)
et sauvegarde ; relancer la meme commande reprend au pas suivant. Au premier plan.

  python entraine.py --systeme A2 --graine 1 [--fmt inv|std]
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

from archis import M_ENTRAINEMENT, SYSTEMES, nb_parametres
from bande import d8, ecrire_json, lire_json, lot, sous_val
from boucle import perte_bande, perte_progressive, perte_tn, tirage_progressif
from evalue import nom_run, systeme_appris
from model import lr_schedule  # E008

ICI = os.path.dirname(os.path.abspath(__file__))


def jalons(pas_total):
    return [pas_total * i // 8 for i in range(1, 9)]


def entrainer(systeme, graine, fmt, dossier, hp, budget_s, log=print, avec_jalons=True,
              arret_pas=None):
    os.makedirs(dossier, exist_ok=True)
    inverse = fmt == "inv"
    regle = SYSTEMES[systeme]["regle"]
    f_etat = os.path.join(dossier, "etat.json")

    mx.random.seed(graine)
    modele = SYSTEMES[systeme]["fabrique"]()
    sched = lr_schedule(hp["lr_max"], hp["montee"], hp["pas"], hp["lr_min"])
    opt = optim.AdamW(learning_rate=sched, betas=hp["betas"], weight_decay=hp["wd"])
    opt.init(modele.trainable_parameters())

    etat = {"pas": 0, "calcul_s": 0.0, "invocations": 0, "params": nb_parametres(modele),
            "systeme": systeme, "graine": graine, "fmt": fmt, "pas_total": hp["pas"]}
    if os.path.exists(f_etat):
        etat = lire_json(f_etat)
        modele.load_weights(os.path.join(dossier, "poids.safetensors"))
        opt.state = tree_unflatten(list(mx.load(os.path.join(dossier, "opt.safetensors")).items()))
    mx.eval(modele.parameters(), opt.state)
    etat["invocations"] += 1

    ex = d8.paires_exclues()
    fn = {"bande": perte_bande, "confiance": perte_progressive, "t_n": perte_tn}[regle]
    loss_and_grad = nn.value_and_grad(modele, fn)
    st = [modele.state, opt.state]

    def pas_eager(x, y, m, *extra):
        l, g = loss_and_grad(modele, x, y, m, *extra)
        g, _ = optim.clip_grad_norm(g, hp["clip"])
        opt.update(modele, g)
        return l

    # recompile si (n, k) / t_max / forme changent. Exception : n + k == M (chaine progressive
    # identique a la chaine principale) fait planter mx.compile 0.29.3 sur A3 -> pas non compile.
    pas_compile = partial(mx.compile, inputs=st, outputs=st)(pas_eager)
    js = jalons(hp["pas"]) if avec_jalons else []
    jeux_j = sous_val(100) if avec_jalons else None

    t0 = time.time()
    somme, n = 0.0, 0
    fin = hp["pas"] if arret_pas is None else min(hp["pas"], arret_pas)  # arret_pas : tests
    while etat["pas"] < fin and time.time() - t0 < budget_s:
        xn, yn, mn, tn = lot(graine, etat["pas"], ex, inverse, hp["lot"])
        if regle == "confiance":
            extra = tirage_progressif(graine, etat["pas"])
        elif regle == "t_n":
            extra = (mx.array(tn), int(tn.max()))
        else:
            extra = ()
        pas_opt = pas_eager if regle == "confiance" and sum(extra) == M_ENTRAINEMENT else pas_compile
        l = pas_opt(mx.array(xn), mx.array(yn), mx.array(mn), *extra)
        mx.eval(st, l)
        etat["pas"] += 1
        lv = l.item()
        if lv != lv:  # NaN : arret net, pas de sauvegarde des poids corrompus
            etat["nan_au_pas"] = etat["pas"]
            ecrire_json(etat, f_etat)
            raise SystemExit(f"perte NaN au pas {etat['pas']}")
        somme += lv
        n += 1
        if etat["pas"] % 250 == 0:
            log(f"{systeme} {fmt} s{graine} pas {etat['pas']} perte {somme / n:.4f} "
                f"({time.time() - t0:.0f} s)")
            with open(os.path.join(dossier, "journal.csv"), "a") as f:
                f.write(f"{etat['pas']},{somme / n:.6f}\n")
            somme, n = 0.0, 0
        if etat["pas"] in js:
            jalon(modele, regle, inverse, jeux_j, etat, hp["lot"], dossier)
    etat["calcul_s"] += time.time() - t0
    etat["fini"] = etat["pas"] >= hp["pas"]
    modele.save_weights(os.path.join(dossier, "poids.safetensors"))
    mx.save_safetensors(os.path.join(dossier, "opt.safetensors"), dict(tree_flatten(opt.state)))
    ecrire_json(etat, f_etat)
    return etat


def jalon(modele, regle, inverse, jeux_j, etat, taille_lot, dossier):
    """VAL (100 / L) ; garde le checkpoint de meilleure moyenne (egalite : le plus tardif)."""
    from evaluate import evaluer, resume  # E008
    t0 = time.time()
    modele.eval()
    r = resume(evaluer(systeme_appris(modele, regle, inverse), jeux_j, "jalon"))["par_jeu"]
    modele.train()
    moy = sum(c["exact"] for c in r.values()) / len(r)
    f = os.path.join(dossier, "courbe.csv")
    neuf = not os.path.exists(f)
    with open(f, "a", newline="") as fh:
        w = csv.writer(fh)
        if neuf:
            w.writerow(["pas", "exemples_vus", "jeu", "L", "exact"])
        for k, c in sorted(r.items()):
            jeu, L = k.split("|")
            w.writerow([etat["pas"], etat["pas"] * taille_lot, jeu, L, f"{c['exact']:.4f}"])
    if moy >= etat.get("meilleur", {}).get("val", -1.0):
        modele.save_weights(os.path.join(dossier, "meilleur.safetensors"))
        etat["meilleur"] = {"pas": etat["pas"], "val": moy}
    etat.setdefault("jalons_s", []).append(round(time.time() - t0, 1))
    print(f"  jalon {etat['pas']} : VAL moy {moy:.3f} "
          + " ".join(f"{k}={c['exact']:.2f}" for k, c in sorted(r.items()))
          + f" ({time.time() - t0:.0f} s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systeme", required=True, choices=list(SYSTEMES))
    ap.add_argument("--graine", type=int, required=True)
    ap.add_argument("--fmt", default="inv", choices=["inv", "std"])
    ap.add_argument("--budget-min", type=float, default=8.5)
    ap.add_argument("--pas", type=int, default=None, help="pilote uniquement (graine 0)")
    args = ap.parse_args()
    if args.budget_min > 9:
        raise SystemExit("budget par invocation plafonne a 9 min (mandat)")
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    if args.pas is not None:
        if args.graine != 0:
            raise SystemExit("--pas reserve au pilote (graine 0)")
        hp["pas"] = args.pas
    dossier = os.path.join(ICI, "runs", nom_run(args.systeme, args.graine, args.fmt))
    etat = entrainer(args.systeme, args.graine, args.fmt, dossier, hp, args.budget_min * 60)
    print(json.dumps(etat))


if __name__ == "__main__":
    main()
