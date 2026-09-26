"""Plafond-vérificateur (PREREGISTREMENT bis §2).

Il sait les vraies propriétés, comme l'oracle-propriétés d'E002, mais avant
de conclure il demande au monde chaque prémisse citée par ses réponses
DÉDUIT et CONTRADICTION, puis recommence jusqu'à ce que toutes soient
vérifiées. Il ne garde rien d'un monde à l'autre.
"""

import chemin_e002  # noqa: F401

from etalons import Aleatoire, DecouvreurNaif, OracleProprietes, repondre
from raisonneur import CONTRADICTION, DEDUIT

A_VERIFIER = (DEDUIT, CONTRADICTION)


def premisses(reponses):
    """Atomes cités comme prémisses par les réponses DÉDUIT et CONTRADICTION."""
    out = set()
    for rep in reponses.values():
        if rep.get("etiquette") in A_VERIFIER:
            for p in rep.get("preuve", {}).get("premisses", []):
                out.add((p[0], p[1], p[2]))
    return out


class PlafondVerificateur(OracleProprietes):
    nom = "plafond_verificateur"

    def debut_monde(self, vue):
        super().debut_monde(vue)
        self.req, self.refuses = {}, set()

    def phase(self, p, observations, demander):
        self._noter(observations)
        while True:
            connus = dict(self.obs)
            connus.update(self.req)
            reps = repondre(self.vue, connus, self.regles)
            a_faire = sorted(premisses(reps) - set(self.req) - self.refuses)
            if not a_faire:
                return reps
            for a in a_faire:
                v = demander(*a)
                if v is None:
                    self.refuses.add(a)
                else:
                    self.req[a] = v

    def proprietes_crues(self):
        return {"regles": self.regles, "requetes": len(self.req)}


ETALONS_BIS = (Aleatoire, OracleProprietes, PlafondVerificateur, DecouvreurNaif)
