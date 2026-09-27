"""E014 -- diagnostic EXPLORATOIRE (post hoc, non preregistre) sur paires TIREES A NEUF (graine 3120),
jamais sur TEST. (1) interface douce (preregistree) vs dure (argmax du lecteur -> one-hot) ;
(2) graine 5 : ou vont les pointeurs du lecteur ; (3) faux et surs de R1G par graine (TEST deja lu).

  python diagnostic14.py -> resultats/diagnostic.json
"""
import json
import os

import mlx.core as mx
import numpy as np

import d14 as D
from m14 import accumule
from s14 import composition_gelee

ICI = os.path.dirname(os.path.abspath(__file__))


def main():
    out = {"interface": {}, "pointeurs_s5": {}, "faux_surs_R1G": {}}
    frais = D.D13._uniformes(3120, [16, 100, 1000], 100)
    for g in range(1, 6):
        m = composition_gelee(g, os.path.join(ICI, "runs", f"R1L-s{g}", "meilleur.safetensors"))
        for L, paires in frais.items():
            n = L + 1
            S = mx.array(D.encode_plat(paires))
            lu = m.lecteur(S, n, eval_tous=64)
            A, B, _, _ = D.encode_aligne(paires, n)
            ia, ib = np.array(mx.argmax(lu[..., :11], -1)), np.array(mx.argmax(lu[..., 11:], -1))
            dur = mx.array(30.0 * np.concatenate([np.eye(11)[ia], np.eye(11)[ib]], -1))
            r = {}
            for nom, lg in (("douce", accumule(m.i1, lu, 64)), ("dure", accumule(m.i1, dur, 64))):
                tok = np.array(mx.argmax(lg, -1))
                r[nom] = float(np.mean([D.decode(tok[j]) == str(a + b)
                                        for j, (a, b) in enumerate(paires)]))
            r["lecture"] = float(np.mean(((ia == A) & (ib == B)).all(axis=1)))
            pa = np.array(mx.max(mx.softmax(lu[..., :11], -1), -1))
            r["p_lecture_min_med"] = float(np.median(pa.min(axis=1)))
            out["interface"][f"s{g}|{L}"] = r
            print(f"s{g} L={L} : lecture {r['lecture']:.2f} addition douce {r['douce']:.2f} "
                  f"dure {r['dure']:.2f} (p_lecture min med {r['p_lecture_min_med']:.3f})", flush=True)
    # (2) pointeurs du lecteur s5 sur 3 paires de 16 chiffres
    m = composition_gelee(5, os.path.join(ICI, "runs", "R1L-s5", "meilleur.safetensors"))
    paires = frais[16][:3]
    _, pos = m.lecteur(mx.array(D.encode_plat(paires)), 17, garder_pos=True)
    pos = np.array(pos).astype(int)
    for j, (a, b) in enumerate(paires):
        out["pointeurs_s5"][f"{a}+{b}"] = {"pos_plus": 1 + len(str(a)), "pos_egal": 2 + len(str(a)) + len(str(b)),
                                          "tete_a": pos[j, :, 0].tolist(), "tete_b": pos[j, :, 1].tolist()}
    print(json.dumps(out["pointeurs_s5"], indent=0)[:1500])
    # (3) faux et surs de R1G par graine (TEST deja lu une fois, simple re-agregation)
    for g in range(1, 6):
        its = [json.loads(l) for l in open(os.path.join(ICI, "runs", f"R1G-s{g}", "eval.jsonl"))]
        ko = [x for x in its if not x["juste"] and x["jeu"] != "T-ID"]
        out["faux_surs_R1G"][f"s{g}"] = {"faux": len(ko), "faux_surs": sum(x["pmin"] >= 0.8 for x in ko),
                                        "faux_surs_L1000": sum(x["pmin"] >= 0.8 and x["L"] == 1000 for x in ko)}
    print(out["faux_surs_R1G"])
    json.dump(out, open(os.path.join(ICI, "resultats", "diagnostic.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
