"""E015 -- phase B : programmes (instructions sur registres de flux), execution numpy, juge, mutations.

Instruction : {"op": "DEC", "r": [i], "v": s} | {"op": "INV", "r": [i]} | {"op": "TRQ", "r": [i]}
              | {"op": "CH", "c": champion, "r": [i, ...], "A": [table 14 -> 11, ...]}
Les references de registre sont reduites modulo le nombre de registres disponibles (reparation).
"""
import numpy as np

from circuits import avant
from d15 import ABS, ABSENT_C, CARS, NSYM, phrase, reference

OPS = ["DEC", "INV", "TRQ", "CH"]
MAX_INS = 12


# ------------------------------------------------------------------ execution
def executer(prog, lib, items, tache, trace=False):
    """-> (reponses [str | None], p_min [float], symboles vus par (instr, port) si trace)."""
    n = len(items)
    regs = [[np.array(phrase(tache, it), dtype=np.int64) for it in items]]
    pmin = np.ones(n, dtype=np.float64)
    vus = {}
    for i, ins in enumerate(prog["ins"]):
        R = len(regs)
        if ins["op"] == "DEC":
            src = regs[ins["r"][0] % R]
            av, ap = [], []
            for s in src:
                w = np.nonzero(s == ins["v"])[0]
                if len(w):
                    av.append(s[: w[0]])
                    ap.append(s[w[0] + 1:])
                else:
                    av.append(s)
                    ap.append(s[:0])
            regs += [av, ap]
        elif ins["op"] == "INV":
            regs.append([s[::-1] for s in regs[ins["r"][0] % R]])
        elif ins["op"] == "TRQ":
            regs.append([s[:-1] for s in regs[ins["r"][0] % R]])
        else:
            ch = lib[ins["c"] % len(lib)]
            k = ch["ports"]
            srcs = [regs[ins["r"][p] % R] for p in range(k)]
            lens = np.array([max(len(srcs[p][j]) for p in range(k)) + 1 for j in range(n)])
            T = int(lens.max())
            X = np.full((n, T, k), ABS, dtype=np.int64)
            for p in range(k):
                for j in range(n):
                    s = srcs[p][j]
                    X[j, : len(s), p] = s
            for p in range(k):
                if trace:
                    vus[(i, p)] = np.unique(np.concatenate(
                        [X[j, : lens[j], p] for j in range(n)]))
                X[:, :, p] = ins["A"][p][X[:, :, p]]
            ys, ps = avant(ch["poids"], X)
            out = []
            for j in range(n):
                out.append(ys[j, : lens[j]])
                pmin[j] = min(pmin[j], float(ps[j, : lens[j]].min()))
            regs.append(out)
    fin = regs[prog["sortie"] % len(regs)]
    reps = [decode(s) for s in fin]
    return reps, pmin, vus


def decode(s):
    """Tout symbole non chiffre -> invalide ; retrait de tous les 0 de tete ; vide -> invalide."""
    if len(s) == 0 or (s > 9).any():
        return None
    t = "".join(CARS[int(x)] for x in s).lstrip("0")
    return t or "0"


def a_un_champion(prog):
    return any(ins["op"] == "CH" for ins in prog["ins"])


# ------------------------------------------------------------------ juge (fixe)
def score(reps, items, tache):
    """exact + 0,1 x exactitude par chiffre alignee a droite ; -> (score, exact)."""
    ex, dig = 0, 0.0
    for rep, it in zip(reps, items):
        att = reference(tache, it)
        if rep == att:
            ex += 1
            dig += 1
        elif rep is not None:
            m = sum(1 for q in range(len(att)) if q < len(rep) and rep[-1 - q] == att[-1 - q])
            dig += m / max(len(att), len(rep))
    n = len(items)
    return ex / n + 0.1 * dig / n, ex / n


