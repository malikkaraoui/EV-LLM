"""E012 -- reseaux facon MDL-RNN (Lan 2022) : genome, execution, lecture, MDL, mutations, preuve.

Genome (dict) :
  nin    : nombre d'entrees (ids 0..nin-1) ; la sortie a l'id nin ; cachees : ids > nin
  cach   : liste ordonnee des ids caches (ordre topologique des connexions avant)
  act    : {id: activation} pour toute unite non-entree
  conns  : liste de (src, dst, rec, num, den) -- poids num/den, num signe != 0, den >= 1
  biais  : {id: (num, den)}
  suiv   : prochain id libre
"""
import math
from fractions import Fraction

import numpy as np

from jeux import RACINE_EXP  # noqa: F401  (chemins E008/E011)
from objectifs import bits_entier, bits_poids  # E011 (codage des poids de Lan)

ACTS = ["id", "relu", "sig", "tanh", "carre", "floor", "marche"]
EPS_BITS = 20.0          # -log2 p plafonne a 20 bits par chiffre
BORNE = 1e12             # saturation numerique des valeurs (garde-fou contre inf/nan)


# ---------------------------------------------------------------- genome
def vide(nin):
    return {"nin": nin, "cach": [], "act": {nin: "id"}, "conns": [], "biais": {}, "suiv": nin + 1}


def copie(g):
    return {"nin": g["nin"], "cach": list(g["cach"]), "act": dict(g["act"]),
            "conns": list(g["conns"]), "biais": dict(g["biais"]), "suiv": g["suiv"]}


def cle(g):
    """Empreinte canonique (renumerotation selon l'ordre)."""
    nin = g["nin"]
    ren = {i: i for i in range(nin + 1)}
    for k, u in enumerate(g["cach"]):
        ren[u] = nin + 1 + k
    return (nin, tuple(g["act"][u] for u in g["cach"]), g["act"][nin],
            tuple(sorted((ren[s], ren[d], r, n, q) for s, d, r, n, q in g["conns"])),
            tuple(sorted((ren[u], v) for u, v in g["biais"].items())))


def ordre(g):
    return list(g["cach"]) + [g["nin"]]


def taille(g):
    return {"cachees": len(g["cach"]), "connexions": len(g["conns"]), "biais": len(g["biais"])}


# ---------------------------------------------------------------- execution numpy
def _act(nom, z):
    if nom == "id":
        return z
    if nom == "relu":
        return np.maximum(z, 0.0)
    if nom == "sig":
        return 0.5 * (1.0 + np.tanh(0.5 * z))
    if nom == "tanh":
        return np.tanh(z)
    if nom == "carre":
        return z * z
    if nom == "floor":
        return np.floor(z)
    if nom == "marche":
        return (z > 0).astype(np.float64)
    raise ValueError(nom)


def compile_(g):
    nin = g["nin"]
    od = ordre(g)
    slot = {i: i for i in range(nin)}
    for k, u in enumerate(od):
        slot[u] = nin + k
    unites = []
    for u in od:
        b = g["biais"].get(u)
        fw = [(slot[s], n, q) for s, d, r, n, q in g["conns"] if d == u and not r]
        rc = [(slot[s] - nin, n, q) for s, d, r, n, q in g["conns"] if d == u and r]
        unites.append((g["act"][u], (b[0] / b[1]) if b else 0.0, fw, rc))
    return nin, unites


def execute(comp, X):
    """X (B, T, nin) -> sorties v (B, T)."""
    nin, unites = comp
    B, T, _ = X.shape
    nu = len(unites)
    prec = np.zeros((nu, B))
    V = np.empty((B, T))
    cour = np.empty((nin + nu, B))
    with np.errstate(all="ignore"):
        for t in range(T):
            cour[:nin] = X[:, t, :].T
            for k, (act, b, fw, rc) in enumerate(unites):
                z = np.full(B, b)
                for s, n, q in fw:
                    z = z + cour[s] * n / q
                for s, n, q in rc:
                    z = z + prec[s] * n / q
                y = _act(act, z)
                y = np.nan_to_num(y, nan=0.0, posinf=BORNE, neginf=-BORNE)
                cour[nin + k] = np.clip(y, -BORNE, BORNE)
            prec = cour[nin:].copy()
            V[:, t] = cour[nin + nu - 1]
    return V


def lecture(V, base):
    """Chiffre choisi (arrondi de clip(v)) et sa probabilite (interpolation lineaire)."""
    v = np.clip(V, 0.0, base - 1.0)
    choisi = np.floor(v + 0.5)
    conf = 1.0 - np.abs(v - choisi)
    return choisi.astype(np.int64), conf


def cout_donnees(V, Y, M, base):
    """|D : G| en bits et nb de chiffres faux (masques)."""
    v = np.clip(V, 0.0, base - 1.0)
    p = np.maximum(0.0, 1.0 - np.abs(v - Y))
    bits = np.where(p > 2.0 ** -EPS_BITS, -np.log2(np.maximum(p, 1e-300)), EPS_BITS)
    choisi, _ = lecture(V, base)
    return float(np.sum(bits * M)), int(np.sum((choisi != Y) * M))


