# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-10-01T14:15:50+02:00 (orchestrateur) — mise à jour du harnais v1.0.0 → v1.1.0 en deux temps

## Où on en est

- **Cap** (Malik 26/09) : un modèle local qui **apprend une procédure** (addition : entraîné court, testé long), puis transfert, puis apprentissage continu. Journal : `vault/notes/2026-09-27-genese-suite.md` ; veille : `vault/notes/2026-09-27-veille-procedure.md`.
- E008 : test valide ; transformer 0 % dès 6 chiffres ; référence (inversé + NoPE) 91 % à 6, 0 dès 8.
- E011 : l'entropie croisée seule **garde** la règle exacte (5/5) ; L2/L1 forts la cassent ; MDL discret 5/5.
- E010 : le brouillon de colonnes fait gagner ≥ 25× en exemples (10 k) mais 0 % dès 7 chiffres — échec = **repérage** ; confiance sur la recopie finale aveugle.
- E009 : non mesuré (rien appris en distribution, budget + GPU partagé) → **E009-bis** en vol (F01, GPU prioritaire).
- **E013 : premier succès** — accumulateur 2 unités, exact jusqu'à 1 000 chiffres, 5/5, dès 1 000 exemples, **avec alignement donné** (recontrôlé en numpy). Entrée plate : 0/5.
- **E012** : l'évolution + MDL retrouve le circuit de la retenue en décimal (4/5, prouvé) — aligné seulement ; plat 0/5.
- **E014 : composition sans réentraînement** — lecteur appris seul + accumulateur gelés = addition exacte 16/100 chiffres, 4/5 (interface discrète = clé). Bout en bout 0/5.
- R010 : E013 confirmé (numpy 15/15) mais RÉSERVE sur I3 → M0029 (F03). E009-bis : architecture seule bloquée.
- **Cap Malik (27/09 20:35)** : ne jamais refaire du connu pour arriver au même résultat ; prendre le contre-pied ; veille d'abord, différence écrite.
- **E015 (M0030) : négatif** — assemblage autonome 0/5 ; câblage donné 2/5 exact à 1 000 ; la recherche échoue (juge OK), la réutilisation n'a pas de prise. **E016 (M0031) : négatif** — aucune langue commune, 1–2 idiolectes ; la règle tout-ou-rien coupe le signal. Les deux contre-vérifiés par l'orchestrateur.
- **Cap semaine (Malik 28/09 07:55)** : le week-end sert à explorer, la semaine le CPU est à d'autres projets → **aucun calcul en semaine**, documentation seulement. Publier les échecs comme succès d'exploration ; afficher la méthode (antériorité, contre-pied, itération rapide, quelques neurones, petit CPU).
- **En vol (01/10)** : **M0040** (F01) = harnais TEMPS 1, `bootstrap --maj --dry-run` à blanc + Mission 0 ; TEMPS 2 (`--maj`) seulement après le oui de Malik. Constat 01/10 : README déjà sur `main` (merge 4ea9bd0, R015 GO) ; M0039 (tip ab352a5) rendu, non traité ; state.json périmé (next_revue_id R015 déjà pris, projet.main a1231e5 ≠ c117209).
- (Historique) **M0039** = reconception bottom-up des puces de synthèse du README (après R013 + R014 RÉSERVE, même classe de défaut) ; puis R015 (relecture + fusion). README pas encore sur `main`.
- 28/09 07:42 : R012 RÉSERVE (défaut de formulation venu de l'orchestrateur, M0034) ; M0032 STOP propre (signal dense scalaire réfuté) ; F05 M0033 retenu (prémisse réfutée par M0030).
- **Décisions attendues de Malik** : (1) E013 : mandat de reconception de la synthèse puis R013 → merge E008+E013 ; (2) E016 : troisième pilote « crédit par colonne » (proposition auteur M0032) ou arrêt de la piste ; (3) E015-A2 : version contre-pied (antériorité faite : co-évolution d'instances MCC sans signal intermédiaire, puis cohérence inter-champions) ou autre cap.
- **Incident** : réveil 23:35 → reprise 07:40 (8 h) : une approbation attendait dans l'app côté Malik. Règle : lancer avant le départ de Malik tout ce qui doit tourner la nuit ; le réveil ne sert qu'à traiter les rendus.
- Réveil vivant : « Réveil ev-llm 2026-09-28 09:00 ».
- Décision attendue de Malik : mention de son enfant dans GENESE (dépôt public).

## Références à ne pas toucher

- `vault/echanges/archive/2026-09-2{5,6}-F01-M000{1,2}-*.md` — références du doublage R001.

## Rappels

- Dépôt **PUBLIC** : rien de secret dans `vault/`, rapports, résultats.
- Passerelle : 5 req/min/équipe (1 fenêtre API à 15 s ou 2 à 26 s) ; tout appel à un modèle témoin impose et journalise son fournisseur ; 402 = arrêt net.
- Défauts harnais signalés : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` absent ; pas de `type` d'événement défini pour `src: fenetre`.
- Source de vérité : `00_INDEX.md` + `vault/runtime/` — et au-dessus, la preuve git rejouée.

## 2026-09-27 20:53 — Règle : antériorité profonde avant chaque lancement
- Malik (20:46) : « Pour chaque expérience tu recherches avant de lancer si cela a déjà été fait et tu cherches profondément. » → règle permanente de l'orchestrateur, ajoutée au gabarit commun des mandats.
- Appliquée à E015/E016 (déjà lancés) : verdict **partiellement fait** pour les deux.
  - E016 : Mahaut 2023, Michel 2023, Tieleman 2019 montrent déjà qu'une population d'agents gelés hétérogènes converge et accueille un nouveau venu ; le brassage des partenaires suffit. Nouveau : pipeline A→B à codes privés, contenu algorithmique jusqu'à 1 000 chiffres, tout-ou-rien avec rejeu. → **M0032 E016-A2** (F02, en-pose) : récompense seule variable (FIXE / IND / TOR / COLL / REJEU-SEUL), nouveaux venus officiels.
  - E015 : PathNet, Braylan 2016, stitching (Guijt 2024), Cully 2015 couvrent chaque brique. Nouveau : interface archivée et jugée sur sa réutilisation GELÉE. → **M0033 E015-A2** (F05, en-pose) : archive d'interfaces, GELÉ / ARCHIVE / ALÉA-GELÉ / FIXE-PATHNET / JETABLE.
- A2 lancés après la fin de M0030/M0031 (GPU non partagé, leçon E009).
- R011 : RÉSERVE (correctif M0029 exact, résidu README l. 195) → pas de merge ; micro-correctif à poser.
