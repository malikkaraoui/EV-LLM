# E011 — préenregistrement : l'objectif (entropie croisée) éloigne-t-il de la règle exacte ?

Mandat M0024 (F03), 2026-09-27, branche `exp/e011-objectif-mdl` (depuis `origin/main` @ `70a8d93`,
puis fusion de `origin/exp/e008-addition` @ `af281f5` pour réutiliser l'évaluateur E008 par import,
sans modifier `research/experiments/E008-addition/`). Rédigé **avant** toute ligne de code et tout
entraînement. Sans API, sans GPU (CPU seulement : F01/F02 tiennent le GPU).

## 0. Vérification des chiffres cités par le mandat (faite avant ce texte)

PDF téléchargés et lus en texte (`pdftotext`), passages exacts courts :

| affirmation du mandat | source | verdict |
|---|---|---|
| addition binaire, format donné (bits alignés, poids faible d'abord) | Lan et al. 2022 §4.5.1 : « fed at each time step i with a tuple of binary digits […] starting from the least significant bit » | [VÉRIFIÉ] |
| apprise à partir de 100 exemples | §4.5.1 : « all pairs of integers up to K = 10 (total 100 samples), and a larger set of all pairs up to K = 20 (total 400) » | [VÉRIFIÉ] (deux corpus : 100 et 400) |
| 100 % « sur des longueurs bien supérieures » | test : « pairs of integers n, m ∈ [K + 1, K + 251], i.e., 62,500 pairs » ; §4.5.2 : « MDLRNNs reached 100% accuracy on both test sets » | **ÉCART** : le test va jusqu'à 271, soit ≤ 9 bits contre ≤ 5 à l'entraînement ; pas « bien supérieures ». La généralité vient de la **preuve**, pas du test |
| prouvé correct pour tous les entiers | Théorème 4.6 : « the output unit at time step i is the ith digit of the sum » ; légende Fig. 9 : « trained on all 400 pairs […] correct for all numbers » | [VÉRIFIÉ] **pour le réseau entraîné sur 400 paires** ; le texte ne donne pas de preuve explicite pour celui des 100 |
| « 1 unité cachée et 7 connexions » | Tableau 6 : « \|D : G\| + \|G\| (MDL) 38.1 25.8 1 7 », légende : « on the a<sup>n</sup>b<sup>n</sup> task » | **CONTREDIT** pour l'addition : 1 unité / 7 connexions est le réseau MDL de a<sup>n</sup>b<sup>n</sup>. Le réseau d'addition de la preuve utilise les unités 3 (retenue, `floor`) et 4 (somme) : **2 unités cachées** [VÉRIFIÉ par le texte de la preuve] |
| recherche génétique 250 îles × 500 × 25 000 générations | §4.1 : « 250 islands, each with population size 500 (total 125,000 networks), 25,000 generations » | [VÉRIFIÉ] |
| Lan et al. 2024 : CE + L1/L2, **même en partant de la solution parfaite, l'entraînement s'en éloigne** | 2402.10013, §4.4 : « if L1 or L2 regularization were used, the golden network would not have been found » | **ÉCART** : tâche a<sup>n</sup>b<sup>n</sup> (LSTM), analyse de la **surface de perte** autour du réseau parfait, pas un entraînement lancé depuis lui ; pas d'addition |
| … « avec MDL elle est un optimum » | idem : « MDL results in the correct solution being an optimum » | [VÉRIFIÉ] (au voisinage tracé, a<sup>n</sup>b<sup>n</sup>) |
| 2505.13398 : idem | résumé : « actively pushed away from perfect initializations » ; §3 : « We train them via backpropagation, starting from the golden weights […] standard regularization consistently drifts away from the golden solution » | [VÉRIFIÉ] mais sur a<sup>n</sup>b<sup>n</sup>, a<sup>n</sup>b<sup>n</sup>c<sup>n</sup>, Dyck-1 ; **pas d'addition** ; MDL lui-même **non entraîné par gradient** (« MDL is excluded due to its nondifferentiability ») ; Adam lr 1e-4, 1 000 époques, λ = 1 |

**Conséquence (STOP §4 du mandat, appliqué strictement)** : un chiffre cité est contredit
(1 unité / 7 connexions) et deux affirmations sont transposées d'une autre tâche. Le mandat dit
alors : « rapporte, continue seulement la partie 1 ». **Seule la partie 1 est exécutée** ; les
parties 2 (réplication évolutive) et 3 (pont décimal) sont laissées à l'arbitrage de
l'orchestrateur. Ajustement du protocole : la partie 1 devient **la première mesure du
phénomène « s'éloigne de la solution parfaite » sur l'addition** (aucun des trois papiers ne l'a
faite sur l'addition) — c'est donc une question ouverte, pas une réplication.

## 1. Question

Un petit réseau récurrent **construit à la main pour être exact** sur l'addition binaire (poids
faible d'abord) reste-t-il exact quand on **continue de l'entraîner** sur 100 exemples courts avec
(a) entropie croisée seule, (b) CE + L2, (c) CE + L1, (d) MDL (codage discret des poids façon
Lan 2022), (e) une approximation différentiable de MDL ? À quelle vitesse dérive-t-il ?

Hypothèse de travail [HYPOTHÈSE] : (a) garde l'exactitude (la CE pousse les gains vers l'infini,
ce qui préserve la règle), (b)/(c) avec λ assez grand l'érodent (les gains baissent jusqu'à ce que
la retenue « fuie » sur les longues séquences), (d)/(e) la gardent. Cette hypothèse peut être
fausse ; elle est écrite pour être réfutable.