def evalue(g, lots, base):
    """(|D:G|, chiffres faux, sequences exactes, n sequences)."""
    comp = compile_(g)
    dg, faux, exactes, n = 0.0, 0, 0, 0
    for X, Y, M, _ in lots:
        V = execute(comp, X)
        d, f = cout_donnees(V, Y, M, base)
        dg += d
        faux += f
        choisi, _ = lecture(V, base)
        exactes += int(np.sum(np.all((choisi == Y) | (M == 0), axis=1)))
        n += len(Y)
    return dg, faux, exactes, n


# ---------------------------------------------------------------- MDL
def longueur_G(g):
    nu = g["nin"] + 1 + len(g["cach"])
    bidx = max(1, math.ceil(math.log2(nu)))
    bits = bits_entier(len(g["cach"])) + 3 * (1 + len(g["cach"])) + bits_entier(len(g["conns"]))
    for s, d, r, n, q in g["conns"]:
        bits += 2 * bidx + 1 + bits_poids(n / q)
    for u in ordre(g):
        bits += 1
        if u in g["biais"]:
            n, q = g["biais"][u]
            bits += bits_poids(n / q)
    return bits


# ---------------------------------------------------------------- systeme au sens E008
def systeme(g, exp_cfg, encodeur):
    base, plat = exp_cfg["base"], exp_cfg["format"] == "plat"
    comp = compile_(g)

    def predire(paires):
        out = [None] * len(paires)
        for X, Y, M, idx in encodeur(paires):
            V = execute(comp, X)
            ch, cf = lecture(V, base)
            for j, i in enumerate(idx):
                m = M[j] > 0
                dig, conf = ch[j][m], float(np.prod(cf[j][m]))
                s = "".join(str(int(c)) for c in (dig if plat else dig[::-1]))
                out[i] = (str(int(s, base)), conf)
        return out

    return predire


# ---------------------------------------------------------------- circuit construit a la main
def circuit_main(base):
    """s = a + b + c(t-1) (id) ; c = floor(s / base) ; v = s - base * c."""
    g = vide(2)
    s, c = 3, 4
    g["cach"] = [s, c]
    g["act"].update({s: "id", c: "floor"})
    g["conns"] = [(0, s, False, 1, 1), (1, s, False, 1, 1), (c, s, True, 1, 1),
                  (s, c, False, 1, base), (s, 2, False, 1, 1), (c, 2, False, -base, 1)]
    g["suiv"] = 5
    return g


# ---------------------------------------------------------------- mutations
def _rationnel(rng):
    k = np.arange(1, 11)
    p = (1.0 / k) / np.sum(1.0 / k)
    n = int(rng.choice(k, p=p))
    q = int(rng.choice(k, p=p))
    n = -n if rng.random() < 0.5 else n
    d = math.gcd(n, q)
    return n // d, q // d


def _reduit(n, q):
    d = math.gcd(n, q)
    return n // d, q // d


def _avant_possibles(g, dst):
    """Sources admissibles d'une connexion avant vers dst (entrees + cachees plus tot)."""
    src = list(range(g["nin"]))
    for u in g["cach"]:
        if u == dst:
            break
        src.append(u)
    return src


def _non_entrees(g):
    return ordre(g)


def mute(g, rng):
    g = copie(g)
    op = int(rng.integers(0, 8))
    nin = g["nin"]
    if op == 0:  # ajouter une cachee
        u = g["suiv"]
        g["suiv"] += 1
        pos = int(rng.integers(0, len(g["cach"]) + 1))
        g["cach"].insert(pos, u)
        g["act"][u] = ACTS[int(rng.integers(0, len(ACTS)))]
        srcs = _avant_possibles(g, u)
        s = srcs[int(rng.integers(0, len(srcs)))]
        n, q = _rationnel(rng)
        g["conns"].append((s, u, False, n, q))
        apres = g["cach"][pos + 1:] + [nin]
        d = apres[int(rng.integers(0, len(apres)))]
        n, q = _rationnel(rng)
        g["conns"].append((u, d, False, n, q))
    elif op == 1:  # retirer une cachee
        if g["cach"]:
            u = g["cach"].pop(int(rng.integers(0, len(g["cach"]))))
            g["conns"] = [c for c in g["conns"] if c[0] != u and c[1] != u]
            g["act"].pop(u)
            g["biais"].pop(u, None)
    elif op in (2, 3):  # ajouter une connexion avant / recurrente
        nes = _non_entrees(g)
        d = nes[int(rng.integers(0, len(nes)))]
        srcs = _avant_possibles(g, d) if op == 2 else nes
        s = srcs[int(rng.integers(0, len(srcs)))]
        rec = op == 3
        if not any(c[0] == s and c[1] == d and c[2] == rec for c in g["conns"]):
            n, q = _rationnel(rng)
            g["conns"].append((s, d, rec, n, q))
    elif op == 4:  # retirer une connexion
        if g["conns"]:
            g["conns"].pop(int(rng.integers(0, len(g["conns"]))))
    elif op == 5:  # modifier un poids
        if g["conns"]:
            i = int(rng.integers(0, len(g["conns"])))
            s, d, r, n, q = g["conns"][i]
            n, q = _modifie(n, q, rng)
            if n == 0:
                g["conns"].pop(i)
            else:
                g["conns"][i] = (s, d, r, n, q)
    elif op == 6:  # biais
        nes = _non_entrees(g)
        u = nes[int(rng.integers(0, len(nes)))]
        if u not in g["biais"]:
            g["biais"][u] = _rationnel(rng)
        elif rng.random() < 1 / 3:
            g["biais"].pop(u)
        else:
            n, q = _modifie(*g["biais"][u], rng)
            if n == 0:
                g["biais"].pop(u)
            else:
                g["biais"][u] = (n, q)
    else:  # changer une activation
        nes = _non_entrees(g)
        u = nes[int(rng.integers(0, len(nes)))]
        g["act"][u] = ACTS[int(rng.integers(0, len(ACTS)))]
    return g


