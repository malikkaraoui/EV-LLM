# E012 — préenregistrement : une recherche évolutive + MDL découvre-t-elle le circuit de l'addition ?

Mandat M0025 (F03), 2026-09-27, branche `exp/e012-evolution` depuis `origin/exp/e011-objectif-mdl`
@ `994c77b` (qui contient déjà l'import du code E008 @ `af281f5`). Rédigé **avant** toute ligne de
code et toute recherche. Sans API, **CPU seulement** (numpy + `multiprocessing`), F01/F02 tiennent le
GPU. Réutilisation **par import** : évaluateur E008 (`evaluate.evaluer` / `resume`, `data.tire_nombre`),
codage des poids MDL d'E011 (`objectifs.bits_entier`, `bits_poids`), jeux binaires d'E011
(`donnees.jeu_validation`, `jeux_test`). Aucune modification de `E008-addition/` ni `E011-objectif-mdl/`.

## 1. Question

Lan et al. (TACL 2022) ont obtenu par recherche génétique + MDL un RNN exact pour l'addition binaire
(bits alignés, poids faible d'abord ; 250 îles × 500 réseaux × 25 000 générations ≈ 3·10⁹
évaluations). E011 a montré que ce circuit, **donné**, est un optimum MDL stable. Ici : une recherche
**réduite** (budget M1, ~10⁷ évaluations par graine, soit ~0,3 % de celui de Lan) le **découvre**-t-elle,
(1) en binaire, (2) en décimal aligné, (3) en décimal au format plat d'E008 ; à partir de combien
d'exemples ?

Hypothèses [HYPOTHÈSE], écrites pour être réfutables : (1) binaire : trouvé par ≥ 3/5 graines ;
(2) décimal aligné : plus rare, meilleur à 1 000 exemples qu'à 100 ; (3) format plat : **aucune**
graine (attendu très dur : voir §6 — un réseau à état flottant fini ne peut pas stocker un opérande
de 100 chiffres ; le seul espoir est la mémorisation locale, qui échouera hors distribution).

## 2. Espace de recherche (réseaux façon Lan, MDL-RNN)

- Graphe d'unités : entrées (valeurs fixes), **une** unité de sortie, unités cachées en nombre
  libre (0 au départ). Activations disponibles (bibliothèque de Lan 2022) : identité, ReLU,
  sigmoïde, tanh, carré, **floor**, marche (`1 si x > 0 sinon 0`).
- Connexions : **avant** (même pas de temps, graphe acyclique selon l'ordre des unités) ou
  **récurrentes** (valeur de l'unité source au pas t−1 → unité cible au pas t ; état initial 0).
  Biais facultatif par unité. Poids **rationnels** `±n/d` (n ≥ 0, d ≥ 1), calcul `x·n/d` en
  flottant 64 bits (division en dernier : exact pour les entiers).
- **Lecture de la sortie (donnée à la main, au budget de structure)** : la sortie scalaire v est
  lue comme une distribution sur les chiffres {0..B−1} (B = 2 ou 10) par interpolation linéaire
  entre les deux chiffres voisins de `clip(v, 0, B−1)` : `p(⌊v⌋) = 1 − frac(v)`, `p(⌊v⌋+1) = frac(v)`.
  v entier ⇒ probabilité 1 sur ce chiffre. Chiffre répondu = arrondi de `clip(v)`.
  Raison : un lecteur à 10 unités de sortie (softmax) rendrait le circuit décimal ~5× plus long ;
  ce choix est un **don de structure**, pas une découverte.

## 3. Objectif MDL (figé)

`MDL = |G| + |D : G|` en bits.
- `|D : G|` = Σ sur les chiffres-cibles d'entraînement de `−log₂ max(p(cible), 2⁻²⁰)`.
- `|G|` (codage préfixe, inspiré de Lan ; entiers codés par `bits_entier` d'E011 = Elias-γ de n+1) :
  `bits_entier(nb cachées)` + 3 bits d'activation par unité non-entrée + `bits_entier(nb connexions)`
  + par connexion : `2·⌈log₂(nb unités)⌉` (source, cible) + 1 bit (avant/récurrente) + `bits_poids`
  (E011 : signe + Elias(num) + Elias(dén)) + par unité non-entrée : 1 bit (biais ?) + `bits_poids`
  du biais s'il existe.

## 4. Algorithme de recherche (figé ; seuls les volumes sont calibrés par le pilote)

Modèle en îles, par graine de recherche : **I = 8 îles × P = 200 réseaux** (valeurs proposées ;
le pilote peut les **réduire**, jamais les augmenter). Initialisation : sortie identité, 0 cachée,
0 à 2 connexions entrée → sortie tirées au hasard. Génération : P enfants par île, parent choisi par
**tournoi de 2** sur MDL, 1 + Poisson(0,5) mutations parmi : ajouter une cachée (activation au hasard,
insérée à une position au hasard, avec une connexion entrante et une sortante), retirer une cachée,
ajouter une connexion avant, ajouter une récurrente, retirer une connexion, modifier un poids
(num ± 1, dén ± 1, signe, ou tirage neuf), ajouter/modifier/retirer un biais, changer une activation.
Tirage neuf d'un rationnel : n, d ∈ {1..10} avec p ∝ 1/k. Remplacement : les P enfants + les 2
meilleurs parents (élitisme), on garde les P meilleurs par MDL. **Migration** toutes les 50
générations : le meilleur de l'île i remplace le pire de l'île i+1 (anneau). Mémo des évaluations
par empreinte du génome (les répétitions ne sont pas comptées comme évaluations).
- **Arrêt** : budget de G générations (fixé par le pilote pour tenir le temps) **ou** arrêt anticipé
  si le réseau MDL-minimal toutes îles est à 100 % entraînement et 100 % validation OOD et que son MDL
  n'a pas changé depuis 300 générations. Validation vérifiée toutes les 25 générations.
- **Réseau rendu** : le MDL-minimal toutes îles à l'arrêt (aucune sélection sur le test). La
  validation ne sert qu'à l'arrêt anticipé et à mesurer « évaluations jusqu'à la découverte ».
- **Invocations ≤ 9 min** avec reprise sur checkpoint (pickle de l'état complet, dont les états des
  générateurs aléatoires) ; aucune tâche de fond.

## 5. Expériences, données, jeux

| id | format | exemples d'entraînement | budget mur (5 graines en parallèle, 5 processus) |
|---|---|---|---|
| X1 | binaire aligné, poids faible d'abord (entrées : bit de a, bit de b) | Lan : **toutes** les paires 0 ≤ a, b ≤ 9 (100), identiques pour toutes les graines | ≤ 60 min |
| X2-100 | décimal aligné, poids faible d'abord (entrées : valeur du chiffre de a, de b ; 0 au-delà) | 100 paires, opérandes 1–5 chiffres (`tire_nombre` E008), tirées par graine | ≤ 45 min |
| X2-1000 | idem | 1 000 paires, idem | ≤ 45 min |
| X3 | plat E008 : `a + b =` caractère par caractère, poids fort d'abord ; entrées : valeur du chiffre, drapeau `+`, drapeau `=`, drapeau « sortie » ; puis L+1 pas de sortie (L = max des longueurs, donné) poids fort d'abord, zéros de tête tolérés | 100 paires 1–5 chiffres | ≤ 45 min |

Les formats alignés ont **L+1 pas** (dernier = retenue finale). « Budget mur » : le mandat dit
« min CPU » ; je le lis comme **temps mur de la machine** avec 5 processus (un par graine), le
mandat autorisant le multiprocessus et fixant ≤ 4 h de calcul au total. Total prévu : 195 min + pilote.

- Graines de recherche officielles **1–5** ; **pilote = graine 0, exclu**, sur X1 et X2-100
  (vitesse, absence d'erreur) : il fixe G (et peut réduire I, P) dans `hyperparametres.json`,
  commité avant les runs officiels.
- **Validation OOD** (arrêt anticipé seulement) : binaire 6, 7, 8 bits (E011, graine 3027) ;
  décimal 6, 7, 8 chiffres, 500 paires / L, graine 3127.
- **Test final intouché, une seule évaluation** : binaire 10, 16, 32, 64, 100, 1 000 bits + adverses
  d'E011 ; décimal 10, 16, 32, 64, 100 chiffres (+ 1 000 en bonus pour les formats alignés), 500
  paires / L (200 à 1 000), graine 3128, + adverses : retenue en cascade (`99…9 + 1`, `1 + 99…9`),
  pleins de zéros (`10…01 + 10…03`, `10…02 + 10…01`), asymétriques (50 × (L, 3) + 50 × (3, L)),
  graine 3129.

## 6. Contrôles, mesures, critères

- **C-ORACLE-ALGO** : addition chiffre à chiffre codée sur listes (sans `a + b`) = 100 % sur tous
  les jeux. **C-ORACLE-CIRCUIT** (mandat : circuit construit à la main, **même** code d'exécution
  et même évaluateur) = 100 % sur tous les jeux : binaire et décimal aligné
  (`s = a + b + c₋₁` identité ; `c = floor(s / B)` ; `v = s − B·c`), 2 cachées, 6 connexions.
  Format plat : **pas** de circuit oracle à état flottant pour 100 chiffres (il faudrait stocker a
  entier dans un flottant) — dit tel quel ; seul C-ORACLE-ALGO. **C-PARCŒUR** (table des paires
  d'entraînement de la graine 1) = 0 % sur validation, test, adverses (+ 100 % sur ses propres
  paires, contrôle positif). Sinon : TEST NON VALIDE, arrêt.
- **Preuve mécanique** (si le réseau n'utilise que identité/ReLU/carré/floor/marche) : exploration
  en **rationnels exacts** (`fractions`) de l'automate produit (état caché du réseau, vraie
  retenue) depuis (0, 0), pour toutes les paires de chiffres d'entrée ; si l'ensemble d'états
  atteignables est fini et que chaque transition émet le bon chiffre, le réseau est **prouvé**
  exact pour toute longueur (format aligné). Sinon « non prouvé ».
- **Graine « a trouvé la règle exacte »** = 100 % sur tout le test final et tous les adverses
  (et, si applicable, preuve mécanique). Rapporté : nombre de graines /5, exact-match moyenne ±
  écart par jeu × L, graines ≥ 90 % à 16 chiffres, évaluations (réseaux distincts évalués) jusqu'à
  la première génération où le MDL-minimal est exact en entraînement + validation, taille du circuit
  (cachées, connexions), |G|, |D:G|.
- **Faux et sûr** : faux avec confiance ≥ 0,8 (confiance = produit des p du chiffre choisi) ; pas
  d'abstention (sans objet).
- **Exemples uniques vus** = taille du jeu d'entraînement (100 / 1 000), journalisée ; nombre
  d'évaluations de réseau journalisé séparément.
- Verdict par expérience : « découvre » si ≥ 3/5 graines exactes ; « parfois » 1–2/5 ; « non » 0/5.
  Aucune conclusion générale sur 5 graines.

## 7. Budget de structure (ce qui est donné à la main)

| expérience | donné |
|---|---|
| X1, X2 | format aligné poids faible d'abord (localité : le chiffre i de a et de b au même pas) ; chiffres codés par leur **valeur** scalaire ; nombre d'itérations = L+1 ; lecture de sortie scalaire par interpolation (§2) ; bibliothèque d'activations **avec floor et marche** (primitives de retenue) ; poids rationnels ; 1 sortie. Non donné : le nombre d'unités, les connexions, les poids, laquelle est la retenue. |
| X3 | format plat poids fort d'abord ; drapeaux `+`, `=`, sortie ; nombre de pas de sortie L+1 ; même lecture et même bibliothèque. Pas d'alignement. |
| tous | aucune trace intermédiaire (seuls les chiffres de la somme sont des cibles). |

## 8. Ordre des commits

préenregistrement (ce fichier, poussé seul) < code < valeurs figées après pilote (graine 0) < résultats.
