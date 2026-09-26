# E001 — résumé (2026-09-26T180807+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| A1-iii | statut | coherent | coherent | 0.62 | 0.62–0.62 | 1174.10 | true | false |
| A1-iii | e_sup_d | true | true | 0.66 | 0.66–0.66 | 1174.10 | true | false |
| A2-iii | deduction | false | false | 0.25 | 0.25–0.25 | 533.10 | true | false |
| A1-iv | statut | coherent | contradiction | 0.68 | 0.68–0.68 | 843.50 | false | false |
| A1-iv | e_sup_d | true | true | 0.70 | 0.70–0.70 | 843.50 | true | false |
| A2-iv | deduction | false | true | 0.85 | 0.85–0.85 | 631.90 | false | true |
| A1-v | statut | contradiction | contradiction | 0.70 | 0.70–0.70 | 451.70 | true | false |
| A1-v | e_sup_d | true | true | 0.54 | 0.54–0.54 | 451.70 | true | false |
| A2-v | deduction | true | true | 0.96 | 0.96–0.96 | 671.40 | true | false |
| B-FAIT | statut | contradiction | coherent | 0.65 | 0.65–0.65 | 543.00 | false | false |
| B-FAIT | e_sup_d | true | false | 0.19 | 0.19–0.19 | 543.00 | false | true |
| B-FAIT2 | statut | contradiction | contradiction | 0.82 | 0.82–0.82 | 624.00 | true | false |
| B-FAIT2 | e_sup_d | true | false | 0.43 | 0.43–0.43 | 624.00 | false | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
