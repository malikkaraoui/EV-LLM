# E009-bis — refaire A avec un budget où l'on apprend au moins la distribution

Mandat M0027 (2026-09-27), correctif de M0022/E009 (5 systèmes × 2 graines à 0 % **même dans la
distribution** → question non mesurée). Préenregistrement : `PREREGISTREMENT-bis.md`
(+ amendements B0 avant pilote, B1 avant runs officiels). Code E009/E008 réutilisé **par import**,
non modifié (`git diff 20f289b HEAD -- ../E009-procedure-apprise ../E008-addition` vide).

**En une phrase.** Avec curriculum de longueur, largeur 128 et 10 000 pas, **1 run sur 5 apprend
la distribution** (A3 Looped NoPE, graine 1, au pas 8 000) — et ce run **ne généralise pas** :
17 % à 6 chiffres, 0 % à 7, 8 et à toutes les longueurs de test (10–100) et adverses. Les 4 autres
runs (A1 × 2, A2-L × 1, A3 graine 2) **n'apprennent pas la distribution à ce budget**.

## Ce qui a changé par rapport à E009

| | E009 (M0022) | E009-bis |
|---|---|---|
| critère préalable | aucun | **T-ID ≥ 95 %** (2–5 chiffres) sinon pas d'évaluation hors distribution |
| budget | 2 000 pas fixes | adaptatif : arrêt dès T-ID ≥ 95 % (contrôle / 1 000 pas), **plafond 10 000** (20 000 préenregistrés, réduit par B1 pour tenir 5 h) |
| pédagogie | aucune | **curriculum** 1–2 chiffres → 1–5, niveau + 1 quand T-ID courant ≥ 90 % (contrôle / 500 pas) |
| largeur / lr | 64 / 1e-3 | **128 / 1e-3** (pilote graine 0 sur T-ID + VAL : C2 gagne pour les trois) |
| systèmes | A1, A2, A2-L, A3, A3-T | A1, A2-L, A3 (A3-T non lancé, budget) |

## Pas nécessaires pour T-ID ≥ 95 % (graines officielles)

| run | T-ID ≥ 95 % ? | pas | niveau de curriculum atteint (pas du passage) | T-ID 2/3/4/5 % (poids finaux) | exemples vus / **uniques** | calcul |
|---|---|---|---|---|---|---|
| A1 s1 | **jamais** | 10 000 (plafond) | 2 | 29 / 0 / 0 / 0 | 2 560 000 / **8 248** | 17 min |
| A1 s2 | **jamais** | 10 000 (plafond) | 3 (5 500) | 0 / 1,5 / 0 / 0 | 2 560 000 / 276 807 | 23 min |
| A2-L s1 | **jamais** | 10 000 (plafond) | 3 (3 500) | 42 / 100 / 0 / 0 | 2 560 000 / 341 179 | 53 min |
| A3 s1 | **oui** | **8 000** | 5 (4 500 ; 6 000 ; 7 000) | 99,5 / 100 / 99,5 / 88,0 (moy. 96,8) | 2 048 000 / 458 474 | 42 min |
| A3 s2 | **jamais** | 10 000 (plafond) | 4 (4 500 ; 7 500) | 97,5 / 92 / 26,5 / 0 | 2 560 000 / 539 372 | 54 min |
| A2-L s2, A3-T | non lancés (budget) | | | | | |

Remarques [VÉRIFIÉ] : A1 s1 est resté au niveau 2, où il n'existe que ≈ 10 000 paires distinctes :
8 248 paires uniques vues ≈ 310 fois chacune, et pourtant 29 % seulement à 2 chiffres. A1 s2 a
atteint 91 % au niveau 2 (pas 5 500) puis s'est **effondré à 0 %** (même à 2 chiffres) dès le
passage au niveau 3, sans remonter en 4 500 pas. A2-L s1 : 100 % à 3 chiffres mais 42 % à 2
chiffres, erreurs presque toutes sur le chiffre des dizaines (`81+16 → 07`), toutes « sûres ».

## Longueurs 6–100 (seul run ayant appris : A3 s1 ; exact-match %)

| VAL 6 | VAL 7 | VAL 8 | TEST 10 | 16 | 32 | 64 | 100 |
|---|---|---|---|---|---|---|---|
| **17,3** | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| B-REF (E008) : 91,2 | 7,9 | 0,1 | 0 | 0 | — | — | — |

Adverses (A3 s1) : ADV-RET (retenues en cascade, 10–100), ADV-ZERO (pleins de zéros), ADV-ASYM
(L + 1, L + 3, 1 + L, 3 + L pour L = 10…100) : **0,0 % partout** (30 jeux × longueurs ; 35 avec TEST).

Graines réussies (≥ 90 % à TEST 16) : **0**. Confirmation à 5 graines : **non déclenchée**
(VAL 8 = 0 % < 50 %). Aucun système « réussi ».

## Faux et sûr (confiance ≥ 0,8) et abstention (A3 s1)

