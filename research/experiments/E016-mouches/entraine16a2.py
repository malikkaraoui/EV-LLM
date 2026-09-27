"""E016-A2 -- la recompense comme seule variable (PREREGISTREMENT.md, amendement A2).

  python entraine16a2.py --conds IND --recomp dense --graines 0 --tag pilote-dense      # A2.1
  python entraine16a2.py --conds IND --recomp 01 --curric --graines 0 --tag pilote-curric
  python entraine16a2.py --conds FIXE IND TOR COLL --recomp dense --graines 1 2 3 4 5      # A2.2

Code M0031 importe, non modifie (m16, entraine16). Differences, et seulement elles :
  - recomp "dense" : credit d'un item = fraction des colonnes justes (chiffre emis par B_j a la
    colonne t = chiffre t de a+b, poids faible d'abord, t < n_pas) ; "01" = addition exacte (M0031) ;
  - conditions : FIXE (A_k<->B_k), IND (par paire), TOR (min sur le tour, sans rejeu),
    COLL (min sur le tour + rejeu), REJEU (par paire + rejeu) ; rejeu d'un tour <=> pas tous exacts ;
  - --curric : operandes a 1 chiffre pendant les 1 000 premiers pas (variante de repli A2.1).
Reprise sur checkpoint et budget par invocation comme entraine16.
"""
import argparse
import json
import os
import time

import mlx.core as mx
import mlx.optimizers as optim
import numpy as np
from mlx.utils import tree_unflatten

import m16
from entraine16 import ESSAIS_MAX, EVAL_TOUS, LOT_TOURS, _sauve, val_9
from m16 import D, Population, echantillonne, perte_reinforce

ICI = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(ICI, "runs", "a2")
CONDS = ("FIXE", "IND", "TOR", "COLL", "REJEU")
MIN_TOUR = ("TOR", "COLL")
AVEC_REJEU = ("COLL", "REJEU")
PAS_CURRIC = 1000


def neufs_du_pas(graine, pas, curric):
    """Problemes neufs du pas : flux M0031 (k = 3 pas + r), ou 1 chiffre en debut de curriculum."""
    if curric and pas < PAS_CURRIC:
        rng = np.random.default_rng([18_000 + graine, pas])
        x = rng.integers(0, 10, size=(3 * D.LOT, 2))
        return [(int(a), int(b)) for a, b in x]
    return [p for r in range(3) for p in D.paires_flux(graine, 3 * pas + r)]


def tours_du_pas(cond, graine, pas, pas_total, file_rejeu, curric=False):
    """Comme entraine16.tours_du_pas (meme rng de partenaires) ; FIXE garde i = j."""
    phase = 1 if pas < pas_total // 2 else 2
    k = 1 if phase == 1 else 3
    tours = list(file_rejeu[:LOT_TOURS])
    neufs = neufs_du_pas(graine, pas, curric)
    besoin = (LOT_TOURS - len(tours)) * k
    for q in range(0, besoin, k):
        tours.append({"p": [tuple(x) for x in neufs[q: q + k]], "essai": 1})
    rng = np.random.default_rng([17_000 + graine, pas])
    for t in tours:
        if phase == 1:
            i, j = int(rng.integers(3)), int(rng.integers(3))
            t["paires"] = [(i, i)] if cond == "FIXE" else [(i, j)]
        else:
            perm = rng.permutation(3)
            t["paires"] = [(a, a) for a in range(3)] if cond == "FIXE" else [(a, int(perm[a])) for a in range(3)]
    return tours, besoin, phase


def credit(probs, dig, recomp):
    """Credit par item : exact (0/1) et fraction des colonnes justes."""
    npas = np.array([D.n_pas(a, b) for a, b in probs])
    juste = np.array([D.decode(dig[q, :npas[q]]) == str(a + b) for q, (a, b) in enumerate(probs)])
    _, _, Y, M = D.encode_aligne(probs, dig.shape[1])
    col = ((dig == Y) * M).sum(1) / M.sum(1)
    return juste, (col if recomp == "dense" else juste.astype(np.float64)), npas


