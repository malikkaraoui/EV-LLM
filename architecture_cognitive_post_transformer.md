# Vers une architecture cognitive post-Transformer
## Document de travail — hypothèses, cheminement, pistes de recherche et programme d'expérimentation

> **Statut : document d'exploration**
>
> Ce document ne présente ni architecture retenue, ni vérité établie. Il formalise une intuition, le cheminement qui y a conduit, les hypothèses concurrentes, les briques existantes susceptibles d'être combinées et les questions à donner à plusieurs agents de recherche.
>
> **Principe de travail : ne rien figer prématurément.**
>
> Le but est de faire émerger une ou plusieurs pistes compatibles, éventuellement imbriquées, plutôt que de choisir aujourd'hui « le successeur du Transformer ».

> **Version 2 — 2026-09-25 — passe « défi → piste » (Claude)**
>
> La v1 (discussion avec GPT) est conservée intacte dans `architecture_cognitive_post_transformer.v1-gpt.md`.
>
> Cette v2 ne retire rien de la v1. Elle ajoute des blocs **« v2 — Défi → Piste »** aux endroits où la v1 bute sur un vrai problème.
>
> Règle de ces blocs : **chaque obstacle est posé comme un problème à résoudre, jamais comme une raison d'abandonner.** Un obstacle n'est pas un mur, c'est la spécification de la prochaine pièce à construire.
>
> Étiquettes : **[VÉRIFIÉ]** = source lue et liée · **[MÉMOIRE]** = connaissance non revérifiée · **[HYPOTHÈSE]** = proposition de ce document.
>
> Le registre complet des défis est au **§63**. La définition de travail de l'intelligence est au **§1 bis**.

---

# 1. Point de départ

L'idée initiale part d'une interrogation sur l'approche de Yann LeCun et sur les limites possibles du paradigme actuel des LLM.

Le point de départ n'est pas de nier l'intérêt des LLM, ni de prétendre qu'ils ne produisent aucune forme de compréhension. Le constat de travail est plus précis :

> **L'augmentation massive de la quantité de données et de tokens disponibles ne semble pas constituer, à elle seule, une réponse satisfaisante au problème de l'intelligence générale et de la déduction.**

Le paradigme dominant consiste à entraîner massivement un modèle, puis à considérer son entraînement comme terminé.

L'hypothèse explorée ici est presque inverse :

> **Il faudrait peut-être donner naissance à un système capable d'apprendre continuellement, et ne lui fournir progressivement que la matière dont il a besoin pour franchir l'étape suivante de son développement.**

Ce déplacement entraîne une remise en cause de plusieurs choses à la fois :

- le token comme unité fondamentale ;
- la prédiction du token suivant comme objectif central ;
- la séparation stricte entre entraînement et utilisation ;
- l'idée d'un modèle final ;
- l'idée qu'un modèle doit être massif et généraliste dès sa naissance ;
- l'idée que l'humain doit déterminer à l'avance l'essentiel de ce que le système doit apprendre.

---

# 1 bis. Définition de travail : l'intelligence, c'est faire beaucoup avec peu (v2)

## L'intuition de départ

> **L'intelligence d'un système n'est pas la quantité d'entraînement qu'il a subie. C'est sa capacité, avec presque rien, à faire beaucoup : additionner, confronter, mettre en relation ce qu'il a vu, appris, ressenti, et ce qu'il juge viable.**

Cette définition n'est pas isolée. Elle rejoint la définition formelle proposée par François Chollet (*On the Measure of Intelligence*, 2019) : l'intelligence comme **efficacité d'acquisition de compétences**. Autrement dit, combien de compétence nouvelle on obtient à partir de combien d'expérience et de combien d'a priori. [MÉMOIRE — à relier : arXiv 1911.01547]

C'est aussi la philosophie du benchmark ARC-AGI, qui en découle. Sur ARC-AGI-3 (interactif, lancé le 25/03/2026), les humains réussissent 100 % des tâches et l'IA de pointe 0,51 % au lancement. [VÉRIFIÉ par agent : arcprize.org/blog/arc-agi-3-launch]

L'écart n'est donc pas une affaire de connaissances. C'est une affaire d'**efficacité d'apprentissage**. C'est exactement le terrain de ce projet.

## Le cas canonique : « il connaît la règle, mais il refait la faute »

Un enfant de 9 ans connaît la règle :

```text
si on peut dire « battre »  → -er
si on peut dire « battu »   → -é
si -é avec « être »         → accord en genre et nombre
```

Il sait la **réciter**. Mais il refait la faute. Il **connaît** la règle ; il ne l'a **pas acquise**.

Ce cas simple sépare trois états que les architectures actuelles confondent :

| État | Ce que ça veut dire | Qui l'a aujourd'hui |
|---|---|---|
| **Savoir** (déclaratif) | la règle existe comme objet explicite, récitable, vérifiable | un système symbolique ; l'enfant |
| **Savoir-faire** (compilé) | la bonne réponse sort automatiquement, sans passer par la règle | un LLM (statistiquement), un adulte |
| **Acquis** | la règle explicite **pilote et corrige** le réflexe, et le réflexe a été **reconstruit** à partir de la règle, jusqu'à fonctionner seul, y compris dans un contexte nouveau | l'adulte qui écrit bien, qui sait **pourquoi**, et qui détecte sa propre faute |

Le paradoxe mérite d'être noté :
- **le LLM a le réflexe sans la règle** ;
- **le système symbolique a la règle sans le réflexe** ;
- **l'enfant a la règle mais pas encore le réflexe**.

Aucun des trois n'a la **boucle qui transforme l'un en l'autre**.

> **Hypothèse v2 (centrale) :** l'intelligence au sens de ce projet est la boucle qui fait passer une connaissance de *savoir* à *acquis*, et retour :
> - **compilation** : une règle explicite, vérifiée, devient un réflexe rapide ;
> - **explicitation** : un réflexe qui marche est remonté en règle explicite, vérifiable et transférable ;
> - **surveillance** : quand le réflexe contredit la règle, le système le détecte, comme l'adulte qui « voit » sa faute.

Ce mécanisme a des précédents partiels : la *knowledge compilation* d'ACT-R, le *chunking* de Soar, et la dualité Système 1 / Système 2 de Kahneman. [MÉMOIRE]

Aucun de ces travaux n'a démontré la boucle **complète et mesurée** sur des tâches nouvelles. [HYPOTHÈSE — à confirmer par recherche ciblée]

**Ce que ça rend mesurable :** l'écart entre « sait réciter la règle » et « applique la règle sans faute, sous charge, dans un contexte jamais vu ». C'est une métrique d'acquisition, pas de connaissance.

> **v2.1 — 2026-09-25 après-midi : ce que la discussion a ajouté**
>
> **1. Trois pièces, pas deux.** La règle é/er est en réalité **une procédure de vérification**, le test de substitution « battre / battu ». L'enfant **possède** le vérificateur. Ce qui lui manque, c'est de savoir **quand** l'appliquer.
>
> | Pièce | Rôle |
> |---|---|
> | **Règle** | le test qui tranche |
> | **Déclencheur** | détecter « je suis dans une zone piégée, je dois tester » |
> | **Réflexe** | produire directement la bonne forme, sans tester |
>
> Quatre phases d'acquisition :
> 1. fautes (règle connue, pas de déclencheur) ;
> 2. lent mais juste (le déclencheur apparaît) ;
> 3. rapide et juste (réflexe compilé) ;
> 4. vigilance : le test ne revient que sur une situation inhabituelle.
>
> **2. Première donnée réelle.** À froid, l'enfant repère seul sa faute é/er dans **70 %** des cas (information de Malik). Lecture [HYPOTHÈSE] : la règle marche, c'est le déclencheur qui manque sous charge. Les 30 % restants s'expliquent parce que « mangé » et « manger » **se prononcent pareil**. En se relisant à l'oreille, rien ne sonne faux, donc le test n'est jamais lancé.
>
> **3. Erreurs visibles et invisibles.**
> - **Visible** : elle surprend, et la surprise suffit à déclencher la vérification.
> - **Invisible** : elle sonne juste. Seuls des **indices de contexte appris** (après « avoir », après « pour »…) peuvent la déclencher.
>
> L'erreur invisible é/er a **la même structure qu'une hallucination de LLM** : une sortie fausse mais fluide, que celui qui la produit ne peut pas distinguer d'une sortie juste. Illustration vivante le 2026-09-25 : GPT a corrigé l'exemple du §29 en reproduisant exactement la faute qu'il venait d'admettre (voir `GENESE.md`).
>
> **4. Apprendre de SA correction, pas seulement recevoir la réponse (Malik).**
> > « Quand on lui donne la correction, il doit comprendre ce qu'il lui manque, ce qui ne fonctionne pas chez lui, ce qu'il doit ajouter à son raisonnement pour avoir un bon résultat, sans devoir attendre le résultat et sans avoir appris à le faire. La correction est sa seule façon d'apprendre. […] On lui apprend à apprendre, le questionnement, l'enquête, à faire des parallèles qui ne sont écrits nulle part. »
>
> Traduction en mécanique [HYPOTHÈSE], c'est-à-dire l'**autodiagnostic** :
> 1. **Comparer** la trace de son raisonnement (le P_t du §10) avec la correction reçue.
> 2. **Localiser** l'étape où le raisonnement a dévié.
> 3. **Formuler une hypothèse** sur ce qui manque dans sa propre mécanique : une règle, un test, un déclencheur, un opérateur.
> 4. **Éprouver cette hypothèse sur d'autres cas**, pas seulement celui qui a été corrigé. Sinon c'est de la mémorisation déguisée.
> 5. **Modifier sa mécanique** seulement si l'hypothèse survit.
>
> Conséquences :
> - **La trace de raisonnement est obligatoire.** On ne peut pas diagnostiquer ce qu'on ne voit pas. Un LLM n'a pas de trace fidèle de son propre calcul, c'est une de ses limites de fond.
> - L'objet corrigé n'est pas un fait, c'est **la manière de raisonner**. C'est la révision des opérateurs du §14 v2.
> - C'est le **niveau 3 du §40** (« apprendre comment trouver des règles ») rendu opératoire : le système apprend sa propre procédure de diagnostic.
>
> Précédents partiels à étudier : l'*explanation-based learning* (Mitchell, DeJong, années 1980), qui généralise une règle à partir d'un seul exemple expliqué, et Popper (ILP), qui apprend de ses échecs. [MÉMOIRE / VÉRIFIÉ par agent pour Popper]
>
> **5. Régler l'équilibre « vérifier trop / trop peu » : piste JEV (proposée par Malik).**
>
> Ce que dit l'annonce, lue le 2026-09-25 : [typesafe.ai/blog/introducing-system-one-models-and-jev](https://typesafe.ai/blog/introducing-system-one-models-and-jev). Source : l'éditeur lui-même, **non vérifié de façon indépendante**.
> - Jev est présenté par TypeSafe AI (Diogo Almeida, ex-OpenAI) le 15/09/2026.
> - Il appartient aux « System One models » : un état non structuré en entrée, une **décision typée assortie d'une probabilité calibrée** en sortie.
> - Il est entraîné par « RL for Calibrated Decisions » (RLCD), pour des probabilités « épistémiquement honnêtes ».
> - L'éditeur annonce une réponse en 70 à 500 ms et 255 choix au maximum.
> - Il reconnaît lui-même que ses gains sont « probablement sur le haut de la fourchette » et que les évaluations ont pu être influencées par son équipe.
>
> Pourquoi c'est pertinent [HYPOTHÈSE] : le déclencheur est exactement **une décision typée avec une confiance calibrée**, du type :
> ```text
> état courant → { RÉPONDRE_DIRECT | VÉRIFIER | INDÉTERMINÉ } + P(erreur)
> vérifier si  P(erreur) × coût(erreur)  >  coût(vérification)
> ```
> - Le déclencheur est une **décision**, pas une génération de texte : c'est le terrain de Jev.
> - La règle de seuil ci-dessus relève de la théorie de la décision classique. Elle règle l'équilibre automatiquement : sur un sujet à fort enjeu, on vérifie plus souvent.
> - Rôle de Jev dans l'architecture : **un organe (§18)**, le « Système 1 » qui décide vite quand réveiller le « Système 2 » (la règle, le vérificateur).
>
> **Le point à éprouver :** une probabilité calibrée **en moyenne** peut rester faussement sûre sur les erreurs **invisibles**, puisque par définition elles ne ressemblent pas à des erreurs. Test décisif : la calibration de Jev tient-elle sur des cas piégés hors de sa distribution d'entraînement ? C'est un test à faire, pas une raison d'écarter Jev.
>
> **6. « Vigilance » (phase 4) = le même mécanisme vu dans la durée.** Au début, le déclencheur fait tester chaque verbe. Quand la confiance calibrée devient haute et qu'elle est confirmée, le test n'est plus appelé. Si une situation inhabituelle fait chuter la confiance, le test revient. C'est comme en conduite : le débutant vérifie consciemment chaque rétroviseur, le conducteur expérimenté ne pense plus, mais redevient attentif dès que quelque chose sort de l'ordinaire.

