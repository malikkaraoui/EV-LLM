---
date: 2026-09-26
revue: R008
branche: exp/e006-replication-frontiere
tip: 57e0e416694f323b8f34288b7984f90c6e521898
verdict: RESERVE
---

# R008 — Doublage de exp/e006-replication-frontiere (M0011, E006)

Doubleur : F03 (Opus, indépendant de l'auteur F04). Worktree détaché en lecture seule `.claude/worktrees/F03-R008` @ `57e0e41`, rien modifié (`git status --porcelain` → 0 ligne). Tous les rejeux faits sur une **copie** dans le scratchpad. Aucun appel API.

**Verdict global : RÉSERVE** — la mécanique, les chiffres et l'hygiène sont irréprochables (6 axes ✅) ; la **lecture** (axe 4) doit être amendée sur deux points avant merge. Pas de merge.

## Tableau des axes

| # | axe | verdict | raison vérifiée (résumé) |
|---|---|---|---|
| 1 | Rejeu | ✅ GO | 12 tests OK ; 18 cas / 0 écart ; `aggregate.py` et `analyse.py` rejoués → sorties identiques ; 103 × 200 et 102 intervalles recomptés ; `gen_cases.py` rejoué → `cases.json` octet-identique |
| 2 | Préenregistrement | ✅ GO | `cases.json` sha256 `0245036b…e042` = valeur citée ; committé `820d85b` 16:43:02 < 1er appel 16:43:09 ; inchangé ensuite ; seuils = ceux d'E001 `run.py` (antérieurs) |
| 3 | Chiffres | ✅ GO | recalcul par parseur indépendant (sans `run.extract`) : R, P, L-PAS, L-DIS, C tous identiques au README |
| 4 | Lecture honnête | ⚠️ RÉSERVE | R-F4-04 `a_sup_f` et L-DIS1 `e_sup_d` à reclasser **contestés** (voir §4) ; « ne change pas P(true) » (C) un cran trop fort ; mention F3-02 « à confirmer par R004 » périmée |
| 5 | Sécurité dépôt public | ✅ GO | `git grep` motifs sensibles → 0 ; aucun `.env` ni `raw.jsonl` suivi |
| 6 | Hygiène git | ✅ GO | trailer sur les 2 commits propres ; diff depuis le merge-base (`08d80f7`) limité à `E006-replication-frontiere/` |
| 7 | CLAUDE.md / rules `paths:` | ✅ GO | aucun CLAUDE.md imbriqué ni `.claude/rules/` au tip ni sur main |

## Gardes

```
$ git rev-parse origin/exp/e006-replication-frontiere
57e0e416694f323b8f34288b7984f90c6e521898
$ git log $(git merge-base origin/main 57e0e41)..origin/main -- research/experiments/E006-replication-frontiere
(vide)
$ ls vault/revues | grep R008
(vide)
```
Garde d'ordre de merge : au démarrage `15487b0` était ABSENT d'`origin/main` ; en cours de doublage R007 a mergé (`a70b907 Merge exp/e005-jev-hors-distribution [R007]`) → `git merge-base --is-ancestor 15487b0 origin/main` → vrai. Merge-base E006/main devenu `08d80f72265d36a56ad5e916c4097426bc93cc05`. Sans objet ici puisque le verdict n'est pas GO. [VÉRIFIÉ] `git diff --stat 08d80f7 15487b0` = `E005/README.md` seul : un merge ultérieur d'E006 sur main sera sans conflit sur E005.

## Axe 1 — Rejeu

```
$ PYTHONDONTWRITEBYTECODE=1 python3 -m unittest test_run_paced
Ran 12 tests in 0.033s
OK
$ python3 verifie_logique.py | tail -1
18 cas logiques verifies, 0 ecart(s)
```
Copie `E001/E005/E006` dans le scratchpad, puis :
```
$ python3 ../E001-jev-sonde/aggregate.py --cases cases.json --out-root $S/agg results/2026-*
meta egal: True rows egal: True nrows 30        # comparaison à agregat-2026-09-26T172726+0200/summary.json (run_id exclu)
summary.md identique (hors en-tete)             # seule la ligne 1 diffère : l'horodatage de l'agrégat
$ python3 analyse.py
analyse.md IDENTIQUE
analyse.json IDENTIQUE                            # cmp octet par octet
$ python3 gen_cases.py
25 cas, 30 questions, 103 reponses 200 visees
gen_cases rejoue : assertions OK, cases.json octet-identique
```
Recompte indépendant (lecture directe des 13 `raw.public.jsonl`) :
```
dossiers 13 appels 103
statuts Counter({200: 103})
intervalle_s n 102 min 26.0 max 26.0            # champ auto-déclaré
depuis t_epoch: n 102 min 25.998 max 26.016      # recalculé depuis les horodatages bruts
premier 2026-09-26T16:43:09+02:00 dernier 2026-09-26T17:27:22+02:00
ordre groupes: R×30 C×40 L×24 P×9                # ordre R→C→L→P respecté
réponses par cas : R et C = 5 ; L et P = 3       # 6×5 + 8×5 + 11×3 = 103
R identiques a E005 (4 champs: state, questions, attendu, justification): 6
```
[VÉRIFIÉ] L'intervalle min 25.998 s depuis `t_epoch` est une granularité d'horloge (26.0 arrondi), pas une violation du rythme de 26 s.

## Axe 2 — Préenregistrement

```
$ shasum -a 256 cases.json
0245036b80c36d451371a1fa3f7555ba17fb2806d375699b341fb61a3888e042  cases.json   # = README l.13
$ git log -1 --format='%H %cI' 820d85b
820d85baa99cc3201e5b555fcf6b01148eab8e41 2026-09-26T16:43:02+02:00            # 1er appel : 16:43:09
$ git log --follow --format='%h %cI %s' 57e0e41 -- .../cases.json
820d85b 2026-09-26T16:43:02+02:00 feat(e006): corpus preenregistre ...          # un seul commit
$ git diff --quiet 820d85b 57e0e41 -- cases.json gen_cases.py verifie_logique.py && echo inchanges
corpus+gen+verif inchanges depuis 820d85b
```
Remarque (sans effet sur le verdict) : `analyse.py` est committé **après** les appels (`57e0e41`). Mais ses seuils sont ceux de `E001/run.py` l.140-141 et l.167 (présents dès `7e953a9`, antérieur), et le critère « répliqué » applique celui du mandat M0011 (« ≥ 4/5 non conformes et P extrême »). [VÉRIFIÉ] Aucun seuil n'a été créé après avoir vu Jev. R-F4-04 tombe pile sur le seuil `≤ 0.2` (médiane 0.20) : ce seuil est hérité, pas ajusté.

## Axe 3 — Chiffres recalculés (script `recalc_r008.py`, parseur `json.loads` indépendant de `run.extract`)

```
R-F1-04  correcte  n=5 P=[0.83, 0.84, 0.84, 0.85, 0.83] med=0.84 nonconf=5
R-F1-05  correcte  n=5 P=[0.87, 0.83, 0.83, 0.84, 0.84] med=0.84 nonconf=5
R-F1-08  correcte  n=5 P=[0.86, 0.87, 0.86, 0.87, 0.86] med=0.86 nonconf=5
R-F3-02  correcte  n=5 P=[0.86, 0.84, 0.85, 0.83, 0.86] med=0.85 nonconf=5
R-F4-04  a_sup_f   n=5 P=[0.37, 0.25, 0.17, 0.2, 0.13] med=0.20 nonconf=5
P-F1-04  correcte  n=3 P=[0.58, 0.64, 0.61] med=0.61 nonconf=0
P-F1-05  correcte  n=3 P=[0.9, 0.91, 0.9] med=0.90 nonconf=0
P-F1-08  correcte  n=3 P=[0.64, 0.75, 0.67] med=0.67 nonconf=0
L-PAS2..6 med = 0.97 / 0.85 / 0.95 / 0.94 / 0.90, nonconf=0 partout
L-DIS0 contradiction×3 P(contradiction) med 0.73 | e_sup_d [0.6, 0.59, 0.61]
L-DIS1 coherent×3      P(contradiction) med 0.34 | e_sup_d [0.21, 0.18, 0.16]
L-DIS2 coherent×3      P(contradiction) med 0.14 | e_sup_d [0.39, 0.4, 0.45]
R-F4-01 coherent×5     P(contradiction) med 0.08 | e_sup_d [0.53, 0.61, 0.68, 0.6, 0.6]
C1 avec=0.9700 sans=0.9760 ecart=-0.0060
C2 avec=0.9700 sans=0.9720 ecart=-0.0020
C3 avec=0.9700 sans=0.9700 ecart=+0.0000
C4 avec=0.9480 sans=0.9600 ecart=-0.0120
ecarts moy -0.0050 min -0.0120 max +0.0000
```
Tous identiques aux tableaux du README et d'`analyse.md`. Aucun écart.

## Axe 4 — Lecture honnête (⚠️ RÉSERVE)

Le README est globalement prudent : [VÉRIFIÉ]/[HYPOTHÈSE] bien posés, limites franches (« aucune conclusion générale », « 5 points ne font pas une courbe », pas de paraphrase). J'ai vérifié chaque [VÉRIFIÉ] contre les données : dispersions (≤ 0.04 phrases, 0.07 F4-01), P(contradiction) monotone 0.73/0.34/0.14/0.08, P(E > D) non monotone 0.60/0.18/0.40/0.60, L-PAS4 0.95 contre R-F4-04 0.20, statut L-DIS0 « P 0.67–0.80 ». Tout est exact. Trois points restent.

### 4a. Point scientifique tranché : R-F4-04 `a_sup_f` et L-DIS1 `e_sup_d` → **à reclasser « contestés »**

- [VÉRIFIÉ] En logique classique, l'attente `true` est correcte. A > F suit de R1 sur les faits donnés, et d'un ensemble contradictoire on déduit de toute façon n'importe quoi. Jev a donc tort au sens strict.
- Mais la question « Peut-on déduire A > F uniquement à partir des faits et règles donnés ? » est posée dans un état où R2 énonce littéralement « ni A > F ni F > A ». En langue naturelle, « peut-on déduire » glisse vers « peut-on conclure valablement ». Or R2, lue comme contrainte prioritaire, l'interdit. La réponse `false` a donc une **lecture défendable**, et le préenregistrement ne levait pas l'ambiguïté : aucune consigne ne dit « déduire au sens de R1 seule » ni « ignorer les contraintes ».
- [VÉRIFIÉ] Les données de l'auteur vont dans ce sens. Mêmes faits, même ordre : L-PAS4 (sans R2) donne 0.95, R-F4-04 (avec R2) donne 0.20. La seule différence est la présence de la règle qui dit « non ». On ne peut pas séparer « erreur de déduction » et « R2 lue comme réponse » : c'est exactement le confondant que l'auteur nomme en Lecture 3 [HYPOTHÈSE].
- **Décision** : ces deux cas ne doivent pas compter comme « faux et sûr » (erreur avérée) mais comme **contestés (ambiguïté de la question dans un ensemble contradictoire)**. Le fait **observé** reste [VÉRIFIÉ] et utile : réponse reproductible, et instabilité de P(E > D) sous un seul fait redondant (0.60 → 0.18 → 0.40 → 0.60).
- Les 5 autres ne dépendent pas de ce point. Il s'agit de F1-04, F1-05, F1-08, F3-02 (non contestée, R004 l.54-64) et F4-01 `statut`. Le critère de `statut` définit explicitement la contradiction comme « règle violée par des faits donnés **ou déduits** », et Jev la détecte à 0 distracteur (L-DIS0, 3/3). [HYPOTHÈSE] Une lecture « R2 bloque R1 » rendrait aussi `coherent` défendable pour F4-01. Mais elle contredit la définition donnée dans la question elle-même, et je ne la retiens pas.
- Compte honnête après reclassement : **5 « faux et sûr » non contestés répliqués sur 5**, plus **1 réponse contestée répliquée** (F4-04). L-DIS1 n'est pas un nouveau « faux et sûr » : c'est un cas contesté, sur 3 appels.

### 4b. Contamination : « ne change pas P(true) » est un cran trop fort

```
C1-avec [0.97 ×5]           C1-sans [0.98, 0.97, 0.97, 0.98, 0.98]
C4-avec [0.94, 0.95 ×4]     C4-sans [0.96 ×5]          # aucun recouvrement
```
[VÉRIFIÉ] L'effet est sans commune mesure avec le signal d'E001 (~0.2) : conclusion de fond correcte. Mais les signes sont 3 négatifs, 0 positif et 1 nul, et sur C4 les deux membres ne se recouvrent pas (5/5 contre 5/5). « Du même ordre que la dispersion (≤ 0.01) » est littéralement vrai (0.012 contre 0.01), mais « ne change pas » ne l'est pas tout à fait. Formulation proposée : « aucun effet de l'ordre de celui d'E001 ; un décalage ≤ 0.012, négatif ou nul sur 4/4 paires, n'est pas exclu (4 paires, non testé statistiquement) ».

### 4c. F3-02 : mention périmée

Le README écrit « attente à confirmer par R004 » (Hypothèses, tableau R, Lecture 1, Limites). Or R004 (sur main, `vault/revues/2026-09-26-R004-…md` l.54) la déclare **non contestée** [VÉRIFIÉ]. L'erreur va dans le sens prudent, mais c'est une documentation en retard (R4).

### Correctifs demandés pour lever la réserve (README seul, aucun chiffre ni donnée à toucher)
1. Lecture 1, Lecture 4 et tableau R : R-F4-04 et L-DIS1 marqués « contestés (ambiguïté) » ; titre de la Lecture 1 réécrit en « 5 faux et sûr non contestés répliqués + 1 contesté ».
2. Lecture 5 : reformuler selon 4b.
3. F3-02 : « non contestée (R004) » partout où « à confirmer » apparaît.
4. `analyse.md`/`analyse.py` peuvent rester tels quels (règle mécanique préenregistrée) ; le reclassement relève de la lecture.

## Axe 5 — Sécurité dépôt public

```
$ git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 57e0e41 -- research/ | wc -l
0
$ git ls-tree -r --name-only 57e0e41 | grep -E '(^|/)\.env$|raw\.jsonl$'
(vide)
$ git grep -nIiE 'karaoui|malik@|ownerId|userId|accountId|projectId|AI_GATEWAY_API_KEY=' 57e0e41 -- research/experiments/E006-replication-frontiere | wc -l
0
```
Note : les `raw.public.jsonl` contiennent `providerMetadata.gateway.routing` (`providerRequestId`, fournisseurs, `startTime`), mais aucun identifiant de compte ou d'équipe. Même format qu'E001/E005 déjà publiés. L'auteur signale lui-même avoir chargé la clé **en mémoire** dans un script ad hoc pour vérifier qu'elle ne fuit pas. Rien n'a été affiché ni écrit, et c'est à la limite de la règle `.env`. Je le note pour l'orchestrateur, sans impact sur le verdict.

## Axe 6 — Hygiène git

```
$ for c in $(git rev-list origin/main..57e0e41); do ... grep -c '^Co-Authored-By: Malik & Claude$'; done
57e0e41 1
820d85b 1                       # aucun autre trailer Co-Authored-By
$ git diff --name-only $(git merge-base origin/main 57e0e41) 57e0e41 | grep -vE '^research/experiments/E00[56]-'
(vide)                          # merge-base = 08d80f7 après le merge R007 : 50 fichiers, tous sous E006-replication-frontiere/
```

## Axe 7 — CLAUDE.md imbriqués / rules à `paths:`

```
$ git ls-tree -r --name-only 57e0e41 | grep -iE '(^|/)CLAUDE\.md$|\.claude/rules/'
(vide)
$ git ls-tree -r --name-only origin/main | grep -iE '(^|/)CLAUDE\.md$|\.claude/rules/'
(vide)
```
Rien à mettre à jour.

## Suite

Pas de merge (verdict RÉSERVE). La levée demande un commit README seul sur la branche, suivi d'un doublage léger ciblé sur l'axe 4. `origin/main` contient déjà E005 corrigé : le merge suivant n'aura plus de garde d'ordre à attendre.
