# EV-LLM — journal de recherche

**En une phrase.** EV-LLM est une exploration, conduite en public, d'une architecture cognitive « post-transformer » : un système qui **apprend une procédure** à partir de peu d'exemples, la **transfère** et l'**assemble** avec d'autres. Ce n'est ni un produit ni un modèle à télécharger. C'est un carnet d'expériences, réussites et échecs compris.

État au 28/09/2026 : 21 expériences ou amendements, menés du 25 au 27/09. Quatre sont relus et fusionnés dans `main`, les autres vivent sur leur branche (liens ci-dessous). Les échecs sont publiés au même titre que les réussites : chacun épargne à d'autres un cycle.

- L'hypothèse de départ : [`architecture_cognitive_post_transformer.md`](architecture_cognitive_post_transformer.md). En bref : l'intelligence serait moins la quantité d'entraînement subie que la capacité à faire beaucoup avec presque rien ; connaître une règle n'est pas l'avoir acquise ; il manque la boucle qui transforme une règle explicite en réflexe fiable, et un réflexe en règle. Le document est une exploration, pas une architecture retenue.
- Le cheminement, jour par jour, avec les erreurs : [`GENESE.md`](GENESE.md) (jusqu'au 26/09). La suite (26–27/09) est dans une note de l'orchestrateur, `vault/notes/2026-09-27-genese-suite.md`, pas encore versionnée.

---

## La méthode

C'est la partie qui compte le plus. Les résultats en découlent.

1. **Antériorité avant chaque expérience.** On cherche d'abord ce qui est publié : sources lues, verdict écrit dans le mandat (« fait », « partiellement fait », « non trouvé »). Au début, ce fut une veille de 10 à 20 minutes ; depuis le 27/09 au soir, c'est une recherche approfondie par des agents dédiés, avant tout lancement.
2. **Ne pas refaire le publié pour arriver au même résultat.** Si c'est déjà fait, on cherche la variante, le contre-pied. Une brique connue (MAP-Elites, MDL, REINFORCE…) n'est qu'un outil ; la question testée doit être nouvelle.
3. **Préenregistrement avant le code.** Hypothèses, prédictions chiffrées et seuils de réussite sont commités et poussés seuls, avant la première ligne de code. Un écart constaté ensuite est un résultat : il est rapporté, pas corrigé en douce. Toute modification passe par un amendement daté.
4. **Garde-fous de mesure** (durcis le 27/09 après une revue hostile) :
   - pilote sur la graine 0, exclue des résultats ;
   - au moins 5 graines (2 à 3 pour les premières expériences, dit à chaque fois) ;
   - validation hors distribution (6 à 8 chiffres) séparée du test final (10 à 1 000 chiffres), lu **une seule fois** ;
   - contrôles de validité : un oracle doit obtenir 100 %, un système « par cœur » 0 % ;
   - tests adverses (retenues en cascade, nombres pleins de zéros, longueurs asymétriques) ;
   - **budget de structure** : on écrit ce qui est donné à la main (alignement, sens de lecture, nombre de pas…) et ce qui est réellement appris.
5. **Relecture indépendante (« doublage ») avant toute fusion.** Un autre agent rejoue, recalcule et relit. Verdicts : GO, RÉSERVE ou CASSÉ. Seul GO fusionne ; « mergeable avec réserve » ne fusionne pas.
6. **Itération rapide, petit calcul.** Une machine : un Mac M1 16 Go (Python, numpy, MLX). Une expérience dure de 3 minutes à 4 heures. Les modèles vont de 22 paramètres (un réseau récurrent construit à la main) à ~3,2 millions (un petit transformer). Chaque README d'expérience donne sa durée de calcul.

Étiquettes utilisées partout : **[VÉRIFIÉ]** = relu dans une source du dépôt ; **[HYPOTHÈSE]** = interprétation non établie. Aucune conclusion générale n'est tirée : les échantillons vont de 7 cas à quelques centaines de milliers d'items, sur une seule tâche à la fois.

---

## Journal des expériences

Chaque entrée : la question, ce qui existait, ce qu'on a changé, le résultat chiffré, le verdict, ce qu'on retient, la relecture. Les chiffres sont recopiés du README de l'expérience, au tip de sa branche.

Statut de relecture : **relu GO** (fusionné dans `main`), **relu avec réserve** (non fusionné), **pas encore relu**. « Contre-vérifié par l'orchestrateur » veut dire que les chiffres ont été recalculés depuis les données par la fenêtre d'orchestration ; ce n'est pas un doublage indépendant.

### Partie 1 — Un déclencheur externe : Jev sait-il quand il se trompe ? (25–26/09)

L'idée : pour savoir *quand* vérifier, il faut une confiance honnête, surtout sur les erreurs « invisibles » (fausses mais fluides). Jev (TypeSafe AI) se présente comme un modèle qui rend des décisions typées avec une probabilité calibrée. On l'a sondé par API.

**1. Première sonde de Jev (E001)** — [dossier](research/experiments/E001-jev-sonde/) · relu GO (R001), fusionné
- Question : sur 7 cas préenregistrés (logique à règle donnée, fautes d'orthographe fluides), Jev est-il « faux et sûr » ?
- Antériorité : annonce de l'éditeur (15/09/2026) ; ses chiffres ne sont pas vérifiés de façon indépendante.
- Résultat : 1er lancement, 21 appels sur 21 refusés (HTTP 403, carte bancaire exigée). Puis logique : 6 questions conformes sur 6 ; contradiction et indétermination distinguées 3 fois sur 3. Fautes fréquentes (« il a manger », « ils sont tombé ») : 4/4 conformes, 13 appels sur 13, 0 « faux et sûr ».
- Verdict : **réussi comme sonde, mais la question n'est pas tranchée** : ces fautes fréquentes n'ont piégé personne.
- Retenu : un service annoncé « gratuit » peut exiger une carte ; tester l'accès réel par un appel à blanc avant de lancer.

**2. Étalon LLM sur les mêmes cas (E003)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e003-etalon-llm/research/experiments/E003-etalon-llm) · relu avec réserve (R005), correctifs pas encore relus
- Question : deux LLM génératifs (`gpt-4.1-mini`, `gemini-2.5-flash`) font-ils mieux ou moins bien que Jev ?
- Résultat : conformité Jev 10/10, `gpt-4.1-mini` 9/10, `gemini-2.5-flash` 10/10. Seul « faux et sûr » : `gpt-4.1-mini` nie E > D 3 fois sur 3, avec une confiance verbalisée de 0,9 à 1.
- Verdict : **mesuré, mais backend non contrôlé** : le fournisseur de la passerelle n'était ni imposé ni journalisé. Le rejeu prévu a été annulé avec l'arrêt des tests Jev.
- Retenu : une confiance verbalisée n'est pas une probabilité ([HYPOTHÈSE]) ; imposer et journaliser le fournisseur de tout modèle témoin.

**3. Jev hors distribution (E005)** — [dossier](research/experiments/E005-jev-hors-distribution/) · relu CASSÉ (R004, total HTTP faux), corrigé, puis relu GO (R007), fusionné
- Question : sur des règles rares (accords savants, homophones, logique avec distracteurs ou à 4 pas), Jev se trompe-t-il avec assurance ?
- Changé : 32 cas en paires minimales, préenregistrés et poussés avant le premier appel.
- Résultat : 151 appels, 34 réponses utiles. **9 évaluations « faux et sûr » sur 42, portant sur 6 questions.** Les 13 phrases justes sont jugées justes ; sur les phrases fausses, 7 évaluations sur 13 jugent correcte une phrase fautive. Au-dessus de 0,8 de probabilité, Jev est conforme 19 fois sur 28.
- Verdict : **négatif pour la calibration sur ce corpus.**
- Retenu : [HYPOTHÈSE] Jev jugerait la plausibilité de surface plutôt que la règle.

**4. Réplication et frontière (E006)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e006-replication-frontiere/research/experiments/E006-replication-frontiere) · relu avec réserve (R008), correctif pas encore relu
- Question : les « faux et sûr » d'E005 se reproduisent-ils ? Où est la frontière ?
- Résultat : 103 appels, tous servis. **5 « faux et sûr » non contestés, reproduits 5 fois sur 5**, plus 1 réponse reclassée « contestée » (question ambiguë, R008). Chaîne logique de 2 à 6 pas : P entre 0,85 et 0,97, pas de pente. Distracteurs : P(contradiction) 0,73 → 0,34 → 0,14 → 0,08 pour 0 à 3 distracteurs. Contamination par une contradiction sans rapport : écart moyen −0,005, non observée.
- Verdict : **réplication réussie** ; la longueur de chaîne n'est pas la frontière, un seul distracteur suffit.
- Retenu : « peut-on déduire X » est ambigu quand une règle interdit X ; préciser le sens de « déduire » dans les corpus.

