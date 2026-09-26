"""Chaînage avant de Horn sur des relations binaires, avec provenance.

Partagé par l'oracle (vraies propriétés), le plafond (vraies propriétés
données) et le découvreur naïf (ses propriétés crues). Sémantique figée
dans PREREGISTREMENT.md §2.2.

Un atome est un tuple (r, x, y). Une règle est un tuple :
  ("reflexive", r) | ("symetrique", r) | ("transitive", r)
  ("antisymetrique", r) | ("composition", ri, rj, rk) | ("exclusion_A", ro)
"""

DEDUIT = "DÉDUIT"
HYPOTHESE = "HYPOTHÈSE"
CONTRADICTION = "CONTRADICTION"
INDETERMINE = "INDÉTERMINÉ"
ETIQUETTES = (DEDUIT, HYPOTHESE, CONTRADICTION, INDETERMINE)

REGLES_DEFINIES = ("reflexive", "symetrique", "transitive", "composition")


class Fermeture:
    """Plus petit modèle M des faits positifs, avec la justification de chaque atome."""

    def __init__(self, positifs, regles, entites):
        self.regles = [tuple(r) for r in regles]
        self.entites = list(entites)
        self.just = {}  # atome -> (règle | None, parents)
        self.succ = {}
        self.pred = {}
        self._file = []
        for r in self.regles:
            if r[0] == "reflexive":
                for x in self.entites:
                    self._ajouter((r[1], x, x), r, ())
        for a in positifs:
            self._ajouter(tuple(a), None, ())
        self._propager()

    def copie_avec(self, atome):
        c = Fermeture.__new__(Fermeture)
        c.regles, c.entites = self.regles, self.entites
        c.just = dict(self.just)
        c.succ = {k: {kk: set(vv) for kk, vv in v.items()} for k, v in self.succ.items()}
        c.pred = {k: {kk: set(vv) for kk, vv in v.items()} for k, v in self.pred.items()}
        c._file = []
        c._ajouter(tuple(atome), ("hypothese-examinee",), ())
        c._propager()
        return c

    def __contains__(self, atome):
        return tuple(atome) in self.just

    def _ajouter(self, a, regle, parents):
        if a in self.just:
            return
        self.just[a] = (regle, parents)
        r, x, y = a
        self.succ.setdefault(r, {}).setdefault(x, set()).add(y)
        self.pred.setdefault(r, {}).setdefault(y, set()).add(x)
        self._file.append(a)

    def _propager(self):
        while self._file:
            a = self._file.pop()
            r, x, y = a
            for regle in self.regles:
                t = regle[0]
                if t == "symetrique" and regle[1] == r:
                    self._ajouter((r, y, x), regle, (a,))
                elif t == "transitive" and regle[1] == r:
                    for z in list(self.succ.get(r, {}).get(y, ())):
                        self._ajouter((r, x, z), regle, (a, (r, y, z)))
                    for w in list(self.pred.get(r, {}).get(x, ())):
                        self._ajouter((r, w, y), regle, ((r, w, x), a))
                elif t == "composition":
                    ri, rj, rk = regle[1], regle[2], regle[3]
                    if r == ri:
                        for z in list(self.succ.get(rj, {}).get(y, ())):
                            self._ajouter((rk, x, z), regle, (a, (rj, y, z)))
                    if r == rj:
                        for w in list(self.pred.get(ri, {}).get(x, ())):
                            self._ajouter((rk, w, y), regle, ((ri, w, x), a))

    def origine(self, atomes):
        """Faits de base et règles qui soutiennent ces atomes."""
        faits, regles, vus = set(), set(), set()
        pile = [tuple(a) for a in atomes]
        while pile:
            a = pile.pop()
            if a in vus:
                continue
            vus.add(a)
            regle, parents = self.just[a]
            if regle is None:
                faits.add(a)
            elif regle[0] == "hypothese-examinee":
                continue
            else:
                regles.add(regle)
                pile.extend(parents)
        return faits, regles


def violations(ferm, negatifs, regles, exclusions):
    """Clauses négatives violées : ensemble de (règle, atomes positifs en cause)."""
    v = set()
    for a in negatifs:
        if tuple(a) in ferm:
            v.add((("fait-negatif",), (tuple(a),)))
    for regle in regles:
        regle = tuple(regle)
        if regle[0] == "antisymetrique":
            r = regle[1]
            for x, ys in ferm.succ.get(r, {}).items():
                for y in ys:
                    if x < y and x in ferm.succ.get(r, {}).get(y, ()):
                        v.add((regle, ((r, x, y), (r, y, x))))
        elif regle[0] == "exclusion_A":
            ro = regle[1]
            for x, y in exclusions:
                for a in ((ro, x, y), (ro, y, x)):
                    if a in ferm:
                        v.add((regle, (a,)))
    return v


