"""E016 -- entrainement REINFORCE de la population, avec reprise et budget par invocation.

  python entraine16.py --conds COLL IND COUPE --graines 1 2 3 4 5        # hyperparametres.json
  python entraine16.py --conds COLL --graines 0 --lr 0.2 --beta 0.01 --pas 4000 --tag pilote-...

S'arrete de lui-meme apres --budget-min minutes (defaut 8,5) en sauvegardant ; relancer la meme
commande reprend. Checkpoint = meilleur exact VAL-OOD moyen sur les 9 paires (egalite : le plus
tardif). PREREGISTREMENT.md section 3 : phase 1 (1 paire / tour) puis phase 2 (3 paires / tour).
"""
import argparse
import json
import os
import time

import mlx.core as mx
import mlx.optimizers as optim
import numpy as np
from mlx.utils import tree_flatten, tree_unflatten

import m16
from m16 import D, Population, echantillonne, perte_reinforce

ICI = os.path.dirname(os.path.abspath(__file__))
LOT_TOURS = 128
ESSAIS_MAX = 4
EVAL_TOUS = 250


def val_9(pop):
    """Exact VAL-OOD (6-8 chiffres) par paire (i, j) -> (moyenne, matrice)."""
    jeu = D.jeu_val()["VAL-OOD"]
    mat = np.zeros((pop.nA, pop.nB))
    for i in range(pop.nA):
        for j in range(pop.nB):
            f = pop.systeme(i, j)
            acc = []
            for L, paires in sorted(jeu.items()):
                acc.append(np.mean([r == str(a + b) for (a, b), (r, _) in zip(paires, f(paires))]))
            mat[i, j] = np.mean(acc)
    return float(mat.mean()), mat


def tours_du_pas(cond, graine, pas, pas_total, file_rejeu):
    """Renvoie la liste des tours : dict(p=[(a, b), ...], essai=k, paires=[(i, j), ...]), n_neufs."""
    phase = 1 if pas < pas_total // 2 else 2
    k = 1 if phase == 1 else 3
    tours = list(file_rejeu[:LOT_TOURS])
    neufs = [p for r in range(3) for p in D.paires_flux(graine, 3 * pas + r)]
    besoin = (LOT_TOURS - len(tours)) * k
    for q in range(0, besoin, k):
        tours.append({"p": [tuple(x) for x in neufs[q: q + k]], "essai": 1})
    rng = np.random.default_rng([17_000 + graine, pas])
    for t in tours:
        if phase == 1:
            t["paires"] = [(int(rng.integers(3)), int(rng.integers(3)))]
        else:
            perm = rng.permutation(3)
            t["paires"] = [(a, int(perm[a])) for a in range(3)]
    return tours, besoin, phase


