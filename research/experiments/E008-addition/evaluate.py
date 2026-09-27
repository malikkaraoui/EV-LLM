"""E008 -- evaluateur UNIQUE pour les 4 systemes (C-ORACLE, C-PARCOEUR, B-STD, B-REF).

Un systeme = fonction (liste de (a, b)) -> liste de (reponse canonique | None, confiance).
La reference est `a + b` de Python ; la comparaison est l'egalite exacte des chaines.

Usage :
  python evaluate.py --systeme B-STD --graine 1      # checkpoint final de runs/B-STD-s1
"""
import argparse
import json
import os
import time
from collections import defaultdict

import numpy as np

from data import (CARS, FIN, PAD, chaine_retenue, ecrire_json, encode_prompt, jeux_de_test,
                  lire_json)

ICI = os.path.dirname(os.path.abspath(__file__))
SEUIL_SUR = 0.8


# ---------------------------------------------------------------- evaluateur
def evaluer(systeme, jeux, nom_systeme):
    """Renvoie la liste des enregistrements item par item."""
    recs = []
    for jeu, par_l in jeux.items():
        for L, paires in sorted(par_l.items()):
            preds = systeme(paires)
            assert len(preds) == len(paires)
            for (a, b), (rep, conf) in zip(paires, preds):
                attendu = str(a + b)
                recs.append({
                    "systeme": nom_systeme, "jeu": jeu, "L": L, "a": a, "b": b,
                    "attendu": attendu, "rep": rep, "juste": rep == attendu,
                    "conf": float(conf), "chaine": chaine_retenue(a, b),
                })
    return recs


def resume(recs):
    """Agregats par jeu x L et par longueur de chaine (T-ID1 exclu de la vue par chaine)."""
    par_jeu = defaultdict(lambda: {"n": 0, "justes": 0, "faux": 0, "faux_surs": 0})
    par_chaine = defaultdict(lambda: {"n": 0, "justes": 0})
    for r in recs:
        k = f"{r['jeu']}|{r['L']}"
        c = par_jeu[k]
        c["n"] += 1
        if r["juste"]:
            c["justes"] += 1
        else:
            c["faux"] += 1
            if r["conf"] >= SEUIL_SUR:
                c["faux_surs"] += 1
        if r["jeu"] != "T-ID1":
            pc = par_chaine[str(r["chaine"])]
            pc["n"] += 1
            pc["justes"] += int(r["juste"])
    for c in par_jeu.values():
        c["exact"] = c["justes"] / c["n"]
    for c in par_chaine.values():
        c["exact"] = c["justes"] / c["n"]
    return {"par_jeu": dict(par_jeu),
            "par_chaine": dict(sorted(par_chaine.items(), key=lambda kv: int(kv[0])))}


# ---------------------------------------------------------------- systeme appris
def systeme_modele(modele, inverse, taille_lot=500):
    """Decodage glouton ; confiance = produit des probabilites des tokens generes."""
    import mlx.core as mx

    def predire(paires):
        out = [None] * len(paires)
        groupes = defaultdict(list)
        for i, (a, b) in enumerate(paires):
            groupes[len(encode_prompt(a, b))].append(i)
        for _, idx in sorted(groupes.items()):
            for k in range(0, len(idx), taille_lot):
                sous = idx[k: k + taille_lot]
                prompts = np.array([encode_prompt(*paires[i]) for i in sous], dtype=np.int32)
                lmax = max(max(len(str(a)), len(str(b))) for a, b in (paires[i] for i in sous))
                n_gen = lmax + 2
                x = mx.array(prompts)
                conf = np.ones(len(sous))
                fini = np.zeros(len(sous), dtype=bool)
                gen = np.full((len(sous), n_gen), PAD, dtype=np.int32)
                for t in range(n_gen):
                    logits = modele(x)[:, -1, :]
                    p = mx.softmax(logits.astype(mx.float32), axis=-1)
                    tok = mx.argmax(p, axis=-1)
                    p_tok = mx.take_along_axis(p, tok[:, None], axis=-1)[:, 0]
                    tok_np, p_np = np.array(tok), np.array(p_tok)
                    actif = ~fini
                    conf[actif] *= p_np[actif]
                    gen[actif, t] = tok_np[actif]
                    fini |= tok_np == FIN
                    x = mx.concatenate([x, tok[:, None].astype(mx.int32)], axis=1)
                    if fini.all():
                        break
                for j, i in enumerate(sous):
                    toks = list(gen[j])
                    if FIN not in toks:
                        out[i] = (None, float(conf[j]))
                        continue
                    s = "".join(CARS[t] for t in toks[: toks.index(FIN)])
                    out[i] = ((s[::-1] if inverse else s), float(conf[j]))
        return out

    return predire


def charge_modele(systeme, dossier):
    import mlx.core as mx
    from model import Additionneur
    m = Additionneur(positions=(systeme == "B-STD"))
    m.load_weights(os.path.join(dossier, "poids.safetensors"))
    mx.eval(m.parameters())
    m.eval()
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--systeme", required=True, choices=["B-STD", "B-REF"])
    ap.add_argument("--graine", type=int, required=True)
    args = ap.parse_args()
    dossier = os.path.join(ICI, "runs", f"{args.systeme}-s{args.graine}")
    etat = lire_json(os.path.join(dossier, "etat.json"))
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    if etat["pas"] < hp["pas"]:
        raise SystemExit(f"entrainement inacheve : {etat['pas']}/{hp['pas']}")
    t0 = time.time()
    m = charge_modele(args.systeme, dossier)
    recs = evaluer(systeme_modele(m, inverse=(args.systeme == "B-REF")), jeux_de_test(),
                   args.systeme)
    with open(os.path.join(dossier, "eval.jsonl"), "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    res = resume(recs)
    res.update({"systeme": args.systeme, "graine": args.graine, "pas": etat["pas"],
                "duree_eval_s": round(time.time() - t0, 1)})
    ecrire_json(res, os.path.join(dossier, "resume.json"))
    print(f"{args.systeme} s{args.graine} : evaluation en {res['duree_eval_s']} s")


if __name__ == "__main__":
    main()