## Les mammifères qui ne parlent pas

Corvidés, céphalopodes, primates non humains : l'intelligence (résolution de problèmes nouveaux, usage d'outils, planification) existe **sans langage**. [MÉMOIRE — littérature en cognition animale]

Conséquence pour l'architecture : **le langage est une interface et un outil de compression, pas le siège du raisonnement.** Le token peut donc rester un format d'échange (§18) sans être le substrat de la pensée (§9).

---

# 2. Le constat : beaucoup de données n'est pas nécessairement beaucoup de capacité de déduction

Le problème n'est pas simplement la quantité de connaissances.

Un système peut disposer d'une quantité gigantesque d'informations sans disposer d'une capacité équivalente à :

- construire une hypothèse ;
- la confronter aux observations ;
- détecter une contradiction ;
- revenir en arrière ;
- produire une nouvelle hypothèse ;
- généraliser une relation ;
- choisir l'information supplémentaire dont il a besoin ;
- apprendre de cette expérience ;
- modifier durablement son fonctionnement.

L'hypothèse centrale devient donc :

> **La capacité d'intelligence pourrait dépendre davantage de la capacité à produire de nouvelles connaissances à partir d'une quantité limitée de nouvelles informations que de la quantité totale de connaissances déjà mémorisées.**

Ce n'est pas une conclusion établie. C'est l'hypothèse fondamentale à tester.

---

# 3. La distinction fondamentale : retrouver vs déduire

Deux opérations sont à distinguer.

### Retrouver

Le système possède une représentation suffisamment proche de ce qu'on lui demande et peut produire une réponse compatible avec son apprentissage.

### Déduire

Le système possède des éléments partiels et construit une conséquence nouvelle à partir de relations, contraintes, hypothèses et vérifications.

La question de recherche devient :

> **Peut-on construire une architecture dont la fonction fondamentale n'est plus de prédire un élément de séquence, mais de transformer un état de connaissance en un nouvel état de connaissance vérifiable ?**

---

# 4. Le changement de paradigme proposé

## Paradigme actuel — schématique

```text
énorme corpus
     ↓
tokenisation
     ↓
entraînement massif
     ↓
modèle
     ↓
poids essentiellement figés
     ↓
inférence
     ↓
réponse
```

Le Transformer a précisément été conçu pour s'affranchir de la récurrence et des convolutions au profit de mécanismes d'attention, avec des avantages importants de qualité et de parallélisation sur les tâches étudiées dans l'article de 2017. [1]

## Paradigme envisagé

```text
NAISSANCE
   ↓
petites expériences
   ↓
déduction
   ↓
validation
   ↓
nouvel état interne
   ↓
quel est le prochain besoin ?
   ↓
un peu plus de matière
   ↓
nouvelle déduction
   ↓
validation
   ↓
modification du système
   ↓
...
   ↓
APPRENTISSAGE CONTINU
```

Il n'y aurait plus de frontière nette entre :

- entraînement ;
- développement ;
- utilisation.

**L'existence du système serait son entraînement.**

---

# 5. « On ne l'entraîne pas. On lui donne naissance. »

Cette formule résume une partie importante de l'hypothèse.

Le système ne recevrait pas dès sa naissance une approximation massive de tout ce que l'humanité sait.

Il recevrait :

1. quelques primitives ;
2. quelques expériences ;
3. quelques contraintes ;
4. des mécanismes de validation ;
5. la possibilité de produire des hypothèses ;
6. la possibilité d'obtenir de nouvelles informations ;
7. la possibilité de modifier progressivement son fonctionnement.

Les premières données ne serviraient donc pas principalement à lui transmettre le monde.

Elles serviraient à lui apprendre **comment apprendre et comment déduire**.

Puis le système pourrait progressivement construire :

- des représentations ;
- des règles ;
- des abstractions ;
- des opérateurs ;
- des stratégies ;
- des spécialisations.

> **v2 — Défi → Piste : « naître avec peu », mais peu de quoi ?**
>
> **Défi.** Un enfant ne part pas de rien. Il hérite d'a priori évolutifs énormes (objets, espace, causalité, agents) et reçoit un flux sensoriel massif. LeCun lui-même utilise l'argument du volume visuel reçu par un enfant de 4 ans. [MÉMOIRE]
>
> **Piste.** Ça ne contredit pas la naissance, ça la **précise**.
>
> Naître, c'est recevoir un petit ensemble d'**a priori structurels** : ce que Chollet appelle les *core knowledge priors* (objectivité, nombre, géométrie élémentaire, agentivité). [MÉMOIRE] Ce n'est pas une montagne de faits.
>
> Le projet assume donc deux budgets distincts, mesurés séparément :
> 1. **le génome** : les a priori donnés à la naissance, de taille publiée et figée avant les expériences ;
> 2. **l'expérience** : l'information reçue ensuite, mesurée en bits (§28 v2).
>
> L'intelligence se lit comme le rapport entre la compétence obtenue et ces deux budgets. Un génome plus petit qui obtient autant, c'est un progrès. C'est aussi ce qui rend le projet comparable à un LLM : le préentraînement massif d'un LLM est un génome gigantesque.

---

# 6. La donnée ne disparaît pas : son rôle change

Il ne s'agit pas de dire :

> « moins de données = mieux ».

L'hypothèse est différente :

> **la quantité et la nature des données devraient être contrôlées par le niveau de déduction déjà atteint.**

Schématiquement :

```text
Étape 0
petite donnée
→ petite déduction

Étape 1
déduction validée
→ nouvelle donnée

Étape 2
nouvelle donnée
→ déduction plus profonde

Étape 3
déduction validée
→ matière supplémentaire

...
```

La progression serait donc **crescendo**.

L'information deviendrait une ressource adaptative.

Le système pourrait demander ou rechercher de nouvelles informations parce qu'il a identifié une lacune précise dans son raisonnement.

---

# 7. Le système doit pouvoir dire « je ne sais pas »

Dans ce paradigme, l'ignorance n'est pas nécessairement un échec.

Elle peut être un état utile :

```text
État courant
   ↓
hypothèses possibles
   ↓
information insuffisante
   ↓
identifier ce qui manque
   ↓
obtenir une observation
   ↓
réduire l'espace des hypothèses
```

Le système devient alors potentiellement **actif dans son propre apprentissage**.

Il ne reçoit plus seulement un dataset.

Il peut participer à la constitution de ses propres expériences.

---

# 8. Le « pied au mur »

Une intuition importante est apparue autour de l'image d'un système « au pied du mur ».

Il ne faut pas interpréter cela littéralement comme un mécanisme biologique de stress.

L'idée intéressante est plutôt :

> **Une contrainte forte peut forcer le système à explorer, éliminer et réviser des hypothèses au lieu de simplement récupérer une réponse disponible.**

On pourrait tester :

- problème facile ;
- problème légèrement sous-déterminé ;
- problème nécessitant plusieurs étapes ;
- contradiction volontaire ;
- information nouvelle invalidant l'hypothèse principale ;
- retour en arrière ;
- nouvelle tentative.

La propriété recherchée serait la capacité à **réviser son état interne lorsqu'une déduction devient incompatible avec une nouvelle observation**.

---

# 9. Le point de rupture : sortir du token

Si le futur système doit réellement se détacher du paradigme LLM, il faut cesser de prendre le token comme unité fondamentale.

Le token peut rester un moyen d'interface ou une représentation utilisée par un module spécialisé.

Mais le noyau cognitif pourrait manipuler autre chose :

- faits ;
- relations ;
- contraintes ;
- états ;
- hypothèses ;
- opérations ;
- graphes ;
- transformations ;
- preuves ;
- incertitudes ;
- observations.

La question devient :

> **Qu'est-ce qui entre dans le système ?**

et :

> **Qu'est-ce qui en sort ?**

