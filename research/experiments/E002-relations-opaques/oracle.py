"""Vérité terrain d'un monde : réponses attendues, contradictions, coût en bits.

- `attendus` : l'étiquette attendue de chaque question, calculée à partir des
  faits connus du système et des VRAIES propriétés (PREREGISTREMENT §2.2).
- `vraie_valeur` : la vérité terrain d'un atome (sert à R, §4).
- Coût d'une requête : une requête est un atome d'expérience comme une
  observation, décrit par (relation, x, y, valeur), soit
  C_ATOME = log2(k) + 2·log2(n) + 1 bits (≈ 9.32 pour k = 5, n = 8).
  Un fait d'exclusion coûte C_EXCLUSION = log2(n(n−1)/2) bits (≈ 4.81).
  Une requête refusée (atome tenu à l'écart) ne coûte rien.
"""

import math

from monde import K_RELATIONS, N_ENTITES, regles_du_monde
from raisonneur import CONTRADICTION, DEDUIT, HYPOTHESE, INDETERMINE, Raisonneur

C_ATOME = math.log2(K_RELATIONS) + 2 * math.log2(N_ENTITES) + 1
C_EXCLUSION = math.log2(N_ENTITES * (N_ENTITES - 1) / 2)
EPSILON = 1 / 64


def raisonneur_oracle(monde, connus):
    return Raisonneur(connus, regles_du_monde(monde), monde["exclusions"], monde["entites"])


def attendus(monde, connus):
    rais = raisonneur_oracle(monde, connus)
    out = {}
    for q in monde["questions"]:
        if q["type"] == "atome":
            out[q["id"]] = rais.atome(q["atome"])
        else:
            out[q["id"]] = rais.exclusion(*q["paire"])
    return out


def vraie_valeur(monde, atome):
    r, x, y = atome
    return [x, y] in monde["verite"][r]


def contradictions(monde, connus):
    """Clauses violées par les faits connus sous les vraies propriétés."""
    return sorted(raisonneur_oracle(monde, connus).v0)


def p_systeme(reponse, p_ref):
    """Probabilité que le système donne à « vrai » (PREREGISTREMENT §4)."""
    e = reponse.get("etiquette")
    if e == DEDUIT and reponse.get("valeur") in (True, False):
        return 1 - EPSILON if reponse["valeur"] else EPSILON
    if e == HYPOTHESE and isinstance(reponse.get("p_vrai"), (int, float)):
        return min(1 - EPSILON, max(EPSILON, float(reponse["p_vrai"])))
    return p_ref


def bits(p_vrai, verite):
    return -math.log2(p_vrai if verite else 1 - p_vrai)


def bits_economises(reponses, tenus, verites, p_ref):
    """Σ sur les atomes tenus à l'écart de bits_ref − bits_sys.

    reponses : {atome: réponse}, verites : {atome: bool}, p_ref : {relation: p}.
    Une question sans réponse vaut INDÉTERMINÉ.
    """
    total = 0.0
    for a in tenus:
        a = tuple(a)
        pr = p_ref[a[0]]
        ps = p_systeme(reponses.get(a, {"etiquette": INDETERMINE}), pr)
        total += bits(pr, verites[a]) - bits(ps, verites[a])
    return total


def juste(reponse, attendu):
    """Exactitude d'étiquette (PREREGISTREMENT §2.3)."""
    e, ea = reponse.get("etiquette"), attendu["etiquette"]
    if ea == DEDUIT:
        return e == DEDUIT and reponse.get("valeur") == attendu["valeur"]
    if ea == CONTRADICTION:
        return e == CONTRADICTION
    return e in (INDETERMINE, HYPOTHESE)


def deduit_infonde(reponse, attendu):
    return reponse.get("etiquette") == DEDUIT and not (
        attendu["etiquette"] == DEDUIT and attendu["valeur"] == reponse.get("valeur"))
