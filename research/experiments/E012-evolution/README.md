# E012 — évolution + MDL : découvrir le circuit de l'addition

Mandat M0025 (F03), 2026-09-27, branche `exp/e012-evolution` (depuis `exp/e011-objectif-mdl` @ `994c77b`).
Préenregistrement : [`PREREGISTREMENT.md`](PREREGISTREMENT.md) (commit `092979f`, poussé seul avant le code).
Sans API, **CPU seulement** (numpy + `multiprocessing`, 5 processus = 5 graines), ~204 min de calcul
mur au total (pilote compris), sous le plafond de 4 h. Évaluateur **E008** importé tel quel ; codage
MDL des poids d'**E011** (`bits_entier`, `bits_poids`) et jeux binaires d'E011 importés.

## Réponse courte

Une recherche évolutive MDL **réduite** (~1–19 M enfants par graine, soit ≲ 0,6 % du budget de Lan
et al. 2022) :

- **Binaire (format de Lan, 100 exemples)** : **0/5** [VÉRIFIÉ]. Les 5 graines finissent dans le même
  piège : un réseau sans unité cachée qui **hésite** (`sortie = carré(affine(a, b))`, probabilités
  fractionnaires), MDL ≈ 355 bits, alors que le circuit exact en coûte **102** (1 cachée) ou 104.
- **Décimal aligné, 100 exemples** : **2/5** graines trouvent un circuit exact **prouvé** pour toute
  longueur [VÉRIFIÉ].
- **Décimal aligné, 1 000 exemples** : **4/5** graines exactes jusqu'à 1 000 chiffres et sur tous les
  adverses (2 prouvées, 2 exactes au test mais non prouvables car elles utilisent sigmoïde) [VÉRIFIÉ].
- **Format plat d'E008** : **0/5**, 0 % partout, même en validation 6–8 chiffres [VÉRIFIÉ] — attendu, et
  **structurellement** attendu (voir Lecture 4).

Le plus court circuit trouvé (X2-1000, graine 5 ; même forme à X2-100 graine 3) **est** l'algorithme
d'école, avec une seule unité cachée qui est la retenue :

```
h1     = marche(a + b + h1(t−1) − 9)            # 1 ssi a + b + retenue ≥ 10 : la RETENUE
sortie = id(a + b + h1(t−1) − 10·h1)            # (a + b + retenue) mod 10
```

Vérifié à la main (table des 200 cas a, b ∈ 0..9, c ∈ {0, 1}) et par la preuve mécanique (automate
produit en rationnels exacts, 20 états, 2 000 transitions) [VÉRIFIÉ]. Tout cela : **5 graines par
condition, un seul algorithme, un budget** ; aucune conclusion générale.

## Tableau principal (test final unique ; détail : [`resultats/summary.md`](resultats/summary.md))

| format | exemples (uniques) | graines exactes (tout test + adverses) | ≥ 90 % à 16 | preuve toute longueur | évaluations jusqu'à la découverte¹ | taille des circuits exacts (cachées / connexions / biais) | \|G\| des circuits exacts (bits) |
|---|---|---|---|---|---|---|---|
| X1 binaire aligné (Lan) | 100 | **0/5** | 0 | — | — | — (rendu : 0 / 2 / 1, MDL 355) | — |
| X2 décimal aligné | 100 | **2/5** | 2 | 2/2 | 0,48 M ; 2,97 M | 2/8/0 ; **1/7/0** | 144 ; 116 |
| X2 décimal aligné | 1 000 | **4/5** | 4 | 2/4 (2 non prouvables : sigmoïde) | 0,21 M ; 0,51 M ; 0,54 M ; 1,12 M | **1/7/1** ; 2/9/2 ; 4/12/3 ; 5/13/0 | 117 ; 176 ; 239 ; 244 |
| X3 décimal plat (E008) | 100 | **0/5** | 0 | sans objet | — | — | — |

¹ Réseaux distincts évalués (cache exclu) jusqu'au premier suivi où le MDL-minimal est exact en
entraînement **et** en validation 6–8 (seul usage de la validation). Circuit construit à la main
(C-ORACLE-CIRCUIT) : 2 / 6 / 0, 104 bits (binaire), 112 bits (décimal).

Exact-match moyen ± écart sur 5 graines, T-OOD : X2-100 **40,0 ± 49,0 %** à 16, 32, 64, 100, 1 000
chiffres (= 2 graines à 100 %, 3 à 0 %) ; X2-1000 **80,0 ± 40,0 %** (4 à 100 %, 1 à 0 %) ; X1 et X3
**0 %** partout.

Budget consommé par graine : X1 12 000 générations = 19,2 M enfants, ~9,7 M évaluations, 55 min ;
X2-100 jusqu'à 3 764 gén. (6,0 M enfants) ; X2-1000 jusqu'à 1 683 gén. ; X3 108–229 gén. (0,17–0,37 M
enfants, 45 min). Arrêts : budget de générations (X1), plafond mur de 45 min ou arrêt anticipé
préenregistré (exact train + val, MDL stable 300 générations).

