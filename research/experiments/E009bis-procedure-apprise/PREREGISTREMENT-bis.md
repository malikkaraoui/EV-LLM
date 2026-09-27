# E009-bis — refaire A avec un budget où l'on apprend au moins la distribution : préenregistrement

Mandat M0027, 2026-09-27, branche `exp/e009bis-procedure-apprise` (depuis
`origin/exp/e009-procedure-apprise` @ `20f289b`). Correctif de M0022 (E009 : 5 systèmes × 2
graines à 0 % **même dans la distribution**, T-ID ≤ 3 % → question « l'architecture suffit-elle ? »
**non mesurée**). Ce document est committé et poussé **seul, avant toute ligne de code et toute
exécution**. Toute modification ultérieure est un amendement daté en fin de fichier, jamais une
réécriture. Les résultats E009 (M0022) restent tels quels ; `E009-procedure-apprise/` et
`E008-addition/` ne sont pas modifiés (réutilisés par import).

**Question.** Inchangée (E009 § préambule) : des biais d'architecture seuls (récurrence, localité,
calcul proportionnel à la taille, arrêt appris) suffisent-ils pour apprendre l'addition sur 1–5
chiffres et la généraliser à toute longueur, sans alignement donné ? **Nouveau : on sépare
nettement « n'apprend pas la distribution » de « apprend mais ne généralise pas ».**

## 1. Ce qui est réutilisé tel quel (E009, lui-même bâti sur E008)

- Bande de calcul, format d'entrée plat `a+b=` + n cases réponse, format de sortie **inversé**
  (seul format de ce mandat), décodage et confiance (`bande.py`, E009 § 2).
- Architectures et règles d'arrêt (`archis.py`, `boucle.py`, E009 § 3) : A1 Neural GPU
  (T = longueur de bande), A2-L Deep Thinking + normalisation spectrale (20 itérations de
  puissance) + ELU sûre, perte progressive M = 24, arrêt par confiance maximale au test (plafond
  C = 512) ; A3 Looped NoPE, même perte progressive, arrêt par confiance ; A3-T (T(n) donné).
  Seuls la **largeur** et le **taux d'apprentissage** changent (§ 3) ; aucune autre modification
  d'architecture.
- Évaluateur unique E008 (`evaluer` / `resume`), jeux VAL (6–8, 300 / L), TEST (10, 16, 32, 64,
  100 ; 200 / L), ADV-RET, ADV-ZERO, ADV-ASYM, T-ID (2–5, 200 / L), T-ID1, contrôles C-ORACLE et
  C-PARCŒUR (`verifie.py`), mêmes graines de jeux. « Faux et sûr » = faux avec confiance ≥ 0,8 ;
  non-réponse (pas de `$`) = abstention, taux parmi les faux rapporté.
- Optimiseur E009 : AdamW, β = (0,9 ; 0,98), wd 0,01, écrêtage 1,0, lot 256, float32, montée
  linéaire 500 pas puis cosinus jusqu'à 1e-5, **calculé sur le plafond de pas** (§ 2).

## 2. Nouveau : critère préalable « apprend la distribution », budget adaptatif, curriculum

1. **Curriculum de longueur** (pédagogie, inscrit au budget de structure) : niveau courant
   ℓ ∈ {2, 3, 4, 5}, départ ℓ = 2. Le lot du pas t de la graine s est tiré par
   `default_rng([10 000 + s, t])` exactement comme le flux E008, **mais longueurs d'opérandes
   indépendantes uniformes dans 1…ℓ** (mêmes exclusions des paires de test E008). À ℓ = 5 le flux
   est **identique** à celui d'E008/E009 (test unitaire). Contrôle du curriculum tous les
   **500 pas** : « T-ID courant » = moyenne exact-match sur T-ID aux longueurs 2…ℓ (100 premiers
   items par L) ; si ≥ 90 %, ℓ ← ℓ + 1 (un niveau au plus par contrôle). Les passages de niveau
   (pas, ℓ) sont journalisés et suffisent à reconstruire le flux (reprise, exemples uniques).
2. **Critère d'arrêt « apprend la distribution »** : tous les **1 000 pas**, si ℓ = 5, T-ID
   complet (200 / L, L = 2–5) ; si la **moyenne ≥ 95 %**, l'entraînement s'arrête et ce
   checkpoint est **le** checkpoint du run (aucun autre choix). Rapporté : pas atteint, exemples
   vus, exemples uniques vus, T-ID par L.
3. **Plafond : 20 000 pas par run.** Échec au plafond = « **n'apprend pas la distribution à ce
   budget** » (écrit tel quel) ; le run n'est alors **pas** évalué hors distribution (ni VAL, ni
   TEST, ni ADV) : on rapporte T-ID, niveau ℓ atteint et perte. Si la vitesse mesurée au pilote
   rend 20 000 pas intenables dans le budget (§ 6), le plafond est réduit **par amendement avant
   tout run officiel**, identique pour tous les systèmes, et écrit.
4. Règles d'arrêt utilisées pendant les contrôles T-ID : celles du test (A1 : T = 2n ; A2-L, A3 :
   confiance max, plafond 512 ; A3-T : T(n)).

## 3. Pilote de faisabilité (graine 0, exclue de tout résultat)

