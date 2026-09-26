# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-09-26T17:08:23+0200 (orchestrateur) — vague 4 en vol

## Où on en est

- `main` = `8a5b865` — E001, E002, E002-bis mergés.
- À doubler/merger : E003 `73cdc79` (R005) · doc v2.2 `bcfb722` (R006) · E005 après correctif (M0013 → re-doublage).
- En vol : M0011 E006 (réplication + contamination, API) · M0013 · R005 · R006 · **M0014 A0 premier candidat**.
- Point pour Malik : GENESE (public) mentionne son enfant — décision à prendre.

## Références à ne pas toucher

- `vault/echanges/archive/2026-09-2{5,6}-F01-M000{1,2}-*.md` et `vault/echanges/F01.md` (M0003) — références du doublage R001.

## Rappels

- Dépôt **PUBLIC** : rien de secret dans `vault/`, rapports, résultats.
- Incident fetch orchestrateur du 25/09 : constaté soldé le 26/09 (lock et refs `pub/*` absents).
- Défauts harnais signalés : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` absent ; pas de `type` d'événement défini pour `src: fenetre`.
- Source de vérité : `00_INDEX.md` + `vault/runtime/` — et au-dessus, la preuve git rejouée.
