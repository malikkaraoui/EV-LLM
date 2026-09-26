# E001 — résumé (2026-09-26T173720+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| D-LOG-VRAI | deduction | true | true | 0.97 | 0.97–0.98 | 892.80 | true | false |
| D-LOG-FAUX | deduction | false | false | 0.02 | 0.02–0.02 | 420.15 | true | false |
| D-GRAM-FAUX | correcte | false | false | 0.08 | 0.08–0.08 | 535.90 | true | false |
| D-GRAM-OK | correcte | true | true | 0.97 | 0.97–0.97 | 661.05 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
