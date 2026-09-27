"""E013 -- modeles MLX : I1 (accumulateur aligne) et I2 (accumulateur + lecture apprise).

Etat transmis d'un pas a l'autre : h de taille H (1 a 8). Couche locale de largeur F = 32,
identique a chaque pas. Rien d'autre ne passe d'un pas au suivant (I2 : + les deux pointeurs).
"""
import mlx.core as mx
import mlx.nn as nn

from donnees import VIDE, VOCAB_PLAT

F = 32
D_PLAT = 8


class Cellule(nn.Module):
    """z = relu(W1 [x ; h]) ; h' = tanh(Wh z) ; logits = Wo z."""

    def __init__(self, d_in, H, n_extra=0):
        super().__init__()
        self.H = H
        self.l1 = nn.Linear(d_in + H, F)
        self.lh = nn.Linear(F, H)
        self.lo = nn.Linear(F, 10 + n_extra)

    def __call__(self, x, h):
        z = nn.relu(self.l1(mx.concatenate([x, h], axis=-1)))
        return mx.tanh(self.lh(z)), self.lo(z)


class I1(nn.Module):
    def __init__(self, H):
        super().__init__()
        self.H = H
        self.cell = Cellule(22, H)

    def __call__(self, A, B, garder_etats=False, eval_tous=0):
        """A, B : (n, T) int. Renvoie logits (n, T, 10) [et etats (n, T, H)]."""
        n, T = A.shape
        x = mx.concatenate([mx.eye(11)[A], mx.eye(11)[B]], axis=-1)
        h = mx.zeros((n, self.H))
        logits, etats = [], []
        for t in range(T):
            h, lg = self.cell(x[:, t], h)
            logits.append(lg)
            if garder_etats:
                etats.append(h)
            if eval_tous and (t + 1) % eval_tous == 0:
                mx.eval(h, logits, etats)
        out = mx.stack(logits, axis=1)
        return (out, mx.stack(etats, axis=1)) if garder_etats else out


def _decale(p, w):
    """p (n, P) ; w (n, 3) = poids des decalages (-1 gauche, 0, +1 droite).
    La masse qui sort a gauche reste en 0 ; celle qui sort a droite reste en P-1."""
    z = mx.zeros_like(p[:, :1])
    gauche = mx.concatenate([p[:, 1:], z], axis=1)            # recoit de i+1
    gauche = gauche + mx.concatenate([p[:, :1], mx.zeros_like(p[:, 1:])], axis=1)
    droite = mx.concatenate([z, p[:, :-1]], axis=1)           # recoit de i-1
    droite = droite + mx.concatenate([mx.zeros_like(p[:, 1:]), p[:, -1:]], axis=1)
    return w[:, 0:1] * gauche + w[:, 1:2] * p + w[:, 2:3] * droite


class I2(nn.Module):
    def __init__(self, H=8):
        super().__init__()
        self.H = H
        self.emb = nn.Embedding(VOCAB_PLAT, D_PLAT)
        self.cle = nn.Linear(3 * D_PLAT, D_PLAT)
        self.q = mx.random.normal((2, D_PLAT))
        self.g = mx.zeros((2,))
        self.cell = Cellule(2 * D_PLAT, H, n_extra=6)

    def __call__(self, S, T, garder_etats=False, eval_tous=0):
        n, P = S.shape
        E = self.emb(S)                                           # (n, P, D)
        z = mx.zeros_like(E[:, :1])
        ctx = mx.concatenate([mx.concatenate([z, E[:, :-1]], 1), E,
                              mx.concatenate([E[:, 1:], z], 1)], axis=-1)
        K = self.cle(ctx)                                         # (n, P, D)
        masque = (S == VIDE)
        ptr = []
        for k in range(2):
            sc = (K @ self.q[k]) / (D_PLAT ** 0.5)
            ptr.append(mx.softmax(mx.where(masque, -1e9, sc), axis=-1))
        gam = 1.0 + nn.softplus(self.g)
        h = mx.zeros((n, self.H))
        logits, etats, pos = [], [], []
        for t in range(T):
            lus = [mx.sum(p[:, :, None] * E, axis=1) for p in ptr]
            h, sortie = self.cell(mx.concatenate(lus, axis=-1), h)
            logits.append(sortie[:, :10])
            if garder_etats:
                etats.append(h)
                pos.append(mx.stack([mx.argmax(p, axis=-1) for p in ptr], axis=-1))
            nouv = []
            for k in range(2):
                w = mx.softmax(sortie[:, 10 + 3 * k: 13 + 3 * k], axis=-1)
                p = _decale(ptr[k], w) + 1e-12
                p = p ** gam[k]
                nouv.append(p / mx.sum(p, axis=-1, keepdims=True))
            ptr = nouv
            if eval_tous and (t + 1) % eval_tous == 0:
                mx.eval(h, ptr, logits)
        out = mx.stack(logits, axis=1)
        if garder_etats:
            return out, mx.stack(etats, axis=1), mx.stack(pos, axis=1)
        return out


def nb_parametres(m):
    from mlx.utils import tree_flatten
    return sum(v.size for _, v in tree_flatten(m.parameters()))


def perte(m, entree, Y, M, T):
    logits = m(*entree, T) if isinstance(m, I2) else m(*entree)
    ce = nn.losses.cross_entropy(logits, Y, reduction="none")
    return (ce * M).sum() / M.sum()
