"""A0-bis : 4 configurations + a0 + 4 étalons d'E002-bis sur les graines 1–20 (PREREGISTREMENT §4–§7).

Usage : python3 evaluer_a0bis.py [--graines 1-20] [--sortie results]
Réutilise evaluer_bis.evaluer_suite (sur evaluer.evaluer_monde d'E002) et les
métriques M1–M4 d'A0 (evaluer_a0.metriques), sans les modifier. Se relance
avec PYTHONHASHSEED=0 (leçon M0007).
"""

import argparse
import datetime
import json
import os
import sys

import chemin  # noqa: F401

from a0 import A0
from a0bis import CONFIGURATIONS
from etalons_bis import ETALONS_BIS
from evaluer import _f, _moy
from evaluer_a0 import metriques
from evaluer_bis import evaluer_suite, resume_md
from monde import generer_monde

COMPLET = "a0bis"
ABLATIONS = ("a0bis_sans_cout_marginal", "a0bis_sans_memoire_famille", "a0bis_sans_bruit_mle")
CONTROLES = ("aleatoire", "oracle_proprietes", "plafond_verificateur", "decouvreur_naif")


def attribution(abl, ref):
    """§5 : la pièce porte le gain si l'ablation est strictement pire sur M1 ;
    elle ne le porte pas si l'ablation fait au moins aussi bien sur M1 et M2."""
    m1, m2 = "M1_R_diff_moyen", "M2_familles_accelerees"
    if abl[m1][0] < ref[m1][0]:
        return "porte"
    if abl[m2][0] >= ref[m2][0]:
        return "ne_porte_pas"
    return "indetermine"


def verdict_candidat(res):
    mc = metriques(res[COMPLET])
    acq = res[COMPLET]["critere_acquerir"]["verdict"] == "REUSSITE"
    controles = {n: res[n]["critere_acquerir"]["verdict"] for n in CONTROLES}
    return {"verdict": "REUSSITE" if acq else "ECHEC", "acquerir_a0bis": acq,
            "metriques": {n: {k: x[0] for k, x in metriques(res[n]).items()}
                          for n in (COMPLET,) + ABLATIONS + ("a0",)},
            "attribution": {n: attribution(metriques(res[n]), mc) for n in ABLATIONS},
            "requetes_moyennes": {n: _moy([l["requetes"] for l in res[n]["mondes"]])
                                  for n in (COMPLET,) + ABLATIONS},
            "eta_fin": {n: res[n]["mondes"][-1]["proprietes_crues"]["eta"] for n in (COMPLET,) + ABLATIONS},
            "controles_acquerir": controles,
            "critere_trop_permissif": any(v == "REUSSITE" for v in controles.values())}


def resume_a0bis(res, verdict, mesure, graines, h):
    L = [resume_md(res, mesure, graines, h).replace("# E002-bis — résultats", "# A0-bis — résultats", 1), "",
         "## Verdict du candidat (PREREGISTREMENT A0-bis §5)", "",
         "**%s** — ACQUÉRIR a0bis : %s ; critère trop permissif (un étalon réussit) : %s." % (
             verdict["verdict"], "oui" if verdict["acquerir_a0bis"] else "non",
             "oui" if verdict["critere_trop_permissif"] else "non"), "",
         "| configuration | M1 R̂_diff moyen | M2 familles accélérées | M3 gain moyen 1er→5e | "
         "M4 DÉDUIT faux (vérité) | requêtes moyennes | η fin | la pièce retirée |", "|---|---|---|---|---|---|---|---|"]
    for n in (COMPLET,) + ABLATIONS + ("a0",):
        m = verdict["metriques"][n]
        L.append("| %s | %s | %d | %s | %s | %s | %s | %s |" % (
            n, _f(m["M1_R_diff_moyen"], 4), m["M2_familles_accelerees"], _f(m["M3_gain_moyen_1er_5e"], 4),
            _f(m["M4_deduits_faux_verite"], 2), _f(verdict["requetes_moyennes"].get(n), 1),
            _f(verdict["eta_fin"].get(n), 3), verdict["attribution"].get(n, "—")))
    L += ["", "## Mémoire par famille de a0bis (famille identifiée pendant le monde → famille de rangement)", ""]
    for l in res[COMPLET]["mondes"]:
        pc = l["proprietes_crues"]
        L.append("- graine %d (banc : famille %d) : identifiée %s, R̂ %s, coût marginal %s bits, requêtes %d" % (
            l["graine"], l["famille"], pc["famille_identifiee"], _f(pc["r_chapeau"], 4),
            _f(pc["cout_marginal"], 3), pc["requetes"]))
    return "\n".join(L) + "\n"


def executer(graines):
    res, mesure = evaluer_suite(tuple(ETALONS_BIS) + (A0,) + tuple(CONFIGURATIONS),
                                [generer_monde(g) for g in graines])
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
    md = resume_a0bis(res, verdict, mesure, graines, h)
    with open(os.path.join(d, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    sys.stdout.write(md)
    print("\nÉcrit dans", d)


if __name__ == "__main__":
    main()
