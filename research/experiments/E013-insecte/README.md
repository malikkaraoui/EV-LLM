# E013 — « insecte » : un accumulateur minuscule apprend-il l'addition à toute longueur ?

Mandat M0026, 2026-09-27, branche `exp/e013-insecte` (depuis `origin/exp/e008-addition` @
`af281f5`). Préenregistrement : [`PREREGISTREMENT.md`](PREREGISTREMENT.md) (commit `997d87f`,
poussé seul avant le code ; amendement A1 `c4b3755` : valeurs figées après pilote). Résultats
agrégés : [`resultats/`](resultats/). Code E008 réutilisé par import, **non modifié**.

## Idée

Les abeilles font de l'**intégration de trajet** avec un petit circuit : Stone et al. 2017,
*Current Biology* 27 : 3069–3085, doi:10.1016/j.cub.2017.08.052 [VÉRIFIÉ, extraits collés au
préenregistrement §0]. Principe testé ici (analogie [HYPOTHÈSE], pas celle des auteurs) : **un état
minuscule mis à jour localement à chaque pas**. Pour l'addition, cet état est la retenue.

## Systèmes et budget de structure (ce qui est donné à la main)

| système | ce qui est donné | ce qui est appris | paramètres |
|---|---|---|---|
| **I1** (H = 1, 2, 4, 8) | alignement des chiffres de même rang ; sens poids faible → fort ; nombre de pas = max(ℓa, ℓb) + 1 ; retrait d'un seul 0 de tête ; symbole « absent » ≠ 0 ; couche locale F = 32 partagée entre pas | la retenue, sa valeur, la table d'addition, où la stocker, qu'« absent » vaut 0 | 1 131 / 1 196 / 1 326 / 1 586 |
| **I2** (H = 8) | sens de sortie ; nombre de pas ; 2 têtes de lecture ; décalages locaux {−1, 0, +1} ; voisinage 3 pour les clés | où commencent les opérandes, qu'il faut reculer, quand s'arrêter sur l'opérande court | 1 922 |
| **I3** (I1, H = 4) | comme I1 + jeu d'entraînement fixe de N paires uniques | idem I1 | 1 326 |

État transmis d'un pas à l'autre : **H nombres** (I2 : + 2 pointeurs). Entropie croisée, Adam
lr 3e-3, **sans L2**, lot 128, 6 000 pas (I2 : 12 000), checkpoint choisi sur **VAL-OOD
(6–8 chiffres) seulement** ; TEST (10–1 000 chiffres + adverses) lu **une seule fois**.
5 graines officielles (1–5) par configuration ; graine 0 = pilote, exclue.

## Rejouer

```
PY=$HOME/.venvs/ev-llm-e008/bin/python      # mlx 0.29.3, numpy 2.0.2 (venv E008)
cd research/experiments/E013-insecte
export PYTHONDONTWRITEBYTECODE=1           # voir « Incident » plus bas
$PY -m unittest -v test_e013                # 12 tests
$PY controles13.py                          # C-ORACLE / C-PARCOEUR -> resultats/controles.json
$PY entraine.py --configs I1-H1 I1-H2 I1-H4 I1-H8 I3-N10 I3-N100 I3-N1000 I3-N10000 I2 \
    --graines 1 2 3 4 5                     # relancer tant que "BUDGET atteint" (<= 8,5 min)
$PY evalue.py --runs <config>-s<g> ...      # TEST, une seule fois par run
$PY analyse.py                              # resultats/resultats.json, summary.md
```

GPU MLX partagé, non reproductible au bit près : un rejeu donnera des chiffres très proches.

## Validité du test

| contrôle | attendu | obtenu |
|---|---|---|
| C-ORACLE (retenue codée à la main, E008) | 100 % partout | **100 %** sur 31 jeux × L (8 030 items, VAL + TEST) |
| C-PARCŒUR (591 106 paires distinctes vues par I1 graine 1) | ≤ 1 % | **0 %** partout |
| Contrôle positif d'architecture (`test_oracle_i1_par_construction`) | un I1 H = 1 à poids écrits à la main passe à 1 000 chiffres | passe ; tué si on coupe la retenue (mutant) |

**Verdict : TEST VALIDE** [VÉRIFIÉ] (`resultats/controles.json`, commité avant la lecture de tout
modèle appris).

