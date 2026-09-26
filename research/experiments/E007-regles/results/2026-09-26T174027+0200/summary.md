# E001 — résumé (2026-09-26T174027+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| D-LOG-VRAI | deduction | true | true | 0.98 | 0.98–0.98 | 429.00 | true | false |
| D-LOG-FAUX | deduction | false | false | 0.02 | 0.02–0.02 | 567.30 | true | false |
| D-GRAM-FAUX | correcte | false | false | 0.08 | 0.08–0.08 | 631.90 | true | false |
| D-GRAM-OK | correcte | true | true | 0.97 | 0.97–0.97 | 466.10 | true | false |
| C-F1-04-fautive | correcte | false | false | 0.09 | 0.09–0.09 | 582.00 | true | false |
| C-F1-04-correcte | correcte | true | true | 0.90 | 0.90–0.90 | 426.70 | true | false |
| C-F1-05-fautive | correcte | false | false | 0.05 | 0.05–0.05 | 625.40 | true | false |
| C-F1-05-correcte | correcte | true | true | 0.92 | 0.92–0.92 | 888.70 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
