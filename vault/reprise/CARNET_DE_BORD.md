# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-09-26T10:28:42+0200 (orchestrateur) — M0002 posé, rejeu sonde Jev

## Où on en est

- `main` = `525be53` — reprise F01 (vault seul) ; `2791564` = décision exception + carnet/index.
- `exp/e001-sonde-jev` = `2719279` — sonde Jev prête (script + 7 cas figés), **non mesurée** : AI Gateway renvoie 403 `customer_verification_required`.
- En vol : **F01 / M0002 `e001-rejeu-mesure`** — rejeu E001 après ajout de la carte Vercel (26/09 10:27). Ensuite : doublage R001 → merge.

## Références à ne pas toucher

- `vault/echanges/archive/2026-09-25-F01-M0001-e001-sonde-jev.md` (M0001) et `vault/echanges/F01.md` (M0002) — références du doublage R001.

## Rappels

- Dépôt **PUBLIC** : rien de secret dans `vault/`, rapports, résultats.
- Incident fetch orchestrateur du 25/09 : constaté soldé le 26/09 (lock et refs `pub/*` absents).
- Défauts harnais signalés : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` absent ; pas de `type` d'événement défini pour `src: fenetre`.
- Source de vérité : `00_INDEX.md` + `vault/runtime/` — et au-dessus, la preuve git rejouée.