## Résultats — exact-match (%) moyenne ± écart sur 5 graines

| config | exemples uniques vus | graines ≥ 90 % à 16 | T-ID 5 | L = 10 | 16 | 32 | 64 | 100 | **1 000** |
|---|---|---|---|---|---|---|---|---|---|
| I1 H = 1 | ≈ 591 000 | **5/5** | 100 | 100 | 100 | 100 | 100,0 ± 0,1 | 100 | 99,3 ± 0,6 |
| I1 H = 2 | ≈ 591 000 | **5/5** | 100 | 100 | 100 | 100 | 100 | 100 | **100** |
| I1 H = 4 | ≈ 591 000 | **5/5** | 100 | 100 | 100 | 100 | 100 | 100 | **100** |
| I1 H = 8 | ≈ 591 000 | **5/5** | 100 | 100 | 100 | 100 | 100 | 100 | **100** |
| I2 (entrée plate) | ≈ 1 120 000 | **0/5** | 60,2 ± 48,7 | 53,5 ± 44,5 | 27,8 ± 32,3 | 2,2 ± 4,4 | 0,0 | 0,0 | 0,0 |
| I3 N = 10 | 10 | 0/5 | 0,0 | 0 | 0 | 0 | 0 | 0 | 0 |
| I3 N = 100 | 100 | 0/5 | 0,4 ± 0,3 | 0 | 0 | 0 | 0 | 0 | 0 |
| I3 N = 1 000 | 1 000 | **5/5** | 100 | 100 | 100 | 100,0 ± 0,1 | 99,9 ± 0,2 | 99,9 ± 0,1 | 98,6 ± 1,6 |
| I3 N = 10 000 | 10 000 | **5/5** | 100 | 100 | 100 | 100 | 100 | 100 | **100** |

T-LONG : 500 paires par L (200 à L = 1 000), les deux opérandes de L chiffres. Par graine et
T-ID 2–5 : [`resultats/summary.md`](resultats/summary.md). Référence E008 sur la même question :
transformer ~3,2 M paramètres, 3 M exemples : **0 %** dès 6 chiffres (B-STD), 0 % dès 8 (B-REF).

**Adverses** (exact-match moyen %, L = 10 / 16 / 32 / 64 / 100 / 1 000) :

| config | ADV-CASCADE (99…9 + 1, retenue partout) | ADV-ZEROS (10…02 + 10…03, creux) | ADV-ASYM (L chiffres + 1–5 chiffres) |
|---|---|---|---|
| I1 H = 1 | 100 partout | **91,7 / 85,1 / 83,0 / 77,2 / 74,5 / 45,5** | 100 / 100 / 99,8 / 99,8 / 99,8 / 99,8 |
| I1 H = 2, 4, 8 | 100 partout | 100 partout | 100 partout |
| I2 | 53,4 / 29,3 / 3,5 / 0,8 / 0,6 / 0,4 | 58,4 / 53,7 / 22,8 / 10,7 / 0,6 / 0,0 | 48,9 / 25,3 / 10,5 / 10,7 / 8,1 / 0,0 |
| I3 N = 1 000 | 100 / 100 / 99,6 / 98,6 / 99,0 / 91,5 | 100 partout | 100 / 99,8 / 99,8 / 100 / 99,8 / 97,8 |
| I3 N = 10 000 | 100 partout | 100 partout | 100 partout |