Pour chaque système piloté (A1, A2-L, A3 ; A3-T reprend les hyperparamètres de A3), configurations
(largeur w, lr max) :
- C1 = (64, 1e-3) ; C2 = (128, 1e-3) ; C3 = (128, 3e-4) ;
- C4 = (256, meilleur lr de C2/C3) **seulement si** le meilleur de C2/C3 bat strictement C1 au
  critère ci-dessous, et seulement si 2 000 pas à w = 256 tiennent en ≤ 12 min (vitesse mesurée
  sur 20 pas), sinon non lancé (écrit).
- A3 : d = w, 4 têtes, FFN 4w. A1 / A2-L : w canaux partout (tête A2-L : w, w/2, VOCAB).

Chaque configuration : **2 000 pas** de la procédure complète (§ 2 : curriculum, contrôles,
plafond 20 000 pour le calendrier de lr) avec la graine 0. À 2 000 pas, mesure : niveau ℓ atteint,
T-ID (2–5, 100 / L), VAL (6–8, 100 / L), perte, s/pas. **Critère de choix, lexicographique** :
(1) ℓ atteint ; (2) moyenne T-ID 2–5 ; (3) moyenne VAL 6–8 ; (4) largeur la plus petite (coût).
**Seuls T-ID et VAL servent à choisir** (jamais TEST/ADV, fermés). Le pilote vérifie donc
l'apprentissage **dans** la distribution, pas seulement la vitesse (leçon M0022). Le choix, les
vitesses et le plafond sont figés par un **commit daté avant les runs officiels** (amendement B1).

## 4. Déroulé officiel (graines 1–5) et ordre de priorité

1. Contrôles de validité (C-ORACLE = 100 %, C-PARCŒUR ≤ 1 % sur tous les jeux ; positif T-ID1 =
   100 %), avant tout modèle officiel. La table C-PARCŒUR est celle du flux de la graine 1 **avec
   curriculum reconstruit**, sur le nombre de pas du plus long run officiel (recalculé en fin).
   Échec = STOP.
2. Runs, dans cet ordre, tant que le budget le permet : A1 s1, A2-L s1, A3 s1 ; puis s2 des
   systèmes dont s1 a appris la distribution ; puis s2 des autres ; puis A3-T s1 (référence
   « structure injectée ») si le budget le permet.
3. Pour chaque run qui apprend la distribution : VAL complète (300 / L) + T-ID au checkpoint.
4. **Confirmation** : tout système dont la moyenne de ses graines ≥ 50 % à VAL 8 passe à 5
   graines (3, 4, 5 ajoutées). Si le budget ne le permet pas : partiel publié, écrit.
5. **Test final** (TEST + ADV-*) : **une seule fois, à la fin**, pour les runs ayant appris la
   distribution (verrou `resultats/FINAL_OUVERT`, refus d'une 2ᵉ évaluation).

Critères : exact-match séquence entière ; graine réussie = ≥ 90 % à TEST 16 ; système « réussi »
seulement avec 5 graines et ≥ 3 réussies ; moyenne ± écart-type **et** nombre de graines réussies.

## 5. Prédictions (confirmées / infirmées, rien d'autre)

- **Q1** : au moins un des trois systèmes (A1, A2-L, A3) apprend la distribution (T-ID ≥ 95 %)
  en ≤ 20 000 pas sur la graine 1.
- **Q2** : A1 (itérations = longueur, donné) apprend la distribution en moins de pas que A3.
- **Q3** : aucun système ayant appris la distribution n'atteint ≥ 90 % à TEST 16 (graine réussie).
- Sans prédiction : parmi les systèmes qui apprennent, VAL 8 dépasse-t-elle B-REF (0,1 %) de
  ≥ 10 points ?

## 6. Budget de calcul

≤ **5 h** de calcul au total (GPU prioritaire pour ce mandat), pilote compris (pilote ≤ 80 min).
Invocations d'entraînement ≤ 9 min, au premier plan, reprise sur checkpoint, aucune tâche de fond,
aucun `sleep`. Un système qui n'apprend pas au plafond est arrêté et on passe au suivant.
Dépassement : partiel publié.

## 7. Budget de structure (ce qui est donné à la main)

| système | format | localité | itérations | traces | pédagogie |
|---|---|---|---|---|---|
| A1 | bande 2n, réponse inversée à droite de `=` | conv k = 3 | **T = longueur de bande, donné** | aucune | curriculum 2→5 |
| A2-L | idem | conv k = 3 + Lipschitz (SN) | M = 24 fixe à l'entraînement ; test ≤ 512, arrêt appris (confiance) | aucune | curriculum 2→5 |
| A3 | idem | aucune (attention causale NoPE) | idem A2-L | aucune | curriculum 2→5 |
| A3-T | idem | idem A3 | **T(n) = max(ℓa, ℓb) + 1, donné** | aucune | curriculum 2→5 |

Commun : longueur de la bande réponse (n cases) et emplacement (après `=`) donnés ; `$` appris ;
aucun alignement, aucun opérande inversé, aucun index de position. Le curriculum ne donne aucune
information sur la procédure, seulement l'ordre des exemples (tirés du même générateur).

## 8. STOP

Contrôle de validité en échec ; test final touché avant la fin ; envie de modifier ce document
après un run officiel (écrite, non appliquée) ; dépassement de budget (partiel publié).
