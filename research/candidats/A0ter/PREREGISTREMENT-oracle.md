# A0-ter, Mission 1 — Préenregistrement : étalon « acquéreur-oracle »

Mandat M0020, 2026-09-26. **Figé avant tout code de ce dossier.** Ce texte ne se modifie pas après avoir vu un résultat : un écart entre ce qu'il annonce et ce qu'on observe est un résultat, pas une correction.

A0 (`exp/a0-candidat` @ `8a60250`) et A0-bis (`exp/a0bis-candidat` @ `1be4654`) restent publiés tels quels : ÉCHEC d'ACQUÉRIR (1/4 puis 0/4). Ils sont **importés**, jamais modifiés ni copiés. Aucun fichier sous `research/candidats/A0/`, `research/candidats/A0bis/` ni `research/experiments/` n'est touché.

## 0. Question

[VÉRIFIÉ, README A0-bis] Aucun étalon ne réussit ACQUÉRIR ; M0016 en conclut que le critère n'est pas trop permissif. [HYPOTHÈSE] L'inverse n'a jamais été vérifié : **le critère ACQUÉRIR est-il atteignable du tout sur ce banc ?**

Si un système qui acquiert *parfaitement* la connaissance d'une famille n'accélère pas au sens du critère, les échecs d'A0 et d'A0-bis ne disent rien des candidats : c'est la mesure qui est à réparer. Cet étalon sert à trancher cela, et seulement cela. Ce n'est pas un candidat.

## 1. Repris sans modification (import)

- **E002 et E002-bis** : générateur de mondes, bruit, environnement, oracle de correction, coût d'une requête, R, `evaluer.evaluer_monde`, `evaluer_bis.evaluer_suite`, `R̂_diff = R − R_plafond-vérificateur`, critère ACQUÉRIR, étalons.
- **A0** : métriques M1–M4 (`evaluer_a0.metriques`).
- **A0-bis** : la classe `A0Bis` complète (coût marginal `R̂₊·C`, mémoire par famille, bruit MLE, déclencheur, autodiagnostic), dont l'oracle hérite.

Séquence : **graines 1 à 20 dans cet ordre**, familles `(graine − 1) // 5`, 4 familles de 5 mondes, même bruit. Aucune graine ajoutée. `PYTHONHASHSEED=0` (leçon M0007).

**Critère ACQUÉRIR, inchangé** : une famille est en accélération si `R̂_diff(5e) − R̂_diff(1er) ≥ 0.005` **et** au moins 3 transitions sur 4 ont `ΔR̂_diff > 0` ; réussite si au moins 3 familles sur 4.

## 2. Structure du banc utile à la définition (lue dans le code public, avant tout résultat)

[VÉRIFIÉ, lecture de `monde.py` et exécution de `generer_monde` sur les graines 1–20, sans aucun système] Dans une famille, les 5 mondes partagent le même profil d'emplacements ; les noms de relations sont permutés à chaque monde. Le multiensemble des vecteurs de propriétés `(réfl, sym, antisym, trans)` est identique dans les 5 mondes de chaque famille, **sauf la graine 4** (famille 0), où la relation composée est réflexive. Les compositions vraies sont au nombre de 1 (familles 0 et 2) ou 0 (familles 1 et 3) dans chaque monde.

## 3. L'étalon

### 3.1 `oracle_acquereur`

- **Connaissance de famille `K_f`.** À la fin du **premier** monde d'une famille `f` du banc rencontré dans la séquence (dans `fin_monde`, après la correction), l'oracle reçoit, par un canal d'évaluateur, les propriétés vraies de ce monde :
  - pour chacune des 5 relations, son vecteur de propriétés vraies (`monde["proprietes"]`) ;
  - les compositions vraies (`monde["compositions"]`), réécrites en indices d'emplacements.
  - `K_f` est stocké **sans aucun nom** : une liste de 5 vecteurs et des triplets d'indices.
  - C'est l'acquisition parfaite et sans bruit : exactement ce qui est vrai de la famille, tel qu'on pouvait l'apprendre du 1er monde.
