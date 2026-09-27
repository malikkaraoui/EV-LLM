"""E009-bis -- entrainement adaptatif : curriculum 2->5, arret a T-ID >= 95 %, plafond de pas.

Chaque invocation s'arrete d'elle-meme apres --budget-min minutes (defaut 8, plafond 9) et
sauvegarde ; relancer la meme commande reprend au pas suivant (niveau de curriculum compris).

  python entraine_bis.py --systeme A1 --graine 1                       # officiel (hp figes)
  python entraine_bis.py --systeme A1 --graine 0 --w 128 --lr 3e-4     # pilote (graine 0)
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

import curric as C
from archis import M_ENTRAINEMENT, nb_parametres  # E009
from bande import ecrire_json, lire_json  # E009
from boucle import perte_bande, perte_progressive, perte_tn, tirage_progressif  # E009
from model import lr_schedule  # E008

ICI = os.path.dirname(os.path.abspath(__file__))
PAS_PILOTE = 1000  # amendement B0


def nom_run(systeme, graine, w=None, lr=None):
    if graine == 0:
        return f"pilote-{systeme}-w{w}-lr{lr:g}"
    return f"{systeme}-s{graine}"


def controle_curriculum(modele, systeme, etat):
    """Tous les 500 pas (si niveau < 5) : T-ID courant (2..niveau, 100 / L) >= 90 % -> niveau + 1."""
    niv = etat["niveau"]
    r = C.mesure(modele, systeme, C.t_id(range(2, niv + 1), C.N_CURR))
    moy = sum(r.values()) / len(r)
    etat.setdefault("controles_curr", []).append([etat["pas"], niv, round(moy, 4)])
    if moy >= C.SEUIL_CURR:
        etat["niveau"] = niv + 1
        etat.setdefault("transitions", []).append([etat["pas"], niv + 1])
    print(f"  curriculum pas {etat['pas']} : niveau {niv}, T-ID courant {moy:.3f} "
          f"-> niveau {etat['niveau']}")


def controle_arret(modele, systeme, etat, dossier):
    """Tous les 1 000 pas si niveau = 5 : T-ID complet (200 / L) ; moyenne >= 95 % -> arret."""
    r = C.mesure(modele, systeme, C.t_id(range(2, 6), C.N_ARRET))
    moy = sum(r.values()) / len(r)
    etat.setdefault("controles_arret", []).append(
        [etat["pas"], round(moy, 4), {k: round(v, 4) for k, v in r.items()}])
    print(f"  arret pas {etat['pas']} : T-ID 2-5 moy {moy:.3f} "
          + " ".join(f"{k}={v:.2f}" for k, v in sorted(r.items())))
    if moy >= C.SEUIL_ARRET:
        modele.save_weights(os.path.join(dossier, "meilleur.safetensors"))
        etat["appris"] = True
        etat["pas_appris"] = etat["pas"]
        etat["t_id_appris"] = {k: v for k, v in r.items()}
        return True
    return False


def entrainer(systeme, graine, w, lr, dossier, hp, budget_s, pas_max, log=print,
              avec_controles=True):
    os.makedirs(dossier, exist_ok=True)
    regle = C.regle(systeme)
    f_etat = os.path.join(dossier, "etat.json")

    mx.random.seed(graine)
    modele = C.fabrique(systeme, w)
    sched = lr_schedule(lr, hp["montee"], hp["plafond_pas"], hp["lr_min"])
    opt = optim.AdamW(learning_rate=sched, betas=hp["betas"], weight_decay=hp["wd"])
    opt.init(modele.trainable_parameters())

    etat = {"pas": 0, "calcul_s": 0.0, "invocations": 0, "params": nb_parametres(modele),
            "systeme": systeme, "graine": graine, "w": w, "lr": lr, "pas_max": pas_max,
            "plafond_pas": hp["plafond_pas"], "niveau": C.L_DEPART, "transitions": [],
            "appris": False, "fini": False}
    if os.path.exists(f_etat):
        etat = lire_json(f_etat)
        modele.load_weights(os.path.join(dossier, "poids.safetensors"))
        opt.state = tree_unflatten(list(mx.load(os.path.join(dossier, "opt.safetensors")).items()))
    if etat["fini"]:
        return etat
    mx.eval(modele.parameters(), opt.state)
    etat["invocations"] += 1

    ex = C.d8.paires_exclues()
    fn = {"bande": perte_bande, "confiance": perte_progressive, "t_n": perte_tn}[regle]
    loss_and_grad = nn.value_and_grad(modele, fn)
    st = [modele.state, opt.state]

    def pas_eager(x, y, m, *extra):
        l, g = loss_and_grad(modele, x, y, m, *extra)
        g, _ = optim.clip_grad_norm(g, hp["clip"])
        opt.update(modele, g)
        return l

    # E009 : n + k == M fait planter mx.compile 0.29.3 (A3) -> ces pas sont executes sans compiler
    pas_compile = partial(mx.compile, inputs=st, outputs=st)(pas_eager)

    t0 = time.time()
    somme, n = 0.0, 0
    while etat["pas"] < pas_max and time.time() - t0 < budget_s:
        xn, yn, mn, tn = C.lot(graine, etat["pas"], ex, etat["niveau"], True, hp["lot"])
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
        if lv != lv:  # NaN : arret net, poids corrompus non sauvegardes
            etat["nan_au_pas"] = etat["pas"]
            etat["fini"] = True
            ecrire_json(etat, f_etat)
            raise SystemExit(f"perte NaN au pas {etat['pas']}")
        somme += lv
        n += 1
        if etat["pas"] % 250 == 0:
            log(f"{systeme} s{graine} w{w} pas {etat['pas']} niveau {etat['niveau']} "
                f"perte {somme / n:.4f} ({time.time() - t0:.0f} s)")
            with open(os.path.join(dossier, "journal.csv"), "a") as f:
                f.write(f"{etat['pas']},{etat['niveau']},{somme / n:.6f}\n")
            somme, n = 0.0, 0
        if not avec_controles:
            continue
        if etat["pas"] % C.PERIODE_CURR == 0 and etat["niveau"] < C.L_FIN:
            controle_curriculum(modele, systeme, etat)
        if (etat["pas"] % C.PERIODE_ARRET == 0 and etat["niveau"] == C.L_FIN
                and controle_arret(modele, systeme, etat, dossier)):
            break
    etat["calcul_s"] += time.time() - t0
    etat["fini"] = etat["appris"] or etat["pas"] >= pas_max
    modele.save_weights(os.path.join(dossier, "poids.safetensors"))
    mx.save_safetensors(os.path.join(dossier, "opt.safetensors"), dict(tree_flatten(opt.state)))
    ecrire_json(etat, f_etat)
    return etat


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systeme", required=True, choices=["A1", "A2-L", "A3", "A3-T"])
    ap.add_argument("--graine", type=int, required=True)
    ap.add_argument("--budget-min", type=float, default=8.0)
    ap.add_argument("--w", type=int, default=None, help="pilote uniquement (graine 0)")
    ap.add_argument("--lr", type=float, default=None, help="pilote uniquement (graine 0)")
    args = ap.parse_args()
    if args.budget_min > 9:
        raise SystemExit("budget par invocation plafonne a 9 min (mandat)")
    hp = lire_json(os.path.join(ICI, "hyperparametres_bis.json"))
    if args.graine == 0:
        if args.w is None or args.lr is None:
            raise SystemExit("pilote : --w et --lr requis")
        w, lr, pas_max = args.w, args.lr, PAS_PILOTE
    else:
        if args.w is not None or args.lr is not None:
            raise SystemExit("--w / --lr reserves au pilote (graine 0)")
        fige = hp["systemes"].get(args.systeme)
        if fige is None:
            raise SystemExit("hyperparametres non figes (amendement B1 absent)")
        w, lr, pas_max = fige["w"], fige["lr"], hp["plafond_pas"]
    dossier = os.path.join(ICI, "runs", nom_run(args.systeme, args.graine, w, lr))
    etat = entrainer(args.systeme, args.graine, w, lr, dossier, hp, args.budget_min * 60, pas_max)
    print(json.dumps({k: v for k, v in etat.items() if not k.startswith("controles")}))


if __name__ == "__main__":
    main()
