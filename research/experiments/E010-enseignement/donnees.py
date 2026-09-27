"""E010 -- donnees : formats F0-F3, reserves d'exemples uniques, jeux de validation/test.

Fige par PREREGISTREMENT.md (sections 2 et 3). Reutilise E008 par import (sans le modifier).
"""
import json
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
E008 = os.path.join(os.path.dirname(ICI), "E008-addition")
if E008 not in sys.path:
    sys.path.append(E008)

from data import jeux_de_test, paires_exclues, tire_nombre  # noqa: E402  (E008)

# ---------------------------------------------------------------- vocabulaire
PLUS, EGAL, FIN, PAD, SEP, DIESE = 10, 11, 12, 13, 14, 15
MOTS_REGLE = ("on additionne colonne par colonne depuis la droite , "
              "on reporte 1 si ≥ 10 .").split()
MOTS = sorted(set(MOTS_REGLE), key=MOTS_REGLE.index)
ID_MOT = {m: 16 + i for i, m in enumerate(MOTS)}
REGLE = [ID_MOT[m] for m in MOTS_REGLE]
VOCAB = 16 + len(MOTS)
SYMB = {**{i: str(i) for i in range(10)}, PLUS: "+", EGAL: "=", FIN: "$", PAD: "_",
        SEP: ";", DIESE: "#", **{v: f"<{k}>" for k, v in ID_MOT.items()}}

FORMATS = ("F0", "F1", "F2", "F3")
BATCH = 256
TRAIN_LMIN, TRAIN_LMAX = 1, 5


# ---------------------------------------------------------------- encodage
def encode_prompt(a, b, fmt):
    p = [int(c) for c in str(a)] + [PLUS] + [int(c) for c in str(b)] + [EGAL]
    return (REGLE + p) if fmt == "F2" else p