def un_pas(pop, opt, cond, recomp, graine, pas, pas_total, file_rejeu, tours=None, geles=None,
           curric=False):
    """Un pas de REINFORCE. `tours` fourni : on n'utilise pas tours_du_pas (nouveaux venus).
    `geles` : fonction qui annule le gradient des tables gelees."""
    if tours is None:
        tours, n_neufs, phase = tours_du_pas(cond, graine, pas, pas_total, file_rejeu, curric)
    else:
        n_neufs, phase = len(tours), 1
    items, probs, tour_de = [], [], []
    for r, t in enumerate(tours):
        for p, ij in zip(t["p"], t["paires"]):
            items.append(ij)
            probs.append(p)
            tour_de.append(r)
    n = len(items)
    cl = np.zeros((n, D.T_TRAIN, 2), np.int32)
    I = np.array([it[0] for it in items])
    for i in range(pop.nA):
        q = np.where(I == i)[0]
        if len(q):
            cl[q] = m16.lit(pop.lecteurs[i], [probs[x] for x in q], D.T_TRAIN)
    act, dig = echantillonne(pop, items, cl, mx.random.key(graine * 1_000_003 + pas))
    juste, c, npas = credit(probs, dig, recomp)
    tour_de = np.array(tour_de)
    ok_tour = np.array([juste[tour_de == r].all() for r in range(len(tours))])
    if cond in MIN_TOUR:
        mins = np.array([c[tour_de == r].min() for r in range(len(tours))])
        rec = mins[tour_de].astype(np.float32)
    else:
        rec = c.astype(np.float32)
    base = np.zeros_like(rec)
    for L in np.unique(npas):
        base[npas == L] = rec[npas == L].mean()
    masque = (np.arange(D.T_TRAIN)[None, :] < npas[:, None]).astype(np.float32)
    lg = mx.value_and_grad(lambda t: perte_reinforce(t, act, rec - base, masque, 0.0))
    _, g = lg(pop.t)
    if geles is not None:
        g = geles(g)
    opt.update(pop.t, g)
    mx.eval(pop.t.parameters(), opt.state)
    nouvelle = []
    if cond in AVEC_REJEU:
        for r, t in enumerate(tours):
            if not ok_tour[r] and t["essai"] < ESSAIS_MAX:
                nouvelle.append({"p": t["p"], "essai": t["essai"] + 1})
    return nouvelle, dict(pas=pas, phase=phase, tours=float(ok_tour.mean()), items=float(juste.mean()),
                          credit=float(c.mean()), n_neufs=n_neufs)


def un_run(cond, recomp, curric, graine, lr, pas_total, dossier, t_fin):
    os.makedirs(dossier, exist_ok=True)
    f_etat = os.path.join(dossier, "etat.json")
    etat = json.load(open(f_etat)) if os.path.exists(f_etat) else None
    if etat and etat["fini"]:
        return True
    pop = Population(graine)
    opt = optim.Adam(learning_rate=lr)
    opt.init(pop.t.parameters())
    if etat:
        pop.t.load_weights(os.path.join(dossier, "poids.safetensors"))
        st = mx.load(os.path.join(dossier, "opt.safetensors"))
        opt.state = tree_unflatten(list(st.items()))
    else:
        etat = dict(cond=cond, recomp=recomp, curric=curric, graine=graine, lr=lr, beta=0.0,
                    pas_total=pas_total, pas=0, fini=False, rejeu=[], journal=[], val=[], meilleur=None)
    rejeu = [{"p": [tuple(x) for x in t["p"]], "essai": t["essai"]} for t in etat["rejeu"]]
    pas = etat["pas"]
    while pas < pas_total:
        if pas == pas_total // 2 or (curric and pas == PAS_CURRIC):
            rejeu = []  # changement de phase (ou de distribution) : file videe
        rejeu, log = un_pas(pop, opt, cond, recomp, graine, pas, pas_total, rejeu, curric=curric)
        pas += 1
        etat["journal"].append([log["pas"], log["phase"], round(log["tours"], 4),
                                round(log["items"], 4), log["n_neufs"], round(log["credit"], 4)])
        if pas % EVAL_TOUS == 0 or pas == pas_total:
            v, mat = val_9(pop)
            lex, _ = pop.lexique()
            etat["val"].append(dict(pas=pas, val=v, mat=mat.round(4).tolist(),
                                    C=pop.indice_commun(), lex=lex))
            meilleur = etat["meilleur"] is None or v >= etat["meilleur"]["val"]
            if meilleur:
                etat["meilleur"] = dict(pas=pas, val=v)
            etat.update(pas=pas, rejeu=rejeu, fini=pas >= pas_total)
            _sauve(dossier, pop, opt, etat, meilleur)
            print(f"  {cond}/{recomp} s{graine} pas {pas}: tours {log['tours']:.3f} items {log['items']:.3f} "
                  f"credit {log['credit']:.3f} VAL {v:.3f} paires>=0.9 {int((mat >= 0.9).sum())}/9 "
                  f"C {pop.indice_commun()}/11", flush=True)
            if time.time() > t_fin and pas < pas_total:
                print("  budget d'invocation atteint, reprise a la prochaine commande", flush=True)
                return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conds", nargs="+", required=True, choices=CONDS)
    ap.add_argument("--recomp", required=True, choices=("dense", "01"))
    ap.add_argument("--curric", action="store_true")
    ap.add_argument("--graines", nargs="+", type=int, required=True)
    ap.add_argument("--tag", default="")
    ap.add_argument("--budget-min", type=float, default=8.5)
    a = ap.parse_args()
    hp = json.load(open(os.path.join(ICI, "hyperparametres.json")))
    t0 = time.time()
    t_fin = t0 + 60 * a.budget_min
    for cond in a.conds:
        for g in a.graines:
            nom = f"{cond}-{a.recomp}{'-curric' if a.curric else ''}-s{g}" + (f"-{a.tag}" if a.tag else "")
            print(f"== {nom} lr {hp['lr']} beta 0 pas {hp['pas']}", flush=True)
            if not un_run(cond, a.recomp, a.curric, g, hp["lr"], hp["pas"], os.path.join(RUNS, nom), t_fin):
                print(f"ARRET (budget) apres {time.time() - t0:.0f} s", flush=True)
                return
    print(f"TERMINE en {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
