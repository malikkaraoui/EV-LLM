"""E002-bis : 20 mondes × 4 étalons, R̂_diff = R − R_plafond-vérificateur.

Usage : python3 evaluer_bis.py [--graines 1-20] [--sortie results]
Réutilise evaluer.evaluer_monde d'E002 ; écrit results/<horodatage>/.
"""

import argparse
import datetime
import json
import os
import sys

import chemin_e002  # noqa: F401

from etalons_bis import ETALONS_BIS
from evaluer import _f, _moy, evaluer_monde
from monde import generer_monde

PLAFOND = "plafond_verificateur"
PLAFOND_SECONDAIRE = "oracle_proprietes"
SEUIL_GAIN = 0.005      # R̂_diff(5e) − R̂_diff(1er) (bis §4)
TRANSITIONS_MIN = 3     # sur 4
FAMILLES_MIN = 3        # sur 4
MONDES_R_NON_POSITIF_MAX = 4   # bis §5 : ≥ 5/20 → mesure non réparée


def r_diff(r_systeme, r_plafond):
    return r_systeme - r_plafond


def acceleration_diff(serie):
    hausses = sum(1 for a, b in zip(serie, serie[1:]) if b - a > 0)
    gain = serie[-1] - serie[0]
    return {"acceleration": gain >= SEUIL_GAIN and hausses >= TRANSITIONS_MIN,
            "gain": gain, "hausses": hausses, "serie": serie}


def verdict_mesure(r_plafond_par_monde):
    non_pos = sum(1 for r in r_plafond_par_monde if r <= 0)
    return {"mondes_R_non_positif": non_pos, "mondes": len(r_plafond_par_monde),
            "verdict": "REPAREE" if non_pos <= MONDES_R_NON_POSITIF_MAX else "NON_REPAREE"}


def evaluer_suite(classes, mondes):
    res = {}
    for cls in classes:
        sys_ = cls()
        lignes = []
        for m in mondes:
            ligne, correction = evaluer_monde(sys_, m)
            sys_.fin_monde(correction)
            lignes.append(ligne)
        res[cls.nom] = {"mondes": lignes}
    ref = {l["graine"]: l["R"] for l in res[PLAFOND]["mondes"]}
    ref2 = {l["graine"]: l["R"] for l in res[PLAFOND_SECONDAIRE]["mondes"]}
    for bloc in res.values():
        for l in bloc["mondes"]:
            l.pop("R_chapeau", None)
            l["R_diff"] = r_diff(l["R"], ref[l["graine"]])
            l["R_diff_oracle_proprietes"] = r_diff(l["R"], ref2[l["graine"]])
        fams = {}
        for l in bloc["mondes"]:
            fams.setdefault(l["famille"], []).append(l["R_diff"])
        acc = {str(f): acceleration_diff(s) for f, s in sorted(fams.items()) if len(s) == 5}
        n_acc = sum(a["acceleration"] for a in acc.values())
        bloc["familles"] = acc
        bloc["critere_acquerir"] = {
            "familles_accelerees": n_acc, "familles": len(acc),
            "verdict": "REUSSITE" if len(acc) == 4 and n_acc >= FAMILLES_MIN else "ECHEC"}
    mesure = verdict_mesure([l["R"] for l in res[PLAFOND]["mondes"]])
    return res, mesure


def resume_md(res, mesure, graines, horodatage):
    L = ["# E002-bis — résultats %s" % horodatage, "",
         "Graines %d–%d, %d mondes, bruit d'E002 inchangé. Moyennes sur les mondes (phase 2). "
         "Voir PREREGISTREMENT.md." % (graines[0], graines[-1], len(graines)), "",
         "**Mesure (bis §5)** : plafond-vérificateur R ≤ 0 sur %d/%d mondes → **%s**."
         % (mesure["mondes_R_non_positif"], mesure["mondes"], mesure["verdict"]), "",
         "| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | requêtes | "
         "bits exp. | bits économisés | R | mondes R > 0 | R̂_diff | R − R_oracle-propriétés | critère ACQUÉRIR |",
         "|" + "---|" * 13]
    for nom, b in res.items():
        m = b["mondes"]
        c = b["critere_acquerir"]
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %d/%d | %s | %s | %s (%d/%d familles) |" % (
            nom, _f(_moy([l["exactitude"] for l in m])),
            _f(_moy([l["taux_deduits_infondes"] for l in m])),
            _f(_moy([l["deduits_faux_en_verite"] for l in m]), 1),
            _f(_moy([l["preuves_valides"] for l in m])),
            _f(_moy([l["requetes"] for l in m]), 1),
            _f(_moy([l["bits_experience_total"] for l in m]), 0),
            _f(_moy([l["bits_economises"] for l in m]), 1),
            _f(_moy([l["R"] for l in m]), 4),
            sum(1 for l in m if l["R"] > 0), len(m),
            _f(_moy([l["R_diff"] for l in m]), 4),
            _f(_moy([l["R_diff_oracle_proprietes"] for l in m]), 4),
            c["verdict"], c["familles_accelerees"], c["familles"]))
    L += ["", "## R par monde", "", "| graine | famille | variante | " + " | ".join(res) + " |",
          "|" + "---|" * (3 + len(res))]
    for i, g in enumerate(graines):
        l0 = res[next(iter(res))]["mondes"][i]
        L.append("| %d | %d | %s | %s |" % (g, l0["famille"], l0["variante"],
                                            " | ".join(_f(res[n]["mondes"][i]["R"], 4) for n in res)))
    L += ["", "## Courbe R̂_diff par famille (monde n → n+1)", ""]
    for nom, b in res.items():
        for f, a in b["familles"].items():
            L.append("- %s, famille %s : R̂_diff = %s (gain %s, hausses %d/4) → accélération %s" % (
                nom, f, " → ".join(_f(v, 4) for v in a["serie"]), _f(a["gain"], 4), a["hausses"],
                "oui" if a["acceleration"] else "non"))
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--graines", default="1-20")
    ap.add_argument("--sortie", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"))
    a = ap.parse_args(argv)
    lo, hi = (int(x) for x in a.graines.split("-"))
    graines = list(range(lo, hi + 1))
    res, mesure = evaluer_suite(ETALONS_BIS, [generer_monde(g) for g in graines])
    h = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H%M%S%z")
    d = os.path.join(a.sortie, h)
    os.makedirs(d)
    with open(os.path.join(d, "resultats.json"), "w", encoding="utf-8") as fh:
        json.dump({"graines": graines, "mesure": mesure, "systemes": res}, fh,
                  ensure_ascii=False, indent=1, sort_keys=True)
    md = resume_md(res, mesure, graines, h)
    with open(os.path.join(d, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    sys.stdout.write(md)
    print("\nÉcrit dans", d)


if __name__ == "__main__":
    main()
