"""E010 -- controles de validite sur TOUS les jeux (PREREGISTREMENT section 4).

C-ORACLE (retenue codee a la main), C-ORACLE-TRACE (sequence F1/F3 de l'oracle relue par
l'analyseur des modeles), C-PARCOEUR (table de la reserve maximale, graine 1).

  python validite.py   -> resultats/controles.json + TEST VALIDE / NON VALIDE
"""
import os
import time

from donnees import BATCH, cible, ecrire_json, jeux_e010, lire_json, lit_sortie, reserve
from controles import addition_retenue  # E008 (chemin ajoute par donnees)  # noqa: E402
from evaluate import evaluer, resume  # E008 : evaluateur unique

ICI = os.path.dirname(os.path.abspath(__file__))


def systeme_oracle(paires):
    return [(addition_retenue(a, b), 1.0) for a, b in paires]


def systeme_oracle_trace(fmt):
    return lambda paires: [(lit_sortie(cible(a, b, fmt), fmt)[0], 1.0) for a, b in paires]


def systeme_parcoeur(table):
    return lambda paires: [((str(a + b), 1.0) if (a, b) in table else (None, 0.0))
                           for a, b in paires]


def main():
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    jeux = jeux_e010(n_id=500, final=True)
    t0 = time.time()
    table = set(reserve(1, hp["pas"] * BATCH))
    systemes = {"C-ORACLE": systeme_oracle, "C-ORACLE-TRACE-F1": systeme_oracle_trace("F1"),
                "C-ORACLE-TRACE-F3": systeme_oracle_trace("F3"),
                "C-PARCOEUR": systeme_parcoeur(table)}
    res = {k: resume(evaluer(s, jeux, k))["par_jeu"] for k, s in systemes.items()}
    oracles_ok = all(c["exact"] == 1.0 for k in systemes if k.startswith("C-ORACLE")
                     for c in res[k].values())
    pc = {k: c["exact"] for k, c in res["C-PARCOEUR"].items() if not k.startswith("T-ID1")}
    pc_ok = max(pc.values()) <= 0.01
    temoin = res["C-PARCOEUR"]["T-ID1|1"]["exact"]
    out = {"verdict": "VALIDE" if oracles_ok and pc_ok else "NON VALIDE",
           "oracles_100_partout": oracles_ok, "parcoeur_max_hors_T-ID1": max(pc.values()),
           "parcoeur_T-ID1_temoin": temoin,
           "table_parcoeur": {"graine": 1, "paires_uniques": len(table)},
           "items_par_systeme": sum(c["n"] for c in res["C-ORACLE"].values()),
           "duree_s": round(time.time() - t0, 1), **res}
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    ecrire_json(out, os.path.join(ICI, "resultats", "controles.json"))
    for k in systemes:
        print(k, " ".join(f"{j}={c['exact']:.3f}" for j, c in sorted(res[k].items())))
    print("TEST", out["verdict"])


if __name__ == "__main__":
    main()
