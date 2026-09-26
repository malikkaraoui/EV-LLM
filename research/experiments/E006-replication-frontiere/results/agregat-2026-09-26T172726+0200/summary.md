# E001 — résumé (agregat-2026-09-26T172726+0200)

cases.json sha256 : `0245036b80c36d451371a1fa3f7555ba17fb2806d375699b341fb61a3888e042` · répétitions : agregat de 13 lancements (HTTP 200 seulement) · appels : 103 · HTTP 200 : 103

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| R-F1-04 | correcte | false | true | 0.84 | 0.83–0.85 | 516.70 | false | true |
| R-F1-05 | correcte | false | true | 0.84 | 0.83–0.87 | 545.60 | false | true |
| R-F1-08 | correcte | false | true | 0.86 | 0.86–0.87 | 475.70 | false | true |
| R-F3-02 | correcte | false | true | 0.85 | 0.83–0.86 | 410.80 | false | true |
| R-F4-01 | statut | contradiction | coherent | 0.91 | 0.85–0.92 | 496.50 | false | true |
| R-F4-01 | e_sup_d | true | true | 0.60 | 0.53–0.68 | 496.50 | true | false |
| R-F4-04 | statut | contradiction | coherent | 0.54 | 0.50–0.58 ; choix : coherent×4, contradiction×1 | 431.30 | false | false |
| R-F4-04 | a_sup_f | true | false | 0.20 | 0.13–0.37 | 431.30 | false | true |
| C1-avec | deduction | true | true | 0.97 | 0.97–0.97 | 453.50 | true | false |
| C1-sans | deduction | true | true | 0.98 | 0.97–0.98 | 498.10 | true | false |
| C2-avec | deduction | true | true | 0.97 | 0.97–0.97 | 536.20 | true | false |
| C2-sans | deduction | true | true | 0.97 | 0.97–0.98 | 421.40 | true | false |
| C3-avec | deduction | true | true | 0.97 | 0.97–0.97 | 436.60 | true | false |
| C3-sans | deduction | true | true | 0.97 | 0.97–0.97 | 583.00 | true | false |
| C4-avec | deduction | true | true | 0.95 | 0.94–0.95 | 430.50 | true | false |
| C4-sans | deduction | true | true | 0.96 | 0.96–0.96 | 567.20 | true | false |
| L-PAS2 | deduction | true | true | 0.97 | 0.97–0.97 | 429.70 | true | false |
| L-PAS3 | deduction | true | true | 0.85 | 0.85–0.90 | 450.10 | true | false |
| L-PAS4 | deduction | true | true | 0.95 | 0.94–0.95 | 497.80 | true | false |
| L-PAS5 | deduction | true | true | 0.94 | 0.93–0.95 | 429.50 | true | false |
| L-PAS6 | deduction | true | true | 0.90 | 0.87–0.92 | 719.40 | true | false |
| L-DIS0 | statut | contradiction | contradiction | 0.73 | 0.67–0.80 | 425.40 | true | false |
| L-DIS0 | e_sup_d | true | true | 0.60 | 0.59–0.61 | 425.40 | true | false |
| L-DIS1 | statut | contradiction | coherent | 0.65 | 0.60–0.69 | 477.20 | false | false |
| L-DIS1 | e_sup_d | true | false | 0.18 | 0.16–0.21 | 477.20 | false | true |
| L-DIS2 | statut | contradiction | coherent | 0.83 | 0.83–0.87 | 735.20 | false | true |
| L-DIS2 | e_sup_d | true | false | 0.40 | 0.39–0.45 | 735.20 | false | false |
| P-F1-04 | correcte | true | true | 0.61 | 0.58–0.64 | 646.20 | true | false |
| P-F1-05 | correcte | true | true | 0.90 | 0.90–0.91 | 616.40 | true | false |
| P-F1-08 | correcte | true | true | 0.67 | 0.64–0.75 | 401.60 | true | false |

Règle de lecture : voir README.md. `NON_PARSE` = forme de réponse différente du guide ; le corps brut est dans raw.jsonl.
