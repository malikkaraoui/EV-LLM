# Veille 27/09 — apprendre une procédure (addition) et généraliser en longueur

Synthèse orchestrateur de 6 recherches. Les chiffres sont vérifiés sur les sources par les agents de veille ; le détail des étiquettes est dans le fil de conversation.

## Ce qui marche sans alignement fourni
- Neural GPU (1511.08228) : 20 → 2000 bits, 0 erreur. Fragile : « quelques runs sur 729 », et échec sur entrées symétriques (1611.00736).
- Deep Thinking + recall (2202.05826) : 32 → 512 bits, 97 %. Réussit 2 fois sur 30 sans contrainte de Lipschitz, 28 fois sur 30 avec (2410.23451).
- Looped Transformer NoPE (2409.15647) : ≈ 100 %, mais le nombre d'itérations T(n) est fourni à l'entraînement.
- Ingrédients communs : un calcul itéré dont la durée dépend de l'entrée, une opération locale sans position absolue, un entraînement anti-raccourci.

## Piste manquée
L'**objectif MDL** (longueur de description minimale) :
- Lan, Geyer, Chemla, Katzir (TACL 2022) : addition binaire apprise à partir de 100 exemples, avec 1 unité et 7 connexions. 100 % de réussite, correction prouvée.
- Lan et al. 2024 et 2505.13398 : avec l'entropie croisée et L1/L2, l'entraînement s'éloigne de la solution parfaite même en partant d'elle.

## Humain
- Faits mémorisés (hippocampe, Qin 2014) séparés de la procédure (colonnes et retenue).
- La valeur de position prédit la réussite (Moeller 2011).
- La feuille sert de mémoire externe.
- Les « bugs » de procédure (Brown & VanLehn 1980) montrent une représentation procédurale.
- L'enseignement de la règle est explicite ; aucune donnée chiffrée sur le nombre d'exemples.

## Déjà existant (ne pas réinventer)
- RÈGLE → RÉFLEXE = production compilation d'ACT-R (Taatgen & Anderson 2002) et chunking de Soar.
- DÉCLENCHEUR / AUTODIAGNOSTIC = critère de confiance de Siegler (1988, addition de l'enfant), SCADS, « feeling of knowing » de Reder.
- NPI (1511.06279) : 100 % jusqu'à 3000 chiffres, mais avec les traces d'exécution fournies.
- Ce qui reste ouvert : **induire** la règle à partir des seules paires, puis la compiler.
- Limites connues : les « expensive chunks » de Soar, d'où un coût de compilation et un oubli actif pour SOMMEIL.

## Revue hostile → protocole durci
- Validation OOD séparée (6–8 chiffres), test final intouché (10–100 chiffres).
- Au moins 5 graines, tests adverses.
- Distinguer exemples uniques et pas d'entraînement ; budget de structure explicite.
- Tâche de contrôle suggérée : la multiplication, ou les tâches de la hiérarchie de Chomsky (2207.02098).

## Conséquence
La vague E009 (architecture), E010 (enseignement) et E011 (objectif MDL) est posée le 27/09.
