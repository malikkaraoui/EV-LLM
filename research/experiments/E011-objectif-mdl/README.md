# E011 — l'objectif MDL contre l'entropie croisée (partie 1 seule : stabilité de la solution parfaite)

Mandat M0024 (F03), 2026-09-27, branche `exp/e011-objectif-mdl`. Préenregistrement :
[`PREREGISTREMENT.md`](PREREGISTREMENT.md) (poussé seul, commit `5159e0e`, avant tout code).
Sans API, **CPU seulement** (numpy, rétropropagation manuelle vérifiée par test de gradient),
~4 min de calcul au total. Évaluateur **E008** (`evaluate.evaluer` / `resume`) importé tel quel.

## Réponse courte

**« L'entropie croisée empêche-t-elle de garder la règle exacte ? » — Ici, non.** Sur l'addition
binaire, un RNN construit à la main pour être exact et **entraîné ensuite par entropie croisée
seule** reste exact jusqu'à 1 000 bits sur **5 graines sur 5** [VÉRIFIÉ]. Ce qui détruit la règle,
ce sont les **pénalités de taille des poids** assez fortes (L2 λ = 0,1 : 2/5 ; L2 λ = 1 : 0/5 ;
L1 λ = 1 : 2/5) [VÉRIFIÉ]. Le **MDL discret** (codage de Lan 2022) garde la règle 5/5 **et la
compresse** (206 → 204 bits) [VÉRIFIÉ] ; **mon approximation différentiable de MDL** fait moins
bien que la CE seule (4/5) [VÉRIFIÉ]. Tout cela sur **un** réseau et **une** tâche : aucune
conclusion générale.

## Écarts trouvés dans les chiffres du mandat (vérifiés dans les PDF, détail au préenregistrement §0)

- **Contredit** : « 1 unité cachée et 7 connexions » est la ligne MDL du Tableau 6 de Lan et al.
  2022, **tâche aⁿbⁿ**. Le réseau d'addition (Fig. 9, Théorème 4.6) utilise 2 unités cachées
  (retenue avec `floor`, somme).
- **Écart** : le test d'addition de Lan 2022 va jusqu'à 271 (≤ 9 bits, entraînement ≤ 5 bits) ; la
  généralité « tous les entiers » vient de la **preuve** (pour le réseau entraîné sur 400 paires).
- **Écart** : Lan et al. 2024 (2402.10013) = LSTM aⁿbⁿ, analyse de **surface de perte** autour du
  réseau parfait, pas un entraînement depuis lui. C'est 2505.13398 qui entraîne depuis la solution
  parfaite (« standard regularization consistently drifts away from the golden solution »), sur
  aⁿbⁿ, aⁿbⁿcⁿ, Dyck-1 — **pas l'addition** — et sans MDL par gradient.
- Vérifiés : format binaire poids faible d'abord, 100 exemples (et 400), 100 % aux tests,
  250 îles × 500 × 25 000 générations.

**STOP §4 appliqué** : un chiffre contredit → seule la partie 1 est exécutée. Parties 2
(réplication évolutive) et 3 (pont décimal) : **non faites**, à arbitrer.

## Protocole (résumé ; figé au préenregistrement)

- Addition binaire, poids faible d'abord, un pas par bit, L+1 pas ; réponse lue au seuil 0,5,
  comparée à `str(a + b)` par l'évaluateur E008.
- **Golden** : RNN d'Elman 2 → 3 sigmoïdes → 1 sigmoïde (22 paramètres), gains k = 10, poids
  entiers : `s = n + m + c`, `h_j = σ(10 (s − θ_j))`, θ = (0,5 ; 1,5 ; 2,5), retenue `c = h_2`,
  sortie `σ(10 (h_1 − h_2 + h_3 − 0,5))`.
- Entraînement : **100 exemples uniques** (opérandes 1–5 bits), tirés par graine (« bruit de
  données ») ; tous les runs partent du golden. Gradient : Adam lr 1e-3, lots de 20, 20 000 pas.
  Recherche locale (d, d-CE, d-L2) : 20 000 propositions ±1/2^j sur un poids, acceptées si
  l'objectif ne monte pas. CE mesurée en bits (somme sur le corpus, comme |D : G|).