## Validité du test (`resultats/controles.json`)

| contrôle | attendu | obtenu |
|---|---|---|
| C-ORACLE-ALGO (addition chiffre à chiffre sur listes, sans `a + b`), base 2 et 10 | 100 % | **100 %** sur tous les jeux × longueurs |
| C-ORACLE-CIRCUIT (circuit à la main, **même** code d'exécution, même évaluateur), base 2 et 10 | 100 % | **100 %** partout, jusqu'à 1 000 chiffres ; prouvé (4 et 20 états) |
| C-PARCŒUR (table des paires d'entraînement, graine 1), X1, X2, X3 | 0 % | **0 %** partout ; 100 % sur ses propres paires (contrôle positif) |

**TEST VALIDE** [VÉRIFIÉ]. Contrôle négatif implicite : les réseaux rendus faux sont bien comptés faux
(la preuve mécanique donne un contre-exemple pour chacun des 9 réseaux faux alignés).

Faux et sûr (confiance ≥ 0,8) : les réseaux **faux** du décimal sont **sûrs d'eux** (1 500 faux sûrs
sur 1 500 à 16 chiffres pour les 3 graines X2-100 ratées) : `floor` donne des sorties entières, donc
une probabilité 1 sur un chiffre faux [VÉRIFIÉ]. X1 et X3 : 0 faux sûr (ils hésitent). Pas
d'abstention (sans objet).

## Circuits trouvés (tous : [`resultats/circuits.md`](resultats/circuits.md))

- **X2-100 graine 3** (1 cachée, 7 connexions, 116 bits, prouvé) :
  `h1 = floor(a/10 + b/10 + h1(t−1)/6)` ; `sortie = relu(a + b − 10·h1 + h1(t−1))`.
  La retenue est bien `h1` : avec c = 1, `floor((a+b)/10 + 1/6)` = 1 ssi a + b ≥ 9 (8,33 arrondi au
  supérieur) ; avec c = 0, ssi a + b ≥ 10. Le poids **1/6 au lieu de 1/10** est équivalent sur les
  200 cas (vérifié) : la recherche trouve une variante, pas la formule de manuel.
- **X2-1000 graine 5** : le circuit d'école ci-dessus (marche, biais −9).
- **X2-1000 graine 3** (prouvé, 111 états) : une retenue codée sur deux unités `floor` couplées.
- **X2-1000 graines 1 et 2** : exacts jusqu'à 1 000 chiffres, mais avec des sigmoïdes (non
  prouvables en rationnels) ; plus longs (239–244 bits).
- **Échecs décimaux** (X2-100 ×3, X2-1000 ×1) : tous le même piège `sortie = floor(a + b + sortie(t−1)/10)`
  — juste tant que a + b ≤ 9 (A-ZEROS à 100 %), faux dès qu'une retenue existe.
- **Échecs binaires** (X1 ×5) : `sortie = carré(±1/2 + α·a + β·b)` — une « hésitation » quadratique.

## Lecture

1. [VÉRIFIÉ, ces 5 graines] **L'objectif n'est pas le problème, la recherche l'est.** Dans les 3
   conditions ratées, le circuit exact a un MDL **bien plus bas** que le réseau rendu (X1 : 102 contre
   355 bits ; X2-1000 graine 4 : 117 contre 22 650). MDL « préfère » la règle ; l'évolution réduite ne
   l'atteint pas. Même conclusion qu'E011 vue de l'autre côté : la règle est un optimum MDL.
2. [VÉRIFIÉ] **Le chemin coûte avant de payer.** Paysage mesuré au pilote (graine 0) en binaire :
   réseau vide 4 226 bits → `v = a + b` 2 632 → sans retenue entrante 1 856 → exact 102. Le réseau qui
   hésite (355) bat toutes les étapes intermédiaires « exactes en partie » : pour les atteindre, la
   population doit **descendre** en MDL de 355 à 2 632. La sélection par troncature l'interdit.
3. [VÉRIFIÉ ici ; HYPOTHÈSE sur le mécanisme] **Le décimal est plus facile que le binaire**, et
   **plus de données aide** (0/5 → 2/5 → 4/5, et découverte plus tôt : médiane 0,53 M évaluations à 1 000 exemples
   contre 1,7 M à 100, sur 4 et 2 graines seulement). Hypothèse : (i) en base 10, hésiter entre deux chiffres voisins rapporte peu, le piège
   « hésitant » du binaire n'existe pas ; (ii) avec 1 000 exemples, \|D:G\| pèse 10× plus lourd face à
   \|G\|, donc payer 50–100 bits de structure pour une retenue devient rentable plus tôt dans la
   descente. Ce n'est pas testé séparément ici.
