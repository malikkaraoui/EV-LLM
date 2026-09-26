# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-09-26T16:14:20+0200 (orchestrateur) — vague 2 en vol (5 fenêtres)

## Où on en est

- `main` = `436c8fa`. Branches : `exp/e001-sonde-jev` 7e953a9 (E001 complet) · `exp/e002-relations-opaques` 1cb586b · `exp/e003-etalon-llm` af117ab.
- En vol : F01/R001 doublage+merge E001 · F02/R002 doublage+merge E002 · F03/M0007 E002-bis · F04/M0008 E003 relance · F05/M0009 E005.
- Suivi : issues GitHub #1–#17 (`vault/notes/2026-09-26-issues-github.md`).

## Références à ne pas toucher

- `vault/echanges/archive/2026-09-2{5,6}-F01-M000{1,2}-*.md` et `vault/echanges/F01.md` (M0003) — références du doublage R001.

## Rappels

- Dépôt **PUBLIC** : rien de secret dans `vault/`, rapports, résultats.
- Incident fetch orchestrateur du 25/09 : constaté soldé le 26/09 (lock et refs `pub/*` absents).
- Défauts harnais signalés : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` absent ; pas de `type` d'événement défini pour `src: fenetre`.
- Source de vérité : `00_INDEX.md` + `vault/runtime/` — et au-dessus, la preuve git rejouée.