- Objectifs : a CE ; b CE + λΣw² ; c CE + λΣ|w| (λ ∈ {0,01 ; 0,1 ; 1}) ; e MDL différentiable (poids
  quantifiés au demi, droit-à-travers, + Σ 2 log₂(1 + 2|w|)) ; d MDL discret (Lan : signe +
  Elias(numérateur) + Elias(dénominateur) + CE) ; d-CE, d-L2 (λ = 0,1) : même recherche locale,
  autres objectifs (isole l'objectif de l'optimiseur).
- Validation OOD 6–8 bits (dérive, aucune sélection) ; **test final unique** : 10, 16, 32, 64,
  100, 1 000 bits + adverses (retenue en cascade, pleins de zéros, longueurs asymétriques L + 3).
- Graines 1–5 officielles, graine 0 = pilote (aucune valeur changée, `hyperparametres.json`).

## Validité du test (`resultats/controles.json`)

| contrôle | attendu | obtenu |
|---|---|---|
| C-ORACLE (retenue binaire sur listes de bits, sans `a + b`) | 100 % | **100 %** sur les 27 jeux × longueurs |
| C-PARCŒUR (table des 100 paires, graine 1) | 0 % | **0 %** partout ; 100 % sur ses propres paires (contrôle positif) |
| C-GOLDEN (réseau construit, avant tout entraînement) | 100 % | **100 %** partout, y compris 1 000 bits et adverses |

**TEST VALIDE** [VÉRIFIÉ]. Contrôle négatif implicite : b λ = 1 tombe à 0 % partout, l'évaluateur
détecte donc bien les réseaux faux.

## Résultats (test final, 5 graines ; détail : [`resultats/summary.md`](resultats/summary.md))

