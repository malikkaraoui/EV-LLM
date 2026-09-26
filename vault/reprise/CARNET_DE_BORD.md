# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-09-26T16:38:48+0200 (orchestrateur) — vague 3 en vol (5 fenêtres)

## Où on en est

- `main` = `df79ad6` — E001 et E002 mergés (R001, R002 GO).
- Branches à doubler : `exp/e002bis-mesure` d35af60 · `exp/e005-jev-hors-distribution` 08d80f7 · `exp/e003-etalon-llm` 01f3c8f (partiel).
- Résultat marquant : Jev **faux et sûr** sur 6 questions hors distribution (E005, à répliquer — E006).
- En vol : R003 · R004 · M0010 E003 rythmé · M0011 E006 · M0012 doc v2.2.
- Contrainte : passerelle AI Gateway = 5 req/min/équipe → rythmeur ≥ 26 s par fenêtre (2 fenêtres API max).

## Références à ne pas toucher

- `vault/echanges/archive/2026-09-2{5,6}-F01-M000{1,2}-*.md` et `vault/echanges/F01.md` (M0003) — références du doublage R001.

## Rappels

- Dépôt **PUBLIC** : rien de secret dans `vault/`, rapports, résultats.
- Incident fetch orchestrateur du 25/09 : constaté soldé le 26/09 (lock et refs `pub/*` absents).
- Défauts harnais signalés : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` absent ; pas de `type` d'événement défini pour `src: fenetre`.
- Source de vérité : `00_INDEX.md` + `vault/runtime/` — et au-dessus, la preuve git rejouée.
