# E001 — résumé (2026-09-26T172052+0200)

cases.json sha256 : `0245036b80c36d451371a1fa3f7555ba17fb2806d375699b341fb61a3888e042` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| L-PAS4 | deduction | true | true | 0.95 | 0.95–0.95 | 571.70 | true | false |
| L-PAS5 | deduction | true | true | 0.95 | 0.95–0.95 | 394.30 | true | false |
| L-PAS6 | deduction | true | true | 0.90 | 0.90–0.90 | 437.90 | true | false |
| L-DIS0 | statut | contradiction | contradiction | 0.80 | 0.80–0.80 | 599.60 | true | false |
| L-DIS0 | e_sup_d | true | true | 0.61 | 0.61–0.61 | 599.60 | true | false |
| L-DIS1 | statut | contradiction | coherent | 0.69 | 0.69–0.69 | 433.10 | false | false |
| L-DIS1 | e_sup_d | true | false | 0.16 | 0.16–0.16 | 433.10 | false | true |
| L-DIS2 | statut | contradiction | coherent | 0.83 | 0.83–0.83 | 405.50 | false | true |
| L-DIS2 | e_sup_d | true | false | 0.45 | 0.45–0.45 | 405.50 | false | false |
| P-F1-04 | correcte | true | true | 0.58 | 0.58–0.58 | 535.60 | true | false |
| P-F1-05 | correcte | true | true | 0.90 | 0.90–0.90 | 616.40 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