| objectif | graines exactes (tout test + adverses, jusqu'à 1 000 bits) | ≥ 90 % à 16 | verdict préenregistré | 1re perte d'exactitude en validation (pas) | ce qui se passe |
|---|---|---|---|---|---|
| a CE seule | **5/5** | 5 | garde la règle | jamais | gains ×1,5–2 (norme 46 → 74), CE train 5,2 → 0,009 bit |
| b L2 λ = 0,01 | 5/5 | 5 | garde | jamais | |
| b L2 λ = 0,1 | **2/5** | 2 | s'en éloigne | 11 000–19 000 (3 graines) | gains ramenés à ~4 : la retenue « fuit », échec croissant avec L (100 % → 0 % à 1 000 bits sur 3 graines) |
| b L2 λ = 1 | **0/5** | 0 | s'en éloigne | 3 100–3 740 | réseau effondré (poids ≈ 0), 0 % partout |
| c L1 λ = 0,01 ; 0,1 | 5/5 ; 5/5 | 5 ; 5 | garde | jamais | |
| c L1 λ = 1 | **2/5** | 2 | s'en éloigne | 8 850–19 030 (3 graines) | même mécanisme que L2 λ = 0,1 |
| e MDL différentiable | **4/5** | 4 | instable | ~3 200 (toutes ; 4 se rétablissent) | gains ramenés à 3–5 ; graine 1 : 49,6 % à 100 bits, 0,5 % à 1 000 |
| d MDL discret | **5/5** | 5 | garde la règle | jamais | 37–43 changements acceptés, poids restés entiers, \|H\| 206 → **204** bits, objectif 211,2 → 205,0 dès ~3 000 pas puis immobile |
| d-CE (recherche locale) | 5/5 | 5 | garde | jamais | 8 192–8 715 changements, gains ×10–20 (dist. ~400) |
| d-L2 λ = 0,1 (recherche locale) | 5/5 | 5 | garde | 90–320 (2 graines, rétablies) | |

Faux et sûr (confiance ≥ 0,8) : **0 partout** — mais la confiance est un produit sur L+1 bits,
elle s'écrase aux grandes longueurs ; l'indicateur est donc **peu informatif** ici [VÉRIFIÉ par
construction]. Pas d'abstention dans ces systèmes. Exemples uniques vus : 100 par run.

## Lecture

1. [VÉRIFIÉ, ce réseau/cette tâche] L'entropie croisée seule **ne** chasse **pas** la solution
   exacte : sur une tâche **déterministe**, son infimum est à l'infini *le long* de la solution
   (grossir les gains la rend plus sûre sans changer la règle). Cela **diffère** du résultat de
   2505.13398 (« none » s'éloigne aussi) ; [HYPOTHÈSE] la différence tient à la cible : leurs
   langues formelles ont des distributions de symboles **probabilistes**, où la CE peut
   sur-apprendre les fréquences du corpus fini ; ici chaque bit est certain.
2. [VÉRIFIÉ] Les pénalités de norme sont le vrai danger : elles tirent les gains vers le bas, la
   retenue perd sa saturation et **l'erreur apparaît d'abord aux longueurs jamais vues** (la
   validation 6–8 bits ne la voit pas toujours : b λ = 0,1 graines 3 et 4 restent exactes, les
   autres tombent à 0 % à 1 000 bits). Le seuil est entre λ = 0,01 et 0,1 pour L2 (CE totale en
   bits sur 100 exemples) — il dépend de cette échelle.
3. [VÉRIFIÉ] MDL discret : la solution parfaite est (presque) un optimum — la recherche en trouve
   un voisin **plus court et toujours exact**, puis s'arrête. C'est l'affirmation de Lan et al.,
   ici confirmée sur l'addition. [VÉRIFIÉ] La même recherche locale avec CE ou L2 garde aussi la
   règle : dans ce cadre, l'optimiseur (pas acceptés seulement s'ils n'aggravent pas l'objectif,
   ici sur 100 exemples) compte autant que l'objectif.
4. [VÉRIFIÉ] Mon approximation différentiable de MDL (quantification + coût lisse en log) se
   comporte comme une pénalité de norme douce : elle rétrécit les gains et casse une graine. Ce
   n'est **pas** un bon substitut de MDL ; il ne faut pas la porter telle quelle à E009/E010.

## Limites

Partie 1 = **stabilité** d'une règle **donnée à la main**, pas sa découverte (budget de structure :
format, localité, nombre d'itérations, architecture **et la solution elle-même** sont donnés).
Un seul réseau (3 sigmoïdes, k = 10), une seule tâche, un seul lr, 20 000 pas. Réseau sigmoïde, pas
le réseau `floor` de Lan. \|H\| des réseaux à poids continus (a, b, c) calculé par
`limit_denominator(2^16)` : chiffres de \|H\| comparables seulement entre d, e et golden.

## Conséquence pour E009/E010 [HYPOTHÈSE]

L'entropie croisée n'est pas, à elle seule, un « plafond caché » pour une tâche déterministe comme
l'addition. Deux pistes plus probables : (i) la **pénalité de poids** (E008 : AdamW wd 0,01) —
à tester en ablation wd = 0 ; (ii) la **découverte** de la règle (pas sa conservation), que la
partie 1 ne mesure pas — c'est l'objet des parties 2–3 non exécutées. Recommandation : lancer la
partie 2 (réplication MDL-RNN réduite) avec les chiffres corrigés.

## Rejouer

```
PY=$HOME/.venvs/ev-llm-e008/bin/python      # numpy 2.0.2 suffit
cd research/experiments/E011-objectif-mdl
$PY -m unittest -v test_e011                 # 7 tests (dont gradient numerique)
$PY controles.py                             # C-ORACLE, C-PARCOEUR, C-GOLDEN (~1 s)
$PY train.py --graines 0                     # pilote (~40 s)
$PY train.py --graines 1 2 3 4 5             # 55 runs (~3,5 min)
$PY evaluation_finale.py                     # test final unique (~20 s)
$PY analyse.py                               # resultats/resultats.json, summary.md, trajectoires.csv
```
Déterministe (numpy CPU, graines fixées) ; `runs/` hors git.
