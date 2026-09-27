"""E015 -- circuit (cellule d'E013 a largeur variable), passe avant numpy, vie MLX (CPU).

z = relu(W1 [x ; h] + b1) ; h' = tanh(Wh z + bh) ; logits = Wo z + bo  (x = one-hot 11 par port)
La passe avant numpy est la seule utilisee pour juger (phase A et phase B).
"""
import numpy as np

from d15 import ABSENT_C, cible_mini, encode_ports

NA = 11  # alphabet d'entree d'un champion : 0-9 + ABSENT


def init_poids(rng, k, H, F):
    def lin(n_out, n_in):
        b = 1 / np.sqrt(n_in)
        return (rng.uniform(-b, b, (n_out, n_in)).astype(np.float32),
                rng.uniform(-b, b, (n_out,)).astype(np.float32))
    W1, b1 = lin(F, NA * k + H)
    Wh, bh = lin(H, F)
    Wo, bo = lin(10, F)
    return {"W1": W1, "b1": b1, "Wh": Wh, "bh": bh, "Wo": Wo, "bo": bo}


def avant(P, X, lens=None):
    """P : poids numpy ; X (n, T, k) symboles 0-10. -> chiffres (n, T), p_emis (n, T)."""
    n, T, k = X.shape
    H = P["Wh"].shape[0]
    eye = np.eye(NA, dtype=np.float32)
    h = np.zeros((n, H), dtype=np.float32)
    ys, ps = np.zeros((n, T), dtype=np.int64), np.zeros((n, T), dtype=np.float32)
    W1x, W1h = P["W1"][:, : NA * k], P["W1"][:, NA * k:]
    # contribution de x precalculee pour tous les pas
    Ex = eye[X].reshape(n, T, NA * k) @ W1x.T + P["b1"]
    for t in range(T):
        z = np.maximum(Ex[:, t] + h @ W1h.T, 0)
        h = np.tanh(z @ P["Wh"].T + P["bh"])
        lg = z @ P["Wo"].T + P["bo"]
        lg = lg - lg.max(axis=1, keepdims=True)
        e = np.exp(lg)
        p = e / e.sum(axis=1, keepdims=True)
        ys[:, t] = p.argmax(axis=1)
        ps[:, t] = p.max(axis=1)
    return ys, ps


def exact_mini(P, tache, items):
    X, lens = encode_ports(items, X_k(tache))
    ys, _ = avant(P, X)
    ok = 0
    for i, it in enumerate(items):
        ok += int(list(ys[i, : lens[i]]) == cible_mini(tache, it))
    return ok / len(items)


def X_k(tache):
    from d15 import PORTS
    return PORTS[tache]


# ------------------------------------------------------------------ vie (MLX, CPU)
def vie(P, tache, graine, pas, lr, n=128, decalage=0):
    """`pas` pas d'Adam sur le flux de la mini-tache ; renvoie les nouveaux poids numpy."""
    import mlx.core as mx
    import mlx.optimizers as optim

    from d15 import lot_mini
    mx.set_default_device(mx.cpu)
    k = X_k(tache)
    params = {c: mx.array(v) for c, v in P.items()}
    H = P["Wh"].shape[0]

    def perte(pr, X, Y, M):
        nb, T, _ = X.shape
        x = mx.eye(NA)[X].reshape(nb, T, NA * k)
        h = mx.zeros((nb, H))
        tot = 0.0
        for t in range(T):
            z = mx.maximum(mx.concatenate([x[:, t], h], axis=-1) @ pr["W1"].T + pr["b1"], 0)
            h = mx.tanh(z @ pr["Wh"].T + pr["bh"])
            lg = z @ pr["Wo"].T + pr["bo"]
            ce = mx.logsumexp(lg, axis=-1) - mx.take_along_axis(lg, Y[:, t:t + 1], axis=-1)[:, 0]
            tot = tot + (ce * M[:, t]).sum()
        return tot / M.sum()

    vg = mx.value_and_grad(perte)
    opt = optim.Adam(learning_rate=lr)
    for s in range(pas):
        items = lot_mini(graine, tache, decalage + s, n)
        X, lens = encode_ports(items, k)
        T = X.shape[1]
        Y = np.zeros((len(items), T), dtype=np.int32)
        M = np.zeros((len(items), T), dtype=np.float32)
        for i, it in enumerate(items):
            y = cible_mini(tache, it)
            Y[i, : len(y)] = y
            M[i, : len(y)] = 1
        _, g = vg(params, mx.array(X.astype(np.int32)), mx.array(Y), mx.array(M))
        params = opt.apply_gradients(g, params)
        mx.eval(params)
    return {c: np.array(v, dtype=np.float32) for c, v in params.items()}


assert ABSENT_C == 10
