---
date: 2026-09-26
tags: [e005, correctif, r004]
session: F01
mandat: e005-correctif-totaux
mandat_id: M0013
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F05-M0009
branche: exp/e005-jev-hors-distribution
derniere_maj: 2026-09-26T17:08:23+0200
---

# M0013 — E005 : corriger les totaux HTTP du README (verdict R004 CASSÉ)

**Tu ne poses JAMAIS de question et tu n'attends JAMAIS de réponse.** Personne n'est devant l'écran. Si tu es sur le point de demander un arbitrage, c'est un **STOP** : écris dans ton rapport la question que tu aurais posée, les options que tu voyais et celle que tu aurais choisie avec sa raison, puis applique les rituels de fin. Un STOP propre est un rendu valable ; une question laisse un mandat mort. Idem pour une autorisation d'outil refusée : contourne par une commande plus simple répondant au même besoin (lecture seule, `git show`, `git -C`, chemin explicite) ; sans contournement, STOP propre avec rapport — jamais une attente.

## Règles communes (dépôt PUBLIC, plusieurs fenêtres en parallèle)

- Dépôt `github.com/malikkaraoui/EV-LLM` **PUBLIC** : rien de secret dans ce que tu commits (ni clé, ni en-tête HTTP, ni identifiant de compte).
- `/Users/malik/Documents/EV-LLM/.env` : **ne JAMAIS le lire, l'afficher, le copier ni l'ouvrir.** Seuls les scripts le chargent, en mémoire.
- **D'autres fenêtres travaillent en même temps** sur d'autres branches. Tu ne touches QUE les chemins de ton mandat. À la racine partagée (`/Users/malik/Documents/EV-LLM`, branche `main`) : `git add -- <chemins explicites>` puis `git commit ... -- <chemins explicites>`, jamais `-a`/`-A`. Si `.git/index.lock` existe au moment d'un commit racine : refais la commande UNE fois ; si le verrou est toujours là, n'y touche pas, note-le au rapport et continue sans ce commit (STOP partiel propre).
- Push `main` : seuls les commits qui ne touchent que `vault/` passent le hook. Si un push `main` est refusé en non-fast-forward : `git fetch origin` puis `git merge --ff-only origin/main` à la racine, puis re-push, UNE fois ; sinon rapport.
- Jamais `sleep`, `stash`, `reset --hard`, `checkout -- .`, `rebase`, `push --force`. Jamais de tâche de fond vivante à la sortie. `rm -rf` seulement sous forme gardée `"${VAR:?}/${SOUS:?}"`.
- Ne touche jamais : `.claude/skills/`, `scripts/harnais-hooks/`, `config/harnais.json`, `.claude/worktrees/` (hors TON worktree), les `vault/echanges/*.md` d'autres fenêtres, `vault/echanges/archive/`, `vault/reprise/00_INDEX.md`, `vault/reprise/CARNET_DE_BORD.md` (sauf mention explicite de ta Mission 0).
- Commits signés du trailer `Co-Authored-By: Malik & Claude` (messages en heredoc), jamais le trailer par défaut de l'outil.
- Étiquettes dans tout texte : [VÉRIFIÉ] / [HYPOTHÈSE] ; aucune conclusion générale sur 7 cas.


Modèle : `opus --effort medium` (barème `realisation_standard` — correction courte mais sur une branche doublée).

## 0. Contexte
Le doublage R004 (`vault/revues/2026-09-26-R004-e005-jev-hors-distribution.md` sur `origin/main`, lis-le EN ENTIER) a rendu **CASSÉ** sur l'axe « chiffres » : dans `research/experiments/E005-jev-hors-distribution/README.md` au tip `08d80f72265d36a56ad5e916c4097426bc93cc05`, **l. 54** annonce « 8 × 503, 109 × 429 » alors que les données donnent **7 × 503, 110 × 429** ; **l. 120** dit « Les 8 × 503 » (7) et « aucun fournisseur tenté » vaut pour **107 des 110** 429. Tout le reste a été vérifié ✅ (dont les 6 « faux et sûr », 0 contesté). Loi des deux patchs : c'est le 1er correctif sur cette classe de défaut.

