"""Trois étalons de référence (PREREGISTREMENT §6, §56 v2).

Un système est un objet unique qui traverse toute la suite de mondes :
  debut_monde(vue) ; phase(p, observations, demander) -> {id: réponse} ;
  fin_monde(correction). Les trois étalons ne gardent rien d'un monde à l'autre.
"""

import random

from raisonneur import CONTRADICTION, DEDUIT, ETIQUETTES, HYPOTHESE, INDETERMINE, Raisonneur

PROPRIETES = ("reflexive", "symetrique", "antisymetrique", "transitive")


class Systeme:
    nom = "?"

    def debut_monde(self, vue):
        self.vue = vue
        self.obs = {}

    def phase(self, p, observations, demander):
        raise NotImplementedError

    def fin_monde(self, correction):
        pass

    def proprietes_crues(self):
        return None

    def _noter(self, observations):
        for r, x, y, v in observations:
            self.obs[(r, x, y)] = v


def regle_semantique(vue):
    s = vue["semantique"]
    return [["exclusion_A", s["relation"]]] if s["variante"] == "A" else []


def repondre(vue, connus, regles):
    rais = Raisonneur(connus, regles, vue["exclusions"], vue["entites"])
    out = {}
    for q in vue["questions"]:
        if q["type"] == "atome":
            out[q["id"]] = rais.atome(q["atome"])
        else:
            out[q["id"]] = rais.exclusion(*q["paire"])
    return out


class Aleatoire(Systeme):
    """Plancher : étiquette, valeur et probabilité tirées au hasard."""
    nom = "aleatoire"

    def __init__(self, graine=0):
        self.rng = random.Random(graine)

    def phase(self, p, observations, demander):
        out = {}
        for q in self.vue["questions"]:
            e = self.rng.choice(ETIQUETTES)
            out[q["id"]] = {
                "etiquette": e,
                "valeur": self.rng.random() < 0.5 if e in (DEDUIT, HYPOTHESE) else None,
                "p_vrai": self.rng.random(),
                "preuve": {"premisses": [], "regles": []},
                "regle_violee": ["hasard"],
                "manque": "hasard",
            }
        return out


class OracleProprietes(Systeme):
    """Plafond « savoir » : on lui DONNE les vraies propriétés ; aucune requête."""
    nom = "oracle_proprietes"

    def recevoir_proprietes(self, regles):
        self.regles = regles

    def phase(self, p, observations, demander):
        self._noter(observations)
        return repondre(self.vue, self.obs, self.regles)

    def proprietes_crues(self):
        return {"regles": self.regles}


