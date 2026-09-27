"""E011 -- controles de validite : C-ORACLE, C-PARCOEUR, C-GOLDEN (PREREGISTREMENT s. 2-3).

Evaluateur unique : evaluate.evaluer / resume de E008, importes tels quels.
Usage : python controles.py   -> resultats/controles.json + verdict
"""
import os

from donnees import ICI, ecrire_json, encode, jeu_entrainement, jeu_validation, jeux_test, lire_json
from evaluate import evaluer, resume  # E008 (chemin ajoute par donnees.py)
from rnn import golden, predit


def addition_bits(a, b):
    """Retenue binaire codee a la main sur les listes de bits (pas de a + b)."""
    la, lb = bin(a)[2:][::-1], bin(b)[2:][::-1]
    out, r = [], 0
    for i in range(max(len(la), len(lb))):
        s = (la[i] == "1" if i < len(la) else 0) + (lb[i] == "1" if i < len(lb) else 0) + r
        out.append(s & 1)
        r = s >> 1
    out.append(r)
    v = 0
    for bit in reversed(out):
        v = (v << 1) | bit
    return str(v)


def systeme_oracle(paires):
    return [(addition_bits(a, b), 1.0) for a, b in paires]


def systeme_parcoeur(table):
    return lambda paires: [((str(a + b), 1.0) if (a, b) in table else (None, 0.0))
                           for a, b in paires]


def tous_les_jeux():
    j = jeu_validation()
    j.update(jeux_test())
    return j


def main():
    hp = lire_json(os.path.join(ICI, "hyperparametres.json"))
    jeux = tous_les_jeux()
    r_or = resume(evaluer(systeme_oracle, jeux, "C-ORACLE"))["par_jeu"]
    table = set(jeu_entrainement(1))
    r_pc = resume(evaluer(systeme_parcoeur(table), jeux, "C-PARCOEUR"))["par_jeu"]
    th = golden(hp["k"], hp["k"])
    r_go = resume(evaluer(lambda p: predit(th, p, encode), jeux, "C-GOLDEN"))["par_jeu"]
    # controle positif de la table : elle rejoue ses propres paires
    r_pc_pos = resume(evaluer(systeme_parcoeur(table), {"TRAIN-s1": {0: sorted(table)}},
                              "C-PARCOEUR"))["par_jeu"]
    oracle_ok = all(c["exact"] == 1.0 for c in r_or.values())
    pc_max = max(c["exact"] for c in r_pc.values())
    golden_ok = all(c["exact"] == 1.0 for c in r_go.values())
    valide = oracle_ok and pc_max == 0.0 and golden_ok
    out = {"verdict": "VALIDE" if valide else "NON VALIDE", "oracle_100_partout": oracle_ok,
           "parcoeur_max": pc_max, "parcoeur_controle_positif": r_pc_pos,
           "golden_100_partout": golden_ok, "k": hp["k"],
           "C-ORACLE": r_or, "C-PARCOEUR": r_pc, "C-GOLDEN": r_go}
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    ecrire_json(out, os.path.join(ICI, "resultats", "controles.json"))
    for nomc, r in (("C-ORACLE", r_or), ("C-PARCOEUR", r_pc), ("C-GOLDEN", r_go)):
        for k, c in sorted(r.items(), key=lambda kv: (kv[0].split("|")[0], int(kv[0].split("|")[1]))):
            print(f"{nomc:10s} {k:16s} exact={c['exact']:.3f} n={c['n']} faux_surs={c['faux_surs']}")
    print("controle positif table :", {k: v["exact"] for k, v in r_pc_pos.items()})
    print("TEST", out["verdict"])


if __name__ == "__main__":
    main()
