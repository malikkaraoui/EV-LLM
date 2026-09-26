# E001 — résumé (agregat-2026-09-26T162249+0200)

cases.json sha256 : `5f3790074e08446e40860a02d56773ae58bfe92cb8e3a046d3345fb3089d2032` · répétitions : agregat de 6 lancements (HTTP 200 seulement) · appels : 151 · HTTP 200 : 34

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| F1-01 | correcte | true | true | 0.84 | 0.84–0.84 | 426.40 | true | false |
| F1-02 | correcte | false | false | 0.27 | 0.27–0.27 | 434.80 | true | false |
| F1-03 | correcte | true | true | 0.56 | 0.56–0.56 | 551.80 | true | false |
| F1-04 | correcte | false | true | 0.84 | 0.84–0.85 | 482.20 | false | true |
| F1-05 | correcte | false | true | 0.80 | 0.80–0.80 | 427.90 | false | true |
| F1-06 | correcte | true | true | 0.91 | 0.91–0.91 | 345.10 | true | false |
| F1-07 | correcte | true | true | 0.73 | 0.73–0.73 | 643.50 | true | false |
| F1-08 | correcte | false | true | 0.86 | 0.86–0.86 | 627.40 | false | true |
| F1-09 | correcte | true | true | 0.58 | 0.58–0.58 | 369.60 | true | false |
| F1-10 | correcte | false | true | 0.67 | 0.67–0.67 | 603.40 | false | false |
| F2-01 | correcte | true | true | 0.86 | 0.86–0.86 | 417.30 | true | false |
| F2-02 | correcte | false | false | 0.15 | 0.15–0.15 | 723.20 | true | false |
| F2-03 | correcte | false | false | 0.15 | 0.15–0.15 | 411.70 | true | false |
| F2-04 | correcte | true | true | 0.90 | 0.90–0.90 | 340.00 | true | false |
| F2-05 | correcte | false | false | 0.32 | 0.32–0.32 | 578.00 | true | false |
| F2-06 | correcte | true | true | 0.92 | 0.92–0.92 | 803.00 | true | false |
| F2-07 | correcte | false | false | 0.17 | 0.17–0.17 | 691.40 | true | false |
| F2-08 | correcte | true | true | 0.94 | 0.94–0.94 | 651.50 | true | false |
| F3-01 | correcte | true | true | 0.92 | 0.92–0.92 | 623.40 | true | false |
| F3-02 | correcte | false | true | 0.86 | 0.86–0.86 | 401.00 | false | true |
| F3-03 | correcte | true | true | 0.89 | 0.89–0.89 | 361.80 | true | false |
| F3-04 | correcte | false | false | 0.45 | 0.45–0.45 | 616.80 | true | false |
| F3-05 | correcte | true | true | 0.79 | 0.79–0.79 | 395.30 | true | false |
| F3-06 | correcte | false | true | 0.77 | 0.77–0.77 | 388.00 | false | false |
| F4-01 | statut | contradiction | coherent | 0.89 | 0.88–0.89 | 671.60 | false | true |
| F4-01 | e_sup_d | true | true | 0.60 | 0.56–0.64 | 671.60 | true | false |
| F4-02 | statut | coherent | coherent | 0.98 | 0.98–0.98 | 394.40 | true | false |
| F4-02 | e_sup_d | true | true | 0.95 | 0.95–0.95 | 394.40 | true | false |
| F4-03 | statut | indetermine | coherent | 0.76 | 0.76–0.76 | 595.00 | false | false |
| F4-03 | e_sup_d | true | true | 0.81 | 0.81–0.81 | 595.00 | true | false |
| F4-04 | statut | contradiction | coherent | 0.56 | 0.55–0.57 | 496.70 | false | false |
| F4-04 | a_sup_f | true | false | 0.17 | 0.15–0.19 | 496.70 | false | true |
| F4-05 | statut | coherent | coherent | 0.92 | 0.92–0.92 | 340.90 | true | false |
| F4-05 | a_sup_f | false | false | 0.04 | 0.04–0.04 | 340.90 | true | false |
| F5-01 | x_sup_z | true | true | 0.98 | 0.98–0.98 | 344.50 | true | false |
| F5-01 | z_sup_x | false | false | 0.02 | 0.02–0.02 | 344.50 | true | false |
| F5-02 | correcte | true | true | 0.97 | 0.97–0.97 | 351.10 | true | false |
| F5-03 | correcte | false | NON_PARSE | — | — | — | — | — |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