class Juge:
    """Compte les appels (essais) et les items uniques juges. Les genomes n'y ont pas acces."""

    def __init__(self, lib, tache):
        self.lib, self.tache = lib, tache
        self.essais = 0
        self.uniques = set()

    def __call__(self, prog, items, trace=False):
        self.essais += 1
        self.uniques.update(items)
        reps, _, vus = executer(prog, self.lib, items, self.tache, trace)
        s, ex = score(reps, items, self.tache)
        return s, ex, vus


# ------------------------------------------------------------------ genese et mutations
def adapt_alea(rng):
    return rng.integers(0, ABSENT_C + 1, NSYM).astype(np.int64)


def ins_alea(rng, lib, R):
    op = OPS[int(rng.integers(0, len(OPS)))]
    if op == "DEC":
        return {"op": op, "r": [int(rng.integers(0, R))], "v": int(rng.integers(0, NSYM))}
    if op in ("INV", "TRQ"):
        return {"op": op, "r": [int(rng.integers(0, R))]}
    c = int(rng.integers(0, len(lib)))
    k = lib[c]["ports"]
    return {"op": "CH", "c": c, "r": [int(rng.integers(0, R)) for _ in range(k)],
            "A": [adapt_alea(rng) for _ in range(k)]}


def n_regs_avant(prog, i):
    return 1 + sum(2 if ins["op"] == "DEC" else 1 for ins in prog["ins"][:i])


def prog_alea(rng, lib):
    prog = {"ins": [], "sortie": 0}
    for _ in range(int(rng.integers(3, 9))):
        prog["ins"].append(ins_alea(rng, lib, n_regs_avant(prog, len(prog["ins"]))))
    prog["sortie"] = n_regs_avant(prog, len(prog["ins"])) - 1
    return prog


def copie(prog):
    return {"ins": [dict(ins, r=list(ins["r"]), **({"A": [a.copy() for a in ins["A"]]}
                                                    if "A" in ins else {}))
                    for ins in prog["ins"]], "sortie": prog["sortie"]}


def mute(rng, prog, lib):
    p = copie(prog)
    for _ in range(int(rng.integers(1, 4))):
        q = int(rng.integers(0, 7))
        m = len(p["ins"])
        i = int(rng.integers(0, m)) if m else 0
        if q == 0 and m < MAX_INS:                                  # insertion
            j = int(rng.integers(0, m + 1))
            p["ins"].insert(j, ins_alea(rng, lib, n_regs_avant(p, j)))
        elif q == 1 and m > 1:                                      # suppression
            del p["ins"][i]
        elif q == 2 and m:                                          # remplacement
            p["ins"][i] = ins_alea(rng, lib, n_regs_avant(p, i))
        elif q == 3 and m:                                          # registre
            ins = p["ins"][i]
            ins["r"][int(rng.integers(0, len(ins["r"])))] = int(
                rng.integers(0, n_regs_avant(p, i)))
        elif q == 4 and m and p["ins"][i]["op"] == "DEC":           # symbole de coupe
            p["ins"][i]["v"] = int(rng.integers(0, NSYM))
        elif q == 5 and m and p["ins"][i]["op"] == "CH":            # champion / adaptateur
            ins = p["ins"][i]
            if rng.random() < 0.5:
                c = int(rng.integers(0, len(lib)))
                k = lib[c]["ports"]
                ins["c"] = c
                ins["r"] = (ins["r"] + [0] * k)[:k]
                ins["A"] = (ins["A"] + [adapt_alea(rng) for _ in range(k)])[:k]
            else:
                a = ins["A"][int(rng.integers(0, len(ins["A"])))]
                a[int(rng.integers(0, NSYM))] = int(rng.integers(0, ABSENT_C + 1))
        else:                                                       # sortie
            p["sortie"] = int(rng.integers(0, n_regs_avant(p, len(p["ins"]))))
    return p