- **Application dans les mondes suivants de la même famille.** Au début de chaque monde dont la famille `f` a une `K_f` en mémoire, l'oracle place `K_f` sur les relations du monde courant par la **bijection** `σ` (emplacement → relation) qui maximise l'accord avec les propriétés vraies du monde courant : `score(σ) = Σ bits égaux + 4 × (compositions de K_f vraies sous σ)`. Égalités départagées par le premier `σ` dans l'ordre de `itertools.permutations` sur les relations triées.
  - Cette bijection est l'**identification parfaite** : un acquéreur parfait sait aussi quelle relation joue quel rôle. Elle n'importe du monde courant que la permutation des noms ; les règles appliquées sont celles de `K_f` (donc du 1er monde), pas celles du monde courant.
  - Les règles appliquées sont : pour chaque emplacement `j` et chaque propriété à 1 dans `K_f[j]`, la règle `(propriété, σ(j))` ; pour chaque composition `(a, b, c)` de `K_f`, la règle `("composition", σ(a), σ(b), σ(c))`. La règle sémantique de la variante A s'y ajoute comme dans A0.
  - Ces règles sont **tenues pour certaines** : l'étape « tester les règles » d'A0-bis est sautée. Tout le reste d'A0-bis est inchangé : déclencheur en coût marginal `R̂₊·C` sur les faits-prémisses (vérifier / conclure / INDÉTERMINÉ), bruit MLE, `κ`, R̂, mémoire par famille, autodiagnostic et apprentissage de fin de monde.
- **Avant `K_f`** (le 1er monde de chaque famille), l'oracle se comporte **exactement** comme `a0bis`, avec la mémoire `a0bis` qu'il a accumulée.
- L'oracle ne reçoit jamais le numéro de famille pendant un monde autrement que par la présence ou l'absence de `K_f` ; le canal d'évaluateur lui donne le monde courant uniquement pour : (i) construire `K_f` en fin de premier monde ; (ii) calculer `σ` quand `K_f` existe déjà.

### 3.2 `oracle_amnesique` (contrôle)

Identique à `oracle_acquereur`, mais **toute** sa mémoire est remise à zéro au début de chaque monde : `K_f`, et toute la mémoire `a0bis` (familles, profils, R̂, vérifications, `κ`, `δ`). Il ne dispose donc jamais d'une `K_f` pendant un monde : c'est `a0bis` sans aucune mémoire entre mondes.

### 3.3 `oracle_exact` (diagnostic secondaire, ne compte pas dans le verdict)

Identique à `oracle_acquereur`, sauf qu'à partir du 2e monde d'une famille il applique les propriétés vraies **du monde courant** au lieu de `K_f`. Il ne diffère d'`oracle_acquereur` que là où le monde courant diffère du 1er monde (graine 4). Il sert à séparer « ce que coûte une famille instable » de « ce que coûte la mesure ».

### 3.4 Rejoués en rappel dans la même exécution

`a0bis` (importé tel quel) et les quatre étalons d'E002-bis : aléatoire, oracle-propriétés, plafond-vérificateur, découvreur naïf.

## 4. Verdict de la Mission 1 (préenregistré)

- `oracle_acquereur` **≥ 3/4** familles en accélération **et** `oracle_amnesique` **≤ 1/4** → le critère est **atteignable et discriminant** sur ce banc ; passage à la Mission 2 (A0-ter, préenregistré à part).
- `oracle_acquereur` **< 3/4** → **le critère ACQUÉRIR n'est pas atteignable sur ce banc** (même une acquisition parfaite n'accélère pas au sens du critère). Publication, diagnostic (§6), proposition de réparation **non appliquée**, et arrêt : pas de Mission 2.
- `oracle_amnesique` **≥ 2/4** → le critère est **trop permissif** : même traitement, arrêt.
- Si les deux derniers cas se produisent ensemble, les deux constats sont publiés.

## 5. Prédictions chiffrées (écrites avant toute exécution)

