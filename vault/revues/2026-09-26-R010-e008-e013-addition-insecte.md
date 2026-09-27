---
date: 2026-09-26
revue: R010
branche: exp/e013-insecte
tip: 3246ae8eaf78c5814dd55e7bf941c7ee30e69dd2
verdict: RESERVE
---

# R010 — Doublage de exp/e013-insecte (E008 palier 0 + E013 insecte)

Doubleur : F03 (Opus, indépendant des auteurs F01/M0021 et F04/M0026). Worktree détaché en lecture seule `.claude/worktrees/F03-R010` @ `3246ae8`, rien modifié (`git status --short` → 0 ligne). Rejeux dans le scratchpad (copie des deux dossiers d'expérience pour le réentraînement). Aucun appel API. Rédigé le 2026-09-27 (date du frontmatter imposée par le mandat).

**Verdict : RÉSERVE — pas de merge.** Le résultat phare tient : [VÉRIFIÉ] I1 H ≥ 2 est exact à 1 000 chiffres, sur des paires que j'ai tirées moi-même, avec une inférence numpy réécrite de zéro et un décodage plus strict que celui de l'auteur ; une graine neuve (11) réentraînée donne le même résultat. La réserve porte sur **une affirmation [VÉRIFIÉ] du README au sujet d'I3 N = 1 000** (« il suffit de 1 000 exemples uniques pour la règle à 100 chiffres »), que mon jeu adverse de **propagation pure** contredit sur 2 graines sur 5. Elle vient d'une faiblesse du jeu ADV-CASCADE officiel, dont seulement ~20 % des rangs sont des rangs de propagation.

## Tableau des 7 axes

| # | axe | verdict | raison vérifiée |
|---|---|---|---|
| 1 | Rejeu | ✅ GO | tests E008 15/15 et E013 12/12 OK ; inférence I1 réimplémentée en numpy, 20/20 graines I1 conformes au rapport sur des paires neuves ; graine 11 réentraînée : 100 % à 1 000 chiffres (numpy et évaluateur officiel) ; E008 recompté, 0 incohérence |
| 2 | Préenregistrement | ✅ GO | préenregistrements E008 et E013 ancêtres du code, poussés seuls, amendements A1 en ajout pur (0 ligne supprimée) ; chronologie : préenregistrement < code < pilotes < A1 < contrôles < runs officiels ; aucun sha256 d'attentes cité (sans objet) |
| 3 | Chiffres | ✅ GO | 9 cellules E013 recalculées depuis les `eval.jsonl` bruts = `par_graine` publié à 1e-12 près ; 5/5 et 0/5 recomptés ; faux et sûrs 204/722 ; E008 : tableau entier + faux et sûrs + longueurs de réponse identiques |
| 4 | Lecture honnête | ⚠️ RÉSERVE | la phrase I3 « 1 000 exemples suffisent pour la règle à 100 chiffres » [VÉRIFIÉ] est **contredite** en propagation pure (graine 5 : 11/100 à L = 100, 81/100 à L = 16) ; écart-type de population (ddof 0) non déclaré dans E013 alors qu'E008 utilise ddof 1 |
| 5 | Sécurité dépôt public | ✅ GO | `git grep` des motifs → rien (rc = 1) ; aucun `.env`/`raw.jsonl` suivi (seul `.env.example`, préexistant sur main, hors diff) ; aucun chemin absolu ni adresse dans le diff ; aucun binaire |
| 6 | Hygiène git | ✅ GO | 10/10 commits avec `Co-Authored-By: Malik & Claude`, aucun autre trailer ; périmètre = 16 fichiers E008 + 15 fichiers E013, rien d'autre |
| 7 | CLAUDE.md / rules | ✅ GO | aucun CLAUDE.md imbriqué ni `.claude/rules/` dans l'arbre ; le diff n'en touche aucun |

## Preuves

### Gardes
```
$ git rev-parse origin/exp/e013-insecte
3246ae8eaf78c5814dd55e7bf941c7ee30e69dd2
$ git log $(git merge-base origin/main 3246ae8)..origin/main -- research/experiments/E008-addition research/experiments/E013-insecte
(vide)            # merge-base 677b9282
$ ls vault/revues | grep R010 ; git ls-tree -r --name-only origin/main -- vault/revues | grep R010
(vide)
```

### Axe 1 — Rejeu

**(1) Tests** (`PYTHONDONTWRITEBYTECODE=1`, venv `ev-llm-e008`, dans le worktree détaché) :
```
E008 : Ran 15 tests in 14.969s  OK
E013 : Ran 12 tests in 10.173s  OK
```

**(2) Inférence I1 réimplémentée** (`rejeu_numpy.py` du scratchpad, qui n'importe **aucun** module E008/E013). Les safetensors sont lus à la main (en-tête JSON + float32 little-endian). La cellule est réécrite en numpy : `z = relu([onehot11(a) ; onehot11(b) ; h] W1ᵀ + b1)`, `h = tanh(z Whᵀ + bh)`, `logits = z Woᵀ + bo`, avec max(ℓa, ℓb) + 1 pas. La vérité est `a + b` de Python. La graine de tirage R010 est `random.Random(2026092710)`, sans lien avec les graines 3013–3018. Deux scores :
- **strict** : la séquence émise complète doit égaler la somme complétée par un 0 de tête (le 0 final doit être émis) ;
- **souple** : la règle de l'auteur (retrait d'un seul 0).

Jeux : uni16 (300), uni100 (200), uni1000 (60) ; cascade (a + b = 10^L) + 99…9 + 1 et 99…9 + 99…9 ; creux (p = 0,15) ; asym (L + 1–5 chiffres), à L = 100 et L = 1 000. Chaque cellule se lit `strict/souple/n` :
```
I1-H2-s1..s5 : uni16=300/300/300 uni100=200/200/200 uni1000=60/60/60 cascade100=40/40/40 creux100=41/41/41 asym100=40/40/40 cascade1000=41/41/41 creux1000=41/41/41 asym1000=40/40/40   (x5, identique)
I1-H4-s1..s5, I1-H8-s1..s5 : idem, 100 % strict partout
I1-H1-s1 uni1000=59/60 creux100=32/41 creux1000=12/41   (reste 100 %)
I1-H1-s2 creux100=15/41 creux1000=2/41
I1-H1-s3 uni1000=59/60 creux100=29/41 creux1000=4/41
I1-H1-s4, s5 : 100 % partout
I3-N100-s1 : 0 partout
```
Le paramétrage lu est cohérent : H = 2 → 1 196 paramètres, comme au README. Le défaut de H = 1 sur les nombres creux (graines 1–3, graines 4–5 saines) est **reproduit** indépendamment. Strict = souple partout : le retrait du 0 de tête n'a rendu aucun service indu.

**(3) Graine neuve 11** (commande du README, sur une copie des dossiers dans le scratchpad) :
```
$ entraine.py --configs I1-H2 --graines 11      -> FILE TERMINEE (42,9 s)
{'pas': 6000, 'meilleur_pas': 6000, 'meilleur_val': 1.0, 'params': 1196, 'exemples_uniques_vus': 590920, 'fini': True}
numpy R010 : I1-H2-s11 uni16=300/300 uni100=200/200 uni1000=60/60 cascade/creux/asym 100 et 1000 = 100 %
evalue.py  : T-LONG 10..1000 = 1.0 ; ADV-CASCADE/ZEROS/ASYM 10..1000 = 1.0 (24 cellules)
propagation pure : P16=100/100 P100=100/100 P1000=40/40
```

**(4) E008 recompté** depuis les `eval.jsonl` (worktree F01-M0021 @ `af281f5`), avec la vérité recalculée `str(int(a) + int(b))` :
```
incoherences juste vs verite recalculee : 0
T-OOD|6 B-STD=0.0±0.0 B-REF=91.2±6.2 ; T-OOD|7 0.0 / 7.9±3.3 ; T-OOD|8 0.0 / 0.1±0.2 ; T-OOD|10,12,16 0.0 / 0.0
T-ID|2..5 B-STD 100.0/99.5/98.8/98.4  B-REF 100 ; T-CARRY|6/7/8 B-REF 87.7±9.4 / 8.6±3.4 / 0.7±0.4 ; T-CARRY|10 B-REF 0.2
faux-surs : B-STD L6 977/1500, L8 488/1500 ; B-REF L6 107/132, L7 924/1381
B-STD s1 L6 : 486 reponses d'1 chiffre, 0 de bonne longueur ; B-REF s1 bonne longueur L6/7/8 : 500/499/494
```
Tout est identique au README E008.

**Fuite et sélection** : la fuite est structurellement impossible pour T-LONG et VAL, puisque l'entraînement se fait sur ≤ 5 chiffres et que les jeux ont L ≥ 6. C-PARCŒUR rejoué dans la copie donne `max 0.000`, table de 591 106 paires, et `controles.json` est identique au fichier commité (verdict, oracle, par jeu). Le checkpoint est choisi sur VAL-OOD, par `>=` (donc le plus tardif en cas d'égalité, comme préenregistré). Aucun `resume.json` sur les 8 runs pilotes : le TEST n'y a pas été lu. `evalue.py` refuse une seconde lecture.

