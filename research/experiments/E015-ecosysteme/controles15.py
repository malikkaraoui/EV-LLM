"""E015 -- C-ORACLE et C-PARCOEUR sur VAL-OOD + TEST des trois taches (PREREGISTREMENT section 5).

  python controles15.py   -> resultats/controles.json + verdict VALIDE / NON VALIDE
C-PARCOEUR : table des items juges par la graine 1, toutes conditions (runs/*-s1/uniques.pkl).
"""
import glob
import json
import os
import pickle

from d15 import TACHES, evaluer, exact_par_jeu, jeu_val, jeux_test, oracle

ICI = os.path.dirname(os.path.abspath(__file__))


def main():
    out, ok_or, pc_max, pc_tid = {}, True, 0.0, 0.0
    for t in TACHES:
        table = set()
        fichiers = sorted(glob.glob(os.path.join(ICI, "runs", f"*-{t}-s1", "uniques.pkl")))
        for f in fichiers:
            table.update(tuple(x) for x in pickle.load(open(f, "rb")))
        jeux = dict(jeu_val(t), **jeux_test(t))
        e_or = exact_par_jeu(evaluer(lambda its: [(oracle(t, it), 1.0) for it in its],
                                     jeux, "C-ORACLE", t))
        from d15 import reference
        e_pc = exact_par_jeu(evaluer(
            lambda its: [((reference(t, it), 1.0) if tuple(it) in table else (None, 0.0))
                         for it in its], jeux, "C-PARCOEUR", t))
        ok_or &= all(v == 1.0 for v in e_or.values())
        pc_max = max(pc_max, max(v for k, v in e_pc.items() if not k.startswith("T-ID")))
        pc_tid = max(pc_tid, max(v for k, v in e_pc.items() if k.startswith("T-ID")))
        out[t] = {"table_items": len(table), "runs_table": [os.path.basename(os.path.dirname(f))
                                                             for f in fichiers],
                  "n_items": sum(len(i) for p in jeux.values() for i in p.values()),
                  "C-ORACLE": e_or, "C-PARCOEUR": e_pc}
        print(f"{t} : oracle min {min(e_or.values()):.3f} ; par-coeur max hors T-ID "
              f"{max(v for k, v in e_pc.items() if not k.startswith('T-ID')):.3f} "
              f"(table {len(table)} items, {len(fichiers)} runs, {out[t]['n_items']} items testes)")
    verdict = "VALIDE" if ok_or and pc_max <= 0.01 else "NON VALIDE"
    out.update(verdict=verdict, oracle_100_partout=ok_or, parcoeur_max_hors_TID=pc_max,
               parcoeur_max_TID=pc_tid)
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    json.dump(out, open(os.path.join(ICI, "resultats", "controles.json"), "w"), indent=1)
    print(f"C-ORACLE 100 % partout : {ok_or} ; C-PARCOEUR max hors T-ID {pc_max:.3f}, T-ID {pc_tid:.3f}")
    print("TEST", verdict)


if __name__ == "__main__":
    main()
