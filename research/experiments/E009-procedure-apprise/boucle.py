"""E009 -- boucle de calcul : pertes d'entrainement et prediction au test, par regle d'arret.

Regles (PREREGISTREMENT section 3) :
  "bande"     : T = longueur de la bande (A1) ;
  "confiance" : perte progressive (M fixe) ; au test t = 1..PLAFOND, sortie de confiance max ;
  "t_n"       : T(n) = max(la, lb) + 1 donne a l'entrainement et au test (A3-T).
"""
import mlx.core as mx
import mlx.nn as nn
import numpy as np

from archis import M_ENTRAINEMENT, PLAFOND_TEST


def ce(logits, y, m):
    l = nn.losses.cross_entropy(logits, y, reduction="none")
    return (l * m).sum() / m.sum()


def perte_bande(modele, x, y, m):
    h, ctx = modele.etat0(x)
    for _ in range(x.shape[1]):
        h = modele.iterer(h, ctx)
    return ce(modele.lire(h), y, m)


def perte_progressive(modele, x, y, m, n, k, M=M_ENTRAINEMENT):
    """1/2 perte apres M iterations + 1/2 perte apres n iterations sans gradient puis k avec."""
    h, ctx = modele.etat0(x)
    h_n = h
    for t in range(M):
        if t == n:
            h_n = h
        h = modele.iterer(h, ctx)
    l_max = ce(modele.lire(h), y, m)
    g = mx.stop_gradient(h_n)
    for _ in range(k):
        g = modele.iterer(g, ctx)
    return 0.5 * l_max + 0.5 * ce(modele.lire(g), y, m)


def perte_tn(modele, x, y, m, t_n):
    h, ctx = modele.etat0(x)
    sel = mx.zeros_like(h)
    for t in range(1, int(t_n.max().item()) + 1):
        h = modele.iterer(h, ctx)
        sel = mx.where((t_n == t)[:, None, None], h, sel)
    return ce(modele.lire(sel), y, m)


def tirage_progressif(graine, pas, M=M_ENTRAINEMENT):
    rng = np.random.default_rng([20_000 + graine, pas])
    n = int(rng.integers(0, M))
    k = int(rng.integers(1, M - n + 1))
    return n, k


# ---------------------------------------------------------------- prediction
def predire(modele, regle, x_np, t_n_np, plafond=PLAFOND_TEST):
    """Bandes de meme longueur 2n, sans remplissage : (tokens (B, n), proba argmax (B, n), t)."""
    x = mx.array(x_np)
    n = x.shape[1] // 2
    h, ctx = modele.etat0(x)
    if regle in ("bande", "t_n"):
        if regle == "bande":
            T = np.full(len(x_np), x.shape[1])
        else:
            T = np.asarray(t_n_np)
        tn = mx.array(T)
        sel = mx.zeros_like(h)
        for t in range(1, int(T.max()) + 1):
            h = modele.iterer(h, ctx)
            sel = mx.where((tn == t)[:, None, None], h, sel)
            mx.eval(sel, h)
        p = mx.softmax(modele.lire(sel)[:, n:, :].astype(mx.float32), axis=-1)
        tok, pm = mx.argmax(p, axis=-1), mx.max(p, axis=-1)
        return np.array(tok), np.array(pm), T
    assert regle == "confiance"
    B = x.shape[0]
    best = mx.full((B,), -np.inf)
    best_tok = mx.zeros((B, n), dtype=mx.uint32)
    best_lp = mx.zeros((B, n))
    best_t = mx.zeros((B,), dtype=mx.int32)
    for t in range(1, plafond + 1):
        h = modele.iterer(h, ctx)
        lp = nn.log_softmax(modele.lire(h)[:, n:, :].astype(mx.float32), axis=-1)
        lpm = mx.max(lp, axis=-1)
        score = lpm.sum(axis=-1)
        mieux = score > best  # strict : a egalite, la premiere iteration
        best = mx.where(mieux, score, best)
        best_tok = mx.where(mieux[:, None], mx.argmax(lp, axis=-1), best_tok)
        best_lp = mx.where(mieux[:, None], lpm, best_lp)
        best_t = mx.where(mieux, t, best_t)
        mx.eval(h, best, best_tok, best_lp, best_t)
    return np.array(best_tok), np.exp(np.array(best_lp)), np.array(best_t)
