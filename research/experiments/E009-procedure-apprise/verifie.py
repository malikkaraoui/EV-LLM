"""E009 -- controles de validite sur TOUS les nouveaux jeux (PREREGISTREMENT section 6).

C-ORACLE (addition avec retenue d'E008) et C-PARCOEUR (table des paires vues, graine 1, S pas).
N'evalue aucun modele. Usage : python verifie.py -> resultats/controles.json + verdict.
"""
import os
import time

from bande import BATCH, d8, ecrire_json, jeux_final, jeux_id, jeux_val, lire_json
from controles import systeme_oracle  # E008
from evaluate import evaluer, resume  # E008

ICI = os.path.dirname(os.path.abspath(__file__))
GRAINE_TABLE = 1


def uniques(graine, pas_total, points=(), lot=BATCH):
    """Paires distinctes du flux ; renvoie (table, {pas: nb d'uniques} aux points demandes)."""
    ex = d8.paires_exclues()
    table, compte = set(), {}
    pts = set(points)
    for t in range(pas_total):
        table.update(d8.paires_du_pas(graine, t, ex, lot))
        if t + 1 in pts:
            compte[t + 1] = len(table)
    return table, compte


def systeme_parcoeur(table):
    return lambda paires: [((str(a + b), 1.0) if (a, b) in table else (None, 0.0))
                           for a, b in paires]


def main():
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    jeux = {**jeux_val(), **jeux_id(), **jeux_final(),
            "T-ID1": d8.jeux_de_test()["T-ID1"]}
    t0 = time.time()
    table, _ = uniques(GRAINE_TABLE, hp["pas"])
    t_table = time.time() - t0
    r_or = resume(evaluer(systeme_oracle, jeux, "C-ORACLE"))["par_jeu"]
    r_pc = resume(evaluer(systeme_parcoeur(table), jeux, "C-PARCOEUR"))["par_jeu"]
    oracle_ok = all(c["exact"] == 1.0 for c in r_or.values())
    pc_nouveaux = {k: c["exact"] for k, c in r_pc.items() if not k.startswith("T-ID1|")}
    pc_ok = all(v <= 0.01 for v in pc_nouveaux.values())
    positif_ok = r_pc["T-ID1|1"]["exact"] == 1.0
    valide = oracle_ok and pc_ok and positif_ok
    tailles = {k: c["n"] for k, c in r_or.items()}
    out = {
        "verdict": "VALIDE" if valide else "NON VALIDE",
        "oracle_100_partout": oracle_ok,
        "parcoeur_max_nouveaux_jeux": max(pc_nouveaux.values()),
        "parcoeur_controle_positif_T-ID1": r_pc["T-ID1|1"]["exact"],
        "table_parcoeur": {"graine": GRAINE_TABLE, "pas": hp["pas"], "lot": hp["lot"],
                           "paires_uniques": len(table), "duree_s": round(t_table, 1)},
        "tailles": tailles,
        "C-ORACLE": r_or,
        "C-PARCOEUR": r_pc,
    }
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    ecrire_json(out, os.path.join(ICI, "resultats", "controles.json"))
    for k in sorted(r_or):
        print(f"{k:16s} n={tailles[k]:4d}  oracle={r_or[k]['exact']:.3f}  "
              f"parcoeur={r_pc[k]['exact']:.3f}")
    print(f"table : {len(table)} paires uniques ({t_table:.0f} s)")
    print("TEST", out["verdict"])


if __name__ == "__main__":
    main()
