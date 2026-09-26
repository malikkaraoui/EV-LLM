# E007 — analyse (appel par appel, HTTP 200 seulement)

## Lancements

| dossier | appels | statuts HTTP | intervalle min–max (s) |
|---|---|---|---|
| `2026-09-26T173720+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T174027+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T174351+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T174722+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T175047+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T175421+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T175744+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T180111+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T180440+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T180807+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T181135+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T181503+0200` | 2 | 2×200 | 26.0–26.0 |

Total : 90 appels ; 90×200 ; intervalles entre départs consécutifs : n = 89, min 26.0 s, max 26.0 s ; premier appel 2026-09-26T17:37:20+02:00.
Évaluations (question × appel 200) : 117 ; NON_PARSE : 0.

## D — contrôles

| cas | question | attendu | P par appel | médiane | conformes |
|---|---|---|---|---|---|
| D-LOG-VRAI | deduction | true | 0.97 / 0.98 / 0.98 | 0.98 | 3/3 |
| D-LOG-FAUX | deduction | false | 0.02 / 0.02 / 0.02 | 0.02 | 3/3 |
| D-GRAM-FAUX | correcte | false | 0.08 / 0.08 / 0.08 | 0.08 | 3/3 |
| D-GRAM-OK | correcte | true | 0.97 / 0.97 / 0.97 | 0.97 | 3/3 |

## C — règle d'accord écrite dans l'état

Mesure : P(correcte). « sans règle » = E006 (forme fautive : R-F1-0x, 5 appels ; forme correcte : P-F1-0x, 3 appels) et rappel C0 d'E007 (forme correcte, 2 appels, même état qu'E006).

| paire | forme | attendu | sans règle E006 (par appel) | méd. | rappel C0 (par appel) | méd. | avec règle (par appel) | méd. | Δ (avec − sans E006) | conformes avec règle |
|---|---|---|---|---|---|---|---|---|---|---|
| F1-04 | fautive | false | 0.83 / 0.84 / 0.84 / 0.85 / 0.83 | 0.84 | — | — | 0.09 / 0.09 / 0.08 / 0.09 / 0.08 | 0.09 | -0.75 | 5/5 |
| F1-04 | correcte | true | 0.58 / 0.64 / 0.61 | 0.61 | 0.56 / 0.52 | 0.54 | 0.90 / 0.86 / 0.86 / 0.87 / 0.86 | 0.86 | +0.25 | 5/5 |
| F1-05 | fautive | false | 0.87 / 0.83 / 0.83 / 0.84 / 0.84 | 0.84 | — | — | 0.05 / 0.06 / 0.05 / 0.05 / 0.05 | 0.05 | -0.79 | 5/5 |
| F1-05 | correcte | true | 0.90 / 0.91 / 0.90 | 0.90 | 0.92 / 0.91 | 0.92 | 0.92 / 0.93 / 0.93 / 0.92 / 0.93 | 0.93 | +0.03 | 5/5 |
| F1-08 | fautive | false | 0.86 / 0.87 / 0.86 / 0.87 / 0.86 | 0.86 | — | — | 0.09 / 0.09 / 0.08 / 0.08 / 0.09 | 0.09 | -0.77 | 5/5 |
| F1-08 | correcte | true | 0.64 / 0.75 / 0.67 | 0.67 | 0.76 / 0.72 | 0.74 | 0.88 / 0.88 / 0.88 / 0.86 / 0.86 | 0.88 | +0.21 | 5/5 |

| paire | P(correcte) avec règle : correcte − fautive | sans règle (E006) : correcte − fautive | corrige son jugement (règle) |
|---|---|---|---|
| F1-04 | +0.77 | -0.23 | **oui** |
| F1-05 | +0.88 | +0.06 | **oui** |
| F1-08 | +0.79 | -0.19 | **oui** |

## A — ablation de règle

Mesure : médiane de P(contradiction) pour A1 `statut`, de P(true) pour A1 `e_sup_d` et A2 `deduction`. Δ = variante − (i). « change » |Δ| ≥ 0.30, « ne change pas » |Δ| < 0.15.

### A1 — T1-A, R2 manipulée — P(contradiction)

