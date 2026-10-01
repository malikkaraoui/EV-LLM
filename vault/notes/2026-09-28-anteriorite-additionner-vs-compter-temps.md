---
date: 2026-09-28
auteur: orchestrateur (agent de recherche dédié, 16 sources ouvertes ; PMC captcha, ScienceDirect et arXiv 2512.04727 refusés par le proxy)
objet: antériorité pour la première expérience de la file — modules gelés « poser » (lecteur E014) et « retenir » (accumulateur E013) retournés vers le temps : détectent-ils qu'une arrivée manque ?
verdict: non trouvé pour la question exacte ; partiellement fait pour chaque brique
---

# Antériorité — « retourner l'addition vers le temps » (additionner vs compter)

Question : un accumulateur appris pour la retenue et un lecteur appris pour poser, gelés, sans horloge fournie, servent-ils à observer un flux d'événements réguliers et à détecter une omission ? Lequel porte l'observation ?

## 1. Transfert d'un circuit arithmétique gelé vers une tâche temporelle
Aucune source ne prend un module d'addition/comptage déjà entraîné et gelé pour le réutiliser sur un flux d'événements et détecter une omission. [VÉRIFIÉ par absence de résultat ; absence ≠ preuve d'inexistence]

## 2. Comptage / numérosité émergents et lien temps–nombre
- **Meck & Church 1983, mode-control model** (lu via Allman, Pelphrey & Meck 2011, https://www.frontiersin.org/journals/integrative-neuroscience/articles/10.3389/fnint.2011.00047/full) : les impulsions sont une « monnaie commune pour le temps et le nombre » tant que le processus d'accumulation peut fonctionner en mode « event » (compter) ou « run » (chronométrer). **Un seul accumulateur, deux modes.** C'est la thèse de fond du projet, formulée en 1983 pour le rat, jamais testée sur un accumulateur artificiel aux poids connus. Propriété scalaire (Gibbon 1977). [VÉRIFIÉ via source secondaire]
- Nasr, Viswanathan & Nieder 2019, Sci. Adv. (https://niederlab.org/Nasr,%20Viswanathan,%20Nieder%20(2019)%20SciAdv.pdf) : 9,6 % d'unités sélectives au nombre dans un HCNN entraîné sur ImageNet ; les auteurs écrivent que l'énumération séquentielle (dans le temps) relève de mécanismes différents. [VÉRIFIÉ]
- Kim, Jang, Baek, Song & Paik 2021, Sci. Adv. (https://www.biorxiv.org/content/10.1101/857482v1) : des « neurones de nombre » apparaissent dans des réseaux **non entraînés**. Témoins : poids permutés, redistribués, réponses mélangées. → **témoin aléatoire gelé indispensable**. [VÉRIFIÉ]
- Tsao et al. 2018, Nature (https://www.nature.com/articles/s41586-018-0459-6) : le cortex entorhinal latéral représente le temps « par l'encodage de l'expérience », sans horloge. [VÉRIFIÉ, abstract]
- Bi & Zhou 2020, PNAS (https://arxiv.org/abs/1910.05546) : des RNN chronomètrent par évolution monotone de l'état le long d'une trajectoire ; « l'anticipation d'événements à venir » produit un signal temporel même dans des tâches non temporelles. [VÉRIFIÉ, abstract]

## 3. Détection d'omission / attente
- Revue Frontiers Neural Circuits 2022 (https://www.frontiersin.org/articles/10.3389/fncir.2022.799581/full) : « les protocoles à intervalle irrégulier ne produisent pas nécessairement de réponse d'omission » → le flux irrégulier est LE témoin. Modèles : masse neurale, microcircuits, codage prédictif ; aucun RNN artificiel entraîné. [VÉRIFIÉ]
- Sci. Rep. 2016 (https://www.nature.com/articles/srep20615) : deux mécanismes chez l'humain — sous ~250 ms, « groupement temporel » (extinction d'un flux) ; au-dessus, **prédiction** du stimulus à venir. → l'intervalle du monde doit être « long » (en pas de temps) pour que la détection soit une prédiction et non l'extinction d'un intégrateur. [VÉRIFIÉ]
- arXiv 2511.21605 (https://arxiv.org/html/2511.21605) : signal d'erreur de prédiction **dédié à l'absence** dans le thalamus auditif ; ISI constant, omission en position 4–6, ITI variable. [VÉRIFIÉ]
- Hollerman & Schultz 1998 (https://www.hms.harvard.edu/bss/neuro/bornlab/nb204/papers/Hollerman_Schultz_NatNeuro_1998.pdf) : omission de récompense → dépression 99 ± 29 ms après l'instant attendu ; récompense retardée → dépression à l'instant habituel + activation au nouvel instant. Avec récompense ; notre cas est sans. [VÉRIFIÉ]

## 4. Additionner vs compter en apprentissage machine
- Weiss, Goldberg & Yahav 2018, ACL (https://arxiv.org/pdf/1805.04908) : LSTM/ReLU-RNN comptent (a^n b^n, entraîné n ≤ 100, généralise jusqu'à 256), « counting dimensions » à croissance régulière, dérive par portes non saturées. Tokens explicites, pas d'intervalle vide. [VÉRIFIÉ]
- Gers, Schraudolph & Schmidhuber 2002, JMLR (https://www.jmlr.org/papers/volume3/gers02a/gers02a.pdf) : mesurer/produire des délais **sans horloge externe** ; deux stratégies : intégration linéaire de l'état (= accumulateur) ou oscillateurs ; généralise 15 → 45. Réentraîné par tâche. [VÉRIFIÉ]
- Trask et al. 2018, NALU (https://proceedings.neurips.cc/paper_files/paper/2018/file/0e64a7b00c83e3d22ce6b3acf2c582b6-Paper.pdf) : MNIST Counting vs Addition : à longueur 10, LSTM 98 % en comptage, 0 % en addition extrapolée. **Compter et additionner sont deux généralisations distinctes pour un même réseau.** [VÉRIFIÉ]
- Fang, Zhou, Chen & McClelland 2018 (https://stanford.edu/~jlmcc/papers/FangZhouChenMcC18Count.pdf) : pointer + compter ; apprendre le pointage d'abord accélère le comptage ; erreurs ±1. Analogie directe poser/retenir, mais spatiale. [VÉRIFIÉ]
- Zorzi et al. 2025, énumération séquentielle dans les LLM (arXiv 2512.04727) : non ouvert. [HYPOTHÈSE]

## Verdict
**Non trouvé** pour la question exacte. **Partiellement fait** pour chaque brique : accumulateur commun temps/nombre (Meck & Church), RNN qui compte et chronomètre par intégration (Gers, Weiss), signaux d'omission et leurs conditions (revue 2022, Hollerman), distinction compter/additionner (NALU). Personne n'a pris un additionneur gelé et vérifié s'il « attend ».

## Ce qui serait nouveau
- Test du mode-control sur un artefact : un accumulateur appris en mode « event » (retenue) fonctionne-t-il en mode « run » (temps) sans réentraînement ?
- Un signal d'omission **sans récompense et sans horloge** produit par ~1 100 paramètres gelés.
- Localiser la faculté : poser (segmentation) vs retenir (accumulation) vs corps composé — Fang 2018 le fait dans l'espace, personne dans le temps.
- Une réponse négative est publiable : un module exact à 1 000 chiffres qui ne sait pas attendre un événement.

## Le contre-pied
Transfert **dans les deux sens** avec le même adaptateur : (i) accumulateur gelé → détection d'omission ; (ii) un intégrateur temporel appris sur flux (type Gers / Bi & Zhou, jamais vu de chiffres), gelé → retenue d'addition. (i) oui et (ii) non : la retenue contient le temps, pas l'inverse. Les deux oui : Meck & Church confirmé sur artefact. Aucun : la thèse « addition = expérience du temps » est falsifiée pour ces modules. Variante qui tranche poser vs retenir : accumulateur seul avec flux déjà découpé en cases (ticks fournis) vs flux brut ; si l'omission n'est détectée qu'avec les cases, la faculté d'attente est dans le lecteur.

## Témoins indispensables (tirés de la littérature)
- Flux irrégulier à même densité moyenne : l'omission ne doit plus être détectée.
- Modules aléatoires gelés de même architecture + poids permutés (Kim 2021), même adaptateur : l'adaptateur ne doit pas être le vrai détecteur.
- Ablation croisée : lecteur seul, accumulateur seul, les deux, adaptateur seul.
- Intervalle long vs court : prédiction vs extinction d'intégrateur.
- Événement retardé vs omis (Hollerman) : le signal doit apparaître à l'instant attendu, pas à l'arrivée tardive.
- Extrapolation : intervalles et nombres d'événements hors de la plage vue par l'adaptateur.
- Dérive (Weiss) : combien d'intervalles vides l'accumulateur tient avant de perdre le compte.
