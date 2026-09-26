# A0 — résultats 2026-09-26T172136+0200

Graines 1–20, 20 mondes, bruit d'E002 inchangé. Moyennes sur les mondes (phase 2). Voir PREREGISTREMENT.md.

**Mesure (bis §5)** : plafond-vérificateur R ≤ 0 sur 0/20 mondes → **REPAREE**.

| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | requêtes | bits exp. | bits économisés | R | mondes R > 0 | R̂_diff | R − R_oracle-propriétés | critère ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aleatoire | 0.328 | 0.767 | 9.1 | 0.000 | 0.0 | 909 | -33.3 | -0.0366 | 0/20 | -0.0488 | -0.0336 | ECHEC (1/4 familles) |
| oracle_proprietes | 1.000 | 0.000 | 4.7 | 1.000 | 0.0 | 909 | -2.8 | -0.0031 | 8/20 | -0.0152 | 0.0000 | ECHEC (0/4 familles) |
| plafond_verificateur | 1.000 | 0.000 | 0.0 | 1.000 | 36.5 | 1249 | 15.2 | 0.0122 | 20/20 | 0.0000 | 0.0152 | ECHEC (0/4 familles) |
| decouvreur_naif | 0.777 | 0.258 | 8.3 | 0.679 | 62.0 | 1487 | -21.7 | -0.0142 | 5/20 | -0.0263 | -0.0111 | ECHEC (0/4 familles) |
| a0 | 0.714 | 0.192 | 2.0 | 0.970 | 0.0 | 909 | 1.0 | 0.0011 | 16/20 | -0.0110 | 0.0042 | ECHEC (1/4 familles) |
| a0_sans_memoire | 0.729 | 0.224 | 3.3 | 0.914 | 0.0 | 909 | -1.5 | -0.0017 | 10/20 | -0.0138 | 0.0014 | ECHEC (1/4 familles) |
| a0_verifie_toujours | 0.753 | 0.158 | 1.0 | 0.911 | 23.1 | 1125 | -0.8 | -0.0006 | 14/20 | -0.0127 | 0.0025 | ECHEC (1/4 familles) |
| a0_verifie_jamais | 0.725 | 0.231 | 3.1 | 0.899 | 0.0 | 909 | -1.4 | -0.0016 | 12/20 | -0.0137 | 0.0015 | ECHEC (1/4 familles) |
| a0_sans_autodiagnostic | 0.711 | 0.283 | 4.2 | 0.829 | 0.0 | 909 | -4.3 | -0.0047 | 10/20 | -0.0169 | -0.0017 | ECHEC (1/4 familles) |

## R par monde