## 1. Gardes — tout écart : STOP + rapport
1. `fetch origin` ; `origin/exp/e005-jev-hors-distribution` = `08d80f72265d36a56ad5e916c4097426bc93cc05`.
2. Worktree `/Users/malik/Documents/EV-LLM/.claude/worktrees/F05-M0009` présent, HEAD `08d80f7…`, branche `exp/e005-jev-hors-distribution`, aucun fichier suivi modifié. (Sinon : `git worktree add /Users/malik/Documents/EV-LLM/.claude/worktrees/F01-M0013 exp/e005-jev-hors-distribution` et travaille là.)

## 1 bis. Mission 0 — racine, `main` (avant la Mission 1)
Committe UNIQUEMENT (s'ils sont nouveaux/modifiés) : `vault/echanges/archive/2026-09-26-F01-R003-doublage-e002bis.md`, `vault/echanges/archive/2026-09-26-F02-R004-doublage-e005.md`, `vault/echanges/archive/2026-09-26-F03-M0010-e003-amendement-2.md`, `vault/echanges/archive/2026-09-26-F05-M0012-doc-v2.2-resultats.md`, `vault/reprise/CARNET_DE_BORD.md`, `vault/reprise/00_INDEX.md` — message `docs(vault): archives vague 3 + carnet/index -- pose vague 4`. Push, `ls-remote` collé.

## 2. Mission 1
1. **Recompte TOI-MÊME** depuis les 6 `results/*/raw.public.jsonl` : statuts HTTP totaux et par lancement ; nombre de 429 avec `providerAttemptCount` = 0 ; tout autre total écrit dans le README (appels, réponses 200, questions couvertes). Script ad hoc dans le scratchpad, sortie collée au rapport.
2. Corrige **uniquement** les chiffres faux du README (et de `results/analyse.md` s'il porte le même total), en ajoutant une note « Correctif M0013 (26/09) : totaux recomptés après R004 ». Aucun autre changement. `cases.json`, résultats bruts, code : intouchés (`git diff --name-only` = README [+ analyse.md]).
3. Commit `fix(e005): totaux HTTP recomptes (R004)` ; push ; `ls-remote`.
4. Si `gh auth status` OK : `gh issue comment 6 -R malikkaraoui/EV-LLM --body "<correctif M0013 + tip>"`.

## 3. Preuves
Recomptage collé ; `git diff` complet collé ; `ls-remote` branche et main.

## Rituels

DÉBUT : `statut: en-cours` à la racine du frontmatter de CE fichier, avant tout.

FIN, dans l'ordre :
1. Rapport appendé sous `## Rapport M0013` (preuves collées).
2. `vault/reprise/F01.md` (état + prochaine étape) — à la racine.
3. Une ligne `vault/runtime/events.jsonl` (`src: "fenetre"`, `type: "RAPPORT_RENDU"`, `f`, `mandat`, `note` ≤ 200 car.) + `windows.F01` dans `vault/runtime/state.json` — hors git, jamais committés. **state.json : lecture JSON → modification de la SEULE clé `windows.F01` → réécriture ; toutes les autres clés (`schema_version`, `next_mandat_id`, `next_revue_id`, `projet`, autres fenêtres) sont conservées à l'identique. Vérifie après écriture que `next_mandat_id` est toujours présent (incident du 26/09 : state.json écrasé).** Toute ligne `events.jsonl` porte `ts` (horloge réelle `TZ=Europe/Paris date +%Y-%m-%dT%H:%M:%S%:z`).
4. Commit de `vault/reprise/F01.md` sur `main` à la racine (vault seul) + push + `git ls-remote origin refs/heads/main` collé.
5. Ta branche (s'il y en a une) poussée + `git ls-remote origin refs/heads/<branche>` collé.
6. Footer de statut, toute dernière ligne du rapport :
```
M0013
Implementation      ✅/❌
Tests               ✅/❌
Commit              ✅/❌
Branch push         ✅/❌
Review              ❌
Merge main          ❌
Main push           ✅/❌   (vault seul)
TASK STATUS         <READY_FOR_INTEGRATION | BLOCKED>
PROJECT STATUS      NOT_INTEGRATED
```
7. EN DERNIER GESTE : `statut: reponse-disponible`.

## Rapport M0013

Fenêtre F01, 2026-09-26. Worktree `.claude/worktrees/F05-M0009` (garde 2 OK, pas de nouveau worktree). API Jev non appelée. `.env` non ouvert.

### Gardes [VÉRIFIÉ]
```
origin/exp/e005-jev-hors-distribution = 08d80f72265d36a56ad5e916c4097426bc93cc05   ✅
worktree F05-M0009 : HEAD 08d80f7…, branche exp/e005-jev-hors-distribution, aucun suivi modifié   ✅
```

### Mission 0 [VÉRIFIÉ]
Commit `702ce495cbdcd9fb0f1f5b18feadf70a1ec6e7aa` « docs(vault): archives vague 3 + carnet/index -- pose vague 4 » : les 4 archives + CARNET_DE_BORD + 00_INDEX (6 fichiers, rien d'autre). Push `8a5b865..702ce49 main -> main`.
```
702ce495cbdcd9fb0f1f5b18feadf70a1ec6e7aa	refs/heads/main
```
(1re tentative : chemins passés via une variable zsh non découpée → `pathspec did not match`, rien committé ; refaite avec chemins littéraux.)

### Mission 1.1 — recomptage indépendant (`scratchpad/recompte.py`, lit seulement les 6 `raw.public.jsonl` + `cases.json`)
```
2026-09-26T161655+0200 appels 32 {200: 9, 429: 22, 503: 1}
2026-09-26T161811+0200 appels 23 {200: 6, 429: 16, 503: 1}
2026-09-26T161845+0200 appels 32 {429: 32}
2026-09-26T161956+0200 appels 20 {200: 8, 429: 10, 503: 2}
2026-09-26T162058+0200 appels 15 {200: 4, 429: 9, 503: 2}
2026-09-26T162237+0200 appels 29 {200: 7, 429: 21, 503: 1}
TOTAL appels 151 {200: 34, 429: 110, 503: 7}
429 avec totalProviderAttemptCount=0 : 107 / 110
429 avec tentative : [('F2-06', 1, ['digitalocean']), ('F2-07', 1, ['digitalocean']), ('F3-06', 1, ['digitalocean'])]
fournisseurs tentes sur 503 : {'digitalocean': 7}
cas distincts avec >=1 reponse 200 : 31 ; questions evaluees (reponses 200 x questions) : 42
cas 32 questions 38 ; >=1 reponse 200 : 37 ; >=2 : [('F1-04', 'correcte'), ('F4-01', 'e_sup_d'), ('F4-01', 'statut'), ('F4-04', 'a_sup_f'), ('F4-04', 'statut')] ; 0 : [('F5-03', 'correcte')]
```
Confrontation au README [VÉRIFIÉ] : tableau par lancement (l. 47-52) = recomptage ; 151 appels, 34 × 200 justes ; **503 : 7 (README 8) ; 429 : 110 (README 109)** ; 107/110 des 429 à `totalProviderAttemptCount` 0 (3 exceptions F2-06, F2-07, F3-06 avec 1 tentative `digitalocean`) ; 503 tous `digitalocean` (7/7) ✅ ; couverture 37/38 questions, 5 à 2 réponses, F5-03 à 0 ✅ ; 42 évaluations ✅. `results/analyse.md` ne porte que le détail par lancement (juste), aucun total → non modifié.

### Mission 1.2 — correctif (README seul)
Écart assumé au périmètre strict de R004 : outre l. 54 et l. 120, j'ai corrigé **l. 126 (Limites)**, qui affirmait le même fait faux (`providerAttemptCount: 0` pour tous les 429) → « `totalProviderAttemptCount: 0` pour 107 des 110 ». Même classe de défaut ; la laisser aurait reproduit le CASSÉ au redoublage. Aucun autre changement.
```diff
diff --git a/research/experiments/E005-jev-hors-distribution/README.md b/research/experiments/E005-jev-hors-distribution/README.md
index f918613..79529db 100644
--- a/research/experiments/E005-jev-hors-distribution/README.md
+++ b/research/experiments/E005-jev-hors-distribution/README.md
@@ -51,7 +51,9 @@ python3 analyse.py
 | 5 | `results/2026-09-26T162058+0200/` | 16:20:58 | 62 s | 15 | 4×200, 2×503, 9×429 |
 | 6 | `results/2026-09-26T162237+0200/` | 16:22:37 | 99 s | 29 | 7×200, 1×503, 21×429 |
 
-Total : **151 appels** (budget 200), **34 × 200**, 8 × 503, 109 × 429. Aucun 401/403/404, aucun code 3. Les lancements 2 à 6 portent sur des sous-corpus dérivés (`derive.py`), dans un ordre de priorité fixé avant chaque lancement : cas sans réponse d'abord, puis réplication des non-conformités, puis le reste.
+Total : **151 appels** (budget 200), **34 × 200**, 7 × 503, 110 × 429. Aucun 401/403/404, aucun code 3. Les lancements 2 à 6 portent sur des sous-corpus dérivés (`derive.py`), dans un ordre de priorité fixé avant chaque lancement : cas sans réponse d'abord, puis réplication des non-conformités, puis le reste.
+
+> Correctif M0013 (26/09) : totaux recomptés après R004 — 7 × 503 et 110 × 429 (et non 8 et 109) ; 107 des 110 réponses 429 ont `totalProviderAttemptCount` = 0. Le tableau par lancement était déjà juste.
 
 Chaque dossier contient `raw.public.jsonl` (= `raw.jsonl` sans la clé `response_headers`, égalité vérifiée ligne à ligne), `summary.json`, `summary.md`. Agrégat `aggregate.py` (médianes, règle d'E001) : [`results/agregat-2026-09-26T162249+0200/summary.md`](results/agregat-2026-09-26T162249+0200/summary.md). Analyse appel par appel : [`results/analyse.md`](results/analyse.md) (+ `analyse.json`).
 
@@ -117,13 +119,13 @@ Toutes questions, probabilité de la réponse renvoyée ≥ 0.8 : 19 conformes s
    - [VÉRIFIÉ] Au-dessus de 0.8 de probabilité sur sa réponse, Jev est conforme 19 fois sur 28 (68 %). Dans la tranche 0.4–0.6, il l'est 4 fois sur 6. La confiance ne sépare pas ici le juste du faux.
    - [HYPOTHÈSE] Avec 42 évaluations tirées d'un corpus construit pour piéger, ce n'est pas une courbe de calibration du modèle, seulement un indice : sur ce type de cas, une P haute ne suffirait pas à décider de ne pas vérifier (§1 bis v2.1, point 5).
 6. **Statuts HTTP.**
-   - [VÉRIFIÉ] Le fournisseur sert 0 à 9 réponses 200 par lancement, puis renvoie des 429 en rafale (`rate_limit_exceeded`, « upstream provider … high demand », aucun fournisseur tenté). Les 8 × 503 viennent tous de `digitalocean`.
+   - [VÉRIFIÉ] Le fournisseur sert 0 à 9 réponses 200 par lancement, puis renvoie des 429 en rafale (`rate_limit_exceeded`, « upstream provider … high demand », aucun fournisseur tenté pour 107 des 110 ; les 3 autres — F2-06, F2-07, F3-06 — ont 1 tentative `digitalocean`). Les 7 × 503 viennent tous de `digitalocean`.
    - [HYPOTHÈSE] Une autre fenêtre (F04, E003) appelait la même passerelle jusque vers 16:20 ; une limite partagée a pu contribuer aux 429.
 
 ## Limites
 
 - 32 cas, 1 à quelques réponses 200 par question : **aucune conclusion générale**. Une paire minimale ne représente pas sa règle.
-- Le fournisseur sature après ~6 à 9 appels enchaînés (429 `rate_limit_exceeded`, « upstream provider … high demand », `providerAttemptCount: 0`) ; les 503 viennent tous de `digitalocean`. L'objectif « ≥ 2 réponses 200 par question » n'est pas atteint partout (tableau de couverture ci-dessus).
+- Le fournisseur sature après ~6 à 9 appels enchaînés (429 `rate_limit_exceeded`, « upstream provider … high demand », `totalProviderAttemptCount: 0` pour 107 des 110) ; les 503 viennent tous de `digitalocean`. L'objectif « ≥ 2 réponses 200 par question » n'est pas atteint partout (tableau de couverture ci-dessus).
 - L'ordre des cas dans les lancements 3 à 6 a été choisi **après** avoir vu les premières réponses (priorité : cas sans réponse, puis réplication des non-conformités). Cela change **quels** cas ont 2 réponses, jamais les attentes ni la règle de lecture ; mais les cas répliqués sont surreprésentés parmi les non-conformités.
 - Lancement 3 parti **34 s** après le lancement 2 (< 60 s exigé) : écart de protocole de la fenêtre, 32 appels perdus en 429. Garde bloquante ajoutée ensuite (refus prouvé à 31 s et 51 s).
 - La consigne demande si la phrase est « orthographiquement correcte ». [HYPOTHÈSE] Jev peut juger une autre notion (plausibilité, fluidité) ; c'est précisément ce que la sonde cherche à exposer, mais la frontière n'est pas mesurée.
```

### Mission 1.3 / 1.4
Commit `15487b062d8e9a319c8ee945c0e2c8a3399aea22` « fix(e005): totaux HTTP recomptes (R004) », trailer `Co-Authored-By: Malik & Claude`. `git diff --name-only HEAD~1 HEAD` = `research/experiments/E005-jev-hors-distribution/README.md` seul. Push `08d80f7..15487b0`.
```
15487b062d8e9a319c8ee945c0e2c8a3399aea22	refs/heads/exp/e005-jev-hors-distribution
```
Issue #6 commentée : https://github.com/malikkaraoui/EV-LLM/issues/6#issuecomment-5847347626

### Pour l'orchestrateur
- Nouveau tip `15487b0` à **redoubler** (loi des deux patchs : 1er correctif sur cette classe). Axes 1, 2, 5, 6, 7 de R004 rejouables rapidement ; axe 3/4 : vérifier les 3 lignes modifiées + la note.
- [HYPOTHÈSE] Le rapport d'auteur M0009 (archive) porte le même total faux ; non modifié (hors périmètre, archive intouchable).
- Candidate leçon transverse (R5) : un total écrit à la main à côté d'un tableau calculé diverge ; le faire sortir du script d'analyse, pas du rédacteur.

### ls-remote main (après commit reprise)
Commit `3e97f5d` (vault/reprise/F01.md seul), push `702ce49..3e97f5d`.
```
3e97f5d638d83aa49bcf61eb67dc0faabddb6474	refs/heads/main
15487b062d8e9a319c8ee945c0e2c8a3399aea22	refs/heads/exp/e005-jev-hors-distribution
```
Runtime : 1 ligne `RAPPORT_RENDU` dans events.jsonl ; `windows.F01` seul modifié dans state.json (clés conservées, `next_mandat_id` = M0015 vérifié après écriture). Hors git.

```
M0013
Implementation      ✅
Tests               ✅
Commit              ✅
Branch push         ✅
Review              ❌
Merge main          ❌
Main push           ✅   (vault seul)
TASK STATUS         READY_FOR_INTEGRATION
PROJECT STATUS      NOT_INTEGRATED
```
