"""E009 -- architectures A1 (Neural GPU), A2 / A2-L (Deep Thinking), A3 / A3-T (Looped NoPE).

Interface commune : etat0(x) -> (h, ctx) ; iterer(h, ctx) -> h ; lire(h) -> logits (B, L, VOCAB).
Aucune position, aucun alignement : entree = bande plate (bande.py).
"""
import mlx.core as mx
import mlx.nn as nn
import numpy as np

from bande import VOCAB
from model import Bloc  # E008 : bloc pre-LN (attention + FFN)

W = 128


# ---------------------------------------------------------------- A1 Neural GPU
class CGRU(nn.Module):
    def __init__(self, w):
        super().__init__()
        self.ur = nn.Conv1d(w, 2 * w, 3, padding=1)
        self.c = nn.Conv1d(w, w, 3, padding=1)

    def __call__(self, h):
        u, r = mx.split(mx.sigmoid(self.ur(h)), 2, axis=-1)
        return u * h + (1 - u) * mx.tanh(self.c(r * h))


class NeuralGPU(nn.Module):
    def __init__(self, w=W):
        super().__init__()
        self.emb = nn.Embedding(VOCAB, w)
        self.g1, self.g2 = CGRU(w), CGRU(w)
        self.tete = nn.Linear(w, VOCAB)

    def etat0(self, x):
        return self.emb(x), None

    def iterer(self, h, ctx):
        return self.g2(self.g1(h))

    def lire(self, h):
        return self.tete(h)


# ---------------------------------------------------------------- A2 Deep Thinking
_V0 = {}


def _vecteur0(dim):
    if dim not in _V0:
        v = np.random.default_rng(dim).standard_normal(dim).astype(np.float32)
        _V0[dim] = v / np.linalg.norm(v)
    return mx.array(_V0[dim])


def norme_spectrale(w, iters=20):
    """Norme spectrale de w vu comme (out, k*in) ; vecteurs de puissance sans gradient."""
    m = w.reshape(w.shape[0], -1)
    v = _vecteur0(m.shape[1])
    for _ in range(iters):
        u = m @ v
        u = u / (mx.linalg.norm(u) + 1e-12)
        v = m.T @ u
        v = v / (mx.linalg.norm(v) + 1e-12)
    u, v = mx.stop_gradient(u), mx.stop_gradient(v)
    return u @ (m @ v)


class ConvSN(nn.Module):
    """Conv1d k=3 dont le poids est divise par sa norme spectrale si `sn`."""

    def __init__(self, cin, cout, sn):
        super().__init__()
        self.conv = nn.Conv1d(cin, cout, 3, padding=1)
        self.sn = sn

    def poids(self):
        w = self.conv.weight
        return w / norme_spectrale(w) if self.sn else w

    def __call__(self, h, w=None):
        w = self.poids() if w is None else w
        return mx.conv1d(h, w, padding=1) + self.conv.bias


class DeepThinking(nn.Module):
    def __init__(self, lipschitz=False, w=W):
        super().__init__()
        self.lipschitz = lipschitz
        self.emb = nn.Embedding(VOCAB, w)
        self.proj = nn.Conv1d(w, w, 3, padding=1)
        self.entree = ConvSN(2 * w, w, lipschitz)
        self.res = [ConvSN(w, w, lipschitz) for _ in range(4)]
        self.t1 = nn.Conv1d(w, w, 3, padding=1)
        self.t2 = nn.Conv1d(w, w // 2, 3, padding=1)
        self.t3 = nn.Conv1d(w // 2, VOCAB, 3, padding=1)

    def act(self, z):
        return nn.elu(z) if self.lipschitz else nn.relu(z)

    def etat0(self, x):
        xt = self.proj(self.emb(x))
        poids = [self.entree.poids()] + [c.poids() for c in self.res]  # une fois par appel
        return mx.zeros_like(xt), (xt, poids)

    def iterer(self, h, ctx):
        xt, (w0, *wr) = ctx
        h = self.act(self.entree(mx.concatenate([h, xt], axis=-1), w0))  # recall
        for i in range(0, 4, 2):
            z = self.act(self.res[i](h, wr[i]))
            h = self.act(h + self.res[i + 1](z, wr[i + 1]))
        return h

    def lire(self, h):
        return self.t3(nn.relu(self.t2(nn.relu(self.t1(h)))))


# ---------------------------------------------------------------- A3 Looped transformer NoPE
class LoopedNoPE(nn.Module):
    def __init__(self, d=W, tetes=4, ffn=512):
        super().__init__()
        self.emb = nn.Embedding(VOCAB, d)
        self.bloc = Bloc(d, tetes, ffn)
        self.ln_f = nn.LayerNorm(d)
        self.tete = nn.Linear(d, VOCAB)

    def etat0(self, x):
        e = self.emb(x)
        T = x.shape[1]
        masque = nn.MultiHeadAttention.create_additive_causal_mask(T).astype(e.dtype)
        return mx.zeros_like(e), (e, masque)

    def iterer(self, h, ctx):
        e, masque = ctx
        return self.bloc(h + e, masque)  # injection de l'entree a chaque tour

    def lire(self, h):
        return self.tete(self.ln_f(h))


# ---------------------------------------------------------------- fabrique
SYSTEMES = {
    "A1": dict(regle="bande", fabrique=lambda: NeuralGPU()),
    "A2": dict(regle="confiance", fabrique=lambda: DeepThinking(False)),
    "A2-L": dict(regle="confiance", fabrique=lambda: DeepThinking(True)),
    "A3": dict(regle="confiance", fabrique=lambda: LoopedNoPE()),
    "A3-T": dict(regle="t_n", fabrique=lambda: LoopedNoPE()),
}
M_ENTRAINEMENT = 24  # iterations max a l'entrainement (perte progressive), fixe
PLAFOND_TEST = 512   # plafond fixe d'iterations au test (regle "confiance")


def nb_parametres(modele):
    from mlx.utils import tree_flatten
    return sum(v.size for _, v in tree_flatten(modele.parameters()))
