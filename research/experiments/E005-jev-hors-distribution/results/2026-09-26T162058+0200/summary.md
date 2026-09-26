# E001 — résumé (2026-09-26T162058+0200)

cases.json sha256 : `0bb67d455a21333c7749ef42710e182bf6beaa246bd89bba90d85855d8fb37ff` · répétitions : 1 · appels : 15 · HTTP 200 : 4

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| F4-01 | statut | contradiction | coherent | 0.89 | 0.89–0.89 | 598.90 | false | true |
| F4-01 | e_sup_d | true | true | 0.56 | 0.56–0.56 | 598.90 | true | false |
| F4-04 | statut | contradiction | coherent | 0.55 | 0.55–0.55 | 568.50 | false | false |
| F4-04 | a_sup_f | true | false | 0.19 | 0.19–0.19 | 568.50 | false | true |
| F1-04 | correcte | false | true | 0.85 | 0.85–0.85 | 413.80 | false | true |
| F3-04 | correcte | false | NON_PARSE | — | — | — | — | — |
| F3-05 | correcte | true | NON_PARSE | — | — | — | — | — |
| F3-06 | correcte | false | NON_PARSE | — | — | — | — | — |
| F2-06 | correcte | true | NON_PARSE | — | — | — | — | — |
| F2-07 | correcte | false | NON_PARSE | — | — | — | — | — |
| F2-08 | correcte | true | NON_PARSE | — | — | — | — | — |
| F5-01 | x_sup_z | true | true | 0.98 | 0.98–0.98 | 344.50 | true | false |
| F5-01 | z_sup_x | false | false | 0.02 | 0.02–0.02 | 344.50 | true | false |
| F5-02 | correcte | true | NON_PARSE | — | — | — | — | — |
| F5-03 | correcte | false | NON_PARSE | — | — | — | — | — |
| F1-05 | correcte | false | NON_PARSE | — | — | — | — | — |
| F1-08 | correcte | false | NON_PARSE | — | — | — | — | — |
| F3-02 | correcte | false | NON_PARSE | — | — | — | — | — |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
