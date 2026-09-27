# E014 — « repérage » : apprendre OÙ lire, puis composer avec l'accumulateur d'E013 — préenregistrement

Mandat M0028, 2026-09-27, branche `exp/e014-reperage` (depuis `origin/exp/e013-insecte` @
`3246ae8`). Ce document est committé et poussé **seul, avant toute ligne de code et toute
exécution**. Toute modification ultérieure est un amendement daté en fin de fichier, jamais une
réécriture.

## 1. Question

E013 : un accumulateur de 2 unités fait l'addition **exacte jusqu'à 1 000 chiffres** quand on lui
donne les chiffres **alignés, poids faible d'abord** (I1, 5/5 graines), mais échoue sur l'entrée
plate `a+b=` (I2, 0/5). E010 : avec un brouillon, chaque colonne est juste mais le modèle ne sait
plus quel chiffre lire ni quand s'arrêter. Hypothèse de travail : **le calcul est résolu, le verrou
est le repérage**. Deux questions :

- **Q1 (repérage)** : un mécanisme de lecture appris sur l'entrée plate généralise-t-il en longueur
  (curriculum ? pointeurs durs ?) ?
- **Q2 (transfert, « voiture → camion »)** : un module de lecture appris sur une tâche **sans
  addition** (poser l'opération en colonnes), branché **gelé** devant l'accumulateur I1 **gelé**
  d'E013, fait-il l'addition **sans aucun entraînement joint** ?

## 2. Données (réutilisées par import ; `E008-addition/` et `E013-insecte/` inchangés)

- Entrée plate de tous les systèmes : `DEBUT` + chaîne E008 `a+b=` (opérandes poids fort d'abord),
  `VIDE` à droite (`donnees.encode_plat` d'E013). Sortie : un chiffre par pas, poids faible
  d'abord, **max(ℓa, ℓb) + 1** pas, retrait d'un seul 0 de tête (`donnees.decode` d'E013).
- **Entraînement** : flux E008 (opérandes de longueurs indépendantes uniformes 1–5, lot du pas t de
  la graine s tiré par `default_rng([10 000 + s, t])`, paires des jeux de test E008 exclues),
  lot de 128 (`donnees.paires_flux` d'E013).
  **Flux curriculum** (R0b seulement) : même tirage (`e008.tire_nombre`, mêmes exclusions) mais
  longueurs uniformes dans 1–Lmax, `default_rng([40 000 + s, t])`, Lmax = 2, 3, 4, 5 sur quatre
  quarts égaux des pas.
- **VAL-OOD** (seul jeu autorisé pour choisir checkpoint et hyperparamètres) : deux opérandes de
  L = 6, 7, 8 chiffres, 500 paires uniques par L, **graine 3113** (≠ E013).
- **VAL-ID** (pilote seulement, contrôle d'apprentissage en distribution) : L = 2–5, 200 paires
  par L, graine 3119.
- **TEST final** (évalué **une seule fois**, à la fin, sur le checkpoint choisi par VAL-OOD) —
  mêmes générateurs qu'E013 (`_uniformes`, `_cascade`, `_zeros`, `_asym`), **graines nouvelles** :
  - **T-LONG** : L = 10, 16, 32, 64, 100 (500 paires, graine 3114) et L = 1 000 (200, graine 3115).
  - **T-ID** (E008, L = 2–5) : contrôle en distribution.
  - **ADV-CASCADE** (graine 3116), **ADV-ZEROS** (3117), **ADV-ASYM** (3118 ; L chiffres + 1–5
    chiffres, et `10…0 + 999`), L ∈ {10, 16, 32, 64, 100, 1 000}.
  Toutes les paires de VAL/TEST ont un opérande de ≥ 6 chiffres (sauf T-ID, exclu du flux par E008) :
  disjonction du flux par construction, vérifiée par un test.
- Critère : **exact-match de la réponse entière** via l'évaluateur E008 (`evaluate.evaluer` /
  `resume`) importé tel quel.

## 3. Systèmes et budget de structure (ce qui est donné à la main)

Commun à R0–R2 (donné) : vocabulaire (14 symboles, dont `+`, `=`, début, vide), sortie poids faible
d'abord, **nombre de pas** = max(ℓa, ℓb) + 1, retrait d'un 0 de tête, contrôleur = cellule d'E013
(couche locale F = 32, état H = 8), 2 têtes de lecture, décalages locaux {−1, 0, +1}, clés de
contenu sur un voisinage de 3. Aucun plongement de position, aucune adresse absolue.
**Non donné** : où commencent/finissent les opérandes, qu'il faut reculer, quand un opérande plus
court est épuisé, la retenue.

- **C-ORACLE** : `controles.addition_retenue` d'E008. Attendu 100 % partout.
- **C-PARCŒUR** : table des paires vues à l'entraînement par la graine 1 (flux E008 sur le plus
  grand nombre de pas utilisé + flux curriculum complet). Attendu **0 %** (≤ 1 % exigé) sur VAL et
  TEST hors T-ID ; **test non valide sinon**.
- **R0a — I2 d'E013 reproduit** (référence, attendu 0/5) : `modeles.I2` d'E013 importé tel quel,
  lr 3e-3, 12 000 pas (A1 d'E013), sans pilote.
- **R0b — I2 + curriculum de longueur** : même modèle, même nombre de pas, flux curriculum.
  Budget en plus : l'ordre des longueurs (donné).
- **R1 — lecture apprise seule, puis composée (transfert).**
  - (a) **Lecteur** : mêmes têtes de lecture qu'I2 (plongements D = 8, clés, pointeurs doux,
    décalages, affûtage γ), contrôleur = cellule E013 (H = 8) qui émet, à chaque pas, **la paire
    alignée** (aₜ, bₜ) (2 × 11 classes : 0–9 et « absent ») + les décalages. Entraîné par entropie
    croisée sur les cibles `encode_aligne` d'E013 (A, B), **jamais sur la somme** : aucune
    information d'addition dans sa perte. Checkpoint = meilleure **exactitude de lecture**
    (toutes les paires justes) sur VAL-OOD.
  - (b) **Composition gelée R1-gel** : lecteur de la graine s (gelé) → probabilités (11 + 11) →
    cellule de l'**I1 H = 4 d'E013, graine s** (gelée ; poids `meilleur.safetensors` copiés du run
    E013 avec leur sha256 dans `i1_e013/`), à la place de ses one-hot. **Aucun entraînement
    joint.** Évaluée telle quelle (c).
  - (d) **R1-joint** : ajustement joint court de la composition (tous les poids libres), perte
    d'addition, flux E008, **1 000 pas, lr 1e-3** (fixés ici, sans pilote), VAL-OOD tous les
    250 pas, pas 0 (= R1-gel) compris dans les candidats.
  - Budget en plus : **la tâche intermédiaire « poser en colonnes »** (le format aligné, le sens
    poids faible d'abord, le symbole « absent ») est donnée par la supervision du lecteur ; I1
    apporte en plus son budget E013 (alignement et sens donnés à son entraînement).
- **R2 — pointeurs relatifs durs** (interprétation du mandat, écrite ici) : I2 a déjà des décalages
  relatifs mais des pointeurs **doux** (distribution qui peut s'étaler au fil des pas). R2 garde
  exactement l'architecture I2 mais le pointeur est **un seul entier** à l'aller : position de
  départ = argmax de l'attention de contenu, puis à chaque pas **un** décalage −1/0/+1 (argmax) ;
  gradient par estimateur droit (straight-through : aller dur, retour doux). Appris de bout en bout
  avec l'accumulateur sur la perte d'addition, 12 000 pas. Budget en plus : pointeur discret.

## 4. Entraînement, sélection, graines

- Entropie croisée moyenne sur les pas émis, **sans L2**, Adam, écrêtage 1,0, float32, MLX, lot 128
  (identique à E013). VAL-OOD tous les 250 pas ; checkpoint = meilleur VAL-OOD (égalité : le plus
  tardif).
- **Pilote (graine 0, exclue)** : lr ∈ {3e-3, 1e-2} pour R0b (12 000 pas), R2 (12 000 pas) et le
  lecteur R1 (6 000 pas) ; choix sur VAL-OOD seul (égalité : 3e-3). Le pilote rapporte aussi
  **VAL-ID** : un système dont aucun réglage n'atteint 90 % en distribution est signalé « n'apprend
  pas en distribution » (on le lance quand même, sans autre réglage). Valeurs figées dans
  `hyperparametres.json`, committées avant tout run officiel.
- **Graines officielles 1–5** pour R0a, R0b, R1 (lecteur, gel, joint), R2.
- Journalisé par run : pas, exemples vus, **exemples uniques vus**, durée.
- **Réussite d'une graine** : exact-match ≥ 90 % sur T-LONG L = 16. Système « réussi » si ≥ 4/5
  graines. Rapporté : moyenne ± écart **et** graines ≥ 90 % à 16 / 100 / 1 000.

## 5. Autodiagnostic (leçon E010 : la confiance porte sur les étapes qui calculent)

- **Confiance** d'une réponse = **min sur les colonnes** de la probabilité du chiffre émis (p_min).
  C'est elle qui est passée à l'évaluateur E008 : « faux et sûr » = faux avec p_min ≥ 0,8. Le
  produit des probabilités (définition E013) est rapporté en second. Pour R1, on rapporte aussi la
  confiance du lecteur (min sur les pas de la probabilité des deux chiffres lus).
- **Abstention** : seuil τ par run, choisi sur VAL-OOD = le plus grand τ de
  {0,5 ; 0,6 ; 0,7 ; 0,8 ; 0,9 ; 0,95 ; 0,99} tel que ≤ 5 % des réponses **justes** de VAL-OOD
  aient p_min < τ. Rapporté sur TEST : taux d'abstention quand faux, quand juste.

## 6. Prédictions

- **P1** : R0a réussit sur ≤ 1/5 graines (reproduit E013).
- **P2** : R0b (curriculum) réussit sur ≤ 1/5 graines [pari : le curriculum ne suffit pas].
- **P3** : le lecteur R1 lit exactement (≥ 90 % de lectures entièrement justes) à L = 16 sur
  ≥ 3/5 graines [pari].
- **P4 (transfert)** : pour chaque graine, l'exact-match d'addition de R1-gel à chaque L de T-LONG
  est ≥ l'exactitude de lecture du lecteur au même L moins 2 points (I1 ne perd rien sur des
  lectures justes) : **la composition marche exactement quand la lecture marche**.
- **P5** : R1-joint ne fait pas moins bien que R1-gel de plus de 5 points à L = 100 (moyenne).
- **P6** : R2 a strictement plus de graines réussies que R0a.
- **P7** : pour chaque système ayant ≥ 20 erreurs sur TEST, la p_min médiane des faux est inférieure
  à celle des justes.

## 7. Budget et ordre

≤ 4 h de calcul (GPU partagé avec F01, prioritaire) ; invocations ≤ 9 min avec reprise sur
checkpoint, aucune tâche de fond. Si le partage ralentit trop : réduction dans cet ordre, écrite au
README — (1) pilote réduit à lr 3e-3 seul, (2) pas divisés par 2 ; jamais moins de 5 graines
officielles (sinon aucune réussite déclarée). Ordre des
commits : préenregistrement (poussé seul) < code < valeurs figées après pilote < contrôles <
résultats.

## Amendement A1 — 2026-09-27, valeurs figées après pilote (avant tout run officiel)

Pilote graine 0, VAL-OOD seul pour le choix (TEST non lu) ; VAL-ID en contrôle
(`resultats/pilote.json`, `pilote14.py`) :

| système | lr 3e-3 : VAL-OOD / VAL-ID | lr 1e-2 : VAL-OOD / VAL-ID | retenu |
|---|---|---|---|
| R0b (12 000 pas) | **1,000** / 1,000 | 0,757 / 0,871 | 3e-3 |
| R1L lecture (6 000 pas) | **1,000** / 1,000 | 1,000 / 1,000 | 3e-3 (égalité → règle §4) |
| R2 (12 000 pas) | **1,000** / 1,000 | 0,891 / 0,940 | 3e-3 |

Tous apprennent en distribution (VAL-ID = 1,000 au réglage retenu). Valeurs figées dans
`hyperparametres.json` : R0a, R0b, R2 : lr 3e-3, 12 000 pas ; R1L : lr 3e-3, 6 000 pas ; R1J :
lr 1e-3, 1 000 pas (fixé au §3). Durée pilote ≈ 21 min (M1 partagé). Aucune réduction.

Limite constatée, **écrite avant les runs officiels** : VAL-OOD (6–8 chiffres) est saturé
(1,000) pour les trois systèmes au réglage retenu, comme pour I2 d'E013 au pilote (0,997), qui a
ensuite échoué à 16 chiffres. VAL-OOD ne discrimine donc plus : le checkpoint retenu sera
souvent le plus tardif (règle d'égalité du §4). On ne change pas la règle (préenregistrée) ; le
TEST reste le seul juge de la généralisation.