**5. Jev lit-il les règles écrites ? (E007)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e007-regles/research/experiments/E007-regles) · pas encore relu
- Résultat : écrire la règle d'accord dans l'énoncé corrige les 3 paires (forme fautive de 0,84–0,86 à 0,05–0,09). Inverser une règle est suivi (0,77 → 0,34 ; 0,95 → 0,28). La retirer ne change presque rien (0,70 ; 0,90) : Jev complète avec le sens usuel des symboles.
- Verdict : **« partiellement »**, au sens du critère préenregistré.
- Retenu : [HYPOTHÈSE] Jev part d'un a priori ; une règle écrite qui le contredit le fait bouger, une règle absente ne l'arrête pas.

**Fin de cette partie (26/09, 18:17).** Décision de Malik : arrêter les tests Jev et travailler sur de petits modèles que l'on entraîne soi-même.

### Partie 2 — Acquérir des règles cachées : la chambre aux relations opaques (26/09)

**6. Le banc et trois étalons (E002)** — [dossier](research/experiments/E002-relations-opaques/) · relu GO (R002), fusionné
- Question : un banc où les propriétés des relations sont cachées, bruitées (5 à 10 %) et piégées sépare-t-il « savoir », « acquérir naïvement » et le hasard ? Gain mesuré en bits économisés (R).
- Antériorité : non documentée dans le README.
- Résultat : même l'étalon qui **connaît** les propriétés a un R moyen de −0,003, positif dans 8 mondes sur 20 seulement. Le ratio à ce plafond est donc indéfini dans 12 mondes sur 20. Sans bruit, son R vaut +0,016, positif partout.
- Verdict : **négatif sur la mesure**, écart rapporté et non corrigé.
- Retenu : déduire juste à partir d'une observation fausse propage la faute.

