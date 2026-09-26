# A0-ter / oracle — résultats 2026-09-26T181138+0200

Graines 1–20, 20 mondes, bruit d'E002 inchangé. Moyennes sur les mondes (phase 2). Voir PREREGISTREMENT.md.

**Mesure (bis §5)** : plafond-vérificateur R ≤ 0 sur 0/20 mondes → **REPAREE**.

| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | requêtes | bits exp. | bits économisés | R | mondes R > 0 | R̂_diff | R − R_oracle-propriétés | critère ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aleatoire | 0.328 | 0.767 | 9.1 | 0.000 | 0.0 | 909 | -33.3 | -0.0366 | 0/20 | -0.0488 | -0.0336 | ECHEC (1/4 familles) |
| oracle_proprietes | 1.000 | 0.000 | 4.7 | 1.000 | 0.0 | 909 | -2.8 | -0.0031 | 8/20 | -0.0152 | 0.0000 | ECHEC (0/4 familles) |
| plafond_verificateur | 1.000 | 0.000 | 0.0 | 1.000 | 36.5 | 1249 | 15.2 | 0.0122 | 20/20 | 0.0000 | 0.0152 | ECHEC (0/4 familles) |
| decouvreur_naif | 0.777 | 0.258 | 8.3 | 0.679 | 62.0 | 1487 | -21.7 | -0.0142 | 5/20 | -0.0263 | -0.0111 | ECHEC (0/4 familles) |
| a0bis | 0.829 | 0.139 | 3.1 | 0.899 | 22.6 | 1120 | 1.5 | 0.0017 | 16/20 | -0.0105 | 0.0047 | ECHEC (0/4 familles) |
| oracle_acquereur | 0.964 | 0.025 | 0.9 | 0.997 | 18.3 | 1080 | 13.6 | 0.0124 | 20/20 | 0.0003 | 0.0155 | ECHEC (2/4 familles) |
| oracle_amnesique | 0.788 | 0.173 | 2.5 | 0.921 | 26.9 | 1160 | 3.7 | 0.0032 | 16/20 | -0.0090 | 0.0062 | ECHEC (0/4 familles) |
| oracle_exact | 0.964 | 0.025 | 0.9 | 0.997 | 18.2 | 1079 | 13.6 | 0.0124 | 20/20 | 0.0003 | 0.0155 | ECHEC (2/4 familles) |

## R par monde

