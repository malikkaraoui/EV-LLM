# A0 — Préenregistrement : premier système candidat « ACQUÉRIR »

Mandat M0014, 2026-09-26. **Figé avant tout code d'évaluation de ce dossier.** Rien ici ne se modifie après avoir vu un résultat : un écart entre ce texte et ce qu'on observe est un résultat, pas une correction.

## 0. Pourquoi A0

Jusqu'ici, le projet a construit des bancs (E002) et une mesure réparée (E002-bis, `research/experiments/E002bis-mesure/`). Sur `origin/main` :
- [VÉRIFIÉ, README E002-bis] le plafond-vérificateur a R > 0 sur 20 mondes sur 20 ;
- [VÉRIFIÉ, idem] les quatre étalons, qui ne gardent rien d'un monde à l'autre, échouent au critère ACQUÉRIR ;
- [VÉRIFIÉ, idem] le découvreur naïf est à ≈ −0.026 de R̂_diff.

A0 est le **premier candidat** : il doit faire ce qu'aucun étalon ne fait, **résoudre le monde n+1 plus vite que le monde n**. Hypothèse de fond (§1 bis v2.1 de l'architecture) : c'est la boucle *savoir ↔ acquis* qui accélère. Trois pièces la portent : la **règle** (ici, les propriétés des relations), le **déclencheur** (« je dois vérifier ») et l'**autodiagnostic** (« quelle pièce de ma mécanique a fauté ? »).

Python standard, aucune dépendance, aucun appel réseau, aucun LLM.

## 1. Ce qui est repris sans modification

Importé depuis `research/experiments/E002-relations-opaques/` et `research/experiments/E002bis-mesure/` (ajout au `sys.path`, **aucun fichier de ces dossiers n'est modifié ni copié**) :
- générateur de mondes, bruit (5–10 % par monde dont une inversion ciblée en phase 2), oracle, étiquettes attendues, environnement interactif, coût d'une requête (`C_atome ≈ 9.32 bits`), R en bits (E002 §1–§5) ;
- `evaluer.evaluer_monde` d'E002 et `evaluer_bis.evaluer_suite` d'E002-bis (R̂_diff, critère ACQUÉRIR, seuils) ;
- les quatre étalons d'E002-bis, rejoués à titre de rappel : aléatoire, oracle-propriétés, plafond-vérificateur, découvreur naïf ;
- la correction de fin de monde d'E002 (`fin_monde(correction)` : pour chaque question, étiquette attendue avec sa preuve, et vérité de l'atome). C'est la **seule** révélation de l'oracle ; A0 ne lit jamais le monde (vérité, types, propriétés, bruit, famille).

## 2. Séquence de mondes

- **Graines 1 à 20, dans cet ordre**, familles `(graine − 1) // 5` : 4 familles de 5 mondes consécutifs. Mêmes graines, même bruit qu'E002-bis.
- Le critère ACQUÉRIR d'E002-bis est défini sur 5 mondes par famille : il est mesurable tel quel. **Aucune graine n'est ajoutée.**
- A0 **ne reçoit pas** le numéro de famille. Il doit reconnaître seul qu'un monde ressemble à ceux qu'il a déjà vus (§3.1).
- Un seul objet A0 traverse les 20 mondes : son état est **conservé** d'un monde à l'autre. Pour l'ablation « sans mémoire », tout l'état appris est remis à zéro au début de chaque monde.

## 3. Mécanismes d'A0

Chaque pièce est désactivable pour ablation (§4). Les constantes initiales ci-dessous sont **fixées ici**, une fois pour toutes. Aucune n'est réglée par monde.

### 3.0 Notations de coût (bits, publiques)

- `p_ref(r)` : prédicteur de Laplace par relation sur les observations, formule publique d'E002 §4. A0 le recalcule lui-même.
- ε = 1/64 (E002 §4). Pour un atome `a` de la relation `r` qu'A0 n'a pas observé :
  - gain d'un `DÉDUIT vrai` juste : `G = log2(1/p_ref) − log2(1/(1−ε))` ;
  - perte s'il est faux : `L = log2(1/ε) − log2(1/(1−p_ref))` ;
  - et symétriquement pour un `DÉDUIT faux`.
