"""Diagnostic HORS PROTOCOLE : mêmes mondes, observations remises à la vérité.

Ne remplace pas les résultats préenregistrés ; sert seulement à isoler la
part du bruit dans le R du plafond et du découvreur (README, « Lecture »).
Usage : python3 diagnostic_sans_bruit.py
"""

import copy

from etalons import DecouvreurNaif, OracleProprietes
from evaluer import evaluer_monde
from monde import generer_monde


def sans_bruit(m):
    m = copy.deepcopy(m)
    for o in m["observations"]:
        if o["bruit"]:
            o["valeur"], o["bruit"] = not o["valeur"], False
    return m


if __name__ == "__main__":
    print("| graine | plafond R (bruit) | plafond R (sans bruit) | découvreur R (bruit) | découvreur R (sans bruit) |")
    print("|---|---|---|---|---|")
    tot = [0.0] * 4
    for g in range(1, 21):
        m = generer_monde(g)
        vals = [evaluer_monde(OracleProprietes(), m)[0]["R"], evaluer_monde(OracleProprietes(), sans_bruit(m))[0]["R"],
                evaluer_monde(DecouvreurNaif(), m)[0]["R"], evaluer_monde(DecouvreurNaif(), sans_bruit(m))[0]["R"]]
        tot = [a + b for a, b in zip(tot, vals)]
        print("| %d | %s |" % (g, " | ".join("%.3f" % v for v in vals)))
    print("| moyenne | %s |" % " | ".join("%.3f" % (t / 20) for t in tot))