def un_pas(pop, opt, cond, graine, pas, pas_total, file_rejeu, beta):
    tours, n_neufs, phase = tours_du_pas(cond, graine, pas, pas_total, file_rejeu)
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
    npas = np.array([D.n_pas(a, b) for a, b in probs])
    juste = np.array([D.decode(dig[q, :npas[q]]) == str(a + b) for q, (a, b) in enumerate(probs)])
    tour_de = np.array(tour_de)
    ok_tour = np.array([juste[tour_de == r].all() for r in range(len(tours))])
    rec = ok_tour[tour_de].astype(np.float32) if cond in ("COLL", "COUPE") else juste.astype(np.float32)
    base = np.zeros_like(rec)
    for L in np.unique(npas):
        base[npas == L] = rec[npas == L].mean()
    masque = (np.arange(D.T_TRAIN)[None, :] < npas[:, None]).astype(np.float32)
    lg = mx.value_and_grad(lambda t: perte_reinforce(t, act, rec - base, masque, beta))
    _, g = lg(pop.t)
    opt.update(pop.t, g)
    mx.eval(pop.t.parameters(), opt.state)
    nouvelle = []
    if cond in ("COLL", "COUPE"):
        for r, t in enumerate(tours):
            if not ok_tour[r] and t["essai"] < ESSAIS_MAX:
                nouvelle.append({"p": t["p"], "essai": t["essai"] + 1})
    return nouvelle, dict(pas=pas, phase=phase, tours=float(ok_tour.mean()), items=float(juste.mean()),
                          n_neufs=n_neufs, rejoues=len(tours) - n_neufs // (1 if phase == 1 else 3))


def _sauve(dossier, pop, opt, etat, meilleur=False):
    mx.save_safetensors(os.path.join(dossier, "poids.safetensors"), dict(tree_flatten(pop.t.parameters())))
    mx.save_safetensors(os.path.join(dossier, "opt.safetensors"), dict(tree_flatten(opt.state)))
    if meilleur:
        mx.save_safetensors(os.path.join(dossier, "meilleur.safetensors"),
                            dict(tree_flatten(pop.t.parameters())))
    json.dump(etat, open(os.path.join(dossier, "etat.json"), "w"))


def un_run(cond, graine, lr, beta, pas_total, dossier, t_fin):
    os.makedirs(dossier, exist_ok=True)
    f_etat = os.path.join(dossier, "etat.json")
    etat = json.load(open(f_etat)) if os.path.exists(f_etat) else None
    if etat and etat["fini"]:
        return True
    pop = Population(graine, coupe=(cond == "COUPE"))
    opt = optim.Adam(learning_rate=lr)
    opt.init(pop.t.parameters())
    if etat:
        pop.t.load_weights(os.path.join(dossier, "poids.safetensors"))
        st = mx.load(os.path.join(dossier, "opt.safetensors"))
        opt.state = tree_unflatten(list(st.items()))
    else:
        etat = dict(cond=cond, graine=graine, lr=lr, beta=beta, pas_total=pas_total, pas=0,
                    fini=False, rejeu=[], journal=[], val=[], meilleur=None)
    rejeu = [{"p": [tuple(x) for x in t["p"]], "essai": t["essai"]} for t in etat["rejeu"]]
    pas = etat["pas"]
    while pas < pas_total:
        if pas == pas_total // 2:
            rejeu = []  # changement de phase : la file de phase 1 est videe
        rejeu, log = un_pas(pop, opt, cond, graine, pas, pas_total, rejeu, beta)
        pas += 1
        etat["journal"].append([log["pas"], log["phase"], round(log["tours"], 4),
                                round(log["items"], 4), log["n_neufs"]])
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
            print(f"  {cond} s{graine} pas {pas}: tours {log['tours']:.3f} items {log['items']:.3f} "
                  f"VAL {v:.3f} C {pop.indice_commun()}/11 (meilleur {etat['meilleur']['val']:.3f} "
                  f"@ {etat['meilleur']['pas']})", flush=True)
            if time.time() > t_fin and pas < pas_total:
                print("  budget d'invocation atteint, reprise a la prochaine commande", flush=True)
                return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conds", nargs="+", required=True)
    ap.add_argument("--graines", nargs="+", type=int, required=True)
    ap.add_argument("--lr", type=float)
    ap.add_argument("--beta", type=float)
    ap.add_argument("--pas", type=int)
    ap.add_argument("--tag", default="")
    ap.add_argument("--budget-min", type=float, default=8.5)
    a = ap.parse_args()
    hp = json.load(open(os.path.join(ICI, "hyperparametres.json"))) if a.lr is None else {}
    t0 = time.time()
    t_fin = t0 + 60 * a.budget_min
    for cond in a.conds:
        for g in a.graines:
            lr = a.lr if a.lr is not None else hp["lr"]
            beta = a.beta if a.beta is not None else hp["beta"]
            pas = a.pas if a.pas is not None else hp["pas"]
            nom = f"{cond}-s{g}" + (f"-{a.tag}" if a.tag else "")
            print(f"== {nom} lr {lr} beta {beta} pas {pas}", flush=True)
            if not un_run(cond, g, lr, beta, pas, os.path.join(ICI, "runs", nom), t_fin):
                print(f"ARRET (budget) apres {time.time() - t0:.0f} s", flush=True)
                return
    print(f"TERMINE en {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
