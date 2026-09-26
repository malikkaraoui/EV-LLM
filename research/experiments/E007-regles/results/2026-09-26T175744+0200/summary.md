# E001 — résumé (2026-09-26T175744+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| A1-i | statut | contradiction | contradiction | 0.81 | 0.81–0.81 | 553.00 | true | false |
| A1-i | e_sup_d | true | true | 0.60 | 0.60–0.60 | 553.00 | true | false |
| A2-i | deduction | true | true | 0.94 | 0.94–0.94 | 594.80 | true | false |
| A1-ii | statut | coherent | contradiction | 0.70 | 0.70–0.70 | 412.30 | false | false |
| A1-ii | e_sup_d | true | true | 0.65 | 0.65–0.65 | 412.30 | true | false |
| A2-ii | deduction | false | true | 0.92 | 0.92–0.92 | 593.20 | false | true |
| A1-iii | statut | coherent | coherent | 0.62 | 0.62–0.62 | 461.40 | true | false |
| A1-iii | e_sup_d | true | true | 0.63 | 0.63–0.63 | 461.40 | true | false |
| A2-iii | deduction | false | false | 0.28 | 0.28–0.28 | 466.30 | true | false |
| A1-iv | statut | coherent | contradiction | 0.63 | 0.63–0.63 | 626.80 | false | false |
| A1-iv | e_sup_d | true | true | 0.68 | 0.68–0.68 | 626.80 | true | false |
| A2-iv | deduction | false | true | 0.87 | 0.87–0.87 | 732.20 | false | true |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
