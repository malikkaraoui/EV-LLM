"""Générateur déterministe par graine d'un monde à relations opaques.

Tous les paramètres viennent de PREREGISTREMENT.md §1. Un monde est un dict
sérialisable JSON ; `generer_monde(g)` rend toujours le même monde pour g.
"""

import json
import random

from raisonneur import Fermeture, violations

N_ENTITES = 8
K_RELATIONS = 5
N_TENUS = 60
N_OBS = 96
N_OBS_PHASE1 = 64
N_REVISION = 20
N_REVISION_CONTRA_MAX = 5
N_EXCLUSIONS = 3
BRUIT_MIN, BRUIT_MAX = 0.05, 0.10
P_COMPOSEE = 0.5

BASES = ("ORDRE", "ORDRE_LARGE", "EQUIVALENCE", "SYM_PIEGE", "CYCLE_PIEGE", "AUCUNE_PIEGE")
PIEGES = ("SYM_PIEGE", "CYCLE_PIEGE", "AUCUNE_PIEGE")
ORDRES = ("ORDRE", "ORDRE_LARGE")


def famille(graine):
    return (graine - 1) // 5


def variante(fam):
    return "A" if fam in (0, 2) else "B"


def tirer_profil(fam):
    """Profil d'une famille : 5 emplacements, composition éventuelle, variante."""
    rng = random.Random(1000 + fam)
    var = variante(fam)
    while True:
        slots = [rng.choice(BASES) for _ in range(4)]
        if rng.random() < P_COMPOSEE:
            i, j = rng.sample(range(4), 2)
            slots.append(("COMPOSEE", i, j))
        else:
            slots.append(rng.choice(BASES))
        if sum(1 for s in slots if s in PIEGES) < 2:
            continue
        if var == "A" and not any(s in ORDRES for s in slots):
            continue
        return {"famille": fam, "variante": var, "emplacements": slots}


# --- propriétés mesurées sur la vérité ----------------------------------------

def est_reflexive(rel, n):
    return all((x, x) in rel for x in range(n))


def est_symetrique(rel):
    return all((y, x) in rel for x, y in rel)


def est_antisymetrique(rel):
    return all(x == y or (y, x) not in rel for x, y in rel)


def temoin_non_transitif(rel):
    succ = {}
    for x, y in rel:
        succ.setdefault(x, set()).add(y)
    for x, y in sorted(rel):
        for z in sorted(succ.get(y, ())):
            if (x, z) not in rel:
                return (x, y, z)
    return None


def composer(a, b):
    succ = {}
    for z, y in b:
        succ.setdefault(z, set()).add(y)
    return {(x, y) for x, z in a for y in succ.get(z, ())}


def fermeture_transitive(rel, n):
    rel = set(rel)
    for k in range(n):
        for i in range(n):
            if (i, k) in rel:
                for j in range(n):
                    if (k, j) in rel:
                        rel.add((i, j))
    return rel


# --- générateurs de types ------------------------------------------------------

def gen_type(t, n, rng, rels):
    if t in ORDRES:
        rang = list(range(n))
        rng.shuffle(rang)
        aretes = {(rang[i], rang[j]) for i in range(n) for j in range(i + 1, n) if rng.random() < 0.35}
        rel = fermeture_transitive(aretes, n)
        if t == "ORDRE_LARGE":
            rel |= {(x, x) for x in range(n)}
        return rel
    if t == "EQUIVALENCE":
        nb = rng.randint(2, 4)
        cls = [rng.randrange(nb) for _ in range(n)]
        return {(x, y) for x in range(n) for y in range(n) if cls[x] == cls[y]}
    if t == "SYM_PIEGE":
        rel = set()
        for x in range(n):
            for y in range(x + 1, n):
                if rng.random() < 0.35:
                    rel |= {(x, y), (y, x)}
        return rel
    if t == "CYCLE_PIEGE":
        cls = [rng.randrange(3) for _ in range(n)]
        return {(x, y) for x in range(n) for y in range(n) if cls[y] == (cls[x] + 1) % 3}
    if t == "AUCUNE_PIEGE":
        while True:
            rel = {(x, y) for x in range(n) for y in range(n) if rng.random() < 0.3}
            if not (est_reflexive(rel, n) or est_symetrique(rel) or est_antisymetrique(rel)
                    or temoin_non_transitif(rel) is None):
                return rel
    if isinstance(t, tuple) and t[0] == "COMPOSEE":
        return composer(rels[t[1]], rels[t[2]])
    raise ValueError(t)