def _regle_json(regle):
    return list(regle)


class Raisonneur:
    """Répond aux questions à partir de faits connus et de règles (PREREGISTREMENT §2.2)."""

    def __init__(self, connus, regles, exclusions, entites):
        # connus : dict atome -> bool
        self.connus = {tuple(a): bool(v) for a, v in connus.items()}
        self.regles = [tuple(r) for r in regles]
        self.exclusions = [tuple(p) for p in exclusions]
        positifs = [a for a, v in self.connus.items() if v]
        self.negatifs = [a for a, v in self.connus.items() if not v]
        self.ferm = Fermeture(positifs, [r for r in self.regles if r[0] in REGLES_DEFINIES], entites)
        self.v0 = violations(self.ferm, self.negatifs, self.regles, self.exclusions)

    def coherent(self):
        return not self.v0

    def _preuve(self, ferm, atomes, regles_sup=(), negatifs_sup=()):
        faits, regles = ferm.origine(atomes)
        prem = sorted([list(a) + [True] for a in faits] + [list(a) + [False] for a in negatifs_sup])
        regles = sorted(_regle_json(r) for r in set(regles) | set(regles_sup))
        return {"premisses": prem, "regles": regles}

    def atome(self, q):
        q = tuple(q)
        if q in self.ferm:
            for regle, atomes in sorted(self.v0):
                if q in atomes:
                    negs = [atomes[0]] if regle[0] == "fait-negatif" else []
                    regles_sup = [] if regle[0] == "fait-negatif" else [regle]
                    return {"etiquette": CONTRADICTION, "valeur": None,
                            "regle_violee": _regle_json(regle),
                            "preuve": self._preuve(self.ferm, atomes, regles_sup, negs)}
            return {"etiquette": DEDUIT, "valeur": True, "preuve": self._preuve(self.ferm, [q])}
        ext = self.ferm.copie_avec(q)
        nouvelles = sorted(violations(ext, self.negatifs, self.regles, self.exclusions) - self.v0)
        if nouvelles:
            regle, atomes = nouvelles[0]
            negs = [atomes[0]] if regle[0] == "fait-negatif" else []
            regles_sup = [] if regle[0] == "fait-negatif" else [regle]
            return {"etiquette": DEDUIT, "valeur": False,
                    "preuve": self._preuve(ext, atomes, regles_sup, negs)}
        return {"etiquette": INDETERMINE, "valeur": None,
                "manque": "aucune règle connue ne relie %s(%s,%s) aux faits connus" % q}

    def exclusion(self, x, y):
        ros = [r[1] for r in self.regles if r[0] == "exclusion_A"]
        if not ros:
            return {"etiquette": INDETERMINE, "valeur": None,
                    "manque": "il manque une règle reliant exclut aux relations"}
        for ro in ros:
            for a in ((ro, x, y), (ro, y, x)):
                if a in self.ferm:
                    return {"etiquette": CONTRADICTION, "valeur": None,
                            "regle_violee": ["exclusion_A", ro],
                            "preuve": self._preuve(self.ferm, [a], [("exclusion_A", ro)])}
        return {"etiquette": DEDUIT, "valeur": True,
                "preuve": {"premisses": [], "regles": [["exclusion_A", r] for r in ros]}}


def verifier_preuve(reponse, question, connus, vraies_regles, exclusions, entites):
    """PREREGISTREMENT §2.3 : prémisses connues, règles vraies, conclusion entraînée."""
    preuve = reponse.get("preuve")
    if not isinstance(preuve, dict):
        return False
    try:
        prem = {(p[0], p[1], p[2]): bool(p[3]) for p in preuve.get("premisses", [])}
        regles = [tuple(r) for r in preuve.get("regles", [])]
    except (TypeError, IndexError, KeyError):
        return False
    connus = {tuple(a): v for a, v in connus.items()}
    if any(connus.get(a) is not v for a, v in prem.items()):
        return False
    vraies = {tuple(r) for r in vraies_regles}
    if any(r not in vraies for r in regles):
        return False
    rais = Raisonneur(prem, regles, exclusions, entites)
    if question["type"] == "atome":
        attendu = rais.atome(question["atome"])
    else:
        attendu = rais.exclusion(*question["paire"])
    return (attendu["etiquette"] == reponse.get("etiquette")
            and attendu.get("valeur") == reponse.get("valeur"))
