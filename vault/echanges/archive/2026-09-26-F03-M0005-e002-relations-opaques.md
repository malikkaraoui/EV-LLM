---
date: 2026-09-26
tags: [e002, acquerir, banc, etalons]
session: F03
mandat: e002-relations-opaques
mandat_id: M0005
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F03-M0005
branche: exp/e002-relations-opaques
derniere_maj: 2026-09-26T15:53:49+0200
---

# M0005 — E002 : chambre aux relations opaques (générateur, oracle, étalons)

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


Modèle : `opus --effort medium` (barème `realisation_standard`) — code moyen, protocole spécifié ci-dessous.

## 0. Contexte (lis d'abord)
Lis sur `origin/main` : `architecture_cognitive_post_transformer.md` §1 bis (bloc v2.1), §11 v2, §14 v2, §28 v2, **§29 v2 et v2.1 (« chambre aux relations opaques », « deux tests »)**, §56 v2, §63 ; et `GENESE.md` (entrées du 25/09). C'est le **test « ACQUÉRIR »** : la règle n'est pas donnée, le système doit découvrir les propriétés des relations, puis résoudre le monde suivant plus vite. Ce mandat construit le **banc** et les **étalons** — PAS encore l'architecture candidate. Aucun appel réseau, aucun LLM.

## 1. Gardes — tout écart : STOP + rapport
1. `git -C /Users/malik/Documents/EV-LLM fetch origin` ; `origin/main` contient `7c453b16b9423a17d1394239724ffc256203f771`.
2. Branche `exp/e002-relations-opaques` et dossier `/Users/malik/Documents/EV-LLM/.claude/worktrees/F03-M0005` absents (local et origin).
3. `python3 --version` ≥ 3.9.

## 2. Mission 1 — worktree
`git -C /Users/malik/Documents/EV-LLM worktree add -b exp/e002-relations-opaques /Users/malik/Documents/EV-LLM/.claude/worktrees/F03-M0005 origin/main`. Tout le travail dans `W=…/F03-M0005`, sous `research/experiments/E002-relations-opaques/`. **Python stdlib uniquement.**

