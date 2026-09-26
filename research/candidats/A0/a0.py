"""A0 — premier système candidat « ACQUÉRIR » (PREREGISTREMENT.md §3).

Trois pièces, chacune désactivable pour ablation (§4) :
  - mémoire inter-mondes des propriétés (§3.1) : bibliothèque de profils de
    vecteurs de propriétés, taux de confirmation des règles fausses, a priori
    des compositions, compteurs de bruit. Aucun nom de relation ni d'entité ;
  - déclencheur calibré (§3.2) : conclure / vérifier / INDÉTERMINÉ selon
    P(erreur)·coût(erreur) contre coût(vérification) ;
  - autodiagnostic (§3.3) : chaque DÉDUIT faux en vérité est attribué à une
    pièce, et seule cette pièce est mise à jour.
Aucun tirage aléatoire : tous les parcours se font sur des listes triées.
"""

import math
from itertools import permutations

import chemin  # noqa: F401

from etalons import PROPRIETES, Systeme, regle_semantique
from oracle import C_ATOME, EPSILON
from raisonneur import CONTRADICTION, DEDUIT, Fermeture, Raisonneur

TYPES = PROPRIETES + ("composition",)
DEFINIES = ("reflexive", "symetrique", "transitive", "composition")
CATEGORIES = ("phase1", "phase2", "violation")
A_PRIORI_BRUIT = {"phase1": (1, 9), "phase2": (1, 9), "violation": (1, 1)}
A_PRIORI_PROPRIETE = 0.5
BUDGET = 150
DELTA_PAS, DELTA_OUBLI = 0.5, 0.1
KAPPA_PAS, KAPPA_MAX = 1.1, 4.0
ERREURS_SUPP = 2
PLANCHER = 1e-12
OPTIONS = ("conclure", "indetermine", "verifier")   # ordre = départage des égalités


def _log(x):
    return math.log(max(x, PLANCHER))


def _logit(p):
    p = min(1 - PLANCHER, max(PLANCHER, p))
    return math.log(p / (1 - p))


def _sigmoide(z):
    if z >= 0:
        return 1 / (1 + math.exp(-z))
    e = math.exp(z)
    return e / (1 + e)


def _logsomexp(vals):
    m = max(vals)
    return m + math.log(sum(math.exp(v - m) for v in vals))


# --- coûts (§3.0) et règle du déclencheur (§3.2) --------------------------------

def gain_perte(p_ref, valeur):
    """(G, L) en bits d'un DÉDUIT `valeur` sur un atome non observé, contre p_ref."""
    p = p_ref if valeur else 1 - p_ref
    g = math.log2(1 / p) - math.log2(1 / (1 - EPSILON))
    l = math.log2(1 / EPSILON) - math.log2(1 / (1 - p))
    return g, l


def valeurs_options(p, somme_g, somme_l, cout=C_ATOME, kappa=1.0):
    return {"conclure": (1 - p) * somme_g - p * kappa * somme_l,
            "verifier": (1 - p) * somme_g - cout,
            "indetermine": 0.0}


def decision(p, somme_g, somme_l, cout=C_ATOME, kappa=1.0):
    """Vérifier bat conclure exactement quand p·κ·ΣL > coût (§3.2)."""
    v = valeurs_options(p, somme_g, somme_l, cout, kappa)
    return max(OPTIONS, key=lambda o: v[o])


# --- instances d'une règle (§3.1) ----------------------------------------------

def _succ(connus, r):
    s = {}
    for (rr, x, y) in sorted(a for a, v in connus.items() if v and a[0] == r):
        s.setdefault(x, []).append(y)
    return s