**7. Réparer la mesure (E002-bis)** — [dossier](research/experiments/E002bis-mesure/) · relu GO (R003), fusionné
- Changé : un plafond qui vérifie ses prémisses auprès du monde avant de conclure ; mesure en différence (R − R_plafond).
- Résultat : R > 0 dans **20 mondes sur 20** (moyenne +0,0122, minimum +0,0067), au prix de 28 à 45 requêtes par monde.
- Verdict : **réussi** (mesure réparée, pour ce banc et ces paramètres).

**8. Premier candidat « acquérir » (A0)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0-candidat/research/candidats/A0) · relu avec réserve (R009)
- Question : une mémoire entre mondes, un déclencheur calibré et un autodiagnostic font-ils résoudre le monde n+1 plus vite que le monde n ?
- Résultat : accélération dans 1 famille sur 4 (il en fallait 3). Meilleur système sans propriétés données (écart au plafond −0,0110), mais son déclencheur n'a **jamais** vérifié : 0 requête sur 20 mondes, coût de vérification mal posé.
- Verdict : **négatif**, cause identifiée.

**9. Candidat corrigé (A0-bis)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0bis-candidat/research/candidats/A0bis) · relu avec réserve (R009 : lecture dépendante d'une seule graine)
- Résultat : coût marginal, les vérifications deviennent actives (22,6 requêtes par monde), mais 0 famille sur 4. L'ablation « sans bruit estimé » fait mieux que le système complet (−0,0076 contre −0,0105).
- Verdict : **négatif**.

**10. Le critère était-il atteignable ? (A0-ter, oracle)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/a0ter-candidat/research/candidats/A0ter) · pas encore relu
- Changé : un « acquéreur parfait », qui reçoit la connaissance exacte de chaque famille après son premier monde.
- Résultat : **2 familles sur 4**. Même l'acquisition parfaite échoue au critère. Le seuil mesurait surtout à quel point le premier monde était raté.
- Verdict : **le critère ne mesurait pas l'apprentissage.** Les échecs d'A0 et A0-bis ne disent donc rien sur ces candidats.
- Retenu, et appliqué depuis à toutes les expériences : **prouver qu'un test est réussissable par un oracle avant d'y juger un candidat.**

### Partie 3 — Apprendre une procédure : l'addition (26–27/09)

La cible est redéfinie : apprendre l'addition sur des nombres de 1 à 5 chiffres, puis réussir sur des nombres bien plus longs. Toutes les expériences de cette partie partent d'E008 et réutilisent son évaluateur.

