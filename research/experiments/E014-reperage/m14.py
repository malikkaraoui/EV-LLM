"""E014 -- modeles MLX : R2 (pointeurs durs), Lecteur (R1a), Composition (R1-gel / R1-joint).

R0a/R0b utilisent `modeles.I2` d'E013 tel quel. `boucle` reproduit exactement la boucle de
lecture d'I2 (verifie par test) et ajoute le mode dur (straight-through : aller one-hot exact,
retour par le gradient de la version douce).
"""
import mlx.core as mx
import mlx.nn as nn

import d14  # noqa: F401  (chemins E013/E008)
from donnees import VIDE
from modeles import D_PLAT, I1, I2, Cellule, _decale

N_LU = 22  # lecteur : 11 classes pour a_t + 11 pour b_t (0-9, absent)


def _dur(p):
    """Straight-through : aller = one-hot de l'argmax, retour = gradient de p."""
    idx = mx.argmax(p, axis=-1)
    h = (mx.arange(p.shape[-1])[None, :] == idx[:, None]).astype(p.dtype)
    return p + mx.stop_gradient(h - p)


def boucle(m, S, T, n_sortie, dur=False, garder_pos=False, eval_tous=0):
    """Boucle de lecture d'I2 (2 tetes). Renvoie sorties (n, T, n_sortie) [, positions (n, T, 2)]."""
    E = m.emb(S)
    z = mx.zeros_like(E[:, :1])
    ctx = mx.concatenate([mx.concatenate([z, E[:, :-1]], 1), E,
                          mx.concatenate([E[:, 1:], z], 1)], axis=-1)
    K = m.cle(ctx)
    masque = (S == VIDE)
    ptr = []
    for k in range(2):
        sc = (K @ m.q[k]) / (D_PLAT ** 0.5)
        p = mx.softmax(mx.where(masque, -1e9, sc), axis=-1)
        ptr.append(_dur(p) if dur else p)
    gam = 1.0 + nn.softplus(m.g)
    h = mx.zeros((S.shape[0], m.H))
    sorties, pos = [], []
    for t in range(T):
        if garder_pos:
            pos.append(mx.stack([mx.argmax(p, axis=-1) for p in ptr], axis=-1))
        lus = [mx.sum(p[:, :, None] * E, axis=1) for p in ptr]
        h, s = m.cell(mx.concatenate(lus, axis=-1), h)
        sorties.append(s[:, :n_sortie])
        nouv = []
        for k in range(2):
            w = mx.softmax(s[:, n_sortie + 3 * k: n_sortie + 3 + 3 * k], axis=-1)
            if dur:
                nouv.append(_decale(ptr[k], _dur(w)))
            else:
                p = _decale(ptr[k], w) + 1e-12
                p = p ** gam[k]
                nouv.append(p / mx.sum(p, axis=-1, keepdims=True))
        ptr = nouv
        if eval_tous and (t + 1) % eval_tous == 0:
            mx.eval(h, ptr, sorties)
    out = mx.stack(sorties, axis=1)
    return (out, mx.stack(pos, axis=1)) if garder_pos else out


class R2(I2):
    """I2 d'E013 a pointeurs durs (un entier par tete, decalages -1/0/+1 exacts)."""

    def __call__(self, S, T, eval_tous=0):
        return boucle(self, S, T, 10, dur=True, eval_tous=eval_tous)


class Lecteur(I2):
    """Memes tetes qu'I2 ; la cellule emet la paire alignee (a_t, b_t) + les decalages."""

    def __init__(self, H=8):
        super().__init__(H)
        self.cell = Cellule(2 * D_PLAT, H, n_extra=N_LU - 10 + 6)

    def __call__(self, S, T, garder_pos=False, eval_tous=0):
        return boucle(self, S, T, N_LU, garder_pos=garder_pos, eval_tous=eval_tous)


class Composition(nn.Module):
    """Lecteur -> probabilites (11 + 11) -> cellule de l'I1 H = 4 d'E013 (a la place des one-hot)."""

    def __init__(self):
        super().__init__()
        self.lecteur = Lecteur(8)
        self.i1 = I1(4)

    def __call__(self, S, T, avec_lecture=False, eval_tous=0):
        lu = self.lecteur(S, T, eval_tous=eval_tous)
        out = accumule(self.i1, lu, eval_tous)
        return (out, lu) if avec_lecture else out


def accumule(i1, lu, eval_tous=0):
    """Interface de composition : logits de lecture (n, T, 22) -> probabilites -> cellule I1."""
    x = mx.concatenate([mx.softmax(lu[..., :11], axis=-1),
                        mx.softmax(lu[..., 11:], axis=-1)], axis=-1)
    h = mx.zeros((lu.shape[0], i1.H))
    logits = []
    for t in range(lu.shape[1]):
        h, lg = i1.cell(x[:, t], h)
        logits.append(lg)
        if eval_tous and (t + 1) % eval_tous == 0:
            mx.eval(h, logits)
    return mx.stack(logits, axis=1)


def perte_addition(m, S, Y, M, T):
    ce = nn.losses.cross_entropy(m(S, T), Y, reduction="none")
    return (ce * M).sum() / M.sum()


def perte_lecture(m, S, A, B, M, T):
    lu = m(S, T)
    ce = (nn.losses.cross_entropy(lu[..., :11], A, reduction="none")
          + nn.losses.cross_entropy(lu[..., 11:], B, reduction="none"))
    return (ce * M).sum() / (2 * M.sum())
