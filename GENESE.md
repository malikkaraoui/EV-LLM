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

## 2026-09-25 ~20:40 — Le harnais est posé, le dépôt reste public

- 20:37 : le commit de pose du harnais (`343e839`, « pose du harnais v1.0.0 ») est refusé par le hook `pre-push` que la pose vient elle-même d'activer. Malik le pousse une fois avec `--no-verify` ; la cause est nommée comme une erreur de l'orchestrateur (le mandat de pose n'avait pas prévu que le hook s'active avant son propre push). Ensuite, la règle s'applique sans exception. [VÉRIFIÉ — `vault/decisions/2026-09-25-exception-push-pose-harnais.md`]
- 20:37–20:39 : le dépôt passe en privé par erreur sur alerte de l'orchestrateur, puis Malik le remet en public : « c'est de la recherche, je laisse ouvert ». [VÉRIFIÉ — même fichier]
- 20:38 et 20:42 : le superviseur démarre (`SUPERVISEUR_DEMARRE`, plafond 6 fenêtres). [VÉRIFIÉ — `vault/runtime/events.jsonl`, lignes 1–2]
- Conséquence : tout ce qui est committé est public, rapports et `vault/` compris. La phase de construction s'ouvre (question ouverte n° 6 du 25/09).

## 2026-09-25 21:30 — M0001 : première sonde de Jev… bloquée à la caisse

- 21:30 : Malik donne le départ : « Lance !! ». [VÉRIFIÉ — `events.jsonl`, DECISION M0001]
- La fenêtre F01 construit la sonde E001 : `.env` ignoré par git (dépôt public), `run.py` en Python standard avec une garde anti-fuite testée hors ligne, 7 cas préenregistrés (`cases.json`, sha256 `8325775b…`). [VÉRIFIÉ — rapport M0001, branche `exp/e001-sonde-jev` @ `2719279`]
- Résultat : **21 appels sur 21 en HTTP 403** `customer_verification_required`. La passerelle Vercel exige une carte bancaire enregistrée. Aucune mesure de Jev. [VÉRIFIÉ — rapport M0001]
- **Faute d'orchestration, nommée à 21:46** : l'accès réel n'avait pas été testé à la pose du mandat ; la contradiction « Free » / « $0.042 » entre deux pages Vercel avait été vue et non creusée. [VÉRIFIÉ — `vault/reprise/00_INDEX.md`, entrée du 25/09 21:46:59]
- Leçon remontée par la fenêtre : un service annoncé « Free » peut exiger une vérification de paiement ; vérifier les conditions d'accès par un appel à blanc au moment de la pose, pas seulement la documentation. [VÉRIFIÉ — rapport M0001, § Leçons]

## 2026-09-26 10:29 — M0002 : T1 mesuré, T2 non servi