### 1a. `PREREGISTREMENT.md` — écrit et committé AVANT tout code d'évaluation
Contient, figés : les propriétés possibles d'une relation (transitive, symétrique, antisymétrique, réflexive, composition R_i∘R_j=R_k, **aucune**) ; la proportion minimale de relations « pièges » non transitives (≥ 30 %) ; le taux de bruit (5–10 % d'observations fausses, étiquetées dans l'oracle seulement) ; la définition des 4 étiquettes de sortie (DÉDUIT avec preuve, HYPOTHÈSE, CONTRADICTION avec règle citée, INDÉTERMINÉ avec manque) ; la **métrique R en bits** (§28 v2 : bits économisés pour prédire des observations tenues à l'écart / bits d'expérience reçus, requêtes comprises) ; la définition du **transfert** (monde n+1 réutilisant les mêmes propriétés sous d'autres noms) ; le critère d'échec d'un système (ex. : pas d'accélération sur 5 mondes consécutifs). Commit séparé : `docs(e002): preregistrement`.

### 1b. Code
- `monde.py` : générateur **déterministe par graine** d'un monde : n entités, k relations opaques `R1…Rk` aux propriétés tirées selon le préenregistrement, faits vrais, observations (avec bruit), sémantique écrite (ex. exclusion). Sérialisable JSON.
- `oracle.py` : vérité terrain — fermeture selon les propriétés, réponse attendue (avec étiquette) à toute requête `R(x,y) ?`, et détection de contradiction définie. Coût d'une requête en bits documenté.
- `interface.py` : l'**environnement interactif** vu par un système : il reçoit des observations, peut poser des requêtes (payantes en bits), et doit rendre des réponses étiquetées ; tout est journalisé pour le calcul de R.
- `etalons.py` — trois étalons de référence (§56 v2) :
  1. **aléatoire** (plancher) ;
  2. **oracle-propriétés** : solveur écrit à la main à qui l'on DONNE les propriétés (plafond « savoir ») ;
  3. **découvreur naïf** : ne connaît pas les propriétés, teste par requêtes l'hypothèse « Ri est transitive/symétrique… » puis l'applique — premier étalon « acquérir », volontairement simple.
- `evaluer.py` : fait tourner un système sur une suite de mondes (graines fixées), calcule par monde : exactitude par étiquette, précision de CONTRADICTION/INDÉTERMINÉ, requêtes utilisées, R en bits, et la **courbe monde n → n+1** (transfert).
- `tests/` : unittest (générateur déterministe, oracle cohérent sur des cas écrits à la main — dont le cas A>B>C>D, E>A, exclusion définie vs non définie de §29 v2.1 variantes A/B —, calcul de R sur un exemple calculé à la main). `python3 -m unittest discover` vert.

### 1c. Exécution
Lance `evaluer.py` sur **20 mondes** (graines 1–20 écrites dans le préenregistrement) pour les 3 étalons. Sorties dans `results/<horodatage>/` (JSON + `summary.md`) — elles sont publiques et ne contiennent rien de sensible : committe-les.

### 1d. `README.md` — Hypothèse, Protocole (renvoi au préenregistrement), Comment rejouer (commande exacte), Résultats (tableau), **Lecture** étiquetée [VÉRIFIÉ]/[HYPOTHÈSE] : l'écart plafond/découvreur, le découvreur s'accélère-t-il d'un monde à l'autre (il ne devrait pas : il ne garde rien — c'est le point de comparaison pour la future architecture), ce que ça dit de la difficulté du banc. Limites. « Prochaine étape proposée » en 3 lignes.

### 1e. Commits ciblés sous `research/experiments/E002-relations-opaques/` uniquement ; push de la branche.

## 3. STOP supplémentaires
Toute envie de modifier le préenregistrement après avoir vu des résultats (décris-la au rapport) ; tout besoin de dépendance hors stdlib ; conflit git.

## 4. Preuves
Gardes ; sha du commit de préenregistrement antérieur aux commits de code (`git log --oneline`) ; tests verts (sortie) ; tableau de résultats collé ; `git log -1 --format=%B <tip>` ; `ls-remote` branche et main.

## Rituels

DÉBUT : `statut: en-cours` à la racine du frontmatter de CE fichier, avant tout.

FIN, dans l'ordre :
1. Rapport appendé sous `## Rapport M0005` (preuves collées).
2. `vault/reprise/F03.md` (état + prochaine étape) — à la racine.
3. Une ligne `vault/runtime/events.jsonl` (`src: "fenetre"`, `type: "RAPPORT_RENDU"`, `f`, `mandat`, `note` ≤ 200 car.) + `windows.F03` dans `vault/runtime/state.json` (remplace SEULEMENT ta fenêtre) — hors git, jamais committés.
4. Commit de `vault/reprise/F03.md` sur `main` à la racine (vault seul) + push + `git ls-remote origin refs/heads/main` collé.
5. Ta branche (s'il y en a une) poussée + `git ls-remote origin refs/heads/<branche>` collé.
6. Footer de statut, toute dernière ligne du rapport :
```
M0005
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

## Rapport M0005

**Rendu : banc E002 construit, testé et exécuté (20 mondes × 3 étalons), branche poussée. Un STOP supplémentaire du §3 s'est déclenché (envie de modifier le préenregistrement) : je ne l'ai PAS modifié, la question est posée ci-dessous.**

### Gardes [VÉRIFIÉ]
- `git fetch origin` OK ; `7c453b16b9423a17d1394239724ffc256203f771` est ancêtre de `origin/main` (`ANCETRE_OK`).
- Branche `exp/e002-relations-opaques` absente en local et sur origin ; dossier `.claude/worktrees/F03-M0005` absent (`No such file or directory`).
- `Python 3.9.6`.

### Ce qui a été fait
- Worktree `.claude/worktrees/F03-M0005`, créé depuis `origin/main` (`7c453b1`). Tout est sous `research/experiments/E002-relations-opaques/`, en Python standard uniquement.
- **Préenregistrement** committé **avant** le code : il fixe le monde, les types, ≥ 30 % de pièges, le bruit de 5 à 10 % (dont une inversion ciblée en phase 2), les 4 étiquettes, R en bits, le transfert par familles de 5 mondes, le critère d'échec et les étalons.
- **Code :**
  - `monde.py`, `raisonneur.py` (chaînage de Horn avec provenance, vérificateur de preuve) ;
  - `oracle.py`, `interface.py`, `etalons.py`, `evaluer.py` ;
  - `tests/` (22 tests) ;
  - `diagnostic_sans_bruit.py` (hors protocole, marqué comme tel).
- **Contrôle des tests :** 10 mutations injectées une à une dans une copie. Les 10 font échouer la suite. 3 passaient au premier essai (probabilité d'un DÉDUIT, `CYCLE_PIEGE`, règle « violation nouvelle ») : j'ai renforcé les tests correspondants **avant** l'exécution officielle.
- **Déterminisme :** une 2e exécution, dans le scratchpad, donne un `resultats.json` identique (`DETERMINISTE_IDENTIQUE`).

### Preuves

Ordre des commits (le préenregistrement précède le code) :
```
1cb586b feat(e002): execution 20 mondes x 3 etalons + README
340f99d feat(e002): banc relations opaques -- generateur, oracle, interface, etalons, evaluation
d8ef3a1 docs(e002): preregistrement
7c453b1 docs(vault): reprise F01 -- M0002 rendu (T1 mesure, T2 non mesure)
```
`git merge-base --is-ancestor d8ef3a1 340f99d` → `PREREG_AVANT_CODE`. Périmètre `git diff --name-only 7c453b1..HEAD` → uniquement `research/experiments/E002-relations-opaques/` (`PERIMETRE_OK`, 13 fichiers).

Tests :
```
$ python3 -m unittest discover
Ran 22 tests in 0.264s

OK
```

Résultats `results/2026-09-26T160728+0200/summary.md` (moyennes sur 20 mondes, phase 2) :

| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | précision CONTRA | rappel CONTRA | précision INDÉT | exclusions justes /3 | requêtes | bits exp. | bits économisés | R | R̂ | révisions requises justes | sur-révisions | critère ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aleatoire | 0.328 | 0.767 | 9.1 | 0.000 | 0.070 | 0.282 | 0.505 | 1.05 | 0.0 | 909 | -33.3 | -0.037 | -3.962 | 44/275 | 1105/1385 | ECHEC (0/4 familles) |
| oracle_proprietes | 1.000 | 0.000 | 4.7 | 1.000 | 1.000 | 1.000 | 1.000 | 3.00 | 0.0 | 909 | -2.8 | -0.003 | 1.000 | 275/275 | 0/1385 | ECHEC (0/4 familles) |
| decouvreur_naif | 0.777 | 0.258 | 8.3 | 0.679 | 0.383 | 0.889 | 0.916 | 3.00 | 62.0 | 1487 | -21.7 | -0.014 | -2.414 | 177/222 | 284/1438 | ECHEC (0/4 familles) |

Diagnostic hors protocole, mêmes mondes sans bruit : R moyen du plafond **+0.016**, positif sur 20 mondes sur 20 ; R moyen du découvreur −0.016.

`git log -1 --format=%B 1cb586b` :
```
feat(e002): execution 20 mondes x 3 etalons + README

Resultats 2026-09-26T160728+0200. Plafond R moyen -0.003 (positif
8/20) : le bruit preenregistre se propage par deduction ; R-chapeau
indefini sur 12/20 mondes, courbe de transfert non mesurable en l'etat
(ecart au preenregistrement, rapporte, non corrige). Decouvreur naif :
exactitude 0.777, 25.8 % de DEDUIT infondes, 45/161 proprietes
acceptees a tort. Diagnostic hors protocole sans bruit.

Co-Authored-By: Malik & Claude
```

### Lecture (détail dans le README)
- [VÉRIFIÉ] **Le plafond « savoir » ne bat pas le prédicteur de fréquence avec le bruit préenregistré.**
  - R = −0.003 en moyenne, positif dans 8 mondes sur 20.
  - Toutes ses erreurs en vérité ont une prémisse bruitée : c'est vérifié sur les graines 6, 7 et 9, et le diagnostic sans bruit donne R > 0 dans les 20 mondes.
- [VÉRIFIÉ] **R̂ = R/R_plafond est indéfini dans 12 mondes sur 20.** La courbe de transfert du §3 n'est pas mesurable en l'état, et les verdicts « ÉCHEC » en découlent en partie.
- [VÉRIFIÉ] **Le découvreur naïf** : 45 propriétés acceptées à tort sur 161, dont 29 compositions (il teste seulement le sens ⊆, avec 3 confirmations). Son R reste négatif même sans bruit.
- [VÉRIFIÉ] **Le Test 1 A/B tient :** 3 questions d'exclusion justes sur 3 dans les 20 mondes, pour le plafond comme pour le découvreur.
- Aucune conclusion générale : 20 mondes, un seul jeu de paramètres.

### STOP supplémentaire (§3) : envie de modifier le préenregistrement, NON exécutée
- **Constat :** avec le bruit préenregistré (5 à 10 %, ε = 1/64), le plafond a R ≤ 0 dans 12 mondes sur 20. Le dénominateur de R̂ n'y a donc pas de sens, et le critère d'accélération est inopérant. Aucun étalon ne peut réussir ni échouer de façon informative.
- **Question que j'aurais posée :** faut-il amender la définition de R̂ et du plafond (dans un E002-bis, préenregistré à nouveau), ou garder le préenregistrement tel quel et accepter que le critère ACQUÉRIR ne soit pas mesurable sur ce banc ?
- **Options :**
  - (a) R̂ en **différence** : `R − R_plafond`, toujours défini ;
  - (b) un plafond « savoir + vérifie par requête les prémisses de ses déductions », qui reste positif sous bruit ;
  - (c) baisser le bruit ou adoucir ε ;
  - (d) ne rien changer.
- **Mon choix :** (a) + (b), dans un **E002-bis** préenregistré à part. Raison : (c) rendrait le banc plus facile au lieu de réparer la mesure, et le bruit est justement ce qui rend le banc discriminant (§11 v2, hiérarchie de confiance). E002 reste tel quel : c'est un résultat.
- Je n'ai pas bloqué le reste du mandat : le préenregistrement est intact (`d8ef3a1`) et l'écart est écrit dans le README et le message de commit.

### Autres écarts ou remarques
- Le tirage des profils a produit 60 à 80 % de relations non transitives (minimum préenregistré : 30 %). Les familles 1 et 3 n'ont aucune composition.
- La branche a d'abord hérité du suivi de `origin/main` (effet de `worktree add -b … origin/main`). J'ai poussé avec un refspec explicite `exp/e002-relations-opaques:exp/e002-relations-opaques -u` : le suivi pointe maintenant vers la branche distante.
- Je n'ai touché ni `.env`, ni les fichiers interdits.

### Push
```
$ git ls-remote origin refs/heads/main
436c8fa328754e56df78554576da1c30205d61ae	refs/heads/main
$ git ls-remote origin refs/heads/exp/e002-relations-opaques
1cb586bd6976e17dd1169a7f3b192ad5e4c04c9e	refs/heads/exp/e002-relations-opaques
```
(`main` : commit vault seul `436c8fa`, `vault/reprise/F03.md`. `events.jsonl` et `state.json` (`windows.F03`) sont à jour, hors git.)

```
M0005
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
