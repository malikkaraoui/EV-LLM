"""E014 -- systemes au format de l'evaluateur E008 et autodiagnostic.

Confiance passee a l'evaluateur = p_min : min sur les colonnes de la probabilite du chiffre emis
(PREREGISTREMENT section 5). Le produit (definition E013) est garde en second.
"""
import os
from collections import defaultdict

import mlx.core as mx
import numpy as np

import d14 as D
from m14 import R2, Composition, Lecteur
from modeles import I2

ICI = os.path.dirname(os.path.abspath(__file__))
TAILLE_LOT = 400
TAUS = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]


def cree(config):
    """R0a, R0b -> I2 d'E013 ; R2 ; R1L -> Lecteur ; R1G, R1J -> Composition."""
    if config in ("R0a", "R0b"):
        return I2(8)
    if config == "R2":
        return R2(8)
    if config == "R1L":
        return Lecteur(8)
    if config in ("R1G", "R1J"):
        return Composition()
    raise ValueError(config)


def composition_gelee(graine, chemin_lecteur):
    """Lecteur (graine s, gele) + I1 H = 4 d'E013 (graine s, gele), aucun entrainement joint."""
    m = Composition()
    m.lecteur.load_weights(chemin_lecteur)
    m.i1.load_weights(os.path.join(ICI, "i1_e013", f"I1-H4-s{graine}.safetensors"))
    mx.eval(m.parameters())
    return m


def charge(config, chemin):
    m = cree(config)
    m.load_weights(chemin)
    mx.eval(m.parameters())
    return m


def _groupes(paires):
    g = defaultdict(list)
    for i, (a, b) in enumerate(paires):
        g[D.n_pas(a, b)].append(i)
    for n, idx in sorted(g.items()):
        for k in range(0, len(idx), TAILLE_LOT):
            yield n, idx[k: k + TAILLE_LOT]


def details(m, paires):
    """Par paire : dict(rep, pmin, prod[, lu_ok, pmin_lu]). Lecteur seul : lu_ok, pmin_lu."""
    out = [None] * len(paires)
    for n, idx in _groupes(paires):
        sous = [paires[i] for i in idx]
        S = mx.array(D.encode_plat(sous))
        lu = None
        if isinstance(m, Lecteur):
            logits, lu = None, m(S, n, eval_tous=64)
        elif isinstance(m, Composition):
            logits, lu = m(S, n, avec_lecture=True, eval_tous=64)
        else:
            logits = m(S, n, eval_tous=64)
        if logits is not None:
            p = mx.softmax(logits.astype(mx.float32), axis=-1)
            tok = np.array(mx.argmax(p, axis=-1))
            pmax = np.array(mx.max(p, axis=-1)).astype(np.float64)
        if lu is not None:
            A, B, _, _ = D.encode_aligne(sous, n)
            pa = mx.softmax(lu[..., :11].astype(mx.float32), axis=-1)
            pb = mx.softmax(lu[..., 11:].astype(mx.float32), axis=-1)
            ok = np.array((mx.argmax(pa, -1) == mx.array(A)) & (mx.argmax(pb, -1) == mx.array(B)))
            plu = np.minimum(np.array(mx.max(pa, -1)), np.array(mx.max(pb, -1))).astype(np.float64)
        for j, i in enumerate(idx):
            r = {}
            if logits is not None:
                r.update(rep=D.decode(tok[j, :n]), pmin=float(pmax[j, :n].min()),
                         prod=float(np.prod(pmax[j, :n])))
            if lu is not None:
                r.update(lu_ok=bool(ok[j, :n].all()), pmin_lu=float(plu[j, :n].min()))
            out[i] = r
    return out


def systeme(m, journal=None):
    """Systeme E008 : (paires) -> [(reponse, p_min)] ; `journal` recoit les details."""
    def f(paires):
        d = details(m, paires)
        if journal is not None:
            journal.extend(d)
        return [(x["rep"], x["pmin"]) for x in d]
    return f


def val_exact(m):
    from evaluate import evaluer, resume  # evaluateur E008
    r = resume(evaluer(systeme(m), D.jeu_val(), "val"))["par_jeu"]
    return float(np.mean([c["exact"] for c in r.values()]))


def lecture_exacte(m, jeux):
    """Lecteur : exactitude de lecture (toutes les paires justes) moyenne sur les jeux x L."""
    acc = [np.mean([x["lu_ok"] for x in details(m, it)])
           for par_l in jeux.values() for it in par_l.values()]
    return float(np.mean(acc))


def seuil_abstention(pmins_justes):
    """Plus grand tau tel que <= 5 % des reponses justes aient p_min < tau (section 5)."""
    x = np.asarray(pmins_justes)
    ok = [t for t in TAUS if len(x) and np.mean(x < t) <= 0.05]
    return max(ok) if ok else None
