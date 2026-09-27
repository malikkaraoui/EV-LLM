# E010 — « B » : enseigner la règle comme à l'école — préenregistrement

Mandat M0023, 2026-09-27, branche `exp/e010-enseignement` (depuis `origin/exp/e008-addition`
@ `af281f5`). Ce document est committé et poussé **seul, avant toute ligne de code et toute
exécution d'un modèle E010**. Toute modification ultérieure est un amendement daté en fin de
fichier, jamais une réécriture.

Seule mesure faite avant ce document : une **sonde de temps** jetable (hors dépôt) sur le
modèle E008, lot 256, positions absolues : 0,098 s / pas à 19 positions, 0,300 s à 57,
0,501 s à 92 (M1, GPU non partagé à ce moment). Elle sert uniquement à dimensionner le budget
(§7) ; aucune donnée d'addition, aucune exactitude.

## 0. Question

Un enfant ne découvre pas la retenue seul : on la lui **montre**. Que change l'**enseignement
explicite** (brouillon colonne par colonne, règle énoncée) pour un petit transformer :
(Q1) **combien d'exemples uniques** faut-il pour ≥ 95 % dans la distribution ; (Q2) la
**généralisation en longueur** (entraîné sur 1–5 chiffres, testé jusqu'à 100 chiffres) ?

## 1. Réutilisation d'E008 (sans modification de `research/experiments/E008-addition/`)

Importés depuis `../E008-addition` : `data.tire_nombre`, `data.chaine_retenue`,
`data.jeux_de_test` (T-ID, T-ID1, T-OOD), `data.paires_exclues`, `evaluate.evaluer` et
`evaluate.resume` (**évaluateur unique** : un système = fonction `(liste de (a, b)) → liste de
(réponse canonique | None, confiance)`, comparaison par égalité exacte de chaînes avec
`str(a + b)`), `controles.addition_retenue` (C-ORACLE). Le modèle est réécrit à l'identique
d'architecture (pré-LN, d = 256, 4 couches, 4 têtes, FFN 1024, GELU, sans dropout, embeddings
non liés) **avec un cache clé/valeur** pour le décodage (indispensable à 100 chiffres) ; un test
vérifie que décodage avec cache = décodage sans cache.

## 2. Formats (le seul facteur étudié, avec les positions)

