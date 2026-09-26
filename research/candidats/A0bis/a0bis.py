"""A0-bis — coût marginal, mémoire par famille, bruit par maximum de vraisemblance (PREREGISTREMENT.md §3).

A0 (`research/candidats/A0/a0.py`) est importé tel quel ; A0-bis en hérite et
remplace trois pièces, chacune désactivable pour ablation (§4) :
  (a) coût d'une requête = R̂₊·C_atome (une requête augmente R ssi ΔE > R·C),
      et valeur de l'information myope d'une instance pour les tests de règles ;
  (b) mémoire indexée par une signature structurelle (variante, profil), avec
      a priori par relation (affectation) et repli global si famille inconnue ;
  (c) bruit estimé par maximum de vraisemblance sur les vérifications faites.
Aucun nom de relation ni d'entité n'est gardé. Aucun tirage aléatoire.
"""

import math
from itertools import permutations

import chemin  # noqa: F401

from a0 import (A0, A_PRIORI_BRUIT, BUDGET, CATEGORIES, DELTA_OUBLI, DELTA_PAS, ERREURS_SUPP, KAPPA_MAX,
                KAPPA_PAS, TYPES, _log, _logit, _logsomexp, _sigmoide, attribuer, etat_initial, instances,
                p_bruit, revelations, valeurs_options, vraisemblances)
from etalons import PROPRIETES
from oracle import C_ATOME, C_EXCLUSION, bits, p_systeme
from raisonneur import DEDUIT, INDETERMINE, Fermeture

D_MAX = 2                  # distance de Hamming max pour ranger un monde dans une famille (§3.2)
SEUIL_IDENTIFICATION = 0.5
PI_BAS, PI_ECART = 0.1, 0.8   # π(r, i) = 0.1 + 0.8·Σ w·bit
MLE_MIN = 5
MLE_BORNES = (0.01, 0.5)
ZERO_NUMERIQUE = 1e-9      # une VOI de cet ordre est un zéro numérique, pas un gain


# --- (a) coût marginal (§3.1) -----------------------------------------------------

def augmente_r(e, b, delta_e, cout=C_ATOME):
    """Vrai si une requête de gain delta_e fait monter R = e/b (calcul direct)."""
    return (e + delta_e) / (b + cout) > e / b


def cout_marginal(r_chapeau, cout=C_ATOME):
    """R̂₊·C : pas de dilution d'un R négatif (garde-fou §3.1)."""
    return max(0.0, r_chapeau) * cout


def rentable(voi, cout):
    return voi > ZERO_NUMERIQUE and voi > cout


def utilite(b, g, l, q):
    return max(0.0, b * g + (1 - b) * (q * g - (1 - q) * l))


def voi_instance(b, g, l, q, eta_, m):
    """VOI myope d'une requête sur le conséquent d'une instance à m antécédents non sûrs."""
    eta_m = 1 - (1 - eta_) ** m
    pc = b * (1 - eta_m) + (1 - b) * q
    pv = 1 - pc
    bc = b * (1 - eta_m) / pc if pc > 0 else b
    bv = b * eta_m / pv if pv > 0 else b
    return pc * utilite(bc, g, l, q) + pv * utilite(bv, g, l, q) - utilite(b, g, l, q)


def voi_premisse(p, somme_g, somme_l, kappa=1.0):
    """Information parfaite sur un fait-prémisse : min(p·κ·ΣL, (1−p)·ΣG)."""
    v = valeurs_options(p, somme_g, somme_l, 0.0, kappa)
    return v["verifier"] - max(v["conclure"], v["indetermine"])


# --- (c) bruit par maximum de vraisemblance (§3.3) --------------------------------

def eta_mle(verifs, cats):
    k = sum(verifs[c][0] for c in cats)
    n = sum(verifs[c][1] for c in cats)
    if n < MLE_MIN:
        return None
    return min(MLE_BORNES[1], max(MLE_BORNES[0], k / n))


def p_bruit_mle(verifs, cat):
    v = eta_mle(verifs, (cat,))
    if v is None:
        v = eta_mle(verifs, CATEGORIES)
    if v is None:
        a, b = A_PRIORI_BRUIT[cat]
        v = a / (a + b)
    return v


def eta_global_mle(verifs):
    v = eta_mle(verifs, ("phase1", "phase2"))
    if v is None:
        v = eta_mle(verifs, CATEGORIES)
    return v if v is not None else (p_bruit_mle(verifs, "phase1") + p_bruit_mle(verifs, "phase2")) / 2


# --- (b) mémoire par famille (§3.2) -----------------------------------------------

