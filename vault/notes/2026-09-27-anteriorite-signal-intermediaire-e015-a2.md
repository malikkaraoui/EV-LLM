---
date: 2026-09-27
auteur: orchestrateur (agent de recherche dédié, 12 recherches web, 14 sources ouvertes)
objet: antériorité pour E015-A2 — un signal intermédiaire AUTO-GÉNÉRÉ (sans récompense partielle humaine) pour guider une recherche de programmes compositionnels sur modules gelés
verdict: partiellement fait
---

# Antériorité — signal intermédiaire auto-généré pour la composition de modules gelés (E015-A2)

Contexte : E015 (branche `exp/e015-ecosysteme`, tip `58abf67`) montre que la recherche évolutive de câblages entre champions gelés, jugée par le seul succès final, converge vers le programme trivial « sortie = a » ; le juge n'est pas en cause (la solution connue vaut 1,100, les rendus 0,004–0,45). L'auteur propose « un signal intermédiaire que la machine se fabrique elle-même ». Question posée à la recherche : cela a-t-il déjà été fait ?

Ce qui n'a pas pu être ouvert (OpenReview bloqué, deux arXiv refusés) est marqué [HYPOTHÈSE].

## Sources lues

1. **Lehman & Stanley — Novelty search (GP)** [VÉRIFIÉ]. « Efficiently Evolving Programs Through the Search for Novelty », GECCO 2010 — https://stars.library.ucf.edu/scopus2010/1037/ ; « Novelty Search and the Problem with Objectives », GPTP 2011 — https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/lehmanNoveltySearch11.pdf. Remplace la fitness par la distance de comportement. Labyrinthe dur : 39/40 vs 3/40 pour la recherche objective. Thèse : « les stepping stones qui mènent à l'objectif ne ressemblent pas à l'objectif » — notre diagnostic. Mais : pas de modules gelés, pas de tâche algorithmique, pas de généralisation en longueur ; la caractérisation du comportement reste choisie par l'humain.
2. **Dolson, Lalejini, Ofria — « Exploring GP Systems with MAP-Elites », GPTP 2018** [VÉRIFIÉ] — https://peerj.com/preprints/27154.pdf. MAP-Elites sur programmes linéaires (somme de 5 entiers, min de 4…) : plus de diversité, mais utilisé comme outil d'analyse, pas comme moteur. Pas de modules gelés.
3. **Brant & Stanley — Minimal Criterion Coevolution, GECCO 2017** [VÉRIFIÉ, abstract] — https://stars.library.ucf.edu/scopus2015/7496/. Aucune fitness : un individu survit s'il satisfait un critère minimal ; problème et solution co-évoluent. Domaine labyrinthe. Transposable : co-évoluer les instances d'addition (longueur, densité de retenues) avec les programmes.
4. **Schmidhuber — Compression progress (2008), PowerPlay (2011)** [VÉRIFIÉ] — https://arxiv.org/pdf/0812.4360 ; https://arxiv.org/pdf/1112.5309. Récompense intrinsèque = bits économisés ; PowerPlay cherche « le problème le plus simple encore non résolu », variante §3.3.3 où le solveur ne peut qu'ajouter des composants (= gel). Le plus proche conceptuellement ; mais pas de composition discrète de modules neuronaux appris, pas d'évaluation en longueur.
5. **Forestier, Mollard, Oudeyer — IMGEP (2017)** [VÉRIFIÉ abstract] — https://arxiv.org/abs/1708.02190 ; **Colas et al. — CURIOUS (ICML 2019)** [HYPOTHÈSE, non ouvert] — https://proceedings.mlr.press/v97/colas19a/colas19a.pdf. Progrès d'apprentissage pour choisir des buts ; politiques par gradient, pas des programmes discrets.
6. **Gaven, Carta, Romac, Colas et al. — MAGELLAN (2025)** [VÉRIFIÉ abstract] — https://arxiv.org/abs/2502.07709. LLM autotélique qui prédit sa propre compétence ; aucune synthèse de programme.
7. **Chen, Liu, Song — Execution-Guided Neural Program Synthesis, ICLR 2019** [VÉRIFIÉ] — https://openreview.net/pdf?id=H1gfOiAqYm. États intermédiaires obtenus « en exécutant les programmes vérité-terrain » : dérivé de solutions humaines, pas auto-généré.
8. **Ellis et al. — DreamCoder (2021)** [VÉRIFIÉ abstract] — https://arxiv.org/abs/2006.08381. Wake-sleep, bibliothèque par compression, problèmes imaginés. Pas de signal intermédiaire supplémentaire ; abstractions symboliques. Le « rêve » (auto-génération de problèmes) est la partie réutilisable.
9. **Valkov et al. — HOUDINI, NeurIPS 2018** [VÉRIFIÉ abstract] — https://arxiv.org/abs/1804.00218v2. Programmes fonctionnels typés composant des fonctions neuronales apprises et réutilisées (compter, sommer, plus court chemin). Cas « modules gelés + câblage discret » le plus proche ; recherche = énumération typée + gradient sur la perte finale ; aucun signal intermédiaire auto-généré.
10. **Chang, Gupta, Levine, Griffiths — Compositional Recursive Learner (2018)** [VÉRIFIÉ] — https://arxiv.org/html/1807.04640v2. Contrôleur PPO qui enchaîne des modules, récompense finale 1/0 ; arithmétique, entraîné à longueur 5, ~60 % à 100. Aveu : « découvrir la décomposition sans curriculum » reste un défi majeur. Modules non gelés.

