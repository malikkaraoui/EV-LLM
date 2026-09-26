# E001 — résumé (2026-09-26T102956+0200)

cases.json sha256 : `8325775b4957bf44664b631ce48096933c6f56d4f245143161405ae6b1e99d0b` · répétitions : 3 · appels : 21 · HTTP 200 : 7

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T1-A | statut | contradiction | contradiction | 0.71 | 0.68–0.76 | 726.70 | true | false |
| T1-A | e_sup_d | true | true | 0.51 | 0.49–0.58 | 726.70 | true | false |
| T1-B | statut | indetermine | indetermine | 0.72 | 0.70–0.73 | 674.60 | true | false |
| T1-B | e_sup_d | true | true | 0.73 | 0.73–0.78 | 674.60 | true | false |
| T1-C | a_sup_c | true | true | 0.97 | 0.97–0.97 | 414.80 | true | false |
| T1-C | c_sup_a | false | false | 0.02 | 0.02–0.02 | 414.80 | true | false |
| T2-1 | correcte | false | NON_PARSE | — | — | — | — | — |
| T2-2 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-3 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-4 | correcte | false | NON_PARSE | — | — | — | — | — |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
