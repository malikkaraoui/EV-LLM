"""Fait tourner des systèmes sur une suite de mondes et calcule les métriques.

Usage : python3 evaluer.py [--graines 1-20] [--sortie results]
Écrit results/<horodatage>/resultats.json et summary.md (PREREGISTREMENT §3–§5).
"""

import argparse
import datetime
import hashlib
import json
import os
import sys

from etalons import ETALONS
from interface import Environnement
from monde import famille, generer_monde, regles_du_monde, vers_json
from oracle import (attendus, bits_economises, deduit_infonde, juste, vraie_valeur)
from raisonneur import CONTRADICTION, DEDUIT, INDETERMINE, verifier_preuve

SEUIL_GAIN = 0.05       # R̂(5e) − R̂(1er) (§3)
TRANSITIONS_MIN = 3     # sur 4 (§3)
FAMILLES_MIN = 3        # sur 4 (§3)


def _cle(rep):
    return (rep.get("etiquette"), rep.get("valeur"))


def _ratio(a, b):
    return a / b if b else None


def evaluer_monde(systeme, monde):
    env = Environnement(monde)
    if hasattr(systeme, "recevoir_proprietes"):
        systeme.recevoir_proprietes(regles_du_monde(monde))
    systeme.debut_monde(env.vue_publique())
    att = {}
    for p in (1, 2):
        obs = env.ouvrir_phase(p)
        env.enregistrer(p, systeme.phase(p, obs, env.demander))
        att[p] = attendus(monde, env.connus(p))

    qs = {q["id"]: q for q in monde["questions"]}
    rep = env.reponses[2]
    vide = {"etiquette": INDETERMINE}
    connus = env.connus(2)
    vraies = regles_du_monde(monde)

    par_attendu = {}
    justes = infondes = deduits = preuves_ok = preuves_n = 0
    sys_contra = sys_indet = vp_contra = vp_indet = 0
    excl_ok = deduit_faux_verite = 0
    for qid, q in qs.items():
        r, a = rep.get(qid, vide), att[2][qid]
        ok = juste(r, a)
        d = par_attendu.setdefault(a["etiquette"], [0, 0])
        d[0] += 1
        d[1] += ok
        justes += ok
        if r.get("etiquette") == DEDUIT:
            deduits += 1
            infondes += deduit_infonde(r, a)
            if q["type"] == "atome" and r.get("valeur") != vraie_valeur(monde, q["atome"]):
                deduit_faux_verite += 1
        if r.get("etiquette") in (DEDUIT, CONTRADICTION):
            preuves_n += 1
            preuves_ok += verifier_preuve(r, q, connus, vraies, monde["exclusions"], monde["entites"])
        if r.get("etiquette") == CONTRADICTION:
            sys_contra += 1
            vp_contra += a["etiquette"] == CONTRADICTION
        if r.get("etiquette") == INDETERMINE:
            sys_indet += 1
            vp_indet += a["etiquette"] == INDETERMINE
        if q["type"] == "exclusion":
            excl_ok += ok

    n_contra = par_attendu.get(CONTRADICTION, [0])[0]
    n_indet = par_attendu.get(INDETERMINE, [0])[0]

    # Révision (§5) : l'attendu change-t-il entre phase 1 et phase 2 ?
    requises = requises_ok = stables = sur_revisions = 0
    for qid in qs:
        r1, r2 = env.reponses[1].get(qid, vide), rep.get(qid, vide)
        if _cle(att[1][qid]) != _cle(att[2][qid]):
            requises += 1
            requises_ok += juste(r2, att[2][qid])
        else:
            stables += 1
            sur_revisions += _cle(r1) != _cle(r2)

    # R (§4)
    tenus = [tuple(a) for a in monde["tenus_a_l_ecart"]]
    par_atome = {tuple(qs[qid]["atome"]): rep.get(qid, vide) for qid in qs if qs[qid]["type"] == "atome"}
    verites = {a: vraie_valeur(monde, a) for a in tenus}
    economie = bits_economises(par_atome, tenus, verites, env.p_ref())
    bx = env.bits_experience()
    bits_exp = sum(bx.values())

    return {
        "graine": monde["graine"],
        "famille": monde["famille"],
        "variante": monde["semantique"]["variante"],
        "sha256_monde": hashlib.sha256(vers_json(monde).encode()).hexdigest(),
        "questions": len(qs),
        "exactitude": justes / len(qs),
        "par_etiquette_attendue": {e: {"n": n, "justes": j, "exactitude": _ratio(j, n)}
                                   for e, (n, j) in sorted(par_attendu.items())},
        "contradiction": {"precision": _ratio(vp_contra, sys_contra), "rappel": _ratio(vp_contra, n_contra),
                          "systeme": sys_contra, "attendues": n_contra},
        "indetermine": {"precision": _ratio(vp_indet, sys_indet), "rappel": _ratio(vp_indet, n_indet),
                        "systeme": sys_indet, "attendus": n_indet},
        "deduits": deduits,
        "deduits_infondes": infondes,
        "taux_deduits_infondes": _ratio(infondes, deduits),
        "deduits_faux_en_verite": deduit_faux_verite,
        "preuves_valides": _ratio(preuves_ok, preuves_n),
        "exclusions_justes": excl_ok,
        "requetes": len(env.requetes),
        "requetes_refusees": len(env.refus),
        "bits_experience": bx,
        "bits_experience_total": bits_exp,
        "bits_economises": economie,
        "R": economie / bits_exp,
        "revision": {"requises": requises, "requises_justes": requises_ok,
                     "stables": stables, "sur_revisions": sur_revisions},
        "proprietes_crues": systeme.proprietes_crues(),
    }, {qid: {"attendu": att[2][qid], "verite": (vraie_valeur(monde, q["atome"]) if q["type"] == "atome" else None)}
        for qid, q in qs.items()}


