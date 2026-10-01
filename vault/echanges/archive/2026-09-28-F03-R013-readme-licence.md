---
date: 2026-09-28
tags: [doublage, readme, licence, merge]
session: F03
mandat: doublage-readme-licence
mandat_id: R013
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F03-R013
branche: docs/readme-2026-09-28
derniere_maj: 2026-09-28T08:41:34+02:00
---

# R013 — Relecture indépendante du README racine + LICENSE (branche `docs/readme-2026-09-28`, tip 6812d10), puis merge si GO

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

Modèle : `opus --effort medium` (barème `doublage_adversarial`). **Aucun calcul, aucun entraînement, aucun appel d'API.** Tu relis de la documentation : la rigueur porte sur les chiffres et les liens, pas sur du code.

## 0. Rôle et contexte
Tu es le **relecteur indépendant**. La branche `docs/readme-2026-09-28` ajoute deux fichiers à la racine : `README.md` (journal de recherche public, en anglais, 284 lignes) et `LICENSE` (MIT). Trois mandats l'ont produite : M0035 (version française, chaque chiffre sourcé « fichier:ligne »), M0036 (traduction anglaise, preuve d'identité ordonnée de 627 nombres, notes du vault versionnées sur main `5b977eb`), M0037 (LICENSE + section License). Rapports à lire EN ENTIER : `vault/echanges/archive/2026-09-28-F01-M0035-readme-racine.md`, `…-M0036-readme-anglais.md`, `…-M0037-licence-mit.md`. Décision Malik (28/09 08:14) : licence MIT pour tout. Consignes Malik sur le README : anglais ; titre H1 avec 🧠 et 🐜 ; échecs publiés comme résultats ; méthode affichée (antériorité, pas de refaire le publié, contre-pied, itération rapide, quelques neurones, petit CPU) ; ton de scientifique sur GitHub ; **aucune mention de son enfant**.

## 1. Gardes — tout écart : STOP + rapport (footer BLOCKED)
1. `git -C /Users/malik/Documents/EV-LLM fetch origin` ; `git rev-parse origin/docs/readme-2026-09-28` = `6812d1045c9973036c7054ed5091cc315e59e806`.
2. `git ls-tree origin/main README.md LICENSE` → vide (rien à écraser côté main).
3. `vault/revues/` ne contient pas déjà un rapport R013.

## 2. Mission 1 — relecture (worktree DÉTACHÉ, lecture seule)
`git -C /Users/malik/Documents/EV-LLM worktree add --detach /Users/malik/Documents/EV-LLM/.claude/worktrees/F03-R013 6812d1045c9973036c7054ed5091cc315e59e806`. Tu n'y modifies RIEN.

