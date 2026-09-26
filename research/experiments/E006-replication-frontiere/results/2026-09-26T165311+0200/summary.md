# E001 — résumé (2026-09-26T165311+0200)

cases.json sha256 : `0245036b80c36d451371a1fa3f7555ba17fb2806d375699b341fb61a3888e042` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| R-F1-04 | correcte | false | true | 0.83 | 0.83–0.83 | 810.60 | false | true |
| R-F1-05 | correcte | false | true | 0.84 | 0.84–0.84 | 545.60 | false | true |
| R-F1-08 | correcte | false | true | 0.86 | 0.86–0.86 | 475.70 | false | true |
| R-F3-02 | correcte | false | true | 0.86 | 0.86–0.86 | 401.30 | false | true |
| R-F4-01 | statut | contradiction | coherent | 0.85 | 0.85–0.85 | 496.50 | false | true |
| R-F4-01 | e_sup_d | true | true | 0.60 | 0.60–0.60 | 496.50 | true | false |
| R-F4-04 | statut | contradiction | coherent | 0.57 | 0.57–0.57 | 414.90 | false | false |
| R-F4-04 | a_sup_f | true | false | 0.13 | 0.13–0.13 | 414.90 | false | true |
| C1-avec | deduction | true | true | 0.97 | 0.97–0.97 | 895.30 | true | false |
| C1-sans | deduction | true | true | 0.97 | 0.97–0.97 | 369.00 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