def instances(regle, connus, entites):
    """(antécédents, conséquent, valeur attendue) : antécédents connus vrais."""
    t = regle[0]
    out = []
    if t == "reflexive":
        r = regle[1]
        out = [((), (r, x, x), True) for x in sorted(entites)]
    elif t in ("symetrique", "antisymetrique"):
        r = regle[1]
        vus = set()
        for (_, x, y) in sorted(a for a, v in connus.items() if v and a[0] == r):
            if x == y or (y, x) in vus:
                continue
            vus.add((x, y))
            out.append((((r, x, y),), (r, y, x), t == "symetrique"))
    elif t == "transitive":
        r = regle[1]
        s = _succ(connus, r)
        for x in sorted(s):
            for y in s[x]:
                if y == x:
                    continue
                for z in s.get(y, ()):
                    if z != y:
                        out.append((((r, x, y), (r, y, z)), (r, x, z), True))
    elif t == "composition":
        ri, rj, rk = regle[1], regle[2], regle[3]
        si, sj = _succ(connus, ri), _succ(connus, rj)
        for x in sorted(si):
            for z in si[x]:
                for y in sj.get(z, ()):
                    out.append((((ri, x, z), (rj, z, y)), (rk, x, y), True))
    return out


def vraisemblances(regle, connus, surs, entites, eta, q):
    """(log P(instances | vraie), log P(instances | fausse), réfutée par des faits sûrs)."""
    lt = lf = 0.0
    refutee = False
    for ants, cons, att in instances(regle, connus, entites):
        if cons not in connus:
            continue
        m = sum(1 for a in ants + (cons,) if a not in surs)
        eta_m = 1 - (1 - eta) ** m
        if connus[cons] == att:
            lt += _log(1 - eta_m)
            lf += _log(q)
        else:
            refutee = refutee or m == 0
            lt += _log(eta_m)
            lf += _log(1 - q)
    return lt, lf, refutee


# --- mémoire (§3.1) : état structurel, sans aucun nom ---------------------------

def etat_initial():
    return {
        "profils": [],                                  # {"vecteurs": [[r,s,a,t]…] triés, "compositions": n}
        "q": {t: [0, 0] for t in TYPES},                # [confirmations, instances sûres] des règles fausses
        "bruit": {c: [0, 0] for c in CATEGORIES},       # [erreurs, faits révélés]
        "compositions": [0, 0],                         # [vraies, candidates]
        "delta": {t: 0.0 for t in TYPES},               # marges de l'autodiagnostic
        "kappa": 1.0,
    }


def q_type(etat, t):
    c, n = etat["q"][t]
    return (c + 1) / (n + 2)


def p_bruit(etat, cat):
    a, b = A_PRIORI_BRUIT[cat]
    e, n = etat["bruit"][cat]
    return (a + e) / (a + b + n)


def eta(etat):
    return (p_bruit(etat, "phase1") + p_bruit(etat, "phase2")) / 2


def a_priori_composition(etat):
    v, n = etat["compositions"]
    return (v + 1) / (n + 5)


def a_priori_proprietes(etat, relations, connus, entites):
    """Marginale du mélange de profils pondérés par la vraisemblance des observations."""
    e = eta(etat)
    ll = {r: [vraisemblances((p, r), connus, (), entites, e, q_type(etat, p))[:2] for p in PROPRIETES]
          for r in relations}
    lib = etat["profils"]
    n_vec = sum(len(pr["vecteurs"]) for pr in lib)
    f_nouveau = [(sum(v[i] for pr in lib for v in pr["vecteurs"]) + 1) / (n_vec + 2) for i in range(4)]
    composants = []
    lw = 0.0
    for r in relations:
        for i in range(4):
            lt, lf = ll[r][i]
            lw += _logsomexp([_log(f_nouveau[i]) + lt, _log(1 - f_nouveau[i]) + lf])
    composants.append((lw, f_nouveau))
    for pr in lib:
        vecs = pr["vecteurs"]
        cout = {(r, j): sum(ll[r][i][0] if vecs[j][i] else ll[r][i][1] for i in range(4))
                for r in relations for j in range(len(vecs))}
        lw = _logsomexp([sum(cout[(r, s)] for r, s in zip(relations, perm))
                         for perm in permutations(range(len(vecs)), len(relations))])
        freq = [(sum(v[i] for v in vecs) + 1) / (len(vecs) + 2) for i in range(4)]
        composants.append((lw, freq))
    z = _logsomexp([c[0] for c in composants])
    poids = [math.exp(c[0] - z) for c in composants]
    return {p: sum(w * c[1][i] for w, c in zip(poids, composants)) for i, p in enumerate(PROPRIETES)}