def _modifie(n, q, rng):
    k = int(rng.integers(0, 4))
    if k == 0:
        n = n + (1 if rng.random() < 0.5 else -1)
    elif k == 1:
        q = max(1, q + (1 if rng.random() < 0.5 else -1))
    elif k == 2:
        n = -n
    else:
        return _rationnel(rng)
    return _reduit(n, q) if n != 0 else (0, 1)


# ---------------------------------------------------------------- preuve (rationnels exacts)
ACTS_EXACTES = {"id", "relu", "carre", "floor", "marche"}


def _act_exacte(nom, z):
    if nom == "id":
        return z
    if nom == "relu":
        return max(z, Fraction(0))
    if nom == "carre":
        return z * z
    if nom == "floor":
        return Fraction(math.floor(z))
    return Fraction(1 if z > 0 else 0)


def preuve_aligne(g, base, max_etats=20000):
    """Automate produit (etat du reseau, vraie retenue) explore en rationnels exacts.

    Renvoie (statut, detail) ; statut in {"PROUVE", "FAUX", "NON_PROUVABLE", "NON_BORNE"}.
    Valable pour toute longueur : les chiffres absents valent 0, entree deja couverte.
    """
    if any(g["act"][u] not in ACTS_EXACTES for u in ordre(g)):
        return "NON_PROUVABLE", "activation non exacte (sig/tanh)"
    nin, unites = compile_(g)
    unites = [(a, Fraction(0) if b == 0 else _frac_biais(g, u), fw, rc)
              for u, (a, b, fw, rc) in zip(ordre(g), unites)]
    depart = (tuple(Fraction(0) for _ in unites), 0)
    vus, pile = {depart}, [depart]
    while pile:
        etat, r = pile.pop()
        for x in range(base):
            for y in range(base):
                cour = [Fraction(x), Fraction(y)]
                for act, b, fw, rc in unites:
                    z = b + sum((cour[s] * n / q for s, n, q in fw), Fraction(0))
                    z += sum((etat[s] * n / q for s, n, q in rc), Fraction(0))
                    cour.append(_act_exacte(act, z))
                v = min(max(cour[-1], Fraction(0)), Fraction(base - 1))
                chiffre = math.floor(v + Fraction(1, 2))
                tot = x + y + r
                if chiffre != tot % base:
                    return "FAUX", {"etat": [str(e) for e in etat], "retenue": r, "x": x, "y": y,
                                    "sortie": str(cour[-1])}
                suiv = (tuple(cour[nin:]), tot // base)
                if suiv not in vus:
                    vus.add(suiv)
                    if len(vus) > max_etats:
                        return "NON_BORNE", f"> {max_etats} etats"
                    pile.append(suiv)
    return "PROUVE", f"{len(vus)} etats atteignables, {len(vus) * base * base} transitions verifiees"


def _frac_biais(g, u):
    n, q = g["biais"][u]
    return Fraction(n, q)


def lisible(g):
    """Ecriture lisible du circuit."""
    nin = g["nin"]
    nom = {i: f"x{i}" for i in range(nin)}
    nom[nin] = "sortie"
    for k, u in enumerate(g["cach"]):
        nom[u] = f"h{k + 1}"
    lignes = []
    for u in ordre(g):
        termes = []
        if u in g["biais"]:
            termes.append(str(Fraction(*g["biais"][u])))
        for s, d, r, n, q in g["conns"]:
            if d == u:
                termes.append(f"{Fraction(n, q)}*{nom[s]}{'(t-1)' if r else ''}")
        lignes.append(f"{nom[u]} = {g['act'][u]}({' + '.join(termes) or '0'})")
    return lignes