**Autodiagnostic** (5 graines cumulées ; confiance = produit des probabilités des chiffres
émis ; « faux et sûr » = faux avec confiance ≥ 0,8 ; **aucun système ne s'abstient** : pas de
mécanisme d'abstention, taux 0 par construction) :

| config, jeu | faux / items | faux et sûrs | confiance médiane justes / faux |
|---|---|---|---|
| I1 H = 2, 4, 8 — tous jeux TEST longs | 0 / 22 650 par taille | 0 | 0,92–0,9996 / — |
| I1 H = 1, ADV-CASCADE | 0 / 3 090 | 0 | 0,90 / — |
| I1 H = 1, ADV-ZEROS | 722 / 3 030 | **204 (28 %)** | 0,995 / 0,53 |
| I1 H = 1, T-LONG | 8 / 13 500 | 0 | 0,96 / 0,25 |
| I3 N = 1 000, ADV-CASCADE | 58 / 3 090 | 0 | 0,82 / 0,013 |
| I2, T-LONG | 11 411 / 13 500 | 108 (0,9 %) | 0,95 / 0,003 |

Durées (M1, GPU partagé avec d'autres fenêtres) : I1 50–85 s par run, I3 21–34 s, I2
230–269 s ; entraînement total pilote compris **3 909 s ≈ 65 min**, évaluations ≈ 3 min.

## Inspection du circuit (T-LONG L = 100, graines réussies)

Corrélation de chaque unité de hₜ avec la vraie retenue sortante du pas t
(`resultats/resultats.json`, clé `circuit`) :

- **Une unité porte la retenue** dans les 30 runs réussis inspectés : |corrélation| 0,974–0,992
  (H = 1), 0,9987–0,9997 (H = 2), 0,998–0,9998 (H = 4), 0,995–0,9992 (H = 8). Le signe et
  l'indice de l'unité varient d'une graine à l'autre (ex. H = 4 : unité 3, 3, 3, 2, 0).
- **Marge de séparation** (écart minimal entre les valeurs « retenue 1 » et « retenue 0 » de
  l'unité porteuse, sur tous les pas) : 0,38–0,63 pour H = 1, 1,10–1,75 pour H = 2, 1,34–1,78 pour
  H = 4. Deux runs I3 réussis ont une marge **négative** (N = 1 000 s5 : −0,12 ; N = 10 000 s2 :
  −0,18) : la retenue n'y est pas séparable par une seule unité, une autre unité y contribue.
- **Pourquoi H = 1 casse sur les nombres creux** [VÉRIFIÉ, `derive_h1`] : après (1,1) puis
  k paires (0, 0) sans retenue, l'état unique **dérive** au lieu de rester fixe, à l'opposé de
  la valeur « retenue », vers une zone jamais visitée à l'entraînement. Graine 1 (retenue ≈ −1,0) :
  0,10 → 0,50 (k = 5) → 0,70 (k ≥ 20) ; graine 2 (retenue ≈ +0,98) : −0,05 → −0,92 (k = 10) ;
  graine 3 : 0,10 → 0,75. Graines 4 et 5 : se stabilisent à −0,14 / −0,26, près de leur zone
  apprise → **0 erreur** sur ADV-ZEROS. Dans la zone dérivée, la couche locale lit mal la paire
  suivante : les erreurs (sonde ponctuelle sur L = 10–64, non scriptée) surviennent après une médiane de
  5–10 paires (0, 0) consécutives, sur la paire suivante (le plus souvent le « 1 + 1 » de tête).
  L'entraînement (≤ 5 chiffres) ne montre jamais plus de 4 paires (0, 0) d'affilée : l'état
  « pas de retenue » n'y est jamais forcé à être un **point fixe**. Avec H ≥ 2, 0 erreur.

## Prédictions préenregistrées

- **P1** (au moins une taille de I1 réussie) : **confirmée** — les 4 tailles, 5/5 graines.
- **P2** (H = 1 réussi sur ≥ 3/5) : **confirmée** — 5/5 à L = 16 (et 100 %).
- **P3** (toute graine I1 réussie reste ≥ 90 % à 1 000) : **confirmée** — minimum 98,5 %
  (H = 1 s3) ; 15/15 graines H = 2, 4, 8 à 100 %.
- **P4** (I2 ≤ 1/5) : **confirmée** — 0/5 ; meilleure graine 83 % à 16, 0 % dès 64.
- **P5** (I3 : N = 10 → 0/5, N = 10 000 → ≥ 4/5) : **confirmée** — 0/5 et 5/5 ; seuil
  **entre 100 et 1 000 exemples uniques** (N = 100 : 0/5 ; N = 1 000 : 5/5).
- **P6** (confiance médiane des erreurs < celle des réussites sur ADV-CASCADE) : **non
  mesurable pour I1** (0 erreur sur 3 090 × 4 tailles) ; mesurable sur I3 N = 1 000 (0,013 contre
  0,82) et I2 (0,003 contre 0,92) : **confirmée** là.

## Lecture

- [VÉRIFIÉ] Un réseau de **1 131 paramètres** dont l'état transmis est **un seul nombre**
  apprend, sur des additions de 1 à 5 chiffres, une règle **exacte à 16, 32, 64, 100 chiffres**
  (5/5 graines, 100 %) et à 99,3 % à 1 000 chiffres. Avec **deux** nombres d'état : **100 % à
  1 000 chiffres**, 5/5 graines, sur tous les adverses (retenue en cascade sur 1 000 chiffres,
  nombres creux, 1 000 + 3 chiffres). E008 : un transformer ~2 800 fois plus gros tombait à 0 % dès
  6 chiffres. Dans ce format et cette tâche, **la forme de la machine** compte plus que sa taille.
- [VÉRIFIÉ] Il suffit de **1 000 exemples uniques** (vus en boucle) pour la règle à 100 chiffres
  (5/5, ≥ 99,8 %) ; 100 ne suffisent pas (0/5, et même 0,4 % dans la distribution à 5 chiffres :
  pas d'apprentissage par cœur utile non plus). 10 000 → 100 % à 1 000 chiffres.
- [VÉRIFIÉ] **Le prix de l'alignement donné** : sans lui (I2, même accumulateur, lecture apprise,
  un peu plus de paramètres, 2 × plus de pas), 0/5 graine ; une graine atteint 83 % à 16 chiffres
  mais **toutes** sont à 0 % dès 64. La lecture douce (pointeurs flous) se dégrade avec la
  longueur ; la retenue, elle, n'est pas le problème. [HYPOTHÈSE] la dérive vient du flou
  accumulé des pointeurs (affûtage appris insuffisant) — non mesuré ici.
- [VÉRIFIÉ] **Sait-il quand il ne sait pas ?** Partiellement. Là où il se trompe, sa confiance
  baisse souvent (médianes 0,003–0,53 contre 0,82–0,995), mais pas toujours : I1 H = 1 fait
  **28 % de faux et sûrs** sur les nombres creux — précisément le cas où son état a dérivé sans
  qu'il le « sente ». Aucun système n'a de voie d'abstention.
- [VÉRIFIÉ] **L'état minimal a un défaut invisible dans la distribution** : H = 1 est à 100 % sur
  T-ID, VAL et T-LONG ≤ 100, et casse sur 3/5 graines dès qu'on enchaîne des (0, 0) — car rien
  dans les données courtes n'oblige « pas de retenue » à être un point fixe. Un deuxième nombre
  d'état a suffi à le rendre robuste ici (0 erreur sur 15 graines).
- **« Avec un rien faire beaucoup »** : oui, **si le rien est bien placé**. Ce qui a été donné
  à la main — l'alignement, le sens, le nombre de pas — est exactement ce qui manquait au
  transformer d'E008 ; la partie apprise (la retenue et la table) est petite et s'apprend avec
  ~10³ exemples. Le résultat mesure donc surtout la **valeur de la structure donnée**, pas une
  capacité à découvrir la procédure seul (I2 montre que la découverte de l'alignement, elle,
  n'est pas acquise).
- Aucune conclusion au-delà de : addition d'entiers positifs, ces tailles, ces budgets, ces
  formats.

## Limites

- Une seule tâche, un seul format de sortie (poids faible d'abord), nombre de pas donné.
- I2 : une seule architecture de lecture, un seul réglage (lr choisi au pilote, pas 2 × I1) ;
  son échec ne prouve pas qu'un lecteur appris ne peut pas aligner.
- I3 : seuls 4 N testés ; le seuil exact entre 100 et 1 000 n'est pas mesuré.
- Confiance = produit sur jusqu'à 1 001 chiffres : elle décroît mécaniquement avec la longueur
  (d'où « faux et sûr » rare aux grandes L) ; la p_min par pas est rapportée dans
  `resultats.json` (`autodiag`).
- Le pilote (graine 0) a vu VAL-OOD pour 4 réglages ; le TEST n'a été lu qu'une fois par run.

## Incident de méthode (transverse)

Pendant la vérification par mutation des tests, un mutant de **même taille** que l'original,
restauré **dans la même seconde**, a laissé un bytecode obsolète : le Python système macOS range
ses `.pyc` dans `~/Library/Caches/com.apple.python/…` (pas dans `__pycache__/`), et l'invalidation
se fait sur (mtime à la seconde, taille). Le test « restauré » exécutait le mutant et échouait.
Parade : `PYTHONDONTWRITEBYTECODE=1` pour toute série de mutations (et pour les runs).
