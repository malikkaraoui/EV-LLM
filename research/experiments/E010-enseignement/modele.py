"""E010 -- meme petit transformer qu'E008 (pre-LN, d=256, 4 couches, 4 tetes, FFN 1024),
reecrit avec un cache cle/valeur pour decoder jusqu'a ~900 tokens (100 chiffres en F1).

positions=True : positions absolues apprises (MAX_POS lignes) ; False : NoPE.
"""
import math

import mlx.core as mx
import mlx.nn as nn
import mlx.optimizers as optim

from donnees import VOCAB

D, COUCHES, TETES, FFN = 256, 4, 4, 1024
MAX_POS = 1024


class Cache:
    """Cache cle/valeur pre-alloue par blocs (ecriture en place, comme mlx-lm)."""
    PAS = 256

    def __init__(self):
        self.k = self.v = None
        self.n = 0

    def ajoute(self, k, v):
        B, h, T, dh = k.shape
        if self.k is None or self.n + T > self.k.shape[2]:
            taille = ((self.n + T + self.PAS - 1) // self.PAS) * self.PAS
            nk, nv = mx.zeros((B, h, taille, dh), k.dtype), mx.zeros((B, h, taille, dh), v.dtype)
            if self.k is not None:
                nk[..., : self.n, :] = self.k[..., : self.n, :]
                nv[..., : self.n, :] = self.v[..., : self.n, :]
            self.k, self.v = nk, nv
        self.k[..., self.n: self.n + T, :] = k
        self.v[..., self.n: self.n + T, :] = v
        self.n += T
        return self.k[..., : self.n, :], self.v[..., : self.n, :]


class Attention(nn.Module):
    def __init__(self, d, tetes):
        super().__init__()
        self.tetes = tetes
        self.query_proj = nn.Linear(d, d, bias=False)
        self.key_proj = nn.Linear(d, d, bias=False)
        self.value_proj = nn.Linear(d, d, bias=False)
        self.out_proj = nn.Linear(d, d, bias=False)

    def __call__(self, x, masque=None, cache=None):
        B, T, d = x.shape
        h = self.tetes

        def tetes(z):
            return z.reshape(B, T, h, d // h).transpose(0, 2, 1, 3)

        q, k, v = tetes(self.query_proj(x)), tetes(self.key_proj(x)), tetes(self.value_proj(x))
        if cache is not None:
            k, v = cache.ajoute(k, v)
        o = mx.fast.scaled_dot_product_attention(q, k, v, scale=1 / math.sqrt(d // h),
                                                 mask=masque)
        return self.out_proj(o.transpose(0, 2, 1, 3).reshape(B, T, d))


class Bloc(nn.Module):
    def __init__(self, d, tetes, ffn):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = Attention(d, tetes)
        self.ln2 = nn.LayerNorm(d)
        self.ff1 = nn.Linear(d, ffn)
        self.ff2 = nn.Linear(ffn, d)

    def __call__(self, x, masque, cache=None):
        x = x + self.attn(self.ln1(x), masque, cache)
        return x + self.ff2(nn.gelu(self.ff1(self.ln2(x))))


class Additionneur(nn.Module):
    def __init__(self, positions, d=D, couches=COUCHES, tetes=TETES, ffn=FFN):
        super().__init__()
        self.positions = positions
        self.tok = nn.Embedding(VOCAB, d)
        if positions:
            self.pos = nn.Embedding(MAX_POS, d)
        self.blocs = [Bloc(d, tetes, ffn) for _ in range(couches)]
        self.ln_f = nn.LayerNorm(d)
        self.tete = nn.Linear(d, VOCAB)

    def __call__(self, x, caches=None, decalage=0):
        """x : (B, T). caches : un Cache par couche (decodage) ; decalage = tokens deja vus."""
        T = x.shape[1]
        h = self.tok(x)
        if self.positions:
            if decalage + T > MAX_POS:
                raise ValueError(f"position {decalage + T} > MAX_POS={MAX_POS}")
            h = h + self.pos(mx.arange(decalage, decalage + T))
        masque = None
        if T > 1:
            masque = nn.MultiHeadAttention.create_additive_causal_mask(T).astype(h.dtype)
            if decalage:
                masque = mx.concatenate([mx.zeros((T, decalage), h.dtype), masque], axis=1)
        for i, b in enumerate(self.blocs):
            h = b(h, masque, None if caches is None else caches[i])
        return self.tete(self.ln_f(h))


def nb_parametres(modele):
    from mlx.utils import tree_flatten
    return sum(v.size for _, v in tree_flatten(modele.parameters()))


def perte(modele, x, y, masque):
    ce = nn.losses.cross_entropy(modele(x), y, reduction="none")
    return (ce * masque).sum() / masque.sum()


def lr_schedule(lr_max, montee, pas_total, lr_min=1e-5):
    return optim.join_schedules(
        [optim.linear_schedule(0.0, lr_max, montee),
         optim.cosine_decay(lr_max, pas_total - montee, lr_min)],
        [montee],
    )
