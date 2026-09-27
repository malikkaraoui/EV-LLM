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

## Amendement A1 (après pilote graine 0, avant toute graine officielle)

Grille COLL, 4 000 pas, graine 0 (exclue), `resultats/pilote.json` :

| lr | β | meilleur VAL-OOD (9 paires) | tours réussis fin phase 1 | tours réussis phase 2 |
|---|---|---|---|---|
| **0,05** | **0** | **0,222** | 0,228 | 0,000 |
| 0,05 | 0,01 | 0,000 | 0,000 | 0,000 |
| 0,2 | 0 | 0,000 | 0,008 | 0,000 |
| 0,2 | 0,01 | 0,000 | 0,001 | 0,000 |

**Figé** : lr = 0,05, β = 0, 4 000 pas (seule case ≥ 10 % : le repli à 12 000 pas ne s'applique
pas). Borne basse de la grille : un lr plus faible n'a pas été essayé (écrit ici, pas corrigé).
Observation du pilote, non utilisée pour choisir : la case retenue apprend **2 paires sur 9**
(A1→B2 et A2→B3 à 100 % en VAL-OOD), lexiques de A1 et A2 sans aucun symbole commun (C = 0/11) ;
en phase 2 (3 paires, tout-ou-rien) plus aucun tour n'est réussi et les tables ne bougent plus.
Aucune autre modification du protocole.

## Amendement A2 (mandat M0032, 2026-09-27, branche `exp/e016-a2` depuis `exp/e016-mouches` @ `867ccaf`) — écrit et poussé AVANT tout run A2

Question : l'effet propre de la règle de Malik (tout-ou-rien collectif + tout le monde recommence),
**séparé** de celui du seul brassage des partenaires. Code M0031 (`m16.py`, `entraine16.py`,
`evalue16.py`) **importé, non modifié** ; A2 ajoute des fichiers `*a2.py`, runs sous `runs/a2/`,
résultats sous `resultats/a2/`. Mêmes agents, canal (V = 48), données, VAL/TEST, graines 1–5,
lr 0,05, β = 0, 4 000 pas, 128 tours par pas, rejeu ≤ 4 essais (A1).

### A2.0 Antériorité (relecture ≈ 10 min des sources de la veille orchestrateur)

- **Déjà fait** [VÉRIFIÉ, résumés relus] : Tieleman et al. 2019 (arXiv 1912.06208) — population
  d'encodeurs/décodeurs **appariés au hasard à chaque itération** : plus la communauté est grande,
  moins il y a d'idiosyncrasies ; signal = reconstruction (différentiable). Mahaut et al. (arXiv
  2302.08913) — réseaux visuels **gelés hétérogènes**, protocole commun, **nouveau venu** qui
  l'adopte vite (jeu référentiel). Marincat 2026 (arXiv 2609.11365) — sociétés indépendantes sur une
  tâche algorithmique : pas de langue unifiée, transfert négatif de l'interface héritée.
  Michel et al. ICLR 2023 (« Revisiting populations ») : page non accessible ici, cité d'après la
  veille orchestrateur [NON RELU] — l'échange de partenaires limite la co-adaptation par paire.
- **Conséquence** : « le brassage des partenaires réduit les idiolectes » et « un nouveau venu
  apprend le protocole » sont **connus** ; A2 ne les présente pas comme neufs. FIXE et IND servent de
  **réplication** de ce connu dans notre montage.
- **Ce qu'A2 ajoute** [HYPOTHÈSE sur la nouveauté, veille non exhaustive] : (a) la comparaison
  **à brassage identique** (mêmes tirages de partenaires) d'une récompense par paire, d'un
  tout-ou-rien collectif sans rejeu et du tout-ou-rien **avec rejeu collectif** — non trouvé dans
  la veille ; (b) un signal de **succès de calcul** (par colonne) sur un calcul coupé en deux entre
  compétences procédurales gelées, jugé jusqu'à 1 000 chiffres ; (c) des nouveaux venus A4/B4 comme
  test de langue commune **côté émission et côté réception séparément**.
