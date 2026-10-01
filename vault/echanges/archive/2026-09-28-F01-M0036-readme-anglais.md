---
date: 2026-09-28
tags: [readme, documentation, traduction, notes]
session: F01
mandat: readme-anglais-notes-versionnees
mandat_id: M0036
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F01-M0035
branche: docs/readme-2026-09-28
derniere_maj: 2026-09-28T08:07:13+0200
---

# M0036 — README racine en ANGLAIS, titre 🧠 🐜, et notes du vault versionnées pour que les liens tiennent

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
- Appels à la passerelle Vercel : tout modèle témoin (`/v1/chat/completions`) impose son fournisseur (`providerOptions.gateway.only`) et journalise le fournisseur réel ; **HTTP 402 (`quota_for_entity_exceeded`, budget) = arrêt net, aucune relance**.
- **Antériorité (règle Malik 27/09 20:46)** : avant tout lancement, l'orchestrateur fait une recherche d'antériorité PROFONDE (agents dédiés, sources lues) ; verdict (fait / partiellement / non trouvé) et la part nouvelle sont écrits dans le mandat. Interdit de refaire du connu pour arriver au même résultat.

Modèle : `opus --effort medium`. **Aucun calcul, aucun entraînement, aucun appel d'API** (CPU réservé à Malik en semaine).

## 0. Contexte
M0035 (archive : `vault/echanges/archive/2026-09-28-F01-M0035-readme-racine.md`, lis-la) a écrit `README.md` (282 lignes, français) sur `docs/readme-2026-09-28`, tip `99ccc79da3b1ba5757da0e361ddc5c6077b421c6`. L'orchestrateur a vérifié 5 chiffres au hasard contre les README d'expériences : conformes. Consignes nouvelles de Malik (28/09 08:06–08:07) : **le README doit être en anglais**, et **le titre doit porter les emojis 🧠 et 🐜, bien gros** (titre H1). Par ailleurs, trois notes citées « pas encore versionnée » et une note d'antériorité neuve doivent entrer dans `main` (dossier `vault/`, autorisé en direct par le hook) pour que le README puisse pointer dessus.

## 1. Gardes
1. `git -C /Users/malik/Documents/EV-LLM fetch origin` ; `git rev-parse origin/docs/readme-2026-09-28` = `99ccc79da3b1ba5757da0e361ddc5c6077b421c6` ; worktree `.claude/worktrees/F01-M0035` existe encore sur cette branche, propre (`status --short` vide) — sinon `git worktree add .claude/worktrees/F01-M0036 docs/readme-2026-09-28` et adapte.
2. À la racine (`main`) : les fichiers suivants existent et sont non suivis (`git status --short vault/notes/` → `??`) : `vault/notes/2026-09-27-debrief-e008.md`, `vault/notes/2026-09-27-genese-suite.md`, `vault/notes/2026-09-27-veille-procedure.md`, `vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md`. Avant de les committer : `grep -nIiE 'sk-[a-z0-9]{10}|bearer |team_[a-z0-9]{6}|x-vercel-id|set-cookie' <ces 4 fichiers>` → rien ; sinon STOP.

## 2. Mission A — notes du vault sur `main` (racine, vault seul)
`git -C /Users/malik/Documents/EV-LLM add -- vault/notes/2026-09-27-debrief-e008.md vault/notes/2026-09-27-genese-suite.md vault/notes/2026-09-27-veille-procedure.md vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md` puis `git commit -- <les 4 chemins>` avec message heredoc `docs(vault): notes 27/09 -- genese-suite, veille procedure, debrief E008, anteriorite E015-A2` + trailer ; push ; `git ls-remote origin refs/heads/main` collé. Si `.git/index.lock` : règle commune (une reprise, sinon note).