**11. Le test est-il juste, et où casse un transformer ? (E008)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e008-addition/research/experiments/E008-addition) · relu avec réserve (R010–R012, réserve portant sur E013, doublé avec), non fusionné
- Antériorité : la littérature prédit l'effondrement au-delà des longueurs vues ; « NoPE + sortie inversée » est un correctif connu.
- Résultat : test valide (oracle 100 %, par cœur 0 %). Transformer de ~3,2 M paramètres, 3 M exemples : 98–100 % dans la distribution, **0,0 % dès 6 chiffres** (3 graines). Avec le correctif : 91,2 % à 6 chiffres, 7,9 % à 7, 0,1 % à 8. 65 à 68 % de ses erreurs à 6–7 chiffres ont une confiance ≥ 0,8. Calcul : 2 h 11.
- Verdict : **référence posée.** Le correctif connu repousse la frontière d'un chiffre.

**12. L'architecture seule (E009)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e009-procedure-apprise/research/experiments/E009-procedure-apprise) · pas encore relu
- Antériorité : Neural GPU, Deep Thinking, Looped Transformer (veille du 27/09, note `vault/notes/2026-09-27-veille-procedure.md`, pas encore versionnée).
- Résultat : 5 architectures de 50 à 110 k paramètres, 512 000 exemples : ≤ 3 % même dans la distribution.
- Verdict : **non mesuré.** Budget trop court, et GPU partagé par quatre fenêtres (erreur d'orchestration, assumée).
- Retenu : un pilote doit vérifier que le modèle apprend la distribution, pas seulement la vitesse de calcul.

**13. L'architecture seule, avec un budget suffisant (E009-bis)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e009bis-procedure-apprise/research/experiments/E009bis-procedure-apprise) · pas encore relu
- Résultat : curriculum, largeur 128, jusqu'à 10 000 pas : **1 run sur 5** apprend la distribution (96,8 %), puis 17,3 % à 6 chiffres et 0 % au-delà.
- Verdict : **négatif** à ce budget. Calcul : ≈ 3 h 52.

**14. Enseigner comme à l'école : le brouillon de colonnes (E010)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e010-enseignement/research/experiments/E010-enseignement) · pas encore relu
- Changé : le modèle écrit chaque colonne (chiffres, retenue entrante, chiffre écrit, retenue sortante) avant la somme.
- Résultat : **10 000 exemples** suffisent pour 99,9 % dans la distribution ; sans brouillon, jamais 95 % avec jusqu'à 256 000, soit au moins 25 fois moins d'exemples. Énoncer la règle en une phrase n'apporte rien. Hors distribution : 33,1 % à 6 chiffres, **0 % dès 7**.
- Verdict : **réussi pour l'efficacité, négatif pour la longueur.**
- Retenu : la retenue est bien calculée, l'échec vient du **repérage** (quel chiffre lire, quand s'arrêter). Et une confiance prise sur la recopie finale est aveugle : 606 erreurs sur 669 sont « sûres ».

