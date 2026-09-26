# A0-bis — résultats 2026-09-26T174546+0200

Graines 1–20, 20 mondes, bruit d'E002 inchangé. Moyennes sur les mondes (phase 2). Voir PREREGISTREMENT.md.

**Mesure (bis §5)** : plafond-vérificateur R ≤ 0 sur 0/20 mondes → **REPAREE**.

| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | requêtes | bits exp. | bits économisés | R | mondes R > 0 | R̂_diff | R − R_oracle-propriétés | critère ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aleatoire | 0.328 | 0.767 | 9.1 | 0.000 | 0.0 | 909 | -33.3 | -0.0366 | 0/20 | -0.0488 | -0.0336 | ECHEC (1/4 familles) |
| oracle_proprietes | 1.000 | 0.000 | 4.7 | 1.000 | 0.0 | 909 | -2.8 | -0.0031 | 8/20 | -0.0152 | 0.0000 | ECHEC (0/4 familles) |
| plafond_verificateur | 1.000 | 0.000 | 0.0 | 1.000 | 36.5 | 1249 | 15.2 | 0.0122 | 20/20 | 0.0000 | 0.0152 | ECHEC (0/4 familles) |
| decouvreur_naif | 0.777 | 0.258 | 8.3 | 0.679 | 62.0 | 1487 | -21.7 | -0.0142 | 5/20 | -0.0263 | -0.0111 | ECHEC (0/4 familles) |
| a0 | 0.714 | 0.192 | 2.0 | 0.970 | 0.0 | 909 | 1.0 | 0.0011 | 16/20 | -0.0110 | 0.0042 | ECHEC (1/4 familles) |
| a0bis | 0.829 | 0.139 | 3.1 | 0.899 | 22.6 | 1120 | 1.5 | 0.0017 | 16/20 | -0.0105 | 0.0047 | ECHEC (0/4 familles) |
| a0bis_sans_cout_marginal | 0.685 | 0.319 | 6.5 | 0.766 | 0.3 | 912 | -13.4 | -0.0144 | 8/20 | -0.0266 | -0.0113 | ECHEC (0/4 familles) |
| a0bis_sans_memoire_famille | 0.737 | 0.195 | 3.2 | 0.909 | 17.4 | 1071 | -3.1 | -0.0016 | 14/20 | -0.0137 | 0.0015 | ECHEC (0/4 familles) |
| a0bis_sans_bruit_mle | 0.831 | 0.134 | 2.4 | 0.901 | 22.4 | 1118 | 4.9 | 0.0046 | 17/20 | -0.0076 | 0.0077 | ECHEC (0/4 familles) |

## R par monde

