"""Environnement interactif vu par un système (PREREGISTREMENT §1.6, §1.7, §4).

Le système ne voit jamais la vérité, les propriétés, les types ni le bruit.
Il reçoit la vue publique, les observations phase par phase, peut demander
des atomes (facturés en bits) et rend des réponses étiquetées. Tout est
journalisé pour le calcul de R.
"""

from oracle import C_ATOME, C_EXCLUSION


class Environnement:
    def __init__(self, monde):
        self._m = monde
        self._vrai = {(r, a, b) for r, paires in monde["verite"].items() for a, b in paires}
        self._tenus = {tuple(a) for a in monde["tenus_a_l_ecart"]}
        self.phase = 0
        self.observations = []   # (phase, atome, valeur) livrées
        self.requetes = []       # (phase, atome, valeur) acceptées
        self.refus = []          # (phase, atome) refusées
        self.reponses = {}       # phase -> {id question: réponse}

    def vue_publique(self):
        m = self._m
        return {
            "entites": list(m["entites"]),
            "relations": list(m["relations"]),
            "semantique": dict(m["semantique"]),
            "exclusions": [list(p) for p in m["exclusions"]],
            "questions": [dict(q) for q in m["questions"]],
            "cout_atome_bits": C_ATOME,
        }

    def ouvrir_phase(self, p):
        self.phase = p
        nouvelles = [(tuple(o["atome"]), o["valeur"]) for o in self._m["observations"] if o["phase"] == p]
        self.observations += [(p, a, v) for a, v in nouvelles]
        return [list(a) + [v] for a, v in nouvelles]

    def demander(self, r, x, y):
        """Vérité sans bruit, ou None si l'atome est tenu à l'écart (refus non facturé)."""
        a = (r, x, y)
        if a in self._tenus:
            self.refus.append((self.phase, a))
            return None
        v = a in self._vrai
        self.requetes.append((self.phase, a, v))
        return v

    def enregistrer(self, p, reponses):
        self.reponses[p] = dict(reponses)

    # --- comptes (lus par l'évaluateur, jamais par le système) ---

    def connus(self, jusqu_a_phase):
        """Faits connus du système : observations puis requêtes, la requête primant."""
        k = {}
        for p, a, v in self.observations:
            if p <= jusqu_a_phase:
                k[a] = v
        for p, a, v in self.requetes:
            if p <= jusqu_a_phase:
                k[a] = v
        return k

    def bits_experience(self):
        return {
            "observations": len(self.observations) * C_ATOME,
            "requetes": len(self.requetes) * C_ATOME,
            "exclusions": len(self._m["exclusions"]) * C_EXCLUSION,
        }

    def p_ref(self):
        """Prédicteur de référence sans structure : Laplace par relation, sur les observations."""
        pos, tot = {}, {}
        for _, (r, _x, _y), v in self.observations:
            tot[r] = tot.get(r, 0) + 1
            pos[r] = pos.get(r, 0) + (1 if v else 0)
        return {r: (pos.get(r, 0) + 1) / (tot.get(r, 0) + 2) for r in self._m["relations"]}
