# E006 — analyse (appel par appel, HTTP 200 seulement)

## Lancements

| dossier | appels | statuts HTTP | intervalle min–max (s) |
|---|---|---|---|
| `2026-09-26T164309+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T164616+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T164940+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T165311+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T165636+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T170010+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T170332+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T170701+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T171028+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T171356+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T171725+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T172052+0200` | 8 | 8×200 | 26.0–26.0 |
| `2026-09-26T172420+0200` | 7 | 7×200 | 26.0–26.0 |

Total : 103 appels ; 103×200 ; intervalles entre départs consécutifs : n = 102, min 26.0 s, max 26.0 s.
Évaluations (question × appel 200) : 122 ; NON_PARSE : 0.

## R — réplication des « faux et sûr » d'E005

Règle : répliqué si n ≥ 5, non conformes ≥ 80 % et médiane de P du mauvais côté au-delà du seuil (≥ 0.8 si attendu false ; ≤ 0.2 si attendu true ; P(choix) ≥ 0.8 sur un mauvais choix).

| cas | question | attendu | E005 | E006 P (par appel) | n | non conformes | faux et sûr (appels) | médiane P | répliqué |
|---|---|---|---|---|---|---|---|---|---|
| R-F1-04 | correcte | false | 0.84 / 0.85 | 0.83 / 0.84 / 0.84 / 0.85 / 0.83 | 5 | 5/5 | 5 | 0.84 | **oui** |
| R-F1-05 | correcte | false | 0.80 | 0.87 / 0.83 / 0.83 / 0.84 / 0.84 | 5 | 5/5 | 5 | 0.84 | **oui** |
| R-F1-08 | correcte | false | 0.86 | 0.86 / 0.87 / 0.86 / 0.87 / 0.86 | 5 | 5/5 | 5 | 0.86 | **oui** |
| R-F3-02 | correcte | false | 0.86 | 0.86 / 0.84 / 0.85 / 0.83 / 0.86 | 5 | 5/5 | 5 | 0.85 | **oui** |
| R-F4-01 | statut | "contradiction" | coherent 0.88 / 0.89 | coherent 0.90 / coherent 0.91 / coherent 0.92 / coherent 0.91 / coherent 0.85 | 5 | 5/5 | 5 | 0.91 | **oui** |
| R-F4-04 | a_sup_f | true | 0.15 / 0.19 | 0.37 / 0.25 / 0.17 / 0.20 / 0.13 | 5 | 5/5 | 3 | 0.20 | **oui** |

Autres questions des cas R (non visées par la règle de réplication) :

- R-F4-01 `e_sup_d` (attendu true) : 0.53 / 0.61 / 0.68 / 0.60 / 0.60 — conformes 5/5
- R-F4-04 `statut` (attendu "contradiction") : coherent 0.52 / coherent 0.58 / contradiction 0.50 / coherent 0.54 / coherent 0.57 — conformes 1/5

## P — paires minimales (forme fautive R vs forme correcte P)

| paire | P(correcte) forme fautive (R) | médiane | P(correcte) forme correcte (P) | médiane | écart des médianes (correcte − fautive) |
|---|---|---|---|---|---|
| R-F1-04 / P-F1-04 | 0.83 / 0.84 / 0.84 / 0.85 / 0.83 | 0.84 | 0.58 / 0.64 / 0.61 | 0.61 | -0.23 |
| R-F1-05 / P-F1-05 | 0.87 / 0.83 / 0.83 / 0.84 / 0.84 | 0.84 | 0.90 / 0.91 / 0.90 | 0.90 | +0.06 |
| R-F1-08 / P-F1-08 | 0.86 / 0.87 / 0.86 / 0.87 / 0.86 | 0.86 | 0.64 / 0.75 / 0.67 | 0.67 | -0.19 |

## L — P(true) en fonction du nombre de pas (chaîne transitive, sans R2)

| cas | pas | P(true) par appel | médiane | conformes |
|---|---|---|---|---|
| L-PAS2 | 2 | 0.97 / 0.97 / 0.97 | 0.97 | 3/3 |
| L-PAS3 | 3 | 0.85 / 0.85 / 0.90 | 0.85 | 3/3 |
| L-PAS4 | 4 | 0.95 / 0.94 / 0.95 | 0.95 | 3/3 |
| L-PAS5 | 5 | 0.94 / 0.93 / 0.95 | 0.94 | 3/3 |
| L-PAS6 | 6 | 0.92 / 0.87 / 0.90 | 0.90 | 3/3 |
| *R-F4-04 (réf.)* | 4 + incompatible(A, F) + R2 | 0.37 / 0.25 / 0.17 / 0.20 / 0.13 | 0.20 | 0/5 |

L-PAS4 et R-F4-04 ont les mêmes faits dans le même ordre ; seuls `incompatible(A, F)` et la règle 2 diffèrent.

## L — statut en fonction du nombre de distracteurs (T1-A, attendu `contradiction`)

| cas | distracteurs | choix (P du choix) par appel | P(contradiction) par appel | médiane P(contradiction) | conformes `statut` | P(E > D) médiane |
|---|---|---|---|---|---|---|
| L-DIS0 | 0 | contradiction 0.73 / contradiction 0.67 / contradiction 0.80 | 0.73 / 0.67 / 0.80 | 0.73 | 3/3 | 0.60 |
| L-DIS1 | 1 | coherent 0.65 / coherent 0.60 / coherent 0.69 | 0.34 / 0.39 / 0.30 | 0.34 | 0/3 | 0.18 |
| L-DIS2 | 2 | coherent 0.83 / coherent 0.87 / coherent 0.83 | 0.14 / 0.10 / 0.15 | 0.14 | 0/3 | 0.40 |
| R-F4-01 | 3 | coherent 0.90 / coherent 0.91 / coherent 0.92 / coherent 0.91 / coherent 0.85 | 0.09 / 0.08 / 0.07 / 0.08 / 0.14 | 0.08 | 0/5 | 0.60 |

Le point à 3 distracteurs est R-F4-01 (état identique à F4-01 d'E005, assertion dans `gen_cases.py`).

## C — contamination (E004) : P(true) avec / sans contradiction indépendante

Écart = moyenne P(avec) − moyenne P(sans). Attendu `true` des deux côtés.

| paire | P avec (par appel) | moy. avec | P sans (par appel) | moy. sans | écart | conformes avec / sans |
|---|---|---|---|---|---|---|
| C1 | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 0.97 | 0.97 / 0.98 / 0.97 / 0.98 / 0.98 | 0.98 | -0.006 | 5/5 · 5/5 |
| C2 | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 0.97 | 0.97 / 0.98 / 0.97 / 0.97 / 0.97 | 0.97 | -0.002 | 5/5 · 5/5 |
| C3 | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 0.97 | 0.97 / 0.97 / 0.97 / 0.97 / 0.97 | 0.97 | +0.000 | 5/5 · 5/5 |
| C4 | 0.95 / 0.95 / 0.94 / 0.95 / 0.95 | 0.95 | 0.96 / 0.96 / 0.96 / 0.96 / 0.96 | 0.96 | -0.012 | 5/5 · 5/5 |

Écart par paire : moyenne -0.005, min -0.012, max +0.000 ; signes : 3 négatif(s), 0 positif(s), 1 nul(s).

