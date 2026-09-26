"""E008 -- donnees : vocabulaire, jeux de test, flux d'entrainement deterministe.

Tout est fige par PREREGISTREMENT.md (sections 1 et 2). numpy seulement.
"""
import json

import numpy as np

# Vocabulaire : un token par chiffre.
PLUS, EGAL, FIN, PAD = 10, 11, 12, 13
VOCAB = 14
CARS = "0123456789+=$_"

TRAIN_LMIN, TRAIN_LMAX = 1, 5
BATCH = 256
SEQ_TRAIN = 20  # 5 + 1 + 5 + 1 + 6 + 1 = 19 tokens au plus -> entree/cible de 19, marge 1

ID_LENS = [2, 3, 4, 5]
OOD_LENS = [6, 7, 8, 10, 12, 16]
CARRY_LENS = [2, 3, 4, 5, 6, 7, 8, 10, 12, 16]
N_PAR_LONGUEUR = 500
GRAINE_ID, GRAINE_OOD, GRAINE_CARRY = 2026, 2027, 2028


# ---------------------------------------------------------------- operandes
def tire_nombre(rng, lg):
    """Un entier de `lg` chiffres (premier chiffre != 0 sauf si lg == 1)."""
    if lg == 1:
        return int(rng.integers(0, 10))
    ch = [int(rng.integers(1, 10))] + [int(x) for x in rng.integers(0, 10, lg - 1)]
    return int("".join(map(str, ch)))


def chaine_retenue(a, b):
    """Plus longue suite de positions consecutives emettant une retenue."""
    best = cur = 0
    r = 0
    while a > 0 or b > 0:
        s = a % 10 + b % 10 + r
        r = 1 if s >= 10 else 0
        cur = cur + 1 if r else 0
        best = max(best, cur)
        a //= 10
        b //= 10
    return best


# ---------------------------------------------------------------- jeux de test
def _jeu_uniforme(graine, lens, n):
    rng = np.random.default_rng(graine)
    jeux = {}
    for L in lens:
        vus, items = set(), []
        while len(items) < n:
            p = (tire_nombre(rng, L), tire_nombre(rng, L))
            if p not in vus:
                vus.add(p)
                items.append(p)
        jeux[L] = items
    return jeux


def _paire_toute_retenue(rng, L):
    """Deux nombres de L chiffres dont chaque position emet une retenue."""
    da, db = [], []
    for i in range(L):  # i = 0 : poids faible
        lo = 1 if i == L - 1 else 0
        seuil = 10 if i == 0 else 9
        ok = [(x, y) for x in range(lo, 10) for y in range(lo, 10) if x + y >= seuil]
        x, y = ok[int(rng.integers(0, len(ok)))]
        da.append(x)
        db.append(y)
    a = int("".join(map(str, reversed(da))))
    b = int("".join(map(str, reversed(db))))
    return a, b


def _jeu_carry(graine, lens, n):
    rng = np.random.default_rng(graine)
    jeux = {}
    for L in lens:
        vus, items = set(), []
        while len(items) < n:
            p = _paire_toute_retenue(rng, L)
            if p not in vus:
                vus.add(p)
                items.append(p)
        neuf = int("9" * L)
        items += [(neuf, 1), (1, neuf)]
        jeux[L] = items
    return jeux


def jeux_de_test():
    """{nom_jeu: {L: [(a, b), ...]}} -- deterministe."""
    return {
        "T-ID1": {1: [(a, b) for a in range(10) for b in range(10)]},
        "T-ID": _jeu_uniforme(GRAINE_ID, ID_LENS, N_PAR_LONGUEUR),
        "T-OOD": _jeu_uniforme(GRAINE_OOD, OOD_LENS, N_PAR_LONGUEUR),
        "T-CARRY": _jeu_carry(GRAINE_CARRY, CARRY_LENS, N_PAR_LONGUEUR),
    }


def paires_exclues(jeux=None):
    """Paires (et paires echangees) interdites a l'entrainement (T-ID1 exclu : ecart assume)."""
    jeux = jeux or jeux_de_test()
    ex = set()
    for nom, par_l in jeux.items():
        if nom == "T-ID1":
            continue
        for items in par_l.values():
            for a, b in items:
                ex.add((a, b))
                ex.add((b, a))
    return ex


# ---------------------------------------------------------------- encodage
def reponse(a, b, inverse):
    s = str(a + b)
    return s[::-1] if inverse else s


def encode_prompt(a, b):
    return [int(c) for c in str(a)] + [PLUS] + [int(c) for c in str(b)] + [EGAL]


def encode_exemple(a, b, inverse):
    return encode_prompt(a, b) + [int(c) for c in reponse(a, b, inverse)] + [FIN]


# ---------------------------------------------------------------- flux d'entrainement
def paires_du_pas(graine, pas, exclues, batch=BATCH):
    """Paires du lot `pas` de la graine `graine` (deterministe, reprise possible)."""
    rng = np.random.default_rng([10_000 + graine, pas])
    out = []
    while len(out) < batch:
        la, lb = (int(x) for x in rng.integers(TRAIN_LMIN, TRAIN_LMAX + 1, 2))
        p = (tire_nombre(rng, la), tire_nombre(rng, lb))
        if p in exclues:
            continue
        out.append(p)
    return out


def lot(graine, pas, exclues, inverse, batch=BATCH):
    """(x, y, masque) numpy int32/float32 de forme (batch, SEQ_TRAIN-1)."""
    paires = paires_du_pas(graine, pas, exclues, batch)
    seq = np.full((batch, SEQ_TRAIN), PAD, dtype=np.int32)
    masque = np.zeros((batch, SEQ_TRAIN - 1), dtype=np.float32)
    for i, (a, b) in enumerate(paires):
        e = encode_exemple(a, b, inverse)
        seq[i, : len(e)] = e
        debut = len(encode_prompt(a, b))  # premier token de reponse
        # cible y[t] = seq[t+1] : les tokens de reponse sont les cibles t = debut-1 .. len(e)-2
        masque[i, debut - 1 : len(e) - 1] = 1.0
    return seq[:, :-1], seq[:, 1:], masque


# ---------------------------------------------------------------- utilitaires
def lire_json(chemin):
    with open(chemin) as f:
        return json.load(f)


def ecrire_json(obj, chemin):
    with open(chemin, "w") as f:
        json.dump(obj, f, indent=1)
