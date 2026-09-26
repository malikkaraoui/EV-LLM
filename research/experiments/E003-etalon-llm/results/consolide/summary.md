# E003 — résumé (consolide)

cases.json sha256 : `8325775b4957bf44664b631ce48096933c6f56d4f245143161405ae6b1e99d0b` · répétitions : 3 · appels : 109 · statuts : {"200": 72, "429": 37}

## LLM-1 — `openai/gpt-4.1-mini`

| cas | question | attendu (préenregistré) | obtenu (majorité des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T1-A | statut | contradiction | contradiction | 1.00 | 1.00–1.00 | 973.60 | true | false |
| T1-A | e_sup_d | true | false | 1.00 | 0.90–1.00 | 1019.00 | false | true |
| T1-B | statut | indetermine | indetermine | 0.90 | 0.90–0.90 | 1158.60 | true | false |
| T1-B | e_sup_d | true | true | 0.90 | 0.90–0.95 | 958.00 | true | false |
| T1-C | a_sup_c | true | true | 1.00 | 1.00–1.00 | 834.70 | true | false |
| T1-C | c_sup_a | false | false | 1.00 | 1.00–1.00 | 974.80 | true | false |
| T2-1 | correcte | false | false | 0.99 | 0.99–0.99 | 1172.20 | true | false |
| T2-2 | correcte | true | true | 0.99 | 0.99–0.99 | 1003.60 | true | false |
| T2-3 | correcte | true | true | 0.95 | 0.95–0.95 | 896.20 | true | false |
| T2-4 | correcte | false | false | 0.95 | 0.95–0.95 | 2217.50 | true | false |

## LLM-2 — `google/gemini-2.5-flash`

| cas | question | attendu (préenregistré) | obtenu (majorité des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T1-A | statut | contradiction | contradiction | 1.00 | 1.00–1.00 | 7709.05 | true | false |
| T1-A | e_sup_d | true | true | 0.90 | 0.90–0.90 | 7041.50 | true | false |
| T1-B | statut | indetermine | indetermine | 1.00 | 1.00–1.00 | 6734.90 | true | false |
| T1-B | e_sup_d | true | true | 1.00 | 1.00–1.00 | 4876.20 | true | false |
| T1-C | a_sup_c | true | true | 1.00 | 1.00–1.00 | 4057.10 | true | false |
| T1-C | c_sup_a | false | false | 1.00 | 1.00–1.00 | 5223.50 | true | false |
| T2-1 | correcte | false | false | 1.00 | 1.00–1.00 | 4760.00 | true | false |
| T2-2 | correcte | true | true | 1.00 | 1.00–1.00 | 4416.00 | true | false |
| T2-3 | correcte | true | true | 1.00 | 1.00–1.00 | 4593.70 | true | false |
| T2-4 | correcte | false | false | 1.00 | 1.00–1.00 | 4208.10 | true | false |

Règle de lecture : PROTOCOLE.md. « P ou confiance » = confiance **verbalisée** (médiane sur les répétitions majoritaires). `NON_PARSE` : raisons dans summary.json.