def apprendre(etat, trace, surs, regles_vraies, autodiagnostic):
    """Fin de monde : mise à jour de la mémoire, puis autodiagnostic (§3.1, §3.3).

    trace : {"relations", "entites", "obs": {atome: (valeur, phase)}, "req": {atome: valeur},
             "cat": {atome: catégorie}, "reponses": {qid: réponse}, "questions": [...],
             "compositions": [règles candidates]}
    surs : {atome: vérité} (requêtes + vérités révélées) ; regles_vraies : règles citées par l'oracle.
    """
    ents, rels = trace["entites"], trace["relations"]
    faits = {a: v for a, (v, _) in trace["obs"].items()}
    faits.update(surs)
    e = eta(etat)

    def verdict(regle):
        lt, lf, ref = vraisemblances(regle, faits, surs, ents, e, q_type(etat, regle[0]))
        if regle in regles_vraies:
            return True, False
        return (not ref and lt - lf > 0), ref

    vecteurs, fausses = [], []
    for r in rels:
        v = []
        for p in PROPRIETES:
            ok, _ = verdict((p, r))
            v.append(ok)
            if not ok:
                fausses.append((p, r))
        vecteurs.append(v)
    comps = sorted(set(trace["compositions"]))
    n_vraies = 0
    for c in comps:
        ok, _ = verdict(c)
        n_vraies += ok
        if not ok:
            fausses.append(c)

    # q : confirmations des règles fausses sur instances entièrement sûres
    for regle in fausses:
        for ants, cons, att in instances(regle, faits, ents):
            if cons in faits and all(a in surs for a in ants + (cons,)):
                etat["q"][regle[0]][0] += faits[cons] == att
                etat["q"][regle[0]][1] += 1

    # bruit : faits observés dont la vérité est révélée, par catégorie
    cats = {a: trace["cat"].get(a, "phase%d" % ph) for a, (_, ph) in trace["obs"].items()}
    for a, (v, _) in sorted(trace["obs"].items()):
        if a in surs:
            cat = cats[a]
            etat["bruit"][cat][0] += v != surs[a]
            etat["bruit"][cat][1] += 1

    etat["profils"].append({"vecteurs": sorted(vecteurs), "compositions": n_vraies})
    etat["compositions"][0] += n_vraies
    etat["compositions"][1] += len(comps)

    diag = []
    if autodiagnostic:
        qs = {q["id"]: q for q in trace["questions"]}
        types_fautifs = set()
        for qid in sorted(trace["reponses"]):
            rep, q = trace["reponses"][qid], qs[qid]
            if q["type"] != "atome" or rep.get("etiquette") != DEDUIT:
                continue
            a = tuple(q["atome"])
            if a not in surs or surs[a] == rep.get("valeur"):
                continue
            piece = attribuer(rep, faits, surs, trace["req"], ents, e, etat, cats)
            diag.append([qid, piece[0]])
            if piece[0] == "propriete":
                etat["delta"][piece[1]] += DELTA_PAS
                types_fautifs.add(piece[1])
            elif piece[0] == "premisse":
                etat["bruit"][piece[1]][0] += ERREURS_SUPP
                etat["bruit"][piece[1]][1] += ERREURS_SUPP
            else:
                etat["kappa"] = min(KAPPA_MAX, etat["kappa"] * KAPPA_PAS)
        for t in TYPES:
            if t not in types_fautifs:
                etat["delta"][t] = max(0.0, etat["delta"][t] - DELTA_OUBLI)
    return diag


def attribuer(rep, faits, surs, req, entites, e, etat, cat):
    """Pièce fautive d'un DÉDUIT faux (§3.3) : ("propriete", type) | ("premisse", catégorie) | ("seuil",)."""
    preuve = rep.get("preuve", {})
    for regle in sorted(tuple(r) for r in preuve.get("regles", [])):
        if regle[0] in TYPES and vraisemblances(regle, faits, surs, entites, e, q_type(etat, regle[0]))[2]:
            return ("propriete", regle[0])
    fautives = {cat[a] for a, v in (((p[0], p[1], p[2]), p[3]) for p in preuve.get("premisses", []))
                if a not in req and a in surs and surs[a] != v}
    for c in ("violation", "phase2", "phase1"):   # ordre sans nom : la plus spécifique d'abord
        if c in fautives:
            return ("premisse", c)
    return ("seuil",)


