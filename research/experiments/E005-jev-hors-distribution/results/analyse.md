# E005 — analyse (appel par appel, HTTP 200 seulement)

Statuts HTTP par lancement : `2026-09-26T161655+0200` 9×200, 22×429, 1×503 ; `2026-09-26T161811+0200` 6×200, 16×429, 1×503 ; `2026-09-26T161845+0200` 32×429 ; `2026-09-26T161956+0200` 8×200, 10×429, 2×503 ; `2026-09-26T162058+0200` 4×200, 9×429, 2×503 ; `2026-09-26T162237+0200` 7×200, 21×429, 1×503

Évaluations (question × appel 200) : 42 ; NON_PARSE : 0.

## Conformité par famille

| famille | questions | évaluations | conformes | faux et sûr |
|---|---|---|---|---|
| F1-accords-rares | 10 | 11 | 6/11 (55 %) | 4 |
| F2-homophones-rares | 8 | 8 | 8/8 (100 %) | 0 |
| F3-juste-atypique | 6 | 6 | 4/6 (67 %) | 1 |
| F4-logique-4-pas | 4 | 6 | 2/6 (33 %) | 2 |
| F4-logique-distracteurs | 6 | 8 | 5/8 (62 %) | 2 |
| F5-controle-trivial | 3 | 3 | 3/3 (100 %) | 0 |
| **total** | 37 | 42 | 28/42 (67 %) | 9 |

## Détail par question

| cas | question | attendu | P (par appel) | conformes | faux et sûr |
|---|---|---|---|---|---|
| F1-01 | correcte | true | 0.84 | 1/1 (100 %) | 0 |
| F1-02 | correcte | false | 0.27 | 1/1 (100 %) | 0 |
| F1-03 | correcte | true | 0.56 | 1/1 (100 %) | 0 |
| F1-04 | correcte | false | 0.84 / 0.85 | 0/2 (0 %) | 2 |
| F1-05 | correcte | false | 0.80 | 0/1 (0 %) | 1 |
| F1-06 | correcte | true | 0.91 | 1/1 (100 %) | 0 |
| F1-07 | correcte | true | 0.73 | 1/1 (100 %) | 0 |
| F1-08 | correcte | false | 0.86 | 0/1 (0 %) | 1 |
| F1-09 | correcte | true | 0.58 | 1/1 (100 %) | 0 |
| F1-10 | correcte | false | 0.67 | 0/1 (0 %) | 0 |
| F2-01 | correcte | true | 0.86 | 1/1 (100 %) | 0 |
| F2-02 | correcte | false | 0.15 | 1/1 (100 %) | 0 |
| F2-03 | correcte | false | 0.15 | 1/1 (100 %) | 0 |
| F2-04 | correcte | true | 0.90 | 1/1 (100 %) | 0 |
| F2-05 | correcte | false | 0.32 | 1/1 (100 %) | 0 |
| F2-06 | correcte | true | 0.92 | 1/1 (100 %) | 0 |
| F2-07 | correcte | false | 0.17 | 1/1 (100 %) | 0 |
| F2-08 | correcte | true | 0.94 | 1/1 (100 %) | 0 |
| F3-01 | correcte | true | 0.92 | 1/1 (100 %) | 0 |
| F3-02 | correcte | false | 0.86 | 0/1 (0 %) | 1 |
| F3-03 | correcte | true | 0.89 | 1/1 (100 %) | 0 |
| F3-04 | correcte | false | 0.45 | 1/1 (100 %) | 0 |
| F3-05 | correcte | true | 0.79 | 1/1 (100 %) | 0 |
| F3-06 | correcte | false | 0.77 | 0/1 (0 %) | 0 |
| F4-01 | statut | "contradiction" | coherent 0.88 / coherent 0.89 | 0/2 (0 %) | 2 |
| F4-01 | e_sup_d | true | 0.64 / 0.56 | 2/2 (100 %) | 0 |
| F4-02 | statut | "coherent" | coherent 0.98 | 1/1 (100 %) | 0 |
| F4-02 | e_sup_d | true | 0.95 | 1/1 (100 %) | 0 |
| F4-03 | statut | "indetermine" | coherent 0.76 | 0/1 (0 %) | 0 |
| F4-03 | e_sup_d | true | 0.81 | 1/1 (100 %) | 0 |
| F4-04 | statut | "contradiction" | coherent 0.57 / coherent 0.55 | 0/2 (0 %) | 0 |
| F4-04 | a_sup_f | true | 0.15 / 0.19 | 0/2 (0 %) | 2 |
| F4-05 | statut | "coherent" | coherent 0.92 | 1/1 (100 %) | 0 |
| F4-05 | a_sup_f | false | 0.04 | 1/1 (100 %) | 0 |
| F5-01 | x_sup_z | true | 0.98 | 1/1 (100 %) | 0 |
| F5-01 | z_sup_x | false | 0.02 | 1/1 (100 %) | 0 |
| F5-02 | correcte | true | 0.97 | 1/1 (100 %) | 0 |
| F5-03 | correcte | false | aucune réponse 200 | 0/0 | 0 |

## « Faux et sûr » (le résultat clé)

