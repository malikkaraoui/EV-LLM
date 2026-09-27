"""E013 -- systemes au format de l'evaluateur E008 : (liste de (a, b)) -> [(reponse, confiance)].

Confiance = produit des probabilites des chiffres emis (meme definition qu'E008).
`details` renvoie en plus la probabilite minimale par pas (autodiagnostic).
"""
from collections import defaultdict

import mlx.core as mx
import numpy as np

import donnees as D
from modeles import I1, I2

TAILLE_LOT = 400


def _groupes(paires):
    g = defaultdict(list)
    for i, (a, b) in enumerate(paires):
        g[D.n_pas(a, b)].append(i)
    for n, idx in sorted(g.items()):
        for k in range(0, len(idx), TAILLE_LOT):
            yield n, idx[k: k + TAILLE_LOT]


def details(m, paires):
    """[(reponse, confiance, p_min)] pour chaque paire."""
    out = [None] * len(paires)
    for n, idx in _groupes(paires):
        sous = [paires[i] for i in idx]
        if isinstance(m, I2):
            logits = m(mx.array(D.encode_plat(sous)), n, eval_tous=64)
        else:
            A, B, _, _ = D.encode_aligne(sous, n)
            logits = m(mx.array(A), mx.array(B), eval_tous=64)
        p = mx.softmax(logits.astype(mx.float32), axis=-1)
        tok = np.array(mx.argmax(p, axis=-1))
        pmax = np.array(mx.max(p, axis=-1)).astype(np.float64)
        for j, i in enumerate(idx):
            out[i] = (D.decode(tok[j, :n]), float(np.prod(pmax[j, :n])), float(pmax[j, :n].min()))
    return out


def systeme(m):
    return lambda paires: [(r, c) for r, c, _ in details(m, paires)]


def cree(config):
    """config : 'I1-H4', 'I2', 'I3-N100' (I3 = I1 H = 4)."""
    if config.startswith("I1-H"):
        return I1(int(config[4:]))
    if config.startswith("I3-N"):
        return I1(4)
    if config == "I2":
        return I2(8)
    raise ValueError(config)


def charge(config, chemin):
    m = cree(config)
    m.load_weights(chemin)
    mx.eval(m.parameters())
    return m
