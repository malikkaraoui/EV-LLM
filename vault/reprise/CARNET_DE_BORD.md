# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-09-26T21:03:45+02:00 (orchestrateur) — cap E008 addition

## Où on en est

- **Cap (Malik, 26/09 soir)** : fin des tests Jev. Cible = un modèle local qui **apprend une procédure** (addition : entraîné court, testé long), puis transfert, puis apprentissage continu. M1 16 Go, MLX.
- Acquis Jev (clos) : 5 « faux et sûr » non contestés répliqués + 1 contesté (E006) ; Jev lit les règles partiellement (E007).
- Leçon M0020 : notre critère ACQUÉRIR était inatteignable même par un oracle → **tout nouveau test prouve d'abord sa validité** (oracle réussit, par-cœur échoue).
- En vol : M0021 E008 palier 0 (F01).
- Non mergés en attente : E006 (re-doublage après M0018), E003 (rejeu annulé), A0/A0-bis (R009 réserve), A0-ter oracle, E007.
- Décision attendue de Malik : mention de son enfant dans GENESE (dépôt public). Budget passerelle : 5 $ sur la clé unique, sans recharge.

## Références à ne pas toucher

- `vault/echanges/archive/2026-09-2{5,6}-F01-M000{1,2}-*.md` — références du doublage R001.

## Rappels

- Dépôt **PUBLIC** : rien de secret dans `vault/`, rapports, résultats.
- Passerelle : 5 req/min/équipe (1 fenêtre API à 15 s ou 2 à 26 s) ; tout appel à un modèle témoin impose et journalise son fournisseur ; 402 = arrêt net.
- Défauts harnais signalés : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` absent ; pas de `type` d'événement défini pour `src: fenetre`.
- Source de vérité : `00_INDEX.md` + `vault/runtime/` — et au-dessus, la preuve git rejouée.
