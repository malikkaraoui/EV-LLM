# E008 — addition, palier 0 : préenregistrement

Mandat M0021, 2026-09-26, branche `exp/e008-addition` (depuis `origin/main` @ `677b928`).
Ce document est committé et poussé **avant toute ligne de code et toute exécution**. Toute
modification ultérieure est un amendement daté, en fin de fichier, jamais une réécriture.

But : (1) prouver que le test de généralisation en longueur est **juste** (leçon M0020 : un
critère doit d'abord être atteignable par un oracle) ; (2) mesurer où casse un transformer de
base (B-STD) et une référence « correctif connu, faible triche » (B-REF). **Aucun mécanisme
EV-LLM ici** : il viendra au palier 1, contre ces références.

## 1. Tâche et format

- Entrée `a+b=`, sortie : la somme `a+b`, puis un token de fin. Entiers positifs ou nuls
  (0 n'apparaît que comme opérande à 1 chiffre), écriture décimale sans zéro de tête.
- Vocabulaire caractère, **un token par chiffre** : `0`…`9` (ids 0–9), `+` (10), `=` (11),
  fin `$` (12), remplissage (13). 14 tokens.
- Séquence d'entraînement : `a₁…aₙ + b₁…bₘ = s… $`, remplissage à droite. La perte
  (entropie croisée) ne porte **que** sur les tokens de la réponse (chiffres de la somme et `$`).
- Sortie B-STD : somme écrite chiffre de poids fort d'abord (standard). Sortie B-REF : somme
  écrite **inversée** (poids faible d'abord) ; les opérandes restent en ordre standard dans les
  deux cas. L'évaluateur ré-inverse la sortie de B-REF avant comparaison (même critère pour tous).

## 2. Données

Longueur d'un opérande = nombre de chiffres. « Longueur L » d'un item de test = les **deux**
opérandes ont L chiffres.

Tirage d'un opérande de longueur ℓ : premier chiffre uniforme dans 1–9 (dans 0–9 si ℓ = 1),
autres chiffres uniformes dans 0–9.

- **Entraînement** : flux engendré à la volée, déterministe : le lot du pas t de la graine s est
  tiré par `numpy.random.default_rng([10_000 + s, t])`. Pour chaque exemple, ℓa et ℓb
  **indépendants et uniformes dans 1–5** (donc uniforme par longueur, pas par nombre), puis
  chiffres comme ci-dessus. Tout exemple dont la paire (a, b) **ou la paire échangée (b, a)**
  appartient à un jeu de test est rejeté puis tiré de nouveau (commutativité exclue elle aussi).
- **T-ID** (dans la distribution, disjoint) : L = 2, 3, 4, 5 ; 500 paires uniques par longueur,
  graine 2026, disjointes de l'entraînement **par construction** (exclusion ci-dessus) et
  **vérifiée par un test** (`unittest` qui rejoue les lots d'entraînement et vérifie qu'aucune
  paire de test n'y figure, dans les deux ordres, sur un échantillon de pas).
- **T-ID1** (non disjoint, contrôle de sanité) : L = 1, les 100 paires possibles. **Écart
  assumé au mandat** : le mandat demande T-ID sur 1–5 chiffres, disjoint, ≥ 500 par longueur ;
  à L = 1 il n'existe que 100 paires, toutes nécessairement vues à l'entraînement. T-ID1 est donc
  rapporté à part, jamais agrégé à T-ID, et exclu du critère C-PARCŒUR.
- **T-OOD** (hors distribution) : L = 6, 7, 8, 10, 12, 16 ; 500 paires uniques par longueur,
  graine 2027.
- **T-CARRY** (retenue en chaîne) : L = 2, 3, 4, 5, 6, 7, 8, 10, 12, 16 ; par longueur,
  500 paires uniques tirées pour que **chaque** position produise une retenue (chaîne de
  longueur L, somme à L + 1 chiffres) : position 0 avec aᵢ + bᵢ ≥ 10, positions suivantes avec
  aᵢ + bᵢ ≥ 9 (paire uniforme parmi les paires admissibles, chiffre de tête ≥ 1), graine 2028 ;
  plus 2 cas spéciaux `99…9 + 1` et `1 + 99…9` (L chiffres + 1 chiffre), rapportés dans le même
  tableau (502 items). Les T-CARRY de longueur 2–5 sont eux aussi exclus de l'entraînement.
- Longueur de chaîne de retenue d'un item = plus longue suite de positions consécutives qui
  émettent une retenue. Calculée pour tous les items de tous les jeux (analyse transversale).
- Tailles figées : 500 par longueur (T-ID, T-OOD), 502 (T-CARRY), 100 (T-ID1).

## 3. Systèmes

Tous passent par **le même évaluateur** (`evaluate.py`) : un système est une fonction
`(liste de (a, b)) → liste de (réponse canonique | None, confiance)`.

- **C-ORACLE** : addition avec retenue, chiffre par chiffre, codée à la main (pas `a + b` de
  Python), confiance 1. Prédiction : **100 % partout**.
- **C-PARCŒUR** : table de consultation des paires d'entraînement effectivement tirées (flux
  complet de la graine 1, tous pas) : réponse si la paire est dans la table, sinon `None`
  (faux). Prédiction : **0 %** sur T-ID et T-OOD (≤ 1 % exigé, §6).
- **B-STD** : transformer decoder-only, pré-normalisation (LayerNorm), attention causale,
  GELU, sans dropout. **d = 256, 4 couches, 4 têtes, FFN 1024**, embeddings de tokens non liés
  à la tête de sortie, **positions absolues apprises** (table de 64 positions, dont seules les
  ~19 premières sont vues à l'entraînement). ≈ 3,2 M paramètres (ordre 1–5 M demandé ;
  justification : taille comparable à Lee 2023, qui rapporte l'échec total hors longueur vue à
  10,6 M ; 4 couches suffisent à l'addition dans la distribution selon la littérature citée au
  mandat [HYPOTHÈSE]). Sortie standard.
- **B-REF** : **même modèle, même hyperparamètres, même flux de données**, sans aucun
  embedding de position (**NoPE** : seule l'attention causale porte l'ordre) et sortie inversée.
- Entraînement (valeurs **provisoires**, pouvant être figées autrement après pilote, §7) :
  AdamW (β = 0,9 / 0,98, weight decay 0,01), lr max 1e-3, montée linéaire 500 pas puis
  décroissance cosinus jusqu'à 1e-5, écrêtage de gradient 1,0, lot 256, **20 000 pas** (5,12 M
  exemples), float32. Même nombre de pas pour B-STD et B-REF.
- **Graines officielles : 1, 2, 3** pour chaque système appris (graine s = initialisation
  `mx.random.seed(s)` et flux de données `[10 000 + s, t]` : B-STD et B-REF de même graine voient
  exactement les mêmes exemples). Graine 0 = pilote, exclue des résultats.
- Décodage : glouton, au plus L_max + 2 tokens générés (L_max = plus longue opérande) ; une
  réponse sans `$` dans cette limite est fausse.

## 4. Mesures

- **Exact-match** : réponse entière identique à la somme (après ré-inversion pour B-REF), par
  jeu × longueur × système, moyenne ± écart-type sur les 3 graines (et valeurs par graine).
- **Par longueur de chaîne de retenue** : exact-match regroupé par longueur de chaîne
  (tous jeux confondus sauf T-ID1), par système.
- **Confiance** = produit des probabilités (softmax) des tokens générés en glouton, `$` inclus.
- **« Faux et sûr »** = réponse fausse avec confiance ≥ 0,8 ; rapporté en taux parmi les
  réponses fausses et parmi tous les items, par jeu × longueur.
- **Courbe d'efficacité** : aux pas 250, 500, 1 000, 2 000, 4 000, 8 000, 12 000, 16 000 et
  final (exemples vus = pas × 256), exact-match sur les **100 premiers** items de T-ID (L = 2–5)
  et de T-OOD (L = 6, 8). Exportée en CSV.

## 5. Prédictions chiffrées [HYPOTHÈSE, littérature]

- P1 — B-STD, T-ID (L = 2–5, moyenne des 3 graines) : **≥ 95 %** à chaque longueur.
- P2 — B-STD, T-OOD à 8 chiffres : **≤ 10 %** (attendu ≈ 0 : positions jamais entraînées).
- P3 — B-REF, T-ID : ≥ 95 % à chaque longueur.
- P4 — B-REF meilleur que B-STD hors distribution : exact-match moyen à **L = 6** de B-REF
  **≥ celui de B-STD + 10 points**. Pas de prédiction défendable au-delà de 6 chiffres ; je
  m'attends [HYPOTHÈSE] à ce que les deux soient près de 0 % à L ≥ 10.
- P5 — T-CARRY : dans la distribution (L = 2–5), exact-match plus bas que T-ID pour les deux
  modèles (sans seuil chiffré : pas de valeur défendable).
- « Faux et sûr » de B-STD hors distribution : **pas de prédiction** (aucune valeur défendable
  dans la littérature citée) ; mesuré seulement.

## 6. Validité du test — critère bloquant

Le test est déclaré **VALIDE** seulement si **C-ORACLE = 100 %** sur tous les items de tous les
jeux **ET C-PARCŒUR ≤ 1 %** sur T-ID (L = 2–5) et sur chaque longueur de T-OOD. Sinon :
rapport, STOP, **aucune lecture des modèles appris**. Les contrôles sont exécutés et publiés
avant la première lecture des résultats de B-STD / B-REF.

## 7. Budget temps et pilote

- Pilote autorisé sur la **graine 0 uniquement**, exclu des résultats : estimer la durée par
  pas et vérifier la convergence (T-ID). Toute valeur changée après pilote (pas, lr, lot) est
  notée « figée après pilote » dans un amendement daté, committé **avant** les exécutions
  officielles.
- Budget : **≤ 3 h de calcul** pour les 6 entraînements officiels (≈ 30 min chacun,
  évaluations de jalon comprises). Si le pilote montre qu'il faut plus, je réduis les pas (puis
  la taille) et je l'écris ; je ne dépasse pas.
- `train.py` reprend sur checkpoint (poids, état de l'optimiseur, pas) ; chaque invocation
  s'arrête d'elle-même après ≤ 9 min de calcul ; les invocations sont enchaînées au premier plan.

## 8. Règles de lecture

- Une prédiction est **confirmée** si le seuil est atteint en moyenne sur les 3 graines,
  **infirmée** sinon ; la dispersion entre graines est rapportée à côté, sans lissage.
- Aucune conclusion générale au-delà de : cette tâche, cette taille, ce budget, ce format.
- Toute envie de modifier ce document après exécution officielle est écrite dans le rapport,
  pas appliquée.