### Axe 2 — Préenregistrement
```
a2f703f 2026-09-26 21:06:52 prereg E008  <  51725c5 21:11:33 code  <  b7ecc54 21:42:06 A1  <  f073298 controles  <  af281f5 resultats
997d87f 2026-09-27 13:11:35 prereg E013  <  4fcbbd4 13:17:57 code  <  pilotes 13:18:03–13:25:03  <  c4b3755 13:25:18 A1  <  42a1e69 13:25:42 controles  <  runs officiels (1er dossier ne 13:25:42)
merge-base --is-ancestor a2f703f 51725c5 : OUI ; 997d87f 4fcbbd4 : OUI
reflog origin/exp/e013-insecte : @{1} = 997d87f (prereg pousse seul), @{0} = 3246ae8
git diff a2f703f..tip PREREGISTREMENT E008 : 19 insertions, 0 suppression ; E013 : 15 insertions, 0 suppression
hyperparametres.json E013 : un seul commit (c4b3755), absent du commit de code
```

### Axe 3 — Chiffres (`recalc_e013.py`, depuis les `eval.jsonl` bruts, avec la vérité recalculée pour L < 100)
```
I1-H1     T-LONG|1000     moy  99.30  ecart(ddof0)  0.60  [993/1000]   = par_graine publie OK   README 99,3 ± 0,6
I1-H2     T-LONG|1000     moy 100.00  ecart 0.00        [1000/1000]                       README 100
I2        T-LONG|16       moy  27.80  ecart(ddof0) 32.33 (ddof1 36.15)                    README 27,8 ± 32,3
I3-N1000  T-LONG|1000     moy  98.60  ecart(ddof0)  1.62                                  README 98,6 ± 1,6
I1-H1     ADV-ZEROS|1000  moy  45.54 ; |10 moy 91.68                                      README 45,5 / 91,7
I3-N100   T-ID|5 0.40 ; I2 T-ID|5 60.20 ; I3-N1000 ADV-CASCADE|1000 91.46                 README 0,4 / 60,2 / 91,5
I1-H1 ADV-ZEROS faux / faux-surs : 722 204                                                README 722 / 204
graines >= 90 % a 16 : I1-H1/H2/H4/H8 5/5 ; I2 0/5 ; I3 N10 0/5, N100 0/5, N1000 5/5, N10000 5/5
```
Aucun écart. L'écart-type E013 est un écart de **population** (ddof 0), celui d'E008 un écart d'échantillon (ddof 1) ; ni l'un ni l'autre n'est déclaré. C'est mineur, mais il faut le préciser.

