# E002-bis — résultats 2026-09-26T161842+0200

Graines 1–20, 20 mondes, bruit d'E002 inchangé. Moyennes sur les mondes (phase 2). Voir PREREGISTREMENT.md.

**Mesure (bis §5)** : plafond-vérificateur R ≤ 0 sur 0/20 mondes → **REPAREE**.

| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | requêtes | bits exp. | bits économisés | R | mondes R > 0 | R̂_diff | R − R_oracle-propriétés | critère ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aleatoire | 0.328 | 0.767 | 9.1 | 0.000 | 0.0 | 909 | -33.3 | -0.0366 | 0/20 | -0.0488 | -0.0336 | ECHEC (1/4 familles) |
| oracle_proprietes | 1.000 | 0.000 | 4.7 | 1.000 | 0.0 | 909 | -2.8 | -0.0031 | 8/20 | -0.0152 | 0.0000 | ECHEC (0/4 familles) |
| plafond_verificateur | 1.000 | 0.000 | 0.0 | 1.000 | 36.5 | 1249 | 15.2 | 0.0122 | 20/20 | 0.0000 | 0.0152 | ECHEC (0/4 familles) |
| decouvreur_naif | 0.777 | 0.258 | 8.3 | 0.679 | 62.0 | 1487 | -21.7 | -0.0142 | 5/20 | -0.0263 | -0.0111 | ECHEC (0/4 familles) |

## R par monde

| graine | famille | variante | aleatoire | oracle_proprietes | plafond_verificateur | decouvreur_naif |
|---|---|---|---|---|---|---|
| 1 | 0 | A | -0.0552 | 0.0068 | 0.0079 | -0.0026 |
| 2 | 0 | A | -0.0340 | 0.0097 | 0.0145 | -0.0064 |
| 3 | 0 | A | -0.0534 | 0.0182 | 0.0128 | 0.0095 |
| 4 | 0 | A | -0.0242 | 0.0079 | 0.0117 | -0.0694 |
| 5 | 0 | A | -0.0162 | -0.0178 | 0.0067 | -0.0015 |
| 6 | 1 | B | -0.0325 | -0.0101 | 0.0076 | -0.0239 |
| 7 | 1 | B | -0.0545 | -0.0247 | 0.0114 | 0.0091 |
| 8 | 1 | B | -0.0351 | 0.0230 | 0.0165 | -0.0143 |
| 9 | 1 | B | -0.0288 | -0.0343 | 0.0142 | -0.0063 |
| 10 | 1 | B | -0.0304 | -0.0226 | 0.0150 | -0.0450 |
| 11 | 2 | A | -0.0205 | -0.0001 | 0.0078 | -0.0310 |
| 12 | 2 | A | -0.0405 | -0.0060 | 0.0095 | -0.0083 |
| 13 | 2 | A | -0.0541 | 0.0145 | 0.0099 | -0.0372 |
| 14 | 2 | A | -0.0227 | -0.0014 | 0.0143 | 0.0040 |
| 15 | 2 | A | -0.0321 | -0.0016 | 0.0075 | -0.0157 |
| 16 | 3 | B | -0.0265 | -0.0075 | 0.0169 | -0.0161 |
| 17 | 3 | B | -0.0460 | -0.0163 | 0.0118 | -0.0024 |
| 18 | 3 | B | -0.0298 | 0.0156 | 0.0213 | 0.0047 |
| 19 | 3 | B | -0.0361 | 0.0053 | 0.0102 | -0.0372 |
| 20 | 3 | B | -0.0601 | -0.0197 | 0.0156 | 0.0069 |

## Courbe R̂_diff par famille (monde n → n+1)

- aleatoire, famille 0 : R̂_diff = -0.0631 → -0.0486 → -0.0662 → -0.0359 → -0.0229 (gain 0.0402, hausses 3/4) → accélération oui
- aleatoire, famille 1 : R̂_diff = -0.0401 → -0.0659 → -0.0515 → -0.0430 → -0.0454 (gain -0.0053, hausses 2/4) → accélération non
- aleatoire, famille 2 : R̂_diff = -0.0283 → -0.0500 → -0.0641 → -0.0370 → -0.0397 (gain -0.0114, hausses 1/4) → accélération non
- aleatoire, famille 3 : R̂_diff = -0.0435 → -0.0578 → -0.0511 → -0.0463 → -0.0757 (gain -0.0322, hausses 2/4) → accélération non
- oracle_proprietes, famille 0 : R̂_diff = -0.0011 → -0.0048 → 0.0054 → -0.0038 → -0.0246 (gain -0.0234, hausses 1/4) → accélération non
- oracle_proprietes, famille 1 : R̂_diff = -0.0177 → -0.0361 → 0.0066 → -0.0485 → -0.0376 (gain -0.0199, hausses 2/4) → accélération non
- oracle_proprietes, famille 2 : R̂_diff = -0.0080 → -0.0155 → 0.0046 → -0.0156 → -0.0091 (gain -0.0012, hausses 2/4) → accélération non
- oracle_proprietes, famille 3 : R̂_diff = -0.0245 → -0.0281 → -0.0057 → -0.0050 → -0.0353 (gain -0.0109, hausses 2/4) → accélération non
- plafond_verificateur, famille 0 : R̂_diff = 0.0000 → 0.0000 → 0.0000 → 0.0000 → 0.0000 (gain 0.0000, hausses 0/4) → accélération non
- plafond_verificateur, famille 1 : R̂_diff = 0.0000 → 0.0000 → 0.0000 → 0.0000 → 0.0000 (gain 0.0000, hausses 0/4) → accélération non
- plafond_verificateur, famille 2 : R̂_diff = 0.0000 → 0.0000 → 0.0000 → 0.0000 → 0.0000 (gain 0.0000, hausses 0/4) → accélération non
- plafond_verificateur, famille 3 : R̂_diff = 0.0000 → 0.0000 → 0.0000 → 0.0000 → 0.0000 (gain 0.0000, hausses 0/4) → accélération non
- decouvreur_naif, famille 0 : R̂_diff = -0.0105 → -0.0209 → -0.0033 → -0.0811 → -0.0082 (gain 0.0023, hausses 2/4) → accélération non
- decouvreur_naif, famille 1 : R̂_diff = -0.0315 → -0.0023 → -0.0307 → -0.0205 → -0.0600 (gain -0.0285, hausses 2/4) → accélération non
- decouvreur_naif, famille 2 : R̂_diff = -0.0388 → -0.0178 → -0.0472 → -0.0102 → -0.0232 (gain 0.0156, hausses 2/4) → accélération non
- decouvreur_naif, famille 3 : R̂_diff = -0.0331 → -0.0141 → -0.0166 → -0.0475 → -0.0087 (gain 0.0243, hausses 2/4) → accélération non
