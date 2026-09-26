# E001 — résumé (2026-09-26T155621+0200)

cases.json sha256 : `49b2dd4aab440b9af4e4e7c7dd4b1cd0dc0ef1af937c88e596b1a5401b82b40e` · répétitions : 1 · appels : 4 · HTTP 200 : 2

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T2-1 | correcte | false | false | 0.07 | 0.07–0.07 | 377.40 | true | false |
| T2-2 | correcte | true | true | 0.97 | 0.97–0.97 | 688.30 | true | false |
| T2-3 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-4 | correcte | false | NON_PARSE | — | — | — | — | — |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