def trace(a, b):
    """Brouillon F1/F3 : par colonne (unites d'abord) a_i b_i c_i s_i c_{i+1} ;"""
    sa, sb = str(a)[::-1], str(b)[::-1]
    out, r = [], 0
    for i in range(max(len(sa), len(sb))):
        da = int(sa[i]) if i < len(sa) else 0
        db = int(sb[i]) if i < len(sb) else 0
        s = da + db + r
        out += [da, db, r, s % 10, s // 10, SEP]
        r = s // 10
    return out


def cible(a, b, fmt):
    """Tokens a predire apres le prompt (brouillon eventuel + reponse + fin)."""
    s = [int(c) for c in str(a + b)]
    if fmt in ("F0", "F2"):
        return s + [FIN]
    rep = s[::-1] if fmt == "F3" else s
    return trace(a, b) + [DIESE] + rep + [FIN]


def seq_train(fmt):
    """Longueur (entree) maximale a l'entrainement : 5 + 5 chiffres."""
    return len(encode_prompt(99999, 99999, fmt)) + len(cible(99999, 99999, fmt)) - 1


def n_gen_max(la, lb, fmt):
    m = max(la, lb)
    return m + 2 if fmt in ("F0", "F2") else 6 * (m + 1) + m + 3


def lit_sortie(toks, fmt):
    """Tokens generes -> (reponse canonique | None, indice du debut de la reponse | None)."""
    if FIN not in toks:
        return None, None
    fin = toks.index(FIN)
    if fmt in ("F0", "F2"):
        debut = 0
    else:
        if DIESE not in toks[:fin]:
            return None, None
        debut = toks.index(DIESE) + 1
    corps = toks[debut:fin]
    if not corps or any(t > 9 for t in corps):
        return None, debut
    s = "".join(str(t) for t in corps)
    return (s[::-1] if fmt == "F3" else s), debut


# ---------------------------------------------------------------- reserves d'entrainement
_CACHE = {}


def reserve(graine, n):
    """Les n premieres paires distinctes (hors paires exclues E008) de la graine."""
    cle = graine
    if cle not in _CACHE or len(_CACHE[cle]) < n:
        ex = paires_exclues()
        rng = np.random.default_rng([30_000 + graine])
        vus, out = set(), []
        while len(out) < n:
            m = 100_000  # blocs de taille fixe : reserves emboitees quel que soit n
            la = rng.integers(TRAIN_LMIN, TRAIN_LMAX + 1, m)
            lb = rng.integers(TRAIN_LMIN, TRAIN_LMAX + 1, m)
            lo_a = np.where(la == 1, 0, 10 ** (la - 1))
            lo_b = np.where(lb == 1, 0, 10 ** (lb - 1))
            a = rng.integers(lo_a, 10 ** la)
            b = rng.integers(lo_b, 10 ** lb)
            for p in zip(a.tolist(), b.tolist()):
                if p in vus or p in ex:
                    continue
                vus.add(p)
                out.append(p)
                if len(out) == n:
                    break
        _CACHE[cle] = out
    return _CACHE[cle][:n]


def indices_du_pas(graine, n, pas, batch=BATCH):
    """Indices dans la reserve (taille n) des exemples du pas `pas` (epoques permutees)."""
    debut = pas * batch
    idx = []
    while len(idx) < batch:
        e, k = divmod(debut + len(idx), n)
        perm = np.random.default_rng([40_000 + graine, n, e]).permutation(n)
        idx += perm[k: k + batch - len(idx)].tolist()
    return idx


def paires_du_pas(graine, n, pas, batch=BATCH):
    r = reserve(graine, n)
    return [r[i] for i in indices_du_pas(graine, n, pas, batch)]


def uniques_vus(n, pas, batch=BATCH):
    return min(n, pas * batch)


def lot(graine, n, pas, fmt, batch=BATCH):
    """(x, y, masque) numpy de forme (batch, seq_train(fmt))."""
    T = seq_train(fmt) + 1
    seq = np.full((batch, T), PAD, dtype=np.int32)
    masque = np.zeros((batch, T - 1), dtype=np.float32)
    for i, (a, b) in enumerate(paires_du_pas(graine, n, pas, batch)):
        p, c = encode_prompt(a, b, fmt), cible(a, b, fmt)
        e = p + c
        seq[i, : len(e)] = e
        masque[i, len(p) - 1: len(e) - 1] = 1.0
    return seq[:, :-1], seq[:, 1:], masque


# ---------------------------------------------------------------- jeux
FIN_LENS = [10, 16, 32, 64, 100]
N_FIN, N_ADV = 200, 20
GRAINE_FIN, GRAINE_ADV = 2030, 2031


def _t_fin():
    rng = np.random.default_rng(GRAINE_FIN)
    jeux = {}
    for L in FIN_LENS:
        vus, items = set(), []
        while len(items) < N_FIN:
            p = (tire_nombre(rng, L), tire_nombre(rng, L))
            if p not in vus:
                vus.add(p)
                items.append(p)
        jeux[L] = items
    return jeux


def _t_adv():
    rng = np.random.default_rng(GRAINE_ADV)
    casc, zeros, asym = {}, {}, {}
    for L in FIN_LENS:
        neuf = int("9" * L)
        c = [(neuf, 1), (1, neuf)]
        while len(c) < N_ADV:
            j = int(rng.integers(1, 4))
            bas = int(rng.integers(0, 10 ** j))
            a = int("9" * (L - j) + str(bas).zfill(j))
            if bas == 0:
                continue
            b = int(rng.integers(10 ** j - bas, 10 ** j))  # a_bas + b >= 10^j : retenue
            p = (a, b) if len(c) % 2 == 0 else (b, a)
            if p not in c:
                c.append(p)
        casc[L] = c
        base = 10 ** (L - 1)
        z = [(base + 2, base + 3)]
        while len(z) < N_ADV:
            p = (base + int(rng.integers(1, 100)), base + int(rng.integers(1, 100)))
            if p not in z:
                z.append(p)
        zeros[L] = z
        s = []
        while len(s) < N_ADV:
            a, b = tire_nombre(rng, L), tire_nombre(rng, 3)
            p = (a, b) if len(s) % 2 == 0 else (b, a)
            if p not in s:
                s.append(p)
        asym[L] = s
    return {"ADV-CASCADE": casc, "ADV-ZEROS": zeros, "ADV-ASYM": asym}


def jeux_e010(n_id=500, final=False):
    """{nom: {L: [(a, b)]}}. Criblage : n_id=200, final=False. Test final : final=True."""
    e8 = jeux_de_test()
    j = {"T-ID1": e8["T-ID1"],
         "T-ID": {L: v[:n_id] for L, v in e8["T-ID"].items()},
         "V-OOD": {L: e8["T-OOD"][L][:n_id] for L in (6, 7, 8)}}
    if final:
        j["T-FIN"] = _t_fin()
        j.update(_t_adv())
    return j


def lire_json(chemin):
    with open(chemin) as f:
        return json.load(f)


def ecrire_json(obj, chemin):
    with open(chemin, "w") as f:
        json.dump(obj, f, indent=1, ensure_ascii=False)