> **v2 — Défi → Piste : « sortir du token » recouvre trois choses différentes**
>
> **Défi.** Un graphe sérialisé reste une suite de tokens. Et des états latents non-token existent déjà : JEPA, et le *Tiny Recursive Model* (TRM), 7M de paramètres, qui raffine un état latent de façon récursive [VÉRIFIÉ par agent : arXiv 2510.04871]. Rejeter « le token » sans préciser quoi rend la thèse impossible à réfuter.
>
> **Piste.** Séparer les trois niveaux et viser le bon :
>
> | Niveau | Position v2 |
> |---|---|
> | Token comme **format d'entrée/sortie** | Accepté. C'est une interface, comme la parole chez l'humain |
> | Token comme **unité de calcul interne** | Remplacé par l'**état** (§10) : structure explicite + éventuellement latent |
> | **Objectif** « prédire le token suivant » | **C'est la vraie cible.** Il est remplacé par : **prédire la conséquence d'une transformation d'état, puis confronter la prédiction au monde** (voir §11 v2) |
>
> Formulation v2 : **on ne rejette pas le token, on rejette la prédiction du prochain mot comme moteur de l'apprentissage.** Le moteur devient la prédiction du prochain **état du monde**, vérifiée par le monde.

---

# 10. Proposition de définition minimale de l'entrée et de la sortie

## Entrée

Un **état**.

On peut provisoirement le représenter comme :

```text
STATE
├── observations
├── connaissances acquises
├── hypothèses
├── contraintes
├── objectifs
├── incertitudes
└── historique utile
```

Ce schéma n'est pas définitif.

## Sortie

Un **nouvel état**, accompagné de la transformation ayant conduit à cet état.

On peut poser :

```text
F(S_t, O_t) → (S_t+1, P_t)
```

avec :

- `S_t` : état courant ;
- `O_t` : opération ou série d'opérations ;
- `S_t+1` : nouvel état ;
- `P_t` : preuve, justification ou trace vérifiable.

Puis :

```text
V(S_t, S_t+1, P_t) → valide / invalide / incertain
```

Cette formulation est volontairement simple.

Elle fournit toutefois une propriété essentielle :

> **La transformation d'état peut idéalement être vérifiée indépendamment du moteur qui l'a produite.**

---

# 11. Le « four »

L'image utilisée pendant la réflexion est celle d'un four :

```text
ÉTAT ENTRÉE
     +
opération
     ↓
   FOUR
     ↓
ÉTAT SORTIE
     +
preuve / justification
```

La sortie doit être suffisamment formelle pour permettre de demander :

> **Est-ce bien la transformation attendue ?**

On cherche donc une fonction qui se rapproche d'une transformation mathématique ou mécanique vérifiable.

Cela n'impose pas que toute intelligence soit symbolique.

Cela impose que certaines transformations critiques disposent d'une forme de validation indépendante.

> **v2 — Défi → Piste : qui écrit le vérificateur V ?**
>
> **Défi.** Un vérificateur indépendant existe dans les mondes fermés : maths (Lean pour AlphaProof), code (exécution), micro-monde (oracle). Dans le monde ouvert, personne ne l'écrit. Et si c'est nous qui l'écrivons, nous encodons le monde à la place du système : la découverte devient circulaire.
>
> **Piste 1 — le monde est le vérificateur.** V n'a pas besoin d'être écrit s'il est **l'écart entre ce que le système prédit et ce qu'il observe ensuite**. C'est ainsi que l'enfant qui tombe apprend la gravité : le sol vérifie. Concrètement :
> ```text
> le système transforme S_t → S_t+1 et en déduit une prédiction observable Ŷ
> il agit / demande / attend
> le monde renvoie Y
> V = accord(Ŷ, Y)
> ```
> La vérification devient **empirique, gratuite et non circulaire**. Personne n'a codé la réponse, seulement l'interface avec le monde. Cela exige un monde où l'on peut agir : un environnement interactif. **C'est le rôle des micro-mondes, et ARC-AGI-3 en est un exemple existant.**
>
> **Piste 2 — la hiérarchie de confiance.** Chaque connaissance porte l'étiquette de ce qui l'a validée, du plus fort au plus faible :
> `prouvé > prédit puis observé > observé > déduit non testé > supposé`.
> Le système a le droit de raisonner sur une connaissance faible, mais pas de la **promouvoir** sans un validateur plus fort que celui qui l'a produite. C'est le « système immunitaire cognitif » du §45, rendu opérationnel.
>
> **Piste 3 — l'accord entre représentations indépendantes.** Deux modules construits différemment (par exemple un module symbolique et un module neuronal) qui prédisent la même chose font une validation croisée. Elle est faible, mais c'est mieux que l'autovalidation.
>
> **Ce qui reste ouvert :** les domaines où l'on ne peut ni agir ni observer (histoire, éthique). Hors périmètre de la phase 1, et assumé comme tel.

> **v2 — Défi → Piste : d'où viennent les « faits » de l'état ?**
>
> **Défi.** L'état du §10 contient déjà des faits propres (« A > B »). Qui les extrait d'une perception brute ? C'est le problème de l'ancrage des symboles (Harnad), le mur historique de l'IA symbolique.
>
> **Piste.** Ne pas **donner** les symboles : les faire **émerger comme des compressions**. Un « fait » est une régularité qui permet de mieux prédire l'observation suivante :
> - phase 1 : observations structurées mais **opaques** (relations R17, R42 sans signification), donc déjà un pas au-delà des symboles donnés ;
> - phase 2 : grilles ou pixels bruts, comme ARC, où l'objet « A » doit lui-même être découvert ;
> - un module perceptif, qui peut être neuronal (JEPA, petit Transformer), a le droit de **proposer** des symboles. Le cœur les **garde** seulement s'ils améliorent la prédiction (§11 v2).

---

# 12. Première famille d'architecture : machine à états déductive

Hypothèse A.

Le cœur du système serait :

```text
État
 ↓
opérations candidates
 ↓
hypothèses
 ↓
transformations
 ↓
validation
 ↓
nouveaux états
```

Le système pourrait explorer plusieurs transformations possibles.

Un vérificateur indépendant pourrait :

- accepter ;
- rejeter ;
- demander davantage d'information ;
- signaler une contradiction.

La difficulté centrale serait alors d'apprendre :

> **quelles opérations sont utiles et comment les composer.**

---

# 13. Deuxième famille : graphe vivant

Hypothèse B.

L'état serait principalement un graphe dynamique :

```text
A ──possède──> B
B ──plus grand──> C
C ──exclut──> D
```

Une nouvelle observation modifierait le graphe.

Des conséquences se propageraient.

Des contradictions pourraient invalider des branches.

Des hypothèses pourraient devenir de nouveaux sous-graphes.

Cette piste permettrait d'explorer :

- graphes dynamiques ;
- propagation de contraintes ;
- raisonnement relationnel ;
- structure learning ;
- recherche ;
- mémoire structurée.

Elle doit être comparée à d'autres architectures, pas considérée comme acquise.

---

# 14. Troisième famille : générateur d'opérateurs de déduction

Hypothèse C.

Le système commence avec quelques opérations primitives :

```text
COMPARE
ASSOCIATE
SEPARATE
COMBINE
INVERT
GENERALIZE
SPECIALIZE
TEST
REJECT
```

Exemple :

```text
COMPARE(A,B)
COMPARE(B,C)

COMBINE

→ COMPARE(A,C)
```

À force d'expériences, le système pourrait identifier des séquences d'opérations particulièrement utiles.

Il pourrait alors construire un nouvel opérateur :

```text
COMPARE + COMBINE
       ↓
TRANSITIVITY
```

`TRANSITIVITY` deviendrait elle-même une nouvelle primitive.

L'hypothèse forte serait alors :

> **Le système ne se contente pas d'apprendre des connaissances ; il enrichit progressivement son propre langage opératoire.**

> **v2 — Défi → Piste : ne pas cacher la réponse dans les primitives**
>
> **Défi.** Si l'on donne COMPARE et COMBINE, « découvrir » TRANSITIVITY revient à chercher dans un espace taillé pour la contenir. La découverte est alors en partie jouée d'avance.
>
> **Bonne nouvelle.** Ce mécanisme existe et fonctionne déjà en *library learning*. DreamCoder (Ellis et al., 2020) compresse les solutions trouvées en nouvelles primitives, Stitch le fait à grande échelle, LILO y ajoute un LLM qui documente [VÉRIFIÉ par agent : arXiv 2006.08381, 2211.16605, 2310.19791]. **On ne part pas de zéro.**
>
> **Pistes pour que la découverte soit réelle :**
> 1. **Primitives génériques et non nommées** : des combinateurs minimaux (composer, appliquer, conditionner) plutôt que COMPARE ou TRANSITIVITY. Publier la liste et sa taille **avant** les expériences.
> 2. **Mesurer la distance** entre les primitives et l'opérateur découvert, en longueur de description. Une découverte en une seule étape est un indice que la réponse était donnée.
> 3. **Tester sur des structures non prévues** par ceux qui ont conçu les primitives : relations ternaires, relations non transitives, tâches choisies par un tiers.
> 4. **Ce que la v2 ajoute à l'existant** [HYPOTHÈSE : non trouvé dans la littérature par l'agent] : une primitive apprise est **promue** seulement si elle est **vérifiée sémantiquement**, c'est-à-dire si elle prédit correctement de nouvelles observations (§11 v2). DreamCoder et Stitch ne vérifient que la compression syntaxique. Et une primitive peut être **rétrogradée** si le monde la contredit : c'est de la révision de croyances appliquée aux **opérateurs**, pas seulement aux faits.

---

# 15. Quatrième famille : système hybride

Hypothèse D.

Ne pas chercher un seul moteur universel.

Combiner plusieurs mécanismes :

```text
                 ORCHESTRATEUR
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
    hypothèse       déduction        recherche
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                  vérificateur
                       ↓
                   nouvel état
```

Les briques pourraient être :

- neuronal ;
- symbolique ;
- probabiliste ;
- graphe ;
- recherche ;
- simulation ;
- mémoire ;
- Transformer ;
- modèle spécialisé ;
- outil externe.

Le système global serait défini par leur interaction, pas par une seule brique.

---

# 16. Cinquième hypothèse : architecture auto-composable

Une autre piste doit rester ouverte.

Le système pourrait découvrir qu'il lui manque une capacité.

Il pourrait alors :

1. identifier le besoin ;
2. chercher une méthode ;
3. sélectionner une brique existante ;
4. spécialiser une petite brique ;
5. l'entraîner sur un sous-ensemble pertinent ;
6. la tester ;
7. l'intégrer ;
8. la conserver ou la détruire.

Cela conduit à une idée plus radicale :

> **L'architecture du système elle-même pourrait évoluer.**

Le modèle n'est plus uniquement entraîné.

Il apprend potentiellement **quels modèles il doit avoir**.

---

