---
date: 2026-09-25
tags: [reprise, sessions, tableau-de-bord]
maintenu_par: orchestrateur
derniere_maj: 2026-09-29T10:20:38+02:00
---

# Tableau de bord — sessions du projet ev-llm

> **29/09 10:25** : R014 **RÉSERVE 8/9** (2e fois la même classe : puces [VERIFIED] non portées par leurs sources — E012 X1 est *aligné* ; « single exception » contredit E008) → **loi des deux patchs** : M0039 = reconception bottom-up des puces de synthèse (procédure imposée, aucune formulation dictée), puis R015. README toujours pas sur `main`. **Latence** : réveil 28/09 10:45 → reprise 29/09 10:19 (24 h).

<!-- rotation-index -->
> **Index court (rotation).** Seuls les derniers jours d'activité sont ici. L'historique complet
> est dans `vault/reprise/archive/index/00_INDEX-AAAA-MM.md` — le chercher par mots-clés, ne
> jamais le charger en entier. Le hook `pre-commit` livré avec ce scaffold refuse un commit qui
> ferait dépasser la limite d'octets à ce fichier, et imprime le remède : c'est le seul garde-fou
> contre un index de plusieurs centaines de kilo-octets relu à chaque démarrage de session.

<!--
CONVENTION D'ÉCRITURE — une entrée par mandat ou revue traité, ordre ANTI-CHRONOLOGIQUE
(le plus récent en tête, immédiatement sous ce bloc). Format d'une entrée :

## <horodatage ISO 8601 avec fuseau> — <Mxxxx|R0xx> (<Fxx>) : <verdict en UNE phrase>

- <fait vérifiable, avec son pointeur : rapport, branche, SHA — jamais un ressenti>
- <ce qui est mergé / non mergé, et ce qui bloque, nommé>
- <réserve ou trou assumé, s'il y en a un — l'absence de réserve se dit aussi>
- <leçon ou décision rattachée, par lien>

Règles :
- Le titre H2 porte le VERDICT, pas le sujet : il doit se lire seul, sans ouvrir le rapport.
- 2 à 4 puces, pas davantage : ce fichier est un index, pas un rapport.
- Jamais de narration : ce qui mérite d'être raconté va dans `vault/revues/`, et l'entrée pointe.
- Cette entrée est une DÉCLARATION, pas une preuve (voir `vault/runtime/README.md`).

Exemple (à supprimer à la première entrée réelle) :

## AAAA-MM-JJTHH:MM:SS+00:00 — <R0xx> (<Fxx>) doublage de <Mxxxx> : GO, mergé <sha court>

- Rapport : `vault/revues/AAAA-MM-JJ-<R0xx>-<slug>.md` ; branche `<branche>` (tip `<sha>`).
- Symptôme d'origine rejoué avant/après ; tests re-mesurés par le doubleur, pas repris du rapport d'auteur.
- Réserve non bloquante : <réserve nommée, ou « aucune »>.
-->

## 2026-09-29T10:20:38+02:00 — R014 (F03) : **RÉSERVE 8/9 — même classe que R013** (l.191 « évolution sans alignement » alors qu'E012 X1 = binaire *aligné* ; l.189 « unique exception » ajoutée par M0038 contredite par E008 B-REF 91,2 % à 6) → **loi des deux patchs : M0039 reconception**, pas de 3e correctif

- Rapport `vault/revues/2026-09-28-R014-readme-licence-final.md` (`ed790c9`) : 17/17 chiffres neufs exacts, 5/5 formules, 31/31 liens, LICENSE OSI, 4/4 trailers ; 4 puces [VERIFIED] portées, 2 non portées. Contre-vérif orchestrateur : E012 l.40/43, README l.189–191 — fondé.
- **Mécanisme fautif nommé** : puces de synthèse écrites de haut en bas (idée puis sources), y compris par l'orchestrateur dans M0034/M0038 (« nécessaires », « exact », « unique exception »). M0039 impose la procédure inverse : inventaire des puces → découpage en affirmations atomiques → tableau affirmation → source:ligne → portée/non portée → réécriture ne gardant que le porté → relecture croisée interne. Aucune formulation dictée.
- Leçon transverse candidate (R014) : une clause d'exclusivité ajoutée par un correctif doit être vérifiée contre TOUTES les sources de l'étiquette.
- Archive : `2026-09-28-F03-R014-readme-licence-final.md`.

## 2026-09-28T10:15:30+02:00 — M0038 (F01) : **6 correctifs README appliqués et sourcés** (`f99553a`) ; l'auteur a durci une formulation dictée par le mandat (E014 : « ≥ 90 % » et non « exact », s2 = 98,4 %) → R014 posé · **Cap « la quête » gravé** · antériorité de la 1re expérience de la file rendue