- `C = C_atome ≈ 9.32 bits` : coût d'une requête.
- A0 ne compte ces gains et pertes que sur les questions portant sur un atome **qu'il n'a pas observé**. Ce sont les seules qui entrent dans R. Il le sait par la définition publique de R, sans savoir lesquelles sont tenues à l'écart.

### 3.1 Mémoire inter-mondes des propriétés (« règles »)

**Règles candidates.** Pour chaque relation, quatre propriétés : réflexive, symétrique, antisymétrique, transitive. S'y ajoutent les compositions `ri∘rj = rk` suggérées par les observations : il existe au moins une chaîne observée et toutes les valeurs connues de `rk` sur ses extrémités sont vraies (même filtre que le découvreur naïf).

**Instances.** Chaque règle se confronte aux faits connus par ses *instances* : antécédents connus vrais, conséquent connu.
- Une instance **confirme** la règle ou la **viole**.
- Soit `m` le nombre d'atomes de l'instance connus **par observation seulement**. Les atomes demandés au monde sont sûrs.
- Sous une règle vraie, une instance ne peut être violée que par le bruit : probabilité `η_m = 1 − (1−η)^m`.
- Sous une règle fausse, elle confirme avec une probabilité `q_type`.
- Croyance, en log-cote :
  `logit b(ρ) = logit a_priori(ρ) − δ_type + Σ_instances log [P(instance | vraie) / P(instance | fausse)]`
  - une violation avec `m = 0` (atomes tous sûrs) réfute la règle ;
  - `δ_type` est la marge de l'autodiagnostic (§3.3).

**Ce qui est mémorisé**, à la fin de chaque monde. Ce sont uniquement des statistiques structurelles : **aucun nom de relation, aucun nom d'entité n'est gardé**.
- **Bibliothèque de profils.**
  - Pour chaque monde vu, A0 garde le multiensemble des vecteurs de propriétés de ses 5 relations, par exemple `(réfl, sym, antisym, trans) = (0,0,1,1)`.
  - Ces vecteurs sont estimés sur les faits sûrs : requêtes et vérités révélées par la correction. S'y ajoutent les règles citées dans les preuves attendues de la correction.
  - Il garde aussi le nombre de compositions vraies trouvées.
- **A priori d'un nouveau monde.**
  - Chaque profil gardé est pondéré par la vraisemblance des observations du nouveau monde, sommée sur les 120 bijections relations → emplacements. Le profil explique-t-il ce qu'on voit ?
  - Un profil « nouveau » est ajouté, de poids a priori 1 comme chaque profil gardé. Ses propriétés sont indépendantes, de fréquence égale à la fréquence moyenne sur la mémoire (Laplace).
  - L'a priori de chaque propriété est la marginale du mélange.
  - Sans mémoire : 0.5 par propriété.
  - A priori d'une composition candidate : `(vraies + 1) / (candidates + 5)` sur la mémoire, soit **0.2 sans mémoire**.
- **Signatures qui trahissent.** `q_type` est appris sur les instances sûres des règles fausses des mondes passés : Laplace, a priori Beta(1, 1), donc 0.5 sans mémoire. Une confirmation pèse donc d'autant plus que les fausses règles de ce type confirment rarement.
- **Ordre de test le plus rentable en bits.**
  - Une règle `ρ` est **utilisée** si son espérance est positive : `b·ΣG + (1−b)·(q·ΣG − (1−q)·ΣL) > 0`.
  - Les sommes portent sur les questions non observées que `ρ` ajoute à la fermeture des règles déjà utilisées.
  - Le **test** suivant est celui qui maximise `P(mauvaise décision)·coût(mauvaise décision) − C`. Il n'est lancé que si ce terme est positif. C'est la règle du déclencheur (§3.2), appliquée aux prémisses-règles.
    - Si `ρ` est utilisée : `P = 1−b`, coût `(1−q)·ΣL − q·ΣG`.
    - Sinon : `P = b`, coût `ΣG`.
  - Un test est **une** requête : le conséquent inconnu d'une instance dont les antécédents sont connus vrais, en préférant les antécédents sûrs.
  - Budget : 150 requêtes par monde, comme le découvreur naïf.

### 3.2 Déclencheur calibré (faits-prémisses)

