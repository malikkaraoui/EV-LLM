---
date: 2026-09-26
tags: [e005, jev, calibration, hors-distribution]
session: F05
mandat: e005-jev-hors-distribution
mandat_id: M0009
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F05-M0009
branche: exp/e005-jev-hors-distribution
derniere_maj: 2026-09-26T16:14:20+0200
---

# M0009 — E005 : Jev hors distribution — où se trompe-t-il, et le sait-il ?

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


Modèle : `opus --effort medium` (barème `conception_critique` : c'est la conception du corpus qui fait la valeur).

## 0. Contexte
Défi D15 (§63 de `architecture_cognitive_post_transformer.md`, §1 bis v2.1 points 3 et 5) : un **déclencheur** (« quand vérifier ») exige une confiance honnête sur les **erreurs invisibles** — fausses mais fluides. E001 (branche `origin/exp/e001-sonde-jev`, README à lire au tip `7e953a9b0197abfe0dd60137343da9a6e308c6c3`) : Jev a été **juste et sûr** sur 7 cas, dont 4 fautes é/er et d'accord **fréquentes** — le « faux et sûr » n'a **jamais été exercé**. But d'E005 : **trouver des cas où Jev se trompe**, et mesurer s'il se trompe avec assurance.

## 1. Gardes — tout écart : STOP + rapport
1. `fetch origin` ; `origin/exp/e001-sonde-jev` = `7e953a9b0197abfe0dd60137343da9a6e308c6c3`.
2. Branche `exp/e005-jev-hors-distribution` et dossier `…/.claude/worktrees/F05-M0009` absents.
3. `test -f /Users/malik/Documents/EV-LLM/.env && echo PRESENT`.

## 2. Mission 1
`git -C /Users/malik/Documents/EV-LLM worktree add -b exp/e005-jev-hors-distribution /Users/malik/Documents/EV-LLM/.claude/worktrees/F05-M0009 origin/exp/e001-sonde-jev` (pour **réutiliser** `run.py` et `aggregate.py` d'E001 par import/appel, sans les modifier). Travail sous `research/experiments/E005-jev-hors-distribution/`.
1. **Corpus préenregistré** `cases.json` (même schéma qu'E001), **committé avant tout appel**, ~30 cas, attentes décidées par TOI avec justification grammaticale d'une ligne par cas (champ `justification`), répartis en familles :
   - F1 accords rares : participe passé avec « avoir » et COD antéposé (« les pommes qu'il a mangées »), verbes pronominaux (« elles se sont lavé les mains » vs « elles se sont lavées »), « laissé/fait » + infinitif ;
   - F2 homophones moins fréquents : « quel/quelle/qu'elle », « censé/sensé », « près/prêt », « a/à » en contexte ambigu ;
   - F3 phrases **justes mais atypiques** (le piège inverse : juste mais qui « sonne faux ») ;
   - F4 logique (format T1) avec **distracteurs** : une règle non pertinente ou un fait redondant ajouté ; et une variante où la contradiction est à 4 pas de déduction ;
   - F5 contrôles triviaux (bornes basse/haute, comme T1-C).
   Environ moitié juste / moitié fausse par famille. Relis chaque attente deux fois ; en cas de doute grammatical réel, retire le cas (ne jamais garder une attente incertaine) et note-le.
2. **Lancements** avec `run.py` d'E001 (appelé tel quel, `--cases` pointant vers ce corpus), `--reps 1`, **plusieurs lancements** ; politique 429/503 : au plus 6 lancements, séparés par des horodatages mesurés (≥ 60 s entre deux départs — mesure l'écart avec `date`, occupe-toi en rédigeant ; **jamais `sleep`**). Objectif : ≥ 2 réponses 200 par question. Budget dur : 200 appels.
3. **Agrégation** via `aggregate.py` d'E001 ; publication `raw.public.jsonl` (sans `response_headers`, équivalence prouvée) ; `raw.jsonl` ignoré.
4. **Analyse** `analyse.py` (stdlib) → `results/analyse.md` : par famille, taux conforme ; **liste des « faux et sûr »** (le résultat clé) ; courbe de calibration grossière (P binnée 0–0.2 … 0.8–1 vs taux de conformité) ; le `confidence` de `providerMetadata` quand présent.
5. **README** : Hypothèse (D15), Protocole, Rejouer, Résultats, Lecture étiquetée — **si aucun « faux et sûr » : le dire tel quel, sans l'adoucir ni le gonfler**, et proposer une famille plus dure ; Limites ; Prochaine étape.
6. Commits ciblés (corpus AVANT appels, prouvé) sous `research/experiments/E005-jev-hors-distribution/` ; push branche.

## 3. STOP supplémentaires
401/403/404, code de fuite, budget atteint, corps avec identifiant de compte/e-mail/nom ; toute envie de modifier une attente après avoir vu une réponse de Jev (écris-la au rapport — c'est une donnée) ; modification d'un fichier d'E001.

## 4. Preuves
Gardes ; commit du corpus antérieur au premier appel ; statuts HTTP par lancement et écarts mesurés entre départs ; tableau par famille ; liste « faux et sûr » ; `grep` = 0 ; `ls-remote` branche et main. Si `gh auth status` OK : `gh issue comment 6 -R malikkaraoui/EV-LLM --body "<résumé>"`.

## Rituels

DÉBUT : `statut: en-cours` à la racine du frontmatter de CE fichier, avant tout.

FIN, dans l'ordre :
1. Rapport appendé sous `## Rapport M0009` (preuves collées).
2. `vault/reprise/F05.md` (état + prochaine étape) — à la racine.
3. Une ligne `vault/runtime/events.jsonl` (`src: "fenetre"`, `type: "RAPPORT_RENDU"`, `f`, `mandat`, `note` ≤ 200 car.) + `windows.F05` dans `vault/runtime/state.json` — hors git, jamais committés. **state.json : lecture JSON → modification de la SEULE clé `windows.F05` → réécriture ; toutes les autres clés (`schema_version`, `next_mandat_id`, `next_revue_id`, `projet`, autres fenêtres) sont conservées à l'identique. Vérifie après écriture que `next_mandat_id` est toujours présent (incident du 26/09 : state.json écrasé).** Toute ligne `events.jsonl` porte `ts` (horloge réelle `TZ=Europe/Paris date +%Y-%m-%dT%H:%M:%S%:z`).
4. Commit de `vault/reprise/F05.md` sur `main` à la racine (vault seul) + push + `git ls-remote origin refs/heads/main` collé.
5. Ta branche (s'il y en a une) poussée + `git ls-remote origin refs/heads/<branche>` collé.
6. Footer de statut, toute dernière ligne du rapport :
```
M0009
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

## Rapport M0009

Fenêtre F05, 2026-09-26 16:14 → 16:26 (Europe/Paris). Branche `exp/e005-jev-hors-distribution`, tip `08d80f7`. Worktree `.claude/worktrees/F05-M0009` conservé.

### Gardes
```
G1  git fetch origin ; git rev-parse origin/exp/e001-sonde-jev
    7e953a9b0197abfe0dd60137343da9a6e308c6c3                      ✅ attendu
G2  git branch -a --list '*e005*'  → (vide) ; ls .claude/worktrees/F05-M0009 → No such file   ✅
G3  test -f .env && echo PRESENT → PRESENT                          ✅ (jamais lu)
```

### Corpus préenregistré AVANT le premier appel
- `research/experiments/E005-jev-hors-distribution/cases.json` : 32 cas, 38 questions, sha256 `5f3790074e08446e40860a02d56773ae58bfe92cb8e3a046d3345fb3089d2032`, généré par `gen_cases.py` (régénération → même sha256, vérifié).
- `git log -1 -- cases.json` → `719d4c0 2026-09-26T16:16:47+02:00`, poussé (`ls-remote` = 719d4c0) **avant** le premier appel `ts 2026-09-26T16:16:55+02:00` (première ligne de `results/2026-09-26T161655+0200/raw.public.jsonl`). `git diff --quiet 719d4c0 HEAD -- cases.json` → inchangé.
- Familles (paires minimales, ≈ moitié juste / fausse) : F1 accords rares 10 (5/5) ; F2 homophones 8 (4/4) ; F3 juste atypique 6 (3/3) ; F4 logique 5 (distracteurs ×3, 4 pas ×2) ; F5 contrôles 3.
- Relecture double faite. **Aucun cas retiré.** Point de doute examiné et gardé : F1-09 « laissé partir » invariable = juste depuis les rectifications de 1990 (attente `true` certaine sous la norme actuelle ; noté en Limites).
- Attentes logiques F4/F5 recalculées mécaniquement par `verifie_logique.py` (fermeture transitive, sans Jev) : 6/6 OK ; test de mutation (F4-04 → coherent) détecté, code 1.
- **Envie de modifier une attente après avoir vu Jev : aucune.** Les attentes contredites (F1-04/05/08, F3-02, F4-01, F4-04) ont été relues à chaque fois contre la règle ; elles tiennent.

### Lancements (run.py d'E001 non modifié, `--reps 1`)
| # | départ | écart mesuré | appels | statuts |
|---|---|---|---|---|
| 1 | 16:16:55 | — | 32 | 9×200, 1×503, 22×429 |
| 2 | 16:18:11 | 76 s | 23 | 6×200, 1×503, 16×429 |
| 3 | 16:18:45 | **34 s ❌** | 32 | 32×429 |
| 4 | 16:19:56 | 71 s | 20 | 8×200, 2×503, 10×429 |
| 5 | 16:20:58 | 62 s | 15 | 4×200, 2×503, 9×429 |
| 6 | 16:22:37 | 99 s | 29 | 7×200, 1×503, 21×429 |

Total 151 appels ≤ 200 ; 34×200, 8×503 (tous `digitalocean`), 109×429 (`rate_limit_exceeded`, « upstream provider … high demand », `providerAttemptCount 0`). Aucun 401/403/404, aucun code 3.

**Écart de protocole (ma faute)** : le lancement 3 est parti 34 s après le 2 (< 60 s). Ma commande affichait l'écart sans le bloquer. Correction : un lanceur avec garde bloquante (écart ≥ 60 s et budget ≤ 200). Le refus a été prouvé deux fois (« GARDE: ecart 51 s < 60 », puis 31 s ; code 8, aucun appel). Coût : 32 appels, tous en 429.
- Lancements 2 à 6 : sous-corpus **dérivés mécaniquement** par `derive.py` (cas recopiés à l'identique, assertion champ par champ), comme `cases-T2.json` d'E001. `aggregate.py` a revérifié state/questions de chaque appel. L'ordre de priorité (cas sans réponse d'abord, puis réplication des non-conformités) a été décidé après avoir vu des réponses ; il est noté en Limites.
- `run.py` écrit dans `E001-jev-sonde/results/` : chaque dossier a été **déplacé** vers `E005…/results/`. `git diff 7e953a9 HEAD -- research/experiments/E001-jev-sonde` → vide ; `git status` E001 → vide.
- **Objectif « ≥ 2 réponses 200 par question » non atteint** : 37/38 questions ont ≥ 1 réponse, 5/38 en ont 2, F5-03 n'en a aucune. Plafond de 6 lancements atteint.
- [HYPOTHÈSE] F04 (E003) appelait la même passerelle jusque vers 16:20, et la limite a pu être partagée.

### Tableau par famille (appel par appel, `results/analyse.md`)
| famille | questions | éval. | conformes | faux et sûr |
|---|---|---|---|---|
| F1 accords rares | 10 | 11 | 6/11 | 4 |
| F2 homophones | 8 | 8 | 8/8 | 0 |
| F3 juste atypique | 6 | 6 | 4/6 | 1 |
| F4 distracteurs | 6 | 8 | 5/8 | 2 |
| F4 4 pas | 4 | 6 | 2/6 | 2 |
| F5 contrôles | 3 | 3 | 3/3 | 0 |
| total | 37 | 42 | 28/42 | 9 |

### Liste « faux et sûr » [VÉRIFIÉ] (l'agrégat médian d'`aggregate.py` marque les mêmes 6 questions)
- F1-04 « Elles se sont lavées les mains avant le repas. » : P(correcte) 0.84 / 0.85 (2 appels)
- F1-05 « Ils se sont parlés pendant des heures. » : 0.80 (pile au seuil)
- F1-08 « Les robes qu'elle a faites faire sont superbes. » : 0.86
- F3-02 « Ci-jointe la facture demandée. » : 0.86
- F4-01 `statut` (T1-A + fait redondant + règle non pertinente) : `coherent` 0.88 / 0.89, `confidence` 0.82 / 0.84 (2 appels)
- F4-04 `a_sup_f` (A > F en 4 pas) : P 0.15 / 0.19 (2 appels)

Lecture courte :
- [VÉRIFIÉ] Phrases justes : 13/13 conformes. Phrases fausses : 6/13 ; les 7 autres évaluations jugent la phrase fautive « correcte ».
- [VÉRIFIÉ] F4 : les 7 réponses `statut` sur 7 valent `coherent`.
- [VÉRIFIÉ] Réponses dont la probabilité est ≥ 0.8 : 19 conformes sur 28.
- [HYPOTHÈSE] Jev juge la plausibilité de surface plutôt que la règle. 42 évaluations : aucune conclusion générale.

### Publication / fuite
- `raw.public.jsonl` = `raw.jsonl` sans `response_headers`, égalité ligne à ligne vérifiée sur les 6 dossiers (32/23/32/20/15/29 lignes, `True`). Les `raw.jsonl` sont ignorés par `.gitignore:42` (`git status --ignored` → `!!`), et 0 est committé.
- Garde anti-fuite de `run.py` : codes de sortie 1, jamais 3.
- `grep` (e-mail, Bearer, Authorization, team_/ownerId/userId/accountId, nom, `AI_GATEWAY_API_KEY=`) sur tous les fichiers committés : **0** dans les données. Une seule occurrence, documentaire : `README.md:56` « sans la clé `response_headers` ».

### Commits (branche)
```
08d80f7 2026-09-26T16:24:06+02:00 feat(e005): 6 lancements, agregat, analyse, README -- 9 « faux et sur »
6ddaab9 2026-09-26T16:21:49+02:00 test(e005): verification mecanique des attentes logiques F4/F5 (sans Jev)
2585f0e 2026-09-26T16:19:43+02:00 feat(e005): derive.py (sous-corpus a l'identique) et analyse.py (stdlib)
719d4c0 2026-09-26T16:16:47+02:00 feat(e005): corpus preregistre (32 cas, 38 questions) avant tout appel
```
Tests : `python3 -m unittest test_aggregate` (E001) → OK ; `verifie_logique.py` → 6/6 OK, et la mutation est détectée.

### GitHub
`gh auth status` OK → `gh issue comment 6` : https://github.com/malikkaraoui/EV-LLM/issues/6#issuecomment-5847030940

### Leçon candidate à la remontée (R5)
Une commande qui **affiche** une contrainte (écart ≥ 60 s) sans la **bloquer** ne la garantit pas : le lancement 3 est parti trop tôt. Il faut une garde bloquante testée sur son chemin d'échec, avant le premier usage. Leçon transverse ; elle n'a pas été écrite dans `vault/` (hors périmètre du mandat).

### Rituels de fin
- `vault/reprise/F05.md` écrit ; `vault/runtime/events.jsonl` : +1 ligne `RAPPORT_RENDU` (ts 2026-09-26T16:25:12+02:00, note de 125 caractères) ; dans `state.json`, seule la clé `windows.F05` a été modifiée. Assertion vérifiée : toutes les autres clés sont identiques et `next_mandat_id` = M0010 est toujours présent. Aucun de ces deux registres n'est committé.
- Commit main `df79ad6` (vault/reprise/F05.md seul), push OK, sans verrou d'index :
```
git ls-remote origin refs/heads/main
df79ad687146e91bb02d0de3372f19a6d87a4626	refs/heads/main
git ls-remote origin refs/heads/exp/e005-jev-hors-distribution
08d80f72265d36a56ad5e916c4097426bc93cc05	refs/heads/exp/e005-jev-hors-distribution
```
- Aucune tâche de fond vivante. Aucun `sleep`.

```
M0009
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
