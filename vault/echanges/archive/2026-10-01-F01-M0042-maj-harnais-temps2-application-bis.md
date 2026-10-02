---
date: 2026-10-01
tags: [harnais, maj, bootstrap, force-skill, v1.1.0]
session: F01
mandat: maj-harnais-temps2-application-bis
mandat_id: M0042
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM
branche: chore/harnais-v1.1.0
derniere_maj: 2026-10-01T16:43:42+0200
---

# M0042 — Mise à jour du harnais, TEMPS 2 (reprise après le STOP de M0041) : application (`--force-skill` puis `--maj`) sur la branche `chore/harnais-v1.1.0`

**Tu ne poses JAMAIS de question et tu n'attends JAMAIS de réponse.** Personne n'est devant l'écran. Si tu es sur le point de demander un arbitrage, c'est un **STOP** : écris dans ton rapport la question que tu aurais posée, les options que tu voyais et celle que tu aurais choisie avec sa raison, puis applique les rituels de fin. Un STOP propre est un rendu valable et laisse l'orchestrateur décider ; une question laisse un mandat mort. Vaut aussi pour une demande d'autorisation d'outil : n'insiste pas ; contourne par une commande plus simple répondant au même besoin (lecture seule, `git show`, `git -C`, chemin explicite dans le dépôt) ; si aucun contournement n'existe, c'est un STOP propre avec rapport — jamais une attente.

## Contexte (tout ce qu'il te faut est ici)

