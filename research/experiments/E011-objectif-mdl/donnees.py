"""E011 -- donnees : addition binaire poids faible d'abord (PREREGISTREMENT section 2).

numpy seulement. Les jeux ont la forme E008 : {nom_jeu: {L: [(a, b), ...]}}.
"""
import json
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
E008 = os.path.join(os.path.dirname(ICI), "E008-addition")
if E008 not in sys.path:
    sys.path.insert(0, E008)

N_TRAIN = 100
TRAIN_LMIN, TRAIN_LMAX = 1, 5
VAL_LENS = [6, 7, 8]
TEST_LENS = [10, 16, 32, 64, 100, 1000]
N_PAR_L = 500
N_1000 = 200
N_ASYM = 50
GRAINE_VAL, GRAINE_TEST, GRAINE_ADV = 3027, 3028, 3029


def tire_bits(rng, lg):
    """Entier de `lg` bits (bit de tete = 1 sauf si lg == 1)."""
    if lg == 1:
        return int(rng.integers(0, 2))
    bits = [1] + [int(x) for x in rng.integers(0, 2, lg - 1)]
    return int("".join(map(str, bits)), 2)


def jeu_entrainement(graine):
    """100 paires distinctes, longueurs uniformes independantes dans 1-5 bits."""
    rng = np.random.default_rng(20_000 + graine)
    vus, out = set(), []
    while len(out) < N_TRAIN:
        la, lb = (int(x) for x in rng.integers(TRAIN_LMIN, TRAIN_LMAX + 1, 2))
        p = (tire_bits(rng, la), tire_bits(rng, lb))
        if p not in vus:
            vus.add(p)
            out.append(p)
    return out


def _uniforme(graine, lens):
    rng = np.random.default_rng(graine)
    jeux = {}
    for L in lens:
        n = N_1000 if L == 1000 else N_PAR_L
        vus, items = set(), []
        while len(items) < n:
            p = (tire_bits(rng, L), tire_bits(rng, L))
            if p not in vus:
                vus.add(p)
                items.append(p)
        jeux[L] = items
    return jeux


def jeu_validation():
    return {"V-OOD": _uniforme(GRAINE_VAL, VAL_LENS)}


def jeux_test():
    """Test final + adverses (evalues une seule fois, a la fin)."""
    rng = np.random.default_rng(GRAINE_ADV)
    cascade, zeros, asym = {}, {}, {}
    for L in TEST_LENS:
        un = 2 ** L - 1
        cascade[L] = [(un, 1), (1, un)]
        h = 2 ** (L - 1)
        zeros[L] = [(h + 1, h + 3), (h + 2, h + 1)]
        asym[L] = ([(tire_bits(rng, L), tire_bits(rng, 3)) for _ in range(N_ASYM)]
                   + [(tire_bits(rng, 3), tire_bits(rng, L)) for _ in range(N_ASYM)])
    return {"T-OOD": _uniforme(GRAINE_TEST, TEST_LENS), "A-CASCADE": cascade,
            "A-ZEROS": zeros, "A-ASYM": asym}


# ---------------------------------------------------------------- encodage
def bits_lsb(x, n):
    return [(x >> i) & 1 for i in range(n)]


def encode(paires, T=None):
    """X (B, T, 2) float, Y (B, T) float, M (B, T) masque ; L+1 pas par paire."""
    longueurs = [max(a.bit_length(), b.bit_length(), 1) + 1 for a, b in paires]
    T = T or max(longueurs)
    B = len(paires)
    X = np.zeros((B, T, 2))
    Y = np.zeros((B, T))
    M = np.zeros((B, T))
    for i, ((a, b), n) in enumerate(zip(paires, longueurs)):
        X[i, :n, 0] = bits_lsb(a, n)
        X[i, :n, 1] = bits_lsb(b, n)
        Y[i, :n] = bits_lsb(a + b, n)
        M[i, :n] = 1.0
    return X, Y, M


def ecrire_json(obj, chemin):
    with open(chemin, "w") as f:
        json.dump(obj, f, indent=1)


def lire_json(chemin):
    with open(chemin) as f:
        return json.load(f)
