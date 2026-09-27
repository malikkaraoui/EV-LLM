# E013 — « insecte » : un accumulateur minuscule apprend-il l'addition à toute longueur ? — préenregistrement

Mandat M0026, 2026-09-27, branche `exp/e013-insecte` (depuis `origin/exp/e008-addition` @
`af281f5`). Ce document est committé et poussé **seul, avant toute ligne de code et toute
exécution**. Toute modification ultérieure est un amendement daté en fin de fichier, jamais une
réécriture.

## 0. Inspiration (référence vérifiée)

Stone T., Webb B., Adden A., … Heinze S. (2017), « An Anatomically Constrained Model for Path
Integration in the Bee Brain », *Current Biology* 27 : 3069–3085,
doi:10.1016/j.cub.2017.08.052 — copie auteur :
<https://www.pure.ed.ac.uk/ws/files/44821394/Stone_Path_Integration_2.pdf>. Extraits (texte de la
copie auteur, collé tel quel) :

> « Path integration is a widespread navigational strategy in which directional changes and
> distance covered are continuously integrated on an outward journey, enabling a straight-line
> return to home. »
>
> « […] by continuously integrating the speed information from optic flow in proportion to the
> input from TB1-neurons, these units could encode the distance travelled in each compass
> direction » (à propos des neurones CPU4, dont le rôle de mémoire est dit « purely speculative »
> par les auteurs).

[VÉRIFIÉ] La référence existe et dit bien : un petit circuit identifié du complexe central,
une mémoire (CPU4) mise à jour en continu à chaque pas. [HYPOTHÈSE] L'analogie avec la retenue
d'une addition est la nôtre, pas celle des auteurs (eux intègrent des vecteurs continus, pas des
chiffres). On teste le **principe** : un état minuscule, mis à jour localement à chaque pas.

## 1. Question

Un réseau récurrent dont l'**état transmis d'un pas à l'autre fait 1 à 8 nombres** apprend-il,
à partir d'additions de 1 à 5 chiffres, une règle qui reste **exacte à 10, 16, 32, 64, 100 et
1 000 chiffres** ? Combien d'exemples uniques lui faut-il ? Et sans l'alignement donné à la main ?

## 2. Données (réutilisées d'E008 par import, `research/experiments/E008-addition/` inchangé)

- **Entraînement** : flux E008 (`data.paires_du_pas`) : longueurs d'opérandes indépendantes et
  uniformes dans 1–5, lot du pas t de la graine s tiré par `default_rng([10 000 + s, t])`, paires
  des jeux de test E008 (et leurs échangées) exclues. Lot de **128** (au lieu de 256 en E008).
