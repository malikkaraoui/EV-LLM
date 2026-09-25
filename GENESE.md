---
titre: EV-LLM — Genèse et cheminement
description: Journal chronologique de la naissance du projet. On y note les idées, les bascules, les erreurs et les décisions, dans l'ordre où elles sont arrivées. On complète, on ne réécrit jamais.
cree: 2026-09-25
convention: une entrée par moment clé, horodatée (heure de Paris). Qui a dit quoi. Ce qui a changé dans la pensée. Ce qui reste ouvert.
---

# EV-LLM — Genèse du projet

> Règle de ce journal : **on ajoute, on ne corrige pas le passé.** Une idée abandonnée reste écrite, avec la raison de son abandon. Le cheminement compte autant que le résultat.

---

## 2026-09-24 (soir) — Naissance de l'intuition (Malik × GPT, version gratuite)

- Point de départ : une interrogation sur l'approche de Yann LeCun et sur les limites du paradigme LLM.
- Intuition de Malik : **ingérer toujours plus de données et de tokens ne donne pas, à soi seul, la capacité de déduire.**
- Formules nées ce soir-là :
  - « On ne l'entraîne pas. On lui donne naissance. »
  - Le Transformer est un organe, pas le cerveau.
  - Token → état ; prédiction → transformation ; modèle final → organisme en évolution.
- Produit : `architecture_cognitive_post_transformer.md` (v1, 62 sections), conservé intact sous le nom `architecture_cognitive_post_transformer.v1-gpt.md`.

## 2026-09-25 10:40 — Lancement avec Claude

- Malik ouvre le projet avec Claude : « si on arrive à quelque chose… on lancera une révolution ».
- Tentative de poser le harnais d'orchestration : **reportée**. Malik le peaufine et fera signe quand il sera prêt.
- Consigne de Malik : se concentrer sur le but du projet.

## 2026-09-25 ~11:00 — Faux départ : Claude commence à construire

