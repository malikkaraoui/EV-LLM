"""E009-bis -- flux avec curriculum de longueur, fabrique a largeur choisie, controles T-ID.

Reutilise E009 (bande, archis, boucle, evalue) et E008 (data, evaluate) par import, sans les
modifier. Fige par PREREGISTREMENT-bis.md (sections 2 et 3).
"""
import os
import sys

import numpy as np

ICI = os.path.dirname(os.path.abspath(__file__))
E009 = os.path.join(os.path.dirname(ICI), "E009-procedure-apprise")
if E009 not in sys.path:
    sys.path.insert(1, E009)

import bande as b9  # noqa: E402  (E009, qui insere lui-meme E008 dans sys.path)
from bande import d8  # noqa: E402

L_DEPART, L_FIN = 2, 5
PERIODE_CURR, SEUIL_CURR, N_CURR = 500, 0.90, 100   # section 2.1
PERIODE_ARRET, SEUIL_ARRET, N_ARRET = 1000, 0.95, 200  # section 2.2
PLAFOND_PAS = 20_000  # section 2.3


# ---------------------------------------------------------------- flux
def paires_du_pas(graine, pas, exclues, lmax, batch=b9.BATCH):
    """Flux E008 (meme rng, meme boucle) avec longueurs uniformes 1..lmax ; lmax = 5 : E008."""
    rng = np.random.default_rng([10_000 + graine, pas])
    out = []
    while len(out) < batch:
        la, lb = (int(x) for x in rng.integers(d8.TRAIN_LMIN, lmax + 1, 2))
        p = (d8.tire_nombre(rng, la), d8.tire_nombre(rng, lb))
        if p in exclues:
            continue
        out.append(p)
    return out


def niveau_au_pas(transitions, pas):
    """transitions : [[pas_debut, niveau], ...] croissant ; niveau en vigueur au pas `pas`."""
    niv = L_DEPART
    for debut, n in transitions:
        if pas >= debut:
            niv = n
    return niv


def lot(graine, pas, exclues, lmax, inverse=True, batch=b9.BATCH):
    return b9.bandes(paires_du_pas(graine, pas, exclues, lmax, batch), inverse)


def uniques(graine, pas_total, transitions, points=(), batch=b9.BATCH):
    """Paires distinctes du flux reconstruit (curriculum compris) ; comptes aux points demandes."""
    ex = d8.paires_exclues()
    table, compte = set(), {}
    pts = set(points)
    for t in range(pas_total):
        table.update(paires_du_pas(graine, t, ex, niveau_au_pas(transitions, t), batch))
        if t + 1 in pts:
            compte[t + 1] = len(table)
    return table, compte


# ---------------------------------------------------------------- modeles
def fabrique(systeme, w):
    from archis import DeepThinking, LoopedNoPE, NeuralGPU
    if systeme == "A1":
        return NeuralGPU(w)
    if systeme == "A2-L":
        return DeepThinking(True, w)
    if systeme in ("A3", "A3-T"):
        return LoopedNoPE(d=w, tetes=4, ffn=4 * w)
    raise ValueError(systeme)


def regle(systeme):
    from archis import SYSTEMES
    return SYSTEMES[systeme]["regle"]


# ---------------------------------------------------------------- jeux de controle
def t_id(longueurs, n):
    tid = b9.jeux_id()["T-ID"]
    return {"T-ID": {L: tid[L][:n] for L in longueurs}}


def mesure(modele, systeme, jeux):
    """{cle: exact} par l'evaluateur unique E008, regle d'arret du test."""
    from evaluate import evaluer, resume  # E008
    from evalue import systeme_appris  # E009
    modele.eval()
    r = resume(evaluer(systeme_appris(modele, regle(systeme), True), jeux, "controle"))["par_jeu"]
    modele.train()
    return {k: c["exact"] for k, c in r.items()}