| variante | attendu | choix (P du choix) | P par appel | médiane | Δ vs (i) | lecture | conformes |
|---|---|---|---|---|---|---|---|
| i (regle presente) | "contradiction" | contradiction 0.81 / contradiction 0.75 / contradiction 0.77 | 0.81 / 0.75 / 0.77 | 0.77 | — | référence | 3/3 |
| ii (regle retiree) | "coherent" | contradiction 0.70 / contradiction 0.67 / contradiction 0.72 | 0.70 / 0.67 / 0.72 | 0.70 | -0.07 | ne change pas | 0/3 |
| iii (regle inversee) | "coherent" | coherent 0.62 / coherent 0.57 / coherent 0.62 | 0.33 / 0.38 / 0.34 | 0.34 | -0.43 | change | 3/3 |
| iv (regle remplacee par une phrase hors sujet de meme longueur) | "coherent" | contradiction 0.63 / contradiction 0.58 / contradiction 0.68 | 0.63 / 0.58 / 0.68 | 0.63 | -0.14 | ne change pas | 0/3 |
| v (regle presente + phrase hors sujet ajoutee) | "contradiction" | contradiction 0.77 / contradiction 0.68 / contradiction 0.70 | 0.77 / 0.68 / 0.70 | 0.70 | -0.07 | ne change pas | 3/3 |

### A1 — T1-A, R2 manipulée — P(E > D) (attendu true partout)

| variante | attendu | P par appel | médiane | Δ vs (i) | lecture | conformes |
|---|---|---|---|---|---|---|
| i (regle presente) | true | 0.60 / 0.55 / 0.59 | 0.59 | — | référence | 3/3 |
| ii (regle retiree) | true | 0.65 / 0.61 / 0.67 | 0.65 | +0.06 | ne change pas | 3/3 |
| iii (regle inversee) | true | 0.63 / 0.63 / 0.66 | 0.63 | +0.04 | ne change pas | 3/3 |
| iv (regle remplacee par une phrase hors sujet de meme longueur) | true | 0.68 / 0.75 / 0.70 | 0.70 | +0.11 | ne change pas | 3/3 |
| v (regle presente + phrase hors sujet ajoutee) | true | 0.57 / 0.50 / 0.54 | 0.54 | -0.05 | ne change pas | 3/3 |

### A2 — chaîne A > B > C > D, R1 manipulée — P(A > D)

| variante | attendu | P par appel | médiane | Δ vs (i) | lecture | conformes |
|---|---|---|---|---|---|---|
| i (regle presente) | true | 0.94 / 0.96 / 0.95 | 0.95 | — | référence | 3/3 |
| ii (regle retiree) | false | 0.92 / 0.89 / 0.90 | 0.90 | -0.05 | ne change pas | 0/3 |
| iii (regle inversee) | false | 0.28 / 0.31 / 0.25 | 0.28 | -0.67 | change | 3/3 |
| iv (regle remplacee par une phrase hors sujet de meme longueur) | false | 0.87 / 0.85 / 0.85 | 0.85 | -0.10 | ne change pas | 0/3 |
| v (regle presente + phrase hors sujet ajoutee) | true | 0.97 / 0.96 / 0.96 | 0.96 | +0.01 | ne change pas | 3/3 |

- **A1-statut** : verdict préenregistré → **partiellement** (baisse ≥ 0.30 : ii non, iii oui, iv non ; (v) stable : oui).
- **A2-deduction** : verdict préenregistré → **partiellement** (baisse ≥ 0.30 : ii non, iii oui, iv non ; (v) stable : oui).

## B — distracteur isolé (T1-A, attendu `contradiction`)

| cas | distracteur | choix (P du choix) par appel | P(contradiction) par appel | médiane | tue la contradiction (< 0.5) | P(E > D) médiane |
|---|---|---|---|---|---|---|
| A1-i | aucun (T1-A, = A1-i) | contradiction 0.81 / contradiction 0.75 / contradiction 0.77 | 0.81 / 0.75 / 0.77 | 0.77 | non | 0.59 |
| B-FAIT | fait redondant A > C (= L-DIS1 E006) | coherent 0.65 / contradiction 0.55 / coherent 0.74 | 0.34 / 0.55 / 0.25 | 0.34 | **oui** | 0.19 |
| B-FAIT2 | fait redondant B > D | contradiction 0.82 / contradiction 0.78 / contradiction 0.64 | 0.82 / 0.78 / 0.64 | 0.78 | non | 0.43 |
| B-REGLE | règle 3 non pertinente seule | coherent 0.58 / coherent 0.61 / coherent 0.61 | 0.41 / 0.38 / 0.38 | 0.38 | **oui** | 0.62 |
| B-NEUTRE | fait couleur(A, rouge) seul | contradiction 0.63 / coherent 0.51 / coherent 0.57 | 0.63 / 0.49 / 0.43 | 0.49 | **oui** | 0.73 |
| A1-v | phrase hors sujet ajoutée (A1-v) | contradiction 0.77 / contradiction 0.68 / contradiction 0.70 | 0.77 / 0.68 / 0.70 | 0.70 | non | 0.54 |
