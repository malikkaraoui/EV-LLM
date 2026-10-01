---
date: 2026-10-01
tags: [harnais, maj, bootstrap, dry-run, v1.1.0]
session: F01
mandat: maj-harnais-temps1-dry-run
mandat_id: M0040
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM
branche: main
derniere_maj: 2026-10-01T14:15:50+0200
---

# M0040 — Mise à jour du harnais, TEMPS 1 : passe À BLANC (`--maj --dry-run`), rien n'est appliqué

**Tu ne poses JAMAIS de question et tu n'attends JAMAIS de réponse.** Personne n'est devant l'écran. Si tu es sur le point de demander un arbitrage, c'est un **STOP** : écris dans ton rapport la question que tu aurais posée, les options que tu voyais et celle que tu aurais choisie avec sa raison, puis applique les rituels de fin. Un STOP propre est un rendu valable et laisse l'orchestrateur décider ; une question laisse un mandat mort. Vaut aussi pour une demande d'autorisation d'outil : n'insiste pas ; contourne par une commande plus simple répondant au même besoin (lecture seule, `git show`, `git -C`, chemin explicite dans le dépôt) ; si aucun contournement n'existe, c'est un STOP propre avec rapport — jamais une attente.

## Contexte (tout ce qu'il te faut est ici)