Avant de rendre ses réponses, A0 répond par le chaînage de Horn d'E002, sur ses faits connus et ses règles utilisées. Pour chaque **fait observé non vérifié** `f` cité comme prémisse d'un `DÉDUIT` sur une question non observée, il compare trois options. Soit `p = P(erreur de f)` :
- **conclure** : `(1−p)·ΣG_f − p·κ·ΣL_f` ;
- **vérifier** (demander `f`) : `(1−p)·ΣG_f − C` ;
- **INDÉTERMINÉ** (écarter `f`, donc ses conséquences) : `0`.

C'est la règle `P(erreur)·coût(erreur) > coût(vérification)` : vérifier bat conclure exactement quand `p·κ·ΣL_f > C`.
- Un fait prémisse d'un `CONTRADICTION` sur une question non observée est vérifié si `p·ΣG_f > C`. On prend ici `G` au plus petit des deux gains possibles.
- A0 exécute la vérification la plus rentable, recalcule et recommence. Quand il ne reste aucune vérification rentable, il écarte les faits dont l'option INDÉTERMINÉ bat « conclure », puis recalcule. Il s'arrête quand plus rien ne change.

`p` vient d'un **compteur appris sur les mondes précédents**, par catégorie de prémisse :
- `violation` : le fait est cité par une clause violée ;
- `phase1` ;
- `phase2`.

Ce compteur est une Beta mise à jour **en fin de monde**, sur tous les faits observés dont la vérité a été révélée (requêtes et correction). A priori : Beta(1, 9) pour `phase1` et `phase2`, Beta(1, 1) pour `violation`. `η` (§3.1) est la moyenne de `phase1` et `phase2`. `κ = 1` au départ.

### 3.3 Autodiagnostic

Après la correction, pour chaque `DÉDUIT` d'A0 **faux en vérité**, A0 attribue l'erreur à **une** pièce, dans cet ordre :
1. **Propriété mal acceptée** : une règle citée dans la preuve est réfutée par les faits sûrs de fin de monde. La marge du type correspondant augmente : `δ_type += 0.5`. Accepter ce type exigera plus de preuves.
2. **Prémisse bruitée non vérifiée** : un fait cité, non demandé, est faux en vérité. Le compteur de sa catégorie reçoit **2 erreurs supplémentaires**. L'erreur coûteuse pèse plus qu'une erreur ordinaire.
3. **Seuil du déclencheur** : aucune des deux causes n'est établie, par exemple parce que la prémisse n'est pas révélée. Alors `κ ← min(4, 1.1·κ)`.

Aucun réapprentissage global : seule la pièce désignée bouge. Un type sans erreur de propriété pendant un monde voit sa marge décroître : `δ_type ← max(0, δ_type − 0.1)`.

### 3.4 Réponses

Les réponses sont celles du chaînage de Horn d'E002 (étiquettes, preuves) sur les faits connus d'A0, faits écartés exclus, avec ses règles utilisées et la règle sémantique de la variante A.
- A0 n'émet **pas** d'`HYPOTHÈSE` : ce qui n'est pas conclu est `INDÉTERMINÉ` et vaut `p_ref` dans R.
- Déterminisme : aucun tirage aléatoire ; tous les parcours se font sur des listes triées ; l'évaluateur se relance avec `PYTHONHASHSEED=0`, comme E002-bis (leçon M0007).

## 4. Configurations (préenregistrées)

| nom | mémoire | déclencheur | autodiagnostic |
|---|---|---|---|
| `a0` (complet) | oui | calibré (§3.2) | oui |
| `a0_sans_memoire` | état remis à zéro à chaque monde | calibré | sans effet (état remis à zéro) |
| `a0_verifie_toujours` | oui | vérifie toute prémisse de tout `DÉDUIT`/`CONTRADICTION`, comme le plafond-vérificateur | oui |
| `a0_verifie_jamais` | oui | conclut toujours, ne vérifie ni n'écarte jamais | oui |
| `a0_sans_autodiagnostic` | oui | calibré | `δ`, `κ` et compteurs supplémentaires figés |

Sont rejoués en rappel les quatre étalons d'E002-bis : aléatoire, oracle-propriétés, plafond-vérificateur, découvreur naïf.

