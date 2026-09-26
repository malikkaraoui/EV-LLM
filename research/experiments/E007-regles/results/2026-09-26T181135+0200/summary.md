# E001 — résumé (2026-09-26T181135+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : rythme (min 26.0 s), 8 appels · appels : 8 · HTTP 200 : 8

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| B-REGLE | statut | contradiction | coherent | 0.59 | 0.58–0.61 | 495.50 | false | false |
| B-REGLE | e_sup_d | true | true | 0.57 | 0.53–0.62 | 495.50 | true | false |
| B-NEUTRE | statut | contradiction | contradiction | 0.57 | 0.51–0.63 ; choix : contradiction×1, coherent×1 | 669.05 | true | false |
| B-NEUTRE | e_sup_d | true | true | 0.71 | 0.69–0.73 | 669.05 | true | false |
| B-FAIT | statut | contradiction | contradiction | 0.65 | 0.55–0.74 ; choix : contradiction×1, coherent×1 | 519.40 | true | false |
| B-FAIT | e_sup_d | true | false | 0.18 | 0.17–0.20 | 519.40 | false | true |
| B-FAIT2 | statut | contradiction | contradiction | 0.71 | 0.64–0.78 | 561.80 | true | false |
| B-FAIT2 | e_sup_d | true | false | 0.47 | 0.42–0.52 | 561.80 | false | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
