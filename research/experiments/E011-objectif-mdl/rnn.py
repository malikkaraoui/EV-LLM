"""E011 -- RNN d'Elman 2 -> 3 sigmoides -> 1 sigmoide, retropropagation manuelle (numpy).

Vecteur de parametres (22) : Wi (3x2) | Wr (3x3) | bh (3) | wo (3) | bo (1).
"""
import numpy as np

H = 3
N_PARAMS = H * 2 + H * H + H + H + 1
LN2 = np.log(2.0)


def decoupe(theta):
    i = 0
    Wi = theta[i:i + 6].reshape(3, 2); i += 6
    Wr = theta[i:i + 9].reshape(3, 3); i += 9
    bh = theta[i:i + 3]; i += 3
    wo = theta[i:i + 3]; i += 3
    bo = theta[i]
    return Wi, Wr, bh, wo, bo


def golden(k=10.0, ko=10.0):
    """Reseau exact (PREREGISTREMENT section 3) : s = n + m + c, h_j = sig(k(s - theta_j))."""
    Wi = np.full((3, 2), k)
    Wr = np.zeros((3, 3))
    Wr[:, 1] = k  # la retenue c_{t-1} = h_2(t-1) entre dans les trois unites
    bh = -k * np.array([0.5, 1.5, 2.5])
    wo = ko * np.array([1.0, -1.0, 1.0])
    bo = -0.5 * ko
    return np.concatenate([Wi.ravel(), Wr.ravel(), bh, wo, [bo]])


def sig(z):
    return 0.5 * (1.0 + np.tanh(0.5 * z))


def forward(theta, X):
    """Logits de sortie (B, T) et etats caches (B, T, 3)."""
    Wi, Wr, bh, wo, bo = decoupe(theta)
    B, T, _ = X.shape
    h = np.zeros((B, H))
    hs = np.zeros((B, T, H))
    for t in range(T):
        h = sig(X[:, t] @ Wi.T + h @ Wr.T + bh)
        hs[:, t] = h
    return hs @ wo + bo, hs


def ce_bits(z, Y, M):
    """CE totale en bits (somme sur les bits masques)."""
    # -log p(y) = softplus(-z) si y = 1, softplus(z) si y = 0
    s = np.where(Y > 0.5, -z, z)
    return float(np.sum(M * np.logaddexp(0.0, s)) / LN2)


def ce_et_grad(theta, X, Y, M):
    Wi, Wr, bh, wo, bo = decoupe(theta)
    z, hs = forward(theta, X)
    loss = ce_bits(z, Y, M)
    dz = (sig(z) - Y) * M / LN2  # (B, T)
    B, T, _ = X.shape
    gWi = np.zeros_like(Wi); gWr = np.zeros_like(Wr); gbh = np.zeros(H)
    gwo = np.einsum("bt,bth->h", dz, hs)
    gbo = dz.sum()
    dpre_suiv = np.zeros((B, H))
    for t in range(T - 1, -1, -1):
        h = hs[:, t]
        dh = dz[:, t, None] * wo + dpre_suiv @ Wr
        dpre = dh * h * (1.0 - h)
        h_prec = hs[:, t - 1] if t > 0 else np.zeros((B, H))
        gWi += dpre.T @ X[:, t]
        gWr += dpre.T @ h_prec
        gbh += dpre.sum(0)
        dpre_suiv = dpre
    g = np.concatenate([gWi.ravel(), gWr.ravel(), gbh, gwo, [gbo]])
    return loss, g


def predit(theta, paires, encode):
    """Systeme au sens E008 : (a, b) -> (somme decimale, confiance = prod max(p, 1-p))."""
    X, _, M = encode(paires)
    z, _ = forward(theta, X)
    p = sig(z)
    bits = (p > 0.5).astype(np.int64)
    conf = np.prod(np.where(M > 0, np.maximum(p, 1.0 - p), 1.0), axis=1)
    out = []
    for i in range(len(paires)):
        n = int(M[i].sum())
        v = 0
        for j in range(n - 1, -1, -1):
            v = (v << 1) | int(bits[i, j])
        out.append((str(v), float(conf[i])))
    return out
