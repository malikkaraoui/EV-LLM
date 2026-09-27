# E009 « A » — la procédure apprise par l'architecture : préenregistrement

Mandat M0022, 2026-09-27, branche `exp/e009-procedure-apprise` (depuis `origin/exp/e008-addition`
@ `af281f5`). Ce document est committé et poussé **seul, avant toute ligne de code et toute
exécution**. Toute modification ultérieure est un amendement daté en fin de fichier, jamais une
réécriture.

**Question.** Des **biais d'architecture, et eux seuls** (récurrence, localité, calcul
proportionnel à la taille, arrêt appris), suffisent-ils pour apprendre l'addition sur des
opérandes de 1 à 5 chiffres et la généraliser à toute longueur, **sans qu'on donne
l'alignement des chiffres** ? Références à battre (E008, chiffres existants, pas de
réentraînement) : B-STD 0 % dès 6 chiffres ; B-REF (NoPE + sortie inversée) 91,2 % à 6,
7,9 % à 7, 0,1 % à 8, 0 % au-delà.

## 1. Ce qui est réutilisé d'E008 (par import, sans modification de `E008-addition/`)

- Opérandes, tirage (`tire_nombre`), **flux d'entraînement** (`paires_du_pas` : lot du pas t de
  la graine s = `default_rng([10 000 + s, t])`, longueurs indépendantes uniformes 1–5, 256
  paires, exclusion des paires de test E008 et de leurs paires échangées).
- **Évaluateur unique** : `evaluer` / `resume` d'E008 (référence = `a + b` Python, égalité exacte
  des chaînes, « faux et sûr » = faux avec confiance ≥ 0,8, chaîne de retenue).
- Oracle `addition_retenue` d'E008 (C-ORACLE).
- Jeu T-ID d'E008 (L = 2–5), 200 premiers items par longueur, pour vérifier l'apprentissage dans
  la distribution.

## 2. Format : entrée plate, bande de calcul

- Entrée : **la même séquence plate qu'E008**, `a₁…aₙ + b₁…bₘ =` (un token par caractère, ids
  E008 0–13). **Aucune grille alignée, aucun index de position, opérandes non inversés.**
- Les trois familles lisent et écrivent sur une **bande** : la séquence d'entrée (longueur
  n = ℓa + ℓb + 2) suivie de **n cases réponse** (token `SLOT`, id 14 ; vocabulaire de 15).
  Bande de longueur 2n. La réponse est écrite dans les cases réponse à partir de la première :
  chiffres de la somme, puis `$` (fin), puis remplissage. n cases suffisent toujours
  (somme ≤ max(ℓa, ℓb) + 1 chiffres). Perte : entropie croisée sur **toutes les cases réponse**
  (y compris fin et remplissage), aucune sur l'entrée. Sortie non autorégressive : toute la
  réponse est lue d'un coup sur la bande au moment de l'arrêt.
- Lots d'entraînement : bandes complétées à droite par du remplissage jusqu'à la plus longue du
  lot (≤ 24). Au test, une bande par longueur, sans remplissage supplémentaire.
