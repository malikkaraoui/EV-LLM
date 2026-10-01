---
date: 2026-09-28
tags: [readme, correctif, r013]
session: F01
mandat: readme-correctifs-r013
mandat_id: M0038
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F01-M0035
branche: docs/readme-2026-09-28
derniere_maj: 2026-09-28T09:03:51+0200
---

# M0038 — README racine : correctifs demandés par la relecture R013 (formule E012, puce « interface », 4 précisions), sans autre changement

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

Modèle : `opus --effort medium`. **Aucun calcul.** Six retouches de texte, chacune recontrôlée contre sa source AVANT d'être écrite.

## 0. Contexte
R013 (`vault/revues/2026-09-28-R013-readme-licence.md`, main `ddf13d1` — lis-le EN ENTIER) : RÉSERVE 7/9. Axe 2 : formule E012 déformée (l.141). Axe 5 : puce l.190 [VERIFIED] non portée par ses sources ; 4 imprécisions (l.61, l.148, l.180, l.189). L'orchestrateur a recontrôlé les deux défauts bloquants : fondés. Leçon R013 : une identité de nombres ne vérifie ni les formules ni le rattachement des étiquettes.

## 1. Gardes
`fetch` ; `git rev-parse origin/docs/readme-2026-09-28` = `6812d1045c9973036c7054ed5091cc315e59e806` ; worktree `.claude/worktrees/F01-M0035` sur la branche, propre (sinon worktree neuf `F01-M0038`). STOP si écart.

## 2. Les six retouches (README.md, branche). Pour CHACUNE : ouvre la source au tip indiqué, colle au rapport la ligne source et le « avant → après ». Si la source contredit la formulation proposée ci-dessous, c'est la source qui gagne : tu écris ce qu'elle dit et tu le signales.
1. **l.141 (E012, source `git show 0a33881:research/experiments/E012-evolution/README.md` l.28–29)** : remplacer `h = step(a + b + h − 9)`, `output = a + b + h − 10·h` par `h(t) = step(a + b + h(t−1) − 9)`, `output = a + b + h(t−1) − 10·h(t)`.
2. **l.190 (sources : E014 `fc698b4` README l.61–65 ; E015 `58abf67` README l.33, l.77, l.90–99 ; E016 `867ccaf` `resultats/resultats.json` DONNE)** : remplacer la puce entière par : `- [VERIFIED — E014, E015 ECH0, E016 DONNÉ] **What got over the wall: a discrete symbolic interface between frozen skills.** Two frozen skills connected by symbols compose without retraining: exact at 16 and 100 digits on 4/5 seeds when the interface is given (E014 R1G), on 2/5 seeds when the wiring is given and the interface must be invented (E015 ECH0), and on 9/9 pairs × 5/5 seeds when the interface is given (E016 DONNÉ, 100 % at 100 digits). At 1,000 digits it holds only sometimes: 1/5 (E014), 2/5 (ECH0), 71.7 % (DONNÉ). The remaining limits come from reading, not from computing.`
3. **l.189 (source E014 `fc698b4` l.61–65)** : « Every time the system must find on its own which digit to read, it fails beyond seen lengths » → « Whenever the system must find on its own which digit to read, it fails beyond seen lengths — the single exception being one seed out of five with a curriculum (E014 R0b, 1/5 at 16 and 100 digits) ». Garde le reste de la puce.
4. **l.180 (source E016-A2 `1c98601` `resultats/a2/pilotes.json`)** : « Senders freeze even faster (entropy 0.002 nat) » → « Senders freeze even faster (entropy 0.002 nat for the dense-signal pilot, 0.018 for the curriculum one, against 0.03–0.16 in E016) » — vérifie 0,03–0,16 dans le README E016 (`867ccaf`, section entropie/effondrement, ≈ l.125) ; si la plage exacte diffère, écris celle du README.
5. **l.61 (source E005 `15487b0` README l.108)** : « The 13 correct sentences are judged correct » → « The 13 evaluations of correct sentences are all conforming (13/13) ».
6. **l.148 (source E013 `044545e` README l.100)** : « pure carry propagation drops to 52.9 % (1 seed out of 5) » → « pure carry propagation drops to 52.9 % on average (± 40.5) at 1,000 digits, with 1 seed out of 5 above 90 % » — adapte à la phrase existante sans en changer le reste.

