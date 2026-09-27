"""E015 -- donnees : mini-taches (phase A), taches nouvelles N1/N2/N3 (phase B), VAL, TEST, oracle.

Reutilise E013 (donnees.py) et E008 (data.py, evaluate.py) par import, sans les modifier.
Fige par PREREGISTREMENT.md sections 2, 3 et 5.
"""
import os
import sys
from collections import defaultdict

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
E013 = os.path.join(os.path.dirname(ICI), "E013-insecte")
if E013 not in sys.path:
    sys.path.insert(0, E013)

import donnees as D13  # noqa: E402  (E013, inchange ; ajoute E008 au chemin)

e008 = D13.e008
from evaluate import SEUIL_SUR, resume  # noqa: E402,F401  (E008, inchange)

# symboles des flux (phase B) ; alphabet des champions : 0-9 + ABSENT_C
PLUS, EGAL, MOINS, ABS = 10, 11, 12, 13
NSYM = 14
ABSENT_C = 10
CARS = "0123456789+=-_"

VAL_LENS = [6, 7, 8]
LONG_LENS = [10, 16, 32, 64, 100]
L_MILLE = 1000
ADV_LENS = [10, 16, 32, 64, 100, 1000]
ID_LENS = [2, 3, 4, 5]
N_VAL, N_LONG, N_MILLE, N_ADV, N_ID = 500, 500, 200, 100, 200
TACHES = ["N1", "N2", "N3"]

# ------------------------------------------------------------------ phase A : mini-taches
MINI = ["M-COPIE", "M-COMPL", "M-SUCC", "M-SOMME", "M-DIFF"]
PORTS = {"M-COPIE": 1, "M-COMPL": 1, "M-SUCC": 1, "M-SOMME": 2, "M-DIFF": 2}


def lsb(x):
    return [ord(c) - 48 for c in reversed(str(x))]


def cible_mini(tache, ops):
    """Sortie attendue (liste de chiffres, max(l)+1 pas) de la mini-tache sur les operandes."""
    T = max(len(str(x)) for x in ops) + 1
    if tache == "M-COPIE":
        y = lsb(ops[0])
    elif tache == "M-COMPL":
        y = [9 - d for d in lsb(ops[0])]
    elif tache == "M-SUCC":
        y = lsb(ops[0] + 1)
    elif tache == "M-SOMME":
        y = lsb(ops[0] + ops[1])
    elif tache == "M-DIFF":
        da, db = lsb(ops[0]), lsb(ops[1])
        y = [((da[t] if t < len(da) else 0) - (db[t] if t < len(db) else 0)) % 10
             for t in range(T - 1)]
    else:
        raise ValueError(tache)
    y = y + [0] * (T - len(y))
    assert len(y) == T
    return y


def items_mini(rng, tache, lmin, lmax, n):
    out = []
    for _ in range(n):
        out.append(tuple(e008.tire_nombre(rng, int(rng.integers(lmin, lmax + 1)))
                         for _ in range(PORTS[tache])))
    return out


def lot_mini(graine, tache, pas, n=128):
    rng = np.random.default_rng([70_000 + graine, MINI.index(tache), pas])
    return items_mini(rng, tache, 1, 5, n)


def val_mini(tache):
    rng = np.random.default_rng([3213, MINI.index(tache)])
    out = []
    for L in VAL_LENS:
        out += items_mini(rng, tache, L, L, 100)
    return out


def encode_ports(items, k):
    """items : tuples d'entiers -> (X (n, T, k) int alphabet champion, lens (n,))."""
    T = max(max(len(str(x)) for x in it) for it in items) + 1
    X = np.full((len(items), T, k), ABSENT_C, dtype=np.int64)
    lens = np.zeros(len(items), dtype=np.int64)
    for i, it in enumerate(items):
        for p, x in enumerate(it):
            d = lsb(x)
            X[i, : len(d), p] = d
        lens[i] = max(len(str(x)) for x in it) + 1
    return X, lens


# ------------------------------------------------------------------ phase B : taches nouvelles
def phrase(tache, it):
    """Phrase brute (poids fort d'abord) : a+b=, a+b+c=, a-b=."""
    ch = lambda x: [int(c) for c in str(x)]  # noqa: E731
    if tache == "N1":
        return ch(it[0]) + [PLUS] + ch(it[1]) + [EGAL]
    if tache == "N2":
        return ch(it[0]) + [PLUS] + ch(it[1]) + [PLUS] + ch(it[2]) + [EGAL]
    if tache == "N3":
        return ch(it[0]) + [MOINS] + ch(it[1]) + [EGAL]
    raise ValueError(tache)