| graine | famille | variante | aleatoire | oracle_proprietes | plafond_verificateur | decouvreur_naif | a0bis | oracle_acquereur | oracle_amnesique | oracle_exact |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | A | -0.0552 | 0.0068 | 0.0079 | -0.0026 | 0.0003 | 0.0003 | 0.0003 | 0.0003 |
| 2 | 0 | A | -0.0340 | 0.0097 | 0.0145 | -0.0064 | 0.0037 | 0.0152 | 0.0058 | 0.0152 |
| 3 | 0 | A | -0.0534 | 0.0182 | 0.0128 | 0.0095 | 0.0037 | 0.0151 | -0.0053 | 0.0151 |
| 4 | 0 | A | -0.0242 | 0.0079 | 0.0117 | -0.0694 | -0.0198 | 0.0103 | 0.0044 | 0.0104 |
| 5 | 0 | A | -0.0162 | -0.0178 | 0.0067 | -0.0015 | 0.0039 | 0.0080 | 0.0009 | 0.0080 |
| 6 | 1 | B | -0.0325 | -0.0101 | 0.0076 | -0.0239 | 0.0057 | 0.0058 | 0.0067 | 0.0058 |
| 7 | 1 | B | -0.0545 | -0.0247 | 0.0114 | 0.0091 | 0.0096 | 0.0127 | 0.0018 | 0.0127 |
| 8 | 1 | B | -0.0351 | 0.0230 | 0.0165 | -0.0143 | 0.0025 | 0.0188 | 0.0016 | 0.0188 |
| 9 | 1 | B | -0.0288 | -0.0343 | 0.0142 | -0.0063 | 0.0144 | 0.0153 | 0.0040 | 0.0153 |
| 10 | 1 | B | -0.0304 | -0.0226 | 0.0150 | -0.0450 | 0.0157 | 0.0167 | 0.0046 | 0.0167 |
| 11 | 2 | A | -0.0205 | -0.0001 | 0.0078 | -0.0310 | 0.0073 | 0.0056 | 0.0048 | 0.0056 |
| 12 | 2 | A | -0.0405 | -0.0060 | 0.0095 | -0.0083 | 0.0008 | 0.0114 | 0.0081 | 0.0114 |
| 13 | 2 | A | -0.0541 | 0.0145 | 0.0099 | -0.0372 | -0.0159 | 0.0112 | -0.0138 | 0.0112 |
| 14 | 2 | A | -0.0227 | -0.0014 | 0.0143 | 0.0040 | -0.0001 | 0.0168 | 0.0076 | 0.0168 |
| 15 | 2 | A | -0.0321 | -0.0016 | 0.0075 | -0.0157 | 0.0071 | 0.0087 | -0.0013 | 0.0087 |
| 16 | 3 | B | -0.0265 | -0.0075 | 0.0169 | -0.0161 | 0.0100 | 0.0099 | 0.0095 | 0.0099 |
| 17 | 3 | B | -0.0460 | -0.0163 | 0.0118 | -0.0024 | 0.0114 | 0.0134 | 0.0092 | 0.0134 |
| 18 | 3 | B | -0.0298 | 0.0156 | 0.0213 | 0.0047 | 0.0216 | 0.0246 | 0.0140 | 0.0246 |
| 19 | 3 | B | -0.0361 | 0.0053 | 0.0102 | -0.0372 | -0.0584 | 0.0114 | 0.0042 | 0.0114 |
| 20 | 3 | B | -0.0601 | -0.0197 | 0.0156 | 0.0069 | 0.0096 | 0.0175 | -0.0035 | 0.0175 |

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
- a0bis, famille 0 : R̂_diff = -0.0076 → -0.0108 → -0.0091 → -0.0315 → -0.0028 (gain 0.0048, hausses 2/4) → accélération non
- a0bis, famille 1 : R̂_diff = -0.0019 → -0.0018 → -0.0139 → 0.0002 → 0.0007 (gain 0.0026, hausses 3/4) → accélération non
- a0bis, famille 2 : R̂_diff = -0.0006 → -0.0087 → -0.0258 → -0.0144 → -0.0004 (gain 0.0001, hausses 2/4) → accélération non
- a0bis, famille 3 : R̂_diff = -0.0070 → -0.0004 → 0.0003 → -0.0687 → -0.0060 (gain 0.0010, hausses 3/4) → accélération non
- oracle_acquereur, famille 0 : R̂_diff = -0.0076 → 0.0006 → 0.0023 → -0.0014 → 0.0013 (gain 0.0088, hausses 3/4) → accélération oui
- oracle_acquereur, famille 1 : R̂_diff = -0.0018 → 0.0013 → 0.0023 → 0.0011 → 0.0017 (gain 0.0035, hausses 3/4) → accélération non
- oracle_acquereur, famille 2 : R̂_diff = -0.0022 → 0.0019 → 0.0012 → 0.0025 → 0.0012 (gain 0.0033, hausses 2/4) → accélération non
- oracle_acquereur, famille 3 : R̂_diff = -0.0071 → 0.0017 → 0.0033 → 0.0011 → 0.0018 (gain 0.0089, hausses 3/4) → accélération oui
- oracle_amnesique, famille 0 : R̂_diff = -0.0076 → -0.0087 → -0.0181 → -0.0073 → -0.0059 (gain 0.0017, hausses 2/4) → accélération non
- oracle_amnesique, famille 1 : R̂_diff = -0.0009 → -0.0096 → -0.0148 → -0.0102 → -0.0104 (gain -0.0095, hausses 1/4) → accélération non
- oracle_amnesique, famille 2 : R̂_diff = -0.0030 → -0.0014 → -0.0238 → -0.0067 → -0.0089 (gain -0.0058, hausses 2/4) → accélération non
- oracle_amnesique, famille 3 : R̂_diff = -0.0074 → -0.0026 → -0.0072 → -0.0060 → -0.0191 (gain -0.0117, hausses 2/4) → accélération non
- oracle_exact, famille 0 : R̂_diff = -0.0076 → 0.0006 → 0.0023 → -0.0013 → 0.0013 (gain 0.0088, hausses 3/4) → accélération oui
- oracle_exact, famille 1 : R̂_diff = -0.0018 → 0.0013 → 0.0023 → 0.0011 → 0.0017 (gain 0.0035, hausses 3/4) → accélération non
- oracle_exact, famille 2 : R̂_diff = -0.0022 → 0.0019 → 0.0012 → 0.0025 → 0.0012 (gain 0.0033, hausses 2/4) → accélération non
- oracle_exact, famille 3 : R̂_diff = -0.0071 → 0.0017 → 0.0033 → 0.0011 → 0.0018 (gain 0.0089, hausses 3/4) → accélération oui


## Verdict de la Mission 1 (PREREGISTREMENT-oracle §4)

**NON_ATTEIGNABLE** — oracle_acquereur : 2/4 familles accélérées ; oracle_amnesique : 0/4 ; oracle_exact (diagnostic) : 2/4. Mission 2 : non.

| système | M1 R̂_diff moyen | M2 familles accélérées | M3 gain moyen 1er→5e | M4 DÉDUIT faux (vérité) | requêtes moyennes |
|---|---|---|---|---|---|
| oracle_acquereur | 0.0003 | 2 | 0.0062 | 0.90 | 18.3 |
| oracle_amnesique | -0.0090 | 0 | -0.0063 | 2.55 | 26.9 |
| oracle_exact | 0.0003 | 2 | 0.0062 | 0.90 | 18.2 |
| a0bis | -0.0105 | 0 | 0.0021 | 3.10 | 22.6 |