Axes, chacun ✅ GO / ⚠️ réserve / ⛔ CASSÉ avec la RAISON vérifiée (commande + sortie) :
1. **Périmètre** : `git diff --name-only $(git merge-base origin/main 6812d10) 6812d10` = exactement `LICENSE` et `README.md`. Autre chose = ⛔.
2. **Chiffres** : tire **au moins 15 chiffres** répartis sur les 21 entrées du journal (pas seulement ceux que M0035 a listés — choisis-en toi-même), et vérifie chacun dans le README de l'expérience **au tip de sa branche** (`git show origin/<branche>:research/experiments/<dossier>/README.md`, liste des tips dans le rapport M0035). Un chiffre absent ou différent = ⛔ ; un chiffre présent mais dont le contexte est déformé (ex. une moyenne présentée comme un maximum) = ⚠️.
3. **Verdicts et statuts de relecture** : pour chaque entrée, le statut annoncé (« reviewed GO / merged », « reviewed with reservation », « not yet reviewed ») est-il vrai ? Vérifie contre `vault/revues/*.md` (frontmatter `verdict:`) et `git branch -r --merged origin/main`. Un statut faux = ⛔.
4. **Liens** : chaque lien relatif existe sur `main` ou sur la branche (`git cat-file -e`) ; chaque lien `tree/<branche>/<dossier>` pointe vers une branche distante existante et un dossier existant au tip. Lien mort = ⛔.
5. **Honnêteté** : le texte présente-t-il les échecs comme des résultats, sans les enjoliver ni les minimiser ? Aucune promesse, aucun superlatif, aucune conclusion générale non étiquetée ? Étiquettes [VERIFIED]/[HYPOTHESIS] cohérentes avec les README sources (un [VERIFIED] du README racine doit correspondre à un [VÉRIFIÉ] du README d'expérience ou à un chiffre publié) ? Écart = ⚠️ minimum.
6. **Consignes Malik** : H1 = `# 🧠🐜 EV-LLM — a public research log` ; anglais partout (résidus français hors noms propres, codes, citations = ⚠️) ; méthode en tête ; `grep -inE "son|child|kid|fils|enfant"` → aucune mention de l'enfant de Malik (une occurrence = ⛔) ; section License = MIT avec lien vers `LICENSE`.
7. **LICENSE** : texte MIT standard intégral (compare mot à mot avec le texte de référence https://opensource.org/license/mit — si le réseau est refusé, compare avec ta connaissance du texte et dis-le [MÉMOIRE]) ; ligne `Copyright (c) 2026 Malik Karaoui` ; 21 lignes ; rien d'autre.
8. **Sécurité dépôt public** : `git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 6812d10 -- README.md LICENSE` → rien ; aucune adresse e-mail personnelle, aucun identifiant de compte.
9. **Hygiène git** : trailer `Co-Authored-By: Malik & Claude` sur les 4 commits de la branche (`git log --format=%B origin/main..6812d10`).

Rapport : `vault/revues/2026-09-28-R013-readme-licence.md`, frontmatter EXACT :
```
---
date: 2026-09-28
revue: R013
branche: docs/readme-2026-09-28
tip: 6812d1045c9973036c7054ed5091cc315e59e806
verdict: <GO | RESERVE | CASSE>
---
```
puis les 9 axes et les preuves (liste des 15+ chiffres vérifiés avec fichier:ligne). **GO seulement si les 9 axes sont ✅.** Réserve ou CASSÉ → pas de merge : rapport sur `main` à la racine (vault seul), commit, push, rendu.

## 3. Mission 2 — merge (SEULEMENT si GO)
```
R=/Users/malik/Documents/EV-LLM ; S=$R/.claude/worktrees/F03-merge
git -C $R fetch origin && git -C $R worktree add --detach $S origin/main
git -C $S merge --no-ff 6812d1045c9973036c7054ed5091cc315e59e806 -m "Merge docs/readme-2026-09-28 [R013]" -m "Co-Authored-By: Malik & Claude"
# vérifie SUR ce résultat : README.md et LICENSE présents à la racine, head -n 1 README.md = H1 attendu
# écris le rapport GO dans $S/vault/revues/2026-09-28-R013-readme-licence.md
git -C $S add -- vault/revues/2026-09-28-R013-readme-licence.md && git -C $S commit -m "docs(revues): R013 -- GO" -m "Co-Authored-By: Malik & Claude"
git -C $R merge --ff-only $(git -C $S rev-parse HEAD)
git -C $R push origin main && git -C $R ls-remote origin refs/heads/main
git -C $R worktree remove $S ; git -C $R worktree remove $R/.claude/worktrees/F03-R013
```
- `ff-only` refusé (racine modifiée localement sur un chemin touché, ou `origin/main` a bougé) : refais le scratch UNE fois depuis `origin/main` à jour ; second refus = STOP, rapport, jamais de force.
- Le hook `pre-push` exige un rapport `verdict: GO` citant le tip : c'est la garde, normal.
- Vérifie `git merge-base --is-ancestor 6812d10 origin/main` et colle `git ls-remote`.

## 4. Mission 3 — après le merge (si GO)
Ouvre https://github.com/malikkaraoui/EV-LLM dans la sortie de `gh repo view malikkaraoui/EV-LLM --json description` si `gh auth status` réussit, uniquement pour vérifier que le README est bien rendu comme page d'accueil (la première ligne du `README.md` sur `main` suffit sinon). Ne modifie rien sur GitHub.

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

## Rapport R013

**Verdict : RÉSERVE → pas de merge (Mission 2 et Mission 3 non exécutées, conformément au mandat).** Rapport complet : `vault/revues/2026-09-28-R013-readme-licence.md` (main `ddf13d1`). Aucun calcul, aucun entraînement, aucun appel d'API ; un seul accès réseau, `curl` en lecture sur opensource.org pour l'axe 7.

### Gardes [VÉRIFIÉ]
```
$ git rev-parse origin/docs/readme-2026-09-28
6812d1045c9973036c7054ed5091cc315e59e806
$ git ls-tree origin/main README.md LICENSE        → (vide)
$ ls vault/revues/ | grep -i R013                  → (vide)
```
Worktree détaché `.claude/worktrees/F03-R013` créé au tip, rien modifié, puis retiré (`git worktree remove`, sans force).

### Axes
| # | Axe | Verdict |
|---|---|---|
| 1 | Périmètre | ✅ `LICENSE`, `README.md` seuls (merge-base 10b8774) |
| 2 | Chiffres | ⚠️ 87 renvois chiffre → ligne vérifiés sur les 21 entrées, 0 absent, 0 différent ; **la formule d'E012 (l.141) est déformée** |
| 3 | Statuts | ✅ 21/21 (revues R001–R012 + `--merged`) |
| 4 | Liens | ✅ 31/31 (`git cat-file -e`) |
| 5 | Honnêteté | ⚠️ puce l.190 [VERIFIED] non portée par ses sources ; 4 imprécisions mineures |
| 6 | Consignes Malik | ✅ (grep enfant : « sonde » seulement) |
| 7 | LICENSE | ✅ 21 lignes, identique au MIT standard et au texte OSI (`curl`) |
| 8 | Sécurité | ✅ grep secrets et e-mail rc=1 |
| 9 | Hygiène | ✅ 3/3 commits avec le trailer (le mandat disait 4 ; la branche en a 3) |

### Les deux défauts bloquants
1. **README l.141 (E012)** : `h = step(a + b + h − 9)`, `output = a + b + h − 10·h`. Lue telle quelle, la sortie vaut a + b − 9h, ce qui est faux. La source (E012 l.28–29) a `h1(t−1)` et `h1`. Le défaut vient de la version française (99ccc79 l.139). Correctif : `h(t) = step(a + b + h(t−1) − 9)`, `output = a + b + h(t−1) − 10·h(t)`.
2. **README l.190** [VERIFIED — E014, E015 ECH0, E016 DONNÉ] « a given … interface … without loss up to 100 digits, and often up to 1,000 » :
   - dans ECH0, l'interface est **à inventer** (E015 l.33, l.77) ;
   - à 1 000 chiffres, les sources donnent 1/5 (E014), 2/5 (ECH0) et 71,7 % (DONNÉ), donc pas « often » ;
   - ECH0 fait 2/5 à 100 chiffres, donc pas « without loss ».

Recommandées dans la même passe : l.189 « every time … fails » (E014 R0b : 1/5 exact à 100) ; l.180 « 0.002 nat » (IND-dense seul, curric 0,018) ; l.61 « 13 correct sentences » (ce sont 13 évaluations) ; l.148 « 52.9 % » (moyenne ± 40,5, à 1 000 chiffres).

### Question que j'aurais posée (aucune posée)
Aucune. Le mandat tranche : GO seulement si 9/9 ✅. J'ai jugé les deux défauts ⚠️ et non ⛔ : aucun chiffre n'est absent ni différent, c'est le contexte qui est déformé (règle de l'axe 2).

### Preuves git
```
$ git log -1 --format='%h %s' ddf13d1
ddf13d1 docs(revues): R013 -- RESERVE (README racine : formule E012, puce l.190)
$ git push origin main
   8be0f35..ddf13d1  main -> main
$ git push origin main   (reprise F03)
   ddf13d1..b0fdd5a  main -> main
$ git ls-remote origin refs/heads/main
b0fdd5a50ffb93f84625241e51380e0d03090964	refs/heads/main
$ git ls-remote origin refs/heads/docs/readme-2026-09-28
6812d1045c9973036c7054ed5091cc315e59e806	refs/heads/docs/readme-2026-09-28   (branche doublée, non modifiée)
```
- `vault/reprise/F03.md` réécrit et commité (`b0fdd5a`, vault seul).
- `events.jsonl` : une ligne `RAPPORT_RENDU` ajoutée (ts 2026-09-28T08:41:02+02:00).
- `state.json` : seule `windows.F03` modifiée. Assertions OK : les autres clés et les autres fenêtres sont identiques, `next_mandat_id` = M0038 et `next_revue_id` = R014 sont présents. Hors git (ignoré).

### Leçon (transverse, candidate à remontée)
Une preuve d'identité des nombres, comme celle de M0036 (627 nombres), ne vérifie ni les formules ni le rattachement des étiquettes. Une formule recopiée peut garder tous ses chiffres et devenir fausse en perdant ses indices. Pour un document de synthèse, le doublage doit relire chaque formule et chaque puce [VERIFIED] contre ses sources citées, pas seulement les nombres.

R013
Implementation      ✅
Tests               ✅
Commit              ✅
Branch push         ❌   (aucune branche propre au mandat ; doublage en lecture seule)
Review              ❌
Merge main          ❌
Main push           ✅   (vault seul)
TASK STATUS         READY_FOR_INTEGRATION
PROJECT STATUS      NOT_INTEGRATED