def reference(tache, it):
    """Reference du juge : arithmetique Python sur les entiers."""
    if tache == "N1":
        return str(it[0] + it[1])
    if tache == "N2":
        return str(it[0] + it[1] + it[2])
    return str(it[0] - it[1])


# ---- oracle : algorithme en colonnes sur les chaines (aucun + / - Python sur les entiers)
def oracle_somme(ops):
    ss = [str(x)[::-1] for x in ops]
    out, r = [], 0
    for i in range(max(len(s) for s in ss)):
        t = r + sum(ord(s[i]) - 48 for s in ss if i < len(s))
        out.append(chr(48 + t % 10))
        r = t // 10
    while r:
        out.append(chr(48 + r % 10))
        r //= 10
    s = "".join(reversed(out)).lstrip("0")
    return s or "0"


def oracle_diff(a, b):
    sa, sb = str(a)[::-1], str(b)[::-1]
    out, e = [], 0
    for i in range(len(sa)):
        t = (ord(sa[i]) - 48) - (ord(sb[i]) - 48 if i < len(sb) else 0) - e
        e = 1 if t < 0 else 0
        out.append(chr(48 + t + 10 * e))
    s = "".join(reversed(out)).lstrip("0")
    return s or "0"


def oracle(tache, it):
    return oracle_diff(*it) if tache == "N3" else oracle_somme(it)


# ---- tirages
def _item(rng, tache, lmin, lmax, lens=None):
    k = 3 if tache == "N2" else 2
    ls = lens or [int(rng.integers(lmin, lmax + 1)) for _ in range(k)]
    it = tuple(e008.tire_nombre(rng, L) for L in ls)
    if tache == "N3" and it[0] < it[1]:
        it = (it[1], it[0])
    return it


def _uniformes(graine, tache, lens, n):
    rng = np.random.default_rng(graine)
    jeux = {}
    for L in lens:
        vus, items = set(), []
        while len(items) < n:
            it = _item(rng, tache, L, L)
            if it not in vus:
                vus.add(it)
                items.append(it)
        jeux[L] = items
    return jeux


def _uniques(gen, n, spec=()):
    items, vus = list(spec), set(spec)
    while len(items) < n + len(spec):
        it = gen()
        if it not in vus:
            vus.add(it)
            items.append(it)
    return items


def _propag(rng, L):
    """a + b = 10^L, a et b de L chiffres, dernier chiffre de a non nul (lecon R010)."""
    ch = [int(rng.integers(1, 9))] + [int(x) for x in rng.integers(0, 10, L - 1)]
    if ch[-1] == 0:
        ch[-1] = int(rng.integers(1, 10))
    a = int("".join(map(str, ch)))
    return (a, 10 ** L - a)


def _cascade3(rng, L):
    return tuple(int("".join(str(int(rng.integers(6 if i else 6, 10))) for i in range(L)))
                 for _ in range(3))


def _propag3(rng, L):
    a = int(str(int(rng.integers(1, 4))) + "".join(str(int(x)) for x in rng.integers(0, 10, L - 1)))
    b = int(str(int(rng.integers(1, 4))) + "".join(str(int(x)) for x in rng.integers(0, 10, L - 1)))
    return (a, b, 10 ** L - a - b)


def _asym3(rng, L):
    it = [e008.tire_nombre(rng, L)] + [e008.tire_nombre(rng, int(rng.integers(1, 6)))
                                       for _ in range(2)]
    rng.shuffle(it)
    return tuple(int(x) for x in it)


def _emprunt(rng, L):
    a = int(rng.integers(1, 10)) * 10 ** (L - 1)
    return (a, e008.tire_nombre(rng, int(rng.integers(1, 6))))


def _egaux(rng, L):
    a = e008.tire_nombre(rng, L)
    return (a, a)


def _asym_sous(rng, L):
    return (e008.tire_nombre(rng, L), e008.tire_nombre(rng, int(rng.integers(1, 6))))


def jeu_val(tache):
    g = {"N1": 3313, "N2": 3323, "N3": 3333}[tache]
    return {"VAL-OOD": _uniformes(g, tache, VAL_LENS, N_VAL)}


