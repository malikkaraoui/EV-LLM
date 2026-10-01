---
date: 2026-09-29
tags: [readme, reconception, synthese, r014]
session: F01
mandat: readme-reconception-synthese
mandat_id: M0039
statut: reponse-disponible
modele: opus
effort: high
worktree: /Users/malik/Documents/EV-LLM/.claude/worktrees/F01-M0035
branche: docs/readme-2026-09-28
derniere_maj: 2026-09-29T10:20:14+0200
---

# M0039 — README racine : RECONCEPTION de la section « What we think we know today » (et de toute puce [VERIFIED]) depuis les sources — pas un patch

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

Modèle : `opus --effort high` (justification : travail de synthèse où deux relectures successives ont trouvé la même classe de défaut ; la rigueur de lecture prime). **Aucun calcul.**

## 0. Pourquoi une reconception et pas un correctif
- R013 (`ddf13d1`) puis R014 (`ed790c9`, `vault/revues/2026-09-28-R014-readme-licence-final.md` — lis-le EN ENTIER, ainsi que R013) ont trouvé deux fois la même classe de défaut : **une puce de synthèse étiquetée [VERIFIED — sources] affirme quelque chose que ses sources ne portent pas** (l.190 : « sans perte, souvent jusqu'à 1 000 » ; l.191 : « évolution sans alignement » alors qu'E012 X1 est *aligné* ; l.189 : « unique exception » alors qu'E008 B-REF fait 91 % à 6 chiffres). Loi des deux patchs (convention §9) : le MÉCANISME est en cause. Le mécanisme fautif : ces puces ont été écrites **de haut en bas** (l'idée d'abord, les sources ensuite) — y compris par l'orchestrateur dans ses mandats correctifs. On inverse : **de bas en haut**.
- Ce mandat ne te dicte AUCUNE formulation. Il te dicte une **procédure**.

## 1. Gardes
`fetch` ; `git rev-parse origin/docs/readme-2026-09-28` = `f99553a89ff4af7fd4c873c232c06d4aaeef9887` ; worktree `.claude/worktrees/F01-M0035` propre sur la branche (sinon worktree neuf `F01-M0039`). STOP si écart.

## 2. Procédure (obligatoire, dans cet ordre)
1. **Inventaire** : liste toutes les puces du README qui portent une étiquette `[VERIFIED — …]` ou `[HYPOTHESIS]` hors du journal des expériences (sections « What we think we know today », « What did not work », « Open leads »). Au tip `f99553a` : l.188–192 et l.224 au moins ; vérifie qu'il n'y en a pas d'autres (`grep -n 'VERIFIED\|HYPOTHESIS' README.md`).
2. **Tableau de traçabilité, AVANT toute réécriture**, dans ton rapport : pour chaque puce, découpe-la en **affirmations atomiques** (une proposition = une ligne), et pour chacune : la source citée dans l'étiquette, le fichier et la ligne au tip de la branche (`git show <tip>:<chemin>` — tips listés dans `vault/echanges/archive/2026-09-28-F01-M0035-readme-racine.md`), la citation exacte, et le verdict **portée / non portée / portée avec une nuance à écrire**. Une affirmation dont aucune source de l'étiquette ne porte le contenu = non portée, même si elle te paraît vraie.
3. **Réécriture de bas en haut** : pour chaque puce, ne garde que les affirmations portées ; ajoute les nuances que les sources imposent (graines, longueurs, « ≥ 90 % » vs « exact », « aligné » vs « plat », etc.) ; retire toute clause d'exclusivité (« seul », « unique », « souvent », « sans perte ») qu'aucune source ne porte mot pour mot ou chiffre pour chiffre ; si une puce ne tient plus, supprime-la ou passe-la en [HYPOTHESIS] avec la raison. L'étiquette ne cite que les expériences réellement utilisées par la puce réécrite.
4. **Relecture croisée interne** : relis chaque puce réécrite contre son tableau (étape 2) une seconde fois, comme si tu étais le relecteur R015. Cherche spécifiquement : mots absolus, généralisations, chiffres arrondis, conditions omises (aligné / donné / gelé / curriculum).
5. Le journal des expériences (21 entrées) n'est **pas** réécrit ; tu ne touches à ces entrées que si l'étape 2 révèle qu'une puce de synthèse s'appuie sur une entrée elle-même fausse — alors tu corriges l'entrée avec la même procédure et tu le signales.
6. Ne change ni le H1, ni la méthode, ni la section License, ni les liens. Aucune mention de l'enfant de Malik. Anglais.

## 3. Preuves exigées
Le tableau de traçabilité complet (étape 2), la version réécrite de chaque puce avec son tableau final (étape 4), `git diff --stat f99553a..HEAD` (README seul), `git diff f99553a..HEAD` collé en entier, `grep -c 'VERIFIED' README.md` avant/après, `git log -1 --format=%B` (trailer), push + `git ls-remote origin refs/heads/docs/readme-2026-09-28` (nouveau tip = garde de R015). Commit : `docs(readme): rebuild synthesis bullets bottom-up from sources (after R013/R014)`.

## 4. STOP
Garde en écart · une source illisible au tip → l'affirmation est retirée, pas devinée · si l'inventaire révèle plus de 12 puces à traiter → fais-les toutes quand même mais signale la charge.

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

## Rapport M0039

**Rendu : puces de synthèse du README reconstruites de bas en haut, commit et push sur `docs/readme-2026-09-28`.** Aucun calcul, aucun appel d'API : `git`, `sed`, `grep`, lecture seule des sources.

### Gardes
- `git fetch origin` OK ; `git rev-parse origin/docs/readme-2026-09-28` = `f99553a89ff4af7fd4c873c232c06d4aaeef9887` ✅.
- Worktree `.claude/worktrees/F01-M0035` propre, sur la branche, HEAD = `f99553a` ✅ (pas de worktree neuf).
- Tips des sources = tips listés dans l'archive M0035, tous revérifiés sur `origin/exp/*` : e005 `15487b0`, e006 `ad54bd4`, e008 `af281f5`, e009bis `e489db9`, e010 `19f7f0d`, e011 `994c77b`, e012 `0a33881`, e013 `044545e`, e014 `fc698b4`, e015 `58abf67`, e016 `867ccaf`, e016-a2 `1c98601` ; note `origin/main:vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md`.
- R013 et R014 lus en entier.

### Étape 1 — Inventaire (`grep -n 'VERIFIED\|HYPOTHESIS' README.md` au tip f99553a)
Hors journal : **8 puces** (sous le seuil de 12).
- « What we believe we know today » : l.188, l.189, l.190, l.191, l.192 ([VERIFIED]) ; l.193 ([HYPOTHESIS]).
- « What did not work » : l.211 (item 11, [HYPOTHESIS] en ligne).
- « Open leads » : l.224 ([VERIFIED — sources listed in the note]).
- Hors périmètre : l.31 (définition des étiquettes) ; l.56, l.63, l.74, l.182 (entrées du journal, étape 5).

### Étape 2 — Traçabilité AVANT réécriture (source = README d'expérience au tip, `git show <tip>:research/experiments/<dossier>/README.md`, numéro de ligne)

Légende : **P** = portée ; **N** = non portée ; **P+n** = portée avec une nuance à écrire.

#### l.188 — [VERIFIED — E011, E012, E013] « Computing is easy with almost nothing »
| # | affirmation atomique | source:ligne | citation (extrait) | verdict |
|---|---|---|---|---|
| 1a | Calculer est « facile avec presque rien » | E013 l.192–197 ; E012 l.111–115 | « oui, **si le rien est bien placé** » ; « Le résultat mesure donc surtout la **valeur de la structure donnée** » ; E012 : [HYPOTHÈSE] « ce n'est pas une découverte "de zéro" » | **P+n** : « facile » n'est dans aucune source ; les sources disent « la partie apprise est petite » **si** la structure est donnée |
| 1b | Une fois les chiffres alignés | E012 l.121 ; E013 l.19 ; E011 l.38 | format aligné poids faible d'abord ; « alignement des chiffres de même rang » | P |
| 1c | La retenue est découverte par évolution | E012 l.17–20, l.40–43 | X2 : 2/5 (100 ex.), 4/5 (1 000 ex.) ; X1 binaire **0/5** ; X3 plat **0/5** | **P+n** : seulement en décimal aligné, pas sur toutes les graines ; primitives de seuil données (l.121) |
| 1d | E012 : une unité cachée | E012 l.24–25, l.41–42 | « Le plus court circuit trouvé … avec une seule unité cachée qui est la retenue » ; tailles 1/7/0, 1/7/1 mais aussi 2/8/0, 2/9/2, 4/12/3, 5/13/0 | **P+n** : c'est le **plus court** circuit trouvé, pas tous |
| 1e | ou apprise (E013 : 1 131 paramètres) | E013 l.19, l.64, l.163 | I1 H = 1 : 1 131 ; 5/5 ; ≈ 591 000 exemples uniques vus | P |
| 1f | avec 100 à 10 000 exemples | E012 l.17, l.19 ; E013 l.21, l.64, l.70–72, l.100 | le modèle de 1 131 paramètres voit **≈ 591 000** ex. ; les jeux fixes N sont I3 (**1 326** paramètres) : N = 100 **0/5**, N = 1 000 5/5 en T-LONG mais 1/5 en propagation pure à 1 000, N = 10 000 100 % | **N** tel quel : la fourchette mêle E012 (100 ex., 2/5) et E013 I3 (10 000), et l'accole au modèle de 1 131 paramètres qui a vu ≈ 591 000 ex. ; E013 N = 100 échoue |
| 1g | reste stable sous entropie croisée (E011) | E011 l.10–14, l.40 | réseau **construit à la main** exact (22 paramètres), binaire, CE seule 5/5 jusqu'à 1 000 bits ; pénalités fortes : L2 λ = 0,1 2/5, λ = 1 0/5, L1 λ = 1 2/5 | **P+n** : règle donnée, pas découverte ; binaire ; les pénalités la cassent |
| 1h | tient jusqu'à 1 000 chiffres | E012 l.19–20 ; E013 l.64–67 ; E011 l.12 | X2-1000 4/5 exactes jusqu'à 1 000 ; H = 1 **99,3 %** à 1 000, H ≥ 2 100 % | **P+n** : H = 1 n'est pas exact à 1 000 (99,3 %) |

#### l.189 — [VERIFIED — E008, E009-bis, E010, E013 I2, E014 R0] « The wall is locating, aligning, wiring »
| # | affirmation atomique | source:ligne | citation (extrait) | verdict |
|---|---|---|---|---|
| 2a | Le mur = repérer | E010 l.139–143 ; E014 l.150–151 | « L'échec hors longueur est un échec de **localité** » ; « Le repérage appris de bout en bout ne généralise pas » | P |
| 2b | Le mur = aligner | E013 l.179–181 ; E012 l.110 | « Le prix de l'alignement donné … 0/5 » ; « **l'alignement est la structure décisive** » | P (E012 hors étiquette, E013 suffit) |
| 2c | Le mur = brancher (câbler) | E015 l.201–202 | « **Le câblage est le mur.** Il suffit qu'il manque une instruction (ECH1) pour passer à 0/5 » | **N par l'étiquette** : E015 n'est pas cité dans l.189 ; aucune source citée ne parle de câblage |
| 2d | Chaque fois que le système doit trouver seul quel chiffre lire, il échoue au-delà des longueurs vues | E008 l.78 ; E009bis l.44 ; E010 l.71 ; E013 l.68 ; E014 l.61–62, l.70 | B-REF **91,2 %** à 6 chiffres ; A3 s1 17,3 % à 6 ; F1-NoPE 33,1 % à 6 ; I2 27,8 % à 16 (meilleure graine 83 %) ; R0b s2 100/99,8 à 16/100 | **N** : « chaque fois » est contredit par E008 B-REF et E014 R0b s2 ; les sources montrent une **chute avec la longueur**, pas un échec dès la première longueur non vue |
| 2e | quelle que soit sa taille (~1 900 à ~3,2 M) | E013 l.20 (1 922) ; E008 l.28 (3 179 022 / 3 162 638) ; E010 l.11 (≈ 3,2 M) | tailles testées | **P+n** : « quelle que soit » généralise ; écrire « à des tailles de 1 922 à ~3,2 M » |
| 2f | l'unique exception : 1 graine sur 5 avec curriculum (E014 R0b, 1/5 à 16 et 100) | E014 l.62, l.70 ; E008 l.78 | R0b 1/5 / 1/5 / 0/5 ; s2 100 / 99,8 / 62,5 | **N** : « single exception » contredit par E008 B-REF (R014). Chiffre R0b exact. Au critère « ≥ 90 % à 16 chiffres », l'énumération source par source (E008 l.81 : 0,0 ; E009bis l.50 : 0 ; E010 l.77 : 0/2 ; E013 l.68 : 0/5 ; E014 l.61–65 : R0a 0/5, R0b 1/5, R2 0/5) est portée chiffre pour chiffre — on l'écrit comme énumération, sans mot d'exclusivité |

#### l.190 — [VERIFIED — E014, E015 ECH0, E016 DONNÉ] « What got over the wall: a discrete symbolic interface between frozen skills »
| # | affirmation atomique | source:ligne | citation (extrait) | verdict |
|---|---|---|---|---|
| 3a | Ce qui a franchi le mur = une interface **discrète** symbolique | E014 l.132–134 ; E014 l.162–165 ; E015 l.59, l.73 ; E016 l.46–47, l.55 | E014 R1G transmet **les probabilités** du lecteur (« l'argmax du lecteur (one-hot) au lieu de ses probabilités » = diagnostic post hoc) ; « Une interface **discrète** … rendrait la composition sans perte » = **[HYPOTHÈSE]** ; E015 table 14 → 11 symboles, sortie discrète ; E016 symboles de canal | **N pour E014 R1G** (interface douce) ; P pour E015 et E016 |
| 3b | Deux compétences gelées reliées par des symboles composent sans réentraînement | E014 l.155–157 ; E015 l.127–135 ; E016 l.42–44, l.55 | E014 : « zéro pas d'entraînement joint » (2 modules gelés) ; E015 ECH0 : **un** champion gelé (M-SOMME) + opérations génériques données (DECOUPE, INV) ; E016 : 3 lecteurs + 3 accumulateurs gelés | **P+n** : E015 ECH0 = un seul module gelé, pas deux ; E014 non symbolique (3a) |
| 3c | ≥ 90 % à 16 et 100 chiffres sur 4/5 graines, interface donnée (E014 R1G) | E014 l.63 ; l.48 ; E015 l.217 | 4/5 / 4/5 / 1/5 ; tâche « poser en colonnes » donnée ; « R1G, dont l'interface était **écrite par nous** » | P |
| 3d | 100 % sur 2/5 graines, câblage donné, interface à inventer (E015 ECH0) | E015 l.93, l.107–108 | s1, s3 : 100/100/100 (T-LONG 16/100/1 000) ; s3 ADV-PROPAG 1 000 : **27,5** | **P+n** : 100 % en T-LONG ; s3 tombe à 27,5 % en propagation pure |
| 3e | 9/9 paires × 5/5 graines, interface donnée (E016 DONNÉ, 100 % à 100) | E016 l.76, l.55 | DONNÉ 5/5, 9 ×5, 100,0 à 16, 100,0 à 100 ; « interface exacte σ_j ∘ π_i⁻¹ » | P |
| 3f | À 1 000 chiffres ça ne tient que parfois : 1/5 (E014), 2/5 (ECH0), 71,7 % (DONNÉ) | E014 l.63 ; E015 l.93, l.107 ; E016 l.76 | chiffres exacts | **P+n** : chiffres exacts ; mais pour ECH0, 2/5 à 1 000 = 2/5 à 16 (aucune chute en T-LONG) : « only sometimes » suggère une chute que ECH0 n'a pas |
| 3g | Les limites restantes viennent de la lecture, pas du calcul | E014 l.161 ; E016 l.92–94 ; **E015 l.199–200** | E014, E016 : limite = lecteur ; E015 : « À 1 000 chiffres, la limite de s3 est la qualité du **champion** en propagation pure, pas l'interface » | **N** en général : E015 ECH0 s3 (dans l'étiquette) contredit ; P pour E014 et E016 |

#### l.191 — [VERIFIED — E012 X1, E015, E016, E016-A2] « What did not get over it »
| # | affirmation atomique | source:ligne | citation (extrait) | verdict |
|---|---|---|---|---|
| 4a | l'évolution aveugle **sans alignement** (← E012 X1) | E012 l.40, l.43 ; l.11 | X1 = « binaire **aligné** (Lan) » 0/5 ; X3 = « décimal **plat** (E008) » 0/5 ; budget ≲ 0,6 % de Lan | **N** (R014) : X1 est aligné ; la condition sans alignement est X3. Nuance : « aveugle » = recherche MDL réduite |
| 4b | l'assemblage libre | E015 l.9–10, l.90, l.96–99 | 0/5 sur les trois tâches nouvelles, de zéro ou depuis une interface trouvée | P |
| 4c | la pression sociale tout-ou-rien | E016 l.77, l.168–173, l.194–195 | COLL 0/5 ; « une seule formulation de la règle a été testée » ; IND (récompense par paire) aussi 0/5 (l.78) | **P+n** : une seule formulation ; le témoin individuel échoue aussi |
| 4d | un signal scalaire dense | E016A2 l.227, l.230–235, l.270 | fraction de colonnes justes ; 1/9 ; « une graine pilote par variante » | **P+n** : pilote-garde, graine 0 seule |

#### l.192 — [VERIFIED — E005, E006, E008, E010, E013, E015] « Misplaced confidence is blind »
| # | affirmation atomique | source:ligne | citation (extrait) | verdict |
|---|---|---|---|---|
| 5a | Les erreurs sont **souvent** « sûres » | E005 l.104 ; E006 l.92 ; E008 l.127 ; E011 l.81 ; E012 l.71 | 9/42 évaluations ; 5 cas répliqués 5/5 ; 65–68 % ; mais E011 « 0 partout », E012 X1/X3 « 0 faux sûr » | **P+n** : « souvent » n'est porté par aucune source comme proportion générale ; écrire les chiffres |
| 5b | … **quand** la confiance porte sur la mauvaise étape | E005, E006, E008 | aucune de ces trois sources ne relie ses faux-sûrs à une étape (E008 l.128–129 : « ne signale pas qu'il est sorti de son domaine ») | **N pour E005, E006, E008** (ils portent « des faux sûrs existent », pas le mécanisme « mauvaise étape ») |
| 5c | la recopie (E010) | E010 l.103–105 | « 606 / 669 faux sont sûrs … elle mesure la sûreté de la recopie, pas celle du calcul » | P |
| 5d | le calcul sans la lecture (← E013) | E013 l.19, l.115, l.184–187 ; **E014 l.142–146, l.175–176 ; E016 l.138–140** | E013 : lecture **donnée** (alignement), faux-sûrs = dérive de l'état sur nombres creux (calcul) ; E014 : « I1 est sûr de sa somme, c'est la lecture qui est fausse » ; E016 : confiance « n'inclut pas le lecteur : les 5 535 faux de DONNÉ … tous "sûrs" » | **N par E013** (pas de lecture à omettre dans E013 I1) ; porté par E014 et E016, dont seul E014 est cité (pour une autre clause) |
| 5e | les champions sans l'interface (E015) | E015 l.156, l.224–227, l.212–215 | ECH0 7 673 / 13 783 faux sûrs ; s5 4 606 / 4 606 ; « Il faut une confiance sur l'interface » = **[HYPOTHÈSE]** | **P+n** : fait portée ; le remède est une hypothèse de la source |
| 5f | Une confiance prise à chaque étape, lecture comprise, sépare beaucoup mieux (E014) | E014 l.31, l.104, l.144–146, l.173–176 | 77,3 % / 1,4 % = p_min **sur les colonnes de la somme** (sans la lecture) ; lecture comprise = ré-agrégation **post hoc** sur TEST déjà lu : faux sûrs R1G 1 218 → 227 | **P+n** : « lecture comprise » n'est mesuré que post hoc (1 218 → 227) ; « beaucoup mieux » → chiffres |

#### l.193 — [HYPOTHESIS] « missing lever = intermediate signal the machine gives itself »
| # | affirmation atomique | source:ligne | citation | verdict |
|---|---|---|---|---|
| 6a | Le levier manquant serait un signal intermédiaire que la machine se donne | E015 l.208–211 | « [HYPOTHÈSE] … Il manque un **signal intermédiaire que la machine se donne elle-même**, par exemple la cohérence entre champions ou la prédiction de ses propres flux, au lieu du seul verdict final » | P (hypothèse de la source, étiquette correcte ; source à nommer) |
| 6b | Rien de cela n'a été testé | E015 l.211 ; note l.44 | « non testée ici » ; « Non lancé (28/09) » | P |

#### l.211 — item 11 « Learned hard pointers (E014 R2) »
| # | affirmation atomique | source:ligne | citation | verdict |
|---|---|---|---|---|
| 7a | 0 même en distribution | E014 l.65, l.73 | « 0 partout, y compris T-ID (… sur les 5 graines officielles) » | P (+n : graines officielles ; le pilote atteint VAL-OOD 1,000, l.170–171) |
| 7b | [HYPOTHESIS] une instabilité d'optimisation | E014 l.170–172 | « ressemble à une instabilité d'optimisation du straight-through » | P |
| 7c | pas une preuve contre **les pointeurs** | E014 l.171–172, l.183–184 | « pas à une preuve contre les pointeurs **relatifs** ; non testé plus avant » | **P+n** : « relatifs » omis |

#### l.224 — [VERIFIED — sources listed in the note] piste « E015-A2: the interface as a first-class object »
| # | affirmation atomique | source:ligne | citation | verdict |
|---|---|---|---|---|
| 8a | Antériorité faite par l'orchestrateur, verdict « partially done » : PathNet, BounceGrad, Braylan 2016, Guijt 2024, Cully 2015, Schug 2024, MAGELLAN, DreamCoder / Voyager / FunSearch ; non trouvé : mesure de la réutilisation de l'interface | la note citée : **absente** (seul MAGELLAN y figure, l.21) ; présente seulement dans `vault/echanges/F05.md` l.49–60 (mandat M0033), **non versionné** (`git ls-files` ne le liste pas) | — | **N** : aucune source du dépôt ne la porte ; la définition l.31 du README exige « a source in the repository » → retirée (règle §4 : source illisible au tip → retirée) |
| 8b | La piste voisine « co-évoluer les problèmes avec les solveurs » a fait l'objet d'une recherche le 27/09 | note l.2–4, l.8, l.41–42 | objet de la note : « un signal intermédiaire AUTO-GÉNÉRÉ … pour guider une recherche de programmes compositionnels sur modules gelés » ; la co-évolution des instances (MCC) est son **contre-pied** (l.41–42) | **N** tel quel : la note ne porte pas sur la co-évolution des problèmes, qui n'y est que le contre-pied |
| 8c | (novelty search, MCC de Brant & Stanley, PowerPlay, DreamCoder, HOUDINI, CRL) | note l.16, l.18, l.19, l.23, l.24, l.25 | présents | P |
| 8d | Verdict « every building block exists, the assembly does not » | note l.5, l.33 | « **Partiellement fait.** Chaque brique existe séparément … Personne n'a assemblé "modules neuronaux gelés + câblage discret évolutif + signal intermédiaire fabriqué par le système + généralisation en longueur…" » | **P+n** : paraphrase entre guillemets ; écrire la traduction fidèle |
| 8e | Le nom « E015-A2 » désigne l'archive d'interfaces | note l.4, l.8 vs F05.md (non versionné) | la note versionnée appelle E015-A2 le **signal auto-généré** | **N** (conflit de nommage) → code retiré du titre de la piste |

**Bilan étape 2** : 8 puces, 41 affirmations atomiques. N (non portées) : 1f, 2c, 2d, 2f, 3a (E014), 3g, 4a, 5b, 5d, 8a, 8b, 8e = **12**. P+n : 17 (dont 7a). P : 12. Aucune source illisible au tip (les 12 README et la note se lisent) ; la seule source absente du dépôt est F05.md (8a).

### Étapes 3 et 4 — Puces réécrites et tableau final (relu une seconde fois contre l'étape 2, comme R015)

Texte intégral des puces : voir le diff collé plus bas (lignes `+`). Pour chaque puce : ce qui reste, sa source, et ce que la seconde lecture a encore corrigé.

| puce | affirmations conservées → source:ligne (tip) | retiré / reformulé (réf. étape 2) | trouvé en 2ᵉ lecture (étape 4) |
|---|---|---|---|
| l.188 « With the alignment given, the learned part is small » | conditions données (même rang, poids faible d'abord, nb de pas) → E012 l.121, E013 l.19, E011 l.38 ; E012 2/5 (100 ex.), 4/5 (1 000), exact jusqu'à 1 000 → l.17–20 ; plus courts circuits = 1 unité cachée, la retenue → l.24–25, l.41–42, l.78 ; primitives de seuil données → l.121 ; binaire 0/5 → l.14 ; E013 I1 1 131 param., 100 % de 16 à 100 (5/5), 99,3 % en moyenne à 1 000, ≈ 591 000 ex. → l.64, l.163–165 ; I3 1 326 param. : N = 100 0/5, N = 1 000 T-LONG oui / propagation pure 1/5 à 1 000 (post hoc), N = 10 000 100 % → l.21, l.70–72, l.88, l.100 ; E011 règle construite à la main, CE seule 5/5 à 1 000 bits, pénalités fortes la cassent → l.10–14, l.40 ; « valeur de la structure donnée » → E013 l.196 | « easy » (1a) ; « 100 to 10,000 examples » accolé à 1 131 param. (1f, **N**) | « 99,3 % » était lu comme par graine → « on average » ; ADV-PROPAG signalé « post hoc » (E013 l.88, l.215) |
| l.189 « In these runs, the wall was locating, aligning, wiring » | E008 B-STD 0,0 dès 6 ; B-REF 91,2 / 7,9 / 0,1 → l.78–80 ; E009-bis 1 run / 5, 17,3 à 6, 0 dès 7 → l.8, l.44 ; E010 F1-NoPE 33,1 à 6, 0 dès 7 → l.71 ; E013 I2 0 % dès 64 pour les 5 → l.68, l.180–181 ; tailles 1 922 → E013 l.20 ; ~3,2 M → E008 l.28, E010 l.11 ; graines ≥ 90 % à 16 : E008 l.81 (0,0), E009bis l.50 (0), E010 l.77 (0/2), E013 l.68 (0/5), E014 l.61, l.65 (R0a, R2 0/5), l.62, l.70 (R0b 1/5, s2 100 / 99,8 / 62,5) ; câblage : E015 l.33–35, l.201–202 | « whenever » (2d, **N**), « whatever its size » (2e), « the single exception » (2f, **N**) ; E015 ajouté à l'étiquette pour « wiring » (2c) | titre au présent général → « In these runs, … was » ; phrase E015 en loi générale → « In E015, … failed whenever » ; R2 ajouté à l'étiquette |
| l.190 « Where length generalisation was obtained: frozen modules plugged together through a given structure, with no retraining » | E014 R1G ≥ 90 % à 16 et 100 sur 4/5, sans joint → l.63, l.155–157 ; tâche et interface définies par nous → E014 l.48, E015 l.217 ; lecteur transmet des probabilités → E014 l.132–134 ; E015 ECH0 câblage donné, un champion, interface inventée, 100 % de 16 à 1 000 sur 2/5 → l.12, l.93, l.107–108, l.127–135 ; E016 DONNÉ traduction exacte, 9/9 × 5/5, 100 % à 16 et 100 → l.55, l.76 ; à 1 000 : 1/5, 2/5, 71,7 % → E014 l.63, E015 l.107, E016 l.76 ; perte due au lecteur → E014 l.161, E016 l.92–94 ; 23,0 contre 28,5 (s1) → E014 l.80 ; ECH0 s3 27,5 % en propagation pure, limite du champion → E015 l.108, l.199–200 | « discrete symbolic interface » pour E014 (3a, **N**) ; « two frozen skills » pour ECH0 (3b) ; « only sometimes » (3f) ; « limits come from reading, not computing » (3g, **N**) | « What passed the length test » : ECH0 échoue à son critère système (P8 ❌, E015 l.187) → « Where length generalisation was obtained » ; 71,7 % = moyenne ; perte d'interface douce d'E014 (P4 ❌, l.123) ajoutée |
| l.191 « What did not work here » | E012 recherche MDL ≲ 0,6 % du budget de Lan → l.11 ; X1 binaire aligné 0/5, piège « hésitant » → l.14–16, l.40 ; X3 plat sans alignement 0/5 → l.21, l.43 ; E015 0/5 sur trois tâches, de zéro ou depuis une interface → l.9–10 ; E016 COLL et IND 0/5, pas de langue commune, une seule formulation → l.77–78, l.117, l.194–195 ; paires apprises ≥ 90 % à 100 → l.92 ; E016-A2 fraction de colonnes, curriculum 1 chiffre, graine pilote, 1/9 → A2 l.227, l.230–235, l.270 | X1 « sans alignement » (4a, **N**) ; nuances 4c, 4d | les paires apprises d'E016 généralisent : ajouté pour ne pas laisser croire à un échec total |
| l.192 « Here, a confidence taken on one step missed the errors made at another » | E005 9/42 → l.104 ; E006 5 répliqués + 1 contesté → l.92 ; E008 B-STD 65–68 % → l.127 ; E013 H = 1 28 % → l.115, l.186 ; E010 606/669, confiance sur la recopie → l.103–105 ; E014 faux sûrs s1–s4 presque tous à 1 000, lecture fausse (post hoc) → l.142–143 ; E016 DONNÉ 5 535 tous sûrs, confiance sans le lecteur → l.133, l.138–140 ; E015 ECH0 7 673 / 13 783, s5 4 606 / 4 606 → l.156, l.224 ; E014 77,3 % / 1,4 % (τ sur VAL) → l.104, l.173–175 ; min(somme, lecture) 1 218 → 227 (post hoc) → l.144–145 | « often » (5a) ; E005/E006/E008 déplacés de « mauvaise étape » vers « faux sûrs mesurés » (5b, **N**) ; E013 retiré de « calcul sans lecture », E014 et E016 mis à sa place (5d, **N**) ; « separates much better » → chiffres (5f) | titre au présent général → « Here, … missed » ; cas F4-04 contesté signalé ; « sit at » → « almost all at » (217/220, 169/205, 29/29, 32/32) ; « standard » transformer d'E008 précisé ; τ fixé en validation |
| l.193 [HYPOTHESIS — E015] | E015 l.208–211 (hypothèse de la source, mots repris) ; « non testée » → E015 l.211 | source nommée dans l'étiquette | — |
| l.211 item 11 | 0 sur les 5 graines officielles, même en distribution → E014 l.65, l.73 ; pilote VAL-OOD 1,000 → l.170–171 ; [HYPOTHÈSE] instabilité du straight-through, pas une preuve contre les pointeurs **relatifs**, non testé → l.170–172 | « pointers » → « relative pointers » (7c) | — |
| l.224 piste « The interface as a first-class object » | description de la piste (pas une affirmation) ; recherche de l'orchestrateur, 27/09, sur la piste voisine du signal auto-généré (« E015-A2 » dans la note) → note l.2–4, l.8 ; sources citées → note l.16, l.18, l.19, l.23, l.24, l.25 ; verdict « partiellement fait », traduction fidèle → note l.5, l.33 ; contre-pied MCC → note l.41–42 ; recherche propre à l'archive d'interfaces non versionnée → `git ls-files vault/echanges/` ne liste pas F05.md | liste PathNet … FunSearch (8a, **N**, source hors dépôt) ; « co-evolving problems with solvers » comme objet de la note (8b, **N**) ; code « E015-A2 » retiré du titre (8e) | — |

**Étape 5 (journal).** Aucune puce réécrite ne s'appuie sur une entrée du journal : toutes renvoient directement aux README d'expérience. Aucune entrée modifiée. Pour la relecture, je signale **sans le corriger** (hors mandat) : l'entrée 19 (E015, l.166) dit « exact up to 1,000 digits » pour ECH0, ce qui est vrai en T-LONG, alors que s3 tombe à 27,5 % en propagation pure à 1 000 (E015 l.108) ; l'entrée 18 (E014) reprend « composition loses nothing as long as the reading is correct », phrase de la source (E014 l.12–13) que sa propre P4 contredit à 1 000 chiffres (l.123). [HYPOTHÈSE] Ce sont les mêmes défauts de classe, mais dans le journal ; ils relèvent d'un autre mandat.

**Points de vigilance pour R0xx.**
- Deux affirmations reposent sur une **énumération** que j'ai rendue exhaustive pour les expériences citées (graines ≥ 90 % à 16, l.189). Contrôle suggéré : ce ne sont pas des clauses d'exclusivité, mais chaque « none » se vérifie ligne par ligne.
- Le dépôt parle désormais d'une recherche d'antériorité « not versioned in the repository » (l.224). C'est vrai au 29/09 (F05.md non suivi par git) ; à mettre à jour si ce mandat est un jour archivé et versionné.
- Les puces sont plus longues (voir diff). C'est le coût du « chiffre pour chiffre » ; le README fait toujours 284 lignes.

### Preuves
```
$ git diff --stat f99553a..HEAD
 README.md | 16 ++++++++--------
 1 file changed, 8 insertions(+), 8 deletions(-)
$ grep -c VERIFIED README.md   (avant, git show f99553a:README.md)
7
$ grep -c VERIFIED README.md   (après, ab352a5)
7
$ git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer …|sk-…|team_…|@gmail' -- README.md → rc=1
$ grep -inE 'fils|enfant|child|kid|son' README.md → (vide)
$ head -1 README.md → # 🧠🐜 EV-LLM — a public research log   (H1 inchangé ; seules les l.188–193, 211, 224 changent)
$ git log -1 --format=%B
docs(readme): rebuild synthesis bullets bottom-up from sources (after R013/R014)

Each labelled bullet outside the experiment log (l.188-193, l.211, l.224)
was split into atomic claims and traced to its sources at their tips
(table in the M0039 report). Only the claims carried by a cited source are
kept; conditions added (aligned/given/frozen/curriculum, seeds, post hoc);
exclusivity words removed (single exception, whenever, often, without loss).
Unsourced claims removed: E012 X1 as "without alignment" (X3 is the flat
condition), "discrete" interface for E014 R1G (soft), "limits come from
reading" (E015 s3), E013 for "computation without the reading", and the
E015-A2 prior-art list (not versioned in the repository).
Experiment log, method, license and links unchanged.

Co-Authored-By: Malik & Claude

$ git push origin docs/readme-2026-09-28
   f99553a..ab352a5  docs/readme-2026-09-28 -> docs/readme-2026-09-28
$ git ls-remote origin refs/heads/docs/readme-2026-09-28
ab352a58a9da5f631717776a14ebb4fb6dba4049	refs/heads/docs/readme-2026-09-28
```

`git diff f99553a..HEAD`, en entier :
```diff
diff --git a/README.md b/README.md
index b522826..b197180 100644
--- a/README.md
+++ b/README.md
@@ -185,12 +185,12 @@ Malik's instruction at 20:35: stop redoing known work, take the opposite tack.
 
 ## What we believe we know today
 
-- [VERIFIED — E011, E012, E013] **Computing is easy with almost nothing.** Once the digits are aligned, the carry is discovered by evolution (E012: one hidden unit) or learned (E013: 1,131 parameters) with 100 to 10,000 examples, stays stable under cross-entropy (E011), and holds up to 1,000 digits.
-- [VERIFIED — E008, E009-bis, E010, E013 I2, E014 R0] **The wall is locating, aligning, wiring.** Whenever the system must find on its own which digit to read, it fails beyond seen lengths, whatever its size (from ~1,900 parameters to ~3.2 million) — the single exception being one seed out of five with a curriculum (E014 R0b, 1/5 at 16 and 100 digits).
-- [VERIFIED — E014, E015 ECH0, E016 DONNÉ] **What got over the wall: a discrete symbolic interface between frozen skills.** Two frozen skills connected by symbols compose without retraining: at least 90 % exact at 16 and 100 digits on 4/5 seeds when the interface is given (E014 R1G), 100 % on 2/5 seeds when the wiring is given and the interface must be invented (E015 ECH0), and on 9/9 pairs × 5/5 seeds when the interface is given (E016 DONNÉ, 100 % at 100 digits). At 1,000 digits it holds only sometimes: 1/5 (E014), 2/5 (ECH0), 71.7 % (DONNÉ). The remaining limits come from reading, not from computing.
-- [VERIFIED — E012 X1, E015, E016, E016-A2] **What did not get over it:** blind evolution without alignment, free assembly, all-or-nothing social pressure, a dense scalar signal.
-- [VERIFIED — E005, E006, E008, E010, E013, E015] **Misplaced confidence is blind.** Errors are often "confident" when confidence bears on the wrong step: the copy, the computation without the reading, the champions without the interface. A confidence taken at each step, reading included, separates much better (E014).
-- [HYPOTHESIS] The missing lever would be an **intermediate signal the machine gives itself** (consistency between modules, prediction of its own flows), rather than the final verdict alone. None of this has been tested.
+- [VERIFIED — E011, E012, E013] **With the alignment given, the learned part is small.** Digits of the same rank presented together, least significant first, number of steps given: an evolutionary search guided by MDL finds an exact carry circuit in aligned decimal on 2/5 seeds with 100 examples and on 4/5 with 1,000, exact up to 1,000 digits; the shortest circuits found have a single hidden unit, the carry (E012, threshold primitives given; in binary, 0/5). A learned accumulator of 1,131 parameters with a one-number state reaches 100 % from 16 to 100 digits (5/5 seeds) and 99.3 % on average at 1,000 (≈ 591,000 unique examples seen). Trained on a fixed set, the same kind of accumulator (1,326 parameters) fails with 100 unique examples (0/5), passes long numbers with 1,000 but not pure carry propagation at 1,000 digits (1/5 seeds at ≥ 90 %, test added post hoc), and scores 100 % everywhere with 10,000 (E013). A binary network built exact by hand keeps its rule up to 1,000 bits under cross-entropy alone (5/5), but not under strong weight penalties (E011). E013 says what this measures: mostly the value of the given structure.
+- [VERIFIED — E008, E009-bis, E010, E013 I2, E014 R0 and R2, E015] **In these runs, the wall was locating, aligning, wiring.** When the system had to find on its own which digit to read (trained on 1 to 5 digits; from 1,922 parameters in E013 I2 to ~3.2 million in E008 and E010), accuracy fell with length: E008, standard transformer 0.0 % from 6 digits, and with the known fix 91.2 % at 6, 7.9 % at 7, 0.1 % at 8; E009-bis, 1 run out of 5 learns the distribution, then 17.3 % at 6 and 0 % from 7; E010, with the column scratchpad, 33.1 % at 6 and 0 % from 7; E013 I2, all 5 seeds at 0 % from 64 digits. Seeds at ≥ 90 % at 16 digits: none in E008, E009-bis, E010, E013 I2, E014 R0a and R2; 1 out of 5 in E014 R0b, with a curriculum (100 % at 16, 99.8 % at 100, 62.5 % at 1,000). In E015, assembling frozen modules failed whenever the wiring was not given in full: 0/5 from scratch, 0/5 with a single instruction missing.
+- [VERIFIED — E014 R1G, E015 ECH0, E016 DONNÉ] **Where length generalisation was obtained: frozen modules plugged together through a given structure, with no retraining.** A reader trained alone to set out the columns, frozen in front of the frozen accumulator of E013, with no joint training: at least 90 % exact at 16 and 100 digits on 4/5 seeds; the intermediate task and the interface were defined by us, and the reader passes probabilities, not symbols (E014 R1G). Wiring given around one frozen champion, symbol-to-symbol interface invented by search: 100 % from 16 to 1,000 digits on 2/5 seeds (E015 ECH0). Exact symbol translation given between frozen readers and frozen accumulators: 9/9 pairs on 5/5 seeds, 100 % at 16 and 100 digits (E016 DONNÉ). At 1,000 digits: 1/5 seeds at ≥ 90 % (E014 R1G), still 2/5 (E015 ECH0), 71.7 % on average (E016 DONNÉ). There, the loss comes mainly from the reader in E014 (the composed addition also falls a few points below the reading, e.g. 23.0 % against 28.5 % for seed 1) and from the reader in E016; in E015, seed 3 falls to 27.5 % on pure carry propagation, a limit of the champion, not of the interface.
+- [VERIFIED — E012 X1 and X3, E015, E016, E016-A2] **What did not work here:** an evolutionary search guided by MDL with ≲ 0.6 % of the budget of Lan et al., in aligned binary (E012 X1: 0/5, all seeds stuck on a "hesitant" network) and on the flat input of E008, without alignment (X3: 0/5); assembly by search alone on three new tasks (E015: 0/5, from scratch or from an interface already found); the collective all-or-nothing reward with replay, a single formulation tested, and the per-pair reward as well (E016 COLL and IND: 0/5 seeds, no common language; the pairs that did learn generalise to 100 digits); a dense scalar reward (fraction of correct columns) or a 1-digit curriculum, on one pilot seed each (E016-A2: 1 pair out of 9).
+- [VERIFIED — E005, E006, E008, E010, E013, E014, E015, E016] **Here, a confidence taken on one step missed the errors made at another.** Wrong answers with a confidence ≥ 0.8 were measured for Jev on rare French rules and logic with distractors (9 evaluations out of 42 in E005; 5 cases replicated 5/5 in E006, one more case contested), for the standard E008 transformer (65–68 % of its errors at 6–7 digits) and for the one-number accumulator on sparse numbers (28 % of its errors, E013). Where the confidence covers one step only, errors from another step pass: on the final copy of the scratchpad, 606 confident errors out of 669 (E010); on the sum without the reading, the confident errors of R1G seeds 1–4 are almost all at 1,000 digits, where the reading is wrong (E014, post hoc), and in E016 DONNÉ, whose confidence excludes the reader, all 5,535 errors are confident; on the champions without the interface, 7,673 confident errors out of 13,783 (E015 ECH0; seed 5: 4,606 out of 4,606). In E014, a per-column confidence on the sum already lets R1G abstain on 77.3 % of its errors for 1.4 % of its correct answers (threshold set on validation); adding the confidence of the reading, recomputed post hoc on the test already read, lowers its confident errors from 1,218 to 227.
+- [HYPOTHESIS — E015] The missing lever would be an **intermediate signal the machine gives itself** (consistency between modules, prediction of its own flows), rather than the final verdict alone. None of this has been tested.
 
 ---
 
@@ -208,7 +208,7 @@ So that these cycles need not be repeated:
 8. **Approximate differentiable MDL** (E011). It behaves like a weight penalty and breaks one seed: not to be reused as is.
 9. **Evolution in binary** (E012). All seeds fall into a "hesitant" trap that could only be left by passing through more costly steps: truncation selection forbids it.
 10. **Single-number state** (E013). Perfect in distribution, wrong and confident on sparse numbers; a second state number is enough here.
-11. **Learned hard pointers** (E014 R2). 0 even in distribution: [HYPOTHESIS] an optimisation instability, not evidence against pointers.
+11. **Learned hard pointers** (E014 R2). 0 on the 5 official seeds, even in distribution, while the pilot seed reached 1.000 in validation: [HYPOTHESIS] an optimisation instability of the straight-through estimator, not evidence against relative pointers; not tested further.
 12. **Free assembly** (E015). Needle-in-a-haystack landscape: more trials (400,000 in the pilot) do not change the "copy a" attractor.
 13. **Collective all-or-nothing with replay** (E016). It freezes the team instead of building a bridge.
 14. **Dense scalar signal and short curriculum** (E016-A2). Faster lock-in, no take-off.
@@ -221,7 +221,7 @@ So that these cycles need not be repeated:
 
 - **Redesign the E013 synthesis**, one source per figure, then have it reviewed. E008 and E013 can then be merged.
 - **Per-column credit** (E016). The reward of column t only pushes the choices of column t; other variants are named in the E016 README (entropy floor, alternating frozen partner).
-- **E015-A2: the interface as a first-class object.** A co-evolved archive of interfaces, judged on their reuse, frozen, on never-seen tasks. Prior-art search done by the orchestrator (verdict "partially done"): PathNet, BounceGrad, Braylan 2016, Guijt et al. 2024, Cully 2015, Schug 2024, MAGELLAN, DreamCoder / Voyager / FunSearch. Not found: a measure of the reuse of the interface itself. The neighbouring lead, co-evolving problems with solvers, was also the subject of an orchestrator search on 27/09 (novelty search, MCC by Brant & Stanley, PowerPlay, DreamCoder, HOUDINI, CRL). Its verdict, "every building block exists, the assembly does not", is recorded with its sources in [`vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md`](vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md) [VERIFIED — sources listed in the note].
+- **The interface as a first-class object.** A co-evolved archive of interfaces, judged on their reuse, frozen, on never-seen tasks. Its prior-art search is not versioned in the repository and is not cited here. A neighbouring lead, an intermediate signal that the system makes for itself to guide the composition of frozen modules (called E015-A2 in the note), was the subject of an orchestrator search on 27/09, recorded with its sources in [`vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md`](vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md) [VERIFIED — the note]: novelty search, MCC by Brant & Stanley, PowerPlay, DreamCoder, HOUDINI, CRL, among others. Verdict "partially done": each building block exists separately; nobody has assembled frozen neural modules, evolved discrete wiring, an intermediate signal made by the system and length generalisation measured on an algorithmic task. The opposite tack proposed by the note: co-evolve the problem instances with the programs (MCC).
 - **ACQUIRE criterion v2** (A0-ter): contrast with an amnesic twin, threshold calibrated on noise, validated first on the oracle.
 
 ---
```

### Rituels de fin
- Rapport : ci-dessus.
- `vault/reprise/F01.md` réécrit (état, prochaine étape, leçon).
- `vault/runtime/events.jsonl` : ligne `RAPPORT_RENDU` ajoutée, `ts` = `2026-09-29T10:30:55+02:00`. `vault/runtime/state.json` : seule la clé `windows.F01` a changé ; les autres clés et fenêtres ont été contrôlées identiques par assertion ; `next_mandat_id` = `M0040` est toujours présent. Les deux fichiers sont ignorés par git.
- **Commit racine : fait. Push `main` : REFUSÉ → STOP partiel propre.**
```
$ git commit -- vault/reprise/F01.md          → 5d9edf4 (main local, vault seul)
$ git push origin main                        → rejected (non-fast-forward)
$ git fetch origin && git merge --ff-only origin/main
fatal: Not possible to fast-forward, aborting.
$ git rev-list --left-right --count main...origin/main
1	10
$ git ls-remote origin refs/heads/main
4bad581e54db25fc0fea1df8b4d99448b7bfdef3	refs/heads/main
```
  Il n'y a pas eu de nouvelle tentative, ni de rebase, ni de reset (règles communes). `main` local porte donc 1 commit non poussé (`5d9edf4`, uniquement `vault/reprise/F01.md`) et diverge d'`origin/main`. À intégrer par l'orchestrateur : merge non fast-forward, ou recréation du commit sur `origin/main`.
- Branche : `docs/readme-2026-09-28` poussée, `ab352a58a9da5f631717776a14ebb4fb6dba4049	refs/heads/docs/readme-2026-09-28`.

### ⚠️ Alerte pour l'orchestrateur : un README a déjà été fusionné sur `main` par une autre branche
Je l'ai découvert au moment du push, après le travail : `origin/main` (`4bad581`) contient déjà un README racine et une LICENSE. Ils viennent de la branche **`docs/readme-digeste`**, fusionnée par `4ea9bd0` après **R015 GO** (tip `39f015f`). Son historique comporte `9a6a11b` : « single pass on all synthesis sentences after R014 (third-party source audit, 13 defects) ». [VÉRIFIÉ] par `git log main..origin/main` et `git ls-tree origin/main README.md`.
- Mes gardes (§1) étaient au vert : tip `f99553a` exact, worktree propre. Le mandat ne demandait pas de vérifier `origin/main`.
- Conséquence : `docs/readme-2026-09-28` est probablement **remplacée** comme candidate au merge. Elle entrera en conflit avec le README de `main`. [HYPOTHÈSE] Le tableau de traçabilité de ce rapport reste utilisable pour contrôler les puces de synthèse du README de `main`. Je ne l'ai pas comparé à ce README : ce serait hors mandat.
- Question que j'aurais posée : « Faut-il encore redoubler et fusionner `docs/readme-2026-09-28`, ou reporter ses constats sur le README de `main` ? » Options : (a) redoubler cette branche puis la fusionner avec résolution de conflit ; (b) abandonner la branche et confronter le README de `main` au tableau de l'étape 2 ; (c) ne rien faire. Je choisirais (b) : un seul document fait foi par sujet (R4), et c'est celui de `main` qui a reçu un GO.
- `sync-vaults.sh` n'a pas été lancé (hors mandat).
- Leçon candidate à la remontée transverse (R5) : écrite dans `vault/reprise/F01.md`. Il faut écrire une synthèse de bas en haut et scoper les titres de puce au présent général.

M0039
Implementation      ✅
Tests               ✅   (traçabilité 41 affirmations + relecture croisée ; greps secrets / enfant / étiquettes ; pas de test exécutable pour un README)
Commit              ✅
Branch push         ✅
Review              ❌
Merge main          ❌
Main push           ❌   (vault seul ; non-fast-forward, ff-only impossible, STOP partiel)
TASK STATUS         READY_FOR_INTEGRATION
PROJECT STATUS      NOT_INTEGRATED