- **Format de sortie** : criblage et confirmation en **inversé** (poids faible dans la première
  case), le format de B-REF. Le meilleur système du criblage est aussi entraîné en **standard**
  (poids fort d'abord), 2 graines, rapporté à côté.
- Décodage : argmax par case ; réponse = cases avant le premier `$` (ré-inversée si format
  inversé) ; pas de `$` → réponse `None` (non-réponse). Confiance = produit des probabilités
  argmax des cases jusqu'au premier `$` inclus (analogue exact de la confiance E008) ; sans `$`,
  produit sur toutes les cases.

## 3. Systèmes (même entrée, même flux, même budget de pas)

Largeur 128 partout, noyau de convolution 3, GELU/ReLU comme indiqué.

- **A1 — Neural GPU** (1511.08228, version 1D) : état initial = plongement de la bande ; à chaque
  itération, 2 couches CGRU (portes u, r et candidat par convolution k = 3) ; **nombre
  d'itérations = longueur de la bande** (2n au test ; longueur de la bande complétée du lot à
  l'entraînement, ≤ 24) ; lecture linéaire de l'état final. Perte sur la sortie finale.
- **A2 — Deep Thinking** (2202.05826) : projection d'entrée (conv) x̃ ; état h₀ = 0 ; itération
  h ← B([h ; x̃]) avec **recall** (x̃ réinjecté à chaque itération), B = conv(2w→w) + 2 blocs
  résiduels (2 conv chacun), ReLU ; tête = 3 conv. **Perte progressive** : L = ½·L(M) +
  ½·L(n→n+k), où L(M) = perte après M = 24 itérations, et pour L(n→n+k) : n ~ U{0…M−1}
  itérations sans gradient, puis k ~ U{1…M−n} avec gradient. M = 24 est **fixe** (longueur
  maximale d'une bande d'entraînement), identique pour tous les exemples.
- **A2-L — Deep Thinking + contrainte de Lipschitz** (approximation de 2410.23451) : A2 avec
  **normalisation spectrale** de chaque convolution du bloc récurrent (norme spectrale de la
  matrice (w_out, w_in·k) estimée par 3 itérations de puissance, poids divisé par elle) et ELU
  à la place de ReLU dans le bloc récurrent. Les autres détails de 2410.23451 ne sont pas
  reproduits (écart assumé).
- **A3 — Looped Transformer NoPE, arrêt par confiance** (2409.15647, version « non trichée ») :
  **un seul** bloc transformer pré-LN (attention **causale**, 4 têtes, d = 128, FFN 512, GELU),
  **sans aucune position** (NoPE), bouclé avec injection de l'entrée (h ← Bloc(h + e(x)),
  h₀ = 0). Entraîné avec la **même perte progressive que A2** (M = 24 fixe) : **aucun T(n)
  fourni à l'entraînement**.
- **A3-T — Looped Transformer, T(n) fourni : « structure injectée »** (référence) : même modèle,
  entraîné et testé avec T(n) = max(ℓa, ℓb) + 1 itérations par exemple (forme reprise de
  2409.15647 pour l'addition [HYPOTHÈSE sur l'identité exacte de la formule]). Perte à T(n).
- **Arrêt au test (A2, A2-L, A3)** : itérations t = 1…C avec **plafond fixe C = 512**, identique
  pour toutes les longueurs ; la sortie retenue est celle de l'itération de **confiance
  maximale**, confiance d'arrêt = somme des log-probabilités argmax sur **toutes** les cases
  réponse (ne lit jamais la référence). A1 : T = 2n exactement. A3-T : T(n) exactement.
- Références B-STD, B-REF : chiffres E008 recopiés (mêmes flux, autre format de sortie :
  autorégressif).

### Budget de structure (ce qui est donné à la main)

| système | format | localité | itérations | traces intermédiaires |
|---|---|---|---|---|
| A1 | bande 2n, cases réponse à droite de `=` | convolution k = 3 (localité imposée) | **T = 2n, donné** (calcul proportionnel à la taille) | aucune |
| A2 | idem | convolution k = 3 | M = 24 fixe à l'entraînement ; au test ≤ 512 fixes, arrêt appris (confiance) | aucune |
| A2-L | idem | idem + contrainte de Lipschitz | idem A2 | aucune |
| A3 | idem | aucune (attention causale globale, NoPE) | idem A2 | aucune |
| A3-T | idem | idem A3 | **T(n) = max(ℓa, ℓb) + 1, donné à l'entraînement et au test** | aucune |
| B-STD / B-REF | E008 (autorégressif) | aucune | profondeur fixe 4 | aucune |

Commun à tous : la longueur de la bande de réponse (n cases) et l'emplacement de la réponse
(juste après `=`) sont donnés ; la fin `$` est apprise. **Aucun** système ne reçoit
l'alignement des chiffres, les opérandes inversés ni un index de position.

## 4. Entraînement (identique pour tous)