## 5. Critères

**Métriques préenregistrées.** Elles sont calculées par l'évaluateur E002-bis, non modifié :
- M1 : R̂_diff moyen sur les 20 mondes (plus haut = mieux) ;
- M2 : nombre de familles en accélération (plus = mieux) ;
- M3 : gain moyen de R̂_diff entre le 1er et le 5e monde, sur les 4 familles (plus haut = mieux) ;
- M4 : `DÉDUIT` faux en vérité, moyenne par monde (plus bas = mieux).

**Critère ACQUÉRIR**, repris d'E002-bis sans modification. Une famille est en accélération si `R̂_diff(5e) − R̂_diff(1er) ≥ 0.005` et si au moins 3 transitions sur 4 ont `ΔR̂_diff > 0`. Le critère est réussi avec au moins 3 familles sur 4 en accélération.

**Réussite du candidat** : `a0` satisfait ACQUÉRIR, **et** chacune des 4 ablations fait strictement moins bien qu'`a0` sur au moins une des métriques M1–M4.

**Échec du candidat** : `a0` échoue ACQUÉRIR. Le résultat est publié tel quel, en nommant la pièce suspecte.

**Cas intermédiaire** : `a0` réussit ACQUÉRIR, mais une ablation fait au moins aussi bien sur M1–M4. On déclare alors que la pièce retirée **ne porte pas** le gain mesuré.

**Contrôle** : les quatre étalons et `a0_sans_memoire` ne gardent rien d'un monde à l'autre et **doivent** échouer ACQUÉRIR. Si l'un d'eux réussit, le critère est déclaré trop permissif sur ce banc. C'est constaté, pas corrigé.

## 6. Tests (unittest, stdlib) et mutations

- **Nom de relation** : la mémoire ne transfère jamais un nom de relation ni d'entité. On sérialise tout l'état appris après plusieurs mondes et on n'y trouve aucun `R1`…`R5` ni aucun `o…`. Le même contrôle se fait par construction : on renomme les relations d'un monde, et l'état appris doit être identique.
- **Déclencheur** : la règle de coût est vérifiée sur un cas calculé à la main (p, ΣG, ΣL, C donnés, décision attendue écrite).
- **Autodiagnostic** : sur une erreur injectée de chaque type (propriété fausse citée ; prémisse bruitée non demandée ; ni l'une ni l'autre), la bonne pièce est mise à jour et elle seule.
- **Déterminisme** : deux exécutions dans deux processus, sous des `PYTHONHASHSEED` ambiants différents, donnent des résultats identiques.
- **Mutations** : au moins 5, injectées une à une, chacune doit faire échouer la suite.

## 7. Exécution

5 configurations A0 + 4 étalons sur les graines 1–20. Sorties : `results/<horodatage>/resultats.json` et `summary.md`, committées. Le rejeu est déterministe et prouvé par `cmp` entre deux exécutions.

## 8. Attentes (avant exécution)

- [HYPOTHÈSE] `a0` a un R̂_diff moyen supérieur à celui du découvreur naïf (≈ −0.026). Raisons : moins de tests grâce aux a priori appris, et les prémisses coûteuses sont vérifiées.
- [HYPOTHÈSE] Le premier monde de chaque famille est le plus bas pour `a0`, puisque le profil n'est pas encore en mémoire. Le gain se concentre sur la transition 1 → 2.
- [HYPOTHÈSE] Risque principal d'échec d'ACQUÉRIR : la variabilité d'un monde à l'autre (écart-type de 0.013 à 0.020 pour les étalons, E002-bis) est du même ordre que le seuil, ce qui rend 3 hausses sur 4 difficiles une fois l'a priori appris. Probabilité subjective de réussite d'ACQUÉRIR : **≤ 30 %**, écrite avant exécution.
- [HYPOTHÈSE] `a0_verifie_toujours` a un R plus stable mais paie plus de requêtes ; `a0_verifie_jamais` a plus de `DÉDUIT` faux en vérité.

## 9. Hors de ce préenregistrement

Émission d'`HYPOTHÈSE` probabilistes, étalons LLM, modification du banc, du bruit ou du coût d'une requête, familles nouvelles, et toute retouche de ce texte après résultats.