def incomparables(rel, n):
    return [(x, y) for x in range(n) for y in range(x + 1, n) if (x, y) not in rel and (y, x) not in rel]


def _instance_valide(slots, rels, n):
    for s, rel in zip(slots, rels):
        if not rel or len(rel) == n * n:
            return False
        if s in PIEGES and temoin_non_transitif(rel) is None:
            return False
        if isinstance(s, tuple) and (rel == rels[s[1]] or rel == rels[s[2]]):
            return False
    return True


def proprietes_vraies(noms, rels, n):
    props = {}
    for nom, rel in zip(noms, rels):
        props[nom] = {
            "reflexive": est_reflexive(rel, n),
            "symetrique": est_symetrique(rel),
            "antisymetrique": est_antisymetrique(rel),
            "transitive": temoin_non_transitif(rel) is None,
        }
    comps = []
    for i in range(len(rels)):
        for j in range(len(rels)):
            if i == j:
                continue
            c = composer(rels[i], rels[j])
            if not c:
                continue
            for k in range(len(rels)):
                if k not in (i, j) and c == rels[k]:
                    comps.append([noms[i], noms[j], noms[k]])
    return props, sorted(comps)


def regles_du_monde(monde):
    """Liste des règles vraies (propriétés + sémantique écrite)."""
    regles = []
    for r in monde["relations"]:
        for p in ("reflexive", "symetrique", "antisymetrique", "transitive"):
            if monde["proprietes"][r][p]:
                regles.append([p, r])
    for c in monde["compositions"]:
        regles.append(["composition"] + c)
    if monde["semantique"]["variante"] == "A":
        regles.append(["exclusion_A", monde["semantique"]["relation"]])
    return regles


def _violations_obs(obs_vals, regles, exclusions, entites):
    pos = [a for a, v in obs_vals.items() if v]
    neg = [a for a, v in obs_vals.items() if not v]
    regles = [tuple(r) for r in regles]
    ferm = Fermeture(pos, [r for r in regles if r[0] != "antisymetrique" and r[0] != "exclusion_A"], entites)
    return violations(ferm, neg, regles, exclusions)