class DecouvreurNaif(Systeme):
    """Teste par requêtes « Ri est-elle réflexive/symétrique/… ? », puis applique.

    Réfutation au premier contre-exemple, acceptation après CONFIRMATIONS
    confirmations, sinon propriété inconnue et non utilisée.
    """
    nom = "decouvreur_naif"
    CONFIRMATIONS = 3
    BUDGET = 150

    def debut_monde(self, vue):
        super().debut_monde(vue)
        self.req, self.refuses, self.nb_req = {}, set(), 0
        self.etat = {(p, r): [0, False] for r in vue["relations"] for p in PROPRIETES}
        self.etat_comp = {}
        self.rng = random.Random(0)  # remis à zéro à chaque monde : rien n'est gardé

    # --- requêtes et faits connus ---

    def _connus(self):
        k = dict(self.obs)
        k.update(self.req)
        return k

    def _demander(self, a):
        if a in self.req:
            return self.req[a]
        if a in self.refuses or self.nb_req >= self.BUDGET:
            return None
        v = self._dem(*a)
        if v is None:
            self.refuses.add(a)
            return None
        self.nb_req += 1
        self.req[a] = v
        return v

    def _decide(self, cle, table=None):
        c, refute = (table or self.etat)[cle]
        return refute or c >= self.CONFIRMATIONS

    def _noter_test(self, cle, ok, table=None):
        t = table or self.etat
        if self._decide(cle, t):
            return
        if ok:
            t[cle][0] += 1
        else:
            t[cle][1] = True

    def _positifs(self, r):
        """Candidats de test : paires OBSERVÉES positives (PREREGISTREMENT §6)."""
        return sorted((a[1], a[2]) for a, v in self.obs.items() if v and a[0] == r)

    # --- tests ---

    def _tester_relation(self, r):
        ents = list(self.vue["entites"])
        self.rng.shuffle(ents)
        for x in ents:
            if self._decide(("reflexive", r)):
                break
            v = self._demander((r, x, x))
            if v is not None:
                self._noter_test(("reflexive", r), v)

        paires = [(x, y) for x, y in self._positifs(r) if x != y]
        self.rng.shuffle(paires)
        for x, y in paires:
            if self._decide(("symetrique", r)) and self._decide(("antisymetrique", r)):
                break
            if self._demander((r, x, y)) is not True:
                continue
            v = self._demander((r, y, x))
            if v is None:
                continue
            self._noter_test(("symetrique", r), v)
            self._noter_test(("antisymetrique", r), not v)

        pos = self._positifs(r)
        succ = {}
        for x, y in pos:
            succ.setdefault(x, []).append(y)
        chaines = [(x, y, z) for x, y in pos for z in succ.get(y, ())]
        self.rng.shuffle(chaines)
        for x, y, z in chaines:
            if self._decide(("transitive", r)):
                break
            if self._demander((r, x, y)) is not True or self._demander((r, y, z)) is not True:
                continue
            v = self._demander((r, x, z))
            if v is not None:
                self._noter_test(("transitive", r), v)

    def _tester_compositions(self):
        rels = self.vue["relations"]
        connus = self.obs
        cands = []
        for ri in rels:
            for rj in rels:
                if ri == rj:
                    continue
                pi, pj = self._positifs(ri), self._positifs(rj)
                succ = {}
                for z, y in pj:
                    succ.setdefault(z, []).append(y)
                chaines = sorted({(x, z, y) for x, z in pi for y in succ.get(z, ())})
                if not chaines:
                    continue
                for rk in rels:
                    if rk in (ri, rj):
                        continue
                    vals = [connus[(rk, x, y)] for x, _, y in chaines if (rk, x, y) in connus]
                    if vals and all(vals):
                        cands.append((-len(vals), ri, rj, rk, chaines))
        cands.sort(key=lambda c: c[:4])
        for _, ri, rj, rk, chaines in cands:
            cle = (ri, rj, rk)
            self.etat_comp.setdefault(cle, [0, False])
            chaines = list(chaines)
            self.rng.shuffle(chaines)
            for x, z, y in chaines:
                if self._decide(cle, self.etat_comp):
                    break
                if self._demander((ri, x, z)) is not True or self._demander((rj, z, y)) is not True:
                    continue
                v = self._demander((rk, x, y))
                if v is not None:
                    self._noter_test(cle, v, self.etat_comp)

    def regles_crues(self):
        regles = [[p, r] for (p, r), (c, ref) in sorted(self.etat.items())
                  if not ref and c >= self.CONFIRMATIONS]
        regles += [["composition", ri, rj, rk] for (ri, rj, rk), (c, ref) in sorted(self.etat_comp.items())
                   if not ref and c >= self.CONFIRMATIONS]
        return regles + regle_semantique(self.vue)

    def phase(self, p, observations, demander):
        self._noter(observations)
        self._dem = demander
        for r in self.vue["relations"]:
            self._tester_relation(r)
        self._tester_compositions()
        return repondre(self.vue, self._connus(), self.regles_crues())

    def proprietes_crues(self):
        refutees = [[p, r] for (p, r), (c, ref) in sorted(self.etat.items()) if ref]
        refutees += [["composition"] + list(k) for k, (c, ref) in sorted(self.etat_comp.items()) if ref]
        return {"regles": self.regles_crues(), "refutees": refutees, "requetes": self.nb_req}


ETALONS = (Aleatoire, OracleProprietes, DecouvreurNaif)

__all__ = ["Systeme", "Aleatoire", "OracleProprietes", "DecouvreurNaif", "ETALONS",
           "CONTRADICTION", "INDETERMINE"]