- M0038 : diff README seul, 6 zones ; chaque retouche « source / avant / après » ; contre-vérif orchestrateur E014 l.71, E016 l.125–126. Écart utile : la source a corrigé le mandat — l'orchestrateur avait encore écrit un « exact » trop fort. Leçon : ne jamais dicter une formulation chiffrée sans avoir la ligne source sous les yeux.
- Décision Malik 09:05 (verbatim dans `vault/decisions/2026-09-28-la-quete-additionner-vs-compter.md`) : « S'ils n'y arrivent pas, c'est qu'ils savent additionner sans savoir ce que compter veut dire » = **la quête**. Semaine = édition d'une file d'expériences cadrées (témoin, procédure aussi propre que l'expérience), zéro calcul ; antériorité pour s'orienter ou consolider (09:06).
- Antériorité (agent, 16 sources) : **non trouvé** pour « additionneur gelé qui attend un événement » ; **consolide** : Meck & Church 1983 (un accumulateur, deux modes event/run), NALU 2018 (compter ≠ additionner), Kim 2021 (témoin aléatoire obligatoire), revue omission 2022 (flux irrégulier = témoin), Hollerman 1998 (retardé vs omis). Contre-pied : transfert dans les deux sens. Note : `vault/notes/2026-09-28-anteriorite-additionner-vs-compter-temps.md` (à committer).
- Latence : réveil 09:25 tiré à 09:28, session reprise à 10:13 (approbation côté app).

## 2026-09-28T09:04:14+02:00 — R013 (F03) : **RÉSERVE 7/9 — pas de merge** (E012 : `h = step(a+b+h−9)` a perdu ses indices `h(t−1)`/`h(t)` ; puce « compose sans perte jusqu'à 100, souvent 1 000 » contredite par 4/5, 2/5, 71,7 % et ECH0 = interface inventée) → M0038 posé

- Rapport `vault/revues/2026-09-28-R013-readme-licence.md` (`ddf13d1`) : 87 renvois chiffre→ligne vérifiés (0 absent, 0 différent), 31/31 liens, 21/21 statuts, LICENSE identique au texte OSI, 3/3 trailers. Défauts = contexte et formules, pas les nombres.
- Contre-vérif orchestrateur : E012 l.28–29 (`h1(t−1)`), E015 ECH0 2/5, E014 1/5 à 1 000, DONNÉ 71,7 % — réserve fondée. **Angle mort nommé** : mon contrôle M0035 (5 chiffres) et la preuve M0036 (627 nombres) ne regardaient que des nombres ; une formule peut garder ses chiffres et devenir fausse. La formule fautive vient de la version FR (M0035).
- M0038 : 6 retouches (l.141, 190, 189, 180, 61, 148), chacune « source / avant / après » au rapport, README seul. Puis R014.
- Archive : `2026-09-28-F03-R013-readme-licence.md`.

## 2026-09-28T08:37:00+02:00 — M0036 + M0037 (F01) : **README en anglais, titre 🧠🐜, 627 nombres identiques à la version FR ; LICENSE MIT** → R013 posé (F03)

- M0036 `ebec0d3` : traduction fidèle (identité ordonnée des 627 nombres, même somme de contrôle), H1 `# 🧠🐜 EV-LLM — a public research log`, 4 notes vault committées sur main (`5b977eb`) et liées ; contre-vérifié par l'orchestrateur (H1, absence de mention de l'enfant, liens).
- M0037 `6812d10` : LICENSE MIT 21 l. (clauses vérifiées), section License du README. **Décision Malik 08:14 : « MIT licence / Évidement »**. Défaut de forme (modèle léger) : 2e ligne `statut:` ajoutée au lieu de remplacée ; superviseur a fermé sur la dernière ; rituel « Main push » de la reprise non fait par la fenêtre mais commit `8be0f35` présent — sans conséquence.
- R013 : 9 axes (périmètre, ≥ 15 chiffres au tip, statuts de relecture, liens, honnêteté, consignes Malik, LICENSE, sécurité, trailers) ; merge `--no-ff` + `ff-only` si GO.
- Archives : `2026-09-28-F01-M0036-readme-anglais.md`, `2026-09-28-F01-M0037-licence-mit.md`.

## 2026-09-28T08:08:20+02:00 — M0035 (F01) : **README racine écrit** (FR, 282 l., `99ccc79`, chaque chiffre sourcé fichier:ligne) ; contre-vérifié 5/5 ; **M0036 posé** (anglais + titre 🧠🐜 + notes versionnées)

