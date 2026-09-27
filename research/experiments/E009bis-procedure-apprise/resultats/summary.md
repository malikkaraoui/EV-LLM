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

Systemes : `{"A1": {"graines": [1, 2], "graines_apprises": [], "val8_moy_apprises": null, "confirmation_5_graines": false, "graines_reussies_test16": 0}, "A2-L": {"graines": [1], "graines_apprises": [], "val8_moy_apprises": null, "confirmation_5_graines": false, "graines_reussies_test16": 0}, "A3": {"graines": [1, 2], "graines_apprises": [1], "val8_moy_apprises": 0.0, "confirmation_5_graines": false, "graines_reussies_test16": 0}}`
Calcul runs officiels : 11369.3 s