### Axe 4 — Lecture honnête : la réserve

**Constat [VÉRIFIÉ].** ADV-CASCADE réutilise `_paire_toute_retenue` d'E008 (paires de chiffres de somme ≥ 9, ≥ 10 au rang 0). Seuls **20,1 % (L = 100) et 19,5 % (L = 1 000)** de ses rangs sont des rangs de **propagation** (somme = 9, la retenue ne fait que traverser). Les autres rangs **génèrent** une retenue, ce qui est plus facile pour un accumulateur mal réglé. La propagation pure n'y figure que par 2 items par L (99…9 + 1, 1 + 99…9).

Jeu R010 « propagation pure » (a de L chiffres, b = 10^L − a ; tous les rangs sauf le premier sont à somme 9) :
```
I1-H1..H8 (20 graines) + I1-H2-s11 : P16=100/100 P100=100/100 P1000=40/40   (toutes)
I3-N1000-s1 P16=100 P100=100 P1000=31/40
I3-N1000-s2 P16=98  P100=75  P1000=2/40
I3-N1000-s3 P16=100 P100=99  P1000=28/40
I3-N1000-s4 P16=100 P100=100 P1000=40/40
I3-N1000-s5 P16=81  P100=11  P1000=0/40
I3-N10000-s1..s5 : 100 % partout
```

