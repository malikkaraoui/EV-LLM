"""E008 -- controles de validite du test : C-ORACLE et C-PARCOEUR (PREREGISTREMENT section 6).

Usage : python controles.py   -> resultats/controles.json + verdict VALIDE / NON VALIDE
"""
import os
import time

from data import BATCH, ecrire_json, jeux_de_test, lire_json, paires_du_pas, paires_exclues
from evaluate import evaluer, resume

ICI = os.path.dirname(os.path.abspath(__file__))
GRAINE_TABLE = 1


def addition_retenue(a, b):
    """Addition chiffre par chiffre avec retenue, sur les chaines (pas de a + b)."""
    sa, sb = str(a)[::-1], str(b)[::-1]
    out, r = [], 0
    for i in range(max(len(sa), len(sb))):
        da = ord(sa[i]) - 48 if i < len(sa) else 0
        db = ord(sb[i]) - 48 if i < len(sb) else 0
        s = da + db + r
        out.append(chr(48 + s % 10))
        r = s // 10
    if r:
        out.append("1")
    return "".join(reversed(out))


def systeme_oracle(paires):
    return [(addition_retenue(a, b), 1.0) for a, b in paires]


def cle(a, b):
    return a * 10 ** 17 + b  # unique tant que b < 10^17 (operandes <= 16 chiffres)


def table_parcoeur(graine, pas_total, lot=BATCH):
    ex = paires_exclues()
    table = set()
    for t in range(pas_total):
        for a, b in paires_du_pas(graine, t, ex, lot):
            table.add(cle(a, b))
    return table


def systeme_parcoeur(table):
    # reponse memorisee = la cible montree a l'entrainement pour cette paire, sinon rien
    return lambda paires: [((str(a + b), 1.0) if cle(a, b) in table else (None, 0.0))
                           for a, b in paires]


def main():
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    jeux = jeux_de_test()
    t0 = time.time()
    table = table_parcoeur(GRAINE_TABLE, hp["pas"], hp["lot"])
    t_table = time.time() - t0
    r_or = resume(evaluer(systeme_oracle, jeux, "C-ORACLE"))
    r_pc = resume(evaluer(systeme_parcoeur(table), jeux, "C-PARCOEUR"))

    oracle_ok = all(c["exact"] == 1.0 for c in r_or["par_jeu"].values())
    pc_vus = {k: c["exact"] for k, c in r_pc["par_jeu"].items()
              if k.startswith("T-ID|") or k.startswith("T-OOD|")}
    pc_ok = all(v <= 0.01 for v in pc_vus.values())
    valide = oracle_ok and pc_ok
    out = {
        "verdict": "VALIDE" if valide else "NON VALIDE",
        "oracle_100_partout": oracle_ok,
        "parcoeur_max_T-ID_T-OOD": max(pc_vus.values()),
        "table_parcoeur": {"graine": GRAINE_TABLE, "pas": hp["pas"], "lot": hp["lot"],
                           "paires_uniques": len(table), "duree_s": round(t_table, 1)},
        "C-ORACLE": r_or["par_jeu"],
        "C-PARCOEUR": r_pc["par_jeu"],
    }
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    ecrire_json(out, os.path.join(ICI, "resultats", "controles.json"))
    print(f"C-ORACLE 100 % partout : {oracle_ok}")
    for k, v in sorted(r_pc["par_jeu"].items()):
        print(f"C-PARCOEUR {k:12s} exact = {v['exact']:.3f} (n={v['n']})")
    print(f"table : {len(table)} paires uniques ({t_table:.0f} s)")
    print("TEST", out["verdict"])


if __name__ == "__main__":
    main()