## 3. Mission B — README en anglais, sur la branche
Traduis `README.md` **en anglais**, fidèlement : même structure, mêmes chiffres, mêmes étiquettes (**[VERIFIED]** / **[HYPOTHESIS]**), mêmes liens. Règles :
- **Titre H1** : `# 🧠🐜 EV-LLM — a public research log` (les deux emojis en tête du H1, c'est le « bien gros » demandé : GitHub rend le H1 en grand ; n'ajoute pas d'image ni de HTML). Tu peux reprendre 🧠 et 🐜 une fois chacun dans le corps si c'est naturel (🐜 pour « l'insecte » E013, 🧠 pour la méthode), pas davantage.
- Anglais sobre, scientifique, sans superlatif ; garde les termes techniques du projet en anglais standard (*carry*, *scratchpad*, *seed*, *out-of-distribution*, *preregistration*, *independent review*), et garde les noms propres et codes (E013, R012, `ECH0`, `COLL`) tels quels. Les citations de Malik traduites entre guillemets avec « (translated) » la première fois.
- Les nombres gardent le format anglais (`91.2 %`, `1,000 digits`, `3.2 M parameters`).
- **Aucun chiffre ne change.** Après traduction : extrais tous les nombres du README français (tip `99ccc79`) et de l'anglais (`grep -oE '[0-9][0-9 ,.]*'` normalisé) et colle au rapport la preuve qu'ils sont identiques à la ponctuation près ; tout écart = tu le corriges avant de committer.
- Remplace les trois mentions « pas encore versionnée » par des liens relatifs vers les notes committées en Mission A (`vault/notes/2026-09-27-genese-suite.md`, `vault/notes/2026-09-27-veille-procedure.md`) ; dans « Pistes ouvertes », le passage « n'est pas encore versionné [HYPOTHÈSE jusqu'à publication des sources] » devient un lien vers `vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md` et l'étiquette redevient [VERIFIED — sources listed in the note].
- Ajoute une ligne sous le H1 : `*Version française : voir l'historique git (commit 99ccc79) — this README is maintained in English.*` en anglais : `*A French version of this file exists in git history (commit 99ccc79); the README is maintained in English.*`
- Toujours aucune mention de l'enfant de Malik. Licence : garde « to be decided » (question ouverte).
- Longueur : ≈ 280–320 lignes ; tableaux ≤ 3 colonnes.
Commit heredoc : `docs(readme): English version, 🧠🐜 title, links to versioned vault notes` + trailer ; push ; `git ls-remote origin refs/heads/docs/readme-2026-09-28` collé (nouveau tip = garde de R013).

## 4. Preuves
`git diff --stat 99ccc79..HEAD` (README.md seul sur la branche) ; `head -n 3 README.md` collé ; preuve d'identité des nombres ; `git ls-remote` des deux refs ; `git log -1 --format=%B` (trailer) sur les deux commits ; `git ls-tree origin/main vault/notes/` montrant les 4 notes.

## 5. STOP
Garde 1–2 en écart · un chiffre impossible à conserver à l'identique (tu ne « corriges » pas un chiffre du README : s'il te paraît faux, tu le laisses et tu le signales au rapport) · diff hors README sur la branche.

## Rituels

DÉBUT : `statut: en-cours` à la racine du frontmatter de CE fichier, avant tout.