- **VAL-OOD** (seul jeu autorisé pour choisir checkpoint et hyperparamètres) : les deux opérandes
  ont L = 6, 7, 8 chiffres, 500 paires uniques par L, graine 3013 (nouvelle, ≠ T-OOD d'E008).
- **TEST final** (évalué **une seule fois**, à la fin, sur le checkpoint choisi par VAL-OOD) :
  - **T-LONG** : les deux opérandes ont L = 10, 16, 32, 64, 100 chiffres (500 paires par L,
    graine 3014) et L = 1 000 (200 paires, graine 3015).
  - **T-ID** (E008, L = 2–5, 500 par L) : contrôle d'apprentissage dans la distribution.
  - **ADV-CASCADE** (retenues en cascade), L ∈ {10, 16, 32, 64, 100, 1 000} : `99…9 + 1`,
    `1 + 99…9`, `99…9 + 99…9`, plus 100 paires où **chaque** position émet une retenue
    (générateur E008 `_paire_toute_retenue`, graine 3016).
  - **ADV-ZEROS** (nombres pleins de zéros), mêmes L : `10…02 + 10…03`, plus 100 paires dont le
    premier chiffre est 1 et chaque autre chiffre est non nul avec probabilité 0,1 (graine 3017).
  - **ADV-ASYM** (longueurs asymétriques), mêmes L : `10…0 (L chiffres) + 999`, plus 100 paires
    (L chiffres + 1–5 chiffres, ordre tiré au hasard), graine 3018.
- Critère : **exact-match de la réponse entière** (`str(a + b)`), via l'évaluateur E008
  (`evaluate.evaluer` / `resume`) importé tel quel ; confiance = produit des probabilités des
  chiffres émis ; « faux et sûr » = faux avec confiance ≥ 0,8.

## 3. Systèmes et budget de structure (ce qui est donné à la main)

- **C-ORACLE** : `controles.addition_retenue` d'E008 (retenue codée à la main). Attendu 100 %
  partout.
- **C-PARCŒUR** : table des paires effectivement vues par I1 (graine 1, flux complet) ; réponse
  si la paire est dans la table, sinon rien. Attendu **0 %** sur VAL-OOD et TEST (≤ 1 % exigé) ;
  **test non valide sinon**.
- **I1 — accumulateur minimal aligné.** À chaque pas t (t = 0 : chiffre de poids faible), il
  lit la **paire alignée** (aₜ, bₜ), chaque chiffre codé en one-hot sur 11 valeurs (0–9 et
  « absent » quand l'opérande est plus court), et son état hₜ₋₁ ∈ ℝᴴ (h₋₁ = 0). Une couche
  cachée locale z = ReLU(W₁[xₜ ; hₜ₋₁] + b₁) de largeur **F = 32** calcule le nouvel état
  hₜ = tanh(W_h z + b_h) et le chiffre émis (softmax sur 10). Tailles **H ∈ {1, 2, 4, 8}**.
  Il fait **max(ℓa, ℓb) + 1** pas ; la réponse est lue poids fort d'abord et, si le dernier
  chiffre émis (la retenue finale) est 0, ce seul 0 est retiré.
  **Budget de structure I1** : alignement des chiffres de même rang (donné), sens poids faible →
  poids fort (donné), nombre de pas = max(ℓa, ℓb) + 1 (donné), retrait d'un seul 0 de tête
  (donné), symbole « absent » distinct de 0 (donné : le réseau doit apprendre qu'il vaut 0),
  couche locale F = 32 identique à chaque pas (donné : localité et partage des poids).
  **Non donné** : la notion de retenue, sa valeur, la table d'addition, où la stocker.
- **I2 — même accumulateur, entrée plate.** Il reçoit la chaîne E008 `a+b=` (opérandes poids
  fort d'abord) précédée d'un symbole de début, et doit **trouver lui-même** les chiffres à lire.
  Deux têtes de lecture (pointeurs doux) : position initiale par attention de contenu
  (clés = convolution de largeur 3 sur des plongements appris de dimension 8, requête apprise
  par tête), puis à chaque pas un décalage appris ∈ {−1, 0, +1} émis par le contrôleur (poids
  softmax), suivi d'un affûtage p^γ appris (γ ≥ 1) ; la masse qui sort à gauche reste sur le
  symbole de début. Contrôleur = la cellule de I1 (F = 32, H = 8) qui lit les deux vecteurs lus
  au lieu des one-hot. Même nombre de pas et même lecture de sortie que I1.
  **Budget de structure I2** : sens de sortie poids faible d'abord (donné), nombre de pas
  (donné), 2 têtes, décalages locaux {−1, 0, +1}, voisinage de 3 pour les clés (donnés).
  **Non donné** : où commencent les opérandes, qu'il faut reculer, quand s'arrêter à un
  opérande plus court. **Attendu difficile** (prédiction P4).
- **I3 — efficacité.** I1 à H = 4 entraîné sur un jeu **fixe** de N = 10, 100, 1 000, 10 000
  paires **uniques** (les N premières paires distinctes du flux E008 de la graine s ; lots de
  min(128, N) tirés uniformément dans ce jeu). Même nombre de pas que I1.

## 4. Entraînement, sélection, graines

- Entropie croisée moyenne sur les chiffres émis (pas t ≤ max(ℓa, ℓb)), **sans L2** (weight
  decay 0 : leçon E011), Adam, écrêtage de gradient 1,0, float32, MLX 0.29.3, lot 128.
- Valeurs **provisoires**, figées après pilote : **lr ∈ {3e-3, 1e-2}** (constant) et **pas
  ∈ {3 000, 6 000}** pour I1/I3 ; I2 : même lr, 2 × les pas de I1. Le pilote (**graine 0**,
  exclue des résultats) choisit lr et pas **sur VAL-OOD uniquement**, pour I1 H = 4 et I2.
  Les valeurs figées sont committées dans `hyperparametres.json` avant tout run officiel.
- Évaluation VAL-OOD tous les 250 pas ; **checkpoint retenu = meilleur exact-match moyen
  VAL-OOD** (égalité : le plus tardif). TEST jamais lu avant la fin des runs officiels.
- **Graines officielles 1–5** pour chaque configuration (I1 × 4 tailles, I2, I3 × 4 valeurs de N).
- Journalisé par run : pas d'optimisation, exemples vus, **exemples uniques vus**, durée.
- Critère de **réussite d'une graine** : exact-match ≥ 90 % sur T-LONG L = 16. Une configuration
  est « réussie » si ≥ 4/5 graines réussissent. Rapporté : moyenne ± écart **et** nombre de
  graines réussies, par L jusqu'à 1 000.

## 5. Prédictions

- **P1** : au moins une taille de I1 est réussie (≥ 4/5 graines ≥ 90 % à L = 16).
- **P2** : I1 H = 1 réussit sur ≥ 3/5 graines (la retenue tient en 1 bit).
- **P3** : toute graine de I1 réussie à L = 16 reste ≥ 90 % à L = 1 000.
- **P4** : I2 réussit sur ≤ 1/5 graines.
- **P5** : I3 : N = 10 → 0/5 graine réussie ; N = 10 000 → ≥ 4/5. Le seuil N intermédiaire
  n'est pas prédit.
- **P6** (autodiagnostic) : sur ADV-CASCADE, si I1 a des erreurs, la confiance médiane de ses
  erreurs est inférieure à celle de ses réussites. I1 ne s'abstient jamais (pas de mécanisme
  d'abstention) : le taux d'abstention est donc 0 par construction, rapporté comme tel.

## 6. Inspection du circuit

Pour chaque graine réussie de I1 : corrélation de chaque unité de hₜ avec la vraie retenue
sortante du pas t (sur T-LONG L = 100) ; unité « porteuse » = |corrélation| maximale ; marge de
séparation (écart entre les valeurs de l'unité pour retenue 0 et 1, minimum sur tous les pas).

## 7. Budget et ordre

≤ 4 h de calcul (GPU partagé avec d'autres fenêtres) ; invocations ≤ 9 min avec reprise ; si
nécessaire, réduction des pas ou des variantes, écrite au README. Ordre des commits :
préenregistrement (poussé seul) < code < valeurs figées après pilote < résultats.

## Amendement A1 — 2026-09-27, valeurs figées après pilote (avant tout run officiel)

Pilote graine 0, VAL-OOD seul (TEST non lu), meilleur exact-match moyen VAL-OOD 6–8 :

| config | lr 3e-3, 3 000 pas | lr 3e-3, 6 000 pas | lr 1e-2, 3 000 pas | lr 1e-2, 6 000 pas |
|---|---|---|---|---|
| I1 H = 4 | 1,000 | 1,000 | 1,000 | 1,000 |
| I2 (2 × pas) | 0,833 | **0,997** | 0,977 | 0,993 |

Le §4 lie lr et pas de I1 et I2 (« même lr, 2 × les pas ») : I1 est à égalité partout, le
couple est donc départagé par I2 → **lr = 3e-3, 6 000 pas (I1, I3), 12 000 pas (I2)**
(`hyperparametres.json`). Règle d'égalité non écrite au §4, ajoutée ici avant les runs
officiels. Durées pilote : I1 ≈ 34 s, I2 ≈ 106 s par run (M1, GPU partagé) : budget 4 h large,
aucune réduction de variantes.
