# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-09-25T21:30:40+0200 (orchestrateur) — M0001 posé, sonde Jev

## Où on en est

- `main` = `343e839` — pose du harnais v1.0.0 (+ `0a644f1` genèse et architecture).
- En vol : **F01 / M0001 `e001-sonde-jev`** — première sonde du modèle Jev (7 cas préregistrés, branche `exp/e001-sonde-jev`, worktree `.claude/worktrees/F01-M0001`).
- Ensuite : doublage indépendant R001, puis merge (hook pre-push).

## Références à ne pas toucher

- `vault/echanges/F01.md` (M0001) — mandat en cours ; sera la pièce de référence du doublage R001.

## Rappels

- Dépôt **PUBLIC** (choix de Malik, 25/09) : rien de secret dans `vault/`, rapports, résultats.
- `.env` à la racine : ignoré seulement par `.git/info/exclude` (local) tant que M0001 n'a pas mergé la règle `.gitignore`. Aucun agent ne le lit ; seul `run.py` le charge.
- Défauts du harnais signalés à Malik (25/09, non corrigés ici) : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` cité par gabarits §4 mais absent.
- Écart de version harnais v1.0.0 (projet) / v1.0.1 (prod) : non vérifié par l'orchestrateur ; pas de `--maj` sans demande de Malik.
- Source de vérité : `vault/reprise/00_INDEX.md` + `vault/runtime/state.json` / `events.jsonl`
  — et, au-dessus d'eux, la preuve git rejouée à l'instant.