**15. L'objectif d'entraînement casse-t-il la règle ? (E011)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e011-objectif-mdl/research/experiments/E011-objectif-mdl) · pas encore relu
- Antériorité : Lan et al. (TACL 2022) obtiennent l'addition binaire exacte avec un objectif MDL ; arXiv 2505.13398 rapporte que la régularisation s'éloigne de la solution parfaite (sur d'autres tâches). Deux chiffres relayés par la veille étaient faux ; l'expérience les a corrigés.
- Changé : on part d'un réseau de 22 paramètres, exact par construction, et on l'entraîne.
- Résultat : entropie croisée seule, règle gardée **5/5** jusqu'à 1 000 bits. Pénalité L2 λ = 1 : 0/5 ; L1 λ = 1 : 2/5. MDL discret : 5/5, et le réseau se compresse (206 → 204 bits). Mon approximation différentiable de MDL : 4/5. Calcul : ~4 min sur CPU.
- Verdict : **réussi** (question tranchée pour ce réseau et cette tâche).
- Retenu : l'objectif n'est pas le plafond caché ; les fortes pénalités de poids le sont.

**16. L'évolution découvre-t-elle le circuit ? (E012)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e012-evolution/research/experiments/E012-evolution) · pas encore relu
- Changé : recherche évolutive guidée par MDL, avec moins de 0,6 % du budget de Lan et al.
- Résultat : binaire 0/5 ; décimal aligné 2/5 avec 100 exemples, **4/5 avec 1 000**, exact jusqu'à 1 000 chiffres ; entrée plate 0/5. Le plus court circuit trouvé est l'algorithme d'école, avec une seule unité qui est la retenue : `h = marche(a + b + h − 9)`, `sortie = a + b + h − 10·h`. Il est prouvé exact pour toute longueur. Calcul : ~204 min.
- Verdict : **réussi quand l'alignement est donné.**
- Retenu : dans les échecs, le circuit exact a un MDL bien plus bas que celui rendu. C'est la **recherche** qui échoue, pas l'objectif.

**17. Un accumulateur minuscule, « l'insecte » (E013)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e013-insecte/research/experiments/E013-insecte) · relu avec réserve (R010, R011, R012), non fusionné
- Antériorité : intégration de trajet chez l'abeille (Stone et al. 2017), un petit état mis à jour à chaque pas. L'analogie est la nôtre, pas celle des auteurs.
- Budget de structure : l'alignement des chiffres, le sens (poids faible d'abord) et le nombre de pas sont donnés.
- Résultat : **1 131 paramètres**, état d'un seul nombre : 100 % de 16 à 100 chiffres (5/5 graines), 99,3 % à 1 000. Avec deux nombres d'état : **100 % à 1 000 chiffres**, 5/5 graines, sur tous les adverses. Avec 1 000 exemples, les nombres longs passent (98,6 % à 1 000 chiffres) mais la propagation pure d'une retenue tombe à 52,9 % (1 graine sur 5) ; avec 10 000, 100 % partout. Sans alignement donné : 0/5. Calcul : 65 min.
- Verdict : **réussi, alignement donné.** Premier succès de longueur du projet.
- Retenu : avec un seul nombre d'état, le réseau se trompe « sûr de lui » sur les nombres creux (28 % de ses erreurs) : rien dans les données courtes n'y force « pas de retenue » à rester stable.
- Réserve : la synthèse du README a été contestée trois fois de suite (seuil d'exemples redit sans source). Elle est à reconcevoir avant fusion.

**18. Apprendre OÙ lire, puis composer (E014)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e014-reperage/research/experiments/E014-reperage) · pas encore relu (contre-vérifié par l'orchestrateur)
- Antériorité : non documentée dans le README. L'orchestrateur note après coup qu'une interface discrète partagée entre modules est connue (stitching, symboles partagés).
- Changé : un lecteur appris seul à « poser en colonnes », sans aucune addition dans sa perte, puis branché **gelé** devant l'accumulateur **gelé** d'E013, sans entraînement commun.
- Résultat : addition exacte à 16 et 100 chiffres sur **4 graines sur 5** ; 1/5 à 1 000 chiffres. Appris de bout en bout, le même lecteur échoue : 0/5, 1/5 avec curriculum, 0/5 avec pointeurs durs. En s'abstenant sous un seuil de confiance, il écarte 77 % de ses erreurs pour 1,4 % de ses réponses justes.
- Verdict : **réussi** pour la composition sans réentraînement.
- Retenu : la composition ne perd rien tant que la lecture est juste ; à 1 000 chiffres, c'est la lecture qui casse. Mais **quelqu'un a défini la tâche intermédiaire** et l'interface entre les deux modules.

### Partie 4 — Sans interface écrite par nous (27/09, soir)

Consigne de Malik à 20:35 : ne plus refaire du connu, prendre le contre-pied.

**19. Écosystème : des compétences s'assemblent-elles seules ? (E015)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e015-ecosysteme/research/experiments/E015-ecosysteme) · pas encore relu (contre-vérifié par l'orchestrateur)
- Antériorité (veille de 15 min) : PathNet, modular meta-learning, NPI, model stitching. Aucun ne demande à la fois de découvrir quels modules gelés enchaîner, l'ordre des opérations **et** l'interface symbole à symbole, avec pour seul signal un juge final.
- Résultat : assemblage libre **0/5** sur trois tâches nouvelles. Câblage donné, interface à inventer : **2/5**, exact jusqu'à 1 000 chiffres, avec une interface que nous n'aurions pas écrite. Qu'il manque une seule instruction au câblage : 0/5. Réutiliser une interface gagnante sur une autre tâche : aucun gain. Calcul : ≈ 1 h.
- Verdict : **négatif.**
- Retenu : la solution connue vaut 1,100 au juge, les programmes rendus entre 0,004 et 0,45. C'est encore la recherche qui échoue : un paysage en aiguille, où aucun câblage partiel n'est mieux noté que « recopier a ». Certaines interfaces fausses détournent un circuit de soustraction en additionneur sans retenue.