- Signal dense vs littérature : Mahaut et Tieleman ont un jeu référentiel / une perte différentiable
  sur le message. Ici le signal reste un **succès de calcul par colonne**, sans aucune supervision de
  la forme du message ni gradient à travers le partenaire (REINFORCE sur un scalaire).

### A2.1 Mission 0-ter : pilote-garde « signal dense » (graine 0, exclue ; ≤ 30 min)

- **IND-dense** = IND de M0031 à **une seule** différence : récompense d'un item = **fraction des
  colonnes de sortie correctes**, (1/n) Σ_{t<n} [chiffre émis par B_j à la colonne t = chiffre t de
  a+b, poids faible d'abord] avec n = n_pas = max(ℓa, ℓb) + 1 (cibles = `encode_aligne` d'E013,
  0 au-delà de la somme). [VÉRIFIÉ, `m16.echantillonne`] B_j produit bien un chiffre par colonne
  (`dig`, n × T), comparé ici aux cibles avant `decode` : aucun module gelé n'est touché. Même
  ligne de base (moyenne du lot par n_pas).
- **Critère de décollage** : graine 0, **≥ 5 paires sur 9 à ≥ 90 %** exact VAL-OOD (6–8 chiffres)
  à au moins un checkpoint (tous les 250 pas) en ≤ 4 000 pas.
- **Sinon, UNE seule autre variante** : **CURRIC** = IND, récompense 0/1 d'origine, opérandes à
  **1 chiffre** (a, b ∈ 0–9 uniformes, rng [18 000 + graine, pas]) pendant les 1 000 premiers pas,
  puis flux 1–5 d'origine ; mêmes 4 000 pas au total, même critère. Si CURRIC ne décolle pas non
  plus : **STOP propre**, aucune condition A2.2 lancée.
- Prédiction Q0 : IND-dense décolle (≥ 5/9) — confiance modérée (≈ 60 %) ; si oui, en **moins de
  2 000 pas**.

### A2.2 Conditions (seulement si Q0 décolle ; sinon avec la variante qui décolle)

Toutes sous la récompense du pilote qui a décollé. Tirage des partenaires **identique** entre IND,
TOR, COLL, REJEU (même générateur `rng([17 000 + graine, pas])` qu'M0031, mêmes problèmes neufs
`paires_flux`). Phase 1 (pas 0–1 999) : 1 paire / tour ; phase 2 (2 000–3 999) : 3 paires / tour
(appariement parfait aléatoire), comme M0031.

| cond. | partenaires | récompense d'un item | rejeu d'un tour raté (≠ tous exacts) |
|---|---|---|---|
| (i) FIXE | A_k↔B_k seulement : phase 1 k tiré au hasard ; phase 2 les 3 paires fixes | par paire (crédit par colonne) | non |
| (ii) IND | rotation (M0031) | par paire | non |
| (iii) TOR | rotation | **min sur les paires du tour** du crédit par colonne (traduction dense de « tout le monde ou personne ») | non |
| (iv) COLL | rotation | min sur les paires du tour | **oui** (mêmes problèmes, nouveau tirage, ≤ 4 essais) |
| (v) REJEU (si budget) | rotation | par paire | oui |

- Écrit d'avance [VÉRIFIÉ par construction] : en phase 1 (1 paire / tour), le min sur le tour est
  la récompense de la paire : **TOR ≡ IND en phase 1**, COLL ≡ REJEU en phase 1. L'effet
  « tout-ou-rien » n'agit qu'en phase 2 ; l'effet « rejeu » agit dans les deux phases.
- Un tour « raté » (déclencheur du rejeu) = au moins une réponse non **exacte** (addition entière),
  comme M0031 — la règle « si une ne donne pas la bonne réponse, tout le monde recommence ».
- Lignes de référence « signal rare » **sans rerun** : IND et COLL de M0031 (`resultats/resultats.json`).
- 5 graines par condition (i)–(iv) ; (v) seulement s'il reste du budget (≤ 3 h au total A2).
  Si le budget manque : réduire d'abord les graines de (ii) IND (seule condition déjà proche de
  M0031), jamais celles de TOR/COLL. Tout écart sera écrit.
