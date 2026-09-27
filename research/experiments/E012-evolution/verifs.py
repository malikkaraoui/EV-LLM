"""E012 -- controles de validite : C-ORACLE-ALGO, C-ORACLE-CIRCUIT, C-PARCOEUR (PREREGISTREMENT s. 6).

Evaluateur unique : evaluate.evaluer / resume d'E008, importes tels quels.
Usage : python verifs.py   -> resultats/controles.json + verdict
"""
import os

from jeux import (EXPERIENCES, ICI, ecrire_json, encodeur, jeu_entrainement, jeu_validation,
                  jeux_test)
from evaluate import evaluer, resume  # E008
from reseau import circuit_main, longueur_G, preuve_aligne, systeme, taille


def addition_listes(a, b, base):
    """Retenue codee a la main sur les listes de chiffres (pas de a + b)."""
    def chiffres(x):
        out = []
        while True:
            out.append(x % base)
            x //= base
            if x == 0:
                return out
    la, lb = chiffres(a), chiffres(b)
    out, r = [], 0
    for i in range(max(len(la), len(lb))):
        s = (la[i] if i < len(la) else 0) + (lb[i] if i < len(lb) else 0) + r
        out.append(s % base)
        r = s // base
    out.append(r)
    v = 0
    for c in reversed(out):
        v = v * base + c
    return str(v)


def tous_les_jeux(base):
    j = jeu_validation(base)
    j.update(jeux_test(base))
    return j


def cles_triees(r):
    return sorted(r.items(), key=lambda kv: (kv[0].split("|")[0], int(kv[0].split("|")[1])))


def main():
    out = {}
    valide = True
    for base in (2, 10):
        jeux = tous_les_jeux(base)
        r_or = resume(evaluer(lambda ps: [(addition_listes(a, b, base), 1.0) for a, b in ps],
                              jeux, "C-ORACLE-ALGO"))["par_jeu"]
        exp_pc = "X1" if base == 2 else "X2-100"
        table = set(jeu_entrainement(exp_pc, 1))
        pc = lambda ps: [((str(a + b), 1.0) if (a, b) in table else (None, 0.0)) for a, b in ps]
        r_pc = resume(evaluer(pc, jeux, "C-PARCOEUR"))["par_jeu"]
        r_pos = resume(evaluer(pc, {"TRAIN-s1": {0: sorted(table)}}, "C-PARCOEUR"))["par_jeu"]
        g = circuit_main(base)
        exp_c = "X1" if base == 2 else "X2-100"
        r_ci = resume(evaluer(systeme(g, EXPERIENCES[exp_c], encodeur(exp_c)), jeux,
                              "C-ORACLE-CIRCUIT"))["par_jeu"]
        preuve = preuve_aligne(g, base)
        ok = (all(c["exact"] == 1.0 for c in r_or.values())
              and max(c["exact"] for c in r_pc.values()) == 0.0
              and all(c["exact"] == 1.0 for c in r_ci.values()) and preuve[0] == "PROUVE")
        valide &= ok
        out[f"base{base}"] = {"ok": ok, "C-ORACLE-ALGO": r_or, "C-PARCOEUR": r_pc,
                              "C-PARCOEUR-positif": r_pos, "C-ORACLE-CIRCUIT": r_ci,
                              "circuit": {"G_bits": longueur_G(g), **taille(g), "preuve": preuve}}
        for nom, r in (("C-ORACLE-ALGO", r_or), ("C-PARCOEUR", r_pc), ("C-ORACLE-CIRCUIT", r_ci)):
            for k, c in cles_triees(r):
                print(f"base{base:<3d}{nom:17s} {k:16s} exact={c['exact']:.3f} n={c['n']}")
        print(f"base{base} controle positif table :", {k: v["exact"] for k, v in r_pos.items()})
        print(f"base{base} circuit main : |G| = {longueur_G(g)} bits, {taille(g)}, preuve = {preuve}")
    # format plat : oracle algorithmique seulement (pas de circuit oracle a etat flottant)
    jeux = tous_les_jeux(10)
    table = set(jeu_entrainement("X3", 1))
    pc = lambda ps: [((str(a + b), 1.0) if (a, b) in table else (None, 0.0)) for a, b in ps]
    r_pc3 = resume(evaluer(pc, jeux, "C-PARCOEUR-X3"))["par_jeu"]
    ok3 = max(c["exact"] for c in r_pc3.values()) == 0.0
    valide &= ok3
    out["X3"] = {"ok": ok3, "C-PARCOEUR": r_pc3,
                 "note": "C-ORACLE-ALGO identique a base10 (memes jeux) ; pas de C-ORACLE-CIRCUIT"}
    print("X3 C-PARCOEUR max :", max(c["exact"] for c in r_pc3.values()))
    out["verdict"] = "VALIDE" if valide else "NON VALIDE"
    os.makedirs(os.path.join(ICI, "resultats"), exist_ok=True)
    ecrire_json(out, os.path.join(ICI, "resultats", "controles.json"))
    print("TEST", out["verdict"])


if __name__ == "__main__":
    main()
