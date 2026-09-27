"""E016 -- population de « mouches » : 3 lecteurs E014 geles (A), 3 accumulateurs I1 d'E013 geles (B),
codes prives (permutations), canal de V symboles sans sens, emetteurs/recepteurs tabulaires appris
par REINFORCE. Fige par PREREGISTREMENT.md sections 1-3.

Seules les tables E (emetteurs, nA x 11 x V) et R (recepteurs, nB x V x 11) apprennent.
"""
import hashlib
import os
import sys

import mlx.core as mx
import mlx.nn as nn
import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
E014 = os.path.join(os.path.dirname(ICI), "E014-reperage")
if E014 not in sys.path:
    sys.path.insert(0, E014)

import d14 as D  # noqa: E402  (E014, inchange ; ajoute E013 et E008 au chemin)
from m14 import Lecteur  # noqa: E402
from modeles import I1  # noqa: E402

V = 48          # symboles du canal
K = 11          # sens : chiffres 0-9 + absent
LECTEURS = (1, 3, 4)   # A1, A2, A3 = R1L-s1, s3, s4 (E014)
I1S = (1, 2, 3)        # B1, B2, B3 = I1 H = 4 graines 1, 2, 3 (E013)
CACHE = os.path.join(ICI, "runs", "cache")


def charge_lecteur(s):
    m = Lecteur(8)
    m.load_weights(os.path.join(ICI, "lecteurs_e014", f"R1L-s{s}.safetensors"))
    m.freeze()
    mx.eval(m.parameters())
    return m


def charge_i1(s):
    m = I1(4)
    m.load_weights(os.path.join(E014, "i1_e013", f"I1-H4-s{s}.safetensors"))
    m.freeze()
    mx.eval(m.parameters())
    return m


def codes_prives(graine, n):
    """n permutations de 11 toutes distinctes (rng 16 000 + graine) : A d'abord, puis B."""
    rng = np.random.default_rng(16_000 + graine)
    out = []
    while len(out) < n:
        p = rng.permutation(K)
        if not any((p == q).all() for q in out):
            out.append(p)
    return out


class Tables(nn.Module):
    def __init__(self, nA, nB):
        super().__init__()
        self.E = mx.zeros((nA, K, V))
        self.R = mx.zeros((nB, V, K))


# ------------------------------------------------------------------ lecture (A, geles)
def _cle(s, paires):
    h = hashlib.sha1(repr(paires).encode()).hexdigest()[:16]
    return os.path.join(CACHE, f"R1L-s{s}-{h}.npy")


def lit(lecteur, paires, T):
    """Classes lues (n, T, 2) int32 (0-9 / 10 absent), argmax du lecteur gele."""
    S = mx.array(D.encode_plat(paires))
    lu = lecteur(S, T, eval_tous=64 if T > 64 else 0)
    c = mx.stack([mx.argmax(lu[..., :11], -1), mx.argmax(lu[..., 11:], -1)], -1)
    return np.array(c).astype(np.int32)


def lit_cache(s, lecteur, paires):
    """Lecture groupee par n_pas, mise en cache disque (jeux d'evaluation fixes)."""
    f = _cle(s, paires)
    if os.path.exists(f):
        return np.load(f, allow_pickle=True)
    out = np.empty(len(paires), dtype=object)
    for n, idx in _groupes(paires):
        c = lit(lecteur, [paires[i] for i in idx], n)
        for k, i in enumerate(idx):
            out[i] = c[k]
    os.makedirs(CACHE, exist_ok=True)
    np.save(f, out, allow_pickle=True)
    return out


def _groupes(paires, taille=400):
    g = {}
    for i, (a, b) in enumerate(paires):
        g.setdefault(D.n_pas(a, b), []).append(i)
    for n, idx in sorted(g.items()):
        for k in range(0, len(idx), taille):
            yield n, idx[k: k + taille]


