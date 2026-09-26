# E001 — résumé (2026-09-26T180440+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| A1-iv | statut | coherent | contradiction | 0.58 | 0.58–0.58 | 392.60 | false | false |
| A1-iv | e_sup_d | true | true | 0.75 | 0.75–0.75 | 392.60 | true | false |
| A2-iv | deduction | false | true | 0.85 | 0.85–0.85 | 510.20 | false | true |
| A1-v | statut | contradiction | contradiction | 0.68 | 0.68–0.68 | 958.10 | true | false |
| A1-v | e_sup_d | true | true | 0.50 | 0.50–0.50 | 958.10 | true | false |
| A2-v | deduction | true | true | 0.96 | 0.96–0.96 | 405.20 | true | false |
| A1-i | statut | contradiction | contradiction | 0.77 | 0.77–0.77 | 708.30 | true | false |
| A1-i | e_sup_d | true | true | 0.59 | 0.59–0.59 | 708.30 | true | false |
| A2-i | deduction | true | true | 0.95 | 0.95–0.95 | 611.60 | true | false |
| A1-ii | statut | coherent | contradiction | 0.72 | 0.72–0.72 | 467.30 | false | false |
| A1-ii | e_sup_d | true | true | 0.67 | 0.67–0.67 | 467.30 | true | false |
| A2-ii | deduction | false | true | 0.90 | 0.90–0.90 | 677.50 | false | true |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
