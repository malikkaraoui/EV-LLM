"""E010 -- systeme appris pour l'evaluateur UNIQUE d'E008 (evaluate.evaluer / resume).

Decodage glouton avec cache ; confiance = produit des probabilites des tokens de la reponse
finale et de la fin (PREREGISTREMENT section 5). Diagnostics F1/F3 dans `diag`.

  python evaluation.py --run F1-nope-N384000-s1            # criblage (T-ID 200/L, V-OOD 200/L)
  python evaluation.py --run F1-nope-N384000-s1 --final    # test final, une seule fois
"""
import argparse
import json
import os
import time
from collections import defaultdict

import numpy as np

from donnees import (FIN, cible, ecrire_json, encode_prompt, jeux_e010, lire_json, lit_sortie,
                     n_gen_max)
from evaluate import evaluer, resume  # E008 : evaluateur unique

ICI = os.path.dirname(os.path.abspath(__file__))


def systeme_modele(modele, fmt, diag=None, taille_lot=250):
    import mlx.core as mx
    from modele import Cache

    def predire(paires):
        out = [None] * len(paires)
        groupes = defaultdict(list)
        for i, (a, b) in enumerate(paires):
            groupes[len(encode_prompt(a, b, fmt))].append(i)
        for _, idx in sorted(groupes.items()):
            for k0 in range(0, len(idx), taille_lot):
                sous = idx[k0: k0 + taille_lot]
                x = mx.array(np.array([encode_prompt(*paires[i], fmt) for i in sous], np.int32))
                n_gen = max(n_gen_max(len(str(paires[i][0])), len(str(paires[i][1])), fmt)
                            for i in sous)
                caches = [Cache() for _ in modele.blocs]
                vu = 0
                fini = np.zeros(len(sous), bool)
                gen = np.full((len(sous), n_gen), -1, np.int32)
                prob = np.ones((len(sous), n_gen))
                for t in range(n_gen):
                    logits = modele(x, caches, vu)[:, -1, :]
                    vu += x.shape[1]
                    p = mx.softmax(logits.astype(mx.float32), axis=-1)
                    tok = mx.argmax(p, axis=-1)
                    p_tok = mx.take_along_axis(p, tok[:, None], axis=-1)[:, 0]
                    tok_np, p_np = np.array(tok), np.array(p_tok)
                    actif = ~fini
                    gen[actif, t] = tok_np[actif]
                    prob[actif, t] = p_np[actif]
                    fini |= tok_np == FIN
                    if fini.all():
                        break
                    x = tok[:, None].astype(mx.int32)
                for j, i in enumerate(sous):
                    toks = [int(v) for v in gen[j] if v >= 0]
                    rep, debut = lit_sortie(toks, fmt)
                    if rep is None:
                        conf = 0.0
                    else:
                        conf = float(np.prod(prob[j, debut: toks.index(FIN) + 1]))
                    out[i] = (rep, conf)
                    if diag is not None and fmt in ("F1", "F3"):
                        a, b = paires[i]
                        vrai = cible(a, b, fmt)
                        n_tr = len(vrai) - len(str(a + b)) - 2  # longueur de la trace
                        tr = toks[: toks.index(15)] if 15 in toks else toks
                        diag[(a, b)] = {"trace_juste": tr == vrai[:n_tr],
                                        "coherent": _coherent(tr, rep, fmt)}
        return out

    return predire


def _coherent(tr, rep, fmt):
    """La reponse recopie-t-elle son propre brouillon (chiffres ecrits + retenue finale) ?"""
    if rep is None or len(tr) % 6 or not tr:
        return False
    cols = [tr[k: k + 6] for k in range(0, len(tr), 6)]
    ch = [c[3] for c in cols]
    if cols[-1][4] == 1:
        ch.append(1)
    return "".join(str(c) for c in reversed(ch)) == rep


def charge_modele(dossier, positions):
    import mlx.core as mx
    from modele import Additionneur
    m = Additionneur(positions=positions)
    m.load_weights(os.path.join(dossier, "poids.safetensors"))
    mx.eval(m.parameters())
    m.eval()
    return m


def evaluer_run(nom, final=False):
    dossier = os.path.join(ICI, "runs", nom)
    etat = lire_json(os.path.join(dossier, "etat.json"))
    if not etat.get("fini"):
        raise SystemExit(f"{nom} : entrainement inacheve ({etat['pas']} pas)")
    sortie = os.path.join(dossier, "final.json" if final else "crible.json")
    if final and os.path.exists(sortie):
        raise SystemExit(f"{nom} : test final deja evalue (une seule fois)")
    fmt, pos = etat["format"], etat["positions"]
    t0 = time.time()
    m = charge_modele(dossier, positions=(pos == "abs"))
    diag = {}
    jeux = jeux_e010(n_id=500 if final else 200, final=final)
    recs = evaluer(systeme_modele(m, fmt, diag), jeux, nom)
    for r in recs:
        d = diag.get((r["a"], r["b"]))
        if d:
            r.update(d)
    with open(os.path.join(dossier, ("final" if final else "crible") + ".jsonl"), "w") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    res = resume(recs)
    abst = defaultdict(lambda: [0, 0, 0, 0])  # [faux, abstentions, traces justes, coherents]
    for r in recs:
        k = f"{r['jeu']}|{r['L']}"
        abst[k][0] += not r["juste"]
        abst[k][1] += r["rep"] is None
        abst[k][2] += bool(r.get("trace_juste"))
        abst[k][3] += bool(r.get("coherent"))
    for k, c in res["par_jeu"].items():
        c["abstentions"], c["traces_justes"], c["coherents"] = abst[k][1], abst[k][2], abst[k][3]
    res.update({"run": nom, "format": fmt, "positions": pos, "graine": etat["graine"],
                "N": etat["N"], "pas": etat["pas"], "uniques_vus": etat["uniques_vus"],
                "duree_eval_s": round(time.time() - t0, 1)})
    ecrire_json(res, sortie)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True, nargs="+")
    ap.add_argument("--final", action="store_true")
    args = ap.parse_args()
    for nom in args.run:
        res = evaluer_run(nom, args.final)
        cles = sorted(res["par_jeu"], key=lambda k: (k.split("|")[0], int(k.split("|")[1])))
        print(nom, res["duree_eval_s"], "s :",
              " ".join(f"{k}={res['par_jeu'][k]['exact']:.3f}" for k in cles))


if __name__ == "__main__":
    main()