- Claude lance trois recherches en parallèle (état de l'art, référence §61, critique adversariale) et commence à préparer un banc d'expérience en Python.
- **12:13 — Malik stoppe :** « tu construis rien. Challenge le document. Pour l'instant, nous discutons. »
- Leçon : **phase de discussion ≠ phase de construction.** Ne rien construire tant que Malik n'a pas ouvert cette phase.

## 2026-09-25 12:13 — Première critique (angle « ça ne marchera pas »)

Claude pointe 12 faiblesses :
- l'orchestrateur est un homoncule ;
- personne ne dit qui écrit le vérificateur ;
- « sortir du token » est flou ;
- l'ancrage des symboles n'est pas traité ;
- l'expérience du §29 est triviale et mal définie ;
- la métrique R peut être gonflée ;
- l'analogie avec l'enfant (qui a en réalité beaucoup d'a priori) ;
- la Bitter Lesson ;
- presque tout existe déjà par morceaux ;
- les LLM avancent sur le même terrain ;
- créer des modules coûte cher ;
- la référence §61 n'est pas retrouvée.

## 2026-09-25 12:38 — Bascule majeure : Malik recadre

Les mots de Malik, à garder :

> « L'intelligence d'un modèle n'est pas l'entraînement qu'il a subi. L'intelligence est cette capacité avec un rien à faire beaucoup. C'est la possibilité d'additionner, faire discuter, mettre en relation ce qu'on a vu, appris, senti, et ce qu'on pense viable. »

> « Certains mammifères sont très intelligents alors qu'ils ne parlent pas. »

> « Le token, c'est juste des prédictions du mot futur. C'est beau, c'est correct… mais c'est stupide. »

> « Je ne veux pas que tu montres du doigt, c'est facile, tu as lu le monde. Prends l'autre angle : oui, il y a une solution, on va la trouver. Ce n'est pas parce qu'un homme n'arrive pas à faire du feu que tous les hommes n'en feront jamais. »

**Le cas fondateur, apporté par Malik :** son fils de 9 ans connaît la règle é/er (« battu → é, battre → er ; avec être, on accorde »), sait la réciter… et refait la faute. **Il connaît la règle, il ne l'a pas acquise.**

Conséquence : changement de posture. **Chaque obstacle devient un problème à résoudre, jamais une raison d'abandonner.**

## 2026-09-25 ~12:45 — Document v2 : « Défi → Piste »

- Claude réécrit le document au même endroit :
  - 13 blocs « v2 — Défi → Piste » ;
  - §1 bis : définition de l'intelligence + cas de l'enfant ;
  - §63 : registre des défis.
- Pistes principales :
  - **le monde est le vérificateur** : l'écart entre la prédiction et l'observation remplace le vérificateur qu'on devrait écrire à la main ;
  - **l'orchestrateur** s'arrête sur une règle de sélection simple, comme la sélection naturelle ;
  - **la mémoire à deux étages**, règles ↔ réflexes ;
  - **R mesuré en bits économisés** sur des données futures ;
  - **la chambre aux relations opaques** ;
  - **le LLM comme étalon**, pas comme ennemi.
- Copies : Documents/EV-LLM, iCloud New projects/EV-LLM, et le doc du projet claude.ai. Incident : une copie est arrivée tronquée ; Claude l'a détecté par empreinte et corrigé.

## 2026-09-25 12:57 — Hypothèse centrale retenue pour la discussion : la boucle savoir ↔ acquis

- Constat :
  - **le LLM a le réflexe sans la règle** ;
  - **le système symbolique a la règle sans le réflexe** ;
  - **l'enfant a la règle sans le réflexe**.
  - Aucun n'a la boucle qui transforme l'un en l'autre.
- Claude affine : la règle é/er est en réalité **une procédure de vérification** (le test de substitution par « battre »). L'enfant possède le vérificateur. **Ce qui manque, c'est le déclencheur**, c'est-à-dire savoir *quand* tester.
- Trois pièces : **règle** (le test), **déclencheur** (détecter la zone piégée), **réflexe** (la réponse compilée).
- Quatre phases d'acquisition :
  1. fautes ;
  2. lent mais juste ;
  3. rapide et juste ;
  4. surveillance en sommeil.
- Deux boucles :
  - **descendante**, règle → réflexe : l'apprentissage ;
  - **montante**, réflexe → règle : la découverte.

## 2026-09-25 13:05 — Première donnée réelle

- Question de Claude : « Quand ton fils se relit à froid, repère-t-il seul sa faute é/er ? »
- **Réponse de Malik : à 70 %.**
- Lecture [HYPOTHÈSE] : au calme, la règle marche la plupart du temps, donc c'est surtout le **déclencheur** qui manque sous charge.
- Les 30 % restants s'expliqueraient ainsi : **« mangé » et « manger » se prononcent pareil**. En se relisant à l'oreille, la faute est invisible, rien ne sonne faux, donc rien ne déclenche le test.
- **Découverte : il y a deux sortes d'erreurs.**
  - **Visibles** : elles surprennent, et la surprise suffit à déclencher la vérification.
  - **Invisibles** : elles sonnent juste. Seuls des indices de contexte appris grâce à des corrections externes (« après avoir », « après pour »…) peuvent déclencher la vérification.
- **Lien fort :** l'erreur invisible é/er a la même structure qu'une **hallucination de LLM**, une sortie fausse et fluide que son producteur ne peut pas distinguer d'une sortie juste.
- Nouvelle métrique : **la calibration du déclencheur**. Il ne faut ni vérifier trop souvent (lenteur), ni trop peu (fautes invisibles).
- Micro-test proposé, optionnel : 10 phrases, d'abord « relis et corrige », puis « teste “battre” sur chaque verbe ». Si le score passe de 70 % à ~100 %, c'est le déclencheur qui manque. S'il reste à 70 %, c'est l'exécution du test. **Pas encore réalisé.**

## 2026-09-25 13:10 — GPT corrige le §29… et reproduit l'erreur

- GPT reconnaît le problème : « exclut » n'était pas défini, et E > A ne contredit rien si « > » est transitif.
- Il propose une version plus propre, avec des étiquettes DÉDUCTION / HYPOTHÈSE / CONTRADICTION, et une bonne question : *le système distingue-t-il ce qui découle de ce qu'il imagine découler ?*
- Mais :
  - **« incompatible » n'est toujours pas relié à « > »**. Le test n'a toujours pas de bonne réponse, c'est la même faute juste après l'avoir admise ;
  - il manque l'étiquette **INDÉTERMINÉ**, le « je ne sais pas » du §7 ;
  - en donnant la règle de transitivité, le test mesure la tenue de comptes, pas l'apprentissage.
- **Moment clé :** c'est une illustration vivante de l'erreur invisible. Une correction fluide qui sonne juste et répète la faute, sans qu'aucun signal interne ne s'allume chez celui qui la produit.
- Synthèse proposée par Claude : **deux tests au lieu d'un**, calqués sur l'enfant.
  - **Test 1 — Savoir** (règle donnée). L'exemple de GPT réparé en deux variantes qui doivent donner des réponses différentes :
    - A, où `incompatible ⇒ ni X>Y ni Y>X` : **CONTRADICTION**, preuve E>A>B>C>D ;
    - B, sans règle qui relie « incompatible » à « > » : **INDÉTERMINÉ**.
    - Même réponse aux deux variantes, c'est de la génération, pas de la déduction.
  - **Test 2 — Acquérir** (règle non donnée) : la chambre aux relations opaques. Il faut découvrir la propriété, puis résoudre le monde suivant plus vite.
- **Pas encore intégré au document**, en attente de la décision de Malik.

## 2026-09-25 13:12 — Décision : tenir ce journal

- Malik : « commence à prendre des notes, cela permettra d'avoir la genèse du projet… le cheminement… c'est super important. »
- Création de ce fichier.

## 2026-09-25 14:26 — « La suite logique ? »

Claude propose trois étapes, toujours sur le papier :
1. graver les acquis dans le document ;
2. concevoir le **déclencheur**, la pièce qui semble nouvelle ;
3. écrire le protocole de la première expérience **avant** de coder (préenregistrement).

## 2026-09-25 14:58 — Dépôt GitHub, et Malik approfondit le déclencheur

- **Dépôt créé :** https://github.com/malikkaraoui/EV-LLM. Le harnais d'orchestration arrive bientôt (avec un vault et des outils) ; le développement pourra alors être lancé. Claude n'a encore rien poussé : le premier commit appartient à Malik ou au harnais.
- Malik autorise Claude à noter les acquis dans un markdown.

**Sur « comment apprendre les indices d'une zone piégée », la réponse de Malik, qui va plus loin que la question :**

> « Les corrections oui, mais plus fort : quand on lui donne la correction, il doit comprendre ce qu'il lui manque, ce qui ne fonctionne pas chez lui, qu'est-ce qu'il doit ajouter à son raisonnement pour avoir un bon résultat sans devoir attendre le résultat et sans avoir appris à le faire. La correction (la sienne) est justement sa seule façon d'apprendre. C'est une grosse différence entre dire “tiens un exercice, tu peux fouiller dans ta mémoire, y'a la réponse” et être en capacité de réflexion réelle, de faire des hypothèses et de changer sa mécanique si cela lui permet d'acquérir de l'intelligence. Mon fils ne va pas faire prof de maths, pourtant on lui enseigne les maths… on lui apprend à apprendre, le questionnement, l'enquête, à tenter des parallèles qui peuvent être faits sans que ce soit écrit nulle part. »

Claude traduit ce passage en une mécanique d'**autodiagnostic** :
1. comparer la trace de son raisonnement à la correction ;
2. localiser l'étape fautive ;
3. formuler une hypothèse sur ce qui manque **dans sa propre mécanique** ;
4. éprouver cette hypothèse sur d'autres cas ;
5. ne modifier la mécanique que si l'hypothèse survit.

Conséquences :
- la trace de raisonnement devient obligatoire ;
- c'est la manière de raisonner qui se corrige, pas un fait ;
- c'est le niveau 3 du §40 rendu opératoire.

**Sur l'équilibre « vérifier trop / trop peu », Malik propose Jev** (TypeSafe AI, annoncé le 15/09/2026, « System One models ») : une décision typée avec une probabilité calibrée, en 70 à 500 ms. Claude a lu l'annonce ; les chiffres sont ceux de l'éditeur, non vérifiés de façon indépendante.

Lecture de Claude : le déclencheur est exactement une décision typée et calibrée, `{RÉPONDRE | VÉRIFIER | INDÉTERMINÉ} + P(erreur)`. On vérifie quand `P(erreur) × coût(erreur) > coût(vérification)`. Jev y joue le rôle d'un organe, le « Système 1 ». Point à éprouver : la calibration tient-elle sur les erreurs **invisibles**, hors de sa distribution d'entraînement ?

**Sur la « mise en sommeil du test »**, Malik : « je ne te comprends pas ». Claude reformule avec la conduite : le débutant vérifie chaque rétroviseur, l'expert ne pense plus, mais redevient attentif dès qu'une situation sort de l'ordinaire. Il ne s'agit pas d'une pièce en plus : **c'est le même déclencheur calibré, vu dans la durée**. Confiance haute et confirmée, pas de test ; confiance qui chute, le test revient. Le terme « sommeil » est remplacé par « vigilance ».

**Gravé dans le document (v2.1) :**
- au §1 bis, les trois pièces, le 70 %, les erreurs visibles et invisibles, l'autodiagnostic, Jev et la vigilance ;
- au §29, les deux tests (savoir A/B, acquérir) et les quatre étiquettes ;
- au §63, les défis D14 à D16.

---

## Questions ouvertes (au 2026-09-25 15:00)

1. ~~Graver dans le document les deux tests, INDÉTERMINÉ, visible/invisible~~ → **fait (v2.1)**.
2. Adopter la boucle savoir ↔ acquis (règle, déclencheur, réflexe, **autodiagnostic**) comme fil directeur de la phase 1 ?
3. Seuils N, X, Y, Z de l'affirmation à défendre (§56 v2).
4. Phase 1 : relations opaques, ou directement des grilles perceptives ?
5. Micro-test é/er avec le fils de Malik : le faire ou non.
6. Harnais d'orchestration : en cours d'arrivée, puis ouverture de la phase de développement.
7. **Nouvelle :** Jev est-il accessible (API, prix, conditions) pour un premier test de calibration sur des cas piégés ?

## Références découvertes en chemin

- Engram, DeepSeek + Université de Pékin, arXiv 2601.07372 : meilleur candidat pour la référence §61. Séparer la mémoire du raisonnement améliore le raisonnement.
- Chollet, *On the Measure of Intelligence* (2019) : l'intelligence comme efficacité d'acquisition. Proche de la définition de Malik. [MÉMOIRE]
- ARC-AGI-3 : IA 0,51 % contre humains 100 % au lancement (mars 2026).
- Belief-R, arXiv 2406.19764 : les LLM révisent mal leurs croyances.
- Briques réutilisables : clingo, Popper, Stitch, pymdp, TRM (détail au §38 v2 du document).
