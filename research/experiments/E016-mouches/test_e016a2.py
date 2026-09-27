"""E016-A2 -- tests du code A2 (lanceur maison, pytest absent du venv comme M0031).

  python test_e016a2.py
"""
import numpy as np

import entraine16 as E1
import entraine16a2 as E2
from m16 import D


def test_credit_oracle_et_bruit():
    probs = [(12, 9), (99999, 1), (0, 0), (5, 57)]
    _, _, Y, M = D.encode_aligne(probs, D.T_TRAIN)
    juste, c, _ = E2.credit(probs, Y.copy(), "dense")
    assert juste.all() and np.allclose(c, 1.0)
    dig = Y.copy()
    dig[1, 0] = (dig[1, 0] + 1) % 10          # 1 colonne fausse sur 6
    juste, c, _ = E2.credit(probs, dig, "dense")
    assert not juste[1] and abs(c[1] - 5 / 6) < 1e-9 and juste[[0, 2, 3]].all()
    _, c01, _ = E2.credit(probs, dig, "01")
    assert list(c01) == [1.0, 0.0, 1.0, 1.0]
    dig[0, 5] = 7                              # hors n_pas : ignore
    assert E2.credit(probs, dig, "dense")[1][0] == 1.0


def test_tours_identiques_a_m0031():
    for pas in (0, 10, 2500):
        t1, b1, p1 = E1.tours_du_pas("IND", 3, pas, 4000, [])
        for cond in ("IND", "TOR", "COLL", "REJEU"):
            t2, b2, p2 = E2.tours_du_pas(cond, 3, pas, 4000, [])
            assert (b1, p1) == (b2, p2) and [t["p"] for t in t1] == [t["p"] for t in t2]
            assert [t["paires"] for t in t1] == [t["paires"] for t in t2]


def test_fixe_diagonale():
    for pas in (0, 2500):
        t, _, _ = E2.tours_du_pas("FIXE", 1, pas, 4000, [])
        assert all(i == j for x in t for i, j in x["paires"])
        assert len({ij for x in t for ij in x["paires"]}) == 3


def test_curriculum():
    t, _, _ = E2.tours_du_pas("IND", 0, 5, 4000, [], curric=True)
    assert all(a < 10 and b < 10 for x in t for a, b in x["p"])
    t, _, _ = E2.tours_du_pas("IND", 0, 1000, 4000, [], curric=True)
    assert any(max(a, b) >= 10 for x in t for a, b in x["p"])


if __name__ == "__main__":
    n = 0
    for k, f in list(globals().items()):
        if k.startswith("test_"):
            f()
            n += 1
            print("ok", k)
    print(f"{n}/{n} tests passent")