- T-ID 5 : 20 faux sûrs / 24 faux ; VAL 6 : 105 / 248 (42 %) ; VAL 7 : 25 / 300 ; VAL 8 : 6 / 300.
- Test final + adverses : 33 faux sûrs / 3 015 faux ; **abstentions (pas de `$`) : 205 / 3 015
  faux** (6,8 %) — l'autodiagnostic est quasi absent : le système se trompe sans s'abstenir, avec
  une confiance basse sur les longs nombres. Itération retenue au test : médiane 150–413 aux
  longueurs ≥ 32, souvent le plafond 512 (l'arrêt par confiance ne se stabilise pas).
- Runs non appris : faux sûrs A2-L s1 T-ID 116/116 à L = 2 ; A3 s2 94/147 à L = 4.

## Budget de structure (ce qui est donné à la main)

| système | format | localité | itérations | traces | pédagogie |
|---|---|---|---|---|---|
| A1 Neural GPU | bande 2n, réponse inversée après `=` | conv k = 3 | **T = longueur de bande, donné** | aucune | curriculum 2→5 |
| A2-L Deep Thinking + Lipschitz | idem | conv k = 3 + normalisation spectrale | M = 24 à l'entraînement ; test : arrêt par confiance (≤ 512) | aucune | curriculum 2→5 |
| A3 Looped NoPE | idem | aucune (attention causale, sans position) | idem A2-L (**aucun T(n)**) | aucune | curriculum 2→5 |

Commun : longueur (n cases) et emplacement de la réponse donnés ; `$` appris ; aucun alignement,
aucun opérande inversé, aucun index de position.

## Validité [VÉRIFIÉ]

`resultats/controles*.json` : C-ORACLE 100 % sur les 43 jeux × longueurs ; C-PARCŒUR 0 % sur tous
les nouveaux jeux (tables : flux niveau 5 × 20 000 pas = 3 308 648 paires ; flux réel A3 s1 =
458 474 ; flux réel A2-L s1 = 341 179) ; contrôle positif T-ID1 = 100 %. Tests : `python -m
unittest test_e009bis` → 9 OK ; mutations tuées (niveau ignoré dans le lot, seuil d'arrêt strict).
Test final ouvert après le commit des runs (`cd619fb` < `919942c`), évalué une fois.

## Diagnostic hors protocole (après le test final, aucun choix) — `diagnostic_iterations.py`

T-ID avec un nombre d'itérations **fixe** t au lieu de l'arrêt par confiance :
- A2-L s1 : identique pour t = 8, 16, 24, 32 (L2 ≈ 50 %, L3 100 %, L4–5 0 %) → **le réseau ne sait
  pas** ; l'arrêt n'y est pour rien.
- A3 s1 : t = 24 donne T-ID 5 = 93,5 % (contre 88 % par confiance), VAL 6 = 17 % (pareil).
- A3 s2 : t = 24 donne T-ID 4 = 52 % (contre 26,5 % par confiance), T-ID 5 = 0 % → l'arrêt par
  confiance coûte des points dans la distribution, mais n'explique pas l'échec.

## Prédictions préenregistrées

- Q1 (≥ 1 système apprend la distribution, graine 1, ≤ 20 000 pas) : **confirmée** (A3 s1, 8 000
  pas, sous le plafond réduit de 10 000).
- Q2 (A1 apprend en moins de pas que A3) : **infirmée** (A1 n'apprend jamais).
- Q3 (aucun système appris ≥ 90 % à TEST 16) : **confirmée** (0 %).
- Question ouverte (VAL 8 > B-REF + 10 points) : **non** (0 %).

## Lecture

- [VÉRIFIÉ] **« N'apprend pas » (à 10 000 pas, curriculum, w = 128)** : A1 × 2 graines, A2-L × 1
  graine, A3 graine 2. Pour eux, la question de la généralisation reste **non mesurée**.
- [VÉRIFIÉ] **« Apprend mais ne généralise pas »** : A3 graine 1 seule. Dans la distribution
  96,8 % ; dès un chiffre de plus (6) : 17 % ; dès deux (7) : 0 % ; 0 % de 10 à 100 chiffres et
  sur tous les adverses. C'est **moins bien** que B-REF d'E008 (91 % à 6).
- [VÉRIFIÉ] L'apprentissage est instable d'une graine à l'autre : A3 1/2, A1 0/2 (dont un
  effondrement après passage de niveau). Aucune conclusion de système sur 2 graines.
- [HYPOTHÈSE] Le Looped NoPE sans position apprend une procédure liée aux longueurs vues (le
  « rang » d'une case se déduit du comptage causal, qui ne se transpose pas au-delà de 5), plutôt
  que la règle locale chiffre + chiffre + retenue.
- [HYPOTHÈSE] Pour les convolutions (A1, A2-L), la difficulté principale est l'**alignement non
  donné** : sur une bande plate, les chiffres de même rang de a et b sont à une distance qui
  dépend de la longueur de b ; les effondrements au changement de niveau (A1 s2) et l'erreur
  systématique sur les dizaines (A2-L s1) vont dans ce sens, sans le prouver.
- Ce que ça dit de l'hypothèse « règle / déclencheur / réflexe » : à ce budget, aucun biais
  d'architecture testé ne transforme la réussite dans la distribution en procédure générale ; le
  seul système qui apprend retient des réflexes liés à la longueur, pas la règle.

## Non testé (angles morts)

Plafond 20 000 pas (préenregistré, réduit pour le budget) ; A2-L graine 2, A3-T ; 3 graines de plus ;
largeur 256 ; continuer après T-ID ≥ 95 % (on s'arrête au premier contrôle réussi, par
préenregistrement) ; format standard ; alignement donné (hors mandat A).

## Calcul

Runs officiels 11 369 s ; pilote 1 590 s ; banc, contrôles, évaluations, diagnostic, tests
≈ 1 000 s → **≈ 3 h 52** (budget 5 h), GPU sans autre entraînement lourd.

## Fichiers

`curric.py` (flux + curriculum, fabrique), `entraine_bis.py`, `evalue_bis.py`, `verifie_bis.py`,
`synthese_bis.py`, `diagnostic_iterations.py`, `test_e009bis.py`, `hyperparametres_bis.json` ;
`resultats/` : `pilote.json`, `controles*.json`, `resultats.json`, `summary.md`,
`diagnostic_iterations.json`, `FINAL_OUVERT`. Les poids (`runs/`) ne sont pas versionnés.