Appui (axe « pas de prise à la sélection ») [VÉRIFIÉ] : Hu et al., End-to-End Module Networks (https://arxiv.org/pdf/1704.05526v2) : layout appris de zéro par récompense finale 69,0 % vs 83,7 % avec clonage de layouts experts. Andreas, Klein, Levine, Policy Sketches (https://arxiv.org/pdf/1611.01796) : sous-politiques via esquisses symboliques humaines. Cai, Shin, Song (https://arxiv.org/abs/1704.06611v1) : addition scolaire récursive [HYPOTHÈSE : traces humaines]. Hors GP : « process reward models » non supervisés par cohérence interne (uPRM, https://arxiv.org/html/2605.10158v1).

Non trouvé : un papier montrant explicitement qu'un module gelé réutilisé n'est pas mieux noté que le trivial sur la nouvelle tâche.

## Verdict

**Partiellement fait.** Chaque brique existe séparément : nouveauté sans objectif (Lehman), co-évolution sans fitness (MCC), progrès d'apprentissage comme signal (Oudeyer, MAGELLAN), MDL + auto-génération de problèmes (DreamCoder, PowerPlay), composition typée de modules neuronaux réutilisés (HOUDINI, CRL). Personne n'a assemblé « modules neuronaux gelés + câblage discret évolutif + signal intermédiaire fabriqué par le système + généralisation en longueur mesurée sur tâche algorithmique ».

## Ce qui serait nouveau
- Un signal de cohérence inter-champions (lecteur et accumulateur doivent « s'accorder » sur les flux échangés) comme critère de survie, sans caractérisation humaine du comportement.
- Le test quantitatif de « pas de prise à la sélection » : score du meilleur programme utilisant un champion contre le trivial, sur N croissants.
- PowerPlay §3.3.3 (ajout seulement, gel) instancié avec des champions neuronaux et jugé en longueur.
- Le rêve DreamCoder appliqué au câblage : générer soi-même des instances qui discriminent les programmes candidats.

## Le contre-pied
Pas de signal intermédiaire du tout, mais **co-évolution des instances** (MCC) : une instance ne survit que si elle sépare deux programmes vivants. Si cela suffit à passer la marche ECH1 (0/5 → > 0/5), la « curiosité sur les sorties » est superflue et c'est le jeu d'instances qui manquait de gradient ; si cela échoue aussi, la prise doit venir de l'intérieur des champions, et le test devient : lequel des trois signaux (cohérence, prédiction, curiosité) fait passer ECH1, une variable à la fois.

Non lancé (28/09) : semaine sans calcul, décision Malik.
