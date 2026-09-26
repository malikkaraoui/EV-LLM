# E001 — résumé (agregat-2026-09-26T181559+0200)

cases.json sha256 : `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` · répétitions : agregat de 12 lancements (HTTP 200 seulement) · appels : 90 · HTTP 200 : 90

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| D-LOG-VRAI | deduction | true | true | 0.98 | 0.97–0.98 | 485.30 | true | false |
| D-LOG-FAUX | deduction | false | false | 0.02 | 0.02–0.02 | 438.00 | true | false |
| D-GRAM-FAUX | correcte | false | false | 0.08 | 0.08–0.08 | 630.80 | true | false |
| D-GRAM-OK | correcte | true | true | 0.97 | 0.97–0.97 | 615.80 | true | false |
| C-F1-04-fautive | correcte | false | false | 0.09 | 0.08–0.09 | 732.20 | true | false |
| C-F1-04-correcte | correcte | true | true | 0.86 | 0.86–0.90 | 426.70 | true | false |
| C-F1-05-fautive | correcte | false | false | 0.05 | 0.05–0.06 | 597.80 | true | false |
| C-F1-05-correcte | correcte | true | true | 0.93 | 0.92–0.93 | 640.20 | true | false |
| C-F1-08-fautive | correcte | false | false | 0.09 | 0.08–0.09 | 459.80 | true | false |
| C-F1-08-correcte | correcte | true | true | 0.88 | 0.86–0.88 | 411.10 | true | false |
| C0-F1-04-correcte | correcte | true | true | 0.54 | 0.52–0.56 | 731.00 | true | false |
| C0-F1-05-correcte | correcte | true | true | 0.92 | 0.91–0.92 | 485.50 | true | false |
| C0-F1-08-correcte | correcte | true | true | 0.74 | 0.72–0.76 | 702.55 | true | false |
| A1-i | statut | contradiction | contradiction | 0.77 | 0.75–0.81 | 553.00 | true | false |
| A1-i | e_sup_d | true | true | 0.59 | 0.55–0.60 | 553.00 | true | false |
| A2-i | deduction | true | true | 0.95 | 0.94–0.96 | 594.80 | true | false |
| A1-ii | statut | coherent | contradiction | 0.70 | 0.67–0.72 | 467.30 | false | false |
| A1-ii | e_sup_d | true | true | 0.65 | 0.61–0.67 | 467.30 | true | false |
| A2-ii | deduction | false | true | 0.90 | 0.89–0.92 | 593.20 | false | true |
| A1-iii | statut | coherent | coherent | 0.62 | 0.57–0.62 | 539.10 | true | false |
| A1-iii | e_sup_d | true | true | 0.63 | 0.63–0.66 | 539.10 | true | false |
| A2-iii | deduction | false | false | 0.28 | 0.25–0.31 | 533.10 | true | false |
| A1-iv | statut | coherent | contradiction | 0.63 | 0.58–0.68 | 626.80 | false | false |
| A1-iv | e_sup_d | true | true | 0.70 | 0.68–0.75 | 626.80 | true | false |
| A2-iv | deduction | false | true | 0.85 | 0.85–0.87 | 631.90 | false | true |
| A1-v | statut | contradiction | contradiction | 0.70 | 0.68–0.77 | 686.80 | true | false |
| A1-v | e_sup_d | true | true | 0.54 | 0.50–0.57 | 686.80 | true | false |
| A2-v | deduction | true | true | 0.96 | 0.96–0.97 | 671.40 | true | false |
| B-FAIT | statut | contradiction | coherent | 0.65 | 0.55–0.74 ; choix : coherent×2, contradiction×1 | 543.00 | false | false |
| B-FAIT | e_sup_d | true | false | 0.19 | 0.17–0.20 | 543.00 | false | true |
| B-FAIT2 | statut | contradiction | contradiction | 0.78 | 0.64–0.82 | 624.00 | true | false |
| B-FAIT2 | e_sup_d | true | false | 0.43 | 0.42–0.52 | 624.00 | false | false |
| B-REGLE | statut | contradiction | coherent | 0.61 | 0.58–0.61 | 447.00 | false | false |
| B-REGLE | e_sup_d | true | true | 0.62 | 0.53–0.62 | 447.00 | true | false |
| B-NEUTRE | statut | contradiction | coherent | 0.57 | 0.51–0.63 ; choix : contradiction×1, coherent×2 | 446.10 | false | false |
| B-NEUTRE | e_sup_d | true | true | 0.73 | 0.69–0.74 | 446.10 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
