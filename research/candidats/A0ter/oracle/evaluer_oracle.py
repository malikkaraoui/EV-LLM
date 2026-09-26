"""A0-ter, Mission 1 : 3 oracles + a0bis + 4 étalons d'E002-bis, graines 1–20 (PREREGISTREMENT-oracle §4–§8).

Usage : python3 evaluer_oracle.py [--graines 1-20] [--sortie results]
Réutilise evaluer_bis.evaluer_suite (sur evaluer.evaluer_monde d'E002) et les
métriques M1–M4 d'A0, sans les modifier. Se relance avec PYTHONHASHSEED=0.
"""

import argparse
import datetime
import json
import math
import os
import sys

import chemin  # noqa: F401

from a0bis import A0Bis
from acquereur_oracle import ORACLES, enregistrer_mondes
from etalons_bis import ETALONS_BIS
from evaluer import _f, _moy
from evaluer_a0 import metriques
from evaluer_bis import SEUIL_GAIN, evaluer_suite, resume_md
from monde import generer_monde

ACQUEREUR, AMNESIQUE, EXACT = "oracle_acquereur", "oracle_amnesique", "oracle_exact"
AFFICHES = (ACQUEREUR, AMNESIQUE, EXACT, "a0bis")
CONTROLES = ("aleatoire", "oracle_proprietes", "plafond_verificateur", "decouvreur_naif")


def _ecart_type(v):
    m = sum(v) / len(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def diagnostic(bloc):
    """§6 : par famille, courbe, écart du 1er monde, dispersion des mondes 2–5, écart au plafond."""
    out = {}
    for f, a in bloc["familles"].items():
        s = a["serie"]
        suite = s[1:]
        ecart1 = sum(suite) / len(suite) - s[0]
        out[f] = {"serie": s, "gain": a["gain"], "hausses": a["hausses"], "acceleration": a["acceleration"],
                  "ecart_1er_monde": ecart1, "ecart_type_2_5": _ecart_type(suite),
                  "moyenne_2_5": sum(suite) / len(suite)}
    return out


def verdict_mission1(res):
    n_acq = res[ACQUEREUR]["critere_acquerir"]["familles_accelerees"]
    n_amn = res[AMNESIQUE]["critere_acquerir"]["familles_accelerees"]
    atteignable = n_acq >= 3
    permissif = n_amn >= 2
    if atteignable and not permissif:
        v = "ATTEIGNABLE_ET_DISCRIMINANT"
    elif not atteignable and permissif:
        v = "NON_ATTEIGNABLE_ET_TROP_PERMISSIF"
    elif not atteignable:
        v = "NON_ATTEIGNABLE"
    else:
        v = "TROP_PERMISSIF"
    return {"verdict": v, "familles_acquereur": n_acq, "familles_amnesique": n_amn,
            "familles_exact": res[EXACT]["critere_acquerir"]["familles_accelerees"],
            "mission2": v == "ATTEIGNABLE_ET_DISCRIMINANT",
            "metriques": {n: {k: x[0] for k, x in metriques(res[n]).items()} for n in AFFICHES},
            "requetes_moyennes": {n: _moy([l["requetes"] for l in res[n]["mondes"]]) for n in AFFICHES},
            "diagnostic": {n: diagnostic(res[n]) for n in AFFICHES},
            "controles_acquerir": {n: res[n]["critere_acquerir"]["verdict"] for n in CONTROLES},
            "k_egale_verite": {n: [[l["graine"], l["proprietes_crues"]["k_egale_verite"],
                                    l["proprietes_crues"]["regles_oracle"]] for l in res[n]["mondes"]]
                               for n in (ACQUEREUR, EXACT)}}


def resume_oracle(res, verdict, mesure, graines, h):
    L = [resume_md(res, mesure, graines, h).replace("# E002-bis — résultats", "# A0-ter / oracle — résultats", 1),
         "", "## Verdict de la Mission 1 (PREREGISTREMENT-oracle §4)", "",
         "**%s** — oracle_acquereur : %d/4 familles accélérées ; oracle_amnesique : %d/4 ; "
         "oracle_exact (diagnostic) : %d/4. Mission 2 : %s." % (
             verdict["verdict"], verdict["familles_acquereur"], verdict["familles_amnesique"],
             verdict["familles_exact"], "oui" if verdict["mission2"] else "non"), "",
         "| système | M1 R̂_diff moyen | M2 familles accélérées | M3 gain moyen 1er→5e | "
         "M4 DÉDUIT faux (vérité) | requêtes moyennes |", "|---|---|---|---|---|---|"]
    for n in AFFICHES:
        m = verdict["metriques"][n]
        L.append("| %s | %s | %d | %s | %s | %s |" % (
            n, _f(m["M1_R_diff_moyen"], 4), m["M2_familles_accelerees"], _f(m["M3_gain_moyen_1er_5e"], 4),
            _f(m["M4_deduits_faux_verite"], 2), _f(verdict["requetes_moyennes"][n], 1)))
    L += ["", "## Diagnostic (§6) : le 1er monde domine-t-il ? la variance noie-t-elle le gain ?", "",
          "Seuil de gain : %s. écart_1 = moyenne(mondes 2–5) − 1er monde." % SEUIL_GAIN, "",
          "| système | famille | courbe R̂_diff | gain 1er→5e | hausses | écart_1 | écart-type 2–5 | "
          "moyenne 2–5 | accélération |", "|---|---|---|---|---|---|---|---|---|"]
    for n in AFFICHES:
        for f, d in verdict["diagnostic"][n].items():
            L.append("| %s | %s | %s | %s | %d/4 | %s | %s | %s | %s |" % (
                n, f, " → ".join(_f(v, 4) for v in d["serie"]), _f(d["gain"], 4), d["hausses"],
                _f(d["ecart_1er_monde"], 4), _f(d["ecart_type_2_5"], 4), _f(d["moyenne_2_5"], 4),
                "oui" if d["acceleration"] else "non"))
    L += ["", "## K_f appliquée (graine, égale aux propriétés vraies du monde courant, nombre de règles)", ""]
    for n, lignes in verdict["k_egale_verite"].items():
        L.append("- %s : %s" % (n, " ; ".join("g%d %s/%s" % (g, "—" if e is None else ("oui" if e else "NON"),
                                                               "—" if k is None else k) for g, e, k in lignes)))
    return "\n".join(L) + "\n"


def executer(graines):
    mondes = [generer_monde(g) for g in graines]
    enregistrer_mondes(mondes)
    res, mesure = evaluer_suite(tuple(ETALONS_BIS) + (A0Bis,) + tuple(ORACLES), mondes)
    return res, mesure, verdict_mission1(res)


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
        json.dump({"graines": graines, "mesure": mesure, "verdict_mission1": verdict, "systemes": res}, fh,
                  ensure_ascii=False, indent=1, sort_keys=True)
    md = resume_oracle(res, verdict, mesure, graines, h)
    with open(os.path.join(d, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    sys.stdout.write(md)
    print("\nÉcrit dans", d)


if __name__ == "__main__":
    main()
