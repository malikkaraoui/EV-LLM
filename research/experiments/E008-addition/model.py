"""E008 -- petit transformer decoder-only (MLX), B-STD et B-REF.

B-STD : positions absolues apprises (table de MAX_POS positions).
B-REF : meme modele sans aucun embedding de position (NoPE).
"""
import mlx.core as mx
import mlx.nn as nn

from data import VOCAB

D, COUCHES, TETES, FFN = 256, 4, 4, 1024
MAX_POS = 64


class Bloc(nn.Module):
    def __init__(self, d, tetes, ffn):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = nn.MultiHeadAttention(d, tetes)
        self.ln2 = nn.LayerNorm(d)
        self.ff1 = nn.Linear(d, ffn)
        self.ff2 = nn.Linear(ffn, d)

    def __call__(self, x, masque):
        h = self.ln1(x)
        x = x + self.attn(h, h, h, mask=masque)
        return x + self.ff2(nn.gelu(self.ff1(self.ln2(x))))


class Additionneur(nn.Module):
    def __init__(self, positions, d=D, couches=COUCHES, tetes=TETES, ffn=FFN):
        super().__init__()
        self.positions = positions  # True : B-STD ; False : NoPE (B-REF)
        self.tok = nn.Embedding(VOCAB, d)
        if positions:
            self.pos = nn.Embedding(MAX_POS, d)
        self.blocs = [Bloc(d, tetes, ffn) for _ in range(couches)]
        self.ln_f = nn.LayerNorm(d)
        self.tete = nn.Linear(d, VOCAB)

    def __call__(self, x):
        T = x.shape[1]
        h = self.tok(x)
        if self.positions:
            if T > MAX_POS:
                raise ValueError(f"sequence de {T} > MAX_POS={MAX_POS}")
            h = h + self.pos(mx.arange(T))
        masque = nn.MultiHeadAttention.create_additive_causal_mask(T).astype(h.dtype)
        for b in self.blocs:
            h = b(h, masque)
        return self.tete(self.ln_f(h))


def nb_parametres(modele):
    from mlx.utils import tree_flatten
    return sum(v.size for _, v in tree_flatten(modele.parameters()))


def perte(modele, x, y, masque):
    logits = modele(x)
    ce = nn.losses.cross_entropy(logits, y, reduction="none")
    return (ce * masque).sum() / masque.sum()


def lr_schedule(lr_max, montee, pas_total, lr_min=1e-5):
    import mlx.optimizers as optim
    return optim.join_schedules(
        [optim.linear_schedule(0.0, lr_max, montee),
         optim.cosine_decay(lr_max, pas_total - montee, lr_min)],
        [montee],
    )

