"""E013 -- donnees : jeux VAL-OOD / TEST / adverses, encodages aligne (I1) et plat (I2).

Reutilise E008 par import (research/experiments/E008-addition/, non modifie) :
flux d'entrainement, tirage des operandes, jeux T-ID, generateur "toute retenue".
Fige par PREREGISTREMENT.md section 2.
"""
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
E008 = os.path.join(os.path.dirname(ICI), "E008-addition")
if E008 not in sys.path:
    sys.path.insert(0, E008)

import data as e008  # noqa: E402  (module E008, inchange)

VAL_LENS = [6, 7, 8]
LONG_LENS = [10, 16, 32, 64, 100]
L_MILLE = 1000
ADV_LENS = [10, 16, 32, 64, 100, 1000]
N_VAL = N_LONG = 500
N_MILLE = 200
N_ADV = 100
LOT = 128
ABSENT = 10          # I1 : chiffre absent (operande plus court)
DEBUT, VIDE = 12, 13  # I2 : symbole de debut, remplissage (0-9, + = 10, = = 11 comme E008)
VOCAB_PLAT = 14


# ---------------------------------------------------------------- jeux
def _uniformes(graine, lens, n):
    rng = np.random.default_rng(graine)
    jeux = {}
    for L in lens:
        vus, items = set(), []
        while len(items) < n:
            p = (e008.tire_nombre(rng, L), e008.tire_nombre(rng, L))
            if p not in vus:
                vus.add(p)
                items.append(p)
        jeux[L] = items
    return jeux


def jeu_val():
    return {"VAL-OOD": _uniformes(3013, VAL_LENS, N_VAL)}


def _cascade(L, rng):
    neuf = int("9" * L)
    items = [(neuf, 1), (1, neuf), (neuf, neuf)]
    vus = set(items)
    while len(items) < 3 + N_ADV:
        p = e008._paire_toute_retenue(rng, L)
        if p not in vus:
            vus.add(p)
            items.append(p)
    return items


def _creux(rng, L):
    ch = [1] + [int(rng.integers(1, 10)) if rng.random() < 0.1 else 0 for _ in range(L - 1)]
    return int("".join(map(str, ch)))


def _zeros(L, rng):
    items = [(10 ** (L - 1) + 2, 10 ** (L - 1) + 3)]
    vus = set(items)
    while len(items) < 1 + N_ADV:
        p = (_creux(rng, L), _creux(rng, L))
        if p not in vus:
            vus.add(p)
            items.append(p)
    return items


def _asym(L, rng):
    items = [(10 ** (L - 1), 999)]
    vus = set(items)
    while len(items) < 1 + N_ADV:
        long_ = e008.tire_nombre(rng, L)
        court = e008.tire_nombre(rng, int(rng.integers(1, 6)))
        p = (long_, court) if rng.random() < 0.5 else (court, long_)
        if p not in vus:
            vus.add(p)
            items.append(p)
    return items


def jeux_test():
    """TEST final (section 2) : {jeu: {L: [(a, b), ...]}}, deterministe."""
    longs = _uniformes(3014, LONG_LENS, N_LONG)
    longs.update(_uniformes(3015, [L_MILLE], N_MILLE))
    rc, rz, ra = (np.random.default_rng(g) for g in (3016, 3017, 3018))
    return {
        "T-ID": e008.jeux_de_test()["T-ID"],
        "T-LONG": longs,
        "ADV-CASCADE": {L: _cascade(L, rc) for L in ADV_LENS},
        "ADV-ZEROS": {L: _zeros(L, rz) for L in ADV_LENS},
        "ADV-ASYM": {L: _asym(L, ra) for L in ADV_LENS},
    }


# ---------------------------------------------------------------- flux d'entrainement
_EXCLUES = None


def exclues():
    global _EXCLUES
    if _EXCLUES is None:
        _EXCLUES = e008.paires_exclues()
    return _EXCLUES


def paires_flux(graine, pas):
    """Lot du pas `pas` : flux E008, lot de 128."""
    return e008.paires_du_pas(graine, pas, exclues(), LOT)


def jeu_fixe(graine, n):
    """I3 : les n premieres paires distinctes du flux de la graine."""
    vus, out, pas = set(), [], 0
    while len(out) < n:
        for p in paires_flux(graine, pas):
            if p not in vus and len(out) < n:
                vus.add(p)
                out.append(p)
        pas += 1
    return out


def paires_fixes(jeu, graine, pas):
    rng = np.random.default_rng([20_000 + graine, pas])
    idx = rng.integers(0, len(jeu), min(LOT, len(jeu)))
    return [jeu[i] for i in idx]


# ---------------------------------------------------------------- encodages
def chiffres_lsb(x):
    return [ord(c) - 48 for c in reversed(str(x))]


def n_pas(a, b):
    return max(len(str(a)), len(str(b))) + 1


def encode_aligne(paires, T=None):
    """I1 : A, B (n, T) int32 poids faible d'abord, ABSENT au-dela ; cibles (n, T) ; masque."""
    T = T or max(n_pas(a, b) for a, b in paires)
    A = np.full((len(paires), T), ABSENT, dtype=np.int32)
    B = np.full((len(paires), T), ABSENT, dtype=np.int32)
    Y = np.zeros((len(paires), T), dtype=np.int32)
    M = np.zeros((len(paires), T), dtype=np.float32)
    for i, (a, b) in enumerate(paires):
        da, db = chiffres_lsb(a), chiffres_lsb(b)
        A[i, : len(da)] = da
        B[i, : len(db)] = db
        n = n_pas(a, b)
        s = chiffres_lsb(a + b)
        Y[i, : len(s)] = s  # au-dela : 0 (retenue finale nulle)
        M[i, :n] = 1.0
    return A, B, Y, M


def encode_plat(paires, P=None):
    """I2 : DEBUT + prompt E008 (a+b=, poids fort d'abord), VIDE a droite."""
    seqs = [[DEBUT] + e008.encode_prompt(a, b) for a, b in paires]
    P = P or max(len(s) for s in seqs)
    S = np.full((len(paires), P), VIDE, dtype=np.int32)
    for i, s in enumerate(seqs):
        S[i, : len(s)] = s
    return S


def decode(chiffres_lsb_emis):
    """Chiffres emis (poids faible d'abord) -> reponse canonique : retire UN seul 0 final."""
    s = "".join(str(int(d)) for d in reversed(chiffres_lsb_emis))
    if len(s) > 1 and s[0] == "0":
        s = s[1:]
    return s
