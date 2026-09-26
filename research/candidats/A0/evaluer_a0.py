"""A0 : 5 configurations + 4 étalons d'E002-bis sur les graines 1–20 (PREREGISTREMENT §4–§7).

Usage : python3 evaluer_a0.py [--graines 1-20] [--sortie results]
Réutilise evaluer_bis.evaluer_suite (lui-même sur evaluer.evaluer_monde d'E002) :
un seul objet par configuration traverse la suite, donc l'état d'A0 est
conservé d'un monde à l'autre ; a0_sans_memoire le remet à zéro lui-même.
Se relance avec PYTHONHASHSEED=0 (choix de preuve d'E002, leçon M0007).
"""

import argparse
import datetime
import json
import os
import sys

import chemin  # noqa: F401

from a0 import CONFIGURATIONS
from etalons_bis import ETALONS_BIS
from evaluer import _f, _moy
from evaluer_bis import evaluer_suite, resume_md
from monde import generer_monde

COMPLET = "a0"
ABLATIONS = ("a0_sans_memoire", "a0_verifie_toujours", "a0_verifie_jamais", "a0_sans_autodiagnostic")
CONTROLES = ("aleatoire", "oracle_proprietes", "plafond_verificateur", "decouvreur_naif", "a0_sans_memoire")


def metriques(bloc):
    """M1–M4 (§5) : (valeur, sens) ; sens +1 = plus haut vaut mieux."""
    m = bloc["mondes"]
    fams = bloc["familles"].values()
    return {
        "M1_R_diff_moyen": (_moy([l["R_diff"] for l in m]), +1),
        "M2_familles_accelerees": (bloc["critere_acquerir"]["familles_accelerees"], +1),
        "M3_gain_moyen_1er_5e": (_moy([a["gain"] for a in fams]), +1),
        "M4_deduits_faux_verite": (_moy([l["deduits_faux_en_verite"] for l in m]), -1),
    }


def pire(abl, ref):
    """Métriques où l'ablation fait strictement moins bien que la référence."""
    out = []
    for k, (v, sens) in abl.items():
        if (v - ref[k][0]) * sens < 0:
            out.append(k)
    return out


def verdict_candidat(res):
    mc = metriques(res[COMPLET])
    acq = res[COMPLET]["critere_acquerir"]["verdict"] == "REUSSITE"
    abl = {n: pire(metriques(res[n]), mc) for n in ABLATIONS}
    controles = {n: res[n]["critere_acquerir"]["verdict"] for n in CONTROLES}
    if not acq:
        v = "ECHEC"
    elif all(abl.values()):
        v = "REUSSITE"
    else:
        v = "INTERMEDIAIRE"
    return {"verdict": v, "acquerir_a0": acq, "metriques_a0": {k: x[0] for k, x in mc.items()},
            "ablations_pires_sur": abl,
            "metriques_ablations": {n: {k: x[0] for k, x in metriques(res[n]).items()} for n in ABLATIONS},
            "controles_acquerir": controles,
            "critere_trop_permissif": any(v == "REUSSITE" for v in controles.values())}


def resume_a0(res, verdict, mesure, graines, h):
    L = [resume_md(res, mesure, graines, h).replace("# E002-bis — résultats", "# A0 — résultats", 1), "",
         "## Verdict du candidat (PREREGISTREMENT A0 §5)", "",
         "**%s** — ACQUÉRIR a0 : %s ; critère trop permissif (un contrôle réussit) : %s." % (
             verdict["verdict"], "oui" if verdict["acquerir_a0"] else "non",
             "oui" if verdict["critere_trop_permissif"] else "non"), "",
         "| configuration | M1 R̂_diff moyen | M2 familles accélérées | M3 gain moyen 1er→5e | "
         "M4 DÉDUIT faux (vérité) | pire qu'a0 sur |", "|---|---|---|---|---|---|"]
    lignes = [(COMPLET, verdict["metriques_a0"], "—")]
    lignes += [(n, verdict["metriques_ablations"][n], ", ".join(verdict["ablations_pires_sur"][n]) or "aucune")
               for n in ABLATIONS]
    for n, m, p in lignes:
        L.append("| %s | %s | %d | %s | %s | %s |" % (
            n, _f(m["M1_R_diff_moyen"], 4), m["M2_familles_accelerees"], _f(m["M3_gain_moyen_1er_5e"], 4),
            _f(m["M4_deduits_faux_verite"], 2), p))
    return "\n".join(L) + "\n"


def executer(graines):
    res, mesure = evaluer_suite(tuple(ETALONS_BIS) + tuple(CONFIGURATIONS), [generer_monde(g) for g in graines])
    return res, mesure, verdict_candidat(res)


def main(argv=None):
    if os.environ.get("PYTHONHASHSEED") != "0":
        os.execve(sys.executable, [sys.executable, os.path.abspath(__file__)] + sys.argv[1:],
                  dict(os.environ, PYTHONHASHSEED="0"))
    ap = argparse.ArgumentParser()
    ap.add_argument("--graines", default="1-20")
    ap.add_argument("--sortie", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"))
    a = ap.parse_args(argv)
    lo, hi = (int(x) for x in a.graines.split("-"))
    graines = list(range(lo, hi + 1))
    res, mesure, verdict = executer(graines)
    h = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H%M%S%z")
    d = os.path.join(a.sortie, h)
    os.makedirs(d)
    with open(os.path.join(d, "resultats.json"), "w", encoding="utf-8") as fh:
        json.dump({"graines": graines, "mesure": mesure, "verdict_candidat": verdict, "systemes": res}, fh,
                  ensure_ascii=False, indent=1, sort_keys=True)
    md = resume_a0(res, verdict, mesure, graines, h)
    with open(os.path.join(d, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    sys.stdout.write(md)
    print("\nÉcrit dans", d)


if __name__ == "__main__":
    main()