## Diagnostic (§6) : le 1er monde domine-t-il ? la variance noie-t-elle le gain ?

Seuil de gain : 0.005. écart_1 = moyenne(mondes 2–5) − 1er monde.

| système | famille | courbe R̂_diff | gain 1er→5e | hausses | écart_1 | écart-type 2–5 | moyenne 2–5 | accélération |
|---|---|---|---|---|---|---|---|---|
| oracle_acquereur | 0 | -0.0076 → 0.0006 → 0.0023 → -0.0014 → 0.0013 | 0.0088 | 3/4 | 0.0083 | 0.0015 | 0.0007 | oui |
| oracle_acquereur | 1 | -0.0018 → 0.0013 → 0.0023 → 0.0011 → 0.0017 | 0.0035 | 3/4 | 0.0034 | 0.0006 | 0.0016 | non |
| oracle_acquereur | 2 | -0.0022 → 0.0019 → 0.0012 → 0.0025 → 0.0012 | 0.0033 | 2/4 | 0.0039 | 0.0006 | 0.0017 | non |
| oracle_acquereur | 3 | -0.0071 → 0.0017 → 0.0033 → 0.0011 → 0.0018 | 0.0089 | 3/4 | 0.0091 | 0.0009 | 0.0020 | oui |
| oracle_amnesique | 0 | -0.0076 → -0.0087 → -0.0181 → -0.0073 → -0.0059 | 0.0017 | 2/4 | -0.0024 | 0.0055 | -0.0100 | non |
| oracle_amnesique | 1 | -0.0009 → -0.0096 → -0.0148 → -0.0102 → -0.0104 | -0.0095 | 1/4 | -0.0103 | 0.0024 | -0.0113 | non |
| oracle_amnesique | 2 | -0.0030 → -0.0014 → -0.0238 → -0.0067 → -0.0089 | -0.0058 | 2/4 | -0.0071 | 0.0096 | -0.0102 | non |
| oracle_amnesique | 3 | -0.0074 → -0.0026 → -0.0072 → -0.0060 → -0.0191 | -0.0117 | 2/4 | -0.0013 | 0.0072 | -0.0087 | non |
| oracle_exact | 0 | -0.0076 → 0.0006 → 0.0023 → -0.0013 → 0.0013 | 0.0088 | 3/4 | 0.0083 | 0.0015 | 0.0007 | oui |
| oracle_exact | 1 | -0.0018 → 0.0013 → 0.0023 → 0.0011 → 0.0017 | 0.0035 | 3/4 | 0.0034 | 0.0006 | 0.0016 | non |
| oracle_exact | 2 | -0.0022 → 0.0019 → 0.0012 → 0.0025 → 0.0012 | 0.0033 | 2/4 | 0.0039 | 0.0006 | 0.0017 | non |
| oracle_exact | 3 | -0.0071 → 0.0017 → 0.0033 → 0.0011 → 0.0018 | 0.0089 | 3/4 | 0.0091 | 0.0009 | 0.0020 | oui |
| a0bis | 0 | -0.0076 → -0.0108 → -0.0091 → -0.0315 → -0.0028 | 0.0048 | 2/4 | -0.0060 | 0.0124 | -0.0135 | non |
| a0bis | 1 | -0.0019 → -0.0018 → -0.0139 → 0.0002 → 0.0007 | 0.0026 | 3/4 | -0.0018 | 0.0069 | -0.0037 | non |
| a0bis | 2 | -0.0006 → -0.0087 → -0.0258 → -0.0144 → -0.0004 | 0.0001 | 2/4 | -0.0118 | 0.0107 | -0.0123 | non |
| a0bis | 3 | -0.0070 → -0.0004 → 0.0003 → -0.0687 → -0.0060 | 0.0010 | 3/4 | -0.0117 | 0.0334 | -0.0187 | non |

## K_f appliquée (graine, égale aux propriétés vraies du monde courant, nombre de règles)

- oracle_acquereur : g1 —/— ; g2 oui/5 ; g3 oui/5 ; g4 NON/5 ; g5 oui/5 ; g6 —/— ; g7 oui/6 ; g8 oui/6 ; g9 oui/6 ; g10 oui/6 ; g11 —/— ; g12 oui/7 ; g13 oui/7 ; g14 oui/7 ; g15 oui/7 ; g16 —/— ; g17 oui/9 ; g18 oui/9 ; g19 oui/9 ; g20 oui/9
- oracle_exact : g1 —/— ; g2 oui/5 ; g3 oui/5 ; g4 oui/6 ; g5 oui/5 ; g6 —/— ; g7 oui/6 ; g8 oui/6 ; g9 oui/6 ; g10 oui/6 ; g11 —/— ; g12 oui/7 ; g13 oui/7 ; g14 oui/7 ; g15 oui/7 ; g16 —/— ; g17 oui/9 ; g18 oui/9 ; g19 oui/9 ; g20 oui/9