- Branche `docs/readme-2026-09-28` depuis `main` `10b8774` ; diff README.md seul ; 21 entrées (question, antériorité, changé, résultat, verdict, retenu, statut de relecture) ; méthode en tête ; 16 impasses ; pistes sans promesse ; reproduction (commandes des README seulement) ; aucune mention de l'enfant ; « licence : à définir ».
- Contre-vérif orchestrateur : E011 l.12–16, E014 l.104, E008 l.28/78–80, E015 l.163–165, E016 l.175 (771 000/217 000 = 3,55) — conformes.
- Décisions de l'auteur validées : notes non versionnées signalées plutôt que liées ; recherche d'antériorité de l'orchestrateur marquée [HYPOTHÈSE] tant qu'elle n'est pas dans le dépôt → note `vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md` écrite par l'orchestrateur, à committer par M0036.
- Consignes Malik 08:06–08:07 : README **en anglais**, emojis 🧠 🐜 **bien gros dans le titre** → M0036.

## 2026-09-28T07:42:07+02:00 — R012 (F03) : **RÉSERVE** (l. 195 « ~10⁴ nécessaires » contredit par I3-N1000 s4 = 102/102/102 ; 3e occurrence → loi des deux patchs, reconcevoir la synthèse) · M0032 E016-A2 (F02) : **STOP propre au pilote-garde** — signal dense par colonne 1/9, curriculum 1/9, verrouillage accéléré (0,002 nat) ; aucune condition lancée

- R012 : rapport `vault/revues/2026-09-27-R012-e008-e013-redoublage-final.md` (`b824fc8`) ; 6/7 ✅ ; **la phrase fautive était dictée par M0034 §2.1 (orchestrateur)** — contre-vérifié : l. 100 du README, graine 4 = 102/102/102 à N = 1 000. E008+E013 toujours **non mergés**. Suite proposée : mandat « reconception de la section Lecture d'E013 : une source par chiffre, pas de seuil redit » puis R013.
- M0032 `1c98601` : préreg A2 `85264fc` poussé seul ; pilotes graine 0 (83 s + 79 s) ; réfute « il manque un signal dense » sous forme scalaire ; option proposée par l'auteur : crédit **par colonne** (la récompense de la colonne t ne pousse que les choix de la colonne t). Contre-vérifié depuis `pilotes.json`. Écart mineur : pilotes exécutés avant le commit du code (code identique, commité avant les valeurs).
- **Incident harnais (orchestrateur)** : réveil « 23:35 » tiré à 23:35:57, session cowork reprise à 07:40 → 8 h sans veille ; rapports rendus à 23:19 / 23:25 non traités avant. Cause [VÉRIFIÉ, Malik 07:48] : demande d'approbation en attente dans l'app Claude. Leçon : un réveil de session n'est pas une veille ; tout ce qui doit tourner la nuit se lance avant le départ de Malik.
- Archives : `2026-09-27-F01-M0030-e015-ecosysteme.md`, `2026-09-27-F02-M0032-e016-a2-stop.md`, `2026-09-27-F03-R012-redoublage-final-e008-e013.md`.

## 2026-09-27T23:19:30+02:00 — M0030 E015 (F01) : **NÉGATIF — la machine n'assemble pas seule ses compétences** (0/5 partout sauf câblage donné ECH0 2/5, exact à 1 000) · M0031 E016 (F04) : **NÉGATIF — aucune langue commune** (C = 0/11 ×15, 1–2 idiolectes par graine) · M0034 rendu → R012 posé · F02 M0032 lancé (amendé) · F05 M0033 retenu

