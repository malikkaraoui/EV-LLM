# E006 — répliquer les « faux et sûr » de Jev, cartographier la frontière, tester la contamination (E004)

Mandat M0011, 2026-09-26, branche `exp/e006-replication-frontiere` (partie de `origin/exp/e005-jev-hors-distribution` @ `08d80f7`). Sonde, pas benchmark.

## Hypothèses

1. **Réplication** [HYPOTHÈSE] : les 6 « faux et sûr » d'E005 (1 à 2 réponses chacun) se reproduisent sur ≥ 5 réponses : F1-04 « se sont lavées les mains », F1-05 « se sont parlés », F1-08 « qu'elle a faites faire », F3-02 « Ci-jointe la facture » (attente à confirmer par R004), F4-01 (T1-A + distracteurs → `coherent`), F4-04 (A > F en 4 pas → nié).
2. **Frontière** [HYPOTHÈSE] : la déduction transitive se dégrade avec le nombre de pas, et la détection de contradiction de T1-A disparaît quand on ajoute des distracteurs.
3. **Contamination** (issue #5, E004) [HYPOTHÈSE] : une contradiction présente **ailleurs** dans l'état fait baisser P(true) sur une déduction transitive indépendante (signal d'E001 : T1-A vs T1-B, `e_sup_d` 0.49–0.58 vs 0.73–0.78).

## Protocole

- **Corpus préenregistré** : [`cases.json`](cases.json) (25 cas, 30 questions), engendré par [`gen_cases.py`](gen_cases.py), sha256 `0245036b80c36d451371a1fa3f7555ba17fb2806d375699b341fb61a3888e042`. Committé et poussé **avant le premier appel** (commit `820d85b`, 16:43:02 ; premier appel 16:43:09). Même schéma qu'E001/E005 + `justification`, `groupe`, `cible`.
  - **R** (6 cas, cible 5) : cas E005 recopiés à l'identique (assertion champ par champ sur `state`, `questions`, `attendu`, `justification`).
  - **C** (4 paires, cible 5) : même déduction transitive (P > R en 1 pas, P > S en 2 pas) sur un sous-graphe **disjoint** d'un bloc A/B/C ; membre `avec` = R2 violée dans le bloc, membre `sans` = **une lettre** change (`incompatible(A, C)` → `incompatible(A, D)`, ou `incompatible(A, B)` → `incompatible(A, C)`), aucune règle violée. C1 : 1 pas, contradiction déduite ; C2 : 2 pas ; C3 : 1 pas, contradiction directe ; C4 : 2 pas, bloc placé avant. Mesure : écart moyen P(avec) − P(sans).
  - **L** (cible 3) : chaîne transitive de 2 à 6 pas, faits mélangés (graine = k), sans R2 ; **L-PAS4 = R-F4-04 sans `incompatible(A, F)` ni R2** (mêmes faits, même ordre). T1-A d'E001 avec 0, 1 (A > C), 2 (+ règle 3 non pertinente) distracteurs ; le point à **3 distracteurs est R-F4-01** (état identique, assertion).
  - **P** (3 cas, cible 3) : forme correcte de F1-04 (= F1-03 d'E005), F1-05 (« se sont parlé »), F1-08 (= F1-07 d'E005).
- **Attentes logiques recalculées sans Jev** : [`verifie_logique.py`](verifie_logique.py) (fermeture transitive, R2 ; vérifie aussi que le membre `avec` viole R2 et pas le membre `sans`) → 18/18, mutation détectée.
- **Appels** : [`run_paced.py`](run_paced.py) importe `run.call` d'E001 (non dupliqué, E001 non modifié) ; départs espacés d'**au moins 26 s** (attente `time.sleep` interne, y compris entre deux invocations, d'après l'heure du dernier appel enregistré) ; **≤ 8 appels par invocation** ; budget dur 130 appels ; arrêt sur 401/403/404 ou 3 échecs consécutifs. Ordre de choix fixé avant tout appel : groupes R, C, L, P ; dans un groupe, le cas qui a le moins de réponses 200 (égalité : ordre du fichier). Tests : [`test_run_paced.py`](test_run_paced.py) (horloge et appels simulés, 12 tests).
- Sorties écrites directement dans `results/<horodatage>/` (plus de déplacement : `run.py` n'est pas lancé, seule sa fonction d'appel est importée). `raw.jsonl` (en-têtes) ignoré par git ; `raw.public.jsonl` = `raw.jsonl` sans `response_headers`, égalité vérifiée par le script à l'écriture.
- **Agrégat** : `aggregate.py` d'E001, non modifié. **Analyse** : [`analyse.py`](analyse.py) → [`results/analyse.md`](results/analyse.md), appel par appel.
- **Règles de lecture** (fixées avant tout appel) : celles d'E001/E005 (conforme ; « faux et sûr » = non conforme avec P ≥ 0.8 pour un attendu `false`, P ≤ 0.2 pour un attendu `true`, P(choix) ≥ 0.8 sur un mauvais `choice`). **Répliqué** = n ≥ 5, non conformes ≥ 80 %, et médiane de P du mauvais côté au-delà du seuil.

## Rejouer

```
cd research/experiments/E006-replication-frontiere
python3 gen_cases.py && python3 verifie_logique.py     # corpus (sha256 identique) + attentes
python3 -m unittest test_run_paced                      # 12 tests, zero reseau
python3 run_paced.py                                    # <= 8 appels, a relancer jusqu'au code 5
python3 ../E001-jev-sonde/aggregate.py --cases cases.json --out-root results results/2026-*
python3 analyse.py
```

## Résultats

### Appels (2026-09-26, 16:43:09 → 17:27:22)

13 invocations de `run_paced.py` (12 × 8 appels + 1 × 7), puis une 14ᵉ qui sort en code 5 (« rien à faire »). **103 appels, 103 × HTTP 200** (budget 130) ; aucun 429, 503, 401/403/404 ; aucun code 3. Intervalles mesurés entre départs consécutifs : **n = 102, min 26,0 s, max 26,0 s**. Fournisseur final : `typesafe-ai` × 100, `digitalocean` × 3. Toutes les cibles atteintes (R et C : 5 réponses ; L et P : 3). 122 évaluations, 0 NON_PARSE.

Agrégat `aggregate.py` (médianes, règle d'E001) : [`results/agregat-2026-09-26T172726+0200/summary.md`](results/agregat-2026-09-26T172726+0200/summary.md). Analyse appel par appel : [`results/analyse.md`](results/analyse.md) (+ `analyse.json`).

### R — réplication (5 réponses par cas)

| cas | question | attendu | E005 | E006 (5 appels) | non conformes | répliqué |
|---|---|---|---|---|---|---|
| F1-04 « se sont lavées les mains » | correcte | false | 0.84 / 0.85 | 0.83–0.85, méd. 0.84 | 5/5 | **oui** |
| F1-05 « se sont parlés » | correcte | false | 0.80 | 0.83–0.87, méd. 0.84 | 5/5 | **oui** |
| F1-08 « qu'elle a faites faire » | correcte | false | 0.86 | 0.86–0.87, méd. 0.86 | 5/5 | **oui** |
| F3-02 « Ci-jointe la facture » | correcte | false (à confirmer, R004) | 0.86 | 0.83–0.86, méd. 0.85 | 5/5 | **oui** |
| F4-01 (T1-A + 3 distracteurs) | statut | contradiction | coherent 0.88 / 0.89 | coherent 0.85–0.92, méd. 0.91 | 5/5 | **oui** |
| F4-04 (A > F, 4 pas) | a_sup_f | true | 0.15 / 0.19 | 0.13–0.37, méd. 0.20 | 5/5 | **oui** (médiane pile au seuil) |

### P — paires minimales (forme correcte, 3 réponses)

| paire | P(correcte) forme **fautive** (méd.) | P(correcte) forme **correcte** (méd.) | écart |
|---|---|---|---|
| « se sont lavées » / « se sont lavé les mains » | 0.84 | 0.61 (0.58–0.64) | −0.23 |
| « se sont parlés » / « se sont parlé » | 0.84 | 0.90 (0.90–0.91) | +0.06 |
| « a faites faire » / « a fait faire » | 0.86 | 0.67 (0.64–0.75) | −0.19 |

### L — frontière en nombre de pas (3 réponses, sans R2)

| pas | 2 | 3 | 4 | 5 | 6 | 4 + `incompatible(A, F)` + R2 (R-F4-04) |
|---|---|---|---|---|---|---|
| P(true) médiane | 0.97 | 0.85 | 0.95 | 0.94 | 0.90 | **0.20** |
| conformes | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 0/5 |

### L — frontière en nombre de distracteurs (T1-A, 3 réponses ; 5 pour d = 3)

| distracteurs | 0 (T1-A) | 1 (+ A > C) | 2 (+ règle 3) | 3 (= F4-01) |
|---|---|---|---|---|
| choix `statut` | contradiction ×3 | coherent ×3 | coherent ×3 | coherent ×5 |
| P(contradiction) médiane | 0.73 | 0.34 | 0.14 | 0.08 |
| P(E > D) par appel | 0.60 / 0.59 / 0.61 | 0.21 / 0.18 / 0.16 | 0.39 / 0.40 / 0.45 | 0.53–0.68 |

### C — contamination (E004), 5 réponses par membre

| paire | moy. P avec | moy. P sans | écart (avec − sans) |
|---|---|---|---|
| C1 (1 pas, contradiction déduite après) | 0.97 | 0.98 | −0.006 |
| C2 (2 pas) | 0.97 | 0.97 | −0.002 |
| C3 (1 pas, contradiction directe) | 0.97 | 0.97 | +0.000 |
| C4 (2 pas, bloc avant) | 0.95 | 0.96 | −0.012 |

Écart par paire : moyenne −0.005, min −0.012, max +0.000 ; 3 négatifs, 1 nul. 40/40 conformes.

## Lecture

1. **Les 6 « faux et sûr » d'E005 se répliquent.**
   - [VÉRIFIÉ] 6/6 répliqués selon la règle préenregistrée : 30 appels, 30 non conformes. La dispersion par cas est faible : ≤ 0.04 sur les phrases, 0.07 sur F4-01. Sur F4-04, P va de 0.13 à 0.37 et la médiane (0.20) est exactement au seuil : 3 appels sur 5 seulement sont « faux et sûr ».
   - [VÉRIFIÉ] F1-05, qui était pile au seuil dans E005 (0.80), est ici entre 0.83 et 0.87.
   - [VÉRIFIÉ] F3-02 se réplique, mais son attente reste à confirmer par R004. Si R004 la déclare contestable, ce cas sort de la liste.
2. **Phrases : Jev préfère la forme fautive à la forme correcte, sur 2 paires sur 3.**
   - [VÉRIFIÉ] Sur « se sont lavé(es) les mains » et « a fait(es) faire », la forme correcte obtient une P(correcte) plus basse que la forme fautive (0.61 contre 0.84, et 0.67 contre 0.86). Sur « se sont parlé(s) », Jev juge les deux formes correctes (0.90 et 0.84) : il ne les distingue pas.
   - [HYPOTHÈSE] La forme accordée « a l'air » plus soignée. Jev noterait la plausibilité de surface, pas la règle d'accord. Ce n'est établi que sur 3 paires.
3. **La longueur de chaîne n'est pas la frontière.**
   - [VÉRIFIÉ] De 2 à 6 pas sans règle 2, P(true) reste entre 0.85 et 0.97 (15/15 conformes). Aucune pente monotone n'apparaît sur ces 5 points.
   - [VÉRIFIÉ] L-PAS4 et R-F4-04 ont les mêmes faits dans le même ordre : L-PAS4 obtient 0.95, R-F4-04 obtient 0.20. Retirer `incompatible(A, F)` et la règle 2 suffit à faire passer P de 0.20 à 0.95.
   - [HYPOTHÈSE] Dans F4-04, Jev ne « perd » pas la chaîne. Il lit la règle 2 (« ni A > F ») comme une réponse à la question « peut-on déduire A > F ? ». La contradiction portant sur les **variables de la question** l'emporte sur la déduction.
4. **Distracteurs : la détection de contradiction tombe dès le premier distracteur.**
   - [VÉRIFIÉ] Un seul fait redondant (A > C) fait passer le statut de `contradiction` (P 0.67–0.80) à `coherent` (3/3). P(contradiction) descend ensuite de façon monotone : 0.73, 0.34, 0.14, 0.08 pour 0, 1, 2 et 3 distracteurs.
   - [VÉRIFIÉ] Avec 1 distracteur, Jev nie aussi E > D (0.16–0.21, médiane 0.18). C'est un nouveau « faux et sûr » à la médiane (L-DIS1 `e_sup_d`, 3 appels), non préenregistré comme cible. P(E > D) ne varie pas de façon monotone avec le nombre de distracteurs (0.60, 0.18, 0.40, 0.60).
5. **Contamination (E004) : non observée sur un sous-graphe indépendant.**
   - [VÉRIFIÉ] Une contradiction dans un bloc de variables disjoint ne change pas P(true) sur la déduction : écart moyen −0.005, |écart| ≤ 0.012 sur 4 paires, 40/40 conformes. Cet écart est du même ordre que la dispersion entre appels d'un même cas (≤ 0.01 ici).
   - [HYPOTHÈSE] Le signal d'E001 (T1-A contre T1-B) et l'effondrement de F4-04 portent tous deux sur des **variables partagées** entre la contradiction et la question. La contamination, si elle existe, serait **locale** (variables communes) et non **globale** (« l'état est contradictoire »). E006 n'a pas testé ce cas par paire contrôlée.

**Attente que j'aurais eu envie de discuter après avoir vu Jev (non modifiée)** : pour R-F4-04 `a_sup_f` et L-DIS1 `e_sup_d`, on peut soutenir que « peut-on déduire A > F » est ambigu dans un ensemble contradictoire. La règle 2 interdit A > F, et la règle 1 l'impose. L'attente `true` est conservée : A > F découle de la règle 1 appliquée aux faits donnés. Mais la réponse de Jev a une lecture défendable, et cela affaiblit ces deux cas comme preuves d'une erreur de déduction.

## Limites

- 25 cas, 3 à 5 réponses par cas : **aucune conclusion générale**. Une paire minimale ne représente pas sa règle, et 5 points de chaîne ne font pas une courbe.
- Les réponses répétées sont très stables (souvent ±0.01) : 5 appels mesurent la **reproductibilité** de Jev sur une entrée, pas sa robustesse à la reformulation. Aucune paraphrase n'a été testée.
- L-PAS : un seul ordre de faits par longueur (graine = k ; ordre de F4-04 pour k = 4). L-DIS : une seule suite de distracteurs, emboîtés, qui mêle deux natures (fait redondant, règle non pertinente, fait de couleur).
- Les paires C testent seulement une contradiction **disjointe** de la question ; la contamination locale (variables partagées) n'est pas contrôlée par paire.
- F3-02 : attente en cours de doublage (R004).
- États en français ; les deux fournisseurs (`typesafe-ai` ×100, `digitalocean` ×3) ne sont pas distingués.
- Le rythme de 26 s a supprimé les 429 pendant cette fenêtre. [HYPOTHÈSE] Cela confirme la cause identifiée par M0008 (5 req/min par équipe), sans exclure une baisse de charge de la passerelle.

## Prochaine étape

1. **E004 bis (contamination locale)** : paires contrôlées où la contradiction porte sur les variables de la question et d'autres où elle ne les touche pas, en variant la **forme** de la règle 2, pour séparer « règle lue comme réponse » et « contamination ».
2. **Paraphrases** des 6 « faux et sûr » (autres verbes pour la même règle d'accord, autre formulation de consigne), pour savoir si l'erreur suit la règle ou la phrase.
3. **Distracteurs** : ne faire varier qu'une nature de distracteur à la fois (faits redondants seuls, règles non pertinentes seules), avec plusieurs ordres.