| graine | famille | variante | aleatoire | oracle_proprietes | plafond_verificateur | decouvreur_naif | a0 | a0_sans_memoire | a0_verifie_toujours | a0_verifie_jamais | a0_sans_autodiagnostic |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0 | A | -0.0552 | 0.0068 | 0.0079 | -0.0026 | -0.0159 | -0.0159 | -0.0199 | -0.0256 | -0.0159 |
| 2 | 0 | A | -0.0340 | 0.0097 | 0.0145 | -0.0064 | 0.0007 | 0.0014 | 0.0012 | 0.0014 | 0.0014 |
| 3 | 0 | A | -0.0534 | 0.0182 | 0.0128 | 0.0095 | 0.0014 | -0.0060 | 0.0033 | 0.0034 | 0.0034 |
| 4 | 0 | A | -0.0242 | 0.0079 | 0.0117 | -0.0694 | 0.0011 | -0.0038 | -0.0095 | -0.0038 | -0.0016 |
| 5 | 0 | A | -0.0162 | -0.0178 | 0.0067 | -0.0015 | 0.0009 | 0.0009 | 0.0008 | 0.0009 | 0.0009 |
| 6 | 1 | B | -0.0325 | -0.0101 | 0.0076 | -0.0239 | 0.0045 | -0.0017 | 0.0037 | 0.0045 | -0.0017 |
| 7 | 1 | B | -0.0545 | -0.0247 | 0.0114 | 0.0091 | 0.0014 | 0.0014 | 0.0011 | 0.0014 | 0.0014 |
| 8 | 1 | B | -0.0351 | 0.0230 | 0.0165 | -0.0143 | -0.0043 | 0.0018 | -0.0044 | -0.0061 | 0.0061 |
| 9 | 1 | B | -0.0288 | -0.0343 | 0.0142 | -0.0063 | 0.0000 | 0.0010 | 0.0008 | 0.0010 | 0.0020 |
| 10 | 1 | B | -0.0304 | -0.0226 | 0.0150 | -0.0450 | 0.0018 | -0.0026 | -0.0031 | -0.0026 | 0.0020 |
| 11 | 2 | A | -0.0205 | -0.0001 | 0.0078 | -0.0310 | 0.0026 | 0.0017 | 0.0022 | 0.0026 | -0.0026 |
| 12 | 2 | A | -0.0405 | -0.0060 | 0.0095 | -0.0083 | 0.0053 | 0.0061 | 0.0056 | 0.0061 | 0.0004 |
| 13 | 2 | A | -0.0541 | 0.0145 | 0.0099 | -0.0372 | -0.0051 | -0.0044 | -0.0166 | -0.0030 | -0.0126 |
| 14 | 2 | A | -0.0227 | -0.0014 | 0.0143 | 0.0040 | 0.0048 | -0.0054 | 0.0049 | 0.0061 | -0.0254 |
| 15 | 2 | A | -0.0321 | -0.0016 | 0.0075 | -0.0157 | 0.0030 | -0.0052 | -0.0041 | -0.0026 | -0.0013 |
| 16 | 3 | B | -0.0265 | -0.0075 | 0.0169 | -0.0161 | 0.0090 | 0.0090 | 0.0075 | 0.0090 | 0.0104 |
| 17 | 3 | B | -0.0460 | -0.0163 | 0.0118 | -0.0024 | 0.0019 | -0.0060 | 0.0016 | -0.0035 | -0.0035 |
| 18 | 3 | B | -0.0298 | 0.0156 | 0.0213 | 0.0047 | 0.0025 | 0.0173 | 0.0020 | 0.0025 | 0.0025 |
| 19 | 3 | B | -0.0361 | 0.0053 | 0.0102 | -0.0372 | 0.0010 | 0.0041 | 0.0026 | 0.0041 | -0.0337 |
| 20 | 3 | B | -0.0601 | -0.0197 | 0.0156 | 0.0069 | 0.0062 | -0.0272 | 0.0089 | -0.0272 | -0.0272 |

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
- a0_sans_memoire, famille 0 : R̂_diff = -0.0238 → -0.0131 → -0.0189 → -0.0154 → -0.0058 (gain 0.0180, hausses 3/4) → accélération oui
- a0_sans_memoire, famille 1 : R̂_diff = -0.0093 → -0.0100 → -0.0146 → -0.0132 → -0.0176 (gain -0.0083, hausses 1/4) → accélération non
- a0_sans_memoire, famille 2 : R̂_diff = -0.0061 → -0.0034 → -0.0144 → -0.0197 → -0.0127 (gain -0.0066, hausses 2/4) → accélération non
- a0_sans_memoire, famille 3 : R̂_diff = -0.0079 → -0.0178 → -0.0039 → -0.0062 → -0.0428 (gain -0.0348, hausses 1/4) → accélération non
- a0_verifie_toujours, famille 0 : R̂_diff = -0.0278 → -0.0133 → -0.0095 → -0.0212 → -0.0059 (gain 0.0219, hausses 3/4) → accélération oui
- a0_verifie_toujours, famille 1 : R̂_diff = -0.0039 → -0.0103 → -0.0209 → -0.0134 → -0.0182 (gain -0.0143, hausses 1/4) → accélération non
- a0_verifie_toujours, famille 2 : R̂_diff = -0.0056 → -0.0039 → -0.0266 → -0.0094 → -0.0117 (gain -0.0061, hausses 2/4) → accélération non
- a0_verifie_toujours, famille 3 : R̂_diff = -0.0094 → -0.0102 → -0.0192 → -0.0076 → -0.0067 (gain 0.0027, hausses 2/4) → accélération non
- a0_verifie_jamais, famille 0 : R̂_diff = -0.0335 → -0.0131 → -0.0094 → -0.0154 → -0.0058 (gain 0.0277, hausses 3/4) → accélération oui
- a0_verifie_jamais, famille 1 : R̂_diff = -0.0031 → -0.0100 → -0.0226 → -0.0132 → -0.0176 (gain -0.0145, hausses 1/4) → accélération non
- a0_verifie_jamais, famille 2 : R̂_diff = -0.0052 → -0.0034 → -0.0129 → -0.0082 → -0.0102 (gain -0.0050, hausses 2/4) → accélération non
- a0_verifie_jamais, famille 3 : R̂_diff = -0.0079 → -0.0153 → -0.0188 → -0.0062 → -0.0428 (gain -0.0348, hausses 1/4) → accélération non
- a0_sans_autodiagnostic, famille 0 : R̂_diff = -0.0238 → -0.0131 → -0.0094 → -0.0133 → -0.0058 (gain 0.0180, hausses 3/4) → accélération oui
- a0_sans_autodiagnostic, famille 1 : R̂_diff = -0.0093 → -0.0100 → -0.0104 → -0.0122 → -0.0130 (gain -0.0037, hausses 0/4) → accélération non
- a0_sans_autodiagnostic, famille 2 : R̂_diff = -0.0104 → -0.0091 → -0.0226 → -0.0397 → -0.0088 (gain 0.0016, hausses 2/4) → accélération non
- a0_sans_autodiagnostic, famille 3 : R̂_diff = -0.0066 → -0.0153 → -0.0188 → -0.0440 → -0.0428 (gain -0.0362, hausses 1/4) → accélération non


## Verdict du candidat (PREREGISTREMENT A0 §5)

**ECHEC** — ACQUÉRIR a0 : non ; critère trop permissif (un contrôle réussit) : non.

| configuration | M1 R̂_diff moyen | M2 familles accélérées | M3 gain moyen 1er→5e | M4 DÉDUIT faux (vérité) | pire qu'a0 sur |
|---|---|---|---|---|---|
| a0 | -0.0110 | 1 | 0.0017 | 2.00 | — |
| a0_sans_memoire | -0.0138 | 1 | -0.0079 | 3.30 | M1_R_diff_moyen, M3_gain_moyen_1er_5e, M4_deduits_faux_verite |
| a0_verifie_toujours | -0.0127 | 1 | 0.0010 | 1.00 | M1_R_diff_moyen, M3_gain_moyen_1er_5e |
| a0_verifie_jamais | -0.0137 | 1 | -0.0066 | 3.15 | M1_R_diff_moyen, M3_gain_moyen_1er_5e, M4_deduits_faux_verite |
| a0_sans_autodiagnostic | -0.0169 | 1 | -0.0051 | 4.15 | M1_R_diff_moyen, M3_gain_moyen_1er_5e, M4_deduits_faux_verite |