**20. « Mouches » : une langue commune par pression sociale ? (E016)** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e016-mouches/research/experiments/E016-mouches) · pas encore relu (contre-vérifié par l'orchestrateur)
- Idée de Malik : 3 agents « lecteurs » et 3 « additionneurs » gelés, aux codes privés incompatibles, un canal libre et un but commun. Récompense collective tout-ou-rien ; si un agent se trompe, tout le monde recommence.
- Antériorité : **déjà fait en partie.** Des réseaux gelés hétérogènes construisent un protocole commun (Mahaut et al., arXiv 2302.08913). Part nouvelle visée : des compétences procédurales, un calcul coupé en deux par le canal, un jugement jusqu'à 1 000 chiffres.
- Résultat : aucune langue commune (0 symbole partagé par les trois émetteurs, 25 runs sur 25). Règle collective : 0/5 graines, 1 ou 2 paires sur 9 par graine. Chaque graine produit un ou deux **idiolectes** de paire, parfaits. Les 13 paires apprises restent ≥ 90 % à 100 chiffres (13/13).
- Verdict : **négatif** pour la langue commune.
- Retenu : le tout-ou-rien collectif **coupe le signal** (0,0 à 0,1 % de tours réussis en équipe) ; le rejeu divise par 3,5 le nombre de problèmes neufs vus.

**21. E016, amendement A2 : un signal plus dense suffit-il ?** — [branche](https://github.com/malikkaraoui/EV-LLM/tree/exp/e016-a2/research/experiments/E016-mouches) (section A2 du README) · pas encore relu (contre-vérifié par l'orchestrateur)
- Antériorité (recherche approfondie, verdict « partiellement fait ») : Tieleman 2019 et Michel et al. 2023 (ce dernier non relu), où l'échange aléatoire de partenaires réduit déjà les idiolectes ; Mahaut et al. ; Marincat 2026.
- Changé : récompense = fraction des colonnes justes, ou curriculum à 1 chiffre. Pilote-garde préenregistré avant tout run.
- Résultat : **1 paire sur 9** dans les deux cas. Les émetteurs se figent encore plus vite (entropie 0,002 nat). Les conditions prévues n'ont pas été lancées. Calcul : ≈ 3 min.
- Verdict : **arrêt propre au pilote-garde.**
- Retenu : « il manque un signal dense » est réfuté sous cette forme (crédit scalaire par item). [HYPOTHÈSE] Le goulot serait l'attribution du mérite et l'exploration.

---

## Ce qu'on croit savoir aujourd'hui

- [VÉRIFIÉ — E011, E012, E013] **Calculer est facile avec presque rien.** Une fois les chiffres alignés, la retenue se découvre par évolution (E012 : une unité cachée) ou s'apprend (E013 : 1 131 paramètres) avec 100 à 10 000 exemples, reste stable sous entropie croisée (E011), et tient jusqu'à 1 000 chiffres.
- [VÉRIFIÉ — E008, E009-bis, E010, E013 I2, E014 R0] **Le mur, c'est repérer, aligner, brancher.** Chaque fois que le système doit trouver seul quel chiffre lire, il échoue hors des longueurs vues, quelle que soit sa taille (de ~1 900 paramètres à ~3,2 millions).
- [VÉRIFIÉ — E014, E015 ECH0, E016 DONNÉ] **Ce qui a franchi le mur : une interface symbolique discrète donnée.** Deux compétences gelées, reliées par des symboles, composent sans perte jusqu'à 100 chiffres, et souvent jusqu'à 1 000. Les limites restantes viennent de la lecture, pas du calcul.
- [VÉRIFIÉ — E012 X1, E015, E016, E016-A2] **Ce qui ne l'a pas franchi :** l'évolution aveugle sans alignement, l'assemblage libre, la pression sociale tout-ou-rien, un signal dense scalaire.
- [VÉRIFIÉ — E005, E006, E008, E010, E013, E015] **Une confiance mal placée est aveugle.** Les erreurs sont souvent « sûres » quand la confiance porte sur la mauvaise étape : la recopie, le calcul sans la lecture, les champions sans l'interface. Une confiance prise à chaque étape, lecture comprise, sépare beaucoup mieux (E014).
- [HYPOTHÈSE] Le levier manquant serait un **signal intermédiaire que la machine se donne elle-même** (cohérence entre modules, prédiction de ses propres flux), plutôt que le seul verdict final. Rien de cela n'a été testé.

---

## Ce qui n'a pas marché, et pourquoi c'est utile

Pour ne pas refaire ces cycles :

1. **Critère non atteignable** (A0, A0-bis, A0-ter). Même un oracle échouait. Cause : le critère récompensait un progrès continu et dépendait de la chance du premier monde. Remède adopté : oracle à 100 % et « par cœur » à 0 % avant toute mesure.
2. **Plafond au ratio sous bruit** (E002). Un ratio à un plafond négatif est indéfini. Remède : mesurer une différence à un plafond qui vérifie ses prémisses (E002-bis).
3. **Déclencheur inerte** (A0). Un coût de vérification exprimé en bits absolus, alors que R est un rapport, rendait toute vérification non rentable.
4. **Sous-budget et GPU partagé** (E009). Aucun apprentissage même dans la distribution : la question n'est pas tranchée, elle n'a pas été posée. Remède : un pilote qui vérifie qu'on apprend la distribution.
5. **Architecture seule sans alignement** (E009-bis). Un run sur cinq apprend, et il ne généralise pas.
6. **Règle énoncée en une phrase** (E010). Un modèle qui ne lit pas la langue n'en tire rien.
7. **Confiance sur la mauvaise étape** (E010, E014, E015). Voir ci-dessus.
8. **MDL différentiable approché** (E011). Il se comporte comme une pénalité de poids et casse une graine : à ne pas réutiliser tel quel.
9. **Évolution en binaire** (E012). Toutes les graines tombent dans un piège « hésitant » qu'il faudrait quitter en passant par des étapes plus coûteuses : la sélection par troncature l'interdit.
10. **État d'un seul nombre** (E013). Parfait dans la distribution, faux et sûr sur les nombres creux ; un deuxième nombre d'état suffit ici.
11. **Pointeurs durs appris** (E014 R2). 0 même dans la distribution : [HYPOTHÈSE] une instabilité d'optimisation, pas une preuve contre les pointeurs.
12. **Assemblage libre** (E015). Paysage en aiguille : plus d'essais (400 000 au pilote) ne changent pas l'attracteur « recopier a ».
13. **Tout-ou-rien collectif avec rejeu** (E016). Il gèle l'équipe au lieu de fabriquer un pont.
14. **Signal dense scalaire et curriculum court** (E016-A2). Verrouillage plus rapide, pas de décollage.
15. **Accès aux API** (E001, E003). Carte bancaire exigée malgré « gratuit », limite de 5 requêtes par minute pour le compte, modèles fermés au niveau gratuit, fournisseur non imposé.
16. **Incidents d'outillage.** Ordre d'itération dépendant de `PYTHONHASHSEED` (E002-bis). Bytecode `.pyc` obsolète après une mutation de même taille restaurée dans la même seconde (E013 : `PYTHONDONTWRITEBYTECODE=1`). Fichier d'état partagé écrasé par une fenêtre (26/09).

---

## Pistes ouvertes (non lancées, sans promesse)

- **Reconcevoir la synthèse d'E013**, une source par chiffre, puis la faire relire. E008 et E013 pourront alors être fusionnés.
- **Crédit par colonne** (E016). La récompense de la colonne t ne pousse que les choix de la colonne t ; d'autres variantes sont nommées dans le README d'E016 (plancher d'entropie, partenaire gelé en alternance).
- **E015-A2 : l'interface comme objet de premier rang.** Une archive d'interfaces co-évoluée, jugée sur sa réutilisation, gelée, sur des tâches jamais vues. Antériorité faite par l'orchestrateur (verdict « partiellement fait ») : PathNet, BounceGrad, Braylan 2016, Guijt et al. 2024, Cully 2015, Schug 2024, MAGELLAN, DreamCoder / Voyager / FunSearch. Non trouvé : une mesure de la réutilisation de l'interface elle-même. La piste voisine, faire co-évoluer les problèmes avec les solveurs, a aussi fait l'objet d'une recherche de l'orchestrateur le 27/09 (novelty search, MCC de Brant & Stanley, PowerPlay, DreamCoder, HOUDINI, CRL). Son verdict, « chaque brique existe, l'assemblage non », n'est pas encore versionné dans le dépôt [HYPOTHÈSE jusqu'à publication des sources].
- **Critère ACQUÉRIR v2** (A0-ter) : contraste avec un jumeau amnésique, seuil calibré sur le bruit, validé d'abord sur l'oracle.

---

## Reproduire

Machine utilisée : Mac Apple M1 (16 Go), Python 3, MLX 0.29.3, numpy 2.0.2. Les expériences E001 à E007 appellent une API payante par la passerelle Vercel ; il faut une clé dans un fichier `.env` (modèle : [`.env.example`](.env.example)), jamais versionné. Les autres expériences tournent hors ligne.

Environnement (README d'E008 ; `requirements.txt` est sur la branche `exp/e008-addition`) :

```
python3 -m venv $HOME/.venvs/ev-llm-e008
$HOME/.venvs/ev-llm-e008/bin/pip install -r research/experiments/E008-addition/requirements.txt
```

Pour une expérience sur branche : `git checkout <branche>`, puis les commandes ci-dessous depuis la racine. Seules les commandes de **tests** sont reprises ici ; les commandes complètes (entraînement, évaluation, analyse) sont dans le README de chaque expérience.

| expérience | branche | tests (commande du README) |
|---|---|---|
| E001 | `main` | `cd research/experiments/E001-jev-sonde && python3 -m unittest test_aggregate` |
| E002 | `main` | `cd research/experiments/E002-relations-opaques && python3 -m unittest discover` |
| E002-bis | `main` | `cd research/experiments/E002bis-mesure && python3 -m unittest discover` |
| E003 | `exp/e003-etalon-llm` | `cd research/experiments/E003-etalon-llm && python3 -m unittest -v test_run_llm` |
| E006 | `exp/e006-replication-frontiere` | `cd research/experiments/E006-replication-frontiere && python3 -m unittest test_run_paced` |
| E007 | `exp/e007-regles` | `cd research/experiments/E007-regles && python3 -m unittest test_run_e007` |
| A0 | `exp/a0-candidat` | `cd research/candidats/A0 && python3 -m unittest discover` |
| A0-bis | `exp/a0bis-candidat` | `cd research/candidats/A0bis && python3 -m unittest discover` |
| A0-ter | `exp/a0ter-candidat` | `cd research/candidats/A0ter/oracle && python3 -m unittest discover` |
| E008 | `exp/e008-addition` | `cd research/experiments/E008-addition && $PY -m unittest -v test_e008` |
| E009 | `exp/e009-procedure-apprise` | `cd research/experiments/E009-procedure-apprise && $PY -m unittest -v test_e009` |
| E010 | `exp/e010-enseignement` | `cd research/experiments/E010-enseignement && $PY -m unittest -v test_e010` |
| E011 | `exp/e011-objectif-mdl` | `cd research/experiments/E011-objectif-mdl && $PY -m unittest -v test_e011` |
| E012 | `exp/e012-evolution` | `cd research/experiments/E012-evolution && $PY -m unittest -v test_e012` |
| E013 | `exp/e013-insecte` | `cd research/experiments/E013-insecte && $PY -m unittest -v test_e013` |

`$PY` désigne `$HOME/.venvs/ev-llm-e008/bin/python`. Pour E013, les README demandent aussi `export PYTHONDONTWRITEBYTECODE=1`.

Commandes données telles quelles par leur README, sans `cd` :
- E005 (`main`) : pas de commande de test propre ; le rejeu passe par ses scripts et par `run.py` / `aggregate.py` d'E001 (voir son README).
- E009-bis : `python -m unittest test_e009bis` (dans son dossier).
- E014 : `python -m unittest test_e014`.
- E015 : `python -m unittest test_e015`.
- E016 : `source $HOME/.venvs/ev-llm-e008/bin/activate`, `cd research/experiments/E016-mouches`, `python test_e016.py`.
- E016-A2 : le README cite `test_e016a2.py` (4 tests) sans commande ; aucune n'est donc donnée ici.

Le GPU MLX n'est pas reproductible au bit près : un rejeu donne des chiffres très proches, pas forcément identiques. Les expériences numpy sur CPU (E011, E012) et les bancs E002 / A0 sont déterministes, graines ou `PYTHONHASHSEED` fixés.

---

## Comment le projet est conduit

Une fenêtre d'orchestration, qui ne code pas, écrit des mandats autonomes. Un superviseur déterministe lance chaque fenêtre de travail, et chaque rendu est doublé par une relecture indépendante avant toute fusion. Le dépôt est public, et aucune donnée secrète n'y est versionnée (la clé d'API reste dans un `.env` ignoré par git). Mandats, rapports, revues et tableau de bord : [`vault/`](vault/) (index : [`vault/reprise/00_INDEX.md`](vault/reprise/00_INDEX.md) ; revues : [`vault/revues/`](vault/revues/)).

---

## Licence et citation

Licence : à définir. Aucun fichier de licence n'est présent dans le dépôt à ce jour.

Pour citer une expérience, pointer le README de son dossier et le SHA du commit lu : les chiffres y sont rattachés à leurs fichiers de résultats.
