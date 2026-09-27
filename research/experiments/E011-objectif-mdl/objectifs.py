"""E011 -- objectifs (PREREGISTREMENT section 4).

Gradient : a (CE), b (CE + L2), c (CE + L1), e (MDL differentiable, quantification au demi).
Recherche locale : d (MDL discret, codage de Lan 2022), d-CE, d-L2.
"""
from fractions import Fraction

import numpy as np

from rnn import LN2, ce_et_grad


# ---------------------------------------------------------------- MDL discret (Lan 2022)
def bits_entier(n):
    """Code prefixe d'Elias gamma de n + 1 (n >= 0) : 2 floor(log2(n+1)) + 1 bits."""
    return 2 * (int(n) + 1).bit_length() - 1


def bits_poids(w):
    """1 bit de signe + numerateur + denominateur (fraction reduite)."""
    f = Fraction(w).limit_denominator(1 << 16)
    return 1 + bits_entier(abs(f.numerator)) + bits_entier(f.denominator)


def longueur_H(theta):
    return sum(bits_poids(float(w)) for w in theta)


# ---------------------------------------------------------------- objectifs a gradient
def quantifie(theta):
    return np.round(2.0 * theta) / 2.0


def objectif_grad(code, lam):
    """Renvoie f(theta, X, Y, M) -> (objectif, ce_bits, gradient)."""
    if code == "a":
        def f(th, X, Y, M):
            ce, g = ce_et_grad(th, X, Y, M)
            return ce, ce, g
    elif code == "b":
        def f(th, X, Y, M):
            ce, g = ce_et_grad(th, X, Y, M)
            return ce + lam * float(th @ th), ce, g + 2.0 * lam * th
    elif code == "c":
        def f(th, X, Y, M):
            ce, g = ce_et_grad(th, X, Y, M)
            return ce + lam * float(np.abs(th).sum()), ce, g + lam * np.sign(th)
    elif code == "e":
        def f(th, X, Y, M):
            # CE avec poids quantifies, gradient droit-a-travers ; cout lisse en bits
            ce, g = ce_et_grad(quantifie(th), X, Y, M)
            cout = float(np.sum(2.0 * np.log2(1.0 + 2.0 * np.abs(th))))
            gc = 2.0 * 2.0 * np.sign(th) / ((1.0 + 2.0 * np.abs(th)) * LN2)
            return ce + cout, ce, g + gc
    else:
        raise ValueError(code)
    return f


def modele_evalue(code, theta):
    """Le reseau reellement utilise (e : poids quantifies)."""
    return quantifie(theta) if code == "e" else theta


# ---------------------------------------------------------------- objectifs de recherche locale
def objectif_local(code):
    from rnn import ce_bits, forward

    def ce(th, X, Y, M):
        return ce_bits(forward(th, X)[0], Y, M)

    if code == "d":
        return lambda th, X, Y, M: longueur_H(th) + ce(th, X, Y, M)
    if code == "d-CE":
        return ce
    if code == "d-L2":
        return lambda th, X, Y, M: ce(th, X, Y, M) + 0.1 * float(th @ th)
    raise ValueError(code)
