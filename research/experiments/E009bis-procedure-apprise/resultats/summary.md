# E009-bis -- resume (genere par synthese_bis.py)

| run | appris | pas (arret ou plafond) | niveau | T-ID 2/3/4/5 % | ex. uniques | perte |
|---|---|---|---|---|---|---|
| A1-s1 | non | 10000 | 2 | 29.0/0.0/0.0/0.0 | 8248 | 0.134 |
| A1-s2 | non | 10000 | 3 | 0.0/1.5/0.0/0.0 | 276807 | 0.385 |
| A2-L-s1 | non | 10000 | 3 | 42.0/100.0/0.0/0.0 | 341179 | 0.007 |
| A3-s1 | oui | 8000 | 5 | 99.5/100.0/99.5/88.0 | 458474 | 0.027 |
| A3-s2 | non | 10000 | 4 | 97.5/92.0/26.5/0.0 | 539372 | 0.088 |

## A3-s1 -- val

| jeu | exact % | faux surs / faux | abstentions parmi faux |
|---|---|---|---|
| T-ID|2 | 99.5 | 1 / 1 | 0 |
| T-ID|3 | 100.0 | 0 / 0 | 0 |
| T-ID|4 | 99.5 | 1 / 1 | 0 |
| T-ID|5 | 88.0 | 20 / 24 | 0 |
| VAL|6 | 17.3 | 105 / 248 | 3 |
| VAL|7 | 0.0 | 25 / 300 | 0 |
| VAL|8 | 0.0 | 6 / 300 | 0 |

## A3-s1 -- final

| jeu | exact % | faux surs / faux | abstentions parmi faux |
|---|---|---|---|
| ADV-ASYM|1+10 | 0.0 | 1 / 50 | 1 |
| ADV-ASYM|1+100 | 0.0 | 0 / 50 | 23 |
| ADV-ASYM|1+16 | 0.0 | 0 / 50 | 6 |
| ADV-ASYM|1+32 | 0.0 | 0 / 50 | 50 |
| ADV-ASYM|1+64 | 0.0 | 0 / 50 | 48 |
| ADV-ASYM|10+1 | 0.0 | 7 / 50 | 1 |
| ADV-ASYM|10+3 | 0.0 | 3 / 50 | 0 |
| ADV-ASYM|100+1 | 0.0 | 0 / 50 | 0 |
| ADV-ASYM|100+3 | 0.0 | 0 / 50 | 0 |
| ADV-ASYM|16+1 | 0.0 | 1 / 50 | 0 |
| ADV-ASYM|16+3 | 0.0 | 0 / 50 | 0 |
| ADV-ASYM|3+10 | 0.0 | 1 / 50 | 1 |
| ADV-ASYM|3+100 | 0.0 | 0 / 50 | 18 |
| ADV-ASYM|3+16 | 0.0 | 0 / 50 | 0 |
| ADV-ASYM|3+32 | 0.0 | 0 / 50 | 19 |
| ADV-ASYM|3+64 | 0.0 | 0 / 50 | 34 |
| ADV-ASYM|32+1 | 0.0 | 0 / 50 | 1 |
| ADV-ASYM|32+3 | 0.0 | 0 / 50 | 0 |
| ADV-ASYM|64+1 | 0.0 | 0 / 50 | 0 |
| ADV-ASYM|64+3 | 0.0 | 0 / 50 | 0 |
| ADV-RET|10 | 0.0 | 1 / 102 | 0 |
| ADV-RET|100 | 0.0 | 0 / 102 | 1 |
| ADV-RET|16 | 0.0 | 0 / 102 | 0 |
| ADV-RET|32 | 0.0 | 0 / 102 | 1 |
| ADV-RET|64 | 0.0 | 0 / 102 | 1 |
| ADV-ZERO|10 | 0.0 | 12 / 101 | 0 |
| ADV-ZERO|100 | 0.0 | 0 / 101 | 0 |
| ADV-ZERO|16 | 0.0 | 0 / 101 | 0 |
| ADV-ZERO|32 | 0.0 | 0 / 101 | 0 |
| ADV-ZERO|64 | 0.0 | 0 / 101 | 0 |
| TEST|10 | 0.0 | 3 / 200 | 0 |
| TEST|100 | 0.0 | 1 / 200 | 0 |
| TEST|16 | 0.0 | 0 / 200 | 0 |
| TEST|32 | 0.0 | 1 / 200 | 0 |
| TEST|64 | 0.0 | 2 / 200 | 0 |

Systemes : `{"A1": {"graines": [1, 2], "graines_apprises": [], "val8_moy_apprises": null, "confirmation_5_graines": false, "graines_reussies_test16": 0}, "A2-L": {"graines": [1], "graines_apprises": [], "val8_moy_apprises": null, "confirmation_5_graines": false, "graines_reussies_test16": 0}, "A3": {"graines": [1, 2], "graines_apprises": [1], "val8_moy_apprises": 0.0, "confirmation_5_graines": false, "graines_reussies_test16": 0}}`
Calcul runs officiels : 11369.3 s