- Projet : `/Users/malik/Documents/EV-LLM`, branche principale `main`, dépôt GitHub **PUBLIC**. Tu travailles **à la racine**, sans worktree ni branche.
- Version actuelle du harnais : `config/harnais.json` → `"harnais": { "version": "v1.0.0" }` (vu par l'orchestrateur le 01/10 à 14:14). Version cible du canon : **v1.1.0** (annoncée par Malik).
- Ce mandat est le TEMPS 1 d'une mise à jour en deux temps : on **regarde** ce que `--maj` ferait. On n'applique rien. Le TEMPS 2 (application) fera l'objet d'un autre mandat, après décision de Malik.
- `~/.harnais/` (le canon, le superviseur, les verrous, les hooks) est **INTOUCHABLE** : lecture seule, aucune écriture, aucun déplacement, aucun lancement d'autre script que la commande ci-dessous.
- L'état actuel du dépôt n'est pas propre (35 lignes porcelain au 01/10 14:14). Décision de Malik (01/10) : une Mission 0 committe d'abord les fichiers de l'orchestrateur, puis la garde exige un dépôt propre **hors** une liste de chemins tolérés (G3).

## Règles communes (dépôt PUBLIC)

- Rien de secret dans ce que tu commits ou colles (ni clé, ni en-tête HTTP, ni identifiant de compte). `/Users/malik/Documents/EV-LLM/.env` : **ne JAMAIS le lire, l'afficher, le copier ni l'ouvrir.**
- Git en lecture : toujours `git --no-optional-locks`. `git add -- <chemins explicites>` puis `git commit ... -- <chemins explicites>`, jamais `-a`/`-A`. Si `.git/index.lock` existe au moment d'un commit : refais la commande UNE fois ; s'il est toujours là, n'y touche pas, note-le au rapport (STOP partiel propre).
- Push `main` : seuls les commits qui ne touchent que `vault/` passent le hook. Push refusé en non-fast-forward : `git fetch origin` puis `git merge --ff-only origin/main`, puis re-push, UNE fois ; sinon rapport.
- Jamais `sleep`, `stash`, `reset --hard`, `checkout -- .`, `update-ref`, `rebase`, `push --force`. **Aucune tâche de fond vivante à ta sortie.** `rm -rf` seulement sous forme gardée `"${VAR:?}/${SOUS:?}"` (tu n'en as pas besoin ici).
- Ne touche jamais : `.claude/skills/`, `scripts/harnais-hooks/`, `config/harnais.json`, `.claude/worktrees/`, les `vault/echanges/*.md` autres que CE fichier, `~/.harnais/`.
- Commits signés du trailer `Co-Authored-By: Malik & Claude` (message en heredoc), jamais le trailer par défaut de l'outil.
- Étiquettes dans tout texte : [VÉRIFIÉ] (vu dans une sortie de commande ou un fichier) / [HYPOTHÈSE]. Jamais un fait sans [VÉRIFIÉ].

## Rituel de DÉBUT

`statut: en-cours` à la racine du frontmatter de CE fichier, avant tout.

## G0 — Branche

```
cd /Users/malik/Documents/EV-LLM
git checkout main
git branch --show-current
```
Sortie différente de `main` → **STOP** (rapport, rien d'autre).

## Mission 0 — commit des fichiers de l'orchestrateur (scope strict, seul geste qui écrit au TEMPS 1)

1. `git --no-optional-locks status --porcelain` → colle-le.
2. Committe **uniquement** ceux de ces chemins qui apparaissent modifiés ou nouveaux (liste exacte, rien d'autre) :
   - `vault/reprise/00_INDEX.md`
   - `vault/reprise/CARNET_DE_BORD.md`
   - `vault/reprise/2026-09-27-passation-orchestrateur.md`
   - `vault/reprise/gabarits/` (4 fichiers : `R.tmpl`, `_commun.md`, `_e9commun.md`, `_rituels.md`)
   - `vault/decisions/2026-09-28-la-quete-additionner-vs-compter.md`
   - `vault/notes/2026-09-28-anteriorite-additionner-vs-compter-temps.md`
   - `vault/echanges/archive/` (fichiers `.md` non suivis : 22 attendus, dont `2026-09-29-F01-M0039-readme-reconception-synthese.md`)
   ```
   git add -- <chemins ci-dessus présents dans le status>
   git commit -F - -- <mêmes chemins> <<'MSG'
   docs(vault): reconciliation orchestrateur -- carnet, index, passation, gabarits, archives F01-F05 (avant M0040)

   Co-Authored-By: Malik & Claude
   MSG
   git push origin main
   git ls-remote origin refs/heads/main
   ```
   Colle la sortie du push et du `ls-remote` ; le SHA distant doit être égal à `git rev-parse HEAD`.
3. Un chemin hors de cette liste apparaît modifié ou nouveau → ne le committe pas ; il sera jugé par G3.
4. Rien à committer → note-le et passe à G1.

## Gardes de précondition (après la Mission 0) — tout écart = STOP, rapport

- **G1** : `git --no-optional-locks fetch origin` puis `git --no-optional-locks rev-parse HEAD origin/main` → les deux SHA identiques. Sinon STOP.
- **G2** : `origin/main` contient `c117209d323fd003e848ab283eac55b25ed64818` : `git --no-optional-locks merge-base --is-ancestor c117209d323fd003e848ab283eac55b25ed64818 origin/main && echo OK`. Sinon STOP.
- **G3 — dépôt propre hors chemins tolérés** : colle `git --no-optional-locks status --porcelain` en entier, puis :
  ```
  git --no-optional-locks status --porcelain | grep -vE '^\?\? vault/echanges/F0[1-5]\.md$|^\?\? vault/runtime/journal/$|^\?\? vault/runtime/log/$|^\?\? vault/runtime/entretien\.lock\.[0-9]+$'
  ```
  Cette seconde commande doit être **vide**. Une seule ligne restante → STOP (colle-la).
- **G4 — version** : colle `grep '"version"' config/harnais.json`. Attendu `"version": "v1.0.0"`. Autre valeur → STOP.
- **G5 — canon présent, en lecture** : colle `ls -la ~/.harnais/canon/bootstrap/bootstrap.sh`. Absent → STOP. Si `~/.harnais/canon` est un dépôt git, colle `git -C ~/.harnais/canon --no-optional-locks rev-parse HEAD` et `git -C ~/.harnais/canon --no-optional-locks status --porcelain` (lecture seule) ; sinon écris « canon non versionné ».

Avant la mission principale, mémorise l'empreinte de l'arbre :
```
git --no-optional-locks status --porcelain > "$TMPDIR/m0040-avant.txt"
shasum config/harnais.json .gitignore > "$TMPDIR/m0040-sha-avant.txt"
```

## Mission principale — passe à blanc

```
cd /Users/malik/Documents/EV-LLM
sh ~/.harnais/canon/bootstrap/bootstrap.sh "$PWD" --maj --dry-run ; echo "rc=$?"
```
- Colle la sortie **ENTIÈRE**, sans coupe, et le `rc`.
- Option refusée (`--dry-run` ou `--maj` inconnu), `rc` ≠ 0, ou toute sortie qui laisse penser qu'une écriture a eu lieu → **STOP** (colle la sortie, n'essaie AUCUNE autre option, ne relance pas).
- **Interdits ici** : lancer `bootstrap.sh` sans `--dry-run` ; `--force-skill` ; tout autre script de `~/.harnais/`.

**Preuve que rien n'a été écrit**, à coller :
```
git --no-optional-locks status --porcelain | diff "$TMPDIR/m0040-avant.txt" - && echo ARBRE_IDENTIQUE
shasum config/harnais.json .gitignore | diff "$TMPDIR/m0040-sha-avant.txt" - && echo SHA_IDENTIQUES
```
Différence → **STOP** immédiat : décris ce qui a changé, ne restaure rien, ne committe rien.

## Rapport attendu (sous `## Rapport M0040`)

1. **Décompte** : nombre de lignes `POSE` / `DEJA` / `DIVERGE` / `OBSOLETE` / `ECHEC`, compté par commande sur la sortie collée (ex. `grep -c '^POSE'` adapté au format réel ; donne la commande utilisée). Si le format réel ne porte pas ces étiquettes, dis-le et donne le décompte que tu peux prouver.
2. **Pour chaque `DIVERGE`** :
   - chemin côté projet et chemin côté canon (tels que donnés par la sortie ; sinon dis « chemin canon non donné par le bootstrap » et cherche-le en lecture seule dans `~/.harnais/canon/`) ;
   - diff court : `diff -u <canon> <projet> | head -40` ;
   - **adapté exprès ? oui / non / je ne sais pas**, avec la preuve : `git --no-optional-locks log --format='%h %ad %s' --date=short -- <chemin projet>`. **oui** seulement si un message de commit, un mandat archivé (`vault/echanges/archive/`) ou une décision (`vault/decisions/`) dit explicitement que ce fichier a été adapté pour EV-LLM ; **non** si l'historique montre une copie du canon jamais retouchée ensuite ; sinon **je ne sais pas**. Jamais deviner.
3. **Pour chaque `OBSOLETE` et `ECHEC`** : la ligne exacte et ce qu'elle signifie selon la sortie (sans inventer).
4. Ce que `--maj` (sans `--dry-run`) toucherait au TEMPS 2 : la liste des fichiers, d'après la sortie seule.
5. Preuves G0–G5, Mission 0, `ARBRE_IDENTIQUE`, `SHA_IDENTIQUES`.

## Conditions STOP (récapitulatif)

G0–G5 en échec ; option refusée ou `rc` ≠ 0 ; arbre ou empreintes modifiés après la passe à blanc ; `.git/index.lock` persistant ; toute envie de poser une question. Un STOP pousse ce qui est déjà commité (Mission 0), sauf si le STOP porte sur un état git incertain : alors ne rien pousser et le dire.

## Rituels de FIN, dans l'ordre

1. Rapport appendé sous `## Rapport M0040` (preuves collées).
2. `vault/reprise/F01.md` réécrit (état + prochaine étape : « TEMPS 2 en attente de la décision de Malik : appliquer ? DIVERGE : version projet ou `--force-skill` ? ») — à la racine.
3. Une ligne `vault/runtime/events.jsonl` (`src: "fenetre"`, `type: "RAPPORT_RENDU"`, `f: "F01"`, `mandat: "M0040"`, `note` ≤ 200 car.) + `windows.F01` dans `vault/runtime/state.json` — hors git, jamais committés. **state.json : lecture JSON → modification de la SEULE clé `windows.F01` → réécriture ; toutes les autres clés conservées à l'identique. Vérifie après écriture que `next_mandat_id` est toujours présent.** `ts` = `TZ=Europe/Paris date +%Y-%m-%dT%H:%M:%S%:z`.
4. Commit de `vault/reprise/F01.md` sur `main` (vault seul, `git commit -F - -- vault/reprise/F01.md`, trailer) + push + `git ls-remote origin refs/heads/main` collé.
5. Pas de branche : rien d'autre à pousser.
6. Footer de statut, toute dernière ligne du rapport :
```
M0040
Implementation      ✅/❌   (passe à blanc exécutée, rc 0, arbre identique)
Tests               ✅/❌   (G0–G5)
Commit              ✅/❌   (Mission 0 + reprise)
Branch push         ❌      (pas de branche)
Review              ❌
Merge main          ❌
Main push           ✅/❌   (vault seul)
TASK STATUS         <READY_FOR_INTEGRATION | BLOCKED>
PROJECT STATUS      NOT_INTEGRATED
```
7. Vérifie qu'aucune tâche de fond ne tourne (`jobs` vide). **EN DERNIER GESTE : `statut: reponse-disponible`.**

## Rapport M0040

**Résultat : STOP propre.** La passe à blanc a tourné une seule fois et a rendu `rc=1`. Le mandat dit : `rc` ≠ 0 → STOP. Rien n'a été écrit par le bootstrap (`ARBRE_IDENTIQUE`, `SHA_IDENTIQUES`). Aucune autre option essayée, aucune relance.

- [VÉRIFIÉ] `rc=1` vient des 2 `DIVERGE` : dernière ligne de la sortie, `GARDEE harnais.version reste v1.0.0 : 2 DIVERGE et 0 ECHEC`.
- [VÉRIFIÉ] C'est le comportement prévu du script : `bootstrap.sh` l.45 (« harnais.version passe à la version du canon SEULEMENT si aucun DIVERGE ni ECHEC (sinon rc 1) ») et l.612-614 (`exit 1`), à blanc comme en réel.
- [VÉRIFIÉ] Les 2 fichiers `DIVERGE` sont octet pour octet ceux du canon au tag `v1.0.0` : le projet est en retard, il n'a pas été adapté (détail en §2).

### Question que j'aurais posée (STOP)

« `rc=1` est-il un échec de la passe à blanc, ou son résultat normal dès qu'il y a un `DIVERGE` ? »

- Option A : le traiter en STOP, rendre le rapport complet en lecture seule, laisser l'orchestrateur décider. **Choisie** : le mandat l'écrit sans exception, et toute l'information utile au TEMPS 2 est déjà dans la sortie.
- Option B : considérer `rc=1` comme attendu et déclarer le mandat réussi. Écartée : ce serait réinterpréter une condition STOP.

Pour le prochain mandat : la condition « `rc` ≠ 0 → STOP » ne peut pas être tenue par un `--maj --dry-run` qui rencontre un `DIVERGE`. Le script sort alors toujours en `rc 1`.

### 1. Décompte

Commande : `for e in POSE DEJA DIVERGE OBSOLETE ECHEC GARDEE MAJ; do printf '%s=' "$e"; grep -cE "^  $e( |$)" m0040-sortie.txt; done` (les étiquettes sont précédées de deux espaces dans le format réel).

| Étiquette | Lignes |
|---|---|
| POSE | 5 |
| DEJA | 16 |
| DIVERGE | 2 |
| OBSOLETE | 0 |
| ECHEC | 0 |
| GARDEE (hors liste du mandat) | 1 |
| MAJ (hors liste du mandat) | 0 |

[VÉRIFIÉ] sur la sortie collée plus bas.

### 2. Les 2 DIVERGE

Preuve commune [VÉRIFIÉ] :

```
$ git --no-optional-locks log --format='%h %ad %s' --date=short -- .claude/skills/orchestration-bureau/SKILL.md
343e839 2026-09-25 chore(harnais): pose du harnais v1.0.0 [M0095]
$ git --no-optional-locks log --format='%h %ad %s' --date=short -- .claude/skills/orchestration-bureau/references/gabarits.md
343e839 2026-09-25 chore(harnais): pose du harnais v1.0.0 [M0095]
$ git -C ~/.harnais/canon --no-optional-locks show v1.0.0:SKILL-orchestration-maison/<f> | diff -q - .claude/skills/orchestration-bureau/<f>
IDENTIQUE_A_v1.0.0 SKILL.md
IDENTIQUE_A_v1.0.0 references/gabarits.md
$ grep -rlE 'orchestration-bureau/(SKILL\.md|references/gabarits\.md)' vault/echanges/archive vault/decisions
(aucun fichier)
```

Les deux fichiers n'apparaissent pas dans `git status` : la copie de travail est celle du commit `343e839`.

**DIVERGE 1**

- Projet : `/Users/malik/Documents/EV-LLM/.claude/skills/orchestration-bureau/SKILL.md`
- Canon : `/Users/malik/.harnais/canon/SKILL-orchestration-maison/SKILL.md` (chemin donné par la sortie)
- **Adapté exprès ? non.** Un seul commit (la pose v1.0.0), jamais retouché, identique au canon `v1.0.0`. Aucun mandat archivé ni décision ne le cite.
- Ce que le canon v1.1.0 a en plus [VÉRIFIÉ, diff] : le « premier geste » ToolSearch en §1 (décision du 30/09), la réservation de `F99`/`M0000`, la 5e règle des sous-agents (attendre leur retour), le §14 « Équiper un projet — le guichet ». 30 lignes modifiées.
- `diff -u <canon> <projet> | head -40` :

~~~~
--- /Users/malik/.harnais/canon/SKILL-orchestration-maison/SKILL.md	2026-10-01 12:34:58
+++ .claude/skills/orchestration-bureau/SKILL.md	2026-09-25 20:30:15
@@ -24,16 +24,6 @@
 
 ## 1. Reprise de session — NON NÉGOCIABLE
 
-```
-PREMIER GESTE, avant toute lecture ou réponse :
-ToolSearch query="select:mcp__remote-devices__device_bash,mcp__remote-devices__device_list_dir,mcp__remote-devices__get_device_info,SendUserMessage,mcp__claude-code-remote__send_later,mcp__claude-code-remote__list_triggers" max_results=10
-Si device_bash n'apparaît pas dans la réponse : le dire tel quel à l'utilisateur avec la liste des outils remote-devices visibles. Ne jamais proposer de consigne non vérifiée.
-```
-
-(Décision du fondateur, 30/09 10:57 : une session Cowork de reprise cherchait les outils du Mac,
-chargés à la demande, par mots-clés, et ne les trouvait pas. Le chargement se fait par leur nom
-exact, d'abord.)
-
 Lire, dans l'ordre : `<racine>/vault/reprise/CARNET_DE_BORD.md` (instantané court, écrasé) →
 `00_INDEX.md` (index court, rotation) → `<runtime>/state.json` + `tail` d'`events.jsonl` →
 `CARTOGRAPHIE_BRANCHES.md` (régénérer si les branches ont changé). Réconcilier CHAQUE affirmation
@@ -56,7 +46,6 @@
 toujours le plus petit numéro libre, jamais un numéro sauté. Parallèle SEULEMENT si branches ET
 fichiers disjoints, sinon séquentiel avec garde de précondition (§3). Plafond simultané :
 `superviseur.plafond`. La numérotation peut dépasser le plafond (fenêtres réutilisées).
-**`F99` et `M0000` sont réservés à l'essai du guichet** (§14) : jamais alloués par l'orchestrateur.
 
 ## 3. Poser un mandat — le cœur
 
@@ -92,13 +81,10 @@
 - **Mission 0** (scope git strict, gabarit §2) : commit pathspec des fichiers de l'orchestrateur
   (archives, carnet, index, `reprise/`) — PAS les registres de `<runtime>` (hors git, §10) ; jamais
   `git add -A`/`-a`, jamais `<echanges>/*.md` hors `archive/`, jamais un fichier généré.
-- **Sous-agents** (5 règles, gabarit §3) si le mandat parallélise : lecture/recherche = agents
+- **Sous-agents** (4 règles, gabarit §3) si le mandat parallélise : lecture/recherche = agents
   FRAIS, jamais `fork` ; aucun sous-agent ne commit, ne pousse, ne modifie `<runtime>`/`reprise/`,
   ni ne tue un autre agent ; leur rapport est VÉRIFIÉ (fichier:ligne recontrôlés) avant le
-  livrable ; après incident : `git status`/`diff`/`log`/`reflog` AVANT toute autre action ;
-  ATTENDRE le retour de tous les sous-agents avant le premier rituel de fin (rendre la main
-  jusqu'à leur notification, jamais `sleep` ni sondage) — échec ou arrêt de l'un = STOP propre,
-  dit au rapport.
+  livrable ; après incident : `git status`/`diff`/`log`/`reflog` AVANT toute autre action.
~~~~

**DIVERGE 2**

- Projet : `/Users/malik/Documents/EV-LLM/.claude/skills/orchestration-bureau/references/gabarits.md`
- Canon : `/Users/malik/.harnais/canon/SKILL-orchestration-maison/references/gabarits.md` (chemin donné par la sortie)
- **Adapté exprès ? non.** Même preuve : un seul commit, identique au canon `v1.0.0`, aucune mention d'adaptation.
- Ce que le canon v1.1.0 a en plus [VÉRIFIÉ, diff] : la règle (5) des sous-agents, les deux lignes « Scellé tests » / « Contre-témoins » du rapport, l'option `--rapport` de `verifier-rendu.mjs rouge`, la convention `bac:<sha>`. 22 lignes modifiées.
- `diff -u <canon> <projet> | head -40` :

~~~~
--- /Users/malik/.harnais/canon/SKILL-orchestration-maison/references/gabarits.md	2026-10-01 12:34:58
+++ .claude/skills/orchestration-bureau/references/gabarits.md	2026-09-25 20:30:15
@@ -52,7 +52,7 @@
 exclusive de la fenêtre qui le rédige. Jamais les registres de `<chemins.runtime>` : ils sont hors
 git.
 
-## 3. Sous-agents — les 5 règles
+## 3. Sous-agents — les 4 règles
 
 ```
 Un sous-agent `fork` herite du CONTEXTE ENTIER de la session (mandat complet, objectif final)
@@ -63,13 +63,7 @@
     ni ne tue un autre agent -- ces actes restent a la session mere ;
 (3) tout rapport de sous-agent est VERIFIE (citations fichier:ligne recontrolees) avant
     d'entrer dans un livrable ;
-(4) apres tout incident : git status/diff/log/reflog AVANT toute autre action ;
-(5) ATTENDRE LE RETOUR DE TOUS les sous-agents lances AVANT le premier rituel de fin
-    (rapport, events.jsonl, statut) -- jamais un livrable "complet" ecrit sur un travail
-    a moitie rendu. Attendre = rendre la main jusqu'a la notification du sous-agent,
-    jamais `sleep` ni sondage (relecture periodique d'une sortie). Ne revient pas =
-    notification d'echec ou d'arret du sous-agent : le dire au rapport (lequel, pour
-    quoi faire, ce qui manque de ce fait), ne rien livrer qui dependait de lui, STOP propre.
+(4) apres tout incident : git status/diff/log/reflog AVANT toute autre action.
 ```
 
 ## 4. Footer de statut — toute dernière ligne du rapport
@@ -94,22 +88,8 @@
 `gardes_deploiement[]`, ajouter la ligne de garde correspondante (§11) : elle conditionne
 `INTEGRATED` au même titre.
 
-**Déclarations de l'auteur d'un correctif** (#35, R061) : dans `## Rapport Mxxxx`, avant le tableau, deux lignes (en puce ou non) :
-
-```
-Scellé tests : <empreinte> (node scripts/verifier-rendu.mjs scelle --base <sha-base> --tip <sha-rendu>)
-Contre-témoins : `<regex des tests neufs voulus verts sur la base (gardes de non-régression)>`
-```
+**Le tableau se vérifie, il ne se croit pas** (#28, #35) : l'orchestrateur, à chaque rapport traité, lance `node scripts/verifier-rendu.mjs effet --rapport <chemins.echanges>/Fxx.md` depuis la racine, après un `git fetch origin` ; le doubleur le relance, puis, pour un correctif, `node scripts/verifier-rendu.mjs rouge --branche <branche> --base <merge-base> --test '<commande de test>'`. Tout `ECART` se résout avant le doublage ou le GO.
 
-`<empreinte>` = les 64 caractères hexadécimaux que la commande entre parenthèses imprime (`SCELLE <empreinte> (…)`),
-lancée sur le commit rendu. `Contre-témoins : aucun` quand tout test neuf est un témoin rouge→vert ; sinon la regex
~~~~

### 3. OBSOLETE et ECHEC

Aucune ligne `OBSOLETE`, aucune ligne `ECHEC` [VÉRIFIÉ, décompte].

Ligne hors liste, à connaître : `GARDEE   harnais.version reste v1.0.0 : 2 DIVERGE et 0 ECHEC ci-dessus -- trancher chacun, puis relancer --maj`. Sens selon la sortie : la version n'est pas montée tant que les 2 `DIVERGE` ne sont pas tranchés.

### 4. Ce que `--maj` sans `--dry-run` toucherait au TEMPS 2 (d'après la sortie seule)

- **`.gitignore`** : 5 lignes ajoutées.
  - `**/vault/runtime/log/`
  - `**/vault/runtime/journal/`
  - `**/vault/runtime/entretien.lock*`
  - `**/archive/*-F99-M0000-essai-equipement-*.md`
  - `/vault/echanges/F99.md`
- **Rien d'autre.** Les 2 `DIVERGE` sont « copie du projet conservée », les 16 `DEJA` ne sont pas réécrits, `config/harnais.json` reste en `v1.0.0` (`GARDEE`).
- [HYPOTHÈSE, d'après `bootstrap.sh` l.612-614] Ce `--maj` réel sortirait lui aussi en `rc 1`, version non montée.
- Pour atteindre `v1.1.0`, il faut d'abord trancher les 2 `DIVERGE`. [VÉRIFIÉ, `bootstrap.sh` l.50-52] Le remède écrit par le script, « si la copie du projet n'a pas été adaptée » : `bootstrap.sh <projet> --nom <projet.nom> --force-skill` puis `bootstrap.sh <projet> --maj`. Non lancé (interdit ici). `projet.nom` = `ev-llm` [VÉRIFIÉ, ligne `Projet :` de la sortie].
- Effet utile attendu des 3 premières lignes `.gitignore` : `vault/runtime/log/`, `journal/` et `entretien.lock.*` sortiraient de `git status` [HYPOTHÈSE].

### 5. Preuves

**G0** [VÉRIFIÉ]
```
$ git checkout main
Already on 'main'
Your branch is up to date with 'origin/main'.
$ git branch --show-current
main
```

**Mission 0** [VÉRIFIÉ] — status avant commit :
```
 M vault/reprise/00_INDEX.md
 M vault/reprise/CARNET_DE_BORD.md
?? vault/decisions/2026-09-28-la-quete-additionner-vs-compter.md
?? vault/echanges/F01.md
?? vault/echanges/F02.md
?? vault/echanges/F03.md
?? vault/echanges/F04.md
?? vault/echanges/F05.md
?? vault/echanges/archive/2026-09-27-F01-M0022-e009-procedure-apprise.md
?? vault/echanges/archive/2026-09-27-F01-M0027-e009bis.md
?? vault/echanges/archive/2026-09-27-F01-M0030-e015-ecosysteme.md
?? vault/echanges/archive/2026-09-27-F02-M0023-e010-enseignement.md
?? vault/echanges/archive/2026-09-27-F02-M0032-e016-a2-stop.md
?? vault/echanges/archive/2026-09-27-F03-M0024-e011-objectif-mdl.md
?? vault/echanges/archive/2026-09-27-F03-M0025-e012-evolution.md
?? vault/echanges/archive/2026-09-27-F03-M0029-e013-correctifs.md
?? vault/echanges/archive/2026-09-27-F03-M0034-e013-micro-correctif.md
?? vault/echanges/archive/2026-09-27-F03-R010-doublage-e008-e013.md
?? vault/echanges/archive/2026-09-27-F03-R011-redoublage-e008-e013.md
?? vault/echanges/archive/2026-09-27-F03-R012-redoublage-final-e008-e013.md
?? vault/echanges/archive/2026-09-27-F04-M0026-e013-insecte.md
?? vault/echanges/archive/2026-09-27-F04-M0028-e014-reperage.md
?? vault/echanges/archive/2026-09-27-F04-M0031-e016-mouches.md
?? vault/echanges/archive/2026-09-28-F01-M0035-readme-racine.md
?? vault/echanges/archive/2026-09-28-F01-M0036-readme-anglais.md
?? vault/echanges/archive/2026-09-28-F01-M0037-licence-mit.md
?? vault/echanges/archive/2026-09-28-F01-M0038-readme-correctifs-r013.md
?? vault/echanges/archive/2026-09-28-F03-R013-readme-licence.md
?? vault/echanges/archive/2026-09-28-F03-R014-readme-licence-final.md
?? vault/echanges/archive/2026-09-29-F01-M0039-readme-reconception-synthese.md
?? vault/notes/2026-09-28-anteriorite-additionner-vs-compter-temps.md
?? vault/reprise/2026-09-27-passation-orchestrateur.md
?? vault/reprise/gabarits/
?? vault/runtime/entretien.lock.590
?? vault/runtime/journal/
?? vault/runtime/log/
```
Commit `8910d3a852922edbf189eafc48435b9adcde5f14` : 31 fichiers (2 modifiés, 29 créés : 22 archives `.md`, 4 gabarits, passation, décision, note), 4306 insertions, 8 suppressions. Aucun chemin hors liste. Recherche de secrets avant commit sur les 31 fichiers : aucun motif trouvé.
```
$ git push origin main
To github.com:malikkaraoui/EV-LLM.git
   c117209..8910d3a  main -> main
$ git ls-remote origin refs/heads/main
8910d3a852922edbf189eafc48435b9adcde5f14	refs/heads/main
$ git rev-parse HEAD
8910d3a852922edbf189eafc48435b9adcde5f14
```

**G1** [VÉRIFIÉ]
```
$ git --no-optional-locks fetch origin   (rc 0)
$ git --no-optional-locks rev-parse HEAD origin/main
8910d3a852922edbf189eafc48435b9adcde5f14
8910d3a852922edbf189eafc48435b9adcde5f14
```

**G2** [VÉRIFIÉ]
```
$ git --no-optional-locks merge-base --is-ancestor c117209d323fd003e848ab283eac55b25ed64818 origin/main && echo OK
OK
```

**G3** [VÉRIFIÉ]
```
$ git --no-optional-locks status --porcelain
?? vault/echanges/F01.md
?? vault/echanges/F02.md
?? vault/echanges/F03.md
?? vault/echanges/F04.md
?? vault/echanges/F05.md
?? vault/runtime/entretien.lock.594
?? vault/runtime/journal/
?? vault/runtime/log/
$ git --no-optional-locks status --porcelain | grep -vE '^\?\? vault/echanges/F0[1-5]\.md$|^\?\? vault/runtime/journal/$|^\?\? vault/runtime/log/$|^\?\? vault/runtime/entretien\.lock\.[0-9]+$'
(vide, grep rc=1)
```

**G4** [VÉRIFIÉ]
```
$ grep '"version"' config/harnais.json
    "version": "v1.0.0"
```

**G5** [VÉRIFIÉ]
```
$ ls -la ~/.harnais/canon/bootstrap/bootstrap.sh
-rwxr-xr-x  1 malik  staff  51455  1 oct.  12:34 /Users/malik/.harnais/canon/bootstrap/bootstrap.sh
$ git -C ~/.harnais/canon --no-optional-locks rev-parse HEAD
e506f6dcd556526168092c2b47920f51b0806ca8
$ git -C ~/.harnais/canon --no-optional-locks status --porcelain
(vide)
$ git -C ~/.harnais/canon --no-optional-locks describe --tags
v1.1.0
```
Canon versionné, propre, sur le tag `v1.1.0`. Tags présents : `v1.0.0 v1.0.1 v1.1.0`.

**Empreinte avant la passe** [VÉRIFIÉ]
```
?? vault/echanges/F01.md
?? vault/echanges/F02.md
?? vault/echanges/F03.md
?? vault/echanges/F04.md
?? vault/echanges/F05.md
?? vault/runtime/entretien.lock.595
?? vault/runtime/journal/
?? vault/runtime/log/
f6ab0070f1a39b57cb9fa0381232d81f06f19e72  config/harnais.json
95e910c4226ee34f1a06b43ba3aab82a12dd3d8e  .gitignore
```

**Sortie ENTIÈRE de `sh ~/.harnais/canon/bootstrap/bootstrap.sh "$PWD" --maj --dry-run ; echo "rc=$?"`** [VÉRIFIÉ] (stdout et stderr réunis, 159 lignes) :

~~~~
### DRY-RUN : rien ne sera écrit ###
Canon  : /Users/malik/.harnais/canon   (version : v1.1.0)
Projet : /Users/malik/Documents/EV-LLM   (nom: ev-llm, version : v1.0.0)

1. Convention -> .claude/skills/orchestration-bureau/
  DIVERGE  .claude/skills/orchestration-bureau/SKILL.md (copie du projet conservée ; diff canon -> projet :)
      --- /Users/malik/.harnais/canon/SKILL-orchestration-maison/SKILL.md	2026-10-01 12:34:58
      +++ /Users/malik/Documents/EV-LLM/.claude/skills/orchestration-bureau/SKILL.md	2026-09-25 20:30:15
      @@ -24,16 +24,6 @@
       
       ## 1. Reprise de session — NON NÉGOCIABLE
       
      -```
      -PREMIER GESTE, avant toute lecture ou réponse :
      -ToolSearch query="select:mcp__remote-devices__device_bash,mcp__remote-devices__device_list_dir,mcp__remote-devices__get_device_info,SendUserMessage,mcp__claude-code-remote__send_later,mcp__claude-code-remote__list_triggers" max_results=10
      -Si device_bash n'apparaît pas dans la réponse : le dire tel quel à l'utilisateur avec la liste des outils remote-devices visibles. Ne jamais proposer de consigne non vérifiée.
      -```
      -
      -(Décision du fondateur, 30/09 10:57 : une session Cowork de reprise cherchait les outils du Mac,
      -chargés à la demande, par mots-clés, et ne les trouvait pas. Le chargement se fait par leur nom
      -exact, d'abord.)
      -
       Lire, dans l'ordre : `<racine>/vault/reprise/CARNET_DE_BORD.md` (instantané court, écrasé) →
       `00_INDEX.md` (index court, rotation) → `<runtime>/state.json` + `tail` d'`events.jsonl` →
       `CARTOGRAPHIE_BRANCHES.md` (régénérer si les branches ont changé). Réconcilier CHAQUE affirmation
      @@ -56,7 +46,6 @@
       toujours le plus petit numéro libre, jamais un numéro sauté. Parallèle SEULEMENT si branches ET
       fichiers disjoints, sinon séquentiel avec garde de précondition (§3). Plafond simultané :
       `superviseur.plafond`. La numérotation peut dépasser le plafond (fenêtres réutilisées).
      -**`F99` et `M0000` sont réservés à l'essai du guichet** (§14) : jamais alloués par l'orchestrateur.
       
       ## 3. Poser un mandat — le cœur
       
      @@ -92,13 +81,10 @@
       - **Mission 0** (scope git strict, gabarit §2) : commit pathspec des fichiers de l'orchestrateur
         (archives, carnet, index, `reprise/`) — PAS les registres de `<runtime>` (hors git, §10) ; jamais
         `git add -A`/`-a`, jamais `<echanges>/*.md` hors `archive/`, jamais un fichier généré.
      -- **Sous-agents** (5 règles, gabarit §3) si le mandat parallélise : lecture/recherche = agents
      +- **Sous-agents** (4 règles, gabarit §3) si le mandat parallélise : lecture/recherche = agents
         FRAIS, jamais `fork` ; aucun sous-agent ne commit, ne pousse, ne modifie `<runtime>`/`reprise/`,
         ni ne tue un autre agent ; leur rapport est VÉRIFIÉ (fichier:ligne recontrôlés) avant le
      -  livrable ; après incident : `git status`/`diff`/`log`/`reflog` AVANT toute autre action ;
      -  ATTENDRE le retour de tous les sous-agents avant le premier rituel de fin (rendre la main
      -  jusqu'à leur notification, jamais `sleep` ni sondage) — échec ou arrêt de l'un = STOP propre,
      -  dit au rapport.
      +  livrable ; après incident : `git status`/`diff`/`log`/`reflog` AVANT toute autre action.
       - **Preuve d'écran** si le mandat touche l'affichage : captures RÉELLES avant/après dans
         `vault/revues/captures-<id>/`, citées au rapport — un harnais local, un composant isolé ou un
         `git diff` n'en tiennent jamais lieu. Impossible → axe UX **pas GO** (⚠️ « non vérifié à
      @@ -324,27 +310,3 @@
       **Source de vérité unique** : la convention vit dans le dépôt du projet. Un skill de compte n'en est
       qu'un **POINTEUR** (texte exact : `references/gabarits.md` §12), qui STOP si le dépôt n'est pas
       accessible, et qui ne change que si le CHEMIN de la source change — aucune version ne s'y grave.
      -
      -## 14. Équiper un projet — le guichet
      -
      -Un projet s'équipe par le **guichet** du superviseur : le fondateur colle dans Cowork le prompt
      -versionné `templates/guichet/prompt-cowork.md` (une ligne à modifier, `PROJET`) ; Cowork dépose une
      -demande, un exécutant déterministe du Mac pose, publie, inscrit, lance un mandat test, et n'active
      -les hooks git qu'après ce test réussi. Voie de secours, au Terminal du Mac : le skill
      -`equiper-projet` (qui passe lui aussi par le guichet pour inscription → essai → hooks). Un mandat de
      -l'orchestrateur peut au plus **préparer** la pose (skill en mode mandat : pose et publication, hooks
      -inactifs, aucun dépôt au guichet) : l'inscription, l'essai et les hooks passent toujours par le guichet. Principe : sur le périmètre de l'utilisateur, le guichet **informe, il ne bloque
      -pas**. Autorité : `superviseur/README.md` § Guichet d'équipement.
      -
      -**`F99` et `M0000` sont réservés à l'essai du guichet.** Le mandat test d'un équipement est posé
      -par le Mac sous `<echanges>/F99.md`, `mandat_id: M0000`, y compris dans un projet déjà servi,
      -pendant que son orchestrateur travaille. En conséquence :
      -
      -- l'orchestrateur n'alloue **jamais** `F99` ni `M0000` (§2, §3) ; aucune numérotation réelle ne
      -  commence à `0000` ;
      -- la **réconciliation** (§1, §6, §7) **ignore** les événements `f=F99` et `M0000` d'`events.jsonl`
      -  et **n'attend pas** de `windows.F99` dans `state.json` : ni fenêtre fantôme, ni mandat perdu ;
      -- `<echanges>/F99.md` et son archive `…/archive/*-F99-M0000-essai-equipement-*.md` sont ignorés par
      -  git (fragment `.gitignore` du bootstrap) : jamais dans une Mission 0, jamais committés ;
      -- un `F99` coincé n'est **pas** libéré à la main par l'orchestrateur : le superviseur le liquide
      -  lui-même (`ESSAI_LIQUIDE`) ; un doute se signale au fondateur.
  DIVERGE  .claude/skills/orchestration-bureau/references/gabarits.md (copie du projet conservée ; diff canon -> projet :)
      --- /Users/malik/.harnais/canon/SKILL-orchestration-maison/references/gabarits.md	2026-10-01 12:34:58
      +++ /Users/malik/Documents/EV-LLM/.claude/skills/orchestration-bureau/references/gabarits.md	2026-09-25 20:30:15
      @@ -52,7 +52,7 @@
       exclusive de la fenêtre qui le rédige. Jamais les registres de `<chemins.runtime>` : ils sont hors
       git.
       
      -## 3. Sous-agents — les 5 règles
      +## 3. Sous-agents — les 4 règles
       
       ```
       Un sous-agent `fork` herite du CONTEXTE ENTIER de la session (mandat complet, objectif final)
      @@ -63,13 +63,7 @@
           ni ne tue un autre agent -- ces actes restent a la session mere ;
       (3) tout rapport de sous-agent est VERIFIE (citations fichier:ligne recontrolees) avant
           d'entrer dans un livrable ;
      -(4) apres tout incident : git status/diff/log/reflog AVANT toute autre action ;
      -(5) ATTENDRE LE RETOUR DE TOUS les sous-agents lances AVANT le premier rituel de fin
      -    (rapport, events.jsonl, statut) -- jamais un livrable "complet" ecrit sur un travail
      -    a moitie rendu. Attendre = rendre la main jusqu'a la notification du sous-agent,
      -    jamais `sleep` ni sondage (relecture periodique d'une sortie). Ne revient pas =
      -    notification d'echec ou d'arret du sous-agent : le dire au rapport (lequel, pour
      -    quoi faire, ce qui manque de ce fait), ne rien livrer qui dependait de lui, STOP propre.
      +(4) apres tout incident : git status/diff/log/reflog AVANT toute autre action.
       ```
       
       ## 4. Footer de statut — toute dernière ligne du rapport
      @@ -94,22 +88,8 @@
       `gardes_deploiement[]`, ajouter la ligne de garde correspondante (§11) : elle conditionne
       `INTEGRATED` au même titre.
       
      -**Déclarations de l'auteur d'un correctif** (#35, R061) : dans `## Rapport Mxxxx`, avant le tableau, deux lignes (en puce ou non) :
      -
      -```
      -Scellé tests : <empreinte> (node scripts/verifier-rendu.mjs scelle --base <sha-base> --tip <sha-rendu>)
      -Contre-témoins : `<regex des tests neufs voulus verts sur la base (gardes de non-régression)>`
      -```
      +**Le tableau se vérifie, il ne se croit pas** (#28, #35) : l'orchestrateur, à chaque rapport traité, lance `node scripts/verifier-rendu.mjs effet --rapport <chemins.echanges>/Fxx.md` depuis la racine, après un `git fetch origin` ; le doubleur le relance, puis, pour un correctif, `node scripts/verifier-rendu.mjs rouge --branche <branche> --base <merge-base> --test '<commande de test>'`. Tout `ECART` se résout avant le doublage ou le GO.
       
      -`<empreinte>` = les 64 caractères hexadécimaux que la commande entre parenthèses imprime (`SCELLE <empreinte> (…)`),
      -lancée sur le commit rendu. `Contre-témoins : aucun` quand tout test neuf est un témoin rouge→vert ; sinon la regex
      -entre accents graves, qui couvre les noms exacts des gardes (un test neuf déjà vert sur la base et non couvert = `ECART`).
      -Une seule valeur par ligne dans la section ; mandat sans test : lignes sans objet.
      -
      -**Le tableau se vérifie, il ne se croit pas** (#28, #35) : l'orchestrateur, à chaque rapport traité, lance `node scripts/verifier-rendu.mjs effet --rapport <chemins.echanges>/Fxx.md` depuis la racine, après un `git fetch origin` ; le doubleur le relance, puis, pour un correctif, `node scripts/verifier-rendu.mjs rouge --branche <branche> --base <merge-base> --test '<commande de test>' --rapport <chemins.echanges>/Fxx.md` : `--rapport` lit les deux lignes ci-dessus dans la section du rapport (ligne absente = `ECART` ; forme manuelle équivalente : `--scelle <empreinte du rapport> --contre-temoins '<regex du rapport>'`, jamais avec `--rapport`). Tout `ECART` se résout avant le doublage ou le GO.
      -
      -**SHA de bac marqués `bac:`** (#53) : dans un rapport, un SHA d'un dépôt jetable (faux origin d'un témoin, fixture de bac) s'écrit `bac:<sha>`, collé, sans espace, `bac:` en minuscules (`BAC:` / `Bac:` ne marquent rien). `effet` ne le cherche pas dans le dépôt et le compte à part (ligne `BAC`, sans effet sur le rc) ; un SHA introuvable écrit nu reste un `ECART`. **Jamais dans le tableau de fin** : `bac:` dans une case est un `ECART` (R053), le tableau ne cite que des SHA du dépôt réel. Toute ligne qui commence par un libellé du footer (`Implementation` … `PROJECT STATUS`), quel que soit son statut (✅ ❌ ⚠️ ⛔ N/A), est une case : chacun de ses SHA est contrôlé strictement (#54).
      -
       ## 5. Bloc de lancement manuel + panneau ⚠️
       
       ```

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
  POSE     .gitignore += **/vault/runtime/log/
  POSE     .gitignore += **/vault/runtime/journal/
  POSE     .gitignore += **/vault/runtime/entretien.lock*
  POSE     .gitignore += **/archive/*-F99-M0000-essai-equipement-*.md
  POSE     .gitignore += /vault/echanges/F99.md

5. Version -> config/harnais.json (harnais.version ; rien d'autre n'est touché)
  GARDEE   harnais.version reste v1.0.0 : 2 DIVERGE et 0 ECHEC ci-dessus -- trancher chacun, puis relancer --maj
rc=1
~~~~

**Preuve que rien n'a été écrit** [VÉRIFIÉ]
```
$ git --no-optional-locks status --porcelain | diff "$TMPDIR/m0040-avant.txt" - && echo ARBRE_IDENTIQUE
ARBRE_IDENTIQUE
$ shasum config/harnais.json .gitignore | diff "$TMPDIR/m0040-sha-avant.txt" - && echo SHA_IDENTIQUES
SHA_IDENTIQUES
```

### Remarques

- [VÉRIFIÉ] Le nom `vault/runtime/entretien.lock.<n>` change tout seul (590 au début, 594 à G3, 595 à l'empreinte). `ARBRE_IDENTIQUE` a tenu ici, mais cette preuve peut casser sans que le bootstrap y soit pour rien. Au TEMPS 2, comparer l'arbre en excluant cette ligne.
- [VÉRIFIÉ] Lectures faites dans `~/.harnais/canon` : `bootstrap.sh` (lecture), `git rev-parse`, `status`, `describe`, `tag -l`, `show v1.0.0:<fichier>`, tous en `--no-optional-locks`. Aucune écriture, aucun autre script lancé.
- `.git/index.lock` : absent à chaque commit [VÉRIFIÉ].

**Rituels de fin** [VÉRIFIÉ]

- `vault/reprise/F01.md` réécrit, commit `afc5d0380ba6ca3bae03b80fe16124b09872bf31` (vault seul, 1 fichier).
```
$ git push origin main
To github.com:malikkaraoui/EV-LLM.git
   8910d3a..afc5d03  main -> main
$ git ls-remote origin refs/heads/main
afc5d0380ba6ca3bae03b80fe16124b09872bf31	refs/heads/main
$ git rev-parse HEAD
afc5d0380ba6ca3bae03b80fe16124b09872bf31
```
- `vault/runtime/events.jsonl` : une ligne `RAPPORT_RENDU` (`src: "fenetre"`, `f: "F01"`, `mandat: "M0040"`, note de 167 caractères, `ts` 2026-10-01T14:19:00+02:00).
- `vault/runtime/state.json` : seule `windows.F01` modifiée ; les autres clés comparées avant/après : identiques ; `next_mandat_id` toujours présent (`M0041`).
- `date` de ce Mac ne connaît pas `%:z` (il rend `:z` tel quel) : `ts` produit par `date +%Y-%m-%dT%H:%M:%S%z`, avec les deux-points remis dans le décalage.
- `jobs` : vide, aucune tâche de fond.

```
M0040
Implementation      ❌   (passe à blanc exécutée une fois, rc 1 et non 0 : 2 DIVERGE ; arbre identique)
Tests               ✅   (G0–G5)
Commit              ✅   (Mission 0 8910d3a + reprise afc5d03)
Branch push         ❌      (pas de branche)
Review              ❌
Merge main          ❌
Main push           ✅   (vault seul, origin/main = afc5d03)
TASK STATUS         BLOCKED
PROJECT STATUS      NOT_INTEGRATED
```