## 2. Tâche, données, jeux (figés)

- Entrée au pas i : `(n_i, m_i)` bits d'indice i (poids faible d'abord), zéros au-delà de la
  longueur de chaque opérande ; **L+1 pas** pour L = max des longueurs (dernier pas = retenue
  finale). Sortie au pas i : probabilité que le bit i de la somme vaille 1. Réponse = les L+1 bits
  lus au seuil 0,5 ; convertie en entier puis en chaîne décimale, comparée à `str(a + b)` par
  l'**évaluateur unique E008** (`evaluate.evaluer` / `resume`, importés tels quels).
- **Entraînement** : pour la graine g, 100 paires distinctes, longueur de chaque opérande
  uniforme et indépendante dans **1–5 bits** (bit de tête = 1 sauf longueur 1),
  `rng = default_rng(20_000 + g)`. **100 exemples uniques** : c'est aussi le nombre d'exemples
  uniques vus (journalisé).
- **Validation OOD** (seule autorisée pour observer la dérive en cours de route ; aucun choix ne
  dépend d'elle, voir §4) : L = 6, 7, 8 bits, 500 paires / L, graine 3027.
- **Test final intouché**, évalué **une fois**, à la fin : L = 10, 16, 32, 64, 100, **1 000** bits
  (1 000 exigé par le mandat), 500 paires / L (200 à 1 000 bits), graine 3028.
- **Tests adverses** (évalués avec le test final) pour L ∈ {10, 16, 32, 64, 100, 1 000} :
  retenue en cascade `(2^L − 1) + 1` et `1 + (2^L − 1)` ; nombres pleins de zéros
  `(2^(L−1) + 1) + (2^(L−1) + 3)` et `(2^(L−1) + 2) + (2^(L−1) + 1)` ; longueurs asymétriques :
  50 paires (L bits, 3 bits) et 50 paires (3 bits, L bits), graine 3029.
- **Contrôles de validité** (recalculés sur tous ces jeux, leçon M0020) : C-ORACLE (retenue binaire
  codée à la main sur les listes de bits, sans `a + b`) = 100 % partout ; C-PARCŒUR (table des 100
  paires d'entraînement de la graine 1) = 0 % sur validation, test et adverses. Sinon : TEST NON
  VALIDE, arrêt.

## 3. Réseau parfait (« golden ») — construit à la main

RNN d'Elman, 2 entrées, **3 unités cachées sigmoïdes**, 1 sortie sigmoïde (22 paramètres) :
`s_t = n_t + m_t + c_{t−1}`, `h_j = σ(k (s_t − θ_j))`, θ = (0,5 ; 1,5 ; 2,5), `c_t = h_2`,
`p_t = σ(k_o (h_1 − h_2 + h_3 − 0,5))`, avec **k = k_o = 10**. Toutes les valeurs sont des entiers
(poids 10, −10 ; biais −5, −15, −25 ; biais de sortie −5) : c'est la solution « simple » au sens de
Lan (rationnels courts). Un réseau à 2 unités façon Lan (`floor`) n'est pas dérivable ; le choix
sigmoïde est fait pour que (a)–(c), (e) soient entraînables par gradient.
**C-GOLDEN** (condition préalable) : 100 % sur validation, test (jusqu'à 1 000 bits) et adverses.
Si échec : k est augmenté (20, puis 30) **avant** tout entraînement, et c'est noté.

## 4. Objectifs et entraînement (figés ; pilote = graine 0, exclue)

Terme de données commun : **CE totale en bits** sur les 100 exemples (somme sur tous les bits de
sortie, log₂), comme |D : G| chez Lan. Tous les runs partent des poids golden exacts.

| code | objectif | optimiseur |
|---|---|---|
| a | CE | Adam, lr 1e-3, lots de 20 exemples (5 lots / époque, ordre selon la graine), **20 000 pas** |
| b | CE + λ Σ w², λ ∈ {0,01 ; 0,1 ; 1} (1 = valeur de 2505.13398) | idem |
| c | CE + λ Σ \|w\|, λ ∈ {0,01 ; 0,1 ; 1} | idem |
| e | MDL différentiable : CE calculée avec les poids **quantifiés au demi** (`round(2w)/2`, gradient droit-à-travers) + Σ 2·log₂(1 + 2\|w\|) (enveloppe lisse de la longueur du code d'Elias du numérateur) | idem |
| d | MDL discret : \|H\| (codage de Lan : 1 bit de signe + code préfixe des numérateur et dénominateur, `2⌊log₂ n⌋ + 1` bits par entier) + CE en bits | recherche locale (1+1) : 20 000 propositions ; une proposition change un poids tiré au hasard de ±1/2^j (j ∈ {0,1,2,3}) ; acceptée si l'objectif **ne monte pas** |
| d-CE, d-L2 | mêmes propositions, objectif CE seule / CE + L2 (λ = 0,1) | idem (isole l'objectif de l'optimiseur, cf. Tableau 3 de 2505) |

- Graines officielles **1, 2, 3, 4, 5** (« bruit de données » : chaque graine tire ses 100 exemples
  et l'ordre des lots / les propositions). Pilote graine 0 : vérifie seulement la durée et
  l'absence de NaN. Le pilote **peut** réduire le nombre de pas (jamais l'augmenter) si le budget
  CPU l'exige ; valeur figée dans `hyperparametres.json` avant les runs officiels.
- **Aucune sélection** de checkpoint ni d'hyperparamètre : on rapporte le réseau au dernier pas.
- Trajectoire (pour la vitesse de dérive), aux pas 0, 10, 30, 100, 300, 1 000, 3 000, 10 000,
  20 000 : CE train (bits), objectif, ‖θ − θ*‖₂, exact-match validation 6–8, **pas de première
  perte d'exactitude en validation**.

## 5. Mesures et critères

- Exact-match par jeu × L (évaluateur E008) ; par objectif : moyenne ± écart sur 5 graines et
  **nombre de graines « exactes »** = 100 % sur tout le test (jusqu'à 1 000 bits) et tous les
  adverses. Seuil du cadre commun (≥ 90 % à 16 chiffres) rapporté aussi.
- **Faux et sûr** : faux avec confiance ≥ 0,8, confiance = produit des max(p, 1 − p) par bit.
  Pas d'abstention dans ces systèmes : taux d'abstention sans objet.
- **Verdict par objectif** : « garde la règle » si 5/5 graines exactes ; « s'en éloigne » si ≤ 2/5 ;
  entre les deux : « instable ». Aucune conclusion générale au-delà de ce réseau et de cette tâche.

## 6. Budget de structure (ce qui est donné à la main)

Format (binaire, poids faible d'abord, bits alignés, un pas par bit, L+1 pas) ; localité (un bit
par pas, la retenue est la seule mémoire) ; nombre d'itérations (= longueur, donné) ; architecture
(3 unités, sigmoïde) ; **la solution elle-même** (initialisation golden). Rien n'est appris « de
zéro » dans la partie 1 : elle mesure la **stabilité** d'une règle donnée, pas sa découverte.

## 7. Ordre des commits

préenregistrement (ce fichier, poussé seul) < code < valeurs figées après pilote < résultats.
