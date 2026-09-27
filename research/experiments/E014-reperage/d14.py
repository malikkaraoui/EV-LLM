"""E014 -- donnees : VAL-OOD / VAL-ID / TEST (graines nouvelles), flux curriculum.

Reutilise E013 (donnees.py) et E008 (data.py) par import, sans les modifier.
Fige par PREREGISTREMENT.md section 2.
"""
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
E013 = os.path.join(os.path.dirname(ICI), "E013-insecte")
if E013 not in sys.path:
    sys.path.insert(0, E013)

import donnees as D13  # noqa: E402  (E013, inchange ; ajoute E008 au chemin)
from donnees import (ABSENT, LOT, decode, encode_aligne, encode_plat, n_pas,  # noqa: E402,F401
                     paires_flux)

e008 = D13.e008
VAL_LENS, LONG_LENS, ADV_LENS = D13.VAL_LENS, D13.LONG_LENS, D13.ADV_LENS
ID_LENS = [2, 3, 4, 5]
T_TRAIN = 6    # max(l) + 1 avec l <= 5
P_TRAIN = 13   # DEBUT + 5 + '+' + 5 + '='


def jeu_val():
    return {"VAL-OOD": D13._uniformes(3113, VAL_LENS, D13.N_VAL)}


def jeu_val_id():
    return {"VAL-ID": D13._uniformes(3119, ID_LENS, 200)}


def jeux_test():
    """TEST final (section 2) : {jeu: {L: [(a, b), ...]}}, deterministe, graines 3114-3118."""
    longs = D13._uniformes(3114, LONG_LENS, D13.N_LONG)
    longs.update(D13._uniformes(3115, [D13.L_MILLE], D13.N_MILLE))
    rc, rz, ra = (np.random.default_rng(g) for g in (3116, 3117, 3118))
    return {
        "T-ID": e008.jeux_de_test()["T-ID"],
        "T-LONG": longs,
        "ADV-CASCADE": {L: D13._cascade(L, rc) for L in ADV_LENS},
        "ADV-ZEROS": {L: D13._zeros(L, rz) for L in ADV_LENS},
        "ADV-ASYM": {L: D13._asym(L, ra) for L in ADV_LENS},
    }


def lmax_curriculum(pas, pas_total):
    """Lmax = 2, 3, 4, 5 sur quatre quarts egaux."""
    return 2 + min(3, (4 * pas) // pas_total)


def paires_curriculum(graine, pas, pas_total):
    rng = np.random.default_rng([40_000 + graine, pas])
    lmax, ex, out = lmax_curriculum(pas, pas_total), D13.exclues(), []
    while len(out) < LOT:
        la, lb = (int(x) for x in rng.integers(1, lmax + 1, 2))
        p = (e008.tire_nombre(rng, la), e008.tire_nombre(rng, lb))
        if p in ex:
            continue
        out.append(p)
    return out
