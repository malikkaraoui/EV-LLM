# E001 — résumé (2026-09-26T164940+0200)

cases.json sha256 : `0245036b80c36d451371a1fa3f7555ba17fb2806d375699b341fb61a3888e042` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| R-F4-01 | statut | contradiction | coherent | 0.92 | 0.91–0.92 | 456.40 | false | true |
| R-F4-01 | e_sup_d | true | true | 0.64 | 0.60–0.68 | 456.40 | true | false |
| R-F4-04 | statut | contradiction | contradiction | 0.52 | 0.50–0.54 ; choix : contradiction×1, coherent×1 | 603.40 | true | false |
| R-F4-04 | a_sup_f | true | false | 0.18 | 0.17–0.20 | 603.40 | false | true |
| R-F1-04 | correcte | false | true | 0.85 | 0.85–0.85 | 408.30 | false | true |
| R-F1-05 | correcte | false | true | 0.84 | 0.84–0.84 | 699.40 | false | true |
| R-F1-08 | correcte | false | true | 0.87 | 0.87–0.87 | 1278.00 | false | true |
| R-F3-02 | correcte | false | true | 0.83 | 0.83–0.83 | 438.20 | false | true |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
