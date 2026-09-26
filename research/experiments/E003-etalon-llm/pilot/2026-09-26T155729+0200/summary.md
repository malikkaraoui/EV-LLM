# E003 — résumé (2026-09-26T155729+0200)

cases.json sha256 : `8325775b4957bf44664b631ce48096933c6f56d4f245143161405ae6b1e99d0b` · répétitions : 1 · appels : 2 · statuts : {"200": 1, "403": 1}

## LLM-1 — `openai/gpt-4.1-mini`

| cas | question | attendu (préenregistré) | obtenu (majorité des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| PILOTE | x_rectangle | true | true | 1.00 | 1.00–1.00 | 1578.70 | true | false |

## LLM-2 — `google/gemini-3.8-flash`

| cas | question | attendu (préenregistré) | obtenu (majorité des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| PILOTE | x_rectangle | true | NON_PARSE | — | — | — | — | — |

Règle de lecture : PROTOCOLE.md. « P ou confiance » = confiance **verbalisée** (médiane sur les répétitions majoritaires). `NON_PARSE` : raisons dans summary.json.