- Sélection du checkpoint : meilleur exact VAL-OOD moyen sur les 9 paires (inchangé, y compris pour
  FIXE : écrit d'avance, cela ne favorise aucune condition rotative).

### A2.3 Mesures (en plus de M0031)

- TEST (lu une fois, 9 paires, jeux E014) : graine réussie = 9 paires ≥ 90 % à 16 chiffres ;
  matrice 3 × 3 à 16 et 100 chiffres **pour les 9 paires y compris FIXE** (paires croisées de FIXE
  = test d'idiolecte) ; extrapolation 16 → 100 → 1 000 ; adverses ; C (M0031) ; faux et sûrs,
  abstention (règles M0031).
- **Nouveaux venus (officiel)**, pour chaque condition (i)–(iv) × 5 graines, sur le checkpoint
  retenu, population **gelée** :
  - **A4** (lecteur `R1L-s2`, jamais vu, code privé neuf = 7e permutation de `codes_prives`) : seule
    sa table E_4 apprend, paires A4↔B_j (j uniforme), récompense du régime (crédit par colonne,
    par paire), ≤ 1 000 pas, lot 128, lr 0,05 ; VAL-OOD sur ses 3 paires tous les 50 pas.
    **Zero-shot (0 pas)** : E_4 = 0 ⇒ émission uniforme / argmax symbole 0 — attendu ≈ 0 **par
    construction** (rapporté, sans valeur informative). Mesure : premier pas où les 3 paires
    A4↔B_j sont ≥ 90 % (sinon « > 1 000 »). A4 ne peut réussir que si, pour chaque sens, **un même
    symbole** est compris par les 3 B : c'est le test côté réception d'une langue commune.
  - **B4** (I1 H = 4 graine 4, jamais vu, code privé = 8e permutation) : seule R_4 apprend face à A1–A3 gelés ; même mesure.
    B4 peut être multilingue (48 symboles) : il ne peut échouer que si deux A emploient le même
    symbole pour deux sens différents (conflit). Test plus faible, côté émission.
- Décomposition préenregistrée de l'effet de la règle, sur (a) nombre de paires ≥ 90 % à 16 par
  graine, (b) C, (c) pas de A4 : (iv) − (ii) = [(iii) − (ii)] (tout-ou-rien) + [(iv) − (iii)] (rejeu).
  n = 5 : on rapporte les 5 valeurs et la médiane, aucune conclusion générale.

### A2.4 Prédictions (écrites avant tout run A2)

| | énoncé |
|---|---|
| Q0 | IND-dense graine 0 décolle (≥ 5/9 paires ≥ 90 % VAL-OOD), en < 2 000 pas |
| Q1 | FIXE : les 3 paires fixes ≥ 90 % à 16 dans ≥ 4/5 graines ; paires croisées ≤ 20 % à 16 (idiolectes) ; C ≤ 2 |
| Q2 | IND (rotation) : médiane ≥ 7/9 paires ≥ 90 % à 16 ; lexique **synonyme** plutôt que commun (médiane C ≤ 4/11) — contre-pied de Tieleman, parce que V = 48 laisse la place à 3 dialectes |
| Q3 | Effet tout-ou-rien (iii) − (ii) : ≤ 0 paire en médiane (le min sur le tour dilue le crédit) ; \|ΔC\| ≤ 1 |
| Q4 | Effet rejeu (iv) − (iii) : ≤ 0 paire en médiane (moins de problèmes neufs) ; \|ΔC\| ≤ 1 |
| Q5 | Ce qui fait la langue commune (C, A4) est dû au brassage, pas à la règle : C(IND) − C(FIXE) > \|C(COLL) − C(IND)\| en médiane |
| Q6 | A4 atteint 90 % en ≤ 1 000 pas : 0/5 en FIXE ; moins de graines que B4 dans chaque condition |
| Q7 | Les paires apprises restent ≥ 90 % à 100 chiffres (comme M0031, 13/13) |