def vie(rng, prog, juge, items, budget, s0=None):
    """Apprentissage de vie : balayage par coordonnees des adaptateurs, <= `budget` essais.

    Ordre aleatoire des (port, symbole vu sur ce port) ; pour chacun, les 10 autres valeurs sont
    essayees et la meilleure est gardee si elle ameliore strictement le score.
    """
    s, ex, vus = juge(prog, items, trace=True) if s0 is None else s0
    paires = [(i, q, int(x)) for i, ins in enumerate(prog["ins"]) if ins["op"] == "CH"
              for q in range(len(ins["A"])) for x in vus.get((i, q), [])]
    rng.shuffle(paires)
    used = 0
    for i, q, x in paires:
        if used + ABSENT_C > budget:
            break
        a = prog["ins"][i]["A"][q]
        meilleur = int(a[x])
        for v in range(ABSENT_C + 1):
            if v == meilleur:
                continue
            ancien = int(a[x])
            a[x] = v
            s2, ex2, _ = juge(prog, items)
            used += 1
            if s2 > s:
                s, ex, meilleur = s2, ex2, v
            a[x] = ancien
        a[x] = meilleur
    return prog, s, ex


# ------------------------------------------------------------------ lecture
def lisible(prog, lib, symboles_vus=None):
    """Programme ecrit lisiblement ; adaptateurs reduits aux symboles vus (si fournis)."""
    lignes, R = [], 1
    for i, ins in enumerate(prog["ins"]):
        if ins["op"] == "DEC":
            lignes.append(f"r{R},r{R+1} = DECOUPE(r{ins['r'][0] % R}, '{CARS[ins['v']]}')")
            R += 2
            continue
        if ins["op"] in ("INV", "TRQ"):
            lignes.append(f"r{R} = {ins['op']}(r{ins['r'][0] % R})")
        else:
            ch = lib[ins["c"] % len(lib)]
            args = []
            for q in range(ch["ports"]):
                a = ins["A"][q]
                syms = (symboles_vus.get((i, q), range(NSYM)) if symboles_vus else range(NSYM))
                tab = " ".join(f"{CARS[s]}>{'A' if a[s] == ABSENT_C else a[s]}" for s in syms)
                args.append(f"r{ins['r'][q] % R}[{tab}]")
            lignes.append(f"r{R} = {ch['niche']}#{ins['c'] % len(lib)}({', '.join(args)})")
        R += 1
    lignes.append(f"sortie = r{prog['sortie'] % R}")
    return lignes


def utiles(prog):
    """Indices des instructions dont la sortie depend (analyse arriere des registres)."""
    prod, R = {}, 1
    for i, ins in enumerate(prog["ins"]):
        k = 2 if ins["op"] == "DEC" else 1
        for d in range(k):
            prod[R + d] = i
        R += k
    besoin, garde = {prog["sortie"] % R}, set()
    for i in reversed(range(len(prog["ins"]))):
        ins = prog["ins"][i]
        mes = {r for r, j in prod.items() if j == i}
        if mes & besoin:
            garde.add(i)
            Ravant = n_regs_avant(prog, i)
            besoin |= {r % Ravant for r in ins["r"][: (len(ins["r"]))]}
    return sorted(garde)


def net(prog):
    """Programme reduit aux instructions utiles, registres renumerotes (meme comportement)."""
    garde = set(utiles(prog))
    carte, R, Rn, ins_n = {0: 0}, 1, 1, []
    for i, ins in enumerate(prog["ins"]):
        k = 2 if ins["op"] == "DEC" else 1
        if i in garde:
            nv = dict(ins, r=[carte[r % R] for r in ins["r"]])
            if "A" in ins:
                nv["A"] = [a.copy() for a in ins["A"]]
            ins_n.append(nv)
            for d in range(k):
                carte[R + d] = Rn + d
            Rn += k
        R += k
    return {"ins": ins_n, "sortie": carte[prog["sortie"] % R]}