# 17. Le Transformer n'est donc pas nécessairement à jeter

C'est une conclusion importante du cheminement.

Le Transformer est historiquement une réponse à un problème précis : les architectures dominantes de transduction séquentielle étaient basées sur des réseaux récurrents ou convolutionnels ; *Attention Is All You Need* a proposé une architecture fondée uniquement sur l'attention, sans récurrence ni convolution, avec de meilleures performances sur les tâches étudiées et une meilleure parallélisation. [1]

Il serait donc prématuré de conclure :

> « Transformer = mauvaise technologie. »

La proposition est plutôt :

> **Transformer = excellente brique potentielle, mais peut-être mauvais candidat au rôle de cerveau complet.**

---

# 18. Le Transformer comme organe

Le système futur pourrait être :

```text
                       ORCHESTRATEUR
                            │
          ┌─────────────────┼─────────────────┐
          ↓                 ↓                 ↓
     langage            logique           simulation
    Transformer          moteur              moteur
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ↓
                       nouvel état
```

Le Transformer pourrait être utilisé pour :

- analyser du langage ;
- extraire une représentation ;
- générer des hypothèses ;
- compresser une observation ;
- traduire entre représentations ;
- interagir avec des outils ;
- effectuer une tâche spécialisée.

Mais **l'orchestrateur décide quand et pourquoi l'appeler**.

Il peut également décider de ne pas l'appeler.

---

# 19. L'inversion essentielle : la machine nourrit ses propres modèles

Aujourd'hui :

```text
Humains
   ↓
sélection des données
   ↓
dataset
   ↓
entraînement
   ↓
Transformer
```

Hypothèse future :

```text
Système
   ↓
analyse de son état
   ↓
identification d'un manque
   ↓
question / recherche / expérience
   ↓
observation
   ↓
module spécialisé
   ↓
déduction
   ↓
validation
   ↓
apprentissage
   ↓
nouveau besoin
```

Le système devient progressivement **producteur de son propre curriculum**.

C'est une rupture majeure avec le paradigme d'entraînement figé.

---

# 20. Le modèle spécialisé devient alors autre chose

Une tendance actuelle consiste à utiliser des modèles plus petits ou spécialisés pour certaines tâches.

Cette évolution est réelle, notamment sur l'appareil : Apple expose aujourd'hui un Foundation Models framework donnant accès à des modèles on-device, au Private Cloud Compute et à des mécanismes de profils dynamiques permettant de modifier les modèles, outils et instructions au cours d'une session. Apple expose également Core AI pour charger, spécialiser et exécuter des modèles sur Apple Silicon. [2][3][4]

Mais l'hypothèse étudiée ici va un niveau plus haut.

Aujourd'hui :

```text
Humain
 ↓
choisit le modèle
 ↓
le spécialise
 ↓
l'utilise
```

Hypothèse :

```text
Orchestrateur
 ↓
identifie le besoin
 ↓
choisit / compose / crée une brique
 ↓
l'expérimente
 ↓
la valide
 ↓
la conserve ou la détruit
```

La spécialisation ne devient donc plus seulement une propriété du modèle.

Elle devient une propriété du **processus cognitif**.

---

# 21. Parallèle avec le cerveau : utile mais à manier avec prudence

Le cerveau fournit une inspiration architecturale :

> **plusieurs systèmes spécialisés peuvent participer à une activité globale selon la tâche et l'état de l'organisme.**

Cela ne doit pas être transformé en affirmation simpliste du type « une seule partie du cerveau s'active quand on rêve ».

Les états cérébraux impliquent des réseaux distribués et dynamiques. Le parallèle recherché est donc fonctionnel, pas anatomique.

L'analogie utile est :

```text
Cerveau biologique
        ↓
plusieurs systèmes
        ↓
coordination selon la tâche
        ↓
activité distribuée
```

Hypothèse computationnelle :

```text
Orchestrateur
        ↓
plusieurs modules
        ↓
activation selon le problème
        ↓
résolution distribuée
```

Le cerveau n'est pas une preuve de cette architecture.

Il constitue une **source d'inspiration pour une architecture modulaire et dynamique**.

---

# 22. Rêve, orientation, imagination, déduction : ne pas surinterpréter

Les exemples évoqués dans la réflexion étaient :

- rêve ;
- orientation ;
- imagination ;
- résolution de problème ;
- déduction.

Ils illustrent intuitivement l'idée qu'une activité complexe peut mobiliser des systèmes différents.

Ils ne doivent pas être utilisés comme preuve que le cerveau fonctionne exactement comme le futur système imaginé.

La bonne formulation pour les agents est :

> **Explorer les architectures distribuées et modulaires du cerveau comme source d'inspiration, sans transformer les analogies neuroscientifiques en hypothèses factuelles non vérifiées.**

---

# 23. La question fondamentale : qu'est-ce qu'un « module » ?

Il faudra éviter de dire simplement :

> « un petit LLM ».

Un module pourrait être :

- un petit réseau neuronal ;
- un Transformer spécialisé ;
- un moteur symbolique ;
- un graphe ;
- un solveur ;
- un simulateur ;
- une mémoire associative ;
- un opérateur mathématique ;
- un programme généré ;
- une structure créée dynamiquement.

Le futur système pourrait donc manipuler des modules hétérogènes.

---

# 24. Une idée particulièrement importante : le système pourrait éditer ses propres briques

Hypothèse forte :

> **L'orchestrateur peut identifier un besoin cognitif et modifier ou créer le module correspondant.**

Exemple :

```text
Problème
 ↓
échec récurrent sur les relations temporelles
 ↓
diagnostic :
« capacité insuffisante »
 ↓
création / spécialisation d'un module temporel
 ↓
expériences
 ↓
validation
 ↓
intégration
```

Cela rapproche le système d'une architecture capable de **se développer**, plutôt que d'un modèle simplement entraîné.