def revelations(questions, correction):
    """Ce que la correction de fin de monde révèle : vérités d'atomes, règles citées par l'oracle."""
    surs, regles_vraies = {}, set()
    for q in questions:
        c = correction[q["id"]]
        if q["type"] == "atome" and c.get("verite") is not None:
            surs[tuple(q["atome"])] = c["verite"]
        att = c["attendu"]
        for r in att.get("preuve", {}).get("regles", []):
            if r[0] in TYPES:
                regles_vraies.add(tuple(r))
        rv = att.get("regle_violee")
        if rv and rv[0] in TYPES:
            regles_vraies.add(tuple(rv))
    return surs, regles_vraies


# --- le système ------------------------------------------------------------------

class A0(Systeme):
    nom = "a0"
    MEMOIRE = True
    DECLENCHEUR = "calibre"        # "calibre" | "toujours" | "jamais"
    AUTODIAGNOSTIC = True

    def __init__(self):
        self.etat = etat_initial()
        self.diagnostics = []

    # --- cycle de vie -----------------------------------------------------------

    def debut_monde(self, vue):
        super().debut_monde(vue)
        if not self.MEMOIRE:
            self.etat = etat_initial()
        self.req, self.refuses, self.nb_req = {}, set(), 0
        self.cat, self.reponses, self.utilisees = {}, {}, []
        self.comps_monde = set()

    def phase(self, p, observations, demander):
        self._dem = demander
        for r, x, y, v in observations:
            self.obs[(r, x, y)] = (v, p)
        self._preparer()
        self._etape_regles()
        self.reponses = self._etape_declencheur()
        return self.reponses

    def fin_monde(self, correction):
        surs, regles_vraies = revelations(self.vue["questions"], correction)
        surs.update(self.req)
        self.diagnostics.append(apprendre(self.etat, self.trace(), surs, regles_vraies, self.AUTODIAGNOSTIC))

    def trace(self):
        return {"relations": list(self.vue["relations"]), "entites": list(self.vue["entites"]),
                "obs": dict(self.obs), "req": dict(self.req), "cat": dict(self.cat),
                "reponses": dict(self.reponses), "questions": list(self.vue["questions"]),
                "compositions": sorted(self.comps_monde)}

    def proprietes_crues(self):
        return {"regles": [list(r) for r in self.utilisees] + regle_semantique(self.vue),
                "requetes": self.nb_req, "kappa": self.etat["kappa"],
                "delta": dict(self.etat["delta"]), "profils_en_memoire": len(self.etat["profils"])}

    # --- faits ------------------------------------------------------------------

    def _connus(self):
        k = {a: v for a, (v, _) in self.obs.items()}
        k.update(self.req)
        return k

    def _demander(self, a):
        v = self._dem(*a)
        if v is None:
            self.refuses.add(a)
        else:
            self.req[a] = v
            self.nb_req += 1
        return v

    def _categorie(self, a):
        return self.cat.get(a) or "phase%d" % self.obs[a][1]

    # --- préparation d'une phase -----------------------------------------------

    def _preparer(self):
        rels, ents = self.vue["relations"], self.vue["entites"]
        pos, tot = {}, {}
        for (r, _, _), (v, _) in self.obs.items():
            tot[r] = tot.get(r, 0) + 1
            pos[r] = pos.get(r, 0) + v
        self.p_ref = {r: (pos.get(r, 0) + 1) / (tot.get(r, 0) + 2) for r in rels}
        self.q_atomes = sorted(tuple(q["atome"]) for q in self.vue["questions"]
                               if q["type"] == "atome" and tuple(q["atome"]) not in self.obs)
        obs = {a: v for a, (v, _) in self.obs.items()}
        self.prior = a_priori_proprietes(self.etat, rels, obs, ents)
        self.prior["composition"] = a_priori_composition(self.etat)
        connus = self._connus()
        comps = []
        for ri in rels:
            for rj in rels:
                if ri == rj:
                    continue
                sj = _succ(connus, rj)
                chaines = [(x, z, y) for (_, x, z) in sorted(a for a, v in connus.items() if v and a[0] == ri)
                           for y in sj.get(z, ())]
                if not chaines:
                    continue
                for rk in rels:
                    if rk in (ri, rj):
                        continue
                    vals = [connus[(rk, x, y)] for x, _, y in chaines if (rk, x, y) in connus]
                    if vals and all(vals):
                        comps.append(("composition", ri, rj, rk))
        self.comps_monde |= set(comps)
        self.candidats = [(p, r) for r in rels for p in PROPRIETES] + sorted(self.comps_monde)

    def croyance(self, regle, connus):
        t = regle[0]
        lt, lf, ref = vraisemblances(regle, connus, self.req, self.vue["entites"],
                                     eta(self.etat), q_type(self.etat, t))
        if ref:
            return 0.0, True
        z = _logit(self.prior[t]) - self.etat["delta"][t] + (lt - lf)
        return _sigmoide(z), False

    # --- étape 1 : règles utilisées et tests (§3.1) -----------------------------

    def _marginal(self, regle, utilisees, pos, ferm, connus):
        t = regle[0]
        if t in DEFINIES:
            f2 = Fermeture(pos, [r for r in utilisees if r[0] in DEFINIES] + [regle], self.vue["entites"])
            nouveaux = [(a, True) for a in self.q_atomes if a in f2 and a not in ferm and a not in connus]
        else:
            r = regle[1]
            f2 = None
            nouveaux = [(a, False) for a in self.q_atomes
                        if a[0] == r and a[1] != a[2] and a not in ferm and a not in connus
                        and (r, a[2], a[1]) in ferm]
        g = l = 0.0
        for a, v in nouveaux:
            gg, ll = gain_perte(self.p_ref[a[0]], v)
            g += gg
            l += ll
        return g, l, f2

    def evaluer_regles(self):
        """Choix glouton des règles utilisées, et valeur d'un test pour chacune."""
        connus = self._connus()
        pos = sorted(a for a, v in connus.items() if v)
        infos = []
        for regle in self.candidats:
            b, ref = self.croyance(regle, connus)
            if not ref:
                infos.append((regle, b))
        infos.sort(key=lambda x: (-x[1], x[0]))
        utilisees, ferm, scores = [], Fermeture(pos, [], self.vue["entites"]), []
        for regle, b in infos:
            g, l, f2 = self._marginal(regle, utilisees, pos, ferm, connus)
            q = q_type(self.etat, regle[0])
            if b * g + (1 - b) * (q * g - (1 - q) * l) > 0:
                utilisees.append(regle)
                if f2 is not None:
                    ferm = f2
                p_faute, cout = 1 - b, (1 - q) * l - q * g
            else:
                p_faute, cout = b, g
            scores.append((p_faute * cout - C_ATOME, regle))
        return utilisees, sorted(scores, key=lambda s: (-s[0], s[1]))

    def _a_tester(self, regle, connus):
        cands = []
        for ants, cons, _ in instances(regle, connus, self.vue["entites"]):
            if cons not in connus and cons not in self.refuses:
                cands.append((sum(1 for a in ants if a not in self.req), cons))
        return min(cands)[1] if cands else None

    def _etape_regles(self):
        while True:
            self.utilisees, scores = self.evaluer_regles()
            if self.nb_req >= BUDGET:
                return
            connus = self._connus()
            for score, regle in scores:
                if score <= 0:
                    return
                a = self._a_tester(regle, connus)
                if a is not None:
                    self._demander(a)
                    break
            else:
                return

    # --- étape 2 : déclencheur sur les faits-prémisses (§3.2) -------------------

    def _repondre(self, ecartes):
        connus = {a: v for a, v in self._connus().items() if a not in ecartes}
        regles = [list(r) for r in self.utilisees] + regle_semantique(self.vue)
        rais = Raisonneur(connus, regles, self.vue["exclusions"], self.vue["entites"])
        reps = {}
        for q in self.vue["questions"]:
            reps[q["id"]] = rais.atome(q["atome"]) if q["type"] == "atome" else rais.exclusion(*q["paire"])
        for _, ats in sorted(rais.v0):
            for a in ats:
                if a in self.obs and a not in self.req:
                    self.cat[a] = "violation"
        for rep in reps.values():
            if rep["etiquette"] == CONTRADICTION:
                for p in rep["preuve"]["premisses"]:
                    a = (p[0], p[1], p[2])
                    if a in self.obs and a not in self.req:
                        self.cat[a] = "violation"
        return reps

    def _premisses_non_verifiees(self, rep):
        out = []
        for p in rep.get("preuve", {}).get("premisses", []):
            a = (p[0], p[1], p[2])
            if a in self.obs and a not in self.req and a not in self.refuses:
                out.append(a)
        return out

    def statistiques_premisses(self, reps):
        """{fait: [ΣG, ΣL, ΣG_contradiction]} sur les questions non observées."""
        stats = {}
        for q in sorted(self.vue["questions"], key=lambda q: q["id"]):
            if q["type"] != "atome" or tuple(q["atome"]) in self.obs:
                continue
            rep, pr = reps[q["id"]], self.p_ref[q["atome"][0]]
            if rep["etiquette"] == DEDUIT:
                g, l = gain_perte(pr, rep["valeur"])
                for a in self._premisses_non_verifiees(rep):
                    s = stats.setdefault(a, [0.0, 0.0, 0.0])
                    s[0] += g
                    s[1] += l
            elif rep["etiquette"] == CONTRADICTION:
                gc = min(gain_perte(pr, True)[0], gain_perte(pr, False)[0])
                for a in self._premisses_non_verifiees(rep):
                    stats.setdefault(a, [0.0, 0.0, 0.0])[2] += gc
        return stats

    def _etape_declencheur(self):
        ecartes = set()
        while True:
            reps = self._repondre(ecartes)
            if self.DECLENCHEUR == "jamais":
                return reps
            if self.DECLENCHEUR == "toujours":
                a_faire = sorted({a for rep in reps.values() if rep["etiquette"] in (DEDUIT, CONTRADICTION)
                                  for a in self._premisses_non_verifiees(rep)})
                if not a_faire:
                    return reps
                for a in a_faire:
                    self._demander(a)
                continue
            stats = self.statistiques_premisses(reps)
            kappa = self.etat["kappa"]
            meilleur, a_ecarter = None, set()
            for a in sorted(stats):
                g, l, gc = stats[a]
                p = p_bruit(self.etat, self._categorie(a))
                v = valeurs_options(p, g, l, C_ATOME, kappa)
                if v["indetermine"] > v["conclure"]:
                    a_ecarter.add(a)
                if self.nb_req >= BUDGET:
                    continue
                benef = max(v["verifier"] - max(v["conclure"], v["indetermine"]), p * gc - C_ATOME)
                if benef > 0 and (meilleur is None or benef > meilleur[0]):
                    meilleur = (benef, a)
            if meilleur is not None:
                self._demander(meilleur[1])
                continue
            if a_ecarter - ecartes:
                ecartes |= a_ecarter
                continue
            return reps


class A0SansMemoire(A0):
    nom = "a0_sans_memoire"
    MEMOIRE = False


class A0VerifieToujours(A0):
    nom = "a0_verifie_toujours"
    DECLENCHEUR = "toujours"


class A0VerifieJamais(A0):
    nom = "a0_verifie_jamais"
    DECLENCHEUR = "jamais"


class A0SansAutodiagnostic(A0):
    nom = "a0_sans_autodiagnostic"
    AUTODIAGNOSTIC = False


CONFIGURATIONS = (A0, A0SansMemoire, A0VerifieToujours, A0VerifieJamais, A0SansAutodiagnostic)
