# E002 — résultats 2026-09-26T160728+0200

Graines 1–20, 20 mondes. Moyennes sur les mondes (phase 2). Voir PREREGISTREMENT.md.

| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | précision CONTRA | rappel CONTRA | précision INDÉT | exclusions justes /3 | requêtes | bits exp. | bits économisés | R | R̂ | révisions requises justes | sur-révisions | critère ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aleatoire | 0.328 | 0.767 | 9.1 | 0.000 | 0.070 | 0.282 | 0.505 | 1.05 | 0.0 | 909 | -33.3 | -0.037 | -3.962 | 44/275 | 1105/1385 | ECHEC (0/4 familles) |
| oracle_proprietes | 1.000 | 0.000 | 4.7 | 1.000 | 1.000 | 1.000 | 1.000 | 3.00 | 0.0 | 909 | -2.8 | -0.003 | 1.000 | 275/275 | 0/1385 | ECHEC (0/4 familles) |
| decouvreur_naif | 0.777 | 0.258 | 8.3 | 0.679 | 0.383 | 0.889 | 0.916 | 3.00 | 62.0 | 1487 | -21.7 | -0.014 | -2.414 | 177/222 | 284/1438 | ECHEC (0/4 familles) |

## R par monde

| graine | famille | variante | aleatoire | oracle_proprietes | decouvreur_naif |
|---|---|---|---|---|---|
| 1 | 0 | A | -0.055 | 0.007 | -0.003 |
| 2 | 0 | A | -0.034 | 0.010 | -0.006 |
| 3 | 0 | A | -0.053 | 0.018 | 0.010 |
| 4 | 0 | A | -0.024 | 0.008 | -0.069 |
| 5 | 0 | A | -0.016 | -0.018 | -0.002 |
| 6 | 1 | B | -0.032 | -0.010 | -0.024 |
| 7 | 1 | B | -0.054 | -0.025 | 0.009 |
| 8 | 1 | B | -0.035 | 0.023 | -0.014 |
| 9 | 1 | B | -0.029 | -0.034 | -0.006 |
| 10 | 1 | B | -0.030 | -0.023 | -0.045 |
| 11 | 2 | A | -0.021 | -0.000 | -0.031 |
| 12 | 2 | A | -0.040 | -0.006 | -0.008 |
| 13 | 2 | A | -0.054 | 0.015 | -0.037 |
| 14 | 2 | A | -0.023 | -0.001 | 0.004 |
| 15 | 2 | A | -0.032 | -0.002 | -0.016 |
| 16 | 3 | B | -0.027 | -0.008 | -0.016 |
| 17 | 3 | B | -0.046 | -0.016 | -0.002 |
| 18 | 3 | B | -0.030 | 0.016 | 0.005 |
| 19 | 3 | B | -0.036 | 0.005 | -0.037 |
| 20 | 3 | B | -0.060 | -0.020 | 0.007 |

## Courbe R̂ par famille (monde n → n+1)

- aleatoire, famille 0 : R̂ = -8.16 → -3.49 → -2.94 → -3.08 → — → accélération non
- aleatoire, famille 1 : R̂ = — → — → -1.52 → — → — → accélération non
- aleatoire, famille 2 : R̂ = — → — → -3.73 → — → — → accélération non
- aleatoire, famille 3 : R̂ = — → — → -1.91 → -6.87 → — → accélération non
- oracle_proprietes, famille 0 : R̂ = 1.00 → 1.00 → 1.00 → 1.00 → — → accélération non
- oracle_proprietes, famille 1 : R̂ = — → — → 1.00 → — → — → accélération non
- oracle_proprietes, famille 2 : R̂ = — → — → 1.00 → — → — → accélération non
- oracle_proprietes, famille 3 : R̂ = — → — → 1.00 → 1.00 → — → accélération non
- decouvreur_naif, famille 0 : R̂ = -0.39 → -0.65 → 0.52 → -8.83 → — → accélération non
- decouvreur_naif, famille 1 : R̂ = — → — → -0.62 → — → — → accélération non
- decouvreur_naif, famille 2 : R̂ = — → — → -2.56 → — → — → accélération non
- decouvreur_naif, famille 3 : R̂ = — → — → 0.30 → -7.09 → — → accélération non
