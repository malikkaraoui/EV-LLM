"""E015 -- phase B : recherche autonome d'un assemblage (evolution + vie), reprise sur point de controle.

  python compose.py --runs EVO-N1-s0            # pilote
  python compose.py --runs EVO-N1-s1 ALEA-N1-s1 ...   # relancer jusqu'a "FILE TERMINEE"
Run = <COND>-<TACHE>-s<graine>, COND in EVO, ALEA, SANSVIE, FROID, CHAUD.
Sortie : runs/<run>/resultat.json (+ programme.pkl, etat.pkl pendant la recherche).
"""
import argparse
import json
import os
import pickle
import time
from multiprocessing import Pool

import numpy as np

import programmes as PG
from d15 import exact_par_jeu, evaluer, jeu_val, lot_train

ICI = os.path.dirname(os.path.abspath(__file__))


def hp():
    return json.load(open(os.path.join(ICI, "hyperparametres.json")))["composition"]


def charge_lib(graine):
    return pickle.load(open(os.path.join(ICI, "runs", f"lib-s{graine}", "bibliotheque.pkl"), "rb"))


def decoupe_nom(run):
    cond, tache, s = run.split("-")
    return cond, tache, int(s[1:])


def systeme(prog, lib, tache):
    def f(items):
        reps, pmin, _ = PG.executer(prog, lib, items, tache)
        return list(zip(reps, pmin))
    return f


def val_exact(prog, lib, tache):
    recs = evaluer(systeme(prog, lib, tache), jeu_val(tache), "val", tache)
    return sum(r["juste"] for r in recs) / len(recs)


def signature(prog, lib):
    return "\n".join(PG.lisible(PG.net(prog), lib))


class Recherche:
    def __init__(self, run):
        self.run = run
        self.cond, self.tache, self.graine = decoupe_nom(run)
        H = hp()
        self.H = H
        self.lib = charge_lib(self.graine)
        self.juge = PG.Juge(self.lib, self.tache)
        self.rng = np.random.default_rng([100_000 + self.graine, hash_cond(self.cond, self.tache)])
        self.n_prop = 0 if self.cond == "SANSVIE" else H["vie"]
        self.gen = 0
        self.pop = []          # [(score, exact, prog)]
        self.cands = {}        # signature -> {prog, essais, score256}
        self.traj = []
        self.sans_champion = {"n": 0, "exemple": None, "max_score": 0.0}
        self.fini = False

    # -- un individu : vie puis candidature
    def vivre(self, prog, items):
        prog, s, ex = PG.vie(self.rng, prog, self.juge, items, self.n_prop)
        if not PG.a_un_champion(prog) and s > 0:
            self.sans_champion["n"] += 1
            if s > self.sans_champion["max_score"]:
                self.sans_champion.update(max_score=s, exemple=PG.lisible(prog, self.lib))
        if ex == 1.0:
            sig = signature(prog, self.lib)
            if sig not in self.cands:
                big = lot_train(self.tache, self.graine, 1_000_000 + self.juge.essais,
                                self.H["rejuge"])
                s2, ex2, _ = self.juge(prog, big)
                if ex2 == 1.0:
                    self.cands[sig] = {"prog": PG.copie(prog), "essais": self.juge.essais,
                                       "score256": s2, "gen": self.gen}
        return (s, ex, prog)

    def initiale(self, items):
        if self.cond == "CHAUD":
            src = json_prog(os.path.join(ICI, "runs", f"ECH0-N1-s{self.graine}", "resultat.json"))
            progs = [src] + [PG.mute(self.rng, src, self.lib) for _ in range(self.H["mu"] - 1)]
        elif self.cond.startswith("ECH"):
            progs = [echafaudage(self.cond, self.rng, self.lib) for _ in range(self.H["mu"])]
        else:
            progs = [PG.prog_alea(self.rng, self.lib) for _ in range(self.H["mu"])]
        return [self.vivre(p, items) for p in progs]

    def pas(self):
        items = lot_train(self.tache, self.graine, self.gen)
        H = self.H
        if self.gen == 0:
            self.pop = self.initiale(items)
        elif self.cond == "ALEA":
            self.pop = [self.vivre(PG.prog_alea(self.rng, self.lib), items)
                        for _ in range(H["lam"])]
        else:
            parents = []
            for _, _, p in self.pop:                       # parents rejuges sur le lot neuf
                s, ex, _ = self.juge(p, items)
                parents.append((s, ex, p))
            enfants = []
            for _ in range(H["lam"]):
                i, j = self.rng.integers(0, len(parents), 2)
                par = parents[i] if parents[i][0] >= parents[j][0] else parents[j]
                enfants.append(self.vivre(PG.mute(self.rng, par[2], self.lib), items))
            tous = parents + enfants
            ordre = sorted(range(len(tous)),
                           key=lambda k: (-tous[k][0], len(tous[k][2]["ins"])))
            self.pop = [tous[k] for k in ordre[: H["mu"]]]
        best = max(self.pop, key=lambda x: x[0])
        self.traj.append([self.gen, self.juge.essais, round(best[0], 4), best[1]])
        self.gen += 1
        if self.juge.essais >= H["budget_essais"]:
            self.fini = True


def hash_cond(cond, tache):
    return {"EVO": 1, "ALEA": 2, "SANSVIE": 3, "FROID": 4, "CHAUD": 5, "ECH0": 6, "ECH1": 7,
            "ECH2": 8}[cond] * 10 + int(tache[1])