def bloc_initial():
    e = etat_initial()
    del e["bruit"], e["kappa"]
    e["r"] = []
    return e


def memoire_initiale():
    return {"globale": bloc_initial(), "familles": [],
            "verifs": {c: [0, 0] for c in CATEGORIES},       # (c) [fausses, vérifications]
            "bruit_a0": {c: [0, 0] for c in CATEGORIES},     # compteurs d'A0 (ablation −bruit-MLE)
            "kappa": 1.0}


def distance_profils(p1, p2):
    """Hamming minimale sur les bijections entre deux multiensembles de 5 vecteurs."""
    return min(sum(a != b for i, j in enumerate(perm) for a, b in zip(p1[i], p2[j]))
               for perm in permutations(range(len(p2)), len(p1)))


def ranger(familles, variante, profil):
    """Indice de la famille où ranger ce profil, ou None (nouvelle famille)."""
    meilleur = None
    for k, f in enumerate(familles):
        if f["variante"] != variante:
            continue
        d = distance_profils(profil, f["representant"])
        if d <= D_MAX and (meilleur is None or d < meilleur[0]):
            meilleur = (d, k)
    return None if meilleur is None else meilleur[1]


def log_vraisemblances(relations, connus, entites, e, qfun):
    return {r: [vraisemblances((p, r), connus, (), entites, e, qfun(p))[:2] for p in PROPRIETES]
            for r in relations}


def _couts(ll, relations, vecs):
    return {(r, j): sum(ll[r][i][0] if vecs[j][i] else ll[r][i][1] for i in range(4))
            for r in relations for j in range(len(vecs))}


def _lw_profil(ll, relations, vecs):
    c = _couts(ll, relations, vecs)
    return _logsomexp([sum(c[(r, s)] for r, s in zip(relations, perm))
                       for perm in permutations(range(len(vecs)), len(relations))])


def frequences_nouveau(profils):
    n_vec = sum(len(pr["vecteurs"]) for pr in profils)
    return [(sum(v[i] for pr in profils for v in pr["vecteurs"]) + 1) / (n_vec + 2) for i in range(4)]


def _lw_nouveau(ll, relations, f):
    return sum(_logsomexp([_log(f[i]) + ll[r][i][0], _log(1 - f[i]) + ll[r][i][1]])
               for r in relations for i in range(4))


def marginale_globale(ll, relations, profils):
    """A priori par type : marginale du mélange de profils (même calcul qu'A0 §3.1)."""
    f = frequences_nouveau(profils)
    comps = [(_lw_nouveau(ll, relations, f), f)]
    for pr in profils:
        vecs = pr["vecteurs"]
        comps.append((_lw_profil(ll, relations, vecs),
                      [(sum(v[i] for v in vecs) + 1) / (len(vecs) + 2) for i in range(4)]))
    z = _logsomexp([c[0] for c in comps])
    w = [math.exp(c[0] - z) for c in comps]
    return {p: sum(wk * c[1][i] for wk, c in zip(w, comps)) for i, p in enumerate(PROPRIETES)}


def identifier(familles, variante, ll, relations, f_nouveau):
    """(indice de la famille identifiée ou None, postérieures) sur les seules observations."""
    cands = [k for k, f in enumerate(familles) if f["variante"] == variante]
    if not cands:
        return None, {}
    lws = {"nouveau": _lw_nouveau(ll, relations, f_nouveau)}
    for k in cands:
        profs = familles[k]["bloc"]["profils"]
        lws[k] = _logsomexp([_lw_profil(ll, relations, pr["vecteurs"]) for pr in profs]) - math.log(len(profs))
    z = _logsomexp(list(lws.values()))
    post = {k: math.exp(v - z) for k, v in lws.items()}
    k = max(cands, key=lambda c: (post[c], -c))
    return (k if post[k] >= SEUIL_IDENTIFICATION else None), post


def a_priori_par_relation(ll, relations, profils):
    """π(r, i) = 0.1 + 0.8·Σ_{profil, bijection} w·vecteur[bijection(r)][i] (§3.2)."""
    termes = []
    for pr in profils:
        vecs = pr["vecteurs"]
        c = _couts(ll, relations, vecs)
        for perm in permutations(range(len(vecs)), len(relations)):
            termes.append((sum(c[(r, s)] for r, s in zip(relations, perm)), vecs, perm))
    z = _logsomexp([t[0] for t in termes])
    pi = {}
    for k, r in enumerate(relations):
        for i, p in enumerate(PROPRIETES):
            pi[(p, r)] = PI_BAS + PI_ECART * sum(math.exp(lw - z) * vecs[perm[k]][i] for lw, vecs, perm in termes)
    return pi


