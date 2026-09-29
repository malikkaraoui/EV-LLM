---
date: 2026-09-28
revue: R015
branche: docs/readme-digeste
tip: 39f015f54129816acb302295dc4945faad4d8f15
verdict: GO
---

# R015 — Doublage du README racine digeste + LICENSE + rangement (`docs/readme-digeste`, tip 39f015f)

**Verdict : GO.** Merge `--no-ff` dans `main` autorisé par Malik (28/09, session Cowork, hors bureau).

## Tip relu et tip mergé

- Le re-doublage final a porté sur **dc4906df895d796550a3ccc8b0dfd3f798293906**.
- Au premier push, le hook `pre-push` a refusé : dc4906d contenait un merge interne (19c5af9) de `f99553a`, qui n'a jamais eu de GO (R013 et R014 en RÉSERVE). Le refus était légitime et le hook n'a pas été contourné.
- La branche a donc été linéarisée par `git rebase origin/main`, sans aucune édition. Le tip devient **39f015f54129816acb302295dc4945faad4d8f15**.
- Preuve d'identité du contenu relu : `git diff --name-only dc4906d 39f015f | grep -v '^vault/'` → **vide**. Les seules différences sont sous `vault/` et viennent de main (ed790c9 R014, 0199c96 reprise F03).
- `git diff -M --stat origin/main 39f015f` touche exactement 6 fichiers : README.md, LICENSE, .gitignore, GENESE.md (1 l.), architecture_cognitive_post_transformer.md (1 l.) et le renommage à 100 % vers `docs/archive/`.

## Contexte

- Base : `docs/readme-2026-09-28` (f99553a, R013 RÉSERVE puis R014 RÉSERVE). Ses 4 commits sont rejoués dans la branche (28e539d, 89b7147, edfcb6f, fb31b84).
- 96e24c6 : mise en page digeste (TL;DR, tableau « Results at a glance » de 21 lignes, journal replié en `<details>`, impasses en tableau, arborescence) ; `architecture_cognitive_post_transformer.v1-gpt.md` → `docs/archive/` (renommage pur, 2 mentions mises à jour) ; `.gitignore` + `.DS_Store`, `.claude/worktrees/`.
- R014 (« loi des deux patchs ») recommandait un audit tiers de TOUTES les phrases de synthèse, étiquette → source → affirmation, puis une seule passe de correction. C'est ce qui a été fait.

## Chaîne de relecture (agents indépendants de l'auteur, lecture seule)

| Étape | Tip (avant rebase) | Portée | Résultat |
|---|---|---|---|
| Relecture fidélité | 22a7bd2 | candidat vs référence f99553a | RÉSERVE : E013 1 131 ≠ 1 196 paramètres (2 nombres d'état) + 13 précisions → 5a34358 |
| Audit tiers des synthèses | 5a34358 | TL;DR, « What we believe », Open leads, 21 × (résultat, verdict), 16 impasses, contre les README sources au tip de chaque branche | 13 défauts, dont les 2 de R014 (l.189 exclusivité, l.191 E012 X1→X3) → passe unique 46209bc |
| Doublage hostile complet | 46209bc | mêmes sections + 26 chiffres du journal hors R013/R014 + liens, rendu, secrets, périmètre | RÉSERVE : 3 moyens (E015-A2 non sourcé, ECH0 = un seul champion, perte à 1 000 chiffres d'E014) + 7 faibles → dc4906d |
| Re-doublage delta | dc4906d | les 10 écarts + `git diff 46209bc dc4906d` | **GO** |

## Axes vérifiés (dc4906d, contenu identique à 39f015f)

| # | Axe | Verdict | Preuve |
|---|---|---|---|
| 1 | Synthèses vs sources | ✅ | Chaque [VERIFIED] est porté par une source de son étiquette. Exclusivité « except 1 seed out of 5 (E014 R0b) » vérifiée à 16 chiffres contre E008 l.81, E009-bis l.44/50, E010 l.77, E013 l.68, E014 l.61–65 |
| 2 | Défauts R014 | ✅ | l.189 → « no seed reaches 90 % at 16 digits … E008 B-REF 91.2 % at 6 » ; l.191 → E012 X3 (l.43) |
| 3 | Chiffres du journal | ✅ | 26 chiffres hors R013/R014, 0 écart ; entrée A0-bis alignée sur R009 l.154/158 |
| 4 | Liens, rendu, secrets | ✅ | 0 lien relatif manquant ; 10 ancres ; 4 tableaux à colonnes constantes ; grep secrets/e-mail rc=1 |
| 5 | Périmètre | ✅ | voir « Tip relu et tip mergé » |

## Réserves de méthode (honnêteté)

- Les relectures sont des sous-agents d'une session Cowork, pas une fenêtre du bureau. Ils sont indépendants de l'auteur, mais c'est lui qui les a lancés.
- La première relecture (22a7bd2) ne vérifiait que la fidélité à f99553a, pas les sources. Elle aurait laissé passer les défauts de R014. Leçon : **une relecture de reformulation doit remonter aux sources, jamais à la version précédente.**
- La liste d'antériorité E015-A2 (Braylan, Guijt, Schug, Cully…) a été retirée du README : elle n'existe que dans le mandat M0033, non versionné.
- Numérotation : R015 est pris par ce rapport. Le prochain doublage du bureau devra partir de R016.