def echafaudage(cond, rng, lib):
    """Amendement A1. ECH0 : cablage N1 donne (DECOUPE +, DECOUPE =, INV, INV, CH a 2 ports, INV),
    champion a 2 ports tire au hasard, adaptateurs aleatoires. ECH1 : sans l'INV final.
    ECH2 : seulement les deux DECOUPE (sortie = r1)."""
    from d15 import EGAL, PLUS
    deux = [c for c in range(len(lib)) if lib[c]["ports"] == 2]
    c = int(deux[int(rng.integers(0, len(deux)))])
    ins = [{"op": "DEC", "r": [0], "v": PLUS}, {"op": "DEC", "r": [2], "v": EGAL},
           {"op": "INV", "r": [1]}, {"op": "INV", "r": [3]},
           {"op": "CH", "c": c, "r": [5, 6], "A": [PG.adapt_alea(rng), PG.adapt_alea(rng)]},
           {"op": "INV", "r": [7]}]
    if cond == "ECH0":
        return {"ins": ins, "sortie": 8}
    if cond == "ECH1":
        return {"ins": ins[:5], "sortie": 7}
    return {"ins": ins[:2], "sortie": 1}


def prog_json(prog):
    return {"ins": [{k: ([a.tolist() for a in v] if k == "A" else v) for k, v in ins.items()}
                    for ins in prog["ins"]], "sortie": prog["sortie"]}


def json_prog(chemin):
    d = json.load(open(chemin))["programme"]
    return {"ins": [{k: ([np.array(a, dtype=np.int64) for a in v] if k == "A" else v)
                     for k, v in ins.items()} for ins in d["ins"]], "sortie": d["sortie"]}


def conclure(R):
    """Choix par VAL-OOD parmi les 5 meilleurs candidats (a defaut, les 5 meilleurs de la pop)."""
    H = R.H
    cands = sorted(R.cands.values(), key=lambda c: (-c["score256"], len(c["prog"]["ins"]),
                                                    c["essais"]))
    source = "candidats" if cands else "population"
    finalistes = ([c["prog"] for c in cands[:5]] if cands
                  else [p for _, _, p in sorted(R.pop, key=lambda x: -x[0])[:5]])
    vals = [val_exact(p, R.lib, R.tache) for p in finalistes]
    k = max(range(len(finalistes)),
            key=lambda i: (vals[i], -len(PG.utiles(finalistes[i]))))
    prog = finalistes[k]
    # post hoc (mesure, pas choix) : VAL de tous les candidats journalises, dans l'ordre d'arrivee
    post = []
    for c in sorted(R.cands.values(), key=lambda c: c["essais"])[: H["max_cands_val"]]:
        post.append({"essais": c["essais"], "gen": c["gen"],
                     "val": val_exact(c["prog"], R.lib, R.tache),
                     "n_ins_utiles": len(PG.utiles(c["prog"]))})
    raccourcis = [p for p in post if p["val"] < 0.1]
    items = lot_train(R.tache, R.graine, 5_000_000, 256)
    prog_net = PG.net(prog)
    _, _, vus_net = PG.executer(prog_net, R.lib, items, R.tache, trace=True)
    return {
        "run": R.run, "cond": R.cond, "tache": R.tache, "graine": R.graine,
        "essais": R.juge.essais, "generations": R.gen,
        "exemples_uniques": len(R.juge.uniques),
        "n_candidats": len(R.cands),
        "essais_premier_candidat": min((c["essais"] for c in R.cands.values()), default=None),
        "essais_premier_candidat_val99": min((p["essais"] for p in post if p["val"] >= 0.99),
                                             default=None),
        "choix": {"source": source, "val_finalistes": vals, "val": vals[k]},
        "programme": prog_json(prog),
        "programme_net": prog_json(prog_net),
        "lisible": PG.lisible(prog_net, R.lib, {k2: v.tolist() for k2, v in vus_net.items()}),
        "candidats_post_hoc": post,
        "triche": {"raccourcis_val_lt_0.1": len(raccourcis),
                   "sans_champion_score_pos": R.sans_champion},
        "trajectoire": R.traj,
    }


def un_run(run):
    dos = os.path.join(ICI, "runs", run)
    os.makedirs(dos, exist_ok=True)
    if os.path.exists(os.path.join(dos, "resultat.json")):
        return run, "deja fini", 0
    et = os.path.join(dos, "etat.pkl")
    R = pickle.load(open(et, "rb")) if os.path.exists(et) else Recherche(run)
    R.lib = charge_lib(R.graine)
    R.juge.lib = R.lib
    t0 = time.time()
    while not R.fini and time.time() - t0 < hp()["mur_invocation_s"]:
        R.pas()
    lib = R.lib
    R.lib, R.juge.lib = None, None
    pickle.dump(R, open(et, "wb"))
    R.lib, R.juge.lib = lib, lib
    if not R.fini:
        return run, f"reprise ({R.juge.essais} essais)", time.time() - t0
    res = conclure(R)
    res["duree_derniere_invocation_s"] = round(time.time() - t0, 1)
    json.dump(res, open(os.path.join(dos, "resultat.json"), "w"), indent=1)
    pickle.dump(sorted(R.juge.uniques), open(os.path.join(dos, "uniques.pkl"), "wb"))
    return run, f"fini : VAL {res['choix']['val']:.3f}, candidats {res['n_candidats']}, " \
                f"1er {res['essais_premier_candidat']}", time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--proc", type=int, default=6)
    a = ap.parse_args()
    restant = 0
    with Pool(min(a.proc, len(a.runs))) as p:
        for run, msg, d in p.imap_unordered(un_run, a.runs):
            print(f"{run:16s} {msg} ({d:.0f} s)", flush=True)
            restant += msg.startswith("reprise")
    print("FILE TERMINEE" if restant == 0 else f"{restant} run(s) a reprendre")


if __name__ == "__main__":
    main()
