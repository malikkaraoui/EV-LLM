# E001 — résumé (agregat-2026-09-26T155633+0200)

cases.json sha256 : `49b2dd4aab440b9af4e4e7c7dd4b1cd0dc0ef1af937c88e596b1a5401b82b40e` · répétitions : agregat de 5 lancements (HTTP 200 seulement) · appels : 20 · HTTP 200 : 13

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T2-1 | correcte | false | false | 0.08 | 0.06–0.10 | 519.10 | true | false |
| T2-2 | correcte | true | true | 0.96 | 0.96–0.97 | 502.90 | true | false |
| T2-3 | correcte | true | true | 0.84 | 0.84–0.85 | 556.50 | true | false |
| T2-4 | correcte | false | false | 0.08 | 0.07–0.08 | 482.25 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
