"""E012 -- donnees et encodages (PREREGISTREMENT section 5).

Formats : binaire aligne (X1), decimal aligne (X2), decimal plat E008 (X3).
Jeux sous la forme E008 : {nom_jeu: {L: [(a, b), ...]}}. numpy seulement.
"""
import json
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE_EXP = os.path.dirname(ICI)
for _d in ("E011-objectif-mdl", "E008-addition"):
    _p = os.path.join(RACINE_EXP, _d)
    if _p not in sys.path:
        sys.path.append(_p)  # apres ICI : nos modules gardent la priorite

from data import tire_nombre  # E008  # noqa: E402
import donnees as e011  # E011 (jeux binaires)  # noqa: E402

DEC_VAL_LENS = [6, 7, 8]
DEC_TEST_LENS = [10, 16, 32, 64, 100, 1000]
N_PAR_L, N_1000, N_ASYM = 500, 200, 50
GRAINE_VAL, GRAINE_TEST, GRAINE_ADV = 3127, 3128, 3129

EXPERIENCES = {
    "X1": {"base": 2, "format": "aligne", "n_train": 100},
    "X2-100": {"base": 10, "format": "aligne", "n_train": 100},
    "X2-1000": {"base": 10, "format": "aligne", "n_train": 1000},
    "X3": {"base": 10, "format": "plat", "n_train": 100},
}


# ---------------------------------------------------------------- entrainement
def jeu_entrainement(exp, graine):
    cfg = EXPERIENCES[exp]
    if cfg["base"] == 2:  # Lan 2022 : toutes les paires 0..9, identiques pour toutes les graines
        return [(a, b) for a in range(10) for b in range(10)]
    rng = np.random.default_rng([40_000 + graine, cfg["n_train"]])
    vus, out = set(), []
    while len(out) < cfg["n_train"]:
        la, lb = (int(x) for x in rng.integers(1, 6, 2))
        p = (tire_nombre(rng, la), tire_nombre(rng, lb))
        if p not in vus:
            vus.add(p)
            out.append(p)
    return out


# ---------------------------------------------------------------- validation / test decimaux
def _uniforme(graine, lens):
    rng = np.random.default_rng(graine)
    jeux = {}
    for L in lens:
        n = N_1000 if L == 1000 else N_PAR_L
        vus, items = set(), []
        while len(items) < n:
            p = (tire_nombre(rng, L), tire_nombre(rng, L))
            if p not in vus:
                vus.add(p)
                items.append(p)
        jeux[L] = items
    return jeux


def jeu_validation(base):
    if base == 2:
        return e011.jeu_validation()
    return {"V-OOD": _uniforme(GRAINE_VAL, DEC_VAL_LENS)}


def jeux_test(base, avec_1000=True):
    """Test final + adverses, evalues une seule fois a la fin."""
    if base == 2:
        return e011.jeux_test()
    lens = DEC_TEST_LENS if avec_1000 else DEC_TEST_LENS[:-1]
    rng = np.random.default_rng(GRAINE_ADV)
    cascade, zeros, asym = {}, {}, {}
    for L in lens:
        neuf = int("9" * L)
        cascade[L] = [(neuf, 1), (1, neuf)]
        h = 10 ** (L - 1)
        zeros[L] = [(h + 1, h + 3), (h + 2, h + 1)]
        asym[L] = ([(tire_nombre(rng, L), tire_nombre(rng, 3)) for _ in range(N_ASYM)]
                   + [(tire_nombre(rng, 3), tire_nombre(rng, L)) for _ in range(N_ASYM)])
    t = _uniforme(GRAINE_TEST, lens)
    return {"T-OOD": t, "A-CASCADE": cascade, "A-ZEROS": zeros, "A-ASYM": asym}


# ---------------------------------------------------------------- encodages
def chiffres_lsb(x, base, n):
    out = []
    for _ in range(n):
        out.append(x % base)
        x //= base
    return out


def nb_chiffres(x, base):
    n = 1
    while x >= base:
        x //= base
        n += 1
    return n


def encode_aligne(paires, base):
    """Liste de lots (X (B,T,2), Y (B,T), M (B,T)) ; un seul lot, L+1 pas par paire."""
    lg = [max(nb_chiffres(a, base), nb_chiffres(b, base)) + 1 for a, b in paires]
    T = max(lg)
    B = len(paires)
    X = np.zeros((B, T, 2))
    Y = np.zeros((B, T), dtype=np.int64)
    M = np.zeros((B, T))
    for i, ((a, b), n) in enumerate(zip(paires, lg)):
        X[i, :n, 0] = chiffres_lsb(a, base, n)
        X[i, :n, 1] = chiffres_lsb(b, base, n)
        Y[i, :n] = chiffres_lsb(a + b, base, n)
        M[i, :n] = 1.0
    return [(X, Y, M, list(range(B)))]


N_ENTREES_PLAT = 4  # valeur du chiffre, drapeau '+', drapeau '=', drapeau sortie


def _sequence_plate(a, b):
    L = max(len(str(a)), len(str(b)))
    x = [[int(c), 0, 0, 0] for c in str(a)] + [[0, 1, 0, 0]]
    x += [[int(c), 0, 0, 0] for c in str(b)] + [[0, 0, 1, 0]]
    debut = len(x)
    x += [[0, 0, 0, 1]] * (L + 1)
    cible = [int(c) for c in str(a + b).rjust(L + 1, "0")]  # poids fort d'abord
    return x, debut, cible


def encode_plat(paires):
    """Un lot par (longueur de a, longueur de b) : sequences de meme forme, sans rembourrage."""
    groupes = {}
    for i, (a, b) in enumerate(paires):
        groupes.setdefault((len(str(a)), len(str(b))), []).append(i)
    lots = []
    for _, idx in sorted(groupes.items()):
        seqs = [_sequence_plate(*paires[i]) for i in idx]
        T = len(seqs[0][0])
        X = np.array([s[0] for s in seqs], dtype=np.float64)
        Y = np.zeros((len(idx), T), dtype=np.int64)
        M = np.zeros((len(idx), T))
        for j, (_, debut, cible) in enumerate(seqs):
            Y[j, debut:] = cible
            M[j, debut:] = 1.0
        lots.append((X, Y, M, idx))
    return lots


def encodeur(exp):
    cfg = EXPERIENCES[exp]
    if cfg["format"] == "plat":
        return encode_plat
    return lambda paires: encode_aligne(paires, cfg["base"])


def n_entrees(exp):
    return N_ENTREES_PLAT if EXPERIENCES[exp]["format"] == "plat" else 2


# ---------------------------------------------------------------- utilitaires
def ecrire_json(obj, chemin):
    with open(chemin, "w") as f:
        json.dump(obj, f, indent=1)


def lire_json(chemin):
    with open(chemin) as f:
        return json.load(f)
