# E003 — résumé (2026-09-26T165127+0200)

cases.json sha256 : `8325775b4957bf44664b631ce48096933c6f56d4f245143161405ae6b1e99d0b` · répétitions : 3 · appels : 8 · statuts : {"200": 8}

## LLM-1 — `openai/gpt-4.1-mini`

| cas | question | attendu (préenregistré) | obtenu (majorité des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T1-A | statut | contradiction | NON_PARSE | — | — | — | — | — |
| T1-A | e_sup_d | true | NON_PARSE | — | — | — | — | — |
| T1-B | statut | indetermine | NON_PARSE | — | — | — | — | — |
| T1-B | e_sup_d | true | NON_PARSE | — | — | — | — | — |
| T1-C | a_sup_c | true | NON_PARSE | — | — | — | — | — |
| T1-C | c_sup_a | false | NON_PARSE | — | — | — | — | — |
| T2-1 | correcte | false | NON_PARSE | — | — | — | — | — |
| T2-2 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-3 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-4 | correcte | false | NON_PARSE | — | — | — | — | — |

## LLM-2 — `google/gemini-2.5-flash`

| cas | question | attendu (préenregistré) | obtenu (majorité des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T1-A | statut | contradiction | NON_PARSE | — | — | — | — | — |
| T1-A | e_sup_d | true | NON_PARSE | — | — | — | — | — |
| T1-B | statut | indetermine | NON_PARSE | — | — | — | — | — |
| T1-B | e_sup_d | true | true | 1.00 | 1.00–1.00 | 5327.00 | true | false |
| T1-C | a_sup_c | true | true | 1.00 | 1.00–1.00 | 4197.15 | true | false |
| T1-C | c_sup_a | false | false | 1.00 | 1.00–1.00 | 5223.50 | true | false |
| T2-1 | correcte | false | NON_PARSE | — | — | — | — | — |
| T2-2 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-3 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-4 | correcte | false | NON_PARSE | — | — | — | — | — |

Règle de lecture : PROTOCOLE.md. « P ou confiance » = confiance **verbalisée** (médiane sur les répétitions majoritaires). `NON_PARSE` : raisons dans summary.json.