| graine | famille | variante | aleatoire | oracle_proprietes | plafond_verificateur | decouvreur_naif | a0 | a0bis | a0bis_sans_cout_marginal | a0bis_sans_memoire_famille | a0bis_sans_bruit_mle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | A | -0.0552 | 0.0068 | 0.0079 | -0.0026 | -0.0159 | 0.0003 | -0.0159 | 0.0003 | 0.0003 |
| 2 | 0 | A | -0.0340 | 0.0097 | 0.0145 | -0.0064 | 0.0007 | 0.0037 | -0.0282 | 0.0013 | 0.0060 |
| 3 | 0 | A | -0.0534 | 0.0182 | 0.0128 | 0.0095 | 0.0014 | 0.0037 | -0.1286 | -0.0041 | -0.0194 |
| 4 | 0 | A | -0.0242 | 0.0079 | 0.0117 | -0.0694 | 0.0011 | -0.0198 | -0.0038 | -0.0065 | -0.0045 |
| 5 | 0 | A | -0.0162 | -0.0178 | 0.0067 | -0.0015 | 0.0009 | 0.0039 | -0.0078 | -0.0301 | 0.0037 |
| 6 | 1 | B | -0.0325 | -0.0101 | 0.0076 | -0.0239 | 0.0045 | 0.0057 | 0.0045 | 0.0042 | 0.0042 |
| 7 | 1 | B | -0.0545 | -0.0247 | 0.0114 | 0.0091 | 0.0014 | 0.0096 | -0.0216 | 0.0012 | 0.0076 |
| 8 | 1 | B | -0.0351 | 0.0230 | 0.0165 | -0.0143 | -0.0043 | 0.0025 | 0.0070 | -0.0422 | 0.0031 |
| 9 | 1 | B | -0.0288 | -0.0343 | 0.0142 | -0.0063 | 0.0000 | 0.0144 | 0.0028 | 0.0032 | 0.0069 |
| 10 | 1 | B | -0.0304 | -0.0226 | 0.0150 | -0.0450 | 0.0018 | 0.0157 | -0.0026 | 0.0043 | 0.0112 |
| 11 | 2 | A | -0.0205 | -0.0001 | 0.0078 | -0.0310 | 0.0026 | 0.0073 | -0.0006 | 0.0036 | 0.0052 |
| 12 | 2 | A | -0.0405 | -0.0060 | 0.0095 | -0.0083 | 0.0053 | 0.0008 | -0.0433 | 0.0055 | 0.0046 |
| 13 | 2 | A | -0.0541 | 0.0145 | 0.0099 | -0.0372 | -0.0051 | -0.0159 | -0.0314 | 0.0015 | 0.0014 |
| 14 | 2 | A | -0.0227 | -0.0014 | 0.0143 | 0.0040 | 0.0048 | -0.0001 | 0.0053 | -0.0001 | 0.0067 |
| 15 | 2 | A | -0.0321 | -0.0016 | 0.0075 | -0.0157 | 0.0030 | 0.0071 | -0.0052 | -0.0045 | -0.0008 |
| 16 | 3 | B | -0.0265 | -0.0075 | 0.0169 | -0.0161 | 0.0090 | 0.0100 | 0.0053 | 0.0082 | 0.0099 |
| 17 | 3 | B | -0.0460 | -0.0163 | 0.0118 | -0.0024 | 0.0019 | 0.0114 | 0.0021 | 0.0017 | 0.0105 |
| 18 | 3 | B | -0.0298 | 0.0156 | 0.0213 | 0.0047 | 0.0025 | 0.0216 | 0.0229 | 0.0114 | 0.0188 |
| 19 | 3 | B | -0.0361 | 0.0053 | 0.0102 | -0.0372 | 0.0010 | -0.0584 | -0.0561 | 0.0036 | 0.0065 |
| 20 | 3 | B | -0.0601 | -0.0197 | 0.0156 | 0.0069 | 0.0062 | 0.0096 | 0.0068 | 0.0061 | 0.0104 |

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
- a0, famille 0 : R̂_diff = -0.0238 → -0.0138 → -0.0114 → -0.0106 → -0.0058 (gain 0.0180, hausses 4/4) → accélération oui
- a0, famille 1 : R̂_diff = -0.0031 → -0.0100 → -0.0207 → -0.0142 → -0.0132 (gain -0.0101, hausses 2/4) → accélération non
- a0, famille 2 : R̂_diff = -0.0052 → -0.0042 → -0.0150 → -0.0095 → -0.0046 (gain 0.0006, hausses 3/4) → accélération non
- a0, famille 3 : R̂_diff = -0.0079 → -0.0099 → -0.0188 → -0.0093 → -0.0095 (gain -0.0015, hausses 1/4) → accélération non
- a0bis, famille 0 : R̂_diff = -0.0076 → -0.0108 → -0.0091 → -0.0315 → -0.0028 (gain 0.0048, hausses 2/4) → accélération non
- a0bis, famille 1 : R̂_diff = -0.0019 → -0.0018 → -0.0139 → 0.0002 → 0.0007 (gain 0.0026, hausses 3/4) → accélération non
- a0bis, famille 2 : R̂_diff = -0.0006 → -0.0087 → -0.0258 → -0.0144 → -0.0004 (gain 0.0001, hausses 2/4) → accélération non
- a0bis, famille 3 : R̂_diff = -0.0070 → -0.0004 → 0.0003 → -0.0687 → -0.0060 (gain 0.0010, hausses 3/4) → accélération non
- a0bis_sans_cout_marginal, famille 0 : R̂_diff = -0.0238 → -0.0428 → -0.1414 → -0.0154 → -0.0145 (gain 0.0092, hausses 2/4) → accélération non
- a0bis_sans_cout_marginal, famille 1 : R̂_diff = -0.0031 → -0.0330 → -0.0094 → -0.0114 → -0.0176 (gain -0.0145, hausses 1/4) → accélération non
- a0bis_sans_cout_marginal, famille 2 : R̂_diff = -0.0084 → -0.0528 → -0.0413 → -0.0089 → -0.0127 (gain -0.0043, hausses 2/4) → accélération non
- a0bis_sans_cout_marginal, famille 3 : R̂_diff = -0.0117 → -0.0096 → 0.0017 → -0.0664 → -0.0088 (gain 0.0029, hausses 3/4) → accélération non
- a0bis_sans_memoire_famille, famille 0 : R̂_diff = -0.0076 → -0.0133 → -0.0169 → -0.0182 → -0.0369 (gain -0.0293, hausses 0/4) → accélération non
- a0bis_sans_memoire_famille, famille 1 : R̂_diff = -0.0034 → -0.0102 → -0.0586 → -0.0110 → -0.0107 (gain -0.0073, hausses 2/4) → accélération non
- a0bis_sans_memoire_famille, famille 2 : R̂_diff = -0.0042 → -0.0040 → -0.0085 → -0.0144 → -0.0121 (gain -0.0078, hausses 2/4) → accélération non
- a0bis_sans_memoire_famille, famille 3 : R̂_diff = -0.0087 → -0.0101 → -0.0099 → -0.0067 → -0.0095 (gain -0.0008, hausses 2/4) → accélération non
- a0bis_sans_bruit_mle, famille 0 : R̂_diff = -0.0076 → -0.0085 → -0.0322 → -0.0162 → -0.0030 (gain 0.0046, hausses 2/4) → accélération non
- a0bis_sans_bruit_mle, famille 1 : R̂_diff = -0.0034 → -0.0038 → -0.0133 → -0.0073 → -0.0039 (gain -0.0004, hausses 2/4) → accélération non
- a0bis_sans_bruit_mle, famille 2 : R̂_diff = -0.0027 → -0.0049 → -0.0086 → -0.0076 → -0.0083 (gain -0.0057, hausses 1/4) → accélération non
- a0bis_sans_bruit_mle, famille 3 : R̂_diff = -0.0071 → -0.0013 → -0.0025 → -0.0038 → -0.0052 (gain 0.0019, hausses 1/4) → accélération non