4. [VÉRIFIÉ pour ce système ; raison structurelle] **Format plat : 0/5**, dit franchement. Lu poids
   fort d'abord sans alignement, il faut **stocker** tout l'opérande a avant de voir b ; un réseau à état
   flottant de taille fixe ne peut pas le faire au-delà de ~15 chiffres (float64), et la recherche ne
   trouve même pas la mémorisation locale (0 % en validation 6–8, MDL ≈ 5 700 bits ≈ 20 bits par
   chiffre, le plafond). Aucun C-ORACLE-CIRCUIT n'existe pour ce format à 100 chiffres. C'est la
   même frontière qu'E008 (B-STD 0 % dès 6 chiffres) : **l'alignement est la structure décisive**.
5. [HYPOTHÈSE] Pour la question de fond (« apprendre la procédure comme un enfant ») : quand on
   **donne** l'alignement, la valeur des chiffres et une primitive de seuil (`floor`/`marche`), une
   recherche aveugle de ~10⁶ réseaux trouve la retenue à partir de 100–1 000 exemples de 1–5 chiffres
   et généralise **prouvablement** à toute longueur. Tout le reste (format, localité, nombre
   d'itérations) est donné à la main : ce n'est pas une découverte « de zéro ».

## Budget de structure (donné à la main)

| expérience | donné |
|---|---|
| X1, X2 | format aligné poids faible d'abord (le chiffre i de a et de b au même pas) ; chiffres codés par leur **valeur** scalaire ; nombre d'itérations = L+1 ; lecture de la sortie scalaire par interpolation linéaire entre chiffres voisins ; bibliothèque d'activations **avec floor et marche** (primitives de seuil) ; poids rationnels ; 1 sortie. **Non donné** : nombre d'unités, connexions, poids, laquelle est la retenue. |
| X3 | format plat poids fort d'abord ; drapeaux `+`, `=`, sortie ; nombre de pas de sortie L+1 ; même lecture et bibliothèque. Pas d'alignement. |
| tous | aucune trace intermédiaire : seuls les chiffres de la somme sont des cibles. Exemples uniques vus = 100 ou 1 000 (le jeu d'entraînement), revus à chaque évaluation. |

## Écarts au préenregistrement (tous tracés)

- **Correctif de code après le pilote, avant tout run officiel** : la somme flottante `0,3 + 0,7`
  donnait `0,999…` et faisait tomber `floor` à tort (un réseau prouvé exact en rationnels ratait 4/100
  exemples). Les entrées d'une unité sont maintenant sommées sur un dénominateur commun (entiers
  exacts), une seule division (test `test_somme_flottante_exacte`).
- **Variantes pilotes essayées puis abandonnées** (graine 0 seulement, aucune amélioration) :
  remplacement générationnel, Poisson(2) mutations, les deux. L'algorithme officiel est **celui du
  préenregistrement** (troncature, 1 + Poisson(0,5)). Tracé dans `hyperparametres.json`.
- **Plafond mur** : préenregistré comme budget, mais codé (`budget_mur_min`) entre deux invocations
  de X2-100, avant qu'il soit atteint ; X1 s'est arrêté au budget de générations (55 min < 60).
  Le compteur « secondes » ne compte que le temps de recherche. Avec 5 processus + les autres fenêtres,
  les vitesses ont varié ; l'arrêt au plafond mur rend X2/X3 **non déterministes** au nombre de
  générations près (le reste est déterministe : graines fixées).
- La mesure « évaluations » compte les réseaux distincts hors cache ; le cache étant vidé à chaque
  reprise, elle dépend légèrement du découpage en invocations. « Enfants » est déterministe.
- Interprétation de « min CPU » : temps mur machine avec 5 processus (dit au préenregistrement).

## Limites

Un algorithme, un jeu de mutations, une taille de population ; ≤ 0,6 % du budget de Lan (X3 : ~0,01 %). X3 n'a
reçu que 108–229 générations (lent : 25 lots par longueur de a × longueur de b). La lecture de sortie
par interpolation est un choix à moi : avec un lecteur softmax à 10 sorties comme chez Lan, le décimal
serait plus coûteux en \|G\|. La preuve couvre le réseau en rationnels exacts ; l'évaluation est en
float64 (identiques ici : 100 % au test pour tous les prouvés).

## Rejouer

```
PY=$HOME/.venvs/ev-llm-e008/bin/python      # numpy 2.0.2
cd research/experiments/E012-evolution
$PY -m unittest -v test_e012                  # 8 tests
$PY verifs.py                                 # C-ORACLE-ALGO, C-ORACLE-CIRCUIT, C-PARCOEUR (~5 s)
for e in X1 X2-100 X2-1000 X3; do             # a relancer jusqu'a "fini=True" (reprise sur checkpoint)
  $PY recherche.py --exp $e --graines 1 2 3 4 5 --minutes 8.5; done
$PY evaluation_e012.py                        # test final unique (~30 s)
$PY analyse_e012.py                           # resultats/resultats.json, summary.md, circuits.md
```
`runs/` hors git (checkpoints ~ Mo).