# ------------------------------------------------------------------ population
class Population:
    """Agents geles + codes prives + tables apprises. `coupe` : le recepteur recoit toujours 0."""

    def __init__(self, graine, lecteurs=LECTEURS, i1s=I1S, coupe=False):
        self.graine, self.coupe = graine, coupe
        self.id_lect, self.id_i1 = tuple(lecteurs), tuple(i1s)
        self.lecteurs = [charge_lecteur(s) for s in lecteurs]
        self.i1 = [charge_i1(s) for s in i1s]
        c = codes_prives(graine, len(lecteurs) + len(i1s))
        self.pi = [np.asarray(p) for p in c[: len(lecteurs)]]          # A_i : classe -> jeton prive
        self.sigma = [np.asarray(p) for p in c[len(lecteurs):]]        # B_j : classe -> jeton prive
        self.sigma_inv = [np.argsort(p) for p in self.sigma]           # jeton prive B_j -> classe
        self.t = Tables(len(lecteurs), len(i1s))
        mx.eval(self.t.parameters())

    @property
    def nA(self):
        return len(self.lecteurs)

    @property
    def nB(self):
        return len(self.i1)

    def interface_donnee(self, force=20.0):
        """Temoin DONNE : A_i emet le symbole = la classe ; B_j la traduit dans son code."""
        E = np.full((self.nA, K, V), -force, np.float32)
        R = np.full((self.nB, V, K), -force, np.float32)
        for i, p in enumerate(self.pi):
            for d in range(K):
                E[i, p[d], d] = force
        for j, s in enumerate(self.sigma):
            for d in range(K):
                R[j, d, s[d]] = force
        self.t.E, self.t.R = mx.array(E), mx.array(R)

    def lexique(self):
        """lex[i][d] = symbole argmax emis par A_i pour le sens d ; dec[j][s] = sens compris par B_j."""
        E, R = np.array(self.t.E), np.array(self.t.R)
        lex = [[int(E[i, self.pi[i][d]].argmax()) for d in range(K)] for i in range(self.nA)]
        dec = [[int(self.sigma_inv[j][R[j, s].argmax()]) for s in range(V)] for j in range(self.nB)]
        return lex, dec

    def indice_commun(self):
        lex, _ = self.lexique()
        return sum(len({lex[i][d] for i in range(self.nA)}) == 1 for d in range(K))

    # ------------------------------------------------------------ evaluation (argmax partout)
    def repond(self, i, j, classes, n):
        """classes (m, n, 2) lues par A_i -> (chiffres (m, n), confiance (m,))."""
        E, R = self.t.E[i], self.t.R[j]
        tok = self.pi[i][classes]                                       # jetons prives de A_i
        pE = mx.softmax(E[mx.array(tok)], -1)                           # (m, n, 2, V)
        sym = mx.argmax(pE, -1)
        if self.coupe:
            sym = mx.zeros_like(sym)
        pR = mx.softmax(R[sym], -1)                                     # (m, n, 2, K)
        rec = mx.argmax(pR, -1)
        cl = mx.array(self.sigma_inv[j])[rec]                           # classe vue par I1
        lg = self.i1[j](cl[..., 0], cl[..., 1], eval_tous=64 if n > 64 else 0)
        pI = mx.softmax(lg.astype(mx.float32), -1)
        conf = mx.minimum(mx.min(mx.max(pE, -1), -1), mx.min(mx.max(pR, -1), -1))
        conf = mx.min(mx.minimum(conf, mx.max(pI, -1)), -1)
        return np.array(mx.argmax(pI, -1)), np.array(conf).astype(np.float64)

    def systeme(self, i, j, cache=True):
        """Systeme au format de l'evaluateur E008 pour la paire (A_i, B_j)."""
        def f(paires):
            if cache:
                lus = lit_cache(self.id_lect[i], self.lecteurs[i], paires)
            out = [None] * len(paires)
            for n, idx in _groupes(paires):
                if cache:
                    cl = np.stack([lus[k] for k in idx])
                else:
                    cl = lit(self.lecteurs[i], [paires[k] for k in idx], n)
                dig, conf = self.repond(i, j, cl, n)
                for q, k in enumerate(idx):
                    out[k] = (D.decode(dig[q, :n]), float(conf[q]))
            return out
        return f


# ------------------------------------------------------------------ un pas de REINFORCE
def echantillonne(pop, items, cl, cle):
    """items : liste (i, j) ; cl (n, T, 2) classes lues. Renvoie actions et chiffres emis."""
    n, T = cl.shape[:2]
    I = np.array([it[0] for it in items])
    J = np.array([it[1] for it in items])
    tok = np.stack([pop.pi[i][cl[q]] for q, i in enumerate(I)])       # (n, T, 2)
    k1, k2 = mx.random.split(cle)
    logE = pop.t.E[mx.array(I)[:, None, None], mx.array(tok)]          # (n, T, 2, V)
    sym = mx.random.categorical(logE, key=k1)
    vu = mx.zeros_like(sym) if pop.coupe else sym
    logR = pop.t.R[mx.array(J)[:, None, None], vu]                     # (n, T, 2, K)
    rec = mx.random.categorical(logR, key=k2)
    rec_np = np.array(rec)
    dig = np.zeros((n, T), np.int32)
    for j in range(pop.nB):
        q = np.where(J == j)[0]
        if len(q) == 0:
            continue
        clB = pop.sigma_inv[j][rec_np[q]]
        lg = pop.i1[j](mx.array(clB[..., 0]), mx.array(clB[..., 1]))
        dig[q] = np.array(mx.argmax(lg, -1))
    return dict(I=I, J=J, tok=tok, sym=np.array(sym), vu=np.array(vu), rec=rec_np), dig


def perte_reinforce(tables, act, avantage, masque, beta):
    """-(R - b) * somme des log-probas des choix + (-beta) * entropie ; masque (n, T)."""
    I, J = mx.array(act["I"]), mx.array(act["J"])
    logE = tables.E[I[:, None, None], mx.array(act["tok"])]
    logR = tables.R[J[:, None, None], mx.array(act["vu"])]
    lpE = nn.log_softmax(logE, -1)
    lpR = nn.log_softmax(logR, -1)
    lp = (mx.take_along_axis(lpE, mx.array(act["sym"])[..., None], -1)[..., 0]
          + mx.take_along_axis(lpR, mx.array(act["rec"])[..., None], -1)[..., 0]).sum(-1)
    ent = (-(mx.exp(lpE) * lpE).sum(-1) - (mx.exp(lpR) * lpR).sum(-1)).sum(-1)
    M = mx.array(masque)
    A = mx.array(avantage)[:, None]
    return -((A * lp + beta * ent) * M).sum() / M.shape[0]
