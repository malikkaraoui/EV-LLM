# E001 — résumé (2026-09-26T181503+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : rythme (min 26.0 s), 2 appels · appels : 2 · HTTP 200 : 2

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| B-REGLE | statut | contradiction | coherent | 0.61 | 0.61–0.61 | 419.50 | false | false |
| B-REGLE | e_sup_d | true | true | 0.62 | 0.62–0.62 | 419.50 | true | false |
| B-NEUTRE | statut | contradiction | coherent | 0.57 | 0.57–0.57 | 407.50 | false | false |
| B-NEUTRE | e_sup_d | true | true | 0.74 | 0.74–0.74 | 407.50 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
