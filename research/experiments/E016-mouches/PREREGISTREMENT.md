# E016 — « mouches » : préenregistrement (avant tout code)

Mandat M0031, 2026-09-27, branche `exp/e016-mouches` (depuis `exp/e014-reperage` @ `fc698b4`).
Code E008, E013, E014 **importé, non modifié**. Ce document est poussé seul, avant le code.

## 0. Veille (≈ 10 min, web) et en quoi E016 diffère

1. Jeux de signalisation de Lewis → communication émergente neuronale : Foerster 2016 (RIAL/DIAL),
   Lazaridou 2017 (jeux référentiels, REINFORCE), Mordatch & Abbeel 2018 (Gumbel) : agents **vierges**,
   langage inventé de zéro, tâche = désigner un objet.
2. Populations : Tieleman 2019, Graesser 2019, Rita 2022 (arXiv 2204.12982, hétérogénéité des
   vitesses d'apprentissage) ; Michel et al. (limiter la co-adaptation par paire) — idiolectes vs
   langue partagée, mais perception identique entre agents.
3. **Déjà fait, contrairement à l'hypothèse de l'orchestrateur** [VÉRIFIÉ, veille] : Mahaut, Dessì,
   Franzon, Baroni (arXiv 2302.08913, TMLR 2025) font communiquer des réseaux visuels
   **pré-entraînés, gelés, hétérogènes** (représentations privées incompatibles) : un protocole
   commun émerge et un **nouveau venu l'apprend facilement**. Voir aussi arXiv 2605.11695 (agents
   visuels hétérogènes, apprentissage décentralisé). « Agents à codes privés incompatibles » n'est
   donc **pas** nouveau en soi.