def jeu_tid(tache):
    if tache == "N1":
        return e008.jeux_de_test()["T-ID"]
    return _uniformes({"N2": 3329, "N3": 3339}[tache], tache, ID_LENS, N_ID)


def jeux_test(tache):
    """TEST final (section 5) : {jeu: {L: [items]}}, deterministe, graines 3314-3339."""
    b = {"N1": 3314, "N2": 3324, "N3": 3334}[tache]
    longs = _uniformes(b, tache, LONG_LENS, N_LONG)
    longs.update(_uniformes(b + 1, tache, [L_MILLE], N_MILLE))
    out = {"T-ID": jeu_tid(tache), "T-LONG": longs}
    r = [np.random.default_rng(b + 2 + i) for i in range(4)]
    if tache == "N1":
        out["ADV-CASCADE"] = {L: D13._cascade(L, r[0]) for L in ADV_LENS}
        out["ADV-ZEROS"] = {L: D13._zeros(L, r[1]) for L in ADV_LENS}
        out["ADV-ASYM"] = {L: D13._asym(L, r[2]) for L in ADV_LENS}
        out["ADV-PROPAG"] = {L: _uniques(lambda: _propag(r[3], L), N_ADV,
                                         [(10 ** L - 1, 1), (5 * 10 ** (L - 1), 5 * 10 ** (L - 1))])
                             for L in ADV_LENS}
    elif tache == "N2":
        out["ADV-CASCADE3"] = {L: _uniques(lambda: _cascade3(r[0], L), N_ADV,
                                           [(10 ** L - 1,) * 3]) for L in ADV_LENS}
        out["ADV-PROPAG3"] = {L: _uniques(lambda: _propag3(r[1], L), N_ADV,
                                          [(10 ** L - 2, 1, 1)]) for L in ADV_LENS}
        out["ADV-ASYM3"] = {L: _uniques(lambda: _asym3(r[2], L), N_ADV) for L in ADV_LENS}
    else:
        out["ADV-EMPRUNT"] = {L: _uniques(lambda: _emprunt(r[0], L), N_ADV,
                                          [(10 ** (L - 1), 1), (10 ** L - 1, 10 ** L - 2)])
                              for L in ADV_LENS}
        out["ADV-EGAUX"] = {L: _uniques(lambda: _egaux(r[1], L), N_ADV) for L in ADV_LENS}
        out["ADV-ASYM"] = {L: _uniques(lambda: _asym_sous(r[2], L), N_ADV) for L in ADV_LENS}
    return out


# ---- flux d'entrainement (lots de 64, tires a neuf a chaque generation)
_EXCL = {}


def exclues(tache):
    if tache not in _EXCL:
        if tache == "N1":
            _EXCL[tache] = e008.paires_exclues()
        else:
            _EXCL[tache] = {it for its in jeu_tid(tache).values() for it in its}
    return _EXCL[tache]


def lot_train(tache, graine, g, n=64):
    if tache == "N1":
        return e008.paires_du_pas(graine, g, exclues("N1"), n)
    rng = np.random.default_rng([{"N2": 50_000, "N3": 60_000}[tache] + graine, g])
    ex, out = exclues(tache), []
    while len(out) < n:
        it = _item(rng, tache, 1, 5)
        if it not in ex:
            out.append(it)
    return out


# ------------------------------------------------------------------ evaluateur (E008 generalise)
def evaluer(systeme, jeux, nom, tache):
    """Comme evaluate.evaluer d'E008 (memes champs), avec la reference de la tache."""
    recs = []
    for jeu, par_l in jeux.items():
        for L, items in sorted(par_l.items()):
            preds = systeme(items)
            assert len(preds) == len(items)
            for it, (rep, conf) in zip(items, preds):
                att = reference(tache, it)
                recs.append({"systeme": nom, "jeu": jeu, "L": L, "item": list(it),
                             "attendu": att, "rep": rep, "juste": rep == att,
                             "conf": float(conf),
                             "chaine": e008.chaine_retenue(*it) if tache == "N1" else 0})
    return recs


def exact_par_jeu(recs):
    agg = defaultdict(lambda: [0, 0])
    for r in recs:
        k = f"{r['jeu']}|{r['L']}"
        agg[k][0] += int(r["juste"])
        agg[k][1] += 1
    return {k: v[0] / v[1] for k, v in agg.items()}
