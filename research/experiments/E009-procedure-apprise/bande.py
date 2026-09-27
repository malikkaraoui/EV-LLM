"""E009 -- donnees : bande de calcul, lots d'entrainement, jeux VAL / TEST / ADV-*.

Reutilise E008 par import (flux d'entrainement, tirage, T-ID) sans le modifier.
Tout est fige par PREREGISTREMENT.md (sections 2 et 5). numpy seulement.
"""
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
E008 = os.path.join(os.path.dirname(ICI), "E008-addition")
if E008 not in sys.path:
    sys.path.insert(1, E008)

import data as d8  # noqa: E402  (E008, non modifie)

PLUS, EGAL, FIN, PAD = d8.PLUS, d8.EGAL, d8.FIN, d8.PAD
SLOT = 14
VOCAB = 15
CARS = d8.CARS + "_"  # SLOT affiche comme remplissage

BATCH = d8.BATCH
VAL_LENS = [6, 7, 8]
TEST_LENS = [10, 16, 32, 64, 100]
N_VAL, N_TEST, N_ADV = 300, 200, 100
N_ASYM = 50
GRAINE_VAL, GRAINE_TEST = 2030, 2031
GRAINE_RET, GRAINE_ZERO, GRAINE_ASYM = 2032, 2033, 2034


# ---------------------------------------------------------------- bande
def bande_entree(a, b):
    """Entree plate E008 (`a+b=`) suivie d'autant de cases reponse : longueur 2n."""
    p = d8.encode_prompt(a, b)
    return p + [SLOT] * len(p)


def cible_cases(a, b, inverse):
    """Cible des n cases reponse : chiffres de la somme, `$`, puis remplissage."""
    n = len(d8.encode_prompt(a, b))
    rep = [int(c) for c in d8.reponse(a, b, inverse)] + [FIN]
    assert len(rep) <= n
    return rep + [PAD] * (n - len(rep))


def t_de_n(a, b):
    """T(n) donne a A3-T : max(la, lb) + 1 (PREREGISTREMENT section 3)."""
    return max(len(str(a)), len(str(b))) + 1


def bandes(paires, inverse):
    """(x, y, masque, t_n) numpy ; bandes completees a droite jusqu'a la plus longue."""
    ns = [len(d8.encode_prompt(a, b)) for a, b in paires]
    L = 2 * max(ns)
    B = len(paires)
    x = np.full((B, L), PAD, dtype=np.int32)
    y = np.full((B, L), PAD, dtype=np.int32)
    m = np.zeros((B, L), dtype=np.float32)
    for i, ((a, b), n) in enumerate(zip(paires, ns)):
        x[i, : 2 * n] = bande_entree(a, b)
        y[i, n: 2 * n] = cible_cases(a, b, inverse)
        m[i, n: 2 * n] = 1.0
    t_n = np.array([t_de_n(a, b) for a, b in paires], dtype=np.int32)
    return x, y, m, t_n


def lot(graine, pas, exclues, inverse, batch=BATCH):
    """Lot du pas `pas` : exactement les paires du flux E008 (meme graine, meme pas)."""
    return bandes(d8.paires_du_pas(graine, pas, exclues, batch), inverse)


# ---------------------------------------------------------------- decodage
def decode_cases(toks, probs, inverse):
    """Cases reponse (argmax, proba argmax) -> (reponse canonique | None, confiance)."""
    toks = [int(t) for t in toks]
    if FIN not in toks:
        return None, float(np.prod(probs))
    k = toks.index(FIN)
    s = "".join(CARS[t] for t in toks[:k])
    return (s[::-1] if inverse else s), float(np.prod(probs[: k + 1]))


# ---------------------------------------------------------------- jeux
def _asym(graine, lens, courts, n):
    rng = np.random.default_rng(graine)
    jeux = {}
    for L in lens:
        for c in courts:
            vus, items = set(), []
            while len(items) < n:
                p = (d8.tire_nombre(rng, L), d8.tire_nombre(rng, c))
                if p not in vus:
                    vus.add(p)
                    items.append(p)
            jeux[f"{L}+{c}"] = items
            jeux[f"{c}+{L}"] = [(b, a) for a, b in items]
    return jeux


def _nombre_creux(rng, L):
    ch = [int(rng.integers(1, 10))]
    for _ in range(L - 1):
        ch.append(0 if rng.random() < 0.9 else int(rng.integers(1, 10)))
    return int("".join(map(str, ch)))


def _zero(graine, lens, n):
    rng = np.random.default_rng(graine)
    jeux = {}
    for L in lens:
        base = 10 ** (L - 1)
        items, vus = [(base + 2, base + 3)], {(base + 2, base + 3)}
        while len(items) < n + 1:
            p = (_nombre_creux(rng, L), _nombre_creux(rng, L))
            if p not in vus:
                vus.add(p)
                items.append(p)
        jeux[L] = items
    return jeux


def jeux_val():
    return {"VAL": d8._jeu_uniforme(GRAINE_VAL, VAL_LENS, N_VAL)}


def jeux_id():
    return {"T-ID": {L: v[:200] for L, v in d8.jeux_de_test()["T-ID"].items()}}


def jeux_final():
    """TEST + adverses : evalues UNE seule fois, a la fin (PREREGISTREMENT section 5)."""
    return {
        "TEST": d8._jeu_uniforme(GRAINE_TEST, TEST_LENS, N_TEST),
        "ADV-RET": d8._jeu_carry(GRAINE_RET, TEST_LENS, N_ADV),
        "ADV-ZERO": _zero(GRAINE_ZERO, TEST_LENS, N_ADV),
        "ADV-ASYM": _asym(GRAINE_ASYM, TEST_LENS, [1, 3], N_ASYM),
    }


def sous_val(n=100):
    return {"VAL": {L: v[:n] for L, v in jeux_val()["VAL"].items()}}


def lire_json(chemin):
    return d8.lire_json(chemin)


def ecrire_json(obj, chemin):
    d8.ecrire_json(obj, chemin)