4. Ce qu'E016 teste et que la veille ne montre pas [HYPOTHÈSE, veille courte] : (a) les compétences
   gelées sont **procédurales et séquentielles** (lecture en colonnes / addition avec retenue), le
   canal porte l'état intermédiaire d'un **calcul coupé en deux**, appris sur 1–5 chiffres et jugé
   sur **16 à 1 000 chiffres** (généralisation en longueur d'un protocole émergent) ; (b) la
   récompense est **uniquement le succès** (REINFORCE, aucun gradient à travers le partenaire), et
   la règle de Malik **tout-ou-rien collectif + tout le monde recommence** est comparée à une
   récompense individuelle — la littérature attribue la récompense par paire ou par équipe, pas
   avec remise en jeu collective de l'échec.
5. Point de méthode, écrit d'avance [VÉRIFIÉ par construction] : un code privé **bijectif** fixé
   (permutation) est, pour un émetteur ou récepteur **tabulaire**, un simple renommage : il ne rend
   pas la tâche plus dure. Ce qu'il garantit : **aucune convention n'est partagée au départ** et
   aucun agent ne peut « recopier l'indice » d'un autre. La question réelle est donc : **une
   convention unique** émerge-t-elle entre 3 émetteurs et 3 récepteurs hétérogènes, ou des
   dialectes par paire (synonymie), et la règle collective y aide-t-elle ?

## 1. Agents (fixés)

- **A1, A2, A3 (« savent poser en colonnes »)** : lecteurs E014 `R1L-s1`, `R1L-s3`, `R1L-s4` gelés
  (lecture exacte 100 % à 100 chiffres dans E014 ; `lecteurs_e014/`, `SHA256SUMS` ; poids copiés du
  worktree E014, non versionnés là-bas). Sortie native à chaque pas t : la classe lue (argmax,
  0–9 ou « absent ») pour a_t et b_t, **ré-étiquetée par la permutation privée π_i** (11 classes).
- **B1, B2, B3 (« savent additionner des colonnes »)** : I1 H = 4 d'E013 graines 1, 2, 3 gelés
  (`E014-reperage/i1_e013/`). Entrée native : un jeton privé (11 classes) par opérande, qui passe par
  **σ_j⁻¹** avant la cellule I1 (B_j ne comprend que son propre code).
- π_i, σ_j : permutations aléatoires tirées par graine (rng 16 000 + graine), toutes distinctes.
- **Nouveaux venus (exploratoire, §6)** : A4 = lecteur `R1L-s2`, B4 = I1 H = 4 graine 4.

## 2. Canal et parties apprises

- Canal de **V = 48 symboles** sans signification préassignée (≥ 3 × 11 : trois dialectes disjoints
  sont possibles, la langue commune n'est **pas** forcée par la pénurie de symboles).
- À chaque colonne t, l'émetteur de A_i écrit **2 symboles** (un pour son jeton de a_t, un pour
  celui de b_t) ; le récepteur de B_j lit ces 2 symboles et choisit 2 jetons de son code privé.
- Émetteur A_i : table E_i (11 × 48) de logits ; récepteur B_j : table R_j (48 × 11). **Seules ces
  tables apprennent** ; lecteurs et I1 gelés. Entraînement : symboles et jetons **échantillonnés** ;
  évaluation : argmax partout (déterministe).
- Apprentissage : **REINFORCE** (récompense ∈ {0, 1}), ligne de base = moyenne de la récompense du
  lot par longueur de problème (n_pas), bonus d'entropie β, Adam. Aucun gradient ne traverse I1, le
  lecteur ou le partenaire.

**Budget de structure (donné à la main, rien de caché)** : la découpe du calcul (A lit, B calcule),
le nombre de pas (celui du lecteur E014 : max(ℓa, ℓb) + 1), la synchronisation colonne par colonne
(1 message = 2 symboles par colonne), le même lexique pour les deux emplacements a/b d'un agent
(la « compositionnalité » par colonne est donc **imposée**, pas émergente), la taille V. Plus le
budget d'E014 (lecteur : tâche « poser en colonnes » supervisée) et d'E013 (I1 : alignement donné).
**Non donné** : quel symbole veut dire quoi, ni qu'il faut une convention commune.

## 3. Règles de récompense (le cœur de l'idée de Malik)

Un lot = 128 **tours**. Une paire = (A_i, B_j) ; A_i lit la phrase brute `a+b=`, parle, B_j répond ;
la réponse est jugée exact-match (évaluateur/décodage E008/E013).

- **Phase 1 « à tour de rôle »** (première moitié des pas) : un tour = **1 paire tirée au hasard**
  (i, j uniformes), 1 problème.
- **Phase 2 « en équipe »** (seconde moitié) : un tour = **3 paires** formées par un appariement
  parfait aléatoire A↔B (redessiné à chaque tour), 3 problèmes distincts.
- **COLL (règle de Malik)** : récompense de **tous** les agents du tour = 1 si **toutes** les
  réponses du tour sont exactes, 0 sinon (tout-ou-rien collectif). **Tout le monde recommence** :
  un tour échoué est **rejoué** au pas suivant avec les **mêmes problèmes** et un **nouveau tirage**
  des paires / de l'appariement, jusqu'à 4 tentatives au total ; ensuite problèmes neufs. Les tours
  rejoués prennent leur place dans le lot de 128, complété par des tours neufs.
- **IND (témoin a)** : mêmes phases, mêmes tirages ; récompense **par paire** (sa propre réponse),
  **aucun rejeu**.
- **COUPÉ (témoin b)** : COLL, mais le récepteur reçoit toujours le symbole 0 (canal coupé).
  Doit échouer.
- **DONNÉ (témoin c, référence haute, sans apprentissage)** : l'interface exacte
  σ_j ∘ π_i⁻¹ (= E014 R1G en interface dure), pour les 9 paires.

Problèmes d'entraînement : flux E008/E013 `paires_flux(graine, k)` (1–5 chiffres, exclusions E008),
k = 3·pas + r (r = 0, 1, 2) pour les tours neufs. Journal : nombre de problèmes **uniques** vus.

## 4. Données, sélection, test

- VAL-OOD 6–8 chiffres (E014, graine 3113) : **seul** juge du checkpoint et des hyperparamètres ;
  critère = exact-match moyen sur les **9 paires** (argmax). Éval tous les 250 pas, meilleur
  checkpoint (égalité : le plus tardif).
- TEST lu **une seule fois** à la fin : jeux E014 identiques (T-ID 2–5, T-LONG 10/16/32/64/100 et
  1 000, ADV-CASCADE / ADV-ZEROS / ADV-ASYM à 10–1 000, graines 3114–3118), sur les **9 paires**.
- C-ORACLE = 100 % et C-PARCŒUR = 0 % recalculés sur VAL-OOD + TEST avec la table des problèmes vus
  par la graine 1 (COLL) : TEST VALIDE sinon rien n'est lu.
- 5 graines officielles (1–5) par condition COLL, IND, COUPÉ ; pilote graine 0 exclu.

## 5. Mesures et critères

- **Graine réussie** : les **9 paires** ≥ 90 % exact à 16 chiffres. **Condition réussie** : ≥ 4/5.
  Rapportés aussi : moyenne ± écart par L, matrice 3 × 3 des paires à 16 et 100 chiffres.
- **Langue commune ?** Lexique argmax : pour chaque sens (0–9, absent), les symboles émis par
  A1–A3. Indice **C** = nombre de sens (sur 11) où les 3 A émettent le **même** symbole.
  Verdict par graine : **commune** (C = 11 et 9 paires réussies) ; **synonymie** (9 paires réussies,
  C < 11 : les B comprennent plusieurs dialectes) ; **idiolectes / échec** (au moins une paire < 90 %).
- **Stabilité** : C et lexique aux checkpoints 250-pas (la table du meilleur checkpoint change-t-elle
  sur les 1 000 derniers pas ?). **Vitesse** : premier pas où l'exact VAL-OOD 9 paires ≥ 90 %.
- **Effet de la règle** : COLL vs IND sur graines réussies, vitesse, C.
- **Autodiagnostic** : confiance = min, sur les colonnes, des probabilités des choix argmax (symbole
  émis, jeton reçu, chiffre d'I1). Faux et sûrs (≥ 0,8). Seuil d'abstention τ par graine sur
  VAL-OOD (plus grand τ de {0,5 … 0,99} laissant ≤ 5 % des justes sous τ, règle E014) ; taux
  d'abstention quand faux / quand juste sur TEST.

## 6. Exploratoire (si le budget le permet, marqué comme tel)

Nouveaux venus sur les graines COLL réussies : A4 (lecteur s2, code neuf) rejoint une population
**gelée** (seul E_4 apprend, paires A4 ↔ B tirées au hasard, récompense COLL par tour d'1 paire),
≤ 1 000 pas ; idem B4 face aux A gelés. Mesure : pas pour atteindre 90 % VAL-OOD sur ses 3 paires,
et s'il adopte le lexique existant. Échange à chaud : aucun ré-entraînement n'est nécessaire pour
permuter les paires puisque les 9 paires sont évaluées.

## 7. Hyperparamètres (pilote graine 0, VAL-OOD seule, amendement A1 après pilote)

Grille pilote en COLL : lr ∈ {0,05 ; 0,2}, β ∈ {0 ; 0,01}, 4 000 pas. Si aucune case n'atteint 10 %
VAL-OOD : essai à 12 000 pas (repli prévu). Si toujours rien : **rendu d'échec** documenté (la
récompense tout-ou-rien seule est trop rare pour ce montage), témoins évalués quand même. IND et
COUPÉ prennent les valeurs de COLL (même budget de pas).

## 8. Prédictions (écrites avant tout run)

| | énoncé |
|---|---|
| P1 | COLL réussit (≥ 4/5 graines, 9 paires ≥ 90 % à 16) — pari incertain : récompense rare |
| P2 | IND atteint 90 % VAL-OOD **plus vite** que COLL (médiane des pas) — la règle collective ralentit l'attribution du mérite (contre-pied) |
| P3 | Sur les graines réussies, lexique **commun** C ≥ 9/11 dans COLL, et C(COLL) ≥ C(IND) |
| P4 | Graines réussies : 9 paires ≥ 90 % aussi à **100 chiffres** (le protocole est par colonne, sans longueur) |
| P5 | COUPÉ : 0/5 graines, ≤ 1 % exact à 16 chiffres |
| P6 | DONNÉ : 9 paires ≥ 99 % à 16 chiffres |
| P7 | Confiance médiane des faux < des justes (COLL, IND) |

Budget calcul ≤ 4 h (plusieurs fenêtres en parallèle) ; invocations ≤ 9 min avec reprise.