def generer_monde(graine):
    fam = famille(graine)
    profil = tirer_profil(fam)
    slots = profil["emplacements"]
    n = N_ENTITES
    rng = random.Random(graine)
    for _ in range(500):
        rels = []
        for s in slots:
            rels.append(gen_type(s, n, rng, rels))
        if not _instance_valide(slots, rels, n):
            continue
        io = next((i for i, s in enumerate(slots) if s in ORDRES), None)
        if profil["variante"] == "A" and len(incomparables(rels[io], n)) < N_EXCLUSIONS:
            continue
        break
    else:
        raise RuntimeError("aucune instance valide pour la graine %d" % graine)

    entites = ["o%03d" % v for v in rng.sample(range(1000), n)]
    noms_perm = ["R%d" % (i + 1) for i in range(K_RELATIONS)]
    rng.shuffle(noms_perm)  # noms_perm[i] = nom de l'emplacement i
    E = entites
    verite = {noms_perm[i]: sorted([E[x], E[y]] for x, y in rels[i]) for i in range(K_RELATIONS)}
    props, comps = proprietes_vraies(noms_perm, rels, n)
    relations = sorted(noms_perm)
    non_trans = sum(1 for r in relations if not props[r]["transitive"])
    assert non_trans / K_RELATIONS >= 0.30, (graine, non_trans)

    # Exclusions et sémantique écrite
    if profil["variante"] == "A":
        ro = noms_perm[io]
        paires = rng.sample(incomparables(rels[io], n), N_EXCLUSIONS)
        texte = "exclut(x,y) ⇒ ni %s(x,y) ni %s(y,x)" % (ro, ro)
    else:
        ro = None
        toutes = [(x, y) for x in range(n) for y in range(x + 1, n)]
        paires = rng.sample(toutes, N_EXCLUSIONS)
        texte = "aucune règle ne relie exclut aux relations %s" % "…".join([relations[0], relations[-1]])
    exclusions = sorted(sorted([E[x], E[y]]) for x, y in paires)

    # Atomes : tenus à l'écart, observés (2 phases), demandables
    vrai = {(r, a, b) for r in relations for a, b in map(tuple, verite[r])}
    atomes = [(r, a, b) for r in relations for a in E for b in E]
    atomes.sort()
    rng.shuffle(atomes)
    tenus = atomes[:N_TENUS]
    obs = atomes[N_TENUS:N_TENUS + N_OBS]
    phase = {a: (1 if i < N_OBS_PHASE1 else 2) for i, a in enumerate(obs)}
    valeur = {a: (a in vrai) for a in obs}

    # Bruit : une inversion ciblée en phase 2, les autres uniformes
    monde = {"relations": relations, "proprietes": props, "compositions": comps,
             "semantique": {"variante": profil["variante"], "relation": ro, "texte": texte}}
    regles = regles_du_monde(monde)
    excl_t = [tuple(p) for p in exclusions]
    taux = rng.uniform(BRUIT_MIN, BRUIT_MAX)
    nb_bruit = round(taux * N_OBS)
    candidats = [a for a in obs if phase[a] == 2]
    rng.shuffle(candidats)
    cible = None
    for exig_excl in ((True, False) if profil["variante"] == "A" else (False,)):
        for a in candidats:
            essai = dict(valeur)
            essai[a] = not essai[a]
            v = _violations_obs(essai, regles, excl_t, E)
            if v and (not exig_excl or any(r[0] == "exclusion_A" for r, _ in v)):
                cible = a
                break
        if cible:
            break
    bruites = [cible] if cible else []
    reste = [a for a in obs if a != cible]
    bruites += rng.sample(reste, nb_bruit - len(bruites))
    for a in bruites:
        valeur[a] = not valeur[a]

    # Questions : 60 tenus à l'écart + 20 de révision + 3 exclusions
    v_fin = _violations_obs(valeur, regles, excl_t, E)
    en_cause = sorted({a for _, ats in v_fin for a in ats if a in valeur})
    rng.shuffle(en_cause)
    revision = en_cause[:N_REVISION_CONTRA_MAX]
    autres = [a for a in obs if a not in revision]
    revision += rng.sample(autres, N_REVISION - len(revision))
    questions = [{"id": "A:%s:%s:%s" % a, "type": "atome", "atome": list(a)} for a in tenus + revision]
    questions += [{"id": "X:%s:%s" % tuple(p), "type": "exclusion", "paire": list(p)} for p in exclusions]
    rng.shuffle(questions)

    monde.update({
        "graine": graine,
        "famille": fam,
        "profil": [s if isinstance(s, str) else list(s) for s in slots],
        "types": {noms_perm[i]: (s if isinstance(s, str) else "COMPOSEE(%s∘%s)" % (noms_perm[s[1]], noms_perm[s[2]]))
                  for i, s in enumerate(slots)},
        "entites": sorted(E),
        "verite": verite,
        "exclusions": exclusions,
        "taux_bruit": round(taux, 4),
        "observations": [{"atome": list(a), "valeur": valeur[a], "phase": phase[a],
                          "bruit": a in bruites, "cible": a == cible} for a in obs],
        "bruit_cible": list(cible) if cible else None,
        "tenus_a_l_ecart": [list(a) for a in tenus],
        "revision": [list(a) for a in revision],
        "questions": questions,
    })
    return monde


def vers_json(monde):
    return json.dumps(monde, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    import sys
    print(json.dumps(generer_monde(int(sys.argv[1]) if len(sys.argv) > 1 else 1),
                     ensure_ascii=False, indent=1))