- Projet : `/Users/malik/Documents/EV-LLM`, branche principale `main`, dépôt GitHub **PUBLIC**. Tu travailles **à la racine**.
- TEMPS 1 (M0040, rapport archivé dans `vault/echanges/archive/2026-10-01-F01-M0040-maj-harnais-temps1-dry-run.md`) : `--maj --dry-run` a donné 5 POSE (`.gitignore`), 16 DEJA, 2 DIVERGE (`.claude/skills/orchestration-bureau/SKILL.md` et `references/gabarits.md`, jamais adaptés, identiques au canon v1.0.0), 0 OBSOLETE, 0 ECHEC, `GARDEE harnais.version reste v1.0.0`, rc 1.
- **Décision de Malik (01/10 14:36), verbatim** : « On applique, version du canon pour les 2 DIVERGE. Temps 2, dans cet ordre, rien d'autre : 1. bootstrap.sh "$PWD" --nom <projet.nom> --force-skill --dry-run → attendu : une ligne FORCE pour .claude/skills/orchestration-bureau, des POSE seulement sous ce dossier, le reste en DEJA ; tout autre écrit = STOP. 2. Même commande sans --dry-run. 3. bootstrap.sh "$PWD" --maj → rc 0 attendu, harnais.version = v1.1.0, plus aucun DIVERGE. 4. Commit des seuls fichiers touchés (skill + .gitignore + config/harnais.json pour la version), trailer du projet, push, colle git log -1 et ls-remote. rc 1 au point 3 = STOP avec la sortie collée. »
- **M0041 (rapport archivé `vault/echanges/archive/2026-10-01-F01-M0041-maj-harnais-temps2-application.md`)** : STOP propre à l'étape 1. La passe `--force-skill --dry-run` (rc 0) annonçait 1 FORCE, 2 POSE sous le skill, **5 POSE `.gitignore`**, 12 DEJA, 1 SAUTE (`vault/lecons/<projet>/.gitkeep (deja renomme)`), 1 IGNORE (hooks non posés). Rien écrit. La branche locale `chore/harnais-v1.1.0` existe (a3e9d07, sans commit propre, non poussée).
- **Décision de Malik (01/10 16:42) : « reprend »**, sur la question « on admet ces 5 lignes `.gitignore` aux étapes 1 et 2 ? » → les 5 POSE `.gitignore` ci-dessous, **et seulement elles, à l'identique**, sont admises aux étapes 1 et 2 ; SAUTE et IGNORE (aucun écrit) aussi. Tout autre écrit reste STOP. Elles sont attendues de toute façon : l'étape 4 de Malik committe `.gitignore`.
- **Décision de Malik (01/10, même échange)** : le hook `pre-push` refuse sur `main` tout commit qui touche un chemin hors `vault/` (`scripts/harnais-hooks/pre-push` l.163-172, décision #41). Donc le travail se fait **sur la branche `chore/harnais-v1.1.0` créée depuis `origin/main`, à la racine** ; on pousse la branche ; le doublage (R016) et le merge viendront dans des mandats séparés. **Tu ne merges PAS, tu ne pousses rien hors `vault/` sur `main`.**
- `~/.harnais/` (canon, superviseur, verrous, hooks) est **INTOUCHABLE** : seul `bootstrap.sh` est exécuté, avec exactement les commandes ci-dessous. Aucun autre script, aucune écriture.

## Règles communes (dépôt PUBLIC)

- Rien de secret dans ce que tu commits ou colles. `/Users/malik/Documents/EV-LLM/.env` : **ne JAMAIS le lire, l'afficher, le copier ni l'ouvrir.**
- Git en lecture : toujours `git --no-optional-locks`. `git add -- <chemins explicites>` puis `git commit ... -- <chemins explicites>`, jamais `-a`/`-A`. `.git/index.lock` présent au moment d'un commit : refais UNE fois ; toujours là → n'y touche pas, STOP partiel propre.
- Push `main` : seuls les commits qui ne touchent que `vault/`. Refus non-fast-forward : `git fetch origin`, `git merge --ff-only origin/main`, re-push, UNE fois ; sinon rapport.
- Jamais `sleep`, `stash`, `reset --hard`, `checkout -- .`, `update-ref`, `rebase`, `push --force`, `restore`. **Aucune tâche de fond vivante à ta sortie.** `rm -rf` seulement sous forme gardée `"${VAR:?}/${SOUS:?}"` (inutile ici).
- Ne touche jamais : `scripts/harnais-hooks/`, `.claude/worktrees/`, les `vault/echanges/*.md` autres que CE fichier, `~/.harnais/`. `.claude/skills/orchestration-bureau/`, `.gitignore` et `config/harnais.json` ne sont modifiés **que par `bootstrap.sh`**, jamais à la main.
- Commits signés du trailer `Co-Authored-By: Malik & Claude` (message en heredoc), jamais le trailer par défaut de l'outil.
- Étiquettes : [VÉRIFIÉ] / [HYPOTHÈSE]. Jamais un fait sans [VÉRIFIÉ].
- Le fichier `vault/runtime/entretien.lock.<n>` change de numéro tout seul (superviseur) : **ignore-le dans toute comparaison d'arbre**.

## Rituel de DÉBUT

`statut: en-cours` à la racine du frontmatter de CE fichier, avant tout.

## G0 — Branche de départ

```
cd /Users/malik/Documents/EV-LLM
git checkout main
git branch --show-current
```
Différent de `main` → **STOP**.

## Mission 0 — fichiers de l'orchestrateur, sur `main` (vault seul)

1. `git --no-optional-locks status --porcelain` → colle-le.
2. Committe **uniquement** ceux de ces chemins qui apparaissent modifiés ou nouveaux :
   - `vault/reprise/00_INDEX.md`
   - `vault/reprise/CARNET_DE_BORD.md`
   - `vault/echanges/archive/2026-10-01-F01-M0041-maj-harnais-temps2-application.md`
   ```
   git add -- <chemins présents>
   git commit -F - -- <mêmes chemins> <<'MSG'
   docs(vault): reconciliation orchestrateur -- index, archive F01/M0041 (avant M0042)

   Co-Authored-By: Malik & Claude
   MSG
   git push origin main
   git ls-remote origin refs/heads/main
   ```
   SHA distant = `git rev-parse HEAD`, sinon STOP. Rien à committer → note-le.

## Gardes de précondition — tout écart = STOP, rapport

- **G1** : `git --no-optional-locks fetch origin` ; `git --no-optional-locks rev-parse HEAD origin/main` identiques.
- **G2** : `git --no-optional-locks merge-base --is-ancestor 79c85591579f47ac538f7f4c82f09e245f2da421 origin/main && echo OK`.
- **G3 — propre hors tolérés** :
  ```
  git --no-optional-locks status --porcelain | grep -vE '^\?\? vault/echanges/F0[1-5]\.md$|^\?\? vault/runtime/journal/$|^\?\? vault/runtime/log/$|^\?\? vault/runtime/entretien\.lock\.[0-9]+$'
  ```
  doit être **vide** (colle aussi le status complet).
- **G4** : `grep '"version"' config/harnais.json` → `"version": "v1.0.0"` ; `grep '"nom"' config/harnais.json` → doit valoir `"ev-llm"`. Sinon STOP.
- **G5** : la branche locale existe et n'a aucun commit propre : `git --no-optional-locks rev-parse refs/heads/chore/harnais-v1.1.0` = `a3e9d071cff3d3b2adcf7e62c3e0e9e9b96850c8` ET `git --no-optional-locks merge-base --is-ancestor chore/harnais-v1.1.0 origin/main && echo ANCETRE` ; la branche distante n'existe pas : `git ls-remote origin refs/heads/chore/harnais-v1.1.0` vide. Sinon STOP.
- **G6** : `ls -la ~/.harnais/canon/bootstrap/bootstrap.sh` présent. Si `~/.harnais/canon` est un dépôt git : colle `git -C ~/.harnais/canon --no-optional-locks rev-parse HEAD` (lecture seule).

## Reprise de la branche (existante, mise à jour en avance rapide)

```
git checkout chore/harnais-v1.1.0
git branch --show-current          # doit afficher chore/harnais-v1.1.0, sinon STOP
git merge --ff-only origin/main    # refus = STOP
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)" && echo BRANCHE_A_JOUR   # sinon STOP
git --no-optional-locks status --porcelain | grep -v 'entretien\.lock' > "$TMPDIR/m0042-t0.txt"
```

## Étape 1 — `--force-skill` à blanc

```
NOM=$(sed -n 's/.*"nom": *"\([^"]*\)".*/\1/p' config/harnais.json | head -1); echo "NOM=$NOM"
test "$NOM" = "ev-llm" || echo STOP_NOM
sh ~/.harnais/canon/bootstrap/bootstrap.sh "$PWD" --nom "$NOM" --force-skill --dry-run ; echo "rc=$?"
```
- Colle la sortie **ENTIÈRE** et le `rc`.
- **Attendu (décisions Malik 14:36 et 16:42)** : une ligne `FORCE` pour `.claude/skills/orchestration-bureau` ; des `POSE` sous `.claude/skills/orchestration-bureau/` ; **en plus, exactement ces 5 `POSE` `.gitignore`, à l'identique** :
  ```
  POSE     .gitignore += **/vault/runtime/log/
  POSE     .gitignore += **/vault/runtime/journal/
  POSE     .gitignore += **/vault/runtime/entretien.lock*
  POSE     .gitignore += **/archive/*-F99-M0000-essai-equipement-*.md
  POSE     .gitignore += /vault/echanges/F99.md
  ```
  `SAUTE` et `IGNORE` admis (aucun écrit) ; tout le reste en `DEJA`. **Tout autre écrit annoncé** (une autre `POSE`, `MAJ`, `DIVERGE`, `ECHEC`, `OBSOLETE`, une écriture ailleurs) **= STOP** avant l'étape 2. Preuve : `grep -E '^  POSE ' <sortie> | grep -v '\.claude/skills/orchestration-bureau/'` doit donner **exactement** ces 5 lignes (compare-les). Compte les lignes par étiquette (donne la commande).
- Option refusée, `NOM` ≠ `ev-llm`, ou `rc` ≠ 0 → STOP (colle la sortie ; aucune autre option essayée).
- Preuve qu'il n'a rien écrit : `git --no-optional-locks status --porcelain | grep -v 'entretien\.lock' | diff "$TMPDIR/m0042-t0.txt" - && echo ARBRE_IDENTIQUE`. Différence → STOP.

## Étape 2 — `--force-skill` réel

```
sh ~/.harnais/canon/bootstrap/bootstrap.sh "$PWD" --nom "$NOM" --force-skill ; echo "rc=$?"
git --no-optional-locks status --porcelain
```
- Colle la sortie ENTIÈRE et le `rc`. `rc` ≠ 0 → STOP (ne committe rien, ne restaure rien).
- Contrôle : toute ligne du status (hors tolérés G3 et `entretien.lock`) doit être sous `.claude/skills/orchestration-bureau/` ou être `.gitignore` :
  ```
  git --no-optional-locks status --porcelain | grep -vE 'entretien\.lock|^\?\? vault/echanges/F0[1-5]\.md$|^\?\? vault/runtime/(journal|log)/$' | grep -vE ' (\.claude/skills/orchestration-bureau/.*|\.gitignore)$'
  ```
  Colle `git --no-optional-locks diff -- .gitignore` : seules les 5 lignes admises ajoutées.
  doit être **vide**. Sinon STOP (ne committe rien, ne restaure rien, décris).

## Étape 3 — `--maj`

```
sh ~/.harnais/canon/bootstrap/bootstrap.sh "$PWD" --maj ; echo "rc=$?"
grep '"version"' config/harnais.json
git --no-optional-locks status --porcelain
```
- Colle la sortie ENTIÈRE et le `rc`.
- **`rc` = 1 → STOP avec la sortie collée** (décision Malik). Tout `rc` ≠ 0 → STOP.
- Attendu : `rc=0`, `"version": "v1.1.0"`, **aucune ligne `DIVERGE`** ni `ECHEC` dans la sortie (le prouver par `grep -c`). Sinon STOP.
- Contrôle des fichiers touchés : hors tolérés, le status ne doit contenir **que** des chemins sous `.claude/skills/orchestration-bureau/`, `.gitignore` et `config/harnais.json` :
  ```
  git --no-optional-locks status --porcelain | grep -vE 'entretien\.lock|^\?\? vault/echanges/F0[1-5]\.md$|^\?\? vault/runtime/(journal|log)/$' | grep -vE ' (\.claude/skills/orchestration-bureau/.*|\.gitignore|config/harnais\.json)$'
  ```
  doit être **vide**. Sinon STOP (ne committe rien).
- Colle `git --no-optional-locks diff --stat` et `git --no-optional-locks diff -- .gitignore config/harnais.json`.

## Étape 4 — commit et push de la branche

```
git add -- .claude/skills/orchestration-bureau .gitignore config/harnais.json
git --no-optional-locks diff --cached --name-status      # colle : seuls ces chemins
git commit -F - -- .claude/skills/orchestration-bureau .gitignore config/harnais.json <<'MSG'
chore(harnais): mise a jour v1.0.0 -> v1.1.0 (skill orchestration-bureau du canon via --force-skill, puis --maj) [M0042]

Decision Malik 2026-10-01 : version du canon pour les 2 DIVERGE (SKILL.md, references/gabarits.md) ; 5 lignes .gitignore du canon admises (16:42).

Co-Authored-By: Malik & Claude
MSG
git log -1
git log -1 --format=%B
git push -u origin chore/harnais-v1.1.0
git ls-remote origin refs/heads/chore/harnais-v1.1.0
git rev-parse HEAD
```
- Colle tout. SHA distant = `git rev-parse HEAD`, sinon STOP. **Pas de merge, pas de push sur `main` de ce commit.**

## Retour sur `main` (la racine est partagée)

```
git checkout main
git branch --show-current     # main
```

## Rapport attendu (sous `## Rapport M0042`)

1. Étape 1 : décompte par étiquette, conformité à l'attendu (oui/non, ligne par ligne si non).
2. Étape 2 : fichiers écrits (status).
3. Étape 3 : `rc`, version, décompte, fichiers touchés, diff `.gitignore` + `config/harnais.json`.
4. Étape 4 : `git log -1`, `ls-remote`, liste `--name-status`.
5. Preuves G0–G6, Mission 0.
6. Pour le doublage R016 : tip complet de `chore/harnais-v1.1.0` et merge-base avec `origin/main`.

## Conditions STOP (récapitulatif)

G0–G6 ; étape 1 non conforme ou `rc` ≠ 0 ; étape 2 écrit hors du dossier du skill ou `rc` ≠ 0 ; étape 3 `rc` ≠ 0 (rc 1 en particulier), version ≠ v1.1.0, un DIVERGE/ECHEC, ou un fichier touché hors des trois chemins ; push refusé ; toute envie de poser une question. En cas de STOP après une écriture du bootstrap : **ne restaure rien, ne committe rien sur la branche**, laisse l'arbre tel quel, reviens sur `main` seulement si `git checkout main` passe sans conflit (sinon reste sur la branche et dis-le), et décris l'état exact (`git status`, `git diff --stat`).

## Rituels de FIN, dans l'ordre

1. Rapport appendé sous `## Rapport M0042` (preuves collées).
2. `vault/reprise/F01.md` réécrit (état + prochaine étape : « doublage R016 de `chore/harnais-v1.1.0` puis merge »).
3. Une ligne `vault/runtime/events.jsonl` (`src: "fenetre"`, `type: "RAPPORT_RENDU"`, `f: "F01"`, `mandat: "M0042"`, `note` ≤ 200 car.) + `windows.F01` dans `vault/runtime/state.json` — hors git. **state.json : lecture JSON → modification de la SEULE clé `windows.F01` → réécriture ; toutes les autres clés conservées. Vérifie que `next_mandat_id` est toujours présent.** `ts` = `TZ=Europe/Paris date +%Y-%m-%dT%H:%M:%S%:z`.
4. Sur `main` : commit de `vault/reprise/F01.md` (vault seul, `git commit -F - -- vault/reprise/F01.md`, trailer) + push + `git ls-remote origin refs/heads/main` collé.
5. Branche `chore/harnais-v1.1.0` poussée + `git ls-remote origin refs/heads/chore/harnais-v1.1.0` collé (déjà fait à l'étape 4 si succès).
6. Footer de statut, toute dernière ligne du rapport :
```
M0042
Implementation      ✅/❌
Tests               ✅/❌   (G0–G6 + contrôles étapes 1–3)
Commit              ✅/❌
Branch push         ✅/❌
Review              ❌
Merge main          ❌
Main push           ✅/❌   (vault seul)
TASK STATUS         <READY_FOR_INTEGRATION | BLOCKED>
PROJECT STATUS      NOT_INTEGRATED
```
7. `jobs` vide (aucune tâche de fond). **EN DERNIER GESTE : `statut: reponse-disponible`.**

## Rapport M0042

**Résultat : les 4 étapes de la décision de Malik sont faites. Le harnais du projet est en `v1.1.0` sur la branche `chore/harnais-v1.1.0`, commit `f7e74ae4a104da5fd97dc5ae7d37e7a5185d8cee`, poussée. Aucun STOP. Rien n'est mergé ; `main` ne porte que des commits `vault/`.**

### 1. Étape 1 — `--force-skill --dry-run`

[VÉRIFIÉ] `NOM=ev-llm`, `rc=0`. Conforme à l'attendu : oui.

Décompte (commande : `grep -E '^  [A-Z]+ ' "$OUT" | awk '{print $1}' | sort | uniq -c`) :

```
  12 DEJA
   1 FORCE
   1 IGNORE
   7 POSE
   1 SAUTE
```

Sortie entière :

```
### DRY-RUN : rien ne sera écrit ###
Canon  : /Users/malik/.harnais/canon   (version : v1.1.0)
Projet : /Users/malik/Documents/EV-LLM   (nom: ev-llm, branche: main, tz: Europe/Paris)

1. Convention -> .claude/skills/orchestration-bureau/
  FORCE    copie du projet écrasée par le canon
  POSE     .claude/skills/orchestration-bureau/references/gabarits.md
  POSE     .claude/skills/orchestration-bureau/SKILL.md

2. Scaffold vault -> vault/
  DEJA     vault/revues/.gitkeep
  DEJA     vault/hypotheses/.gitkeep
  DEJA     vault/reprise/CARNET_DE_BORD.md
  DEJA     vault/reprise/archive/index/.gitkeep
  DEJA     vault/reprise/00_INDEX.md
  DEJA     vault/reprise/CARTOGRAPHIE_BRANCHES.md
  DEJA     vault/runtime/README.md
  DEJA     vault/decisions/.gitkeep
  SAUTE    vault/lecons/<projet>/.gitkeep (deja renomme)
  DEJA     vault/lecons/transverse/.gitkeep
  DEJA     vault/echanges/archive/.gitkeep
  DEJA     vault/echanges/README.md

3. Config -> config/harnais.json
  DEJA     config/harnais.json existe -- conservée intacte (aucune fusion automatique).

4. .gitignore -> registres hors git
  POSE     .gitignore += **/vault/runtime/log/
  POSE     .gitignore += **/vault/runtime/journal/
  POSE     .gitignore += **/vault/runtime/entretien.lock*
  POSE     .gitignore += **/archive/*-F99-M0000-essai-equipement-*.md
  POSE     .gitignore += /vault/echanges/F99.md

5. Hooks git
  IGNORE   non posés (--hooks pour les poser : ils changent le comportement de git)

Fait. Suite :
  1. Relire et compléter '/Users/malik/Documents/EV-LLM/config/harnais.json'
     (au minimum : git.trailer, chemins.doctrine_projet, pieges_worktree)
  2. Superviseur : sh '/Users/malik/.harnais/canon/superviseur/install.sh' --ajouter '/Users/malik/Documents/EV-LLM'
  3. Ouvrir une session d'orchestration et lire
     .claude/skills/orchestration-bureau/SKILL.md en entier.
rc=0
```

- [VÉRIFIÉ] `grep -E '^  POSE ' "$OUT" | grep -v '\.claude/skills/orchestration-bureau/'` donne exactement les 5 lignes admises : `diff` contre les 5 lignes du mandat écrites dans un fichier → vide, `CINQ_POSE_IDENTIQUES`.
- [VÉRIFIÉ] Aucune ligne `MAJ`, `DIVERGE`, `ECHEC`, `OBSOLETE`.
- [VÉRIFIÉ] Rien écrit : `ARBRE_IDENTIQUE` (diff du status contre `$TMPDIR/m0042-t0.txt`).

### 2. Étape 2 — `--force-skill` réel

[VÉRIFIÉ] `rc=0`. Sortie identique à celle de l'étape 1, sans la ligne `### DRY-RUN ###` (1 FORCE, 7 POSE, 12 DEJA, 1 SAUTE, 1 IGNORE).

Status après l'étape 2 :

```
 M .claude/skills/orchestration-bureau/SKILL.md
 M .claude/skills/orchestration-bureau/references/gabarits.md
 M .gitignore
?? vault/echanges/F01.md
?? vault/echanges/F02.md
?? vault/echanges/F03.md
?? vault/echanges/F04.md
?? vault/echanges/F05.md
```

- [VÉRIFIÉ] Contrôle hors périmètre (filtre du mandat) : vide.
- [VÉRIFIÉ] `git diff -- .gitignore` : seules les 5 lignes admises ajoutées (diff collé au point 3, inchangé entre les deux étapes).
- [VÉRIFIÉ] Dès l'étape 2, `vault/runtime/journal/`, `log/` et `entretien.lock.*` disparaissent du status de la branche : les nouvelles lignes `.gitignore` font leur effet.

### 3. Étape 3 — `--maj`

[VÉRIFIÉ] `rc=0`, `"version": "v1.1.0"`, `DIVERGE=0 ECHEC=0` (`grep -c`). Décompte : `19 DEJA`, `1 MAJ`.

Sortie entière :

```
Canon  : /Users/malik/.harnais/canon   (version : v1.1.0)
Projet : /Users/malik/Documents/EV-LLM   (nom: ev-llm, version : v1.0.0)

1. Convention -> .claude/skills/orchestration-bureau/
  DEJA     .claude/skills/orchestration-bureau/SKILL.md
  DEJA     .claude/skills/orchestration-bureau/references/gabarits.md

2. Scaffold vault -> vault/   (un fichier existant est une donnée du projet : jamais comparé)
  DEJA     vault/decisions/.gitkeep
  DEJA     vault/echanges/README.md
  DEJA     vault/echanges/archive/.gitkeep
  DEJA     vault/hypotheses/.gitkeep
  DEJA     vault/lecons/ev-llm/.gitkeep
  DEJA     vault/lecons/transverse/.gitkeep
  DEJA     vault/reprise/00_INDEX.md
  DEJA     vault/reprise/CARNET_DE_BORD.md
  DEJA     vault/reprise/CARTOGRAPHIE_BRANCHES.md
  DEJA     vault/reprise/archive/index/.gitkeep
  DEJA     vault/revues/.gitkeep
  DEJA     vault/runtime/README.md

3. Hooks git -> scripts/harnais-hooks/
  DEJA     scripts/harnais-hooks/README.md
  DEJA     scripts/harnais-hooks/commit-msg
  DEJA     scripts/harnais-hooks/pre-commit
  DEJA     scripts/harnais-hooks/pre-push

4. .gitignore -> registres hors git
  DEJA     fragment déjà présent (aucune ligne manquante)

5. Version -> config/harnais.json (harnais.version ; rien d'autre n'est touché)
  MAJ      harnais.version v1.0.0 -> v1.1.0
rc=0
```

Fichiers touchés ([VÉRIFIÉ] contrôle hors périmètre vide) — `git diff --stat` :

```
 .claude/skills/orchestration-bureau/SKILL.md       | 42 ++++++++++++++++++++--
 .../orchestration-bureau/references/gabarits.md    | 26 ++++++++++++--
 .gitignore                                         |  5 +++
 config/harnais.json                                |  2 +-
 4 files changed, 69 insertions(+), 6 deletions(-)
```

`git diff -- .gitignore config/harnais.json` :

```
diff --git a/.gitignore b/.gitignore
index c8ee5e1..985e883 100644
--- a/.gitignore
+++ b/.gitignore
@@ -44,3 +44,8 @@ research/experiments/*/results/**/raw.jsonl
 # Bruit local : fichiers macOS et worktrees des fenêtres (jamais versionnés)
 .DS_Store
 .claude/worktrees/
+**/vault/runtime/log/
+**/vault/runtime/journal/
+**/vault/runtime/entretien.lock*
+**/archive/*-F99-M0000-essai-equipement-*.md
+/vault/echanges/F99.md
diff --git a/config/harnais.json b/config/harnais.json
index cd0b7e7..ec3db7b 100644
--- a/config/harnais.json
+++ b/config/harnais.json
@@ -1,6 +1,6 @@
 {
   "harnais": {
-    "version": "v1.0.0"
+    "version": "v1.1.0"
   },
   "projet": {
     "nom": "ev-llm",
```

**Preuve indépendante du bootstrap (hors mandat, lecture seule)** — le `DEJA` de `--maj` vient du même script qui a posé les fichiers ; je l'ai recoupé par empreintes SHA-256 (16 premiers caractères) :

```
0966b873504ae522  ~/.harnais/canon/SKILL-orchestration-maison/SKILL.md
5e5133e5684af7b4  ~/.harnais/canon/SKILL-orchestration-maison/references/gabarits.md
f68224766f1f19ca  ~/.harnais/canon/.claude/skills/orchestration-bureau/SKILL.md
5e5133e5684af7b4  ~/.harnais/canon/.claude/skills/orchestration-bureau/references/gabarits.md
0966b873504ae522  (projet) .claude/skills/orchestration-bureau/SKILL.md
5e5133e5684af7b4  (projet) .claude/skills/orchestration-bureau/references/gabarits.md
```

- [VÉRIFIÉ] Le projet est identique à `SKILL-orchestration-maison/`, la source que `bootstrap.sh` copie (l.582 et l.697).
- [VÉRIFIÉ] **Écart dans le canon lui-même, à signaler à Malik** : `~/.harnais/canon/.claude/skills/orchestration-bureau/SKILL.md` (la copie que le dépôt du canon s'installe à lui-même) diffère de `SKILL-orchestration-maison/SKILL.md`. Il lui manque le « PREMIER GESTE » ToolSearch, la réserve `F99`/`M0000` et le §14 (guichet) ; il porte en plus deux lignes « cmux muet ou lent : `CMUX_LENT` … » absentes de la source. Je n'y ai pas touché (`~/.harnais/` intouchable). Sans effet sur ce projet.
- [HYPOTHÈSE] Les deux lignes `CMUX_LENT` sont soit un ajout fait dans la mauvaise copie (jamais reporté dans la source), soit un retrait volontaire de la source. Non tranché.

### 4. Étape 4 — commit et push de la branche

`git diff --cached --name-status` :

```
M	.claude/skills/orchestration-bureau/SKILL.md
M	.claude/skills/orchestration-bureau/references/gabarits.md
M	.gitignore
M	config/harnais.json
```

`git log -1` :

```
commit f7e74ae4a104da5fd97dc5ae7d37e7a5185d8cee
Author: Malik <karaoui.malik@gmail.com>
Date:   Thu Oct 1 16:44:56 2026 +0200

    chore(harnais): mise a jour v1.0.0 -> v1.1.0 (skill orchestration-bureau du canon via --force-skill, puis --maj) [M0042]

    Decision Malik 2026-10-01 : version du canon pour les 2 DIVERGE (SKILL.md, references/gabarits.md) ; 5 lignes .gitignore du canon admises (16:42).

    Co-Authored-By: Malik & Claude
```

Push et `ls-remote` :

```
 * [new branch]      chore/harnais-v1.1.0 -> chore/harnais-v1.1.0
rc_push=0
f7e74ae4a104da5fd97dc5ae7d37e7a5185d8cee	refs/heads/chore/harnais-v1.1.0     (git ls-remote origin)
f7e74ae4a104da5fd97dc5ae7d37e7a5185d8cee                                    (git rev-parse HEAD)
```

- [VÉRIFIÉ] SHA distant = `HEAD`. `origin/main` inchangé par ce push (`fbdd03a`). Pas de merge.
- [VÉRIFIÉ] Retour sur `main` : `git checkout main` rc 0, `git branch --show-current` = `main`, `config/harnais.json` y est toujours en `v1.0.0`.

### 5. Preuves G0–G6, Mission 0

- **G0** [VÉRIFIÉ] `git branch --show-current` = `main`.
- **Mission 0** [VÉRIFIÉ] status initial : ` M vault/reprise/00_INDEX.md`, `?? vault/echanges/archive/2026-10-01-F01-M0041-maj-harnais-temps2-application.md` (plus les tolérés). `CARNET_DE_BORD.md` non modifié, donc non committé. Commit `fbdd03a6f5a8ee1a1719a95a6a307c05889b2a0c` (2 fichiers, 414 insertions), push `79c8559..fbdd03a main -> main`, `ls-remote origin refs/heads/main` = `fbdd03a6f5a8ee1a1719a95a6a307c05889b2a0c` = `HEAD`.
- **G1** [VÉRIFIÉ] fetch rc 0 ; `HEAD` = `origin/main` = `fbdd03a6f5a8ee1a1719a95a6a307c05889b2a0c`.
- **G2** [VÉRIFIÉ] `79c8559…` ancêtre d'`origin/main` : `OK`.
- **G3** [VÉRIFIÉ] status complet : `?? vault/echanges/F01.md` à `F05.md`, `?? vault/runtime/entretien.lock.877`, `?? vault/runtime/journal/`, `?? vault/runtime/log/` ; filtré : vide.
- **G4** [VÉRIFIÉ] `"version": "v1.0.0"`, `"nom": "ev-llm",`.
- **G5** [VÉRIFIÉ] `refs/heads/chore/harnais-v1.1.0` = `a3e9d071cff3d3b2adcf7e62c3e0e9e9b96850c8`, `ANCETRE`, `ls-remote` de la branche vide.
- **G6** [VÉRIFIÉ] `-rwxr-xr-x 1 malik staff 51455 1 oct. 12:34 ~/.harnais/canon/bootstrap/bootstrap.sh` ; canon `HEAD` = `e506f6dcd556526168092c2b47920f51b0806ca8`.
- **Reprise de la branche** [VÉRIFIÉ] `git merge --ff-only origin/main` : `Updating a3e9d07..fbdd03a`, rc 0, `BRANCHE_A_JOUR`.

### 6. Pour le doublage R016

- Tip de `chore/harnais-v1.1.0` : `f7e74ae4a104da5fd97dc5ae7d37e7a5185d8cee` (local = distant).
- Merge-base avec `origin/main` : `fbdd03a6f5a8ee1a1719a95a6a307c05889b2a0c` (un seul commit à doubler, 4 fichiers).
- À rejouer par le doubleur : les deux empreintes du skill contre `~/.harnais/canon/SKILL-orchestration-maison/`, et `bootstrap.sh "$PWD" --maj --dry-run` sur la branche (attendu : tout `DEJA`, rc 0).
- Après le merge, les rapports suivants n'auront plus à tolérer `vault/runtime/journal/`, `log/` ni `entretien.lock.*` dans G3 : ils seront ignorés par git.

### Écarts et notes

- Mon contrôle par empreintes a été lancé dans la même commande que le commit ; le commit était donc fait avant que je lise son résultat. J'ai suspendu le push le temps de lever l'écart (la copie comparée d'abord était la mauvaise : `canon/.claude/skills/`), puis poussé une fois l'identité avec la vraie source établie.
- `date +%:z` n'existe pas sur macOS (`date` BSD rend `:z` littéral). `ts` construit par `date +%Y-%m-%dT%H:%M:%S%z | sed 's/\(..\)$/:\1/'`.
- `sync-vaults.sh` (remontée vers le vault central) non lancé : hors des commandes du mandat.
- Leçon candidate transverse (R5) consignée dans `vault/reprise/F01.md` : lire dans le script de pose quel exemplaire il copie avant de comparer « au canon » ; lancer un recoupement avant le geste qu'il doit autoriser.

### Rituels de fin

- [VÉRIFIÉ] `vault/reprise/F01.md` réécrit (état + prochaine étape : doublage R016 de `chore/harnais-v1.1.0` puis merge).
- [VÉRIFIÉ] `events.jsonl` : une ligne `RAPPORT_RENDU` (`ts` `2026-10-01T16:51:42+02:00`, note 162 car.), fichier entier relu comme JSONL valide. `state.json` : seule `windows.F01` modifiée (`RAPPORT_RENDU`, `M0042`, tip `f7e74ae`) ; égalité des autres clés avant/après vérifiée par assertion ; `next_mandat_id` = `M0043` toujours présent.
- [VÉRIFIÉ] Commit de la reprise sur `main` (vault seul, 1 fichier) et push :

```
[main c0d7b76] docs(vault): reprise F01 -- M0042 rendu (harnais v1.1.0 sur chore/harnais-v1.1.0 f7e74ae, pousse ; a doubler R016 puis merger)
M	vault/reprise/F01.md
   fbdd03a..c0d7b76  main -> main
c0d7b762652ddda2ab9c61dff12beab09405d641	refs/heads/main                    (git ls-remote origin)
c0d7b762652ddda2ab9c61dff12beab09405d641                                   (git rev-parse HEAD)
f7e74ae4a104da5fd97dc5ae7d37e7a5185d8cee	refs/heads/chore/harnais-v1.1.0    (git ls-remote origin)
```

- [VÉRIFIÉ] Status final sur `main` : uniquement les tolérés (`vault/echanges/F01.md` à `F05.md`, `entretien.lock.907`, `journal/`, `log/`). `jobs` : vide.
- Merge-base de la branche avec `origin/main` inchangé après ce push : `fbdd03a6f5a8ee1a1719a95a6a307c05889b2a0c` (`main` a un commit vault de plus, `c0d7b76`).

```
M0042
Implementation      ✅
Tests               ✅   (G0–G6 + contrôles étapes 1–3)
Commit              ✅
Branch push         ✅
Review              ❌
Merge main          ❌
Main push           ✅   (vault seul)
TASK STATUS         READY_FOR_INTEGRATION
PROJECT STATUS      NOT_INTEGRATED
```

