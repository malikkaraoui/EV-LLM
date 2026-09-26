# E001 — résumé (2026-09-26T161956+0200)

cases.json sha256 : `4037b738438118b3d8dd786362c5c07db876d7529583c02f7f9fb9add9135c16` · répétitions : 1 · appels : 20 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| F4-01 | statut | contradiction | coherent | 0.88 | 0.88–0.88 | 744.30 | false | true |
| F4-01 | e_sup_d | true | true | 0.64 | 0.64–0.64 | 744.30 | true | false |
| F4-02 | statut | coherent | coherent | 0.98 | 0.98–0.98 | 394.40 | true | false |
| F4-02 | e_sup_d | true | true | 0.95 | 0.95–0.95 | 394.40 | true | false |
| F4-03 | statut | indetermine | coherent | 0.76 | 0.76–0.76 | 595.00 | false | false |
| F4-03 | e_sup_d | true | true | 0.81 | 0.81–0.81 | 595.00 | true | false |
| F4-04 | statut | contradiction | coherent | 0.57 | 0.57–0.57 | 424.90 | false | false |
| F4-04 | a_sup_f | true | false | 0.15 | 0.15–0.15 | 424.90 | false | true |
| F4-05 | statut | coherent | coherent | 0.92 | 0.92–0.92 | 340.90 | true | false |
| F4-05 | a_sup_f | false | false | 0.04 | 0.04–0.04 | 340.90 | true | false |
| F3-01 | correcte | true | true | 0.92 | 0.92–0.92 | 623.40 | true | false |
| F3-02 | correcte | false | true | 0.86 | 0.86–0.86 | 401.00 | false | true |
| F3-03 | correcte | true | true | 0.89 | 0.89–0.89 | 361.80 | true | false |
| F3-04 | correcte | false | NON_PARSE | — | — | — | — | — |
| F3-05 | correcte | true | NON_PARSE | — | — | — | — | — |
| F3-06 | correcte | false | NON_PARSE | — | — | — | — | — |
| F2-06 | correcte | true | NON_PARSE | — | — | — | — | — |
| F2-07 | correcte | false | NON_PARSE | — | — | — | — | — |
| F2-08 | correcte | true | NON_PARSE | — | — | — | — | — |
| F5-01 | x_sup_z | true | NON_PARSE | — | — | — | — | — |
| F5-01 | z_sup_x | false | NON_PARSE | — | — | — | — | — |
| F5-02 | correcte | true | NON_PARSE | — | — | — | — | — |
| F5-03 | correcte | false | NON_PARSE | — | — | — | — | — |
| F1-04 | correcte | false | NON_PARSE | — | — | — | — | — |
| F1-05 | correcte | false | NON_PARSE | — | — | — | — | — |
| F1-08 | correcte | false | NON_PARSE | — | — | — | — | — |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
