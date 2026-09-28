---
titre: EV-LLM — Genèse (suite) 26–27/09/2026
description: Suite du journal claude/GENESE.md — bascule Jev → addition, veille, vague E008–E013. On ajoute, on ne réécrit pas.
---

# EV-LLM — Genèse, suite (26–27/09)

---

## 2026-09-26 — Journée Jev (résumé ; détail dans `vault/reprise/00_INDEX.md` du dépôt)

- Le harnais d'orchestration est posé. Six vagues de mandats sont lancées en parallèle, avec une revue indépendante avant chaque merge.
- **Jev se trompe en étant sûr de lui** sur 5 questions incontestées (accords pronominaux, « a faites faire », « ci-jointe », contradiction masquée par un distracteur…), reproduites 5 fois sur 5 (E006). Une 6ᵉ réponse est reclassée « contestée » (question ambiguë, R008). Jev lit les règles écrites **partiellement** (E007).
- Candidats ACQUÉRIR (A0, A0-bis) : échec. Puis M0020 montre que **même un oracle échoue au critère**. Le test ne mesurait donc pas l'apprentissage.
- Oubli assumé par Claude : le fournisseur des modèles témoins (Vertex, etc.) n'était ni imposé ni journalisé dans E003. Un budget passerelle de 5 $ est posé sur la clé unique.

## 2026-09-26 18:17 — Bascule : on arrête Jev, on devient radical

> Malik : « je pense qu'il faut arrêter les tests ensuite avec jev… on doit être plus radical… un model super léger avec open weight… le modeler et l'entraîner… mais avant tout il faut savoir ce qu'on cherche. »

- Tour de Hugging Face : SmolLM2, Qwen3.5-0.8B, Pythia, RWKV7. Entraînement possible sur M1 16 Go avec MLX.
- La cible est redéfinie :

> Malik : « J'ai pas eu besoin d'apprendre toutes les additions pour savoir que 100 + 20,5 = 120,5… j'ai pas eu besoin d'apprendre à conduire un camion, j'ai appris à conduire une voiture… je peaufine ma conduite, mes réflexes en continu. »

- Trois capacités mesurables : **apprendre une procédure** (généralisation systématique), **transférer**, **apprendre en continu**.
- Claude objecte que les « quelques heures » de conduite reposent sur 18 ans d'acquis. La cible devient donc : **avec une base, apprendre la couche suivante en peu d'exemples, sans casser la base**.
- Premier test choisi par Malik : **l'addition**, entraînée sur des nombres courts et testée sur des nombres longs. « j'adore ce test… lance l'expérience. »

## 2026-09-26 21:00 → 27/09 00:00 — E008, palier 0 (sur le Mac de Malik)

- Le test est **valide** : un oracle obtient 100 %, un système « par cœur » 0 %.
- Transformer standard : ~99 % sur 1 à 5 chiffres, **0 % dès 6 chiffres**. Il répond « 6 » à 601 320 + 549 467, avec une confiance de 1,00.
- Variante sortie inversée + NoPE : 91 % à 6 chiffres, 8 % à 7, **0 % dès 8**.
- Un « faux et sûr » massif réapparaît, cette fois sur un modèle qu'on contrôle.

> Malik (27/09 08:32) : « Ce qui est fou c'est que ce que je t'ai dit hier sur le fait que j'ai appris quelques additions m'a permis de faire des additions bien plus complexes. Et ben un LLM n'y arrive pas. Si on y arrive, on tient un truc. »

## 2026-09-27 matin — Veille scientifique (6 recherches)

- **Enfant** : les faits (tables) sont mémorisés, la procédure (colonnes + retenue) est calculée. La feuille sert de mémoire externe. Les « bugs » de procédure (Brown & VanLehn) prouvent une représentation procédurale. **La règle est enseignée explicitement** ; la prémisse « quelques exemples » est à nuancer.
- **IA** : les seuls succès combinent (1) un calcul itéré dont la longueur dépend de l'entrée, (2) une opération locale sans position absolue, (3) un entraînement anti-raccourci. Exemples : Neural GPU, Deep Thinking, Looped Transformer. Aucun résultat ne montre une généralisation arbitraire apprise « à partir de rien ».
- **Déjà existant** : règle → réflexe (compilation ACT-R, chunking Soar) ; déclencheur (critère de confiance de Siegler, sur l'addition de l'enfant). **Ce qui reste ouvert : induire la règle à partir des seules paires, puis la compiler.**
- Revue hostile : le protocole est durci (validation 6–8 chiffres, test 10–100 touché une seule fois, 5 graines, tests adverses, budget de structure explicite).
- Décision de Malik : « On fait A et B… explorer un maximum… je suis sûr qu'on loupe un truc. »

## 2026-09-27 12:47 — « Pourquoi pas s'inspirer de la nature ? »

- Malik interroge : pourquoi ça paierait, pourquoi seulement trois expériences, pourquoi pas la nature.
- Pistes retenues : **l'évolution** (trouver la forme du circuit), **l'insecte** (intégration de trajet : un accumulateur minuscule), **le bébé** (a priori innés), **le sommeil** (consolidation par rejeu, pour plus tard).
- Feu vert à 13:07 : « enchaîne… tous les plans ».

## 2026-09-27 — Premiers résultats de la vague E009–E013

- **E011 (objectif)** : en partant de la règle exacte (addition binaire), **l'entropie croisée seule la garde (5/5)**. Ce sont les pénalités fortes (L2 λ=1 : 0/5) qui la cassent. MDL discret : 5/5.
  - Deux affirmations de la veille relayées par Claude étaient **fausses** : « 1 neurone, 7 connexions » concernait une autre tâche, et la « dérive » sous entropie croisée n'avait pas été testée sur l'addition. L'expérience les a corrigées.
- **E010 (enseigner)** : un brouillon colonne par colonne donne 99,9 % sur les nombres vus avec 10 000 exemples, **au moins 25× moins** qu'un modèle sans brouillon, qui n'y arrive pas avec 256 000.
  - Énoncer la règle seule ne sert à rien.
  - **Toujours 0 % dès 7 chiffres.** La cause est le **repérage** (quel chiffre lire, quand s'arrêter), pas le calcul.
  - Une confiance mesurée sur la recopie finale est aveugle : 606 erreurs sur 669 sont « sûres ». **L'autodiagnostic doit porter sur les étapes qui calculent.**
- **E009 (architecture)** : **non mesuré**. Les modèles n'ont même pas appris la distribution, faute de budget suffisant et parce que le GPU était partagé par 4 fenêtres (responsabilité de Claude, qui a lancé trop de calcul en parallèle). Correctif lancé : E009-bis.
- En cours : E012 (évolution + MDL), E013 (accumulateur « insecte »), E009-bis. Prochaine suite prévue : E014 « repérage ».

## Leçons de méthode (26–27/09)

1. Tout test doit d'abord prouver qu'il est **réussissable** (un oracle le passe) et **non trichable** (le par-cœur échoue).
2. Un pilote doit vérifier que le modèle **apprend la distribution**, pas seulement la vitesse de calcul.
3. Recouper la veille par l'expérience : deux affirmations « vérifiées » étaient fausses.
4. Incident outil : la copie de fichiers vers le Mac réutilisait un cache lié au nom du fichier source. Désormais : nom neuf, empreinte md5, puis bascule du statut.
