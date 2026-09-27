"""E013 -- ADV-PROPAG : propagation pure de la retenue. AJOUT POST HOC, NON PREENREGISTRE.

Demande par le doublage R010 (M0029). Evalue les checkpoints retenus (`meilleur.safetensors`)
des runs I1 et I3 officiels, SANS reentrainement et sans toucher a `eval.jsonl` / `resume.json`.

Jeu, par L = 16, 100, 1000 :
  - 99...9 + 1 et 1 + 99...9 ;
  - N_PROPAG paires (a, b) de L chiffres chacune avec a + b = 10^L et dernier chiffre non nul :
    rang 0 = 10 (genere la retenue), tous les autres rangs = 9 (la retenue ne fait que traverser).
Graine de tirage 3019 (hors 3013-3018 du preenregistrement).
Mesure aussi la part de rangs de propagation (somme des chiffres = 9) dans ADV-CASCADE officiel.

  python adv_propag.py            # -> resultats/adv_propag.json, resultats/adv_propag.md
"""
import json
import os

import numpy as np

import donnees as D
from systemes import charge, details

ICI = os.path.dirname(os.path.abspath(__file__))
LENS = [16, 100, 1000]
N_PROPAG = 100
GRAINE = 3019
CONFIGS = ["I1-H1", "I1-H2", "I1-H4", "I1-H8", "I3-N10", "I3-N100", "I3-N1000", "I3-N10000"]
GRAINES = [1, 2, 3, 4, 5]
SEUIL = 0.9


def _propag(L, rng):
    neuf = int("9" * L)
    items = [(neuf, 1), (1, neuf)]
    vus = set(items)
    while len(items) < 2 + N_PROPAG:
        ch = [int(rng.integers(1, 9))] + [int(rng.integers(0, 10)) for _ in range(L - 2)] \
            + [int(rng.integers(1, 10))]
        a = int("".join(map(str, ch)))
        p = (a, 10 ** L - a)
        if p not in vus:
            vus.add(p)
            items.append(p)
    return items


def jeu_propag():
    rng = np.random.default_rng(GRAINE)
    return {L: _propag(L, rng) for L in LENS}


def rangs_propagation(paires):
    """(rangs de somme 9, rangs ou les deux chiffres existent)."""
    n9 = tot = 0
    for a, b in paires:
        da, db = D.chiffres_lsb(a), D.chiffres_lsb(b)
        for x, y in zip(da, db):
            tot += 1
            n9 += x + y == 9
    return n9, tot


def main():
    jeu = jeu_propag()
    res = {"post_hoc": True, "preenregistre": False, "graine_tirage": GRAINE,
           "n_par_L": {L: len(v) for L, v in jeu.items()}, "par_graine": {}, "par_config": {},
           "part_propagation_adv_cascade": {}}
    for L, it in D.jeux_test()["ADV-CASCADE"].items():
        n9, tot = rangs_propagation(it)
        res["part_propagation_adv_cascade"][L] = round(n9 / tot, 4)
    n9, tot = rangs_propagation([p for it in jeu.values() for p in it[2:]])
    res["part_propagation_adv_propag"] = round(n9 / tot, 4)
    for c in CONFIGS:
        par_L = {L: [] for L in LENS}
        for g in GRAINES:
            nom = f"{c}-s{g}"
            etat = json.load(open(os.path.join(ICI, "runs", nom, "etat.json")))
            m = charge(etat["config"], os.path.join(ICI, "runs", nom, "meilleur.safetensors"))
            ligne = {}
            for L, it in jeu.items():
                d = details(m, it)
                justes = sum(r == str(a + b) for (a, b), (r, _, _) in zip(it, d))
                ligne[L] = {"justes": justes, "n": len(it)}
                par_L[L].append(justes / len(it))
            res["par_graine"][nom] = ligne
            print(nom, " ".join(f"P{L}={v['justes']}/{v['n']}" for L, v in ligne.items()),
                  flush=True)
        res["par_config"][c] = {
            L: {"moy": float(np.mean(v)), "ecart_ddof0": float(np.std(v)),
                "graines_ge_90": int(sum(x >= SEUIL for x in v)), "graines": v}
            for L, v in par_L.items()}
    json.dump(res, open(os.path.join(ICI, "resultats", "adv_propag.json"), "w"), indent=1)

    lignes = ["# ADV-PROPAG (post hoc, non préenregistré ; demandé par R010)", "",
              f"{N_PROPAG} paires a + b = 10^L (L chiffres chacun) + 99…9 + 1 et 1 + 99…9 par L ; "
              f"graine {GRAINE}. Exact-match (%) moyenne ± écart-type de population (ddof 0) "
              "sur 5 graines ; graines ≥ 90 %.", "",
              "| config | P16 | P100 | P1000 | graines ≥ 90 % (16 / 100 / 1000) | par graine "
              "(justes P16/P100/P1000 sur 102) |", "|---|---|---|---|---|---|"]
    for c in CONFIGS:
        pc = res["par_config"][c]
        cel = [f"{100 * pc[L]['moy']:.1f} ± {100 * pc[L]['ecart_ddof0']:.1f}" for L in LENS]
        ge = " / ".join(f"{pc[L]['graines_ge_90']}/5" for L in LENS)
        pg = "; ".join(f"s{g} " + "/".join(str(res["par_graine"][f"{c}-s{g}"][L]["justes"])
                                            for L in LENS) for g in GRAINES)
        lignes.append(f"| {c} | " + " | ".join(cel) + f" | {ge} | {pg} |")
    lignes += ["", "Part de rangs de propagation (somme des chiffres = 9) : ADV-CASCADE "
               + ", ".join(f"L = {L} : {100 * v:.1f} %"
                           for L, v in res["part_propagation_adv_cascade"].items())
               + f" ; ADV-PROPAG (hors 2 items spéciaux) : "
                 f"{100 * res['part_propagation_adv_propag']:.1f} %."]
    open(os.path.join(ICI, "resultats", "adv_propag.md"), "w").write("\n".join(lignes) + "\n")
    print("\n".join(lignes))


if __name__ == "__main__":
    main()
