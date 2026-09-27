"""E016-A2 -- tableau des pilotes-gardes A2.1 (graine 0, exclue) -> resultats/a2/pilotes.json.

  python pilotes16a2.py
Diagnostic (non preregistre comme critere) : entropie moyenne des tables au dernier pas, sur les
lignes effectivement utilisees (sens 0-9 + absent, via les codes prives).
"""
import json
import os

import mlx.core as mx
import numpy as np

from m16 import Population

ICI = os.path.dirname(os.path.abspath(__file__))
PILOTES = {"IND-dense": "IND-dense-s0-pilote", "IND-01-curric": "IND-01-curric-s0-pilote"}


def entropie(logits):
    p = np.exp(logits - logits.max(-1, keepdims=True))
    p /= p.sum(-1, keepdims=True)
    return float(-(p * np.log(p + 1e-12)).sum(-1).mean())


def main():
    out = {}
    for nom, d in PILOTES.items():
        e = json.load(open(os.path.join(ICI, "runs", "a2", d, "etat.json")))
        pop = Population(0)
        pop.t.load_weights(os.path.join(ICI, "runs", "a2", d, "poids.safetensors"))
        E, R = np.array(pop.t.E), np.array(pop.t.R)
        best = max(e["val"], key=lambda v: (v["val"], v["pas"]))
        n90 = [int((np.array(v["mat"]) >= 0.9).sum()) for v in e["val"]]
        j = np.array(e["journal"])
        out[nom] = dict(
            decolle=max(n90) >= 5, max_paires_90=max(n90), meilleur=dict(pas=best["pas"], val=round(best["val"], 4)),
            mat_meilleur=best["mat"], C_fin=e["val"][-1]["C"],
            paires_90_par_checkpoint=dict(zip([v["pas"] for v in e["val"]], n90)),
            credit_moyen_fin_ph1=round(float(j[1750:2000, 5].mean()), 4),
            items_exacts_fin_ph1=round(float(j[1750:2000, 3].mean()), 4),
            tours_exacts_ph2=round(float(j[2000:, 2].mean()), 4),
            items_exacts_fin_ph2=round(float(j[3750:, 3].mean()), 4),
            entropie_emetteurs=round(entropie(E), 3), entropie_recepteurs=round(entropie(R), 3),
            entropie_uniforme=round(float(np.log(48)), 3))
        if "curric" in nom:
            out[nom]["items_exacts_1chiffre_pas_750_1000"] = round(float(j[750:1000, 3].mean()), 4)
            out[nom]["items_exacts_pas_1000_1250"] = round(float(j[1000:1250, 3].mean()), 4)
        print(nom, {k: v for k, v in out[nom].items() if k not in ("mat_meilleur", "paires_90_par_checkpoint")})
        print("   paires >= 0.9 par checkpoint :", out[nom]["paires_90_par_checkpoint"])
        print("   matrice meilleur :", best["mat"])
    os.makedirs(os.path.join(ICI, "resultats", "a2"), exist_ok=True)
    json.dump(out, open(os.path.join(ICI, "resultats", "a2", "pilotes.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