Rien d'autre ne change : `git diff --stat 6812d10..HEAD` = `README.md` seul, et `git diff 6812d10..HEAD` ne montre que ces six zones. Contrôle final : `grep -c '\[VERIFIED' README.md` inchangé ; H1 inchangé ; `grep -inE "his (son|child)|malik's (son|child)"` vide.

## 3. Commit et preuves
Commit heredoc : `docs(readme): fixes from review R013 -- E012 formula indices, interface claim, 4 precisions` + trailer. Push ; `git ls-remote origin refs/heads/docs/readme-2026-09-28` collé (nouveau tip = garde de R014). Au rapport : les six « source / avant / après », `git diff --stat`, `git log -1 --format=%B`.

## 4. STOP
Garde en écart · une source qui ne dit pas ce que le mandat suppose ET dont tu ne peux pas tirer une formulation exacte → laisse la ligne telle quelle, signale-la, continue les autres.

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

## Rapport M0038

**Rendu : six retouches appliquées sur `docs/readme-2026-09-28`, nouveau tip `f99553a`.** Chaque retouche a été recontrôlée contre sa source au tip indiqué avant écriture. Il y a deux écarts avec la formulation du mandat, tous deux imposés par la source (retouches 2 et 4, détail ci-dessous).

### Gardes [VÉRIFIÉ]
```
$ git fetch origin ; git rev-parse origin/docs/readme-2026-09-28
6812d1045c9973036c7054ed5091cc315e59e806
$ git -C .claude/worktrees/F01-M0035 branch --show-current ; status --porcelain ; rev-parse HEAD
docs/readme-2026-09-28
(vide)
6812d1045c9973036c7054ed5091cc315e59e806
```
R013 lu en entier.

### Les six retouches : source / avant / après

**1. l.141, E012** [VÉRIFIÉ]
- Source : `git show 0a33881:research/experiments/E012-evolution/README.md` l.28–29 : `h1     = marche(a + b + h1(t−1) − 9)` / `sortie = id(a + b + h1(t−1) − 10·h1)`.
- Avant : `` `h = step(a + b + h − 9)`, `output = a + b + h − 10·h` ``
- Après : `` `h(t) = step(a + b + h(t−1) − 9)`, `output = a + b + h(t−1) − 10·h(t)` `` (conforme au mandat).

**2. l.190, puce « What got over the wall »** [VÉRIFIÉ]. **Écart avec le mandat**, imposé par la source.
- Sources :
  - E014 `fc698b4` l.63 : `| **R1G** (gelé, sans joint) | **4/5 / 4/5 / 1/5** |`, colonne « graines ≥ 90 % à 16 / 100 / 1 000 ».
  - E014 l.71 : `R1G : s1 100/100/23,0 ; s2 100/98,4/3,0 ; s3 100/100/89,5 ; s4 100/100/91,0 ; s5 0/0/0`.
  - E015 `58abf67` l.33 : « Avec le câblage entier donné (ECH0), 2/5 graines réussissent ».
  - E015 l.77 : « ECH0 reçoit **tout le câblage** N1 ». E015 l.75–76 : la table d'interface n'est pas donnée.
  - E015 l.93 : ECH0 2/5, 40,0 ± 49,0 à 100 et à 1 000.
  - E015 l.107–108 : s1 et s3 font 100 / 100 / 100.
  - E016 `867ccaf` `resultats.json` DONNE : 5 graines × 9 paires, T-LONG|16 = T-LONG|100 = 1.0 partout.
  - E016 README l.76 : `DONNÉ | 5/5 | 9 ; 9 ; 9 ; 9 ; 9 | 100,0 ± 0,0 | 100,0 | 71,7`.
- **Écart** : le mandat proposait « exact at 16 and 100 digits on 4/5 seeds » pour E014 R1G. C'est faux au sens strict, car la graine s2 fait 98,4 % à 100 chiffres. 4/5 est le critère ≥ 90 % (l.63), et seules 3/5 graines sont exactes à 100. J'ai donc écrit « at least 90 % exact » pour E014. Pour ECH0, « 100 % on 2/5 seeds » est exact (l.107–108).
- Avant : `- [VERIFIED — E014, E015 ECH0, E016 DONNÉ] **What got over the wall: a given discrete symbolic interface.** Two frozen skills, connected by symbols, compose without loss up to 100 digits, and often up to 1,000. The remaining limits come from reading, not from computing.`
- Après : `- [VERIFIED — E014, E015 ECH0, E016 DONNÉ] **What got over the wall: a discrete symbolic interface between frozen skills.** Two frozen skills connected by symbols compose without retraining: at least 90 % exact at 16 and 100 digits on 4/5 seeds when the interface is given (E014 R1G), 100 % on 2/5 seeds when the wiring is given and the interface must be invented (E015 ECH0), and on 9/9 pairs × 5/5 seeds when the interface is given (E016 DONNÉ, 100 % at 100 digits). At 1,000 digits it holds only sometimes: 1/5 (E014), 2/5 (ECH0), 71.7 % (DONNÉ). The remaining limits come from reading, not from computing.`
- À 1 000 chiffres :
  - E014 1/5 : l.63, s4 = 91,0.
  - ECH0 2/5 : l.107–108.
  - DONNÉ 71,7 : l.76.
  - Les compétences sont bien gelées dans les trois cas : E014 « gelé » (l.63), E015 « 10 champions gelés » (l.51), E016 « gelés » (l.9).

**3. l.189** [VÉRIFIÉ]
- Sources : E014 `fc698b4` l.47 (`R0b — I2 + curriculum`), l.62 (`R0b | 1/5 / 1/5 / 0/5`), l.70 (`s2 100/99,8/62,5`).
- Avant : « Every time the system must find on its own which digit to read, it fails beyond seen lengths, whatever its size (from ~1,900 parameters to ~3.2 million). »
- Après : « Whenever the system must find on its own which digit to read, it fails beyond seen lengths, whatever its size (from ~1,900 parameters to ~3.2 million) — the single exception being one seed out of five with a curriculum (E014 R0b, 1/5 at 16 and 100 digits). »
- La parenthèse de taille est conservée. L'exception est placée en fin de phrase pour la lisibilité. Je n'ai pas écrit « exact », car R0b s2 fait 99,8 % à 100 chiffres.

**4. l.180, E016-A2** [VÉRIFIÉ]. Précision ajoutée au mandat.
- Sources :
  - `1c98601` `resultats/a2/pilotes.json` l.49 : `IND-dense … "entropie_emetteurs": 0.002`. L.100 : `IND-01-curric … "entropie_emetteurs": 0.018`.
  - E016 README `867ccaf` l.125–126 : « 0,07–0,23 nat (COLL) et 0,03–0,16 (IND) ».
- La plage 0,03–0,16 est **celle d'IND seul** ; COLL est à 0,07–0,23. J'ai donc écrit « for IND in E016 », plutôt que « in E016 » seul qui laisserait croire que la plage couvre tout E016.
- Avant : « Senders freeze even faster (entropy 0.002 nat). »
- Après : « Senders freeze even faster (entropy 0.002 nat for the dense-signal pilot, 0.018 for the curriculum one, against 0.03–0.16 for IND in E016). »

**5. l.61, E005** [VÉRIFIÉ]
- Source : `15487b0` E005 README l.108 : « Les 13 évaluations de phrases justes sont conformes (13/13). »
- Avant : « The 13 correct sentences are judged correct; »
- Après : « The 13 evaluations of correct sentences are all conforming (13/13); »

**6. l.148, E013** [VÉRIFIÉ]
- Sources : `044545e` E013 README l.100 : `I3 N = 1 000 | … | **52,9 ± 40,5** | **4/5 / 3/5 / 1/5** | … 102/102/102 …`. L.172 : « 52,9 ± 40,5 % à 1 000 (1/5) ».
- Avant : « pure carry propagation drops to 52.9 % (1 seed out of 5); »
- Après : « pure carry propagation drops to 52.9 % on average (± 40.5) at 1,000 digits, with 1 seed out of 5 above 90 %; »
- Le reste de la phrase est inchangé. La seule graine réussie est à 102/102, soit 100 % : « above 90 % » est donc exact.

### Contrôles [VÉRIFIÉ]
```
$ git diff --stat 6812d10..HEAD
 README.md | 12 ++++++------
 1 file changed, 6 insertions(+), 6 deletions(-)
$ git diff -U0 6812d10 | grep '^@@'   → @@ -61 @@, -141, -148, -180, -189,2 (six zones exactement)
$ grep -c '\[VERIFIED' README.md      → 7 (avant : 7)
$ head -1 README.md                   → # 🧠🐜 EV-LLM — a public research log
$ grep -inE "his (son|child)|malik's (son|child)" README.md → vide (rc=1)
$ git log -1 --format=%B
docs(readme): fixes from review R013 -- E012 formula indices, interface claim, 4 precisions

Co-Authored-By: Malik & Claude
$ git ls-remote origin refs/heads/docs/readme-2026-09-28
f99553a89ff4af7fd4c873c232c06d4aaeef9887	refs/heads/docs/readme-2026-09-28
```
**Garde de R014 : `f99553a89ff4af7fd4c873c232c06d4aaeef9887`.**

Leçon, candidate transverse (R5) : proposer une formulation corrigée sans la confronter aux données par graine réintroduit le défaut qu'on corrige. Ici, « exact » contre ≥ 90 % pour E014 R1G à 100 chiffres. Un correctif est lui-même une affirmation, à recontrôler contre sa source.

### Fin de rituels [VÉRIFIÉ]
- `vault/reprise/F01.md` a été réécrit et commité sur `main` : `53fb97f` (vault seul).
- `events.jsonl` : une ligne `RAPPORT_RENDU` ajoutée.
- `state.json` : seule la clé `windows.F01` a été modifiée ; les autres clés sont identiques (vérifié par assertion) et `next_mandat_id` = M0039 est toujours présent.
```
$ git ls-remote origin refs/heads/main
53fb97f731880077cdfbc4f6acf445720d277d0f	refs/heads/main
$ git ls-remote origin refs/heads/docs/readme-2026-09-28
f99553a89ff4af7fd4c873c232c06d4aaeef9887	refs/heads/docs/readme-2026-09-28
```

```
M0038
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
