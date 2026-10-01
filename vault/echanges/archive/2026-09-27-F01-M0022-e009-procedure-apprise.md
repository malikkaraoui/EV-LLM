---
date: 2026-09-27
tags: [e009, procedure, architecture, longueur]
session: F01
mandat: e009-procedure-apprise
mandat_id: M0022
statut: reponse-disponible
modele: opus
effort: medium
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F01-M0022
branche: exp/e009-procedure-apprise
derniere_maj: 2026-09-27T09:33:41+0200
---

# M0022 — E009 « A » : la procédure apprise par l'architecture (règle locale bouclée), sans donner l'alignement

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

## Cadre commun E009–E011 (décision Malik 27/09 : explorer A et B à fond)
- Question de fond : un système peut-il **apprendre la procédure** de l'addition sur des nombres courts et la généraliser à toute longueur, comme un enfant ? Palier 0 (E008, branche `exp/e008-addition`, tip `af281f5`, lire README + `vault/echanges/archive/2026-09-26-F01-M0021-e008-addition-palier0.md`) : transformer standard 0 % dès 6 chiffres ; sortie inversée + NoPE 91 % à 6, 8 % à 7, 0 % dès 8.
- **Réutilise** le code E008 (données, évaluateur unique, contrôles) **par import depuis ta branche créée à partir de `origin/exp/e008-addition`**, sans modifier `research/experiments/E008-addition/`.
- **Protocole durci (revue critique orchestrateur, sources arXiv 2108.12284, 2402.09371, 1611.00736)** — obligatoire, préenregistré :
  1. Entraînement : opérandes 1–5 chiffres (comme E008). **Validation OOD séparée : 6–8 chiffres**, seule autorisée pour choisir checkpoint/hyperparamètres. **Test final intouché : 10, 16, 32, 64, 100 chiffres**, évalué une seule fois à la fin.
  2. **Tests adverses** (en plus) : retenues en cascade (99…9 + 1), nombres pleins de zéros (100…002 + 100…003), **longueurs asymétriques** (100 chiffres + 3 chiffres).
  3. **≥ 5 graines** pour tout système déclaré « réussi » ; exact-match séquence entière, moyenne ± écart **et** nombre de graines réussies (≥ 90 % à 16 chiffres).
  4. **Exemples uniques ≠ pas d'optimisation** : journaliser le nombre d'exemples **uniques** vus.
  5. C-ORACLE = 100 % et C-PARCŒUR = 0 % recalculés sur tous les nouveaux jeux (validité, leçon M0020).
  6. **Budget de structure** : pour chaque système, une ligne qui dit ce qui est donné à la main (format, localité, nombre d'itérations, traces) — rien de caché.
  7. « Faux et sûr » (faux avec confiance ≥ 0,8) et, si le système s'abstient, taux d'abstention quand il a tort (autodiagnostic).
- Machine : Mac M1 16 Go, MLX (venv `$HOME/.venvs/ev-llm-e008`, réutilisable ; ajoute des paquets seulement si justifié). **Plusieurs fenêtres entraînent en parallèle** : budget **≤ 4 h de calcul** pour ton mandat ; si le partage du GPU ralentit trop, réduis (moins de pas / de variantes) et écris-le, ne dépasse pas. Entraînement par invocations ≤ 9 min avec reprise sur checkpoint ; aucune tâche de fond, aucun `sleep`.
- Ordre des commits : préenregistrement (poussé seul) < code < valeurs figées après pilote (pilote = graine 0, exclue) < résultats.

Modèle : `opus --effort medium` (barème `realisation_standard`). Aucun appel d'API.

## 0. But
Tester si des **biais d'architecture** (et seulement eux) suffisent pour apprendre l'addition et la généraliser à toute longueur. Littérature (vérifiée par l'orchestrateur le 27/09) : Neural GPU (arXiv 1511.08228) 20 → 2000 bits mais « quelques runs sur 729 » et échec sur entrées symétriques (1611.00736) ; Deep Thinking + recall + perte progressive (2202.05826) 32 → 512 bits, 2/30 runs sans contrainte de Lipschitz contre 28/30 avec (2410.23451) ; Looped Transformer NoPE (2409.15647) ≈ 100 % mais **nombre d'itérations T(n) fourni à l'entraînement**. Théorie : échec des transformers = profondeur fixe + positions absolues (2310.16028, 2207.00729).

## 1. Gardes
`fetch` ; `origin/exp/e008-addition` = `af281f53efddf97aa542bfa11f1bac34ecff06d4` ; pas de branche `exp/e009-procedure-apprise` ; worktree `.claude/worktrees/F01-M0022` sur nouvelle branche `exp/e009-procedure-apprise` depuis `origin/exp/e008-addition`.

## 1 bis. Mission 0 — racine `main`
Committe UNIQUEMENT `vault/echanges/archive/2026-09-26-F01-M0021-e008-addition-palier0.md` (s'il est nouveau) — message `docs(vault): archive M0021 -- pose vague E009-E011`. Push, `ls-remote`.

## 2. Systèmes (dossier `research/experiments/E009-procedure-apprise/`)
Entrée : **la même séquence de caractères plate qu'E008** (`a+b=`), aucune grille alignée fournie, aucun index de position. Format de sortie : standard ET inversé testés pour le meilleur système (le dire).
- **A1 — Neural GPU** : GRU convolutionnel 1D (noyau local) appliqué en boucle sur la séquence ; nombre d'itérations = longueur d'entrée (dépend de l'entrée, pas de la réponse : c'est un biais « calcul proportionnel à la taille », à inscrire au budget de structure).
- **A2 — Deep Thinking** : bloc récurrent convolutionnel avec **recall** (réinjection de l'entrée) et **perte progressive**, + variante avec contrainte de Lipschitz ; au test, itérations supplémentaires autorisées jusqu'à un plafond fixé.
- **A3 — Looped Transformer NoPE** : un seul bloc bouclé, **arrêt par confiance maximale, SANS T(n) fourni à l'entraînement** (c'est la version « non trichée ») ; + une variante **avec** T(n) fourni, étiquetée « structure injectée », comme référence.
- Références : reprends B-STD et B-REF d'E008 (chiffres existants, pas de réentraînement).

## 3. Déroulé
1. Préenregistrement (hypothèses, seuils, budget de structure de chaque système) → commit poussé seul.
2. **Criblage** : chaque système × 2 graines, budget égal ; sélection sur la **validation 6–8** uniquement.
3. **Confirmation** : les systèmes ≥ 50 % à 8 chiffres en validation passent à 5 graines ; puis test final intouché (10–100) + adverses, une seule fois.
4. Courbe d'efficacité (exemples uniques) pour le meilleur système.

## 4. README + publication
Tableau par longueur (jusqu'à 100) × système, graines réussies, adverses, faux et sûr, budget de structure ; **Lecture** [VÉRIFIÉ]/[HYPOTHÈSE] sans gonfler ; « ce que ça dit de l'hypothèse règle/déclencheur/réflexe ». Push ; `gh issue create ... --title "E009 — A : procédure apprise par l'architecture"` si `gh` OK.

## 5. STOP
Contrôles de validité en échec ; test final touché avant la fin ; envie de modifier le préenregistrement (écris-la) ; dépassement de budget (publie le partiel).

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

## Rapport M0022

**Rendu : READY_FOR_INTEGRATION** (résultat négatif, protocole suivi). Test [VÉRIFIÉ] VALIDE ; 5 systèmes × 2 graines entraînés et évalués ; **0 % partout, y compris dans la distribution (T-ID ≤ 3 %)** ; la question « l'architecture suffit-elle à généraliser en longueur ? » est **non mesurée** à ce budget (A non réfutée). Branche `exp/e009-procedure-apprise`, tip `20f289b` ; issue #24.

### Gardes [VÉRIFIÉ]
`git fetch origin` OK ; `origin/exp/e008-addition` = `af281f53efddf97aa542bfa11f1bac34ecff06d4` ; aucune branche `exp/e009*` locale ni distante ; worktree `.claude/worktrees/F01-M0022` créé sur nouvelle branche `exp/e009-procedure-apprise` depuis `origin/exp/e008-addition`.

### Mission 0 [VÉRIFIÉ]
`70a8d93 docs(vault): archive M0021 -- pose vague E009-E011` (1 fichier, l'archive M0021), `30c8611..70a8d93  main -> main`, `ls-remote` → `70a8d93ceb79891bef72140acace5ac6f83ec3e4 refs/heads/main`.

### Ordre des commits (`git log --format='%h %ci %s' af281f5..HEAD`)
```
20f289b feat(e009): synthese -- diagnostic chiffre par chiffre (longueur, poids faible, chiffres justes)
f8ecf76 2026-09-27 13:00:30 data(e009): resultats A -- 0 % partout (...) ; question non mesuree a ce budget
870f23d 2026-09-27 12:21:35 data(e009): criblage (VAL 6-8 + T-ID) -- 0 % en VAL (...) ; test final encore ferme
8f6977e 2026-09-27 10:10:37 data(e009): controles de validite -- TEST VALIDE
77b5a9d 2026-09-27 10:10:24 docs(e009): amendement A1 -- S = 2 000 pas, largeur 64, compile, ELU sure (avant runs officiels)
ffb612d 2026-09-27 09:48:53 feat(e009): code A1/A2/A2-L/A3/A3-T (...)
a8f918d 2026-09-27 09:39:00 docs(e009): preenregistrement A (avant tout code) -- poussé seul
```
Préenregistrement < code < valeurs figées après pilote (graine 0) < contrôles < criblage < test final (ouvert après `870f23d`, `resultats/FINAL_OUVERT`, évalué une fois par run ; `evalue.py` refuse une 2ᵉ évaluation).

### Réutilisation E008 [VÉRIFIÉ]
Import par chemin (`bande.py` insère `E008-addition/` dans `sys.path`) : `data` (flux, tirage, exclusions, T-ID, générateur retenues), `evaluate.evaluer/resume` (évaluateur unique), `controles.systeme_oracle`, `model.Bloc` et `lr_schedule`. `git diff af281f5 HEAD -- research/experiments/E008-addition/` : vide.

### Tests [VÉRIFIÉ]
`python -m unittest test_e009` : `Ran 17 tests — OK` (relancé sur l'état final). Mutations tuées par assertion nommée : décodage sans inversion (`test_decodage`, `test_parfait`, `test_mauvais_format`), sélection T(n) ignorée au test (`test_t_n_selectionne_le_bon_tour`), idem dans la perte, A1 à T = n au lieu de 2n, arrêt par confiance inversé (`test_arret_confiance_max_et_plafond`). Base reverte verte après chaque mutation. Test de reprise : tolérance 1e-3 (GPU non déterministe, 1,07e-4 observé une fois) + contrôle négatif autre graine > 1e-2.

### Validité [VÉRIFIÉ] (`resultats/controles.json`)
C-ORACLE 100 % sur 43 jeux × longueurs (VAL, TEST, ADV-RET/ZERO/ASYM, T-ID, T-ID1). C-PARCŒUR (405 818 paires distinctes, graine 1, 2 000 pas) = 0,000 partout ; T-ID1 = 1,000 (contrôle positif). Contrôle de sanité hors protocole : A3-T sur-apprend un lot de 64 à 100 % en 300 pas (le pipeline peut apprendre) ; A2 n'y arrive pas (perte 1,2).

### Tableau (exact-match %, graines 1–2)
| système | T-ID 2/3/4/5 | VAL 6/7/8 | TEST 10–100 | ADV-* | graines ≥ 90 % à 16 | perte finale |
|---|---|---|---|---|---|---|
| A1 | 0/0/0/0 | 0/0/0 | 0 | 0 | 0/2 | 1,28 / 1,27 |
| A2 | 1,0/0,3/0/0 | 0/0/0 | 0 | 0 | 0/2 | 1,00 / 0,94 |
| A2-L | 1,5/0/0/0 | 0/0/0 | 0 | 0 | 0/2 | 1,06 / 0,95 |
| A3 (sans T(n)) | 0/0/0/0 | 0/0/0 | 0 | 0 | 0/2 | 1,16 / 1,09 |
| A3-T (T(n) donné) | 1,3/0,3/0,3/0 | 0/0/0 | 0 | 0 | 0/2 | 0,82 / 0,80 |
| B-REF (E008) | 100 | 91,2/7,9/0,1 | 0 (10–16) | — | — | — |
Faux et sûr : 0 pour A2, A2-L, A3, A3-T ; A1 1 745 / 6 030 (29 %) au test final. Poids faible juste 1–14 % (hasard ≈ 10 %). A3-T : bonne longueur de réponse 87–95 % (T-ID) mais chiffres au hasard. Arrêt appris : A2-L s'arrête à 1–2 itérations quelle que soit la longueur.
Prédictions : P1 infirmée (5/5), P2 infirmée, P3 infirmée (égalité à 0), P4 et P5 confirmées trivialement. Question ouverte : non.

### Écarts au mandat (assumés, écrits)
1. **Budget** : amendement A1 figé après pilote, avant tout run officiel : S = 2 000 pas (au lieu de 6 000 provisoires), largeur 64 (au lieu de 128), SN 20 itérations de puissance (au lieu de 3), ELU sûre (bug `nn.elu` → gradient NaN, reproduit au pas 65), `mx.compile` avec repli non compilé si n + k = M (bug MLX 0.29.3 `unordered_map::at`, reproduit).
2. **Confirmation à 5 graines non déclenchée** (aucun système ≥ 50 % à VAL 8).
3. **Format standard non entraîné** : la règle préenregistrée (VAL 8 puis 7 puis 6) ne départage pas des 0. Question que j'aurais posée : « quel système en standard quand tout est à 0 ? » ; options : (a) aucun, (b) A3-T (seul à apprendre la longueur), (c) tous ; choix (a), seul conforme à la règle écrite.
4. Courbe d'efficacité du « meilleur » sans objet ; courbes de tous les runs dans `resultats/courbe.csv` avec exemples uniques (405 818 / 512 000 à 2 000 pas, graine 1).
5. Deux appels ont dépassé le délai de l'outil et sont passés en arrière-plan (fin de A3 s1 + début s2 ; éval finale A2-L) ; chacun s'est terminé seul (budget interne), aucun autre calcul lancé en parallèle ; aucune tâche vivante à la sortie.

### Calcul
Entraînements officiels 7 391 s ; évaluations finales 2 214 s ; VAL ≈ 3 min ; pilotes + bancs + tests ≈ 25 min → **≈ 3 h 05** (budget 4 h), GPU partagé avec d'autres fenêtres.

### Envie de modifier le préenregistrement (écrite, NON appliquée)
Après A3-T s1 (T-ID 0 %) : ajouter un critère préalable « T-ID ≥ 95 % » avec budget de pas adaptatif, un pilote qui vérifie l'apprentissage dans la distribution (pas seulement la vitesse), et un réglage lr/largeur par famille sur VAL/T-ID. Non appliqué (§ 9 : modifier après un run officiel = STOP).

### Lecture courte
- [VÉRIFIÉ] Test juste, pipeline capable d'apprendre ; à ce budget, aucun biais d'architecture n'apprend l'addition *dans* la distribution.
- [HYPOTHÈSE] Causes non départagées : budget (512 k ex., ≪ littérature), largeur 64, lecture non autorégressive (une case doit « savoir » son rang sans position), entraînabilité des récurrences profondes (A2).
- Aucune conclusion sur la capacité des architectures à généraliser : non mesurée.

### Non testé (angles morts)
Budget plus grand ; hyperparamètres par famille ; format standard ; sortie autorégressive sur bande ; opérandes inversés (interdit par le mandat).

### Leçon candidate (transverse, R5)
Un pilote qui ne mesure que la vitesse ne protège pas d'un budget où rien n'apprend : le pilote doit aussi vérifier qu'au moins la tâche *dans* la distribution est apprise avant de figer le budget — sinon toute la suite mesure le budget, pas l'hypothèse.

### Push final [VÉRIFIÉ]
- Reprise : `999f632 docs(vault): reprise F01 -- M0022 rendu (...)`, `008909e..999f632  main -> main`.
- `git ls-remote origin refs/heads/main` → `999f632a0a9fc5f08ef4fd6722f071aac9711c85	refs/heads/main`
- `git ls-remote origin refs/heads/exp/e009-procedure-apprise` → `20f289b9f3c951b75724afc240c9489a6d87133e	refs/heads/exp/e009-procedure-apprise`
- Issue : https://github.com/malikkaraoui/EV-LLM/issues/24
- Runtime : `events.jsonl` (RAPPORT_RENDU, ts 2026-09-27T13:01:47+02:00) ; `state.json` : seule `windows.F01` modifiée, autres clés vérifiées identiques, `next_mandat_id` = M0025 présent. Aucune tâche de fond vivante (0 processus entraine/evalue).

```
M0022
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