FIN, dans l'ordre :
1. Rapport appendé sous `## Rapport <mandat_id>` (preuves collées).
2. `vault/reprise/<Fxx>.md` (état + prochaine étape) — à la racine.
3. Une ligne `vault/runtime/events.jsonl` (`src: "fenetre"`, `type: "RAPPORT_RENDU"`, `f`, `mandat`, `note` ≤ 200 car.) + `windows.<Fxx>` dans `vault/runtime/state.json` — hors git, jamais committés. **state.json : lecture JSON → modification de la SEULE clé `windows.<Fxx>` → réécriture ; toutes les autres clés (`schema_version`, `next_mandat_id`, `next_revue_id`, `projet`, autres fenêtres) sont conservées à l'identique. Vérifie après écriture que `next_mandat_id` est toujours présent (incident du 26/09 : state.json écrasé).** Toute ligne `events.jsonl` porte `ts` (horloge réelle `TZ=Europe/Paris date +%Y-%m-%dT%H:%M:%S%:z`).
4. Commit de `vault/reprise/<Fxx>.md` sur `main` à la racine (vault seul) + push + `git ls-remote origin refs/heads/main` collé.
5. Ta branche (s'il y en a une) poussée + `git ls-remote origin refs/heads/<branche>` collé.
6. Footer de statut, toute dernière ligne du rapport :
```
<mandat_id>
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

## Rapport M0036

**Rendu : Missions A et B faites.** Aucun calcul, aucun entraînement, aucun appel d'API ; seulement `git`, `grep`, `sed`, `python3` (lecture JSON / comptage).

### Gardes
1. [VÉRIFIÉ] `git fetch origin` OK ; `origin/docs/readme-2026-09-28` = `99ccc79da3b1ba5757da0e361ddc5c6077b421c6` ; worktree `.claude/worktrees/F01-M0035` présent sur cette branche, `status --short` vide → réutilisé.
2. [VÉRIFIÉ] Les 4 notes étaient `??` ; grep secrets (`sk-…|bearer |team_…|x-vercel-id|set-cookie`) sur les 4 : aucune ligne (exit 1). Pas de `.git/index.lock`.

### Mission A — notes sur `main`
Commit `5b977ebb771431a8e5f13eefca8dc9c15d5b4787` (4 fichiers, +194), vault seul. Un premier essai a échoué sans effet (zsh ne découpe pas une variable de chemins → `pathspec did not match`, aucun commit créé) ; refait avec chemins explicites.
```
$ git log -1 --format=%B 5b977eb
docs(vault): notes 27/09 -- genese-suite, veille procedure, debrief E008, anteriorite E015-A2

Co-Authored-By: Malik & Claude
$ git push origin main
   169b0a8..5b977eb  main -> main
$ git ls-remote origin refs/heads/main
5b977ebb771431a8e5f13eefca8dc9c15d5b4787	refs/heads/main
$ git ls-tree origin/main vault/notes/
100644 blob d19de4816f379f4b8d980c226e46925e57791f45	vault/notes/2026-09-26-issues-github.md
100644 blob 5e3ccf8d9c9a72510af7dc0f993d5b210a029b20	vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md
100644 blob 9a67f1636e5cb3e257bb9c12409fd2f364d8fde7	vault/notes/2026-09-27-debrief-e008.md
100644 blob 2a856662f579f85eb5c71b55e51a39ac45d84121	vault/notes/2026-09-27-genese-suite.md
100644 blob 3ed2581c00095843a130d8f298d6f4f8b73f4776	vault/notes/2026-09-27-veille-procedure.md
```

### Mission B — README anglais
```
$ git diff --stat 99ccc79..HEAD
 README.md | 440 +++++++++++++++++++++++++++++++-------------------------------
 1 file changed, 221 insertions(+), 219 deletions(-)
$ wc -l README.md
     284 README.md
$ head -n 3 README.md
# 🧠🐜 EV-LLM — a public research log

*A French version of this file exists in git history (commit 99ccc79); the README is maintained in English.*
$ git log -1 --format=%B
docs(readme): English version, 🧠🐜 title, links to versioned vault notes

Traduction fidele du README (tip 99ccc79) : meme structure, memes chiffres
(identite ordonnee des 627 nombres verifiee), etiquettes [VERIFIED]/[HYPOTHESIS].
Liens relatifs vers les notes vault committees sur main (5b977eb).

Co-Authored-By: Malik & Claude
$ git push origin docs/readme-2026-09-28
   99ccc79..ebec0d3  docs/readme-2026-09-28 -> docs/readme-2026-09-28
$ git ls-remote origin refs/heads/docs/readme-2026-09-28
ebec0d357011f19d46b56c5a854994377ea1316c	refs/heads/docs/readme-2026-09-28
```
**Nouveau tip (garde de R013) : `ebec0d357011f19d46b56c5a854994377ea1316c`.**

### Preuve d'identité des nombres
Normalisation : `grep -oE '[0-9][0-9 ,.]*'`, puis suppression des séparateurs finaux et de tous les espaces/virgules/points (donc `1 000` ≡ `1,000`, `0,005` ≡ `0.005`, `1,100` (fr) ≡ `1.100` (en)).
- Multiensemble brut : FR 633 nombres, EN 651. `diff` trié : **aucun nombre du français ne manque** ; 18 ajouts, tous expliqués : `99`, `79` (ligne « commit 99ccc79 » demandée) ; `2026`×4, `09`×4, `27`×4, `015`×2, `2`×2 = cibles des liens ajoutés (`vault/notes/2026-09-27-genese-suite.md` et `…-veille-procedure.md` une fois de plus chacun, `…-anteriorite-signal-intermediaire-e015-a2.md` deux fois).
- Suite **ordonnée**, après retrait des seuls chemins `vault/notes/2026-09-27-*.md` et de « commit 99ccc79 » :
```
FR 627 nombres, EN 627 nombres ; diff vide → ORDERED IDENTICAL
shasum : 71da680cb9e5358b645aa1a0a63aa048e9588ef9 (fr) = 71da680cb9e5358b645aa1a0a63aa048e9588ef9 (en)
```
Aucun chiffre modifié ; aucun chiffre ne m'a paru faux à signaler.

### Autres contrôles [VÉRIFIÉ]
- « pas encore versionnée » : 0 occurrence ; les 3 mentions sont remplacées par des liens relatifs (genese-suite l.9, veille-procedure entrée E009, anteriorité dans « Open leads » avec `[VERIFIED — sources listed in the note]`). Les 3 cibles existent sur `origin/main` (`git cat-file -e` OK). J'ai vérifié que la note d'antériorité contient bien les sources (MCC, PowerPlay, DreamCoder, HOUDINI, CRL, novelty search) et le verdict « chaque brique existe séparément… personne n'a assemblé ».
- Emojis : 🧠 ×2 (H1 + titre « Method »), 🐜 ×2 (H1 + entrée E013 « the insect »).
- Tableaux : 3 colonnes max. Aucune mention de l'enfant de Malik (`grep -iE 'fils|enfant|son of|child'` vide). Licence : « to be decided ».
- Codes gardés tels quels : E0xx, R0xx, `ECH0`, `DONNÉ` (nom de condition dans le README d'E016), I2, R0, R2, X1. Dates gardées au format jj/mm (pour l'identité des nombres).

### Écarts / remarques
- Aucune citation directe de Malik entre guillemets dans le README source (consignes paraphrasées) → pas de « (translated) » nécessaire ; la consigne de 20:35 reste paraphrasée.
- Verdicts de revue traduits : GO / RESERVATION / BROKEN (source : GO / RÉSERVE / CASSÉ).
- « Mon approximation différentiable de MDL » (E011) rendu par « Our … » (cohérence de voix du README).

### Rituels de fin
- `vault/reprise/F01.md` mis à jour ; commit `d87052f` sur `main` (vault seul), poussé.
- `events.jsonl` : ligne `RAPPORT_RENDU` (ts 2026-09-28T08:12:06+02:00) ; `state.json` : seule `windows.F01` modifiée (assertions : autres clés et autres fenêtres identiques ; `next_mandat_id` = M0037 présent). Hors git (ignoré).
```
$ git ls-remote origin refs/heads/main
d87052fb2df08e0791bdeb5d655886a144ea1044	refs/heads/main
$ git ls-remote origin refs/heads/docs/readme-2026-09-28
ebec0d357011f19d46b56c5a854994377ea1316c	refs/heads/docs/readme-2026-09-28
```

```
M0036
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