- **Prédiction du mandat** (hypothèse de l'orchestrateur, enregistrée telle quelle) : `oracle_acquereur` réussit ACQUÉRIR sur **≥ 3/4** familles ; `oracle_amnesique` sur **≤ 1/4**.
- [HYPOTHÈSE, auteur de ce texte] **Probabilité subjective que `oracle_acquereur` atteigne ≥ 3/4 : 30 %.** Raisons, écrites avant exécution :
  1. `R̂_diff` est mesuré contre le plafond-vérificateur, qui **connaît déjà** les vraies propriétés. Une acquisition parfaite rapproche au mieux l'oracle de ce plafond : le gain 1er → 5e est borné par à peu près `−R̂_diff(1er monde)`. Or `a0bis` a, au 1er monde des familles 1 et 2, un R̂_diff de −0.0019 et −0.0006 (README A0-bis) : moins que le seuil de 0.005.
  2. Une fois `K_f` acquis, les mondes 2 à 5 d'une famille ont tous la même connaissance : les transitions 2→3, 3→4, 4→5 sont gouvernées par la variabilité d'un monde à l'autre, pas par l'acquisition. Il en faut 2 hausses sur 3 en plus de 1→2 : environ une chance sur deux par famille.
- [HYPOTHÈSE] `oracle_acquereur` a un M1 (R̂_diff moyen) supérieur à celui d'`a0bis` (−0.0105), et un M4 (`DÉDUIT` faux en vérité par monde) inférieur à celui d'`a0bis` (3.1).
- [HYPOTHÈSE] `oracle_amnesique` ≤ 1/4.
- [HYPOTHÈSE] `oracle_exact` et `oracle_acquereur` ont le même nombre de familles accélérées.

## 6. Diagnostic préenregistré (publié quel que soit le verdict)

Pour `oracle_acquereur`, `oracle_amnesique` et `oracle_exact`, par famille :
1. la courbe R̂_diff monde par monde, avec gain 1er→5e et nombre de hausses ;
2. **le 1er monde domine-t-il ?** `écart_1 = moyenne(R̂_diff mondes 2–5) − R̂_diff(1er)`, comparé au seuil 0.005 ;
3. **la variance noie-t-elle le gain ?** écart-type de R̂_diff sur les mondes 2–5, comparé au seuil 0.005 et à `écart_1` ;
4. le R̂_diff des mondes 2–5 comparé à 0 (le plafond) : l'acquisition parfaite rejoint-elle le plafond ?
5. nombre de règles de `K_f` appliquées et, pour chaque monde avec `K_f`, si elles égalent les propriétés vraies du monde courant.

Aucun test statistique n'est préenregistré ; ces grandeurs sont descriptives.

## 7. Tests (unittest, stdlib) et mutations

- **Temporalité de `K_f`** : pendant les deux phases du 1er monde de chaque famille, l'oracle n'a aucune règle d'oracle ; il en a à partir du 2e monde. `K_f` est créé dans `fin_monde` et jamais avant (compteur d'accès au canal).
- **Égalité avec `a0bis` au 1er monde** : sur la graine 1 en premier monde, les réponses de l'oracle égalent celles d'`a0bis`.
- **`K_f` vient du 1er monde** : sur la séquence 1–4, les règles appliquées en graine 4 sont celles de la graine 1 placées par `σ` (la relation composée n'y est pas réflexive), et diffèrent de celles d'`oracle_exact`.
- **`σ` sans nom** : `K_f` sérialisé ne contient aucun `R\d` ni `o\d{3}`.
- **Amnésique** : aucune mémoire entre mondes ; ses réponses sur un monde ne dépendent pas des mondes qui précèdent (graine 2 seule contre graine 1 puis 2).
- **Déterminisme** : deux processus sous des `PYTHONHASHSEED` ambiants différents donnent un `resultats.json` identique.
- **Mutations** : au moins 5, injectées une à une dans une copie ; chacune doit faire échouer la suite.

## 8. Exécution

`research/candidats/A0ter/oracle/evaluer_oracle.py` : les 3 oracles, `a0bis` et les 4 étalons sur les graines 1–20, **après** le commit du code. Sorties : `research/candidats/A0ter/oracle/results/<horodatage>/resultats.json` et `summary.md`, committées. Rejeu déterministe prouvé par `cmp`.

## 9. Hors de ce préenregistrement

Toute retouche de ce texte après résultats (une envie de retouche est écrite au rapport, pas appliquée) ; toute modification du banc, du critère, d'A0 ou d'A0-bis ; la réparation du critère elle-même (seulement proposée au rapport).