- Flux E008 (graines officielles 1–5 ; **graine 0 = pilote, exclue**), 256 paires par pas.
- AdamW, lr max 1e-3 (montée 500 pas, puis cosinus jusqu'à 1e-5), β = (0,9 ; 0,98), wd 0,01,
  écrêtage 1,0, float32, MLX 0.29.3 sur M1.
- **Nombre de pas S : provisoire 6 000, figé après le pilote** (graine 0) par amendement, pour
  tenir le budget (§8). Même S pour tous les systèmes (budget égal).
- **Choix du checkpoint** : jalons à 1/8, 2/8, … 8/8 de S ; à chaque jalon, validation sur
  100 items par longueur de VAL (6, 7, 8) ; on garde le checkpoint de meilleure moyenne VAL
  (égalité : le plus tardif). **Seule VAL sert à choisir.**
- Journalisé : pas, exemples vus (pas × 256) et **exemples uniques vus** (paires distinctes du
  flux jusqu'à ce pas), perte, durée de calcul.

## 5. Jeux d'évaluation (tous nouveaux sauf T-ID ; déterministes)

« Longueur L » = les deux opérandes ont L chiffres, sauf mention.

- **VAL** (validation OOD, seule utilisée pour choisir) : L = 6, 7, 8 ; 300 paires uniques par
  longueur, graine 2030.
- **TEST** (final, **intouché jusqu'à la fin, évalué une seule fois**) : L = 10, 16, 32, 64, 100 ;
  200 paires uniques par longueur, graine 2031.
- **ADV-RET** (retenues en cascade) : par L ∈ TEST, 100 paires à retenue à chaque position
  (générateur E008) + `99…9 + 1` et `1 + 99…9` ; graine 2032.
- **ADV-ZERO** (pleins de zéros) : par L, `10…02 + 10…03` + 100 paires dont chaque chiffre non
  de tête vaut 0 avec probabilité 0,9 (sinon uniforme 1–9) ; graine 2033.
- **ADV-ASYM** (longueurs asymétriques) : par L, a à L chiffres et b à 1 ou 3 chiffres, dans les
  deux ordres (a + b et b + a), 50 paires par combinaison (200 par L) ; graine 2034.
- **T-ID** (E008, 200 premiers items par L = 2–5) : contrôle d'apprentissage dans la distribution.
- ADV-* et TEST sont évalués **en même temps, une seule fois, à la fin**.

## 6. Contrôles de validité (recalculés sur tous les nouveaux jeux, avant tout modèle appris)

- **C-ORACLE** (addition avec retenue codée à la main, E008) : 100 % attendu sur VAL, TEST,
  ADV-*, T-ID.
- **C-PARCŒUR** (table des paires distinctes vues par la graine 1 sur S pas ; répond la somme
  si la paire est dans la table, rien sinon) : ≤ 1 % attendu sur VAL, TEST, ADV-*, T-ID ;
  contrôle positif T-ID1 d'E008 (100 paires à 1 chiffre) = 100 % attendu.
- **C-BANDE** (test unitaire) : un faux modèle qui renvoie exactement la bande cible encodée
  (inversée et standard) passe à 100 % par le décodeur ; un faux modèle qui décale d'une case
  tombe à ≈ 0 %.
- Échec d'un contrôle = **STOP**, aucun modèle lu.

## 7. Déroulé, seuils et prédictions

1. **Criblage** : A1, A2, A2-L, A3, A3-T × graines 1 et 2, S pas chacun. Évaluation VAL complète
   (300 / L) + T-ID sur le checkpoint retenu.
2. **Passage en confirmation** : moyenne des 2 graines **≥ 50 % à L = 8 en VAL**. Graines 3, 4, 5
   ajoutées (les graines 1–2 comptent : 5 graines au total).
3. **Format standard** : le meilleur système du criblage (moyenne VAL 8, puis 7, puis 6) est
   aussi entraîné en format standard, graines 1–2.
4. **Test final** : tous les runs entraînés, TEST + ADV-*, une seule fois, à la fin.
5. **Courbe d'efficacité** du meilleur système : VAL (100 / L) aux jalons en fonction des
   exemples uniques vus.

Critères : exact-match séquence entière. Une **graine réussie** = ≥ 90 % à L = 16 (TEST). Un
système n'est déclaré **« réussi »** qu'avec 5 graines et ≥ 3 graines réussies ; on rapporte
toujours moyenne ± écart-type **et** nombre de graines réussies. « Faux et sûr » et taux de
non-réponse (pas de `$`) parmi les faux, par jeu et longueur.

Prédictions (confirmées / infirmées, rien d'autre) :
- **P1** : chaque système atteint ≥ 95 % sur T-ID 2–5 (moyenne des graines de criblage).
- **P2** : A3-T (structure injectée) ≥ 50 % à VAL 8.
- **P3** : A3 (sans T(n)) < A3-T à VAL 8.
- **P4** : A1 < 50 % à VAL 8 (littérature : peu de runs réussis).
- **P5** : A2-L ≥ A2 à VAL 8.
- Question ouverte, **sans prédiction** : un des systèmes sans structure d'itération donnée
  (A2, A2-L, A3) dépasse-t-il B-REF de ≥ 10 points à L = 8 ?

## 8. Budget

≤ 4 h de calcul pour le mandat (plusieurs fenêtres partagent le GPU). Invocations
d'entraînement ≤ 9 min avec reprise sur checkpoint, au premier plan, aucune tâche de fond.
Si la projection après pilote dépasse 4 h : réduire S (figé par amendement avant les runs
officiels), puis le nombre de graines de confirmation, et l'écrire. Dépassement en cours de
route : publier le partiel.

## 9. STOP

Contrôle de validité en échec ; test final touché avant la fin ; envie de modifier ce document
(écrite en amendement ou au rapport, non appliquée) ; dépassement de budget.

## Amendement A1 — 2026-09-27T10:10:08+0200 (après pilote graine 0, avant tout run officiel et tout contrôle)

Pilote (graine 0, exclue) : vitesse mesurée sur M1 **partagé avec d'autres fenêtres**.
Largeur 128, non compilé : 0,85–1,2 s/pas (A1, A2, A3) → 6 000 pas ≈ 1 h 30 par run, budget
intenable (10 runs de criblage). Banc (8 pas, même lot) : largeur 64 + `mx.compile` →
A1 0,27 ; A2 0,15 ; A3 0,29 s/pas. Coût de l'évaluation finale mesuré sur des paires
synthétiques de 100 chiffres (pas le jeu TEST) : A3 ≈ 0,6 s/item (plafond 512 sur bande 404),
soit ≈ 9 min par run A3.

Changements (aucun ne dépend d'un résultat de validation ; VAL = 0 % partout au pilote) :
1. **S = 2 000 pas** (512 000 exemples, 1/6 d'E008) au lieu de 6 000 provisoires, pour tenir
   ≤ 4 h avec 10 runs de criblage, les évaluations au plafond 512 et le format standard.
2. **Largeur 64** au lieu de 128 pour toutes les familles (A3 : d = 64, FFN 256, 4 têtes).
   Paramètres : A1 76 047 ; A2 / A2-L 107 343 ; A3 / A3-T 51 791.
3. **Normalisation spectrale : 20 itérations de puissance** au lieu de 3 (mesuré : 5 itérations
   sous-estiment σ de ~9 % sur un poids initial, 20 de ~3 %).
4. **ELU sûre** dans A2-L : `nn.elu` de MLX calcule exp(z) sur la branche positive → inf →
   gradient NaN (reproduit au pas 65 du pilote ; vérifié : grad elu(200) = NaN). Même fonction,
   calcul borné.
5. `mx.compile` du pas d'optimisation ; les pas où n + k = M (chaîne progressive identique à la
   chaîne principale) font planter `mx.compile` 0.29.3 sur A3 (`unordered_map::at`) : ces pas
   sont exécutés sans compilation. Mathématiquement identique.
