# E001 — résumé (2026-09-26T161655+0200)

cases.json sha256 : `5f3790074e08446e40860a02d56773ae58bfe92cb8e3a046d3345fb3089d2032` · répétitions : 1 · appels : 32 · HTTP 200 : 9

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| F1-01 | correcte | true | true | 0.84 | 0.84–0.84 | 426.40 | true | false |
| F1-02 | correcte | false | false | 0.27 | 0.27–0.27 | 434.80 | true | false |
| F1-03 | correcte | true | true | 0.56 | 0.56–0.56 | 551.80 | true | false |
| F1-04 | correcte | false | true | 0.84 | 0.84–0.84 | 550.60 | false | true |
| F1-05 | correcte | false | true | 0.80 | 0.80–0.80 | 427.90 | false | true |
| F1-06 | correcte | true | true | 0.91 | 0.91–0.91 | 345.10 | true | false |
| F1-07 | correcte | true | true | 0.73 | 0.73–0.73 | 643.50 | true | false |
| F1-08 | correcte | false | true | 0.86 | 0.86–0.86 | 627.40 | false | true |
| F1-09 | correcte | true | NON_PARSE | — | — | — | — | — |
| F1-10 | correcte | false | true | 0.67 | 0.67–0.67 | 603.40 | false | false |
| F2-01 | correcte | true | NON_PARSE | — | — | — | — | — |
| F2-02 | correcte | false | NON_PARSE | — | — | — | — | — |
| F2-03 | correcte | false | NON_PARSE | — | — | — | — | — |
| F2-04 | correcte | true | NON_PARSE | — | — | — | — | — |
| F2-05 | correcte | false | NON_PARSE | — | — | — | — | — |
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
