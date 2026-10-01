# Passation orchestrateur — 27/09/2026 21:10 (session saturée → nouvelle session cowork)

## Où on en est (fenêtres)
- F01 **M0030 E015 « écosystème »** — en cours (lancé ~20:40), branche `exp/e015-ecosysteme`, préenregistrement `f8cd480`.
- F04 **M0031 E016 « mouches »** — en cours (lancé ~20:40), branche `exp/e016-mouches`, préenregistrement `0bf43e1`.
- F02 **M0032 E016-A2** — `en-pose` (récompense = seule variable : FIXE / IND / TOR / COLL / REJEU-SEUL ; nouveaux venus officiels). À passer `pret-a-lancer` QUAND M0031 a rendu (archiver F04 d'abord).
- F05 **M0033 E015-A2** — `en-pose` (archive d'interfaces, réutilisation à interface GELÉE, ablations). À passer `pret-a-lancer` QUAND M0030 a rendu (archiver F01 d'abord).
- F03 **R011** — rendu **RÉSERVE** (correctif M0029 exact, résidu README E013 l. 195) → pas de merge ; poser un micro-correctif puis re-doublage/merge E008+E013 (tip actuel `a749c29`).
- state.json : `next_mandat_id` M0034, `next_revue_id` R012.
- Le réveil 21:45 de l'ancienne session est SUPPRIMÉ : la nouvelle session reprend ces tâches.

## Résultats acquis (branches)
- E008 `af281f5` : transformer standard 0 % dès 6 chiffres ; sortie inversée+NoPE 91/7,9/0,1 % à 6/7/8.
- E009 / E009-bis : négatifs. E010 `19f7f0d` : scratchpad ×25 en efficacité d'exemples, mais 0 % dès 7 (localité).
- E011 `994c77b` : CE seule garde la règle exacte 5/5 ; L2/L1 λ=1 la cassent ; MDL discret 5/5.
- E012 `0a33881` : évolution, décimal aligné 2/5 (100 ex.) 4/5 (1000 ex.), circuit prouvé ; binaire et plat 0/5.
- E013 `a749c29` : I1 H=2/4/8 exact jusqu'à 1 000 chiffres 5/5 (adverses + propagation) ; H=1 échoue sur zéros ; entrée plate 0/5.
- E014 `fc698b4` : lecteur seul + accumulateur E013, gelés, 0 pas conjoint → exact 16/100 chiffres 4/5, 1/5 à 1 000 ; bout en bout 0/5 ; abstention attrape 77 % des erreurs pour 1,4 % des justes.
- Constat convergent : **calculer est facile avec presque rien (2 neurones) ; le goulot est le repérage / l'alignement (« poser l'opération »)**. La composition de compétences apprises séparément marche quand l'interface est symbolique discrète (connu).

## Règles actives (toutes obligatoires)
- **Antériorité PROFONDE avant chaque lancement** (Malik 20:46) : agents de recherche dédiés, sources lues, verdict (fait / partiel / non trouvé) + part nouvelle écrits dans le mandat. **Interdit de refaire du connu pour arriver au même résultat : prendre le contre-pied** (Malik 20:35).
- Protocole durci : train 1–5 ; VAL-OOD 6–8 seule sélection ; TEST 10/16/32/64/100/1000 une seule fois ; adverses cascade/zéros/asym/propagation 10^L ; ≥ 5 graines ; C-ORACLE 100 % / C-PARCŒUR 0 % ; budget de structure ; pilote qui vérifie l'apprentissage ; préenregistrement poussé seul.
- Pas deux entraînements GPU lourds en parallèle sans raison (leçon E009).
- Écriture de mandat : nouveau nom de fichier source, vérif md5 sur l'appareil, PUIS flip de statut — **séquentiel, jamais en parallèle** (incident M0018).
- Orchestrateur : aucune écriture git, aucun `sleep`. Jamais lire `.env`. Rien de secret dans vault/ (dépôt PUBLIC). Pas de `--maj` sans accord. Passerelle Vercel : fournisseur imposé, 402 = arrêt net ; plafond 5 $ sur la seule clé.
- Vérifier soi-même les conclusions des mandats (réimplémentation numpy indépendante si besoin) ; croiser la recherche avec l'expérience (erreur E011).
- Communication avec Malik : français simple, **pas de tableaux** (smartphone), zéro complaisance, étiquettes [VÉRIFIÉ]/[MÉMOIRE]/[HYPOTHÈSE].

## Gabarits de mandat
`vault/reprise/gabarits/` : `_commun.md` (règles communes, dont antériorité + 402), `_rituels.md`, `_e9commun.md` (protocole durci), `R.tmpl` (revue). Mandats en cours = meilleurs exemples (`vault/echanges/F0x.md`).

## File d'attente
1. Lancer E015-A2 / E016-A2 à la fin de M0030 / M0031 ; lire, vérifier, expliquer simplement à Malik.
2. Micro-correctif README E013 → R012 → merge E008+E013.
3. Revue E014, puis E012-bis, transfert soustraction/multiplication, apprentissage continu (« sommeil »).
4. Décision en attente de Malik : mention de son fils dans GENESE (dépôt public).

## Notes de référence
`vault/notes/2026-09-27-veille-procedure.md`, `2026-09-27-genese-suite.md`, `2026-09-27-debrief-e008.md` ; carnet `CARNET_DE_BORD.md` (entrée 20:53) ; archives `vault/echanges/archive/`.
