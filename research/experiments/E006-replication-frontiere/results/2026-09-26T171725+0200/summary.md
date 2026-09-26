# E001 — résumé (2026-09-26T171725+0200)

cases.json sha256 : `0245036b80c36d451371a1fa3f7555ba17fb2806d375699b341fb61a3888e042` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| L-PAS4 | deduction | true | true | 0.94 | 0.94–0.94 | 497.80 | true | false |
| L-PAS5 | deduction | true | true | 0.93 | 0.93–0.93 | 429.50 | true | false |
| L-PAS6 | deduction | true | true | 0.87 | 0.87–0.87 | 844.20 | true | false |
| L-DIS0 | statut | contradiction | contradiction | 0.67 | 0.67–0.67 | 407.10 | true | false |
| L-DIS0 | e_sup_d | true | true | 0.59 | 0.59–0.59 | 407.10 | true | false |
| L-DIS1 | statut | contradiction | coherent | 0.60 | 0.60–0.60 | 477.20 | false | false |
| L-DIS1 | e_sup_d | true | false | 0.18 | 0.18–0.18 | 477.20 | false | true |
| L-DIS2 | statut | contradiction | coherent | 0.87 | 0.87–0.87 | 960.80 | false | true |
| L-DIS2 | e_sup_d | true | false | 0.40 | 0.40–0.40 | 960.80 | false | false |
| L-PAS2 | deduction | true | true | 0.97 | 0.97–0.97 | 389.30 | true | false |
| L-PAS3 | deduction | true | true | 0.90 | 0.90–0.90 | 430.50 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
