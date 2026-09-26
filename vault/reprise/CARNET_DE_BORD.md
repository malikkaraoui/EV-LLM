# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-09-26T15:53:49+0200 (orchestrateur) — 4 mandats en vol (F01–F04)

## Où on en est

- `main` = `7c453b1`. `exp/e001-sonde-jev` = `08672e4` (E001 : T1 mesuré 6/6, T2 non servi).
- En vol : F01/M0003 rejeu T2 · F02/M0004 issues GitHub · F03/M0005 E002 relations opaques · F04/M0006 E003 étalon LLM.
- Ensuite : doublages R001 (E001), puis E002/E003 ; nouvelles pistes selon résultats (E004 contamination, E005 calibration hors distribution).

## Références à ne pas toucher

- `vault/echanges/archive/2026-09-2{5,6}-F01-M000{1,2}-*.md` et `vault/echanges/F01.md` (M0003) — références du doublage R001.

## Rappels

- Dépôt **PUBLIC** : rien de secret dans `vault/`, rapports, résultats.
- Incident fetch orchestrateur du 25/09 : constaté soldé le 26/09 (lock et refs `pub/*` absents).
- Défauts harnais signalés : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` absent ; pas de `type` d'événement défini pour `src: fenetre`.
- Source de vérité : `00_INDEX.md` + `vault/runtime/` — et au-dessus, la preuve git rejouée.