def acceleration(serie):
    """serie : liste ordonnée des R̂ d'une famille (§3)."""
    if any(v is None for v in serie):
        return {"acceleration": False, "raison": "R̂ indéfini", "serie": serie}
    hausses = sum(1 for a, b in zip(serie, serie[1:]) if b - a > 0)
    gain = serie[-1] - serie[0]
    return {"acceleration": gain >= SEUIL_GAIN and hausses >= TRANSITIONS_MIN,
            "gain": gain, "hausses": hausses, "serie": serie}


def evaluer_suite(classes, graines):
    mondes = [generer_monde(g) for g in graines]
    res = {}
    for cls in classes:
        sys_ = cls()
        lignes = []
        for m in mondes:
            ligne, correction = evaluer_monde(sys_, m)
            sys_.fin_monde(correction)
            lignes.append(ligne)
        res[cls.nom] = {"mondes": lignes}
    plafond = {l["graine"]: l["R"] for l in res["oracle_proprietes"]["mondes"]}
    for nom, bloc in res.items():
        for l in bloc["mondes"]:
            rp = plafond[l["graine"]]
            l["R_chapeau"] = l["R"] / rp if rp > 0 else None
        fams = {}
        for l in bloc["mondes"]:
            fams.setdefault(l["famille"], []).append(l["R_chapeau"])
        acc = {str(f): acceleration(s) for f, s in sorted(fams.items()) if len(s) == 5}
        n_acc = sum(a["acceleration"] for a in acc.values())
        bloc["familles"] = acc
        bloc["critere_acquerir"] = {
            "familles_accelerees": n_acc, "familles": len(acc),
            "verdict": "REUSSITE" if len(acc) == 4 and n_acc >= FAMILLES_MIN else "ECHEC",
        }
    return res


def _moy(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else None


def _f(v, d=3):
    return "—" if v is None else ("%.*f" % (d, v))


def resume_md(res, graines, horodatage):
    L = ["# E002 — résultats %s" % horodatage, "",
         "Graines %d–%d, %d mondes. Moyennes sur les mondes (phase 2). Voir PREREGISTREMENT.md."
         % (graines[0], graines[-1], len(graines)), "",
         "| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | "
         "précision CONTRA | rappel CONTRA | précision INDÉT | exclusions justes /3 | requêtes | "
         "bits exp. | bits économisés | R | R̂ | révisions requises justes | sur-révisions | critère ACQUÉRIR |",
         "|" + "---|" * 18]
    for nom, b in res.items():
        m = b["mondes"]
        rq = sum(l["revision"]["requises"] for l in m)
        rqj = sum(l["revision"]["requises_justes"] for l in m)
        st = sum(l["revision"]["stables"] for l in m)
        sr = sum(l["revision"]["sur_revisions"] for l in m)
        c = b["critere_acquerir"]
        L.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %d/%d | %d/%d | %s (%d/%d familles) |" % (
            nom, _f(_moy([l["exactitude"] for l in m])),
            _f(_moy([l["taux_deduits_infondes"] for l in m])),
            _f(_moy([l["deduits_faux_en_verite"] for l in m]), 1),
            _f(_moy([l["preuves_valides"] for l in m])),
            _f(_moy([l["contradiction"]["precision"] for l in m])),
            _f(_moy([l["contradiction"]["rappel"] for l in m])),
            _f(_moy([l["indetermine"]["precision"] for l in m])),
            _f(_moy([l["exclusions_justes"] for l in m]), 2),
            _f(_moy([l["requetes"] for l in m]), 1),
            _f(_moy([l["bits_experience_total"] for l in m]), 0),
            _f(_moy([l["bits_economises"] for l in m]), 1),
            _f(_moy([l["R"] for l in m])),
            _f(_moy([l["R_chapeau"] for l in m])),
            rqj, rq, sr, st, c["verdict"], c["familles_accelerees"], c["familles"]))
    L += ["", "## R par monde", "", "| graine | famille | variante | " + " | ".join(res) + " |",
          "|" + "---|" * (3 + len(res))]
    for i, g in enumerate(graines):
        l0 = res[next(iter(res))]["mondes"][i]
        L.append("| %d | %d | %s | %s |" % (g, l0["famille"], l0["variante"],
                                            " | ".join(_f(res[n]["mondes"][i]["R"]) for n in res)))
    L += ["", "## Courbe R̂ par famille (monde n → n+1)", ""]
    for nom, b in res.items():
        for f, a in b["familles"].items():
            L.append("- %s, famille %s : R̂ = %s → accélération %s" % (
                nom, f, " → ".join(_f(v, 2) for v in a["serie"]), "oui" if a["acceleration"] else "non"))
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--graines", default="1-20")
    ap.add_argument("--sortie", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "results"))
    a = ap.parse_args(argv)
    lo, hi = (int(x) for x in a.graines.split("-"))
    graines = list(range(lo, hi + 1))
    res = evaluer_suite(ETALONS, graines)
    h = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H%M%S%z")
    d = os.path.join(a.sortie, h)
    os.makedirs(d)
    with open(os.path.join(d, "resultats.json"), "w", encoding="utf-8") as fh:
        json.dump({"graines": graines, "systemes": res}, fh, ensure_ascii=False, indent=1, sort_keys=True)
    md = resume_md(res, graines, h)
    with open(os.path.join(d, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write(md)
    sys.stdout.write(md)
    print("\nÉcrit dans", d)


if __name__ == "__main__":
    main()