Opérandes toujours en ordre standard. Un token par chiffre. Perte sur **tout ce qui suit le
prompt** (brouillon + réponse + fin). Exact-match sur la **réponse finale seule** (le brouillon
n'est pas noté), via l'évaluateur E008.

- **F0 — réponse seule** : `a + b =` → somme (poids fort d'abord) `$`. = format B-STD d'E008.
- **F1 — brouillon de colonnes** : `a + b =` puis, pour chaque colonne i = 0 (unités) …
  max(ℓa, ℓb) − 1, les 6 tokens `aᵢ bᵢ cᵢ sᵢ cᵢ₊₁ ;` (chiffre de a, chiffre de b — 0 si
  l'opérande est plus court —, retenue entrante, chiffre écrit, retenue sortante, séparateur),
  puis `#`, puis la somme en ordre standard, puis `$`. C'est la ligne « chiffre_a + chiffre_b
  + retenue = chiffre, nouvelle retenue » du mandat, en notation compacte (les symboles `+`,
  `=`, `,` constants sont retirés : ils n'apportent aucune information et coûtent 40 % de
  calcul). **La trace ne contient aucun indice de position absolue** (ni numéro de colonne, ni
  longueur).
- **F2 — règle énoncée** : une ligne constante de 16 tokens-mots en tête de chaque exemple
  (entrée, non notée) : `on additionne colonne par colonne depuis la droite , on reporte 1 si
  ≥ 10 .` (les « mots » `1` et `10` sont des tokens distincts des chiffres), puis le format F0.
  Tokenisation en mots (et non en caractères) pour limiter la longueur de séquence (§7).
- **F3 — brouillon, réponse inversée** : F1 mais la somme après `#` est écrite poids faible
  d'abord (ablation : la réponse devient une copie dans l'ordre du brouillon).

Vocabulaire : `0`–`9` (0–9), `+` 10, `=` 11, `$` 12, remplissage 13, `;` 14, `#` 15, puis les
14 mots distincts de la règle (16–29). 30 tokens pour tous les formats (tables identiques).

**Positions** : **abs** (positions absolues apprises, table de 1 024 lignes pour couvrir 100
chiffres en F1 ; seules les ≈ 50 premières lignes reçoivent un gradient à l'entraînement) et
**NoPE** (aucun embedding de position). 4 formats × 2 positions = **8 conditions**.

## 3. Données

- **Réserve d'entraînement** d'une graine s : suite déterministe de paires tirées comme E008
  (ℓa, ℓb indépendants uniformes dans 1–5, chiffres uniformes, premier ≠ 0 sauf ℓ = 1),
  `default_rng([30_000 + s])`, **dédoublonnée** (paire ordonnée) et privée de
  `paires_exclues()` d'E008 (tous les jeux T-ID, T-OOD, T-CARRY et paires échangées). La
  réserve de taille N = les N premières paires distinctes (réserves **emboîtées**).
  Conséquence assumée : les petites combinaisons de longueurs (100 paires possibles à 1 + 1
  chiffre) sont sous-représentées dans les grandes réserves.
- **Lots** : parcours par époques ; époque e = permutation `default_rng([40_000 + s, N, e])`
  de la réserve ; le pas t prend les exemples t·256 … t·256 + 255 de la concaténation des
  époques. Même graine ⇒ **mêmes exemples dans le même ordre** pour les 8 conditions.
- **Exemples uniques vus** = min(N, pas × 256), journalisé pour chaque run (≠ nombre de pas).
- **Jeux** (les deux opérandes ont L chiffres, sauf adverses asymétriques) :
  - **T-ID** : E008 T-ID, L = 2–5 (criblage : 200 premiers items / L ; conditions finales : 500).
  - **T-ID1** : E008, 100 paires à 1 chiffre (non disjoint, rapporté à part).
  - **V-OOD (validation)** : E008 T-OOD, L = 6, 7, 8 (criblage : 200 premiers / L ; final :
    500). **Seul jeu autorisé pour tout choix** (hyperparamètres au pilote, conditions
    retenues pour 5 graines). Pas de choix de checkpoint : on prend toujours le **dernier**.
  - **T-FIN (test final intouché)** : L = 10, 16, 32, 64, 100 ; 200 paires uniques / L,
    graine 2030. Évalué **une seule fois**, à la fin, sur les conditions finales.
  - **T-ADV (adverses)**, L = 10, 16, 32, 64, 100, 20 items par type et par L, graine 2031 :
    **cascade** (`99…9 + 1`, `1 + 99…9`, puis 18 paires `9…9x + y` où les j ≤ 3 derniers
    chiffres débordent et la retenue traverse tous les 9 ; ordre échangé une fois sur deux) ;
    **zéros** (`10…02 + 10…03`, puis 19 paires `10^(L−1) + x` et `10^(L−1) + y`, x, y
    uniformes dans 1–99) ; **asymétriques** (a de L chiffres + b de 3 chiffres, ordre échangé
    une fois sur deux). Évalué une seule fois, avec T-FIN.
- Aucun item de V-OOD, T-FIN, T-ADV n'a deux opérandes ≤ 5 chiffres : disjonction de
  l'entraînement par construction ; T-ID disjoint par l'exclusion E008 (vérifié par test).

## 4. Validité (leçon M0020) — publiée avant toute lecture de modèle

Recalculés sur **tous** les jeux (T-ID1, T-ID, V-OOD, T-FIN, T-ADV) par l'évaluateur unique :
- **C-ORACLE** (retenue codée à la main) = **100 %** partout ;
- **C-ORACLE-TRACE** : la séquence F1/F3 produite par l'oracle, relue par le **même
  analyseur** que les modèles, = **100 %** (valide l'analyseur de brouillon) ;
- **C-PARCŒUR** (table des paires de la réserve maximale de la graine 1) ≤ **1 %** sur T-ID,
  V-OOD, T-FIN, T-ADV ; contrôle positif : 100 % sur T-ID1.
Verdict « TEST VALIDE » exigé avant de lire un modèle ; sinon STOP.

## 5. Mesures

- Exact-match de la réponse finale par jeu × L ; moyenne ± écart-type entre graines **et**
  valeurs par graine.
- **Confiance** = produit des probabilités (décodage glouton) des tokens de la **réponse
  finale et de `$`** (tokens après `#` en F1/F3 ; toute la sortie en F0/F2), pour rester
  comparable entre formats. **« Faux et sûr »** = faux avec confiance ≥ 0,8, parmi les faux.
- **Non-réponse** (pas de `$` ou pas de `#` dans la limite de génération) : comptée fausse,
  rapportée à part comme « abstention » (les modèles n'ont pas d'abstention explicite) ;
  taux d'abstention parmi les faux.
- F1/F3 : diagnostic « brouillon juste » (trace entière exacte) et « réponse cohérente avec
  son propre brouillon ».
- Limite de génération : F0/F2 : max(ℓa, ℓb) + 2 tokens ; F1/F3 : 6·(max + 1) + max + 3.

## 6. Plan et critères de décision

1. **Pilote** (graine 0, exclue de tout résultat) : fixe le nombre de pas S et le lr (§7).
2. **Criblage** : 8 conditions × graines 1, 2, réserve maximale N_max = S × 256 (chaque
   exemple vu une fois). Évaluation T-ID (200/L) + V-OOD (200/L).
3. **Courbe d'efficacité** : F0, F1 × abs, NoPE, réserves N = 1 000, 10 000, 100 000
   (+ N_max du criblage), **même nombre de pas S** (itérations appariées), **graine 1
   seulement** (réduction budgétaire, §7). « Exemples nécessaires pour 95 % » = plus petit N
   de la grille dont la moyenne T-ID (L = 2–5) ≥ 95 % ; « > N_max » sinon.
4. **5 graines** (ajout des graines 3, 4, 5) pour toute condition dont la moyenne V-OOD 8
   (graines 1, 2) **dépasse 50 %**. Si le budget ne le permet pas pour toutes, priorité à la
   plus haute V-OOD 8, et l'amputation est écrite.
5. **Test final** (T-ID 500/L, V-OOD 500/L, T-FIN, T-ADV), **une seule fois**, sur les 8
   conditions du criblage (toutes leurs graines) — ce sont les conditions finales.
6. Une graine est « **réussie** » si T-FIN 16 ≥ 90 %. Une condition n'est déclarée
   « **réussie** » que si elle a ≥ 5 graines et ≥ 4/5 réussies ; toujours rapporté : k/5 ou
   k/2, moyenne ± écart.

## 7. Budget de calcul et hyperparamètres

- Budget du mandat : **≤ 4 h de calcul** total (entraînement + évaluation + pilote), invocations
  ≤ 9 min avec reprise sur checkpoint, au premier plan. Coût mesuré ≈ 5 ms par position de
  séquence et par pas : longueurs d'entraînement F0 18, F2 34, F1/F3 49 positions.
- Valeurs **provisoires**, figées après pilote par amendement (avant tout run officiel) :
  AdamW (β 0,9 / 0,98, wd 0,01), lr max 1e-3, montée linéaire 150 pas puis cosinus jusqu'à
  1e-5, écrêtage 1,0, lot 256, float32, **S = 1 500 pas** (384 000 exemples ; N_max = 384 000).
  Règle de choix au pilote : S est la plus grande valeur de {1 000, 1 500, 2 000} qui tient le
  plan (§6.2–6.3 + 30 min de réserve) dans le budget au temps mesuré ; lr ∈ {1e-3, 3e-3}
  choisi sur **V-OOD** (puis T-ID) de F1-NoPE et F0-NoPE graine 0.
- **Conséquences assumées** : le point « 1 000 000 exemples uniques » demandé par le mandat
  n'est pas atteignable (N_max = S × 256 < 10⁶) ; la courbe n'a qu'une graine ; F0 reçoit
  8 × moins de pas qu'E008 (E008 B-STD : 73 % à T-ID 5 après 1,0 M exemples) — F0 pourrait ne
  pas atteindre 95 % en distribution ; c'est une mesure, pas un défaut à corriger.

## 8. Budget de structure (ce qui est donné à la main)

| format | donné à la main |
|---|---|
| F0 | format `a+b=`, un token par chiffre, fin `$`. Rien d'autre. |
| F1 | + **l'algorithme entier en traces** : ordre des colonnes (unités d'abord), chiffres alignés recopiés, retenue entrante/sortante, chiffre écrit ; le **nombre d'itérations** est implicite (une colonne par chiffre du plus long + arrêt), la **localité** (quel chiffre lire) n'est **pas** donnée : ni index, ni alignement, ni position. |
| F2 | + une phrase constante (aucune information propre à l'exemple). |
| F3 | comme F1, + réponse dans l'ordre du brouillon (supprime la relecture inverse). |
| abs / NoPE | abs : table de positions apprise ; NoPE : ordre porté par le seul masque causal. |

Aucun index de colonne, aucun opérande pré-aligné, aucun couplage de positions.

## 9. Prédictions (falsifiables)

- **P1** : F1-NoPE atteint ≥ 95 % T-ID avec **au moins 10 × moins** d'exemples uniques que
  F0-NoPE (ou F0-NoPE n'atteint jamais 95 % sur la grille alors que F1-NoPE si).
- **P2** : F2 ≈ F0 (|écart| ≤ 5 points sur T-ID moyen et V-OOD 6), pour chaque position.
- **P3** : F1-abs et F3-abs ≤ 10 % à V-OOD 8 (positions jamais entraînées).
- **P4** : F1-NoPE > F0-NoPE de ≥ 20 points à V-OOD 6 (Kazemnejad 2023 : le brouillon n'aide
  la longueur qu'avec NoPE).
- **P5** : F3-NoPE ≥ F1-NoPE à V-OOD 8.
- **P6** : aucune condition n'est « réussie » (≥ 90 % à 16 chiffres) [prédiction sceptique].

## 10. Ordre des commits

Préenregistrement (seul, poussé) < code + tests < contrôles de validité < valeurs figées après
pilote (amendement A1) < résultats.