| lancement | cas | question | attendu | obtenu | P |
|---|---|---|---|---|---|
| 2026-09-26T161655+0200 | F1-04 | correcte | false | true | 0.84 |
| 2026-09-26T161655+0200 | F1-05 | correcte | false | true | 0.80 |
| 2026-09-26T161655+0200 | F1-08 | correcte | false | true | 0.86 |
| 2026-09-26T161956+0200 | F4-01 | statut | "contradiction" | "coherent" | 0.88 |
| 2026-09-26T161956+0200 | F4-04 | a_sup_f | true | false | 0.15 |
| 2026-09-26T161956+0200 | F3-02 | correcte | false | true | 0.86 |
| 2026-09-26T162058+0200 | F4-01 | statut | "contradiction" | "coherent" | 0.89 |
| 2026-09-26T162058+0200 | F4-04 | a_sup_f | true | false | 0.19 |
| 2026-09-26T162058+0200 | F1-04 | correcte | false | true | 0.85 |

Toutes les non-conformités (sûres ou non) : 14.

- 2026-09-26T161655+0200 F1-04 `correcte` : attendu false, obtenu true, P = 0.84 — **faux et sûr**
- 2026-09-26T161655+0200 F1-05 `correcte` : attendu false, obtenu true, P = 0.80 — **faux et sûr**
- 2026-09-26T161655+0200 F1-08 `correcte` : attendu false, obtenu true, P = 0.86 — **faux et sûr**
- 2026-09-26T161655+0200 F1-10 `correcte` : attendu false, obtenu true, P = 0.67
- 2026-09-26T161956+0200 F4-01 `statut` : attendu "contradiction", obtenu "coherent", P = 0.88 — **faux et sûr**
- 2026-09-26T161956+0200 F4-03 `statut` : attendu "indetermine", obtenu "coherent", P = 0.76
- 2026-09-26T161956+0200 F4-04 `statut` : attendu "contradiction", obtenu "coherent", P = 0.57
- 2026-09-26T161956+0200 F4-04 `a_sup_f` : attendu true, obtenu false, P = 0.15 — **faux et sûr**
- 2026-09-26T161956+0200 F3-02 `correcte` : attendu false, obtenu true, P = 0.86 — **faux et sûr**
- 2026-09-26T162058+0200 F4-01 `statut` : attendu "contradiction", obtenu "coherent", P = 0.89 — **faux et sûr**
- 2026-09-26T162058+0200 F4-04 `statut` : attendu "contradiction", obtenu "coherent", P = 0.55
- 2026-09-26T162058+0200 F4-04 `a_sup_f` : attendu true, obtenu false, P = 0.19 — **faux et sûr**
- 2026-09-26T162058+0200 F1-04 `correcte` : attendu false, obtenu true, P = 0.85 — **faux et sûr**
- 2026-09-26T162237+0200 F3-06 `correcte` : attendu false, obtenu true, P = 0.77

## Calibration grossière

a) Questions `boolean` : P(true) renvoyée, binnée, contre la part d'attendus `true` et le taux de conformité.

| bin P(true) | n | part attendu true | conformes |
|---|---|---|---|
| 0.0–0.2 | 7 | 2/7 (29 %) | 5/7 (71 %) |
| 0.2–0.4 | 2 | 0/2 (0 %) | 2/2 (100 %) |
| 0.4–0.6 | 4 | 3/4 (75 %) | 4/4 (100 %) |
| 0.6–0.8 | 5 | 3/5 (60 %) | 3/5 (60 %) |
| 0.8–1.0 | 17 | 12/17 (71 %) | 12/17 (71 %) |

b) Toutes questions : probabilité de la réponse renvoyée (max(P, 1−P) ou P(choix)), binnée, contre le taux de conformité.

| bin P(réponse) | n | conformes |
|---|---|---|
| 0.0–0.2 | 0 | 0/0 |
| 0.2–0.4 | 0 | 0/0 |
| 0.4–0.6 | 6 | 4/6 (67 %) |
| 0.6–0.8 | 8 | 5/8 (62 %) |
| 0.8–1.0 | 28 | 19/28 (68 %) |

## `providerMetadata.typesafe.confidence`

- Questions `choice` : 7 évaluations, `confidence` présent sur 7.
  - 2026-09-26T161956+0200 F4-01 : choix coherent (P 0.88), confidence 0.82
  - 2026-09-26T161956+0200 F4-02 : choix coherent (P 0.98), confidence 0.98
  - 2026-09-26T161956+0200 F4-03 : choix coherent (P 0.76), confidence 0.63
  - 2026-09-26T161956+0200 F4-04 : choix coherent (P 0.57), confidence 0.36
  - 2026-09-26T161956+0200 F4-05 : choix coherent (P 0.92), confidence 0.87
  - 2026-09-26T162058+0200 F4-01 : choix coherent (P 0.89), confidence 0.84
  - 2026-09-26T162058+0200 F4-04 : choix coherent (P 0.55), confidence 0.33
- Questions `boolean` : 35 évaluations, `confidence` présent sur 0.

Fournisseur final (évaluations) : digitalocean ×12, typesafe-ai ×30

