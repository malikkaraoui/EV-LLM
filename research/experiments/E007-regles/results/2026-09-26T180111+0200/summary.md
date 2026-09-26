# E001 — résumé (2026-09-26T180111+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| A1-v | statut | contradiction | contradiction | 0.77 | 0.77–0.77 | 686.80 | true | false |
| A1-v | e_sup_d | true | true | 0.57 | 0.57–0.57 | 686.80 | true | false |
| A2-v | deduction | true | true | 0.97 | 0.97–0.97 | 854.40 | true | false |
| A1-i | statut | contradiction | contradiction | 0.75 | 0.75–0.75 | 409.00 | true | false |
| A1-i | e_sup_d | true | true | 0.55 | 0.55–0.55 | 409.00 | true | false |
| A2-i | deduction | true | true | 0.96 | 0.96–0.96 | 430.70 | true | false |
| A1-ii | statut | coherent | contradiction | 0.67 | 0.67–0.67 | 814.40 | false | false |
| A1-ii | e_sup_d | true | true | 0.61 | 0.61–0.61 | 814.40 | true | false |
| A2-ii | deduction | false | true | 0.89 | 0.89–0.89 | 408.30 | false | true |
| A1-iii | statut | coherent | coherent | 0.57 | 0.57–0.57 | 539.10 | true | false |
| A1-iii | e_sup_d | true | true | 0.63 | 0.63–0.63 | 539.10 | true | false |
| A2-iii | deduction | false | false | 0.31 | 0.31–0.31 | 1310.90 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
