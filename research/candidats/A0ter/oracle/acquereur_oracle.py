"""Étalon « acquéreur-oracle » (PREREGISTREMENT-oracle.md §3).

`oracle_acquereur` hérite d'`A0Bis` (importé tel quel). À la fin du 1er monde
d'une famille du banc, il reçoit par un canal d'évaluateur la connaissance
parfaite de cette famille, K_f : les vecteurs de propriétés vraies des 5
relations et les compositions vraies, sans aucun nom. Dans les mondes suivants
de la même famille, K_f est placée sur les relations courantes par la
bijection d'accord maximal (identification parfaite) et appliquée comme règles
certaines ; tout le reste est celui d'A0-bis. Avant K_f, il est A0-bis.
`oracle_amnesique` : tout est remis à zéro à chaque monde.
`oracle_exact` (diagnostic) : applique les propriétés vraies du monde courant.
"""

from itertools import permutations

import chemin  # noqa: F401

from a0bis import A0Bis, memoire_initiale
from etalons import PROPRIETES

POIDS_COMPOSITION = 4   # §3.1 : score(σ) = bits égaux + 4 × compositions vraies sous σ

# --- canal d'évaluateur -------------------------------------------------------------
# L'évaluateur enregistre les mondes de la séquence ; l'oracle les retrouve par la
# signature de la vue publique (identifiants des questions). Chaque accès est journalisé.

_SOURCE = {}


def signature(vue):
    return tuple(sorted(q["id"] for q in vue["questions"]))


def enregistrer_mondes(mondes):
    for m in mondes:
        _SOURCE[signature(m)] = m


def _monde(vue):
    return _SOURCE[signature(vue)]


# --- connaissance de famille, sans nom ------------------------------------------------

def connaissance(monde):
    """K_f : 5 vecteurs de propriétés vraies (ordre des relations triées) + compositions en indices."""
    rels = sorted(monde["relations"])
    vecs = [[int(monde["proprietes"][r][p]) for p in PROPRIETES] for r in rels]
    comps = sorted([rels.index(a), rels.index(b), rels.index(c)] for a, b, c in monde["compositions"])
    return {"vecteurs": vecs, "compositions": comps}


def regles_vraies(monde):
    """Propriétés et compositions vraies du monde courant, comme règles."""
    rels = sorted(monde["relations"])
    out = [(p, r) for r in rels for p in PROPRIETES if monde["proprietes"][r][p]]
    out += [("composition",) + tuple(c) for c in monde["compositions"]]
    return sorted(out)


def placer(k, monde):
    """σ d'accord maximal (identification parfaite), puis règles de K_f sous σ."""
    rels = sorted(monde["relations"])
    vrai = {r: [int(monde["proprietes"][r][p]) for p in PROPRIETES] for r in rels}
    comps_vraies = {tuple(c) for c in monde["compositions"]}
    meilleur = None
    for perm in permutations(rels):
        s = sum(a == b for j, r in enumerate(perm) for a, b in zip(k["vecteurs"][j], vrai[r]))
        s += POIDS_COMPOSITION * sum((perm[a], perm[b], perm[c]) in comps_vraies for a, b, c in k["compositions"])
        if meilleur is None or s > meilleur[0]:
            meilleur = (s, perm)
    perm = meilleur[1]
    out = [(p, perm[j]) for j in range(len(perm)) for i, p in enumerate(PROPRIETES) if k["vecteurs"][j][i]]
    out += [("composition", perm[a], perm[b], perm[c]) for a, b, c in k["compositions"]]
    return sorted(out)


class OracleAcquereur(A0Bis):
    nom = "oracle_acquereur"
    AMNESIQUE = False
    EXACT = False

    def __init__(self):
        super().__init__()
        self.connaissances = {}     # famille du banc -> K_f (sans nom)
        self.acces_canal = []       # (moment, graine, K_f utilisée) : traçabilité de la temporalité

    def debut_monde(self, vue):
        if self.AMNESIQUE:
            self.memoire = memoire_initiale()
            self.connaissances = {}
        super().debut_monde(vue)
        self.regles_oracle, self.k_egale_verite = None, None
        if not self.connaissances:
            return
        m = _monde(vue)
        connue = m["famille"] in self.connaissances
        self.acces_canal.append(("debut_monde", m["graine"], connue))
        if not connue:
            return
        vraies = regles_vraies(m)
        self.regles_oracle = vraies if self.EXACT else placer(self.connaissances[m["famille"]], m)
        self.k_egale_verite = self.regles_oracle == vraies

    def _etape_regles(self):
        if self.regles_oracle is None:
            return super()._etape_regles()
        self.utilisees = list(self.regles_oracle)   # règles certaines : aucun test

    def fin_monde(self, correction):
        super().fin_monde(correction)
        m = _monde(self.vue)
        self.acces_canal.append(("fin_monde", m["graine"], True))
        if m["famille"] not in self.connaissances:
            self.connaissances[m["famille"]] = connaissance(m)

    def proprietes_crues(self):
        d = super().proprietes_crues()
        d.update({"regles_oracle": None if self.regles_oracle is None else len(self.regles_oracle),
                  "k_egale_verite": self.k_egale_verite})
        return d


class OracleAmnesique(OracleAcquereur):
    nom = "oracle_amnesique"
    AMNESIQUE = True


class OracleExact(OracleAcquereur):
    nom = "oracle_exact"
    EXACT = True


ORACLES = (OracleAcquereur, OracleAmnesique, OracleExact)