def q_bloc(bloc, t):
    c, n = bloc["q"][t]
    return (c + 1) / (n + 2)


def a_priori_composition_bloc(bloc):
    v, n = bloc["compositions"]
    return (v + 1) / (n + 5)


def r_realise(questions, obs, reponses, surs, p_ref, n_req, n_excl):
    """R du monde recalculé avec les seules informations publiques (§3.1)."""
    e = 0.0
    for q in questions:
        if q["type"] != "atome":
            continue
        a = tuple(q["atome"])
        if a in obs or a not in surs:
            continue
        pr = p_ref[a[0]]
        e += bits(pr, surs[a]) - bits(p_systeme(reponses.get(q["id"], {"etiquette": INDETERMINE}), pr), surs[a])
    b = (len(obs) + n_req) * C_ATOME + n_excl * C_EXCLUSION
    return e / b


def apprendre_bis(mem, k_ident, trace, surs, regles_vraies, variante, r_monde,
                  par_famille=True, bruit_mle=True, autodiagnostic=True, eta_=None):
    """Fin de monde : mise à jour des blocs (famille + global), bruit, autodiagnostic (§3.2, §3.3)."""
    ents, rels = trace["entites"], trace["relations"]
    faits = {a: v for a, (v, _) in trace["obs"].items()}
    faits.update(surs)
    glob = mem["globale"]
    travail = mem["familles"][k_ident]["bloc"] if k_ident is not None else glob

    def verdict(regle):
        if regle in regles_vraies:
            return True
        lt, lf, ref = vraisemblances(regle, faits, surs, ents, eta_, q_bloc(travail, regle[0]))
        return not ref and lt - lf > 0

    vecteurs, fausses = [], []
    for r in rels:
        v = []
        for p in PROPRIETES:
            ok = verdict((p, r))
            v.append(int(ok))
            if not ok:
                fausses.append((p, r))
        vecteurs.append(v)
    profil = sorted(vecteurs)
    comps = sorted(set(trace["compositions"]))
    n_vraies = 0
    for c in comps:
        ok = verdict(c)
        n_vraies += ok
        if not ok:
            fausses.append(c)

    k_range = None
    if par_famille:
        k_range = ranger(mem["familles"], variante, profil)
        if k_range is None:
            mem["familles"].append({"variante": variante, "representant": profil, "bloc": bloc_initial()})
            k_range = len(mem["familles"]) - 1
    cibles = [glob] + ([mem["familles"][k_range]["bloc"]] if k_range is not None else [])
    q_inc = {t: [0, 0] for t in TYPES}
    for regle in fausses:
        for ants, cons, att in instances(regle, faits, ents):
            if cons in faits and all(a in surs for a in ants + (cons,)):
                q_inc[regle[0]][0] += faits[cons] == att
                q_inc[regle[0]][1] += 1
    for bl in cibles:
        for t in TYPES:
            bl["q"][t][0] += q_inc[t][0]
            bl["q"][t][1] += q_inc[t][1]
        bl["profils"].append({"vecteurs": profil, "compositions": n_vraies})
        bl["compositions"][0] += n_vraies
        bl["compositions"][1] += len(comps)
        bl["r"].append(r_monde)

    cats = {a: trace["cat"].get(a, "phase%d" % ph) for a, (_, ph) in trace["obs"].items()}
    if not bruit_mle:   # compteurs d'A0 : faits observés révélés (requêtes + correction)
        for a, (v, _) in sorted(trace["obs"].items()):
            if a in surs:
                mem["bruit_a0"][cats[a]][0] += v != surs[a]
                mem["bruit_a0"][cats[a]][1] += 1

    diag = []
    if autodiagnostic:
        blocs_delta = [glob] + ([travail] if travail is not glob else [])
        qs = {q["id"]: q for q in trace["questions"]}
        fautifs = set()
        for qid in sorted(trace["reponses"]):
            rep, q = trace["reponses"][qid], qs[qid]
            if q["type"] != "atome" or rep.get("etiquette") != DEDUIT:
                continue
            a = tuple(q["atome"])
            if a not in surs or surs[a] == rep.get("valeur"):
                continue
            piece = attribuer(rep, faits, surs, trace["req"], ents, eta_, travail, cats)
            diag.append([qid, piece[0]])
            if piece[0] == "propriete":
                for bl in blocs_delta:
                    bl["delta"][piece[1]] += DELTA_PAS
                fautifs.add(piece[1])
            elif piece[0] == "premisse":
                if not bruit_mle:   # (c) : une faute attribuée ne touche plus au bruit
                    mem["bruit_a0"][piece[1]][0] += ERREURS_SUPP
                    mem["bruit_a0"][piece[1]][1] += ERREURS_SUPP
            else:
                mem["kappa"] = min(KAPPA_MAX, mem["kappa"] * KAPPA_PAS)
        for bl in blocs_delta:
            for t in TYPES:
                if t not in fautifs:
                    bl["delta"][t] = max(0.0, bl["delta"][t] - DELTA_OUBLI)
    return {"diagnostic": diag, "famille_rangee": k_range, "profil": profil}


