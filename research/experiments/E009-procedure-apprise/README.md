# E009 « A » — la procédure apprise par l'architecture seule

Mandat M0022, 2026-09-27, branche `exp/e009-procedure-apprise` (depuis `origin/exp/e008-addition`
@ `af281f5`). Préenregistrement : [`PREREGISTREMENT.md`](PREREGISTREMENT.md) (amendement A1 :
S = 2 000 pas, largeur 64, figés après le pilote). Résultats agrégés : [`resultats/`](resultats/).

**En une phrase.** Avec ce budget (2 000 pas × 256 = 512 000 exemples, ~50–110 k paramètres,
M1 partagé), **aucune** des cinq architectures n'apprend l'addition, **même dans la
distribution** : 0 % en validation 6–8, 0 % au test final 10–100 et sur les adverses, et
T-ID 2–5 ≤ 3 %. L'expérience **ne répond pas** à la question « l'architecture suffit-elle pour
généraliser en longueur ? » : elle montre seulement que, sous ce budget, ces biais
n'apprennent même pas la tâche. [VÉRIFIÉ]

## Protocole (résumé)

- Entrée : la séquence plate d'E008 `a+b=` (aucune grille alignée, aucun index de position,
  opérandes non inversés), suivie de n cases réponse (bande de 2n). Réponse lue d'un coup dans
  les cases, format **inversé** (poids faible d'abord). Flux d'entraînement, exclusions,
  évaluateur unique, oracle : **importés d'E008** sans modification.
- Systèmes : A1 Neural GPU (CGRU, T = 2n), A2 Deep Thinking (recall + perte progressive,
  M = 24), A2-L (A2 + normalisation spectrale, ELU), A3 Looped Transformer NoPE (arrêt par
  confiance maximale, **sans T(n)**), A3-T (idem **avec T(n) = max(ℓa, ℓb) + 1 donné**,
  « structure injectée »). Au test, A2/A2-L/A3 : plafond fixe 512 itérations, sortie de
  l'itération de confiance maximale.
- Validation (seule pour choisir) : VAL 6, 7, 8 (300 / L). Test final intouché : 10, 16, 32,
  64, 100 (200 / L), + ADV-RET (retenue à chaque position + `99…9+1`), ADV-ZERO (`10…02 + 10…03`
  et nombres creux), ADV-ASYM (L chiffres + 1 ou 3 chiffres, deux ordres). Évalué **une seule
  fois**, après le commit du criblage (`870f23d`).
- Graines 1 et 2 (criblage) ; graine 0 = pilote exclu.

## Rejouer

```
PY=$HOME/.venvs/ev-llm-e008/bin/python          # venv d'E008 (mlx 0.29.3), rien d'ajouté
cd research/experiments/E009-procedure-apprise
$PY -m unittest -v test_e009                    # 17 tests
$PY verifie.py                                  # C-ORACLE / C-PARCŒUR -> resultats/controles.json
for s in A1 A2 A2-L A3 A3-T; do for g in 1 2; do
  $PY entraine.py --systeme $s --graine $g      # relancer tant que "fini": false (<= 8,5 min)
  $PY evalue.py --systeme $s --graine $g --phase val
done; done
date > resultats/FINAL_OUVERT                   # ouvre le test final (une fois par run)
for s in A1 A2 A2-L A3 A3-T; do for g in 1 2; do $PY evalue.py --systeme $s --graine $g --phase final; done; done
$PY synthese.py                                 # resultats/resultats.json, summary.md, courbe.csv
```

## Validité du test [VÉRIFIÉ] (`resultats/controles.json`, commit `8f6977e`)

| contrôle | attendu | obtenu |
|---|---|---|
| C-ORACLE | 100 % partout | **100 %** sur les 43 jeux × longueurs (VAL, TEST, ADV-*, T-ID, T-ID1) |
| C-PARCŒUR (405 818 paires distinctes, graine 1, 2 000 pas) | ≤ 1 % | **0 %** partout ; **100 %** sur T-ID1 (contrôle positif) |
| C-BANDE (tests) | cible exacte → 100 %, décalée d'une case → ≈ 0 % | vérifié (`test_e009`), et 5 mutations du code tuées par une assertion nommée |

**Verdict : TEST VALIDE.** Le pipeline apprend quand la tâche est apprenable : A3-T sur-apprend
un lot de 64 exemples à 100 % en 300 pas (contrôle de sanité, hors protocole).

## Résultats (exact-match %, graines 1 et 2)

| système | params | T-ID 2 / 3 / 4 / 5 | VAL 6 / 7 / 8 | TEST 10 / 16 / 32 / 64 / 100 | ADV-RET / ZERO / ASYM | graines réussies (≥ 90 % à 16) | perte finale (par case) |
|---|---|---|---|---|---|---|---|
| A1 Neural GPU | 76 047 | 0 / 0 / 0 / 0 | 0 / 0 / 0 | 0 partout | 0 / 0 / 0 | 0 / 2 | 1,28 / 1,27 |
| A2 Deep Thinking | 107 343 | 1,0 / 0,3 / 0 / 0 | 0 / 0 / 0 | 0 partout | 0 / 0 / 0 | 0 / 2 | 1,00 / 0,94 |
| A2-L (+ Lipschitz) | 107 343 | 1,5 / 0 / 0 / 0 | 0 / 0 / 0 | 0 partout | 0 / 0 / 0 | 0 / 2 | 1,06 / 0,95 |
| A3 Looped NoPE, sans T(n) | 51 791 | 0 / 0 / 0 / 0 | 0 / 0 / 0 | 0 partout | 0 / 0 / 0 | 0 / 2 | 1,16 / 1,09 |
| A3-T (T(n) donné) | 51 791 | 1,3 / 0,3 / 0,3 / 0 | 0 / 0 / 0 | 0 partout | 0 / 0 / 0 | 0 / 2 | 0,82 / 0,80 |
| B-STD (E008, 3,2 M, 3,1 M ex.) | — | 100 / 99,5 / 98,8 / 98,4 | 0 / 0 / 0 | 0 (10, 12, 16) | — | — | — |
| B-REF (E008) | — | 100 / 100 / 100 / 100 | 91,2 / 7,9 / 0,1 | 0 (10, 12, 16) | — | — | — |

B-STD/B-REF : chiffres E008 recopiés (autres jeux de mêmes longueurs, 12 000 pas, 6× plus
d'exemples, 30–60× plus de paramètres) — la comparaison n'est **pas** à budget égal.

**Diagnostic (VAL + T-ID, `resultats/resultats.json` → `diagnostic`)** : chiffre de poids
faible juste dans 1–14 % des cas (hasard ≈ 10 %), chiffres justes 0–34 %. Seul A3-T produit
presque toujours une réponse de la **bonne longueur** (T-ID 87–95 %, VAL 8 : 66–74 %) : il a
appris la longueur de la somme, pas les chiffres. A1, A2, A2-L, A3 : bonne longueur 0–90 %
selon la longueur et la graine, sans régularité.

**« Faux et sûr »** (confiance ≥ 0,8 parmi les faux) : **0** pour A2, A2-L, A3, A3-T sur tous
les jeux ; **A1 : 29 % au test final** (1 745 / 6 030, 0 en VAL). **Non-réponses** (pas de `$`)
parmi les faux au test final : A1 1 758, A2 1 793, A2-L 183, A3 4 594, A3-T 1 467 (sur 6 030).
Aucun système ne s'abstient au sens fort ; la non-réponse est un échec de format.

**Arrêt appris** (itération retenue, médiane, graine 1, test final) : A2-L s'arrête à 1–2
itérations quelle que soit la longueur (la confiance ne croît pas avec le calcul) ; A2 et A3
choisissent des itérations croissantes mais erratiques (A3 : 2 → 51) ; le plafond 512 n'est
jamais la règle.

**Prédictions préenregistrées** : P1 (≥ 95 % sur T-ID) **infirmée** pour les 5 systèmes ;
P2 (A3-T ≥ 50 % à VAL 8) **infirmée** ; P3 (A3 < A3-T à VAL 8) **infirmée** (égalité à 0) ;
P4 (A1 < 50 % à VAL 8) **confirmée**, trivialement ; P5 (A2-L ≥ A2) **confirmée**,
trivialement (0 = 0). Question ouverte (dépasser B-REF de 10 points à 8) : **non**.

Déroulé : aucun système ≥ 50 % à VAL 8 → **aucune confirmation à 5 graines** ; la règle de
choix du « meilleur système » (VAL 8, puis 7, puis 6) ne départage pas des 0 → **format
standard non entraîné** et courbe d'efficacité du « meilleur » sans objet (les courbes de
tous les runs, en exemples uniques, sont dans `resultats/courbe.csv` : 0 à tous les jalons ;
405 818 exemples uniques sur 512 000 vus, graine 1).

Calcul : entraînements officiels 7 391 s (A1 582 / 593, A2 707 / 674, A2-L 904 / 884, A3 1 233
/ 1 276, A3-T 261 / 277 s) ; évaluations finales 2 214 s ; pilotes, bancs, tests ≈ 25 min.
Total ≈ **3 h 05** (budget 4 h), GPU partagé avec d'autres fenêtres.

## Budget de structure

| système | donné à la main |
|---|---|
| tous | bande de n cases réponse juste après `=` (emplacement et longueur max de la réponse) ; fin `$` apprise ; aucun alignement, aucun index, opérandes non inversés |
| A1 | localité (convolution k = 3) ; **T = 2n itérations** (calcul proportionnel à la taille) |
| A2 / A2-L | localité ; M = 24 fixe à l'entraînement ; au test ≤ 512, arrêt par confiance (appris) ; A2-L : contrainte de Lipschitz |
| A3 | rien de local ; attention causale NoPE ; M = 24 ; arrêt par confiance |
| A3-T | idem A3 + **T(n) = max(ℓa, ℓb) + 1 donné** à l'entraînement et au test |

## Lecture

- [VÉRIFIÉ] Le test est juste (oracle 100 %, par-cœur 0 %) et le pipeline peut apprendre
  (sur-apprentissage d'un lot). Les 0 % ne viennent pas d'un défaut de mesure détecté.
- [VÉRIFIÉ] Sous ce budget, **aucun** biais d'architecture testé ne suffit à apprendre
  l'addition *dans* la distribution ; la question de la généralisation en longueur n'est
  donc **pas testée** ici. Il serait faux de lire ce résultat comme « l'architecture ne
  suffit pas ».
- [VÉRIFIÉ] Même la version « structure injectée » (A3-T), la plus proche de la littérature
  qui annonce ≈ 100 %, n'apprend que la **longueur** de la réponse. C'est l'indice le plus net
  que le budget (et non le seul biais) est en cause.
- [HYPOTHÈSE] Causes plausibles, non départagées : (1) budget 6× inférieur à E008 et très
  inférieur à la littérature (Deep Thinking, Looped Transformer entraînent 10⁵–10⁶ pas) ;
  (2) largeur 64 ; (3) lecture non autorégressive : la case j doit « savoir » qu'elle est la
  j-ième sans position — en NoPE causal, cela exige de compter, ce qu'E008 (autorégressif)
  n'exigeait pas ; (4) entraînabilité des récurrences profondes : A2 ne sur-apprend pas
  64 exemples en 300 pas (perte 1,2), là où A3-T y arrive.
- [VÉRIFIÉ] Les modèles A2–A3 ne sont **jamais sûrs** de leurs erreurs (0 faux et sûr) :
  cohérent avec des modèles qui n'ont rien appris ; A1 est sûr de 29 % de ses erreurs au test
  long — la confiance d'un modèle qui n'a rien appris n'est donc pas un signal fiable.

## Ce que ça dit de l'hypothèse règle / déclencheur / réflexe

Rien de positif. [HYPOTHÈSE] Si la « règle » (la procédure de retenue) doit s'installer par la
seule architecture, ce palier indique qu'elle **ne s'installe pas à petit budget** : les
biais « calcul proportionnel à la taille » (A1) et « arrêt appris » (A2, A3) ne suffisent pas
à faire émerger un réflexe chiffre par chiffre sans un volume d'exemples bien supérieur. La
piste B (donner explicitement la trace ou l'alignement, avec budget de structure déclaré)
reste la plus directe à ce budget ; A n'est **pas réfutée**, elle est **non mesurée**.

## Limites et écarts

- Budget réduit par amendement A1 (S = 2 000, largeur 64) : le résultat est conditionnel à
  ce budget. Une seule valeur d'hyperparamètres, aucune recherche sur VAL (VAL = 0 ne
  discrimine rien).
- A2-L est une **approximation** de 2410.23451 (normalisation spectrale + ELU). A1 sans les
  astuces du Neural GPU original (curriculum, bruit, relaxation).
- Format standard **non testé** (règle de choix non départagée) ; confirmation à 5 graines
  **non déclenchée**.
- GPU MLX non déterministe au bit (tests à 1e-3, contrôle négatif autre graine > 1e-2).

## Envie de modifier le préenregistrement (écrite, non appliquée)

Après le premier run officiel (A3-T graine 1 : T-ID 0 %), j'aurais voulu : (1) un critère
préalable « apprend T-ID ≥ 95 % » avant toute lecture de généralisation, avec budget de pas
adaptatif jusqu'à ce critère ; (2) un pilote qui vérifie l'apprentissage *dans* la
distribution et pas seulement la vitesse ; (3) lr et largeur réglés sur VAL/T-ID pour chaque
famille. Non appliqué : c'eût été modifier le protocole après un résultat officiel (§ 9).
