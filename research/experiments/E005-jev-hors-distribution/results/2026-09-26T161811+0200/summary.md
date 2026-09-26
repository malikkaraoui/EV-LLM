# E001 — résumé (2026-09-26T161811+0200)

cases.json sha256 : `2b4fcf05a1748f73a3482f0e94df7eeab6ba6c4b7a1016ce207eac6c80bb6517` · répétitions : 1 · appels : 23 · HTTP 200 : 6

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| F1-09 | correcte | true | true | 0.58 | 0.58–0.58 | 369.60 | true | false |
| F2-01 | correcte | true | true | 0.86 | 0.86–0.86 | 417.30 | true | false |
| F2-02 | correcte | false | false | 0.15 | 0.15–0.15 | 723.20 | true | false |
| F2-03 | correcte | false | false | 0.15 | 0.15–0.15 | 411.70 | true | false |
| F2-04 | correcte | true | true | 0.90 | 0.90–0.90 | 340.00 | true | false |
| F2-05 | correcte | false | false | 0.32 | 0.32–0.32 | 578.00 | true | false |
| F2-06 | correcte | true | NON_PARSE | — | — | — | — | — |
| F2-07 | correcte | false | NON_PARSE | — | — | — | — | — |
| F2-08 | correcte | true | NON_PARSE | — | — | — | — | — |
| F3-01 | correcte | true | NON_PARSE | — | — | — | — | — |
| F3-02 | correcte | false | NON_PARSE | — | — | — | — | — |
| F3-03 | correcte | true | NON_PARSE | — | — | — | — | — |
| F3-04 | correcte | false | NON_PARSE | — | — | — | — | — |
| F3-05 | correcte | true | NON_PARSE | — | — | — | — | — |
| F3-06 | correcte | false | NON_PARSE | — | — | — | — | — |
| F4-01 | statut | contradiction | NON_PARSE | — | — | — | — | — |
| F4-01 | e_sup_d | true | NON_PARSE | — | — | — | — | — |
| F4-02 | statut | coherent | NON_PARSE | — | — | — | — | — |
| F4-02 | e_sup_d | true | NON_PARSE | — | — | — | — | — |
| F4-03 | statut | indetermine | NON_PARSE | — | — | — | — | — |
| F4-03 | e_sup_d | true | NON_PARSE | — | — | — | — | — |
| F4-04 | statut | contradiction | NON_PARSE | — | — | — | — | — |
| F4-04 | a_sup_f | true | NON_PARSE | — | — | — | — | — |
| F4-05 | statut | coherent | NON_PARSE | — | — | — | — | — |
| F4-05 | a_sup_f | false | NON_PARSE | — | — | — | — | — |
| F5-01 | x_sup_z | true | NON_PARSE | — | — | — | — | — |
| F5-01 | z_sup_x | false | NON_PARSE | — | — | — | — | — |
| F5-02 | correcte | true | NON_PARSE | — | — | — | — | — |
| F5-03 | correcte | false | NON_PARSE | — | — | — | — | — |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
