"""E009-bis -- controles de validite (PREREGISTREMENT-bis 4.1) : C-ORACLE et C-PARCOEUR.

Table C-PARCOEUR = paires distinctes du flux de la graine 1 AVEC curriculum reconstruit.
  python verifie_bis.py                 # avant les runs : flux au niveau 5 sur 20 000 pas
  python verifie_bis.py --run A1-s1     # en fin : transitions et pas du run officiel indique
N'evalue aucun modele. Sortie : resultats/controles[_<run>].json + verdict.
"""
import argparse
import os
import time

import curric as C
from bande import ecrire_json, jeux_final, jeux_id, jeux_val, lire_json  # E009
from controles import systeme_oracle  # E008
from evaluate import evaluer, resume  # E008
from verifie import systeme_parcoeur  # E009

ICI = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", default=None)
    args = ap.parse_args()
    if args.run:
        e = lire_json(os.path.join(ICI, "runs", args.run, "etat.json"))
        assert e["graine"] == 1, "table C-PARCOEUR : graine 1"
        pas, transitions = e["pas"], e["transitions"]
    else:
        pas, transitions = C.PLAFOND_PAS, [[0, C.L_FIN]]
    jeux = {**jeux_val(), **jeux_id(), **jeux_final(), "T-ID1": C.d8.jeux_de_test()["T-ID1"]}
    t0 = time.time()
    table, _ = C.uniques(1, pas, transitions)
    t_table = time.time() - t0
    r_or = resume(evaluer(systeme_oracle, jeux, "C-ORACLE"))["par_jeu"]
    r_pc = resume(evaluer(systeme_parcoeur(table), jeux, "C-PARCOEUR"))["par_jeu"]
    oracle_ok = all(c["exact"] == 1.0 for c in r_or.values())
    pc_nouveaux = {k: c["exact"] for k, c in r_pc.items() if not k.startswith("T-ID1|")}
    pc_ok = all(v <= 0.01 for v in pc_nouveaux.values())
    positif_ok = r_pc["T-ID1|1"]["exact"] == 1.0
    valide = oracle_ok and pc_ok and positif_ok
    out = {
        "verdict": "VALIDE" if valide else "NON VALIDE",
        "oracle_100_partout": oracle_ok,
        "parcoeur_max_nouveaux_jeux": max(pc_nouveaux.values()),
        "parcoeur_controle_positif_T-ID1": r_pc["T-ID1|1"]["exact"],
        "table_parcoeur": {"graine": 1, "pas": pas, "transitions": transitions,
                           "paires_uniques": len(table), "duree_s": round(t_table, 1)},
        "tailles": {k: c["n"] for k, c in r_or.items()},
        "C-ORACLE": r_or,
        "C-PARCOEUR": r_pc,
    }
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    nom = f"controles_{args.run}.json" if args.run else "controles.json"
    ecrire_json(out, os.path.join(ICI, "resultats", nom))
    for k in sorted(r_or):
        print(f"{k:16s} n={out['tailles'][k]:4d}  oracle={r_or[k]['exact']:.3f}  "
              f"parcoeur={r_pc[k]['exact']:.3f}")
    print(f"table : {len(table)} paires uniques ({t_table:.0f} s), pas {pas}, {transitions}")
    print("TEST", out["verdict"])


if __name__ == "__main__":
    main()