## Verdict du candidat (PREREGISTREMENT A0-bis §5)

**ECHEC** — ACQUÉRIR a0bis : non ; critère trop permissif (un étalon réussit) : non.

| configuration | M1 R̂_diff moyen | M2 familles accélérées | M3 gain moyen 1er→5e | M4 DÉDUIT faux (vérité) | requêtes moyennes | η fin | la pièce retirée |
|---|---|---|---|---|---|---|---|
| a0bis | -0.0105 | 0 | 0.0021 | 3.10 | 22.6 | 0.123 | — |
| a0bis_sans_cout_marginal | -0.0266 | 0 | -0.0017 | 6.55 | 0.3 | 0.010 | porte |
| a0bis_sans_memoire_famille | -0.0137 | 0 | -0.0113 | 3.25 | 17.4 | 0.147 | porte |
| a0bis_sans_bruit_mle | -0.0076 | 0 | 0.0001 | 2.40 | 22.4 | 0.183 | ne_porte_pas |
| a0 | -0.0110 | 1 | 0.0017 | 2.00 | — | — | — |

## Mémoire par famille de a0bis (famille identifiée pendant le monde → famille de rangement)

- graine 1 (banc : famille 0) : identifiée None, R̂ 0.0000, coût marginal 0.000 bits, requêtes 11
- graine 2 (banc : famille 0) : identifiée 0, R̂ 0.0003, coût marginal 0.003 bits, requêtes 18
- graine 3 (banc : famille 0) : identifiée 0, R̂ 0.0020, coût marginal 0.019 bits, requêtes 14
- graine 4 (banc : famille 0) : identifiée 1, R̂ 0.0037, coût marginal 0.035 bits, requêtes 44
- graine 5 (banc : famille 0) : identifiée 0, R̂ -0.0052, coût marginal 0.000 bits, requêtes 4
- graine 6 (banc : famille 1) : identifiée None, R̂ -0.0016, coût marginal 0.000 bits, requêtes 13
- graine 7 (banc : famille 1) : identifiée 3, R̂ 0.0057, coût marginal 0.053 bits, requêtes 35
- graine 8 (banc : famille 1) : identifiée None, R̂ 0.0077, coût marginal 0.071 bits, requêtes 41
- graine 9 (banc : famille 1) : identifiée 3, R̂ 0.0059, coût marginal 0.055 bits, requêtes 21
- graine 10 (banc : famille 1) : identifiée 3, R̂ 0.0081, coût marginal 0.075 bits, requêtes 26
- graine 11 (banc : famille 2) : identifiée 1, R̂ 0.0040, coût marginal 0.037 bits, requêtes 18
- graine 12 (banc : famille 2) : identifiée None, R̂ 0.0073, coût marginal 0.068 bits, requêtes 24
- graine 13 (banc : famille 2) : identifiée 4, R̂ 0.0073, coût marginal 0.068 bits, requêtes 33
- graine 14 (banc : famille 2) : identifiée None, R̂ 0.0025, coût marginal 0.023 bits, requêtes 18
- graine 15 (banc : famille 2) : identifiée 4, R̂ -0.0043, coût marginal 0.000 bits, requêtes 28
- graine 16 (banc : famille 3) : identifiée 3, R̂ 0.0096, coût marginal 0.089 bits, requêtes 9
- graine 17 (banc : famille 3) : identifiée 6, R̂ 0.0100, coût marginal 0.093 bits, requêtes 18
- graine 18 (banc : famille 3) : identifiée 6, R̂ 0.0096, coût marginal 0.089 bits, requêtes 34
- graine 19 (banc : famille 3) : identifiée 6, R̂ 0.0143, coût marginal 0.134 bits, requêtes 27
- graine 20 (banc : famille 3) : identifiée 6, R̂ -0.0039, coût marginal 0.000 bits, requêtes 16