# --- le système ------------------------------------------------------------------

class A0Bis(A0):
    nom = "a0bis"
    COUT_MARGINAL = True
    MEMOIRE_FAMILLE = True
    BRUIT_MLE = True

    def __init__(self):
        super().__init__()
        self.memoire = memoire_initiale()
        self.journal = []

    def debut_monde(self, vue):
        super().debut_monde(vue)
        self.k_ident, self.r_chapeau, self.post = None, None, {}
        self.pi = None

    # --- bruit -------------------------------------------------------------------

    def _p(self, cat):
        if self.BRUIT_MLE:
            return p_bruit_mle(self.memoire["verifs"], cat)
        return p_bruit({"bruit": self.memoire["bruit_a0"]}, cat)

    def _eta(self):
        if self.BRUIT_MLE:
            return eta_global_mle(self.memoire["verifs"])
        return (self._p("phase1") + self._p("phase2")) / 2

    def _demander(self, a):
        v = super()._demander(a)
        if v is not None and a in self.obs:
            c = self.memoire["verifs"][self._categorie(a)]
            c[0] += self.obs[a][0] != v
            c[1] += 1
        return v

    # --- mémoire de travail --------------------------------------------------------

    def _bloc(self):
        if self.k_ident is not None:
            return self.memoire["familles"][self.k_ident]["bloc"]
        return self.memoire["globale"]

    def _cout(self):
        return cout_marginal(self.r_chapeau) if self.COUT_MARGINAL else C_ATOME

    def _preparer(self):
        rels, ents = self.vue["relations"], self.vue["entites"]
        obs = {a: v for a, (v, _) in self.obs.items()}
        glob = self.memoire["globale"]
        e = self._eta()
        ll = log_vraisemblances(rels, obs, ents, e, lambda t: q_bloc(glob, t))
        self.k_ident, self.post, self.pi = None, {}, None
        if self.MEMOIRE_FAMILLE:
            self.k_ident, self.post = identifier(self.memoire["familles"], self.vue["semantique"]["variante"],
                                                 ll, rels, frequences_nouveau(glob["profils"]))
        bloc = self._bloc()
        if self.k_ident is not None:
            ll_f = log_vraisemblances(rels, obs, ents, e, lambda t: q_bloc(bloc, t))
            self.pi = a_priori_par_relation(ll_f, rels, bloc["profils"])
        if self.r_chapeau is None:   # figé pour le monde (§3.1)
            rs = bloc["r"]
            self.r_chapeau = sum(rs) / len(rs) if rs else 0.0
        # A0._preparer calcule p_ref, q_atomes, compositions candidates et self.prior (via self.etat) :
        # on lui présente un état de travail sans nom, puis on remplace les a priori.
        self.etat = {"profils": glob["profils"], "q": bloc["q"], "bruit": self.memoire["bruit_a0"],
                     "compositions": bloc["compositions"], "delta": bloc["delta"], "kappa": self.memoire["kappa"]}
        super()._preparer()
        self.prior = marginale_globale(ll, rels, glob["profils"])
        self.prior["composition"] = a_priori_composition_bloc(bloc)

    def croyance(self, regle, connus):
        t = regle[0]
        bloc = self._bloc()
        lt, lf, ref = vraisemblances(regle, connus, self.req, self.vue["entites"], self._eta(), q_bloc(bloc, t))
        if ref:
            return 0.0, True
        a_priori = self.pi[(t, regle[1])] if (self.pi is not None and t in PROPRIETES) else self.prior[t]
        z = _logit(a_priori) - bloc["delta"][t] + (lt - lf)
        return _sigmoide(z), False

    # --- étape 1 : règles, VOI d'une instance ---------------------------------------

    def _instance_a_tester(self, regle, connus):
        cands = []
        for ants, cons, _ in instances(regle, connus, self.vue["entites"]):
            if cons not in connus and cons not in self.refuses:
                cands.append((sum(1 for a in ants if a not in self.req), cons))
        return min(cands) if cands else None

    def evaluer_regles(self):
        connus = self._connus()
        pos = sorted(a for a, v in connus.items() if v)
        infos = []
        for regle in self.candidats:
            b, ref = self.croyance(regle, connus)
            if not ref:
                infos.append((regle, b))
        infos.sort(key=lambda x: (-x[1], x[0]))
        utilisees, ferm, scores = [], Fermeture(pos, [], self.vue["entites"]), []
        e, cout, bloc = self._eta(), self._cout(), self._bloc()
        for regle, b in infos:
            g, l, f2 = self._marginal(regle, utilisees, pos, ferm, connus)
            q = q_bloc(bloc, regle[0])
            if b * g + (1 - b) * (q * g - (1 - q) * l) > 0:
                utilisees.append(regle)
                if f2 is not None:
                    ferm = f2
            inst = self._instance_a_tester(regle, connus)
            if inst is None:
                continue
            voi = voi_instance(b, g, l, q, e, inst[0])
            if rentable(voi, cout):
                scores.append((voi - cout, regle, inst[1]))
        return utilisees, sorted(scores, key=lambda s: (-s[0], s[1]))

    def _etape_regles(self):
        while True:
            self.utilisees, scores = self.evaluer_regles()
            if self.nb_req >= BUDGET or not scores:
                return
            self._demander(scores[0][2])

    # --- étape 2 : faits-prémisses ------------------------------------------------

    def _etape_declencheur(self):
        ecartes = set()
        cout = self._cout()
        while True:
            reps = self._repondre(ecartes)
            stats = self.statistiques_premisses(reps)
            kappa = self.memoire["kappa"]
            meilleur, a_ecarter = None, set()
            for a in sorted(stats):
                g, l, gc = stats[a]
                p = self._p(self._categorie(a))
                v = valeurs_options(p, g, l, 0.0, kappa)
                if v["indetermine"] > v["conclure"]:
                    a_ecarter.add(a)
                if self.nb_req >= BUDGET:
                    continue
                voi = max(voi_premisse(p, g, l, kappa), p * gc)
                if rentable(voi, cout) and (meilleur is None or voi - cout > meilleur[0]):
                    meilleur = (voi - cout, a)
            if meilleur is not None:
                self._demander(meilleur[1])
                continue
            if a_ecarter - ecartes:
                ecartes |= a_ecarter
                continue
            return reps

    # --- fin de monde ----------------------------------------------------------------

    def fin_monde(self, correction):
        surs, regles_vraies = revelations(self.vue["questions"], correction)
        surs.update(self.req)
        r_monde = r_realise(self.vue["questions"], self.obs, self.reponses, surs, self.p_ref,
                            self.nb_req, len(self.vue["exclusions"]))
        out = apprendre_bis(self.memoire, self.k_ident, self.trace(), surs, regles_vraies,
                            self.vue["semantique"]["variante"], r_monde, par_famille=self.MEMOIRE_FAMILLE,
                            bruit_mle=self.BRUIT_MLE, autodiagnostic=self.AUTODIAGNOSTIC, eta_=self._eta())
        out.update({"r_realise": r_monde, "famille_identifiee": self.k_ident, "r_chapeau": self.r_chapeau})
        self.journal.append(out)
        self.diagnostics.append(out["diagnostic"])

    def proprietes_crues(self):
        return {"regles": [list(r) for r in self.utilisees], "requetes": self.nb_req,
                "famille_identifiee": self.k_ident, "familles_en_memoire": len(self.memoire["familles"]),
                "r_chapeau": self.r_chapeau, "cout_marginal": self._cout(), "kappa": self.memoire["kappa"],
                "eta": self._eta(), "p_bruit": {c: self._p(c) for c in CATEGORIES},
                "verifications": {c: list(v) for c, v in sorted(self.memoire["verifs"].items())}}


class A0BisSansCoutMarginal(A0Bis):
    nom = "a0bis_sans_cout_marginal"
    COUT_MARGINAL = False


class A0BisSansMemoireFamille(A0Bis):
    nom = "a0bis_sans_memoire_famille"
    MEMOIRE_FAMILLE = False


class A0BisSansBruitMLE(A0Bis):
    nom = "a0bis_sans_bruit_mle"
    BRUIT_MLE = False


CONFIGURATIONS = (A0Bis, A0BisSansCoutMarginal, A0BisSansMemoireFamille, A0BisSansBruitMLE)
