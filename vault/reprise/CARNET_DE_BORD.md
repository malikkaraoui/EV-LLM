# CARNET DE BORD — instantané (1 minute)

Dernière mise à jour : 2026-09-26T18:03:33+02:00 (orchestrateur) — vague 6 en vol

## Où on en est

- `main` contient E001, E002, E002-bis, **E005**, doc v2.2 + GENESE.
- Jev : **5 « faux et sûr » non contestés, répliqués 5/5** (E006) + 1 réponse contestée (question ambiguë, R008) ; E007 teste « Jev lit-il les règles ? ».
- Candidats ACQUÉRIR : A0 1/4, A0-bis 0/4 → M0020 vérifie d'abord que le critère est **atteignable** (étalon oracle).
- E003 : backend passerelle non contrôlé (défaut de protocole) → M0019 puis rejeu M0021 ; merge E003 bloqué d'ici là.
- En vol : M0017 (F05) · M0018 · M0019 · R009 · M0020.
- Décisions attendues de Malik : mention de son enfant dans GENESE (dépôt public) ; budget passerelle 5 $ (à poser, navigateur non connecté).

## Références à ne pas toucher

- `vault/echanges/archive/2026-09-2{5,6}-F01-M000{1,2}-*.md` — références du doublage R001.

## Rappels

- Dépôt **PUBLIC** : rien de secret dans `vault/`, rapports, résultats.
- Passerelle : 5 req/min/équipe (1 fenêtre API à 15 s ou 2 à 26 s) ; tout appel à un modèle témoin impose et journalise son fournisseur ; 402 = arrêt net.
- Défauts harnais signalés : `.claude/worktrees/` non ignoré ; `scripts/verifier-rendu.mjs` absent ; pas de `type` d'événement défini pour `src: fenetre`.
- Source de vérité : `00_INDEX.md` + `vault/runtime/` — et au-dessus, la preuve git rejouée.
