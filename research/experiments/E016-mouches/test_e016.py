"""E016 -- tests : python test_e016.py (sans dependance)."""
import hashlib
import os

import mlx.core as mx
import mlx.optimizers as optim
import numpy as np

import entraine16 as T
import m16
from m16 import D, K, Population, perte_reinforce

ICI = os.path.dirname(os.path.abspath(__file__))
_POP = {}


def pop(coupe=False):
    if coupe not in _POP:
        _POP[coupe] = Population(7, coupe=coupe)
    return _POP[coupe]


def _paires(L, n=40, g=99):
    rng = np.random.default_rng(g)
    return [(D.e008.tire_nombre(rng, L), D.e008.tire_nombre(rng, L)) for _ in range(n)]


def test_poids_lecteurs_sha256():
    d = os.path.join(ICI, "lecteurs_e014")
    for ligne in open(os.path.join(d, "SHA256SUMS")):
        h, f = ligne.split()
        assert hashlib.sha256(open(os.path.join(d, f), "rb").read()).hexdigest() == h


def test_codes_prives_bijectifs_et_distincts():
    c = m16.codes_prives(3, 6)
    for p in c:
        assert sorted(p) == list(range(K))
    assert len({tuple(p) for p in c}) == 6


def test_interface_donnee_exacte_9_paires():
    p = Population(7)
    p.interface_donnee()
    paires = _paires(16)
    for i in range(3):
        for j in range(3):
            r = p.systeme(i, j, cache=False)(paires)
            assert all(x == str(a + b) for (a, b), (x, _) in zip(paires, r))


def test_politique_initiale_ne_sait_rien():
    r = pop().systeme(0, 0, cache=False)(_paires(8))
    assert np.mean([x == str(a + b) for (a, b), (x, _) in zip(_paires(8), r)]) < 0.1


def test_canal_coupe_ignore_le_message():
    p = pop(coupe=True)
    act, _ = m16.echantillonne(p, [(0, 0)] * 8, np.random.randint(0, 11, (8, 6, 2)).astype(np.int32),
                               mx.random.key(1))
    assert (act["vu"] == 0).all() and not (act["sym"] == 0).all()


def test_appariement_phase2_parfait_et_phase1_une_paire():
    tours, _, ph = T.tours_du_pas("COLL", 1, 10, 100, [])
    assert ph == 1 and all(len(t["paires"]) == 1 for t in tours) and len(tours) == T.LOT_TOURS
    tours, n_neufs, ph = T.tours_du_pas("COLL", 1, 60, 100, [])
    assert ph == 2 and n_neufs == 3 * T.LOT_TOURS
    for t in tours:
        assert sorted(i for i, _ in t["paires"]) == [0, 1, 2]
        assert sorted(j for _, j in t["paires"]) == [0, 1, 2]
        assert len(set(t["p"])) == 3


def test_rejeu_memes_problemes_nouveau_tirage_et_plafond():
    file = [{"p": [(12, 34)], "essai": 2}]
    tours, n_neufs, _ = T.tours_du_pas("COLL", 1, 5, 100, file)
    assert tours[0]["p"] == [(12, 34)] and tours[0]["essai"] == 2 and n_neufs == T.LOT_TOURS - 1
    p = Population(8)  # politique uniforme : quasi tout echoue
    opt = optim.Adam(learning_rate=0.0)
    opt.init(p.t.parameters())
    file = [{"p": [(5, 7)], "essai": T.ESSAIS_MAX}] + [{"p": [(3, 4)], "essai": 1}]
    nouv, _ = T.un_pas(p, opt, "COLL", 1, 5, 100, file, 0.0)
    ps = [t["p"] for t in nouv]
    assert [(5, 7)] not in ps                     # 4e essai echoue -> abandonne
    if [(3, 4)] in ps:
        assert nouv[ps.index([(3, 4)])]["essai"] == 2
    nouv_ind, _ = T.un_pas(p, opt, "IND", 1, 5, 100, file, 0.0)
    assert nouv_ind == []                         # IND : aucun rejeu


def test_reinforce_renforce_le_choix_recompense():
    p = Population(9)
    act, _ = m16.echantillonne(p, [(1, 2)], np.zeros((1, 6, 2), np.int32), mx.random.key(3))
    import mlx.nn as nn
    avant = float(nn.log_softmax(p.t.E[1, int(p.pi[1][0])])[int(act["sym"][0, 0, 0])])
    opt = optim.SGD(learning_rate=1.0)
    _, g = mx.value_and_grad(lambda t: perte_reinforce(t, act, np.ones(1, np.float32),
                                                       np.eye(1, 6, dtype=np.float32), 0.0))(p.t)
    opt.update(p.t, g)
    apres = float(nn.log_softmax(p.t.E[1, int(p.pi[1][0])])[int(act["sym"][0, 0, 0])])
    assert apres > avant


if __name__ == "__main__":
    import sys
    tests = [(k, f) for k, f in sorted(globals().items()) if k.startswith("test_")]
    echecs = 0
    for k, f in tests:
        try:
            f()
            print("ok  ", k)
        except Exception as e:  # noqa: BLE001  (lanceur de tests : on rapporte et on continue)
            echecs += 1
            print("ECHEC", k, repr(e))
    print(f"{len(tests) - echecs}/{len(tests)} tests passent")
    sys.exit(1 if echecs else 0)
