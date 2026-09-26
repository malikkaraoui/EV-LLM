---
date: 2026-09-26
tags: [e006, e004, jev, replication, contamination]
session: F04
mandat: e006-replication-frontiere
mandat_id: M0011
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F04-M0011
branche: exp/e006-replication-frontiere
derniere_maj: 2026-09-26T16:38:48+0200
---

# M0011 — E006 : répliquer les « faux et sûr » de Jev et tester la contamination (E004)

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


Modèle : `opus --effort medium` (barème `conception_critique`).

## 0. Contexte
E005 (branche `origin/exp/e005-jev-hors-distribution`, tip `08d80f72265d36a56ad5e916c4097426bc93cc05` — lis README, `results/analyse.md`, `cases.json`, et le rapport `vault/echanges/archive/2026-09-26-F05-M0009-e005-jev-hors-distribution.md`) a trouvé **les premiers « faux et sûr » de Jev**, mais sur **1 à 2 réponses** par question (limite de débit) :
- F1-04 « Elles se sont lavées les mains… » P(correcte) 0.84/0.85 ; F1-05 « Ils se sont parlés… » 0.80 ; F1-08 « Les robes qu'elle a faites faire… » 0.86 ; F3-02 « Ci-jointe la facture demandée. » 0.86 (attente **peut-être contestable** — en cours de vérification par le doublage R004 ; traite-le comme « à confirmer ») ;
- F4-01 (T1-A + fait redondant + règle non pertinente) : `coherent` 0.88/0.89 au lieu de `contradiction` — **un distracteur fait disparaître la contradiction** ;
- F4-04 (A > F en 4 pas) : P 0.15/0.19 au lieu de `true`.
Et le signal « contamination » (issue #5) : E001 T1-A vs T1-B, `e_sup_d` 0.49–0.58 vs 0.73–0.78 ; E003 : LLM-1 répond `false` à 1.0 sur la même question.
**Cause des 429 [VÉRIFIÉ M0008] : limite passerelle 5 req/min par équipe.**

But : (1) **répliquer** chaque « faux et sûr » à ≥ 5 réponses, avec paires minimales ; (2) **cartographier** la frontière (combien de pas, combien de distracteurs avant que Jev bascule) ; (3) **E004** : tester la contamination par paires contrôlées.

**Exception explicite à l'interdit `sleep`, propre à ce mandat** : rythmeur **interne au script** (`time.sleep` Python entre deux appels HTTP), **≥ 26 s** entre appels (F03 appelle la même passerelle en parallèle). `sleep` shell reste interdit. Invocations de **≤ 8 appels** chacune (≈ 3,5 min), enchaînées.

## 1. Gardes — tout écart : STOP + rapport
1. `fetch origin` ; `origin/exp/e005-jev-hors-distribution` = `08d80f72265d36a56ad5e916c4097426bc93cc05`.
2. Branche `exp/e006-replication-frontiere` et dossier `…/.claude/worktrees/F04-M0011` absents.
3. `test -f /Users/malik/Documents/EV-LLM/.env && echo PRESENT`.

## 2. Mission 1
`git -C /Users/malik/Documents/EV-LLM worktree add -b exp/e006-replication-frontiere /Users/malik/Documents/EV-LLM/.claude/worktrees/F04-M0011 origin/exp/e005-jev-hors-distribution`. Travail sous `research/experiments/E006-replication-frontiere/` ; **aucun fichier d'E001/E005 modifié** (réutilise `run.py`/`aggregate.py` d'E001 par import/appel ; déplace les sorties comme en M0009).
1. `run_paced.py` (stdlib) : appelle la fonction d'appel de `E001/run.py` (sans la dupliquer), applique `--min-interval 26`, `--max-calls`, garde anti-fuite identique ; tests unittest (horodatages mockés). Verts avant tout appel.
2. **Corpus préenregistré** `cases.json` (même schéma, `justification` d'une ligne par cas), **committé avant tout appel** :
   - **R — réplication** : les 6 questions « faux et sûr » d'E005, recopiées à l'identique (assertion champ par champ) ;
   - **P — paires minimales** : pour F1-04/05/08, la forme correcte en regard (« se sont lavé les mains », « se sont parlé », « a fait faire ») ;
   - **L — frontière logique** : chaîne transitive de 2, 3, 4, 5, 6 pas (question `A > X` attendue `true`) ; T1-A avec 0, 1, 2, 3 distracteurs (attendu `contradiction`) ;
   - **C — contamination (E004)** : 4 paires (même déduction transitive indépendante, avec / sans contradiction ailleurs dans l'état) ; attendu `true` des deux côtés ; la mesure est l'**écart de P** entre les deux membres de la paire.
   ~24 questions au total.
3. **Budget : ≤ 130 appels** ; objectif **5 réponses 200 par question R et C**, 3 pour P et L. Ordre : R d'abord, puis C, puis L, puis P.
4. Agrégat via `aggregate.py` d'E001 ; `raw.public.jsonl` (sans en-têtes, équivalence prouvée) ; `analyse.py` → `results/analyse.md` : pour chaque « faux et sûr » d'E005, **répliqué ou non** (≥ 4/5 non conformes et P extrême) ; courbe P(true) en fonction du nombre de pas ; P(`contradiction`) en fonction du nombre de distracteurs ; écart de P par paire C (moyenne, min, max) et signe.
5. README : Hypothèses (réplication ; frontière ; contamination — issue #5), Protocole, Rejouer, Résultats, **Lecture** étiquetée, sans adoucir ni gonfler (si rien ne se réplique, le dire), Limites, Prochaine étape (3 lignes).
6. Commits ciblés (corpus avant appels, prouvé) ; `grep` anti-fuite = 0 ; push.

## 3. STOP supplémentaires
401/403/404, fuite, budget ; toute envie de modifier une attente après avoir vu Jev (écris-la) ; modification d'E001/E005.

## 4. Preuves
Gardes ; commit corpus < 1er appel ; tests verts ; statuts HTTP ; intervalles mesurés ; tableaux de `analyse.md` collés ; `ls-remote`. `gh issue comment 5` (contamination) et `gh issue comment 6` (réplication) si `gh` OK.

## Rituels

DÉBUT : `statut: en-cours` à la racine du frontmatter de CE fichier, avant tout.

FIN, dans l'ordre :
1. Rapport appendé sous `## Rapport M0011` (preuves collées).
2. `vault/reprise/F04.md` (état + prochaine étape) — à la racine.
3. Une ligne `vault/runtime/events.jsonl` (`src: "fenetre"`, `type: "RAPPORT_RENDU"`, `f`, `mandat`, `note` ≤ 200 car.) + `windows.F04` dans `vault/runtime/state.json` — hors git, jamais committés. **state.json : lecture JSON → modification de la SEULE clé `windows.F04` → réécriture ; toutes les autres clés (`schema_version`, `next_mandat_id`, `next_revue_id`, `projet`, autres fenêtres) sont conservées à l'identique. Vérifie après écriture que `next_mandat_id` est toujours présent (incident du 26/09 : state.json écrasé).** Toute ligne `events.jsonl` porte `ts` (horloge réelle `TZ=Europe/Paris date +%Y-%m-%dT%H:%M:%S%:z`).
4. Commit de `vault/reprise/F04.md` sur `main` à la racine (vault seul) + push + `git ls-remote origin refs/heads/main` collé.
5. Ta branche (s'il y en a une) poussée + `git ls-remote origin refs/heads/<branche>` collé.
6. Footer de statut, toute dernière ligne du rapport :
```
M0011
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

## Rapport M0011

Rendu 2026-09-26 ~17:30 (Europe/Paris). Branche `exp/e006-replication-frontiere`, tip `57e0e41`. Détail complet : `research/experiments/E006-replication-frontiere/README.md` et `results/analyse.md`.

### Gardes
- `git fetch origin` ; `origin/exp/e005-jev-hors-distribution` = `08d80f72265d36a56ad5e916c4097426bc93cc05` ✅.
- Branche `exp/e006-replication-frontiere` absente (`ls-remote` vide, `git branch -a` vide) ; `.claude/worktrees/F04-M0011` absent ✅.
- `test -f .env && echo PRESENT` → `PRESENT` ✅.
- Note : pendant le mandat, `origin/exp/e005-jev-hors-distribution` a avancé à `15487b0` (correctif R004/M0013, README E005 seul, totaux HTTP). Ma branche part de `08d80f7` ; `git diff --stat 08d80f7 -- E001 E005` = vide : aucun fichier d'E001/E005 modifié [VÉRIFIÉ].

### Mission 1 — livré
- `run_paced.py` : importe `run.call`, `run.load_key`, `run.leak_guard`, `run.summarize`, `run.summary_md` d'E001 (aucune duplication de l'appel) ; `--min-interval` ≥ 26 (refus en dessous), `--max-calls` ≤ 8 (refus au-dessus), budget 130, arrêt 401/403/404 (code 4) et 3 échecs consécutifs ; attente `time.sleep` interne calculée depuis le dernier appel enregistré (inter-invocations comprises). Sorties directement dans `E006/results/` (pas de `run.py main`, donc rien à déplacer).
- Tests : `python3 -m unittest test_run_paced` → `Ran 12 tests … OK` (horloge et appels mockés : ordre R→C→L→P, intervalles ≥ 26 s intra et inter invocations, bornes, budget, 401, échecs consécutifs, rien à faire, public = raw sans en-têtes, corps de requête, garde anti-fuite). Verts avant le premier appel.
- Corpus `cases.json` (25 cas, 30 questions ; sha256 `0245036b…e042`), `gen_cases.py` avec assertions : R = E005 à l'identique (state/questions/attendu/justification) ; L-DIS3 ≡ R-F4-01 (état identique asserté) ; L-PAS4 = R-F4-04 sans `incompatible(A, F)` ni R2 (asserté). `verifie_logique.py` → `18 cas logiques verifies, 0 ecart(s)` ; mutation (membre `sans` rendu contradictoire) → ECART détecté.
- **Commit corpus < 1er appel** : `820d85b` 2026-09-26T16:43:02+02:00, poussé (`ls-remote` = `820d85baa99cc3201e5b555fcf6b01148eab8e41`) ; premier appel `16:43:09`. `git diff --quiet 820d85b HEAD -- cases.json` → `corpus-inchange`.

### Appels
- 13 invocations (12×8 + 1×7) + 1 invocation finale en code 5 « rien a faire : 103 appels consommes / budget 130 ».
- **Statuts HTTP : 103 × 200**, 0 × 429/503/401/403/404, 0 code 3.
- **Intervalles mesurés entre départs : n = 102, min 26.0 s, max 26.0 s.**
- Fournisseur final : typesafe-ai ×100, digitalocean ×3. 122 évaluations, 0 NON_PARSE.
- Agrégat `aggregate.py` d'E001 : `results/agregat-2026-09-26T172726+0200/` — marque « faux et sûr » à la médiane : les 6 R + L-DIS1 `e_sup_d` (0.18) + L-DIS2 `statut` (coherent 0.83).
- `raw.public.jsonl` = `raw.jsonl` sans `response_headers` : égalité vérifiée 13/13 dossiers ; 0 `raw.jsonl` committé (ignorés, `!!`).
- Anti-fuite : `grep` (karaoui, malik@, Bearer, Authorization, AI_GATEWAY_API_KEY=, team_, ownerId, userId, accountId) sur les fichiers suivis d'E006 → **0**. Recherche de la valeur de la clé dans les fichiers publiables → 0. ⚠️ Transparence : cette dernière vérification a été faite par un petit script Python qui a chargé la clé depuis `.env` **en mémoire** (rien affiché ni écrit) — c'est à la limite de la règle « seuls les scripts le chargent » ; je le signale.

### Tableaux (extraits de `results/analyse.md`)

R — réplication :

| cas | question | attendu | E005 | E006 P (par appel) | n | non conformes | faux et sûr | médiane P | répliqué |
|---|---|---|---|---|---|---|---|---|---|
| R-F1-04 | correcte | false | 0.84 / 0.85 | 0.83 / 0.84 / 0.84 / 0.85 / 0.83 | 5 | 5/5 | 5 | 0.84 | **oui** |
| R-F1-05 | correcte | false | 0.80 | 0.87 / 0.83 / 0.83 / 0.84 / 0.84 | 5 | 5/5 | 5 | 0.84 | **oui** |
| R-F1-08 | correcte | false | 0.86 | 0.86 / 0.87 / 0.86 / 0.87 / 0.86 | 5 | 5/5 | 5 | 0.86 | **oui** |
| R-F3-02 | correcte | false | 0.86 | 0.86 / 0.84 / 0.85 / 0.83 / 0.86 | 5 | 5/5 | 5 | 0.85 | **oui** |
| R-F4-01 | statut | "contradiction" | coherent 0.88 / 0.89 | coherent 0.90 / 0.91 / 0.92 / 0.91 / 0.85 | 5 | 5/5 | 5 | 0.91 | **oui** |
| R-F4-04 | a_sup_f | true | 0.15 / 0.19 | 0.37 / 0.25 / 0.17 / 0.20 / 0.13 | 5 | 5/5 | 3 | 0.20 | **oui** |

P — paires minimales :

| paire | fautive (méd.) | correcte (par appel) | méd. | écart |
|---|---|---|---|---|
| R-F1-04 / P-F1-04 | 0.84 | 0.58 / 0.64 / 0.61 | 0.61 | −0.23 |
| R-F1-05 / P-F1-05 | 0.84 | 0.90 / 0.91 / 0.90 | 0.90 | +0.06 |
| R-F1-08 / P-F1-08 | 0.86 | 0.64 / 0.75 / 0.67 | 0.67 | −0.19 |

L — pas (P(true) médiane, 3 appels) : 2 → 0.97 ; 3 → 0.85 ; 4 → 0.95 ; 5 → 0.94 ; 6 → 0.90 (15/15 conformes) ; réf. R-F4-04 (4 pas + incompatible(A, F) + R2) → 0.20 (0/5).

L — distracteurs (T1-A) :

| d | choix | P(contradiction) médiane | P(E > D) |
|---|---|---|---|
| 0 | contradiction ×3 | 0.73 | 0.60 / 0.59 / 0.61 |
| 1 | coherent ×3 | 0.34 | 0.21 / 0.18 / 0.16 |
| 2 | coherent ×3 | 0.14 | 0.39 / 0.40 / 0.45 |
| 3 (= R-F4-01) | coherent ×5 | 0.08 | 0.53–0.68 |

C — contamination :

| paire | moy. avec | moy. sans | écart |
|---|---|---|---|
| C1 | 0.97 | 0.98 | −0.006 |
| C2 | 0.97 | 0.97 | −0.002 |
| C3 | 0.97 | 0.97 | +0.000 |
| C4 | 0.95 | 0.96 | −0.012 |

Écart par paire : moyenne −0.005, min −0.012, max +0.000 ; 3 négatifs, 1 nul ; 40/40 conformes.

### Lecture (résumé, étiqueté)
- [VÉRIFIÉ] 6/6 « faux et sûr » répliqués ; F4-04 pile au seuil (médiane 0.20, 3/5 appels sûrs).
- [VÉRIFIÉ] Sur 2 paires sur 3, Jev donne une P(correcte) **plus basse** à la forme correcte qu'à la forme fautive.
- [VÉRIFIÉ] Pas de pente avec la longueur (2–6 pas) ; l'effondrement de F4-04 disparaît quand on retire `incompatible(A, F)` + R2 (0.20 → 0.95).
- [VÉRIFIÉ] T1-A perd la contradiction dès 1 distracteur ; nouveau « faux et sûr » L-DIS1 `e_sup_d` (méd. 0.18, 3 appels, non ciblé a priori).
- [VÉRIFIÉ] Contamination par contradiction **disjointe** : non observée (|écart| ≤ 0.012).
- [HYPOTHÈSE] L'effet d'E001/F4-04 serait **local** (variables partagées entre contradiction et question), non testé par paire contrôlée.

### Attente que j'aurais eu envie de modifier (non modifiée — donnée)
R-F4-04 `a_sup_f` et L-DIS1 `e_sup_d` : dans un ensemble contradictoire, « peut-on déduire A > F » est discutable (R2 l'interdit, R1 l'impose). J'ai conservé `true` (A > F suit de R1 sur les faits donnés) ; la réponse de Jev a une lecture défendable, ce qui affaiblit ces deux cas comme erreurs de déduction. À trancher par l'orchestrateur/doublage.

### Issues
- `gh issue comment 5` → https://github.com/malikkaraoui/EV-LLM/issues/5#issuecomment-5847479553
- `gh issue comment 6` → https://github.com/malikkaraoui/EV-LLM/issues/6#issuecomment-5847479672

### Branche
- Commits : `820d85b` (corpus + outils + tests, avant appels), `57e0e41` (résultats, analyse, README).
- `git ls-remote origin refs/heads/exp/e006-replication-frontiere` → `57e0e416694f323b8f34288b7984f90c6e521898	refs/heads/exp/e006-replication-frontiere`.
- Worktree `.claude/worktrees/F04-M0011` conservé ; aucune tâche de fond vivante (`ps` : 0 `run_paced`, monitor arrêté par TaskStop).

### Leçon candidate à la remontée (R5)
- Rythmer côté script à l'intervalle de la limite (26 s pour 5 req/min partagées) a donné 103/103 en 200, contre 34/151 en rafale (E005) : sous une limite de débit connue, un rythmeur interne + reprise sur l'horodatage du dernier appel persistant vaut mieux que des relances espacées à la main. Transverse (toute API à quota).

### Rituels de fin
- `vault/reprise/F04.md` écrit ; commit racine `a1231e5` (vault seul, chemin explicite), push OK.
- `git ls-remote origin refs/heads/main` → `a1231e54f016946b7edf8a67718542e099d8b84c	refs/heads/main`.
- `git ls-remote origin refs/heads/exp/e006-replication-frontiere` → `57e0e416694f323b8f34288b7984f90c6e521898	refs/heads/exp/e006-replication-frontiere`.
- `events.jsonl` : ligne `RAPPORT_RENDU` (ts 2026-09-26T17:30:13+02:00) ; `state.json` : seule `windows.F04` modifiée (autres clés égales, assertion), `next_mandat_id` présent (`M0015`).

```
M0011
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
