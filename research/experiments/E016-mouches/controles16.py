"""E016 -- C-ORACLE et C-PARCOEUR recalcules sur VAL-OOD + TEST (PREREGISTREMENT section 4).

  python controles16.py   -> resultats/controles.json + verdict VALIDE / NON VALIDE

Table par coeur : toutes les paires du flux E008 que la graine 1 a pu consommer
(paires_flux(1, k), k < 3 x pas) -- sur-ensemble des problemes vus, donc controle conservateur.
"""
import json
import os
import time

from m16 import D  # en premier : ajoute E014, E013, E008 au chemin
from controles import systeme_oracle  # noqa: E402  (E008 : retenue codee a la main)
from evaluate import evaluer, resume  # noqa: E402

ICI = os.path.dirname(os.path.abspath(__file__))


def main():
    hp = json.load(open(os.path.join(ICI, "hyperparametres.json")))
    jeux = dict(D.jeu_val(), **D.jeux_test())
    t0 = time.time()
    table = set()
    for k in range(3 * hp["pas"]):
        table.update(D.paires_flux(1, k))
    parcoeur = lambda paires: [((str(a + b), 1.0) if (a, b) in table else (None, 0.0))
                               for a, b in paires]
    r_or = resume(evaluer(systeme_oracle, jeux, "C-ORACLE"))["par_jeu"]
    r_pc = resume(evaluer(parcoeur, jeux, "C-PARCOEUR"))["par_jeu"]
    oracle_ok = all(c["exact"] == 1.0 for c in r_or.values())
    pc_max = max(c["exact"] for k, c in r_pc.items() if not k.startswith("T-ID"))
    out = {"verdict": "VALIDE" if oracle_ok and pc_max <= 0.01 else "NON VALIDE",
           "oracle_100_partout": oracle_ok, "parcoeur_max_hors_TID": pc_max,
           "table_parcoeur": {"graine": 1, "pas_flux": 3 * hp["pas"], "paires_uniques": len(table)},
           "n_items": sum(c["n"] for c in r_or.values()),
           "duree_s": round(time.time() - t0, 1), "C-ORACLE": r_or, "C-PARCOEUR": r_pc}
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    json.dump(out, open(os.path.join(ICI, "resultats", "controles.json"), "w"), indent=1)
    print(f"C-ORACLE 100 % partout : {oracle_ok} ({out['n_items']} items, {len(r_or)} jeux x L)")
    print(f"C-PARCOEUR max hors T-ID : {pc_max:.3f} (table {len(table)} paires uniques)")
    print("TEST", out["verdict"])


if __name__ == "__main__":
    main()