- M0030 `58abf67` (#28) : EVO/ALEA/SANS-VIE/ECH1/ECH2 0/5, N2/N3 froid et chaud 0/5 ; ECH0 2/5 exact 100 % à 1 000 (s3 : 27,5 % en propagation pure) ; interfaces inventées lisibles, détournements (s4, s5 faux et sûr 4 606/4 606) ; diagnostic : solution connue vaut 1,100 au juge, rendus 0,004–0,45 → **c'est la recherche qui échoue** ; programme N1 sur N2/N3 = trivial → **la réutilisation n'a pas de prise**. Écart tracé (A1 : vie par balayage, 150 k essais, échelle ECH ajoutée). **Contre-vérif orchestrateur** depuis `resultats.json` : graines/adverses/faux-sûrs conformes ; préreg `f8cd480` < code ; 4/4 trailers ; périmètre E015 seul.
- M0031 `867ccaf` (#29) : DONNÉ 9/9 ×5 (100 % à 16/100, 71,7 % à 1 000) ; COLL 1;1;1;1;2 paires/9, IND 0;2;2;1;2, COUPÉ 0 ; phase 2 COLL 0 ; cause proposée : succès exact ≈ 0,05 % + effondrement (entropie 0,1 nat) ; **manque nommé par l'auteur : signal dense, non testé**. **Contre-vérif orchestrateur** : recalcul par_paire identique, C = 0 sur 15 runs ; préreg `0bf43e1` < code ; 5/5 trailers ; branche empilée sur e014 (diff vs main inclut E008/E013/E014 non mergés — attendu).
- Décisions orchestrateur (nuit, Malik absent — à confirmer) : M0032 amendé (0-bis) plutôt que lancé tel quel (comparer des zéros = connu) ; M0033 **non lancé** (prémisse réfutée), réécriture contre-pied préparée en-pose.
- Archives : `2026-09-27-F04-M0031-e016-mouches.md`, `2026-09-27-F03-M0034-e013-micro-correctif.md` ; F01 à archiver à la pose de F05 v2.

## 2026-09-27T21:37:30+02:00 — R011 (F03) re-doublage E008+E013 : **RÉSERVE** (correctif M0029 exact au bit près ; paraphrase résiduelle README E013 l. 195) → **M0034 micro-correctif posé** (F03, `pret-a-lancer`) ; R012 ensuite

- Rapport : `vault/revues/2026-09-26-R011-e008-e013-redoublage.md` (`de5610a`, main) ; branche `exp/e013-insecte` tip `a749c29` inchangée. 6/7 axes ✅ ; axe 4 ⚠️ : « s'apprend avec ~10³ exemples » contredit par ADV-PROPAG (I3 N = 1 000 : 52,9 % / 1 sur 5 à 1 000 chiffres).
- Contre-vérification orchestrateur (`git show a749c29:…/README.md` l. 100, 169–176, 193–195) : contradiction réelle, réserve fondée. Pas de merge.
- M0034 : une phrase à aligner + chasse aux paraphrases (leçon R011), README seul, tests verts, nouveau tip = garde de R012 (re-doublage puis merge E008+E013 si GO).
- Archive : `vault/echanges/archive/2026-09-27-F03-R011-redoublage-e008-e013.md`.

## 2026-09-27T20:37:46+02:00 — M0029 correctifs E013 (ADV-PROPAG : I1 100 % en propagation pure 20/20 ; I3-N1000 insuffisant, N10000 OK) ; **cap Malik : ne plus refaire du connu — contre-pied** ; vague E015 écosystème + E016 mouches + R011

- M0029 `a749c29` : ADV-PROPAG post hoc ; I3 reformulé ; ddof déclaré. R011 re-doublage (F03, merge E008+E013 si GO).
- Consigne Malik 20:35 : « interdis-toi de faire quelque chose de connu si c'est pour arriver au même résultat ; prends le contre-pied ». Chaque mandat commence par 20 min de veille : ce qui existe / en quoi on diffère.
- M0030 E015 (F01) : population de circuits + bibliothèque + satisfaction = progrès jugé de l'extérieur ; la machine doit **assembler seule** des compétences sans interface écrite par nous.
- M0031 E016 (F04) « mouches » (idée Malik) : 3 agents langage A + 3 agents langage B, codes privés incompatibles, canal libre, but commun, récompense collective tout-ou-rien avec remise à zéro : langue commune par pression sociale ?

## 2026-09-27T19:16:46+02:00 — **M0028 E014 : COMPOSITION SANS RÉENTRAÎNEMENT — lecteur appris seul + accumulateur E013 gelés = addition exacte à 16 et 100 chiffres, 4/5 graines** ; bout en bout 0/5 ; R010 RÉSERVE (I3 à reformuler) ; E009-bis négatif

- M0028 `fc698b4` (#27) : R1G (lecteur « poser en colonnes » sans somme dans sa perte, gelé, devant I1 E013 gelé, 0 pas joint) 4/5 à 16/100, 1/5 à 1 000 (interface douce ; dure = lecture, post hoc) ; R0a 0/5, curriculum 1/5, pointeurs durs 0/5. Abstention : 77 % des faux pour 1,4 % des justes. **Contre-vérif orchestrateur** depuis `eval.jsonl` (vérité a+b) : s1–s4 500/500 à 10/16/32/64, s5 0/500 — conforme.
- R010 (doublage E008+E013) : RÉSERVE 6/7 — I1 confirmé en numpy 15/15 graines ; I3 « 1 000 ex. suffisent à 100 chiffres » contredit en propagation pure → M0029 correctifs (F03).
- M0027 E009-bis : 4/5 n'apprennent pas la distribution à 10 000 pas ; A3 s1 apprend sans généraliser (17 % à 6). Voie « architecture seule, sans alignement » : bloquée à ce budget.
- Interface discrète = clé de la composition (connu en littérature : stitching / symboles partagés). E015 « écosystème » proposé à Malik, en attente.

## 2026-09-27T17:46:45+02:00 — M0025 E012 : **l'évolution + MDL découvre le circuit de la retenue en décimal (4/5 à 1 000 exemples, prouvé toute longueur 2 fois)** ; binaire 0/5 ; entrée plate 0/5

- `0a33881` (#26) : X2 décimal aligné 100 ex. 2/5, 1 000 ex. 4/5 ; circuit minimal `h = marche(a+b+h−9)`, `sortie = a+b+h−10h` prouvé (automate exact, 20 états) ; X1 binaire 0/5 ; X3 plat 0/5. Échecs = la **recherche**, pas l'objectif (MDL du circuit exact plus bas).
- Contre-vérification orchestrateur : `resultats.json` concordant (n_exactes 0/2/4/0) ; formule du circuit simulée indépendamment sur 200 paires de 1 000 chiffres : 200/200.
- Convergence E010/E012/E013 : **calcul résolu avec presque rien, verrou = alignement/repérage**. R010 (doublage E008+E013) posé.

## 2026-09-27T16:18:27+02:00 — M0026 E013 : **PREMIER SUCCÈS — accumulateur de 2 unités, addition exacte jusqu'à 1 000 chiffres, 5/5 graines, dès 1 000 exemples** (alignement + sens DONNÉS) ; entrée plate 0/5 → E014 repérage

- `3246ae8` (#25) : I1 H=2/4/8 100 % à 16/100/1 000 + adverses ; H=1 casse sur les nombres creux ; seuil d'exemples entre 100 et 1 000 ; I2 (entrée plate, pointeurs appris) 0/5. Référence Stone 2017 vérifiée.
- Contre-vérification orchestrateur **indépendante** : réimplémentation numpy des poids, paires tirées à neuf (graine 424242) : 100 % à 16/100/1 000, cascade/creux/asymétrique OK (H=2 s1/s3/s5, I3-N1000 s1/s4) ; I3-N100 0 % ; H=1 échoue au creux — conforme au rapport.
- Budget de structure : alignement des colonnes et sens poids faible → le verrou restant est le **repérage** (convergent avec E010). Suite : M0028 E014 (lecture apprise, composition gelée = transfert).

## 2026-09-27T14:32:02+02:00 — M0022 E009 : **non mesuré** (0 % même en distribution, budget trop court + GPU partagé) → E009-bis ; M0023 E010 : **le brouillon fait gagner ≥ 25× en exemples mais 0 % dès 7 chiffres** (échec = localité)

- M0022 `20f289b` (#24) : 5 archis × 2 graines, T-ID ≤ 3 % ; test valide ; cause budget/largeur/GPU partagé (orchestrateur : trop de calcul en parallèle). Correctif M0027 : budget adaptatif jusqu'à T-ID ≥ 95 %, curriculum, GPU prioritaire.
- M0023 `19f7f0d` (#23) : F1-NoPE (brouillon) T-ID 99,9 % dès 10 k exemples (F0 jamais à 256 k) ; VAL 6 : 33 % ; 0 % dès 7 ; règle énoncée seule (F2) inutile ; confiance sur la recopie finale aveugle (606/669 faux sûrs). JSON recontrôlé.
- Leçons : un pilote doit vérifier l'apprentissage en distribution ; l'autodiagnostic doit porter sur les étapes qui calculent.

## 2026-09-27T13:01:03+02:00 — M0024 E011 : **l'entropie croisée seule GARDE la règle exacte (5/5) ; ce sont L2/L1 forts qui la cassent** ; MDL discret 5/5 ; STOP partiel (chiffres de veille contredits)

- `994c77b` (#22) : départ solution exacte d'addition binaire ; CE 5/5, L2 λ=1 0/5, L1 λ=1 2/5, MDL discret 5/5, MDL différentiable 4/5 (JSON recontrôlé par l'orchestrateur).
- Veille corrigée : « 1 unité / 7 connexions » = tâche aⁿbⁿ, pas l'addition (2 unités) ; la « dérive CE » de 2505.13398 ne porte pas sur l'addition et régularise.
- Parties 2–3 (recherche évolutive, pont décimal) non faites → candidat E012 « évolution », en attente de Malik.

## 2026-09-27T09:34:26+02:00 — M0021 E008 : **test valide ; transformer 0 % dès 6 chiffres, référence 91 % à 6 puis 0 dès 8** ; vague E009–E011 posée (A + B + objectif)

- M0021 `af281f5` (#21) : C-ORACLE 100 %, C-PARCŒUR 0 % ; B-STD 0 % de 6 à 16 ; B-REF 91,2/7,9/0,1 % à 6/7/8 ; faux et sûr massif hors distribution. Recalcul indépendant orchestrateur depuis `eval.jsonl` : concordant.
- Veille (27/09) : littérature = boucle locale + calcul proportionnel + pas de position absolue ; **piste manquée : objectif MDL** (Lan et al. TACL 2022 : addition binaire exacte, 100 exemples, prouvée) ; revue hostile → protocole durci (validation OOD 6–8, test 10–100 intouché, ≥ 5 graines, tests adverses).
- Vague : M0022 E009 A (Neural GPU, Deep Thinking, Looped NoPE sans T(n)) · M0023 E010 B (enseignement explicite, courbe d'exemples) · M0024 E011 (entropie croisée vs MDL).

## 2026-09-26T21:03:45+02:00 — Vague 6 + **changement de cap** : critère ACQUÉRIR inatteignable même par un oracle (M0020) ; Jev arrêté ; E008 « addition » lancé

- M0020 `395550e` : oracle-acquéreur 2/4 → **le critère ACQUÉRIR ne mesurait pas l'apprentissage** ; échecs A0/A0-bis non informatifs sur les candidats. R009 ⚠️ confirme les échecs (lecture A0-bis dépend d'une seule graine).
- M0017 E007 : Jev lit les règles **partiellement**. M0018 : lecture E006 amendée (`ad54bd4`, re-doublage à faire). M0019 : fournisseur imposé E003 (`4e2b02b`, #19) ; rejeu E003 **annulé** (arrêt Jev).
- Décision Malik 26/09 : fin des tests Jev ; cible = apprendre une **procédure** (généralisation), puis transfert, puis apprentissage continu, sur modèle local (M1 16 Go, MLX).
- M0021 E008 palier 0 : validité du test (oracle / par-cœur) + références B-STD et B-REF (NoPE + inversé).

## 2026-09-26T18:03:33+02:00 — Vague 5 : **E005 mergé (R007 GO)** ; E006 en RÉSERVE (2 « faux et sûr » reclassés contestés) ; A0-bis échoue 0/4 ; défaut fournisseur E003 ; vague 6 posée

- R007 GO 7/7 → E005 mergé (`e1448c4`). R008 ⚠️ E006 : R-F4-04 et L-DIS1 **contestés** (question ambiguë dans un ensemble contradictoire) → compte honnête : **5 faux et sûr non contestés + 1 contesté** (et non 6) ; correctif README M0018.
- M0015 E003 `bbc50ae` : raw.public.jsonl + `.gitignore` pilot/. **Défaut orchestrateur** : aucun fournisseur imposé ni journalisé (gemini servi via Vertex) → backend non contrôlé ; M0019 (fournisseur imposé, 402 = arrêt), rejeu M0021.
- M0016 A0-bis `1be4654` : ÉCHEC ACQUÉRIR 0/4 ; coût marginal active 22.6 requêtes, exactitude 0.83, R̂_diff −0.0105 ; MLE de bruit biaisé (échantillon sélectionné).
- Vague 6 : M0018 E006 Lecture · M0019 E003 fournisseur · R009 doublage A0+A0-bis · **M0020 ACQUÉRIR atteignable ? (oracle) puis A0-ter** · M0017 E007 toujours en vol.

## 2026-09-26T17:32:59+02:00 — Vague 4 : **E006 réplique les 6 « faux et sûr » de Jev** ; A0 échoue ACQUÉRIR (cause trouvée) ; doc v2.2 mergée ; vague 5 posée

- M0011 E006 `57e0e41` : 6/6 répliqués (5/5 appels) ; forme **correcte** notée plus bas que la forme fautive sur 2/3 paires ; T1-A perd la contradiction dès 1 distracteur ; pas de pente 2–6 pas ; contamination disjointe nulle (|écart| ≤ 0.012). 103×200 à 26 s.
- M0014 A0 `8a60250` : ÉCHEC ACQUÉRIR (1/4) ; meilleur système sans propriétés données (R̂_diff −0.011) ; déclencheur inerte (coût absolu vs R rapport) → A0-bis.
- R006 GO → doc v2.2 + GENESE mergées (réserve : GENESE cite l'enfant de Malik — décision de Malik). R005 ⚠️ (raw.jsonl suivis) → M0015. M0013 → E005 corrigé `15487b0`.
- Vague 5 : R007 (E005) · M0015 (E003) · R008 (E006, merge après E005) · M0016 A0-bis · M0017 E007 « Jev lit-il les règles ? ».

## 2026-09-26T17:08:23+02:00 — Vague 3 : E002-bis mergé (R003 GO), E005 CASSÉ sur un total (R004), E003 complet, doc v2.2 prête ; vague 4 posée

- R003 GO → E002-bis mergé (`main` contient d35af60). R004 ⛔ : totaux HTTP du README E005 faux (7×503/110×429) — **les 6 « faux et sûr » de Jev sont confirmés par sources (0 contesté)** ; correctif M0013.
- M0010 E003 `73cdc79` : 60/60 mesuré, 0×429 grâce au rythme 26 s ; seul « faux et sûr » : gpt-4.1-mini sur T1-A `e_sup_d` (contamination ?).
- M0012 doc `bcfb722` : GENESE +11 entrées, architecture v2.2 (D17–D21).
- Vague 4 : M0013 correctif E005 · R005 doublage E003 · R006 doublage doc v2.2 · **M0014 A0, premier candidat ACQUÉRIR** · (M0011 E006 toujours en vol).

## 2026-09-26T16:38:48+02:00 — Vague 2 rendue : E001+E002 mergés (GO), mesure E002 réparée, **premiers « faux et sûr » de Jev** ; vague 3 posée

- R001 GO → E001 mergé ; R002 GO → E002 mergé (`main` contient 7e953a9 et 1cb586b ; `main` = df79ad6).
- M0007 E002-bis `d35af60` : plafond-vérificateur R > 0 sur 20/20 — mesure réparée. M0008 E003 `01f3c8f` partiel : 429 = **limite passerelle 5 req/min/équipe** ; LLM-2 tronqué ; LLM-1 faux et sûr sur T1-A `e_sup_d`.
- **M0009 E005 `08d80f7` : Jev faux et sûr sur 6 questions** (accords pronominaux, « fait faire », « ci-jointe » à confirmer, contradiction masquée par distracteurs, chaîne de 4 pas) — 1 à 2 réponses chacune, à répliquer.
- Vague 3 : R003 (E002-bis), R004 (E005 + vérif grammaticale), M0010 (E003 rythmé), M0011 (E006 réplication + contamination E004), M0012 (doc v2.2 + GENESE).

## 2026-09-26T16:14:20+02:00 — Vague 1 rendue (M0003–M0006) ; vague 2 posée (R001, R002, M0007–M0009)

- M0003 ✅ T2 : 4/4 conforme, 0 « faux et sûr » (fautes fréquentes) — `exp/e001-sonde-jev` 7e953a9. M0004 ✅ 17 issues (#1–#17) + index `vault/notes/2026-09-26-issues-github.md`.
- M0005 ✅ E002 banc (22 tests) — plafond R ≤ 0 sur 12/20 sous bruit : mesure à réparer (E002-bis). M0006 ⛔ STOP 403 free tier LLM-2 — 2/70 appels.
- Incident : `state.json` écrasé par une fenêtre (compteurs perdus) — reconstruit depuis `events.jsonl` ; garde ajoutée aux rituels.
- Vague 2 : R001 (doublage+merge E001), R002 (doublage+merge E002), M0007 E002-bis, M0008 E003 relance, M0009 E005 Jev hors distribution.

## 2026-09-26T15:53:49+02:00 — M0003–M0006 (F01–F04) posés en parallèle : rejeu T2, issues GitHub, E002, E003

- Décision Malik 26/09 15:50 : rejeu T2 avant doublage ; enchaîner les pistes en parallèle ; issues GitHub pour ne rien oublier.
- F01/M0003 `exp/e001-sonde-jev` (T2 seul, réparti) · F02/M0004 `main` (labels + 17 issues + `vault/notes/2026-09-26-issues-github.md`) · F03/M0005 `exp/e002-relations-opaques` (banc « acquérir » + 3 étalons, sans réseau) · F04/M0006 `exp/e003-etalon-llm` (2 LLM via AI Gateway, ≤ 70 appels).
- Branches et fichiers disjoints ; F01 et F04 appellent la même passerelle (risque 429 partagé, assumé).

## 2026-09-26T10:46:10+02:00 — M0002 (F01) : première mesure Jev partielle — T1 6/6 conforme, T2 non servi (429/503)

- Rapport : `vault/echanges/F01.md` § Rapport M0002 ; branche `exp/e001-sonde-jev` tip `08672e4` (non doublée, non mergée) ; `main` = `7c453b1`.
- 21 appels : 7×200, 3×503 (digitalocean), 11×429 (passerelle) — vérifié par l'orchestrateur dans `raw.public.jsonl`.
- T1-A « contradiction » / T1-B « indéterminé » distingués, stables 3/3 ; `e_sup_d` affaibli en présence de contradiction (0.49–0.58 vs 0.73–0.78) [hypothèse].
- Bloquant scientifique : T2 (erreurs invisibles) entièrement non mesuré. Décision Malik attendue : rejeu T2 seul avant doublage R001.

## 2026-09-26T10:28:42+02:00 — M0002 (F01) posé : rejeu E001 après carte Vercel, en attente de rendu

- Mandat : `vault/echanges/F01.md` ; branche `exp/e001-sonde-jev` (tip `2719279`), même worktree ; `cases.json` figé (sha256 `8325775b…`).
- Publication : `raw.public.jsonl` sans en-têtes de réponse ; `raw.jsonl` gitignoré.
- Archive M0001 : `vault/echanges/archive/2026-09-25-F01-M0001-e001-sonde-jev.md`.

## 2026-09-25T21:46:59+02:00 — M0001 (F01) : BLOCKED propre, sonde Jev construite mais 403 facturation Vercel sur 21/21 appels

- Rapport : `vault/echanges/F01.md` § Rapport M0001 ; branche `exp/e001-sonde-jev` tip `2719279` (non doublée, non mergée).
- Livré : `.env` ignoré par `.gitignore`, `run.py` stdlib + garde anti-fuite testée hors ligne, `cases.json` sha256 `8325775b…` figé.
- Bloquant : `customer_verification_required` — carte à enregistrer sur Vercel (geste Malik), puis rejeu à l'identique (nouveau dossier results/).
- Réserve orchestrateur : l'accès réel n'a pas été testé à la pose (contradiction « Free » / « $0.042 » vue et non creusée).

## 2026-09-25T21:30:40+02:00 — M0001 (F01) posé : sonde Jev e001, en attente de rendu

- Mandat : `vault/echanges/F01.md` ; branche à créer `exp/e001-sonde-jev` depuis `origin/main` = `343e839`.
- Périmètre : ignorer `.env` (dépôt public), script Python stdlib `research/experiments/E001-jev-sonde/run.py`, 7 cas préregistrés, sortie brute conservée.
- Décision : GO de Malik 25/09 21:30 (« Lance !! »).

## 2026-10-01T14:15:50+02:00 — M0040 posé (F01) : harnais TEMPS 1, passe à blanc `--maj --dry-run`

- Mission 0 (carnet, index, passation, gabarits, décision, note, 22 archives) puis gardes G0–G5 ; garde « propre hors F0x.md et runtime/journal|log|entretien.lock » (décision Malik 01/10).
- F01/M0039 archivé : `vault/echanges/archive/2026-09-29-F01-M0039-readme-reconception-synthese.md`.

## 2026-10-01T14:20:37+02:00 — M0040 traité : STOP propre (rc=1)

- Mission 0 `8910d3a` + reprise `afc5d03` sur main. Passe à blanc : 5 POSE (.gitignore), 16 DEJA, 2 DIVERGE (SKILL.md, gabarits.md : identiques au canon v1.0.0, jamais adaptés), 0 OBSOLETE, 0 ECHEC ; GARDEE version v1.0.0 ; rien écrit.
- Faute orchestrateur : « rc ≠ 0 → STOP » incompatible avec un dry-run qui rencontre un DIVERGE (bootstrap sort rc 1 par conception).
- En attente de Malik : appliquer ? DIVERGE : projet ou canon (--force-skill) ?

## 2026-10-01T14:46:23+02:00 — M0041 posé (F01) : harnais TEMPS 2

- Décision Malik 14:36 : on applique, version du canon pour les 2 DIVERGE (--force-skill --dry-run, réel, puis --maj rc 0 → v1.1.0).
- Décision Malik : branche `chore/harnais-v1.1.0` depuis origin/main (pre-push refuse main hors vault/, #41) ; R016 + merge en mandats séparés.

## 2026-10-01T14:56:11+02:00 — M0041 traité : STOP propre étape 1

- `--force-skill --dry-run` rc 0 : 1 FORCE, 2 POSE skill, **5 POSE .gitignore** (mêmes lignes que M0040), 12 DEJA, 1 SAUTE, 1 IGNORE. Critère « POSE seulement sous le skill » non tenu → STOP. Rien écrit.
- Branche locale `chore/harnais-v1.1.0` = a3e9d07 (ancêtre de main), non poussée. Main 79c8559.
- En attente de Malik : admettre les 5 POSE .gitignore aux étapes 1–2 ?

## 2026-10-01T16:43:42+02:00 — M0042 posé (F01) : harnais TEMPS 2 bis

- Malik 16:42 « reprend » → 5 POSE .gitignore admises (à l'identique) aux étapes 1–2, SAUTE/IGNORE admis ; reste inchangé. Branche locale existante reprise (ff-only origin/main).
- Signalé à Malik : aucun mandat F02 dans EV-LLM (F02 = M0032 du 27/09, aucun événement F02 le 01/10).