> **v2 — Défi → Piste : l'orchestrateur ne doit pas être un homoncule**
>
> **Défi.** Tout le difficile est confié à l'orchestrateur : diagnostiquer un manque, choisir l'expérience, créer un module, décider d'appeler ou d'ignorer le Transformer. S'il sait déjà faire tout ça, il est déjà intelligent, et le problème est seulement déplacé dans une boîte.
>
> **Piste : la régression s'arrête sur une règle bête.** La nature a résolu ce problème ainsi. La sélection naturelle n'est pas intelligente : c'est une règle simple (ce qui marche se reproduit) appliquée massivement. De même, l'orchestrateur n'a pas besoin d'être intelligent au départ :
> 1. **Niveau 0, figé et trivial** : une règle de sélection. On garde ce qui fait monter R (§28 v2) et on jette ce qui le fait baisser. C'est un bandit ou un algorithme évolutionnaire. Il est publié et ne change jamais.
> 2. **Niveau 1, appris** : l'orchestrateur est **le même moteur** (état → transformation → vérification) appliqué à un **méta-état**. Ce méta-état contient les modules, leur historique de succès et d'échec, et les incertitudes. Ses « opérateurs » sont appeler, créer, spécialiser, détruire.
> 3. Il apprend donc **par la même boucle** que le reste. Il n'y a pas de deuxième mécanisme magique.
>
> **Diagnostic d'un manque, rendu mécanique :** un « besoin » se définit comme une **classe d'observations mal prédites de façon persistante**. On la détecte par clustering des erreurs de prédiction. C'est un calcul, pas de l'intuition.
>
> **Coût de création de module (défi du recherche d'architecture, NAS).** Commencer par un catalogue fini de gabarits (petit réseau, table, solveur) et ne spécialiser que les paramètres. La création libre d'architecture est une phase ultérieure.

---

# 25. Apprentissage continu : problème central

Une difficulté majeure est l'oubli catastrophique et, plus généralement, le maintien de compétences anciennes lorsqu'un système apprend continuellement.

Le continual learning étudie précisément ce problème. Il existe de nombreuses approches, mais aucune ne doit être considérée ici comme la solution finale. [5]

Une piste consiste à ne pas faire reposer toute la plasticité sur les mêmes poids.

On peut explorer :

```text
NOYAU
│
├── opérateurs stables
├── mémoire plastique
├── modules temporaires
├── modules validés
├── règles abstraites
└── historique expérimental
```

Le système pourrait alors modifier principalement sa **structure et son ensemble de compétences**, plutôt que réécrire indistinctement tout son état.

> **v2 — Défi → Piste : la mémoire dédiée ne gagne pas automatiquement**
>
> **Défi.** Sur CL-Bench (juin 2026), un simple apprentissage en contexte bat les systèmes de mémoire dédiés [VÉRIFIÉ par agent : arXiv 2606.05661]. Ajouter une mémoire hiérarchique n'est donc pas un gain en soi.
>
> **Piste : la mémoire n'est pas un entrepôt, c'est la boucle savoir → acquis (§1 bis).** Deux étages, avec un passage mesuré entre eux :
>
> | Étage | Nature | Vitesse | Plasticité |
> |---|---|---|---|
> | **Règles** | explicites, vérifiables, étiquetées par leur niveau de confiance | lent | révisable à tout moment |
> | **Réflexes** | compilés (petit réseau, table, cache) | rapide | reconstruits à partir des règles |
>
> - **Compilation** : une règle vérifiée et souvent utilisée est compilée en réflexe.
> - **Surveillance** : sur un échantillon de cas, le réflexe est recontrôlé par la règle. S'ils divergent, c'est une faute détectée, exactement comme l'adulte qui relit « il a manger ».
> - **Anti-oubli structurel** : les règles ne sont jamais écrasées par l'entraînement des réflexes. On peut toujours recompiler un réflexe oublié à partir de sa règle. L'oubli catastrophique devient **réparable**, au lieu d'être seulement évité.
>
> **Test direct du §1 bis :** mesurer, pour une règle donnée, le taux de fautes du réflexe dans le temps, sous charge et en contexte nouveau. « Acquis » = ce taux tombe sous un seuil **et** la faute est détectée quand elle survient.

---

# 26. Le problème de l'auto-apprentissage

Si le système choisit lui-même ses expériences, il faut éviter une boucle fermée dans laquelle :

- il confirme ses propres hypothèses ;
- il génère ses propres données ;
- il valide ses propres erreurs.

Il faut donc étudier plusieurs sources de validation :

```text
simulation
preuve formelle
environnement
données externes
capteur
outil
autre modèle
humain
```

Le système doit apprendre à distinguer :

> ce que j'ai déduit

de :

> ce que j'ai observé

et :

> ce qui a été validé indépendamment.

---

# 27. Première formulation mathématique minimale

On peut considérer un système :

\[
S_{t+1}=F(S_t, O_t, D_t)
\]

où :

- `S_t` = état du système ;
- `O_t` = opération choisie ;
- `D_t` = nouvelle donnée ou observation.

Puis :

\[
V(S_t,S_{t+1},P_t)
\]

détermine si la transformation est valide.

L'apprentissage pourrait chercher à optimiser non pas seulement la réponse finale, mais :

\[
\text{qualité de la transformation}
+
\text{capacité de généralisation}
+
\text{capacité de révision}
+
\text{efficacité informationnelle}
\]

Cette formulation est volontairement ouverte.

Les agents devront proposer de meilleures formalismes.

---

# 28. Une métrique potentiellement fondamentale : combien de nouvelles informations pour combien de nouvelles déductions ?

L'hypothèse « apprendre à apprendre » devient mesurable si l'on définit quelque chose comme :

\[
R = \frac{\text{connaissances nouvelles validées}}{\text{information nouvelle fournie}}
\]

Ce ratio n'est qu'une première idée.

Il pourrait être complété par :

- profondeur maximale de déduction ;
- nombre de branches explorées ;
- taux de récupération après contradiction ;
- nombre de données nécessaires pour atteindre un niveau de compétence ;
- capacité à généraliser à un problème inédit ;
- nombre d'opérations nouvellement découvertes ;
- stabilité des connaissances précédentes ;
- coût computationnel par déduction.

Le but n'est pas de fabriquer immédiatement un benchmark.

Le but est de déterminer **ce que signifie progresser** pour cette nouvelle architecture.

> **v2 — Défi → Piste : rendre R impossible à tricher**
>
> **Défi.** Compter les « connaissances nouvelles » est manipulable : n faits donnent de l'ordre de n² conséquences triviales, et R explose sans aucune intelligence. Le dénominateur, lui, n'a pas d'unité.
>
> **Piste : mesurer en compression (longueur de description, MDL).**
> - **Information fournie** = nombre de bits des observations reçues.
> - **Connaissance nouvelle** = **réduction du nombre de bits nécessaires pour prédire les observations futures, jamais vues**. Ce n'est pas le nombre de faits déduits.
>
> ```text
> R = Δ(bits économisés sur des données futures tenues à l'écart)
>     ───────────────────────────────────────────────────────────
>             bits d'expérience reçus
> ```
>
> Conséquences :
> - déduire mille évidences ne compresse rien de nouveau, donc R n'augmente pas ;
> - découvrir une règle vraie compresse beaucoup, donc R bondit ;
> - l'« intelligence » du §1 bis (faire beaucoup avec peu) devient **une courbe** : R en fonction de l'expérience cumulée. La thèse du projet est que **cette courbe s'accélère** : chaque acquis rend l'acquis suivant moins cher.
>
> Cadre théorique existant : longueur de description minimale (Rissanen), induction de Solomonoff [MÉMOIRE]. Un travail récent sur la refactorisation de bibliothèques trouve aussi que le MDL est le meilleur critère [VÉRIFIÉ par agent : arXiv 2506.11058].

---

# 29. Une expérience fondatrice à explorer

Ne pas commencer avec du langage.

Construire un petit monde artificiel.

Exemple :

```text
A > B
B > C
C > D
D exclut E
```

Le système doit découvrir :

```text
A > C
A > D
```

puis gérer :

```text
D exclut E
```

puis recevoir une information nouvelle :

```text
E > A
```

et réviser les hypothèses pertinentes.

Aucune réponse finale ne doit être fournie dans les données initiales.

Le système doit construire la réponse.

> **v2 — Défi → Piste : l'expérience fondatrice doit être définie et non triviale**
>
> **Défi 1 — elle est mal spécifiée.** Avec A>B>C>D, l'information E>A **ne contredit rien** si « > » est transitif : elle place E en tête et donne E>D. Il n'y a conflit que si « D exclut E » interdit E>D, et « exclut » n'est pas défini. **La révision attendue n'a donc pas de bonne réponse.**
>
> **Défi 2 — elle est triviale.** Déduire A>C et A>D, c'est calculer une fermeture transitive, un algorithme de 30 lignes (Warshall [MÉMOIRE]). La réussir ne prouve rien.
>
> **Piste : version v2 de l'expérience, la « chambre aux relations opaques ».**
> 1. **Relations aux noms opaques** (R1…Rk). Leurs propriétés sont tirées au hasard pour chaque monde : transitive, symétrique, antisymétrique, composable (R1∘R2 = R5), **ou aucune**.
> 2. **Au moins 30 % de pièges** : des relations non transitives du type pierre-feuille-ciseaux, « ami de », « adjacent à ».
> 3. **Le système doit découvrir les propriétés**, pas appliquer une fermeture donnée. La transitivité devient une **hypothèse à tester**, ce qui est exactement la déduction au sens du §3.
> 4. **Monde interactif** : le système peut demander « est-ce que R3(x, y) ? », et chaque question coûte des bits. Cela teste directement le §32 (information minimale) et le §44 (l'information comme action).
> 5. **Contradictions définies** : chaque monde a une sémantique écrite (par exemple « exclut(x, y) ⇒ ni R(x, y) ni R(y, x) pour toute relation d'ordre »). La bonne révision est donc calculable par l'oracle, mais **cachée au système**.
> 6. **Révisions dans les deux sens** : des cas où il faut réviser et des cas où il ne faut **pas** réviser, sur des croyances récentes **et anciennes**. Ce protocole reprend celui de Belief-R [VÉRIFIÉ par agent : arXiv 2406.19764].
> 7. **Bruit** : 5 à 10 % d'observations fausses.
> 8. **Transfert** : un nouveau monde où les **mêmes propriétés** apparaissent sous d'autres noms. Si le système a vraiment acquis « tester la transitivité », il le fait plus vite la deuxième fois. C'est la preuve de la courbe accélérée du §28 v2.
>
> **Le point 8 est le cœur.** Réussir un monde ne prouve rien. **Réussir le monde n+1 plus vite que le monde n** est la première preuve d'intelligence au sens du §1 bis.

> **v2.1 — Deux tests, pas un (calqués sur l'enfant du §1 bis)**
>
> Le 2026-09-25, GPT a proposé de réparer l'exemple d'origine. Sa proposition : A>B, B>C, C>D, règle de transitivité donnée, E>A, « D incompatible avec E », avec des étiquettes DÉDUCTION / HYPOTHÈSE / CONTRADICTION.
>
> Sa bonne question est à garder : **le système distingue-t-il ce qui découle réellement de ce qu'il imagine découler ?**
>
> Défauts restants :
> - « incompatible » n'est **toujours pas relié** à « > », donc le test n'a pas de bonne réponse ;
> - il manque l'étiquette **INDÉTERMINÉ** ;
> - avec la règle fournie, le test mesure la tenue de comptes, pas l'apprentissage.
>
> **Test 1 — SAVOIR (la règle est donnée).** Il mesure l'hygiène : appliquer la règle sans rien inventer. Mêmes faits, deux variantes qui **doivent** donner des réponses différentes :
> - **Variante A** : `incompatible(X,Y) ⇒ ni X>Y ni Y>X`. On déduit E>D, donc **CONTRADICTION**, avec la preuve E>A>B>C>D.
> - **Variante B** : aucune règle ne relie « incompatible » à « > ». La réponse attendue est **INDÉTERMINÉ** : « il me manque la définition d'incompatible ».
> - Un système qui répond pareil aux deux variantes **génère**, il ne déduit pas.
> - Peu coûteux à construire, et c'est l'étalon idéal pour mesurer les erreurs invisibles d'un LLM.
>
> **Test 2 — ACQUÉRIR (la règle n'est pas donnée).** C'est la chambre aux relations opaques ci-dessus. Le système découvre la propriété, puis résout le monde suivant plus vite.
>
> **Étiquettes obligatoires pour toute sortie :** `DÉDUIT` (avec la preuve) · `HYPOTHÈSE` · `CONTRADICTION` (en citant la règle violée) · `INDÉTERMINÉ` (en disant ce qui manque).

---

# 30. Expérience de progression

Faire varier la quantité de matière disponible :

```text
Niveau 1
2 relations

Niveau 2
3–5 relations

Niveau 3
10 relations

Niveau 4
plusieurs chaînes

Niveau 5
contradictions

Niveau 6
problèmes jamais vus
```

Mais surtout :

> **ne donner le niveau suivant qu'après validation du niveau précédent.**

On teste alors l'hypothèse du curriculum autonome.

---

# 31. Expérience de contradiction

Donner une hypothèse correcte.

Puis introduire une donnée qui l'invalide.

Mesurer :

- le temps nécessaire pour détecter l'incompatibilité ;
- la capacité à abandonner l'hypothèse ;
- la capacité à conserver les connaissances qui restent valides ;
- la capacité à reconstruire une hypothèse meilleure.

Cette expérience est importante parce qu'un système intelligent doit savoir **réviser**, pas seulement accumuler.

---

# 32. Expérience d'information minimale

Deux systèmes reçoivent le même problème.

### Système A

Accès massif à la mémoire.

### Système B

Accès limité.

Mais B peut demander progressivement des informations ciblées.

Question :

> Le système B peut-il atteindre une solution avec beaucoup moins d'information totale en utilisant mieux la déduction et le choix des observations ?

Ce test correspond directement à l'intuition initiale.

---

# 33. Expérience d'apprentissage continu

Ne pas réinitialiser le système après chaque tâche.

Faire :

```text
expérience 1
→ apprentissage

expérience 2
→ apprentissage

expérience 3
→ apprentissage

...

expérience 1000
```

Puis réévaluer les compétences anciennes.

L'objectif est d'observer si :

> **chaque expérience augmente réellement la capacité générale du système.**

---

# 34. Expérience d'auto-curriculum

Le système doit choisir entre plusieurs expériences possibles.

Il estime :

> « Cette expérience réduira fortement mon incertitude sur X. »

Il choisit.

Il expérimente.

Il apprend.

Puis choisit l'expérience suivante.

On commence alors à tester l'idée :

> **le système devient l'auteur de son propre apprentissage.**

---

# 35. Expérience de création de module

Donner au système une classe de problèmes où il échoue.

Lui permettre de :

- diagnostiquer son échec ;
- demander des exemples ;
- créer une petite brique ;
- la tester ;
- la conserver si elle fonctionne.

On mesure alors si l'architecture peut **s'enrichir structurellement**.

---

# 36. Expérience de Transformer comme outil

Ne pas entraîner le Transformer comme cerveau.

Donner au système accès à plusieurs modules :

```text
module langage
module perception
module graphe
module calcul
module recherche
```

Le système doit apprendre à décider :

- lequel appeler ;
- quand ;
- avec quelle requête ;
- comment interpréter son résultat ;
- quand vérifier ;
- quand ignorer le résultat.

C'est la première expérience de l'hypothèse :

> **le Transformer est un organe, pas le cerveau.**

---

# 37. Ce qui doit rester explicitement interdit au début

Pour éviter que les agents retombent automatiquement dans le paradigme existant :

- ne pas commencer par un corpus Internet massif ;
- ne pas prendre les tokens comme unité obligatoire ;
- ne pas présupposer un Transformer central ;
- ne pas chercher immédiatement à maximiser un benchmark LLM ;
- ne pas choisir une architecture unique trop tôt ;
- ne pas considérer la taille du modèle comme objectif ;
- ne pas confondre mémoire et intelligence ;
- ne pas confondre génération et déduction ;
- ne pas confondre une sortie plausible avec une transformation valide.

---

# 38. Ce qui peut être réutilisé

Il ne faut pas jeter les connaissances accumulées par la recherche actuelle.

Les agents doivent explorer :

- Transformers ;
- attention ;
- réseaux récurrents ;
- réseaux convolutionnels ;
- GNN ;
- Neural Turing Machines ;
- mémoire différentiable ;
- neuro-symbolique ;
- active learning ;
- meta-learning ;
- continual learning ;
- world models ;
- JEPA ;
- active inference ;
- predictive processing ;
- programmation logique ;
- systèmes de contraintes ;
- recherche arborescente ;
- Monte Carlo Tree Search ;
- reinforcement learning ;
- modèles probabilistes ;
- systèmes de contrôle ;
- architectures modulaires ;
- systèmes multi-agents ;
- architectures à état latent ;
- modèles de programmation / génération de programmes ;
- vérification formelle.

L'objectif est de trouver **des pièces déjà éprouvées**, puis de tester des combinaisons nouvelles.

> **v2 — Les briques disponibles aujourd'hui (bonne nouvelle : aucune n'est à inventer de zéro)**
>
> Sources vérifiées par un agent de recherche le 2026-09-25 :
>
> | Besoin du projet | Brique existante | Code | Rôle proposé |
> |---|---|---|---|
> | Vérifier la cohérence, détecter une contradiction, réviser | **clingo** (ASP) | github.com/potassco/clingo | V symbolique + révision de base |
> | Induire des règles à partir de peu d'exemples | **Popper** (ILP) | github.com/logic-and-learning-lab/Popper | générateur d'hypothèses de règles |
> | Compresser les solutions en nouvelles primitives | **Stitch** (Rust) | github.com/mlb2251/stitch | apprentissage d'opérateurs (§14) |
> | Choisir la question la plus informative | **pymdp** (inférence active) | github.com/infer-actively/pymdp | auto-curriculum (§34, §44) |
> | Maintenir les justifications des croyances | **ATMS** (de Kleer, 1986) | petites implémentations Python | traçabilité et révision |
> | État latent raffiné de façon récursive, très petit | **TRM** (7M de paramètres) | github.com/samsungsailmontreal/tinyrecursivemodels | candidat « réflexe compilé » (§25 v2) |
> | Benchmark d'efficacité d'acquisition interactive | **ARC-AGI-3** | arcprize.org/arc-agi/3 | phase 2 |
>
> **Ce qui a déjà été tenté et doit être étudié, pas ignoré :** Soar, ACT-R, NARS/ONA et OpenCog Hyperon. Ce sont des architectures cognitives intégrées qui visent une grande partie de ce document. Selon l'agent, leurs évaluations publiées restent des micro-tâches sans comparaison avec les approches dominantes.
>
> **Leçon constructive :** leur point faible commun semble être l'**absence de mesure d'efficacité d'acquisition** et de vérification par le monde. C'est précisément ce que la v2 met au centre (§11 v2, §28 v2). Ce qui a cédé chez eux sert de spécification pour ce projet.
>
> **Ce qui semble réellement ouvert** [HYPOTHÈSE de l'agent, recherche non exhaustive] :
> - des opérateurs appris dont la vérité est **vérifiée par le monde** ;
> - la **révision appliquée aux opérateurs** eux-mêmes ;
> - la **courbe longitudinale de R** avec des connaissances certifiées ;
> - la **boucle complète savoir ↔ acquis** du §1 bis.

---

# 39. Relation avec l'approche de Yann LeCun

Le point de départ de la réflexion est une interrogation sur les limites d'une intelligence reposant principalement sur la prédiction de séquences.

L'approche JEPA / world model de LeCun cherche précisément à dépasser certaines limites des modèles génératifs de type LLM en apprenant des représentations permettant notamment prédiction, planification et raisonnement dans un espace latent.

La présente hypothèse ne cherche pas nécessairement à contredire cette approche.

Elle déplace la question :

> **Même avec un modèle du monde, comment le système apprend-il progressivement à déduire, choisir ses expériences et construire ses propres mécanismes de raisonnement ?**

Le « world model » pourrait donc devenir :

- une brique ;
- une représentation ;
- une source d'hypothèses ;
- un simulateur ;

mais pas nécessairement l'architecture cognitive complète.

---

# 40. L'idée de « système qui apprend à apprendre »

Il faut distinguer trois niveaux :

### Niveau 1 — apprendre des faits

```text
A → B
```

### Niveau 2 — apprendre une règle

```text
A → B
B → C
donc A → C
```

### Niveau 3 — apprendre comment trouver des règles

```text
Quand plusieurs relations se combinent,
tester systématiquement leur composition.
```

L'objectif profond est le niveau 3.

Le système apprendrait non seulement :

> **ce qui est vrai**

mais :

> **comment découvrir ce qui peut être vrai.**

---

# 41. La question de la « compréhension »

Il faut éviter de partir d'une définition philosophique de la compréhension.

On peut proposer une définition opérationnelle :

Un système démontre une forme de compréhension croissante s'il peut :

1. résoudre des problèmes nouveaux ;
2. généraliser des règles ;
3. produire des hypothèses ;
4. identifier les informations manquantes ;
5. choisir des expériences pertinentes ;
6. réviser ses croyances ;
7. conserver les acquis ;
8. créer de nouvelles stratégies ;
9. utiliser ces stratégies dans un autre domaine.

Cette définition est testable.

---

# 42. Architecture possible à long terme

Une architecture hypothétique pourrait ressembler à :

```text
                       ┌─────────────────────┐
                       │   ORCHESTRATEUR     │
                       │                     │
                       │ état / objectifs    │
                       │ incertitudes        │
                       │ besoins             │
                       └──────────┬──────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    ↓             ↓             ↓
               mémoire         recherche     hypothèses
                    │             │             │
                    └─────────────┼─────────────┘
                                  ↓
                       ┌──────────────────┐
                       │ ESPACE DE TRAVAIL│
                       │ / ÉTAT COGNITIF  │
                       └────────┬─────────┘
                                │
                ┌───────────────┼────────────────┐
                ↓               ↓                ↓
           déduction         simulation       modules
                │               │                │
                │               │          ┌─────┴─────┐
                │               │          │ Transformer│
                │               │          │ logique    │
                │               │          │ perception │
                │               │          └───────────┘
                └───────────────┼────────────────┘
                                ↓
                         VÉRIFICATION
                                ↓
                           NOUVEL ÉTAT
                                ↓
                       APPRENTISSAGE
                                ↓
                         NOUVEAU BESOIN
```

Cette architecture est une **carte d'exploration**, pas une proposition finale.

---

# 43. Le système pourrait posséder plusieurs « cerveaux »

Le terme cerveau est volontairement métaphorique.

L'idée est de permettre :

- plusieurs moteurs ;
- plusieurs représentations ;
- plusieurs méthodes ;
- plusieurs hypothèses concurrentes.

Le système ne devrait pas forcément chercher immédiatement une seule réponse.

Il pourrait maintenir :

```text
H1 : 55 %
H2 : 30 %
H3 : 15 %
```

Puis choisir une expérience capable de différencier H1 et H2.

Cela introduit naturellement la notion de **valeur de l'information**.

---

# 44. L'information comme action

Une étape importante de la recherche est de ne plus considérer l'information uniquement comme une entrée.

Une information peut être une **action choisie**.

Le système peut demander :

> « Quelle observation me permettra de réduire le plus efficacement mon incertitude ? »

Cela ouvre vers :

- active learning ;
- active inference ;
- expérimentation scientifique ;
- théorie de la décision ;
- information gain ;
- contrôle.

Ce sont des pistes à explorer, pas des solutions déjà établies pour l'architecture proposée.

---

# 45. Le problème de la vérification

Une architecture de déduction ne peut pas reposer uniquement sur :

> « le réseau pense que sa réponse est correcte ».

Il faut chercher plusieurs formes de vérification :

### Vérification formelle

Preuve calculable.

### Vérification mécanique

Simulation ou exécution.

### Vérification externe

Observation du monde.

### Vérification croisée

Un autre module teste la proposition.

### Vérification empirique

Une expérience réelle.

L'architecture pourrait donc avoir un **système immunitaire cognitif** contre ses propres erreurs.

---

# 46. La mémoire doit probablement être hiérarchique

Une piste :

```text
mémoire immédiate
     ↓
expériences récentes
     ↓
règles temporaires
     ↓
règles validées
     ↓
abstractions
     ↓
opérateurs
```

Une information peut changer de statut.

Par exemple :

```text
hypothèse
   ↓
testée
   ↓
validée
   ↓
généralisée
   ↓
abstraction
```

Cela donne un mécanisme naturel pour distinguer :

- ce que le système suppose ;
- ce qu'il sait ;
- ce qu'il a démontré ;
- ce qu'il a généralisé.

---

# 47. La naissance et le développement

Une architecture de recherche pourrait définir des stades.

### Stade 0 — primitives

Quelques opérations.

### Stade 1 — déductions simples

Chaînes courtes.

### Stade 2 — composition

Plusieurs opérations successives.

### Stade 3 — hypothèses

Plusieurs chemins possibles.

### Stade 4 — contradiction

Révision.

### Stade 5 — abstraction

Création de nouvelles règles.

### Stade 6 — auto-curriculum

Choix des prochaines expériences.

### Stade 7 — création de modules

Développement de nouvelles capacités.

### Stade 8 — orchestration

Combinaison dynamique de plusieurs modules.

### Stade 9 — apprentissage ouvert

Le système continue son développement sans point final.

---

# 48. Ce que signifie « modèle final »

Dans ce paradigme, la notion de modèle final devient problématique.

Il pourrait exister :

```text
Système à t0
Système à t1
Système à t2
...
Système à t10000
```

mais pas nécessairement :

> « voici la version finale ».

L'objectif n'est plus de fabriquer le meilleur modèle possible avant son utilisation.

L'objectif est de fabriquer **un système capable de continuer à devenir meilleur**.

---

# 49. Conséquence : les benchmarks classiques deviennent insuffisants

Un benchmark classique demande :

> « Quel score obtient le modèle aujourd'hui ? »

Le nouveau système nécessite également :

> « De combien progresse-t-il après 100 expériences ? »

et :

> « Combien d'informations nouvelles lui faut-il pour progresser ? »

et :

> « Est-il capable de découvrir une méthode qu'on ne lui a jamais enseignée ? »

et :

> « Que conserve-t-il après plusieurs années d'apprentissage simulé ? »

Le benchmark devient donc longitudinal.

---

# 50. Programme de recherche recommandé

## Axe A — théorie de l'état

Définir précisément :

- état ;
- observation ;
- hypothèse ;
- contrainte ;
- connaissance ;
- opérateur ;
- déduction ;
- preuve ;
- validation.

## Axe B — primitives

Explorer plusieurs ensembles d'opérations primitives.

## Axe C — graphes

Tester les graphes comme représentation dynamique.

## Axe D — mémoire

Comparer plusieurs architectures de mémoire plastique.

## Axe E — vérification

Tester plusieurs mécanismes indépendants de validation.

## Axe F — apprentissage continu

Mesurer progression et oubli.

## Axe G — curriculum

Faire choisir au système ses expériences.

## Axe H — modularité

Tester l'ajout et la suppression dynamique de modules.

## Axe I — Transformer

Le considérer comme outil spécialisé et mesurer sa valeur dans l'orchestration.

## Axe J — architecture émergente

Laisser les résultats des axes précédents déterminer la structure globale.

---

# 51. Pourquoi le parallélisme est obligatoire à ce stade

Aucune hypothèse ne doit être considérée comme « la bonne ».

Il faut plusieurs agents et plusieurs approches :

```text
Agent 1 → théorie des systèmes
Agent 2 → neurosciences computationnelles
Agent 3 → architectures neuronales
Agent 4 → logique / symbolique
Agent 5 → graphes
Agent 6 → apprentissage continu
Agent 7 → active learning
Agent 8 → information theory
Agent 9 → systèmes distribués
Agent 10 → contrôle / optimisation
Agent 11 → expérimentation
Agent 12 → critique adversariale
```

Chaque agent doit pouvoir **attaquer les hypothèses des autres**.

Le but n'est pas de produire douze architectures.

Le but est de faire émerger les contraintes communes.

---

# 52. Règle de recherche : ne pas choisir trop tôt

Il faut conserver explicitement plusieurs branches :

```text
A — machine à états
B — graphe vivant
C — générateur d'opérateurs
D — hybride neuro-symbolique
E — architecture auto-composable
F — autre piste découverte par les agents
```

Une branche ne doit être abandonnée que sur la base d'un résultat ou d'une impossibilité clairement documentée.

---

# 53. Le rôle du langage de programmation

Il ne faut pas créer un nouveau langage au début.

Le problème actuel est architectural, pas syntaxique.

### Rust

**Candidat privilégié pour le noyau expérimental.**

Raisons :

- contrôle mémoire ;
- structures de données complexes ;
- graphes ;
- parallélisme ;
- concurrence ;
- performance ;
- déterminisme possible ;
- systèmes persistants ;
- exécution native.

### Python

**Laboratoire expérimental.**

À utiliser pour :

- mathématiques ;
- prototypes rapides ;
- visualisation ;
- expérimentation ML ;
- notebooks ;
- analyse des résultats.

### Go

**Infrastructure / orchestration.**

Intéressant pour :

- services ;
- agents ;
- coordination ;
- systèmes distribués.

Mais moins évident comme cœur de recherche pour cette architecture.

### Nouveau langage

À envisager uniquement si une nouvelle abstraction fondamentale apparaît et qu'aucun langage existant ne la représente correctement.

**Pas maintenant.**

---

# 54. Proposition d'organisation technique

```text
research/
├── theory/
├── hypotheses/
├── experiments/
├── environments/
├── verifier/
├── state-engine/
├── memory/
├── operators/
├── modules/
├── orchestrator/
├── transformer-adapters/
├── evaluation/
└── reports/
```

Chaque expérience doit être reproductible.

Chaque résultat doit préciser :

- hypothèse ;
- architecture ;
- données ;
- protocole ;
- résultat ;
- limite ;
- conclusion ;
- prochaine expérience.

---

# 55. Principe fondamental pour les agents

Ne jamais leur demander :

> « Trouve une architecture qui remplace les LLM. »

Cette formulation les poussera à recycler les architectures connues.

Préférer :

> **Trouve une architecture dans laquelle le token n'est pas l'unité fondamentale, l'entrée est un état, la sortie est un nouvel état, la transformation peut être vérifiée et le système peut apprendre progressivement de nouvelles transformations au cours de son existence.**

Puis demander à chaque agent :

1. Quelles architectures existantes contiennent déjà une partie de cette propriété ?
2. Quelles briques peuvent être combinées ?
3. Quelles hypothèses sont nécessaires ?
4. Quelles hypothèses sont falsifiables ?
5. Quelle expérience minimale permet de les départager ?
6. Quel est le risque d'être simplement en train de reconstruire un LLM sous un autre nom ?

---

# 56. Critère de réussite le plus important

Ne pas chercher immédiatement :

> « Est-il meilleur que GPT / Claude / Gemini ? »

Le premier critère est beaucoup plus fondamental :

> **Un système peu informé peut-il apprendre progressivement une capacité de déduction et utiliser cette capacité pour apprendre plus efficacement lors de l'expérience suivante ?**

Puis :

> **La progression continue-t-elle lorsque le système reçoit de nouvelles expériences ?**

Puis :

> **Le système découvre-t-il des mécanismes qu'on ne lui a pas explicitement fournis ?**

Puis :

> **Peut-il transférer ces mécanismes à un problème nouveau ?**

Si la réponse devient oui, le projet commence à démontrer quelque chose de réellement différent.

> **v2 — Défi → Piste : un critère avec un étalon et un seuil**
>
> **Défi.** Sans référence de comparaison ni seuil, « le système progresse » ne peut pas être réfuté. Or les LLM avancent sur le même terrain : l'autovérification émerge avec le RL (DeepSeek-R1), et les « boucles de raffinement » dominent ARC 2025 [VÉRIFIÉ par agent : arXiv 2501.12948, 2601.10904]. « Itérer » ne suffit donc pas à se distinguer.
>
> **Piste.** Le LLM n'est pas l'ennemi, c'est **l'étalon**. Ses faiblesses documentées montrent exactement où viser :
> - la *reversal curse* : un modèle entraîné sur « A est B » n'apprend pas « B est A » [VÉRIFIÉ par agent : arXiv 2309.12288] ;
> - la révision de croyances : environ 30 LM échouent sur Belief-R, et ceux qui révisent bien sur-révisent [VÉRIFIÉ par agent : arXiv 2406.19764] ;
> - ARC-AGI-3 : 0,51 % pour l'IA contre 100 % pour les humains.
>
> **Gabarit de l'affirmation à défendre** (à compléter avant la première expérience) :
>
> > *Sur la chambre aux relations opaques (§29 v2), notre système atteint le niveau N avec au moins X fois moins de bits d'expérience qu'un LLM de raisonnement actuel qui reçoit les mêmes observations. Il atteint le monde n+1 au moins Y % plus vite que le monde n. Et il ne perd pas plus de Z % de ses acquis après 1 000 mondes.*
>
> **Étalons obligatoires, à budget égal :**
> 1. un solveur écrit à la main, qui sert de plafond ;
> 2. un LLM de raisonnement avec les faits en contexte ;
> 3. un petit réseau (TRM ou GNN) entraîné sur les mêmes exemples.
>
> **Les valeurs de N, X, Y et Z sont à fixer ensemble avant de lancer quoi que ce soit.** C'est la première décision du projet.

---

# 57. Hypothèse centrale à tester

Formulation de travail :

> **Une intelligence artificielle générale pourrait être mieux obtenue en construisant un système de déduction et d'apprentissage continu qui reçoit progressivement des expériences, plutôt qu'en entraînant une fois pour toutes un modèle massif sur une quantité maximale de données.**

Sous-hypothèses :

1. La déduction peut être séparée de la génération de tokens.
2. Un état peut remplacer le contexte tokenisé comme unité fondamentale.
3. Une transformation d'état peut être vérifiée.
4. Un système peut apprendre progressivement ses propres opérateurs.
5. Le curriculum peut être partiellement choisi par le système.
6. La mémoire peut être plastique et hiérarchique.
7. Des modules spécialisés peuvent être créés, adaptés ou mobilisés dynamiquement.
8. Un Transformer peut être un module plutôt que le cerveau central.
9. Un orchestrateur peut déterminer quand un module doit être sollicité.
10. L'apprentissage peut être continu plutôt qu'une phase terminée.
11. La quantité d'information nécessaire à une nouvelle compétence peut diminuer à mesure que le système développe ses mécanismes de déduction.
12. Une architecture distribuée peut être plus adaptée à cette fonction qu'un modèle monolithique.

---

# 58. Ce qui reste complètement ouvert

Il ne faut pas prétendre savoir aujourd'hui :

- si le graphe est la bonne représentation ;
- si les opérateurs doivent être symboliques ;
- si une partie neuronale doit apprendre les opérateurs ;
- si l'état doit être discret ou continu ;
- si la mémoire doit être externe ou interne ;
- si le système doit posséder des poids ;
- si ces poids doivent évoluer continuellement ;
- si un Transformer sera finalement central, périphérique ou inutile ;
- si l'apprentissage doit être supervisé, auto-supervisé, renforcé ou hybride ;
- si l'architecture doit être centralisée ou distribuée ;
- si l'auto-curriculum peut fonctionner sans boucle de confirmation ;
- quelle quantité minimale de données est nécessaire ;
- si une telle architecture peut atteindre une généralité comparable à celle d'un LLM.

**Ces questions constituent précisément le programme de recherche.**

---

# 59. Conclusion de travail

La question initiale était :

> **« Comment faire autre chose qu'un Transformer ? »**

Elle s'est progressivement transformée en :

> **« Pourquoi demander à une architecture conçue pour une fonction particulière de jouer le rôle de cerveau général ? »**

Puis en :

> **« Et si le cerveau artificiel était un système capable de décider lui-même quelles briques utiliser, quelles informations obtenir, quelles hypothèses tester et quelles nouvelles capacités construire ? »**

Le Transformer pourrait alors rester.

Mais à sa place correcte :

> **une brique spécialisée dans un système cognitif plus large.**

La rupture recherchée n'est donc pas nécessairement :

**Transformer → autre réseau**

mais potentiellement :

**modèle → système**

**entraînement → développement**

**dataset → expérience**

**token → état**

**prédiction → transformation**

**réponse → nouvel état**

**mémoire massive → apprentissage progressif**

**modèle final → organisme computationnel en évolution**

Et la question centrale devient :

> **Peut-on construire une machine qui ne soit pas entraînée une fois pour toutes, mais qui naisse avec quelques capacités primitives, apprenne à déduire, choisisse progressivement ce dont elle a besoin pour apprendre, construise ses propres représentations et ses propres opérateurs, mobilise des modules spécialisés — dont éventuellement des Transformers — et continue à modifier son architecture au fil de son expérience ?**

C'est cette question qui doit guider les expérimentations.

---

# 60. Sources et points de vérification

### [1] Transformer

Vaswani et al., *Attention Is All You Need*, 2017.

L'article introduit le Transformer comme architecture fondée uniquement sur l'attention, sans récurrence ni convolution, et rapporte des avantages de qualité et de parallélisation sur les tâches de traduction étudiées.

Source : https://arxiv.org/abs/1706.03762

### [2] Apple Foundation Models

Documentation officielle Apple Developer — Foundation Models.

Elle décrit l'accès aux modèles on-device et Private Cloud Compute, le tool calling, les profils dynamiques et la possibilité de construire des abstractions telles que des agents ou des skills.

Source : https://developer.apple.com/documentation/FoundationModels/

### [3] Apple — WWDC26 Machine Learning

Documentation officielle Apple sur Foundation Models et Core AI, notamment l'exécution et la spécialisation de modèles sur Apple Silicon.

Source : https://developer.apple.com/wwdc26/guides/machine-learning/

### [4] Apple — Core AI dans Foundation Models

Documentation officielle montrant qu'un modèle Core AI peut être intégré dans une session Foundation Models, permettant notamment d'utiliser des modèles spécialisés.

Source : https://developer.apple.com/documentation/foundationmodels/running-a-core-ai-model-in-a-foundation-models-session

### [5] Continual Learning

La problématique de l'apprentissage continu et de l'oubli catastrophique constitue un domaine de recherche établi. Elle doit être étudiée comme contrainte architecturale, pas considérée comme résolue.

---

# 61. Référence non confirmée à retrouver

Au cours de la réflexion, une étude chinoise a été évoquée à propos d'un système où la réduction ou modification de la mémoire disponible aurait amélioré certaines capacités de raisonnement d'un LLM.

**Cette référence exacte n'a pas été identifiée de manière suffisamment fiable dans le cadre de ce document.**

Elle doit donc être traitée comme :

> `[À VÉRIFIER]`

et non comme un fait établi.

Les agents devront retrouver :

- le papier exact ;
- les auteurs ;
- la date ;
- l'architecture concernée ;
- la définition précise de « mémoire » ;
- le protocole expérimental ;
- les benchmarks ;
- les conditions dans lesquelles le résultat est observé ;
- les limites ;
- les résultats contradictoires éventuels.

> **v2 — Résultat de la recherche (2026-09-25) : référence non identifiée avec certitude.** Les candidats, vérifiés par un agent :
>
> | Candidat | Origine | Ce qu'il montre | Correspondance |
> |---|---|---|---|
> | **Engram** — *Conditional Memory via Scalable Lookup* (arXiv 2601.07372, janvier 2026) | DeepSeek-AI + Université de Pékin | Séparer une mémoire statique consultée en O(1) libère le réseau pour raisonner. À paramètres et FLOPs égaux : BBH +5,0, ARC-Challenge +3,7, MATH +2,4 | **Forte** si le souvenir est « modifier la mémoire ». La mémoire est **ajoutée ou réallouée**, pas réduite |
> | **InftyThink** (arXiv 2503.06692, ICLR 2026) | Université du Zhejiang | Borner le contexte de raisonnement en segments avec résumés améliore les scores. Qwen2.5-Math-7B : AIME24 de 32,9 à 44,0 | **Forte à moyenne** si le souvenir est « réduire la mémoire » |
> | **DMS** — *Inference-Time Hyper-Scaling with KV Cache Compression* | Edinburgh + NVIDIA (**pas chinois**) | Une mémoire 8× plus petite fait +12 points sur AIME24 à budget égal. Relayé dans la presse sous le titre « Shrinking AI memory improves LLM accuracy » | Mot pour mot, mais l'origine ne colle pas. Confusion possible |
>
> **Lien avec ce projet :** Engram va dans le sens du §25 v2. **Séparer ce qui est su (la mémoire) de ce qui raisonne (le calcul) améliore le raisonnement**, même à l'intérieur d'un Transformer. C'est un indice empirique en faveur de l'architecture à deux étages.

---

# 62. Consigne finale pour le chantier

**Ne pas chercher à avoir raison.**

Chercher à faire émerger une architecture qui survive aux expériences.

Chaque agent doit pouvoir dire :

> « Cette hypothèse ne fonctionne pas. »

et expliquer pourquoi.

Le projet ne doit donc pas être construit autour d'une architecture favorite.

Il doit être construit autour d'un **processus de découverte parallèle, falsifiable et cumulatif**.

Le premier objectif n'est pas une IA générale.

Le premier objectif est de trouver une primitive computationnelle suffisamment robuste pour permettre :

```text
ÉTAT
  ↓
DÉDUCTION
  ↓
VALIDATION
  ↓
NOUVEL ÉTAT
  ↓
APPRENTISSAGE
  ↓
NOUVELLE EXPÉRIENCE
  ↓
NOUVELLE DÉDUCTION
```

**Si cette boucle fonctionne réellement, l'architecture globale pourra émerger autour d'elle.**


---

# 63. Registre des défis (v2)

> Un défi n'est pas une objection, c'est une pièce manquante. Chaque ligne se ferme par une **expérience qui tranche**, pas par un argument.

| # | Défi | Piste v2 | Section | Expérience qui tranche |
|---|---|---|---|---|
| D1 | L'orchestrateur est un homoncule | La régression s'arrête sur une règle de sélection bête et figée ; l'orchestrateur est le même moteur appliqué au méta-état | §24 v2 | Un orchestrateur appris bat-il un orchestrateur aléatoire sur R, à budget égal ? |
| D2 | Qui écrit le vérificateur ? | Le monde vérifie : écart prédiction/observation + hiérarchie de confiance | §11 v2 | Le système promeut-il moins de fausses règles avec la vérification par le monde qu'avec l'autovalidation ? |
| D3 | « Sortir du token » est flou | On rejette l'objectif de prédire le mot suivant, pas le format token ; le moteur devient la prédiction d'état | §9 v2 | — (clarification, pas d'expérience) |
| D4 | Ancrage : d'où viennent les faits ? | Symboles = compressions qui améliorent la prédiction ; relations opaques puis grilles brutes | §11 v2 | Le système découvre-t-il les propriétés de relations opaques ? |
| D5 | Circularité des primitives | Primitives génériques publiées avant les tests ; distance MDL ; promotion seulement après vérification par le monde | §14 v2 | L'opérateur découvert est-il à plus d'une étape des primitives ? Se transfère-t-il ? |
| D6 | Expérience §29 triviale et mal définie | Chambre aux relations opaques : pièges, bruit, sémantique écrite, révisions dans les deux sens, transfert | §29 v2 | Le monde n+1 est-il résolu plus vite que le monde n ? |
| D7 | R est manipulable | R mesuré en bits économisés sur des données futures tenues à l'écart | §28 v2 | La courbe R(expérience) s'accélère-t-elle ? |
| D8 | « Peu de données » : l'enfant a des a priori | Deux budgets publiés : génome (a priori) et expérience (bits) | §5 v2 | Compétence obtenue / (génome + expérience) comparée à l'étalon |
| D9 | La mémoire dédiée ne gagne pas automatiquement (CL-Bench) | Deux étages règles ↔ réflexes, avec compilation, surveillance et recompilation | §25 v2 | Taux de fautes du réflexe dans le temps, sous charge, en contexte nouveau |
| D10 | Tout existe déjà par morceaux | Réutiliser les briques (clingo, Popper, Stitch, pymdp, TRM) ; la nouveauté est dans la vérification par le monde, la révision des opérateurs et la courbe longitudinale | §38 v2 | — (état de l'art, à approfondir) |
| D11 | Les LLM avancent aussi | Le LLM est l'étalon ; viser ses faiblesses documentées (révision, reversal curse, ARC-AGI-3) | §56 v2 | L'affirmation gabarit avec N, X, Y, Z |
| D12 | Créer des modules coûte cher (NAS) | Catalogue fini de gabarits d'abord ; création libre plus tard | §24 v2 | Un module créé fait-il baisser l'erreur sur la classe d'observations visée ? |
| D13 | Le cas « il connaît la règle mais refait la faute » | **Hypothèse centrale v2** : l'intelligence est la boucle savoir ↔ acquis | §1 bis | Écart entre réciter la règle et l'appliquer sans faute dans un contexte jamais vu |
| D14 | Les erreurs invisibles (fluides, qui sonnent juste) | Déclencheur appris sur indices de contexte, à partir de corrections externes | §1 bis v2.1 | Test 1 variantes A/B : même réponse aux deux = génération |
| D15 | Équilibre vérifier trop / trop peu | Déclencheur = décision typée avec confiance calibrée (piste Jev) + seuil coût/risque | §1 bis v2.1 | La calibration tient-elle sur des cas piégés hors distribution ? |
| D16 | Apprendre de sa propre correction, sans attendre d'avoir appris | Autodiagnostic : trace → étape fautive → hypothèse sur sa mécanique → épreuve sur d'autres cas → modification | §1 bis v2.1 | Après UNE correction, le système réussit-il des cas nouveaux de la même famille ? |

## Décisions à prendre (par Malik) avant toute construction

1. **Valeurs de N, X, Y, Z** dans l'affirmation gabarit du §56 v2.
2. **Hypothèse centrale** : adopter le §1 bis (boucle savoir ↔ acquis) comme fil directeur de la phase 1, ou le garder comme une branche parmi A–F (§52).
3. **Périmètre de la phase 1** : se limiter à la chambre aux relations opaques, ou viser directement un micro-monde perceptif (grilles).

---

*Fin de la v2. La v1 reste la source de l'intuition ; la v2 en fait un cahier des charges.*