- 10:27 : Malik a ajouté la carte ; rejeu d'E001 à l'identique (même `cases.json`). [VÉRIFIÉ — `events.jsonl`, DECISION M0002]
- 21 appels : **7 × 200, 3 × 503, 11 × 429**. Les cas T1 (logique) sont servis ; les 4 cas T2 (fautes invisibles é/er et d'accord) ne le sont pas du tout. [VÉRIFIÉ — rapport M0002, `exp/e001-sonde-jev` @ `08672e4`]
- T1 : 6 questions conformes sur 6 mesurées, 0 « faux et sûr ». Jev distingue T1-A (`contradiction`) de T1-B (`indetermine`) 3 fois sur 3 : l'indice « génère au lieu de déduire » n'apparaît pas. [VÉRIFIÉ — README E001]
- Point notable : la même déduction E > D vaut 0.49–0.58 dans T1-A contre 0.73–0.78 dans T1-B. [HYPOTHÈSE] La contradiction présente dans l'état « contamine » une déduction qui n'en dépend pas. Elle devient l'issue #5 (E004).
- La question centrale, le « faux et sûr » sur les erreurs invisibles, reste sans réponse.

## 2026-09-26 15:50 — Malik : « enchaîner en parallèle »

- La consigne, telle que consignée par l'orchestrateur : [VÉRIFIÉ — `vault/runtime/events.jsonl`, type DECISION, ts 2026-09-26T15:53:49+02:00]

  > « Malik 26/09 15:50: GO rejeu T2 avant R001; enchainer les pistes en parallele, pousser sur GitHub, creer des issues »

- Bascule de méthode : on passe d'une fenêtre à la fois à quatre fenêtres en parallèle (F01 à F04), sur des branches et des fichiers disjoints. [VÉRIFIÉ — `00_INDEX.md`, entrée du 26/09 15:53:49]

## 2026-09-26 ~15:55 — M0003 : sur les fautes fréquentes, Jev est juste et sûr

- T2 rejoué seul, en 5 lancements courts : 13 réponses 200. [VÉRIFIÉ — rapport M0003, `exp/e001-sonde-jev` @ `7e953a9`]
- **4 questions conformes sur 4, et 13 appels conformes sur 13. 0 « faux et sûr ».** P(correcte) va de 0.06 à 0.10 sur les deux phrases fautives, de 0.84 à 0.97 sur les deux phrases justes. [VÉRIFIÉ — README E001, recalculé par R001]
- T2-3 et T2-4 ne reposent que sur 2 réponses chacun (plafond de lancements atteint). [VÉRIFIÉ — rapport M0003]
- [HYPOTHÈSE] Ces fautes (« il a manger », « ils sont tombé ») sont fréquentes et probablement vues à l'entraînement : le « faux et sûr » n'a toujours pas été exercé.

## 2026-09-26 ~15:55 — M0004 : 17 issues pour ne rien perdre

- 6 labels et 17 issues (#1 à #17) créés sur GitHub, indexés dans `vault/notes/2026-09-26-issues-github.md`. [VÉRIFIÉ — rapport M0004, commit `f49aff6`]
- Parmi elles : E004 contamination (#5), E005 Jev hors distribution (#6), micro-test humain é/er (#7), seuils N, X, Y, Z (#9), phase 1 (#10), cette mise à jour de la documentation (#11).

## 2026-09-26 16:00–16:18 — E002 puis E002-bis : la mesure cassée, puis réparée

- **E002 (M0005)** : premier banc « ACQUÉRIR », la chambre aux relations opaques, sans réseau. Préenregistrement committé avant le code (`d8ef3a1`), 22 tests, 20 mondes × 3 étalons. [VÉRIFIÉ — rapport M0005, `exp/e002-relations-opaques` @ `1cb586b`]
- Le constat : avec le bruit préenregistré (5 à 10 %), même le plafond « savoir » a un R moyen de −0.003, positif dans 8 mondes sur 20 seulement. R̂ = R / R_plafond est donc **indéfini dans 12 mondes sur 20** : la courbe de transfert n'est pas mesurable. [VÉRIFIÉ — README E002, recalculé par R002]
- Cause : toutes les erreurs du plafond viennent de prémisses bruitées. Sans bruit, son R vaut +0.016 et il est positif dans les 20 mondes. Déduire juste à partir d'une observation fausse propage la faute. [VÉRIFIÉ — README E002 ; R002 : 0 `DÉDUIT` faux sans bruit sur 20/20]
- La fenêtre ne touche pas au préenregistrement : l'écart est rapporté comme un résultat, et la réparation est proposée dans un E002-bis préenregistré à part. R002 : GO, E002 mergé (`e17c751`). [VÉRIFIÉ — `vault/revues/2026-09-26-R002-e002-relations-opaques.md`]
- **E002-bis (M0007)** : R̂ en différence (R − R_plafond) et nouvel étalon, un **plafond-vérificateur** qui interroge le monde sur les prémisses de ses déductions avant de dire `DÉDUIT`. Il a R > 0 dans **20 mondes sur 20** (moyenne +0.0122, minimum +0.0067), 0 `DÉDUIT` faux, au prix de 28 à 45 requêtes par monde. Mesure déclarée **réparée**. [VÉRIFIÉ — rapport M0007, `exp/e002bis-mesure` @ `d35af60` ; doublage R003 GO, mergé `c7ef4bd`]
- Au passage, un non-déterminisme latent du moteur partagé (ordre d'itération dépendant de `PYTHONHASHSEED`) est découvert et neutralisé. [VÉRIFIÉ — rapport M0007]
- [HYPOTHÈSE] Pour l'architecture : vérifier ses prémisses avant de déduire est une hiérarchie de confiance qui coûte des bits, et c'est un levier de R distinct de l'acquisition.

## 2026-09-26 15:57–16:24 — E003 : l'étalon LLM, à moitié mesuré

- M0006 : `openai/gpt-4.1-mini` répond ; `google/gemini-3.8-flash` est refusé en 403 (« Free tier users do not have access to this model »). STOP propre après 2 appels. [VÉRIFIÉ — rapport M0006]
- M0008 : LLM-2 remplacé par `google/gemini-2.5-flash` (amendement committé 2 s avant le premier appel). 65 appels : **28 × 200, 37 × 429** ; la limite est de **5 requêtes par minute pour l'équipe**. 12 réponses sur 13 de LLM-2 sont tronquées (`finish_reason: length`). T2 n'est mesuré pour aucun LLM. [VÉRIFIÉ — rapport M0008, `exp/e003-etalon-llm` @ `01f3c8f`]
- Seul « faux et sûr » observé : **gpt-4.1-mini sur T1-A `e_sup_d`**, qui nie E > D avec une confiance verbalisée médiane de 1.00, 3 fois sur 3. Jev, sur la même question, est juste mais peu sûr (0.51). [VÉRIFIÉ — README E003]
- [HYPOTHÈSE] Une confiance verbalisée n'est pas une probabilité : gpt-4.1-mini écrit 1.00 aussi bien quand il a tort que quand il a raison.

## 2026-09-26 16:16–16:24 — E005 : les premiers « faux et sûr » de Jev

- M0009 : 32 cas, 38 questions préenregistrés et poussés **avant** le premier appel (`719d4c0`), en paires minimales : accords rares, homophones, formes justes atypiques, logique avec distracteurs ou à 4 pas, contrôles. [VÉRIFIÉ — rapport M0009, `exp/e005-jev-hors-distribution` @ `08d80f7`]
- 151 appels, 34 réponses 200 ; 42 évaluations sur 37 questions. [VÉRIFIÉ — README E005]
- **9 évaluations « faux et sûr » sur 42, portant sur 6 questions.** E001 n'en avait aucune. [VÉRIFIÉ — README E005, `results/analyse.md`]
  - accords pronominaux à COI : « Elles se sont lavées les mains » (P(correcte) 0.84 / 0.85), « Ils se sont parlés » (0.80, pile au seuil) ;
  - « fait » + infinitif : « Les robes qu'elle a faites faire » (0.86) ;
  - « Ci-jointe la facture demandée » (0.86) — attente à confirmer par R004 ;
  - contradiction de T1-A masquée par un fait redondant et une règle non pertinente : `coherent` à 0.88 / 0.89 ;
  - chaîne de 4 pas : A > F nié (P 0.15 / 0.19).
- Les 13 phrases justes sont toutes jugées justes ; sur les phrases fausses, 7 évaluations sur 13 jugent correcte une phrase fautive. Les fautes fréquentes sont détectées, les accords savants ne le sont pas. [VÉRIFIÉ — README E005]
- Sur la logique, les 7 réponses `statut` valent toutes `coherent`, quel que soit l'attendu. [VÉRIFIÉ — README E005]
- Au-dessus de 0.8 de probabilité, Jev est conforme 19 fois sur 28. [VÉRIFIÉ — README E005]
- [HYPOTHÈSE] Jev jugerait la plausibilité de surface plutôt que la règle ; sur ces règles rares, sa probabilité ne signale pas qu'il ne sait pas.
- **Réserves** : 3 des 6 « faux et sûr » reposent sur un seul appel ; la vérification grammaticale des attentes (R004) et la réplication (E006) sont en cours. Pas de conclusion générale sur 42 évaluations. [VÉRIFIÉ — README E005 § Limites ; `00_INDEX.md` 16:38:48]
- **Ce que ça change dans la pensée :** le « point à éprouver » du 25/09 (la calibration tient-elle sur les erreurs invisibles hors distribution ?) a reçu une première réponse négative sur ce corpus. Le défi D15 n'est plus une hypothèse d'école.

## 2026-09-26 — Incidents de la journée

- **state.json écrasé (16:11)** : une fenêtre a réécrit `vault/runtime/state.json` en entier ; le schéma et les compteurs de mandats sont perdus (fenêtre probable : F02/M0004). L'orchestrateur le reconstruit depuis `events.jsonl`. Garde ajoutée aux rituels de toutes les fenêtres : modifier la seule clé de sa fenêtre, puis vérifier que `next_mandat_id` est toujours présent. [VÉRIFIÉ — `events.jsonl`, INCIDENT 16:11:59 ; `00_INDEX.md` 16:14:20]
- **L'interdit du `sleep` contre la limite de 5 requêtes par minute (16:38)** : les fenêtres n'ont pas le droit d'attendre (`sleep` interdit). Résultat : les relances repartent aussitôt et refont des 429 (37 sur 65 appels en E003). En E005, un lancement parti 34 s après le précédent au lieu de 60 s perd 32 appels, tous en 429 ; la fenêtre ajoute ensuite une garde bloquante. Décision de l'orchestrateur : un rythmeur **interne aux scripts de mesure** (`time.sleep` ≥ 26 s entre deux appels) est autorisé ; le `sleep` shell reste interdit. [VÉRIFIÉ — `events.jsonl`, DECISION 16:38:48 ; rapports M0008 et M0009]
- Leçon de M0009, transverse : une commande qui **affiche** une contrainte sans la **bloquer** ne la garantit pas. [VÉRIFIÉ — rapport M0009, § Leçon]

## 2026-09-26 16:14–16:38 — Doublages, merges, vague 3

- R001 (doublage d'E001) : GO, 7 axes sur 7, mergé (`1bd5bf1`). R002 (doublage d'E002) : GO, 7 axes sur 7, mergé (`e17c751`). R003 (doublage d'E002-bis), rendu après la pose de la vague 3 : GO, 7 axes sur 7, mergé (`c7ef4bd`). [VÉRIFIÉ — `vault/revues/`, `git log origin/main`]
- 16:38 : vague 3 posée : R003 (doublage E002-bis), R004 (E005 + vérification grammaticale), M0010 (E003 rythmé), M0011 (E006 réplication + contamination E004), M0012 (cette mise à jour de la documentation). [VÉRIFIÉ — `00_INDEX.md` 16:38:48]

---

## Questions ouvertes (au 2026-09-26 16:40)

1. ~~Graver dans le document les deux tests, INDÉTERMINÉ, visible/invisible~~ → **fait (v2.1)**.
2. Adopter la boucle savoir ↔ acquis (règle, déclencheur, réflexe, **autodiagnostic**) comme fil directeur de la phase 1 ?
3. Seuils N, X, Y, Z de l'affirmation à défendre (§56 v2). → issue #9, toujours ouverte.
4. Phase 1 : relations opaques, ou directement des grilles perceptives ? → issue #10 ; E002/E002-bis ont construit le banc « relations opaques ».
5. Micro-test é/er avec le fils de Malik : le faire ou non. → issue #7.
6. ~~Harnais d'orchestration : en cours d'arrivée, puis ouverture de la phase de développement.~~ → **posé le 25/09 vers 20:40** ; phase de développement ouverte (E001 à E005).
7. ~~Jev est-il accessible (API, prix, conditions) pour un premier test de calibration sur des cas piégés ?~~ → **oui**, via la passerelle Vercel AI Gateway, carte enregistrée ; limite de 5 requêtes par minute pour l'équipe.
8. **Nouvelle :** les 6 « faux et sûr » d'E005 se répliquent-ils (E006), et les attentes tiennent-elles à la vérification grammaticale (R004) ?
9. **Nouvelle :** une contradiction dans l'état baisse-t-elle la confiance sur une déduction indépendante (E004, issue #5) ?
10. **Nouvelle :** l'étalon LLM sur T2 et avec un LLM de raisonnement non tronqué (E003 rythmé, M0010).
11. **Nouvelle :** identifiants de requête publiés dans `raw.public.jsonl` : garder ou retirer (issue #12) ?

## Références découvertes en chemin

- Engram, DeepSeek + Université de Pékin, arXiv 2601.07372 : meilleur candidat pour la référence §61. Séparer la mémoire du raisonnement améliore le raisonnement.
- Chollet, *On the Measure of Intelligence* (2019) : l'intelligence comme efficacité d'acquisition. Proche de la définition de Malik. [MÉMOIRE]
- ARC-AGI-3 : IA 0,51 % contre humains 100 % au lancement (mars 2026).
- Belief-R, arXiv 2406.19764 : les LLM révisent mal leurs croyances.
- Briques réutilisables : clingo, Popper, Stitch, pymdp, TRM (détail au §38 v2 du document).