**Ce que ça change.**
- Le **résultat phare I1** sort **renforcé** : il est exact aussi en propagation pure, à toutes les tailles et sur les 21 graines.
- En revanche, la phrase du README « [VÉRIFIÉ] Il suffit de **1 000 exemples uniques** (vus en boucle) pour la règle à 100 chiffres (5/5, ≥ 99,8 %) » est vraie sur T-LONG et fausse comme énoncé sur « la règle ». En propagation pure, la graine 5 est à 11 % à 100 chiffres et à **81 % à 16 chiffres**, donc sous le critère de réussite de 90 % ; la graine 2 est à 75 % à 100 chiffres. Mesuré sur ce jeu, N = 1 000 ferait **4/5** au critère « 16 chiffres » et **3/5** à 100 chiffres ≥ 90 %.
- Le seuil de P5 (« entre 100 et 1 000 ») dépend donc du jeu d'évaluation. [HYPOTHÈSE] Le vrai seuil pour la règle complète se situe entre 1 000 et 10 000.
- La marge négative de deux runs I3 que signale déjà le README (N = 1 000 s5 : −0,12) est cohérente avec ce constat : la graine s5 est justement celle qui casse.

**Correction attendue avant merge** (courte, sans nouveau calcul d'entraînement) :
1. Reformuler la lecture I3 : « 1 000 exemples suffisent pour T-LONG, pas pour la propagation pure (2/5 graines < 90 % à 100 chiffres) ; 10 000 suffisent pour les deux ».
2. Ajouter un jeu **ADV-PROPAG** (propagation pure) au TEST, en l'annonçant comme ajout post hoc du doublage, ou au moins citer ces chiffres R010.
3. Déclarer l'écart-type (population, n = 5).
4. Signaler dans les limites que l'ADV-CASCADE hérité d'E008 ne compte qu'environ 20 % de rangs de propagation.

Un re-doublage limité au diff de correction suffira ensuite.

Les autres affirmations [VÉRIFIÉ] sont soutenues par les données : I1 (toutes tailles, T-LONG et adverses), I2 0/5, la dérive de H = 1 (reproduite indépendamment sur les graines 1–3), les faux et sûrs, et la chronologie. La phrase « médiane 5–10 paires (0, 0) » est déjà étiquetée comme sonde non scriptée. La comparaison « 2 800 fois plus gros » est tempérée plus loin par le README lui-même (« mesure surtout la valeur de la structure donnée »). E008 : aucune réserve.

### Axe 5 — Sécurité
```
$ git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 3246ae8 -- research/   -> (rien, rc=1)
$ git ls-tree -r --name-only 3246ae8 | grep -E '(^|/)\.env|raw\.jsonl$'   -> .env.example (preexistant sur main, hors diff)
diff : aucun fichier hors .py/.md/.json/.csv/.txt/.gitignore ; aucun '/Users/' ni adresse
```

### Axe 6 — Hygiène git
```
3246ae8 1 | 42a1e69 1 | c4b3755 1 | 4fcbbd4 1 | 997d87f 1 | af281f5 1 | f073298 1 | b7ecc54 1 | 51725c5 1 | a2f703f 1
     10 Co-Authored-By: Malik & Claude      (aucun autre trailer)
perimetre : 16 research/experiments/E008-addition ; 15 research/experiments/E013-insecte
```

### Axe 7 — CLAUDE.md / rules
`git ls-tree -r --name-only 3246ae8 | grep -iE '(^|/)CLAUDE\.md$|\.claude/rules/'` → rien ; le diff ne touche ni CLAUDE.md ni rules.

## Angles morts du doublage (non testés)
- I2 n'a pas été réimplémenté : son résultat négatif n'est vérifié que par recomptage.
- Une seule graine neuve (11), et seulement pour H = 2.
- La propagation pure n'a pas été testée sur I2.
- Les pas intermédiaires n'ont pas été évalués hors checkpoint retenu.
- Le déterminisme GPU n'a pas été recontrôlé (l'auteur le déclare non reproductible au bit près).
