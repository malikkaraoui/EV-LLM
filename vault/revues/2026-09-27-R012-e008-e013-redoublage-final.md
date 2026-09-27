---
date: 2026-09-27
revue: R012
branche: exp/e013-insecte
tip: 044545ec9828c44984e5494969e1a38c454c990c
verdict: RESERVE
---

# R012 — Re-doublage final de exp/e013-insecte après le micro-correctif M0034 (tip 044545e)

Doubleur : F03 (Opus, indépendant de l'auteur de M0034). Le worktree détaché `.claude/worktrees/F03-R012` @ `044545e` est resté en lecture seule (`git status --short` → 0 ligne). Les rejeux ont été faits dans le scratchpad, sur une copie du code au tip (`git archive`) et sur les checkpoints `meilleur.safetensors` de l'auteur. Aucun appel API.

**Verdict : RÉSERVE — pas de merge. Loi des deux patchs déclenchée.**

Le périmètre est conforme : `git diff a749c29 044545e` = README E013 seul, 5 lignes. Tests E008 15/15 et E013 14/14 au tip. `adv_propag.py` rejoué : JSON et MD **identiques** au publié. Sécurité et hygiène OK.

**Axe 4 : troisième occurrence de la même classe de défaut** (affirmation sur le seuil d'exemples, non soutenue par les données). La phrase corrigée de la synthèse dit :

> README l. 194–196 : « ~10³ exemples suffisent pour T-LONG à 100 chiffres, mais **~10⁴ sont nécessaires pour la règle complète** en propagation pure »

- La première moitié est soutenue [VÉRIFIÉ] : I3 N = 1 000, T-LONG|100 = 99,92 %, 5/5, min 99,8.
- La seconde moitié est une affirmation de **nécessité** que les données ne portent pas :
  1. **Contre-exemple dans le tableau même** : I3 N = 1 000, graine s4 = **102/102/102** en ADV-PROPAG à 16, 100 et 1 000 chiffres (l. 100). Pour ce run, 10³ exemples ont suffi pour la règle complète. Ce que les données montrent : « 10³ ne suffisent **pas de façon fiable** (1/5 graine ≥ 90 % à 1 000 chiffres), 10⁴ suffisent (5/5) ». Elles ne montrent pas que ~10⁴ sont nécessaires.
  2. **Contradiction avec le statut déclaré du seuil dans le même README.** L. 176 : « [HYPOTHÈSE] le seuil pour la règle complète se situe entre 1 000 et 10 000 ; **non mesuré** ». L. 207–208 : « au-delà de 1 000, **au plus** 10 000 […] ne sont pas mesurés ». La synthèse transforme une borne **supérieure** hypothétique (≤ 10⁴ suffit) en borne **inférieure** non étiquetée (≈ 10⁴ nécessaire). Un seuil à 2 000 serait compatible avec toutes les données et contredirait « ~10⁴ nécessaires ».
- Origine [VÉRIFIÉ, mandat M0034 §2.1] : la formulation « ~10⁴ sont nécessaires pour la règle complète » était **prescrite par le mandat**. L'auteur l'a appliquée fidèlement. Le défaut vient donc de la chaîne orchestrateur → correctif, pas d'une négligence de l'auteur.

Après R010 (puce I3) et R011 (l. 195 « ~10³ exemples »), c'est la troisième fois que ce seuil est mal paraphrasé. Conformément au mandat, **je ne propose pas de troisième patch**. Recommandation explicite : **reconcevoir la section synthèse (« Lecture ») du README**. Voir « Recommandation » plus bas.

## Tableau des 7 axes

| # | axe | verdict | raison vérifiée |
|---|---|---|---|
| 1 | Rejeu | ✅ GO | diff a749c29..044545e = `README.md` E013 seul (3+/2−) ; diff 3246ae8..tip = 5 fichiers E013 ; diff des `resultats.json`, `PREREGISTREMENT.md`, `hyperparametres.json` et `summary.md` vide ; tests E008 15/15 et E013 14/14 OK au tip ; `adv_propag.py` rejoué : JSON et MD identiques au publié ; points de l'axe 4 de R010 : toujours traités (l. 58–60, 88–105, 169–176, 209–214) |
| 2 | Préenregistrement | ✅ GO | `git log --follow` inchangé depuis R010/R011 (préenregistrement puis A1 seulement) ; `--is-ancestor` a2f703f→51725c5 et 997d87f→4fcbbd4 : OUI ; `hyperparametres.json` : un seul commit (c4b3755) ; aucun sha256 d'attentes cité (sans objet) |
| 3 | Chiffres | ✅ GO | 7 cellules recalculées depuis les JSON publiés au tip, aucun écart (sortie ci-dessous) ; le diff ne modifie aucun chiffre, les recalculs de R011 restent valables |
| 4 | Lecture honnête | ⚠️ RÉSERVE | l. 195 « ~10⁴ sont **nécessaires** pour la règle complète » : contredite par I3-N1000 s4 = 102/102/102 (l. 100) et par le statut [HYPOTHÈSE] / « non mesuré » / « au plus 10 000 » du seuil (l. 176, 207–208) ; 3e occurrence de la classe « seuil d'exemples » → reconcevoir la synthèse |
| 5 | Sécurité dépôt public | ✅ GO | `git grep` des motifs au tip → rien (rc = 1) ; seul `.env.example` suivi (préexistant, hors diff) ; aucun `raw.jsonl` ; lignes ajoutées sans `/Users/` ni adresse (rc = 1) |
| 6 | Hygiène git | ✅ GO | 12/12 commits de la branche portent `Co-Authored-By: Malik & Claude`, aucun autre trailer ; périmètre depuis le merge-base 677b928 : 16 fichiers E008 et 18 fichiers E013, rien d'autre |
| 7 | CLAUDE.md / rules | ✅ GO | aucun CLAUDE.md imbriqué ni `.claude/rules/` au tip ni sur `origin/main` (rc = 1 et rc = 1) |

## Recommandation (au lieu d'un 3e patch)

Aujourd'hui, la section « Lecture » **redit** en prose des seuils quantitatifs déjà établis ailleurs : puce I3 l. 169–176, Limites l. 207–208, P5 l. 153–156. À chaque retouche, une copie diverge. C'est un défaut de conception, pas de formulation (R4 : un seul document fait foi par sujet ; ici, une seule phrase devrait faire foi par affirmation).

Piste [HYPOTHÈSE sur l'efficacité] :
- une **seule** source pour le seuil d'exemples : la puce I3, qui porte déjà les chiffres et l'étiquette [HYPOTHÈSE] ;
- la synthèse « Avec un rien faire beaucoup » ne cite **aucun** chiffre de seuil et renvoie à la puce I3 (« la partie apprise est petite ; voir I3 pour le nombre d'exemples ») ;
- puis une passe de relecture de **toute** la section « Lecture » : une phrase par affirmation, chacune étiquetée et liée à sa ligne de tableau.

La décision revient à l'orchestrateur. Il faudra un re-doublage du diff ensuite.

Si l'orchestrateur choisit malgré tout une retouche minimale, voici la formulation que les données soutiennent : « ~10³ exemples suffisent pour T-LONG à 100 chiffres, pas de façon fiable pour la règle complète en propagation pure (1/5 graine à 1 000 chiffres) ; 10⁴ suffisent pour les deux ».

## Preuves

### Gardes
```
$ git fetch origin ; git rev-parse origin/exp/e013-insecte
044545ec9828c44984e5494969e1a38c454c990c
$ git log $(git merge-base origin/main 044545e)..origin/main -- research/experiments/E008-addition research/experiments/E013-insecte
(vide)                                   # merge-base 677b9282ba8f
$ ls vault/revues | grep -i R012 ; git ls-tree -r --name-only origin/main vault/revues | grep R012
(vide)
```

### Axe 1 — Rejeu
```
$ git diff --stat a749c29 044545e
 research/experiments/E013-insecte/README.md | 5 +++--
 1 file changed, 3 insertions(+), 2 deletions(-)
$ git diff --name-only 3246ae8 044545e
research/experiments/E013-insecte/README.md
research/experiments/E013-insecte/adv_propag.py
research/experiments/E013-insecte/resultats/adv_propag.json
research/experiments/E013-insecte/resultats/adv_propag.md
research/experiments/E013-insecte/test_e013.py
$ git diff --stat 3246ae8 044545e -- '**/resultats.json' '**/PREREGISTREMENT.md' '**/hyperparametres.json' '**/summary.md'
(vide)
```
Tests (venv `ev-llm-e008`, `PYTHONDONTWRITEBYTECODE=1`, worktree détaché au tip) :
```
E008 : Ran 15 tests in 11.009s  OK
E013 : Ran 14 tests in 9.577s   OK
git status --short (worktree) -> 0
```
Rejeu de `adv_propag.py` (code du tip via `git archive`, checkpoints des runs I1/I3 copiés depuis le worktree de l'auteur, graine 0 exclue) :
```
| I3-N1000 | 95.9 ± 6.1 | 77.1 ± 31.7 | 52.9 ± 40.5 | 4/5 / 3/5 / 1/5 | s1 102/98/78; s2 97/79/7; s3 102/98/81; s4 102/102/102; s5 86/16/2 |
| I3-N10000 | 100.0 ± 0.0 | 100.0 ± 0.0 | 100.0 ± 0.0 | 5/5 / 5/5 / 5/5 | s1..s5 102/102/102 |
Part de rangs de propagation : ADV-CASCADE L=100 : 18.3 %, L=1000 : 17.8 % ; ADV-PROPAG : 99.7 %
JSON IDENTIQUE        (json.dumps sort_keys, publié vs rejoué)
MD IDENTIQUE          (diff -q)
```
Axes non touchés par le diff (2, 3, 5, 6, 7 pour les 11 premiers commits) : je reprends les preuves de R010 et R011. Ce qui est vérifiable au nouveau tip a été refait ci-dessous.

### Axe 2 — Préenregistrement
```
git log --follow PREREGISTREMENT.md @044545e
E008 : b7ecc54 2026-09-26 21:42:06 amendement A1 ; a2f703f 2026-09-26 21:06:52 preenregistrement
E013 : c4b3755 2026-09-27 13:25:18 amendement A1 ; 997d87f 2026-09-27 13:11:35 preenregistrement
merge-base --is-ancestor a2f703f 51725c5 : OUI ; 997d87f 4fcbbd4 : OUI
hyperparametres.json E013 : c4b3755 seul
git grep -niE 'sha-?256' 044545e -- E008 E013 -> rc=1
```

### Axe 3 — Chiffres (`recalc_r012.py`, depuis `resultats/resultats.json` et `resultats/adv_propag.json` au tip, ddof 0)
```
I3-N1000 T-LONG|100 moy 99.92 ddof0 0.10 min 99.80 >=90 5/5          README l.71/170 : 99,9 ± 0,1 ; « 5/5, ≥ 99,8 % »
ADV-PROPAG I3-N1000 L=16   moy 95.9 ± 6.1   >=90 4/5  [102, 97, 102, 102, 86]    README l.100 identique
ADV-PROPAG I3-N1000 L=100  moy 77.1 ± 31.7  >=90 3/5  [98, 79, 98, 102, 16]     README l.100 identique
ADV-PROPAG I3-N1000 L=1000 moy 52.9 ± 40.5  >=90 1/5  [78, 7, 81, 102, 2]       README l.100 identique
ADV-PROPAG I3-N10000 L=16/100/1000 moy 100.0 ± 0.0 >=90 5/5 [102 x5]            README l.101 identique
```
Aucun écart. On voit aussi la graine s4 de N = 1 000 à 102 aux trois tailles : c'est le contre-exemple de l'axe 4.

### Axe 4 — Lecture honnête : chasse aux paraphrases (faite par le doubleur, pas reprise de M0034)
```
$ grep -n -iE '10\^?3|10³|10\^?4|10⁴|1 ?000 ex|10 ?000 ex|mille|suffis|nécessai' README.md
154 | 169 | 170 | 173 | 174 | 183 | 194 | 195
$ grep (même motif) sur les autres .md d'E013 -> PREREGISTREMENT.md:130 « nécessaire, réduction des pas » (hors sujet)
```
| ligne | verdict |
|---|---|
| 154 | cohérente : critère **préenregistré** (T-LONG 16 chiffres, N = 100 : 0/5, N = 1 000 : 5/5), nuancé post hoc l. 155–156 |
| 169–170 | cohérentes : « 1 000 suffisent pour T-LONG à 100 chiffres (5/5, ≥ 99,8 %), pas pour la règle complète », recalculé ci-dessus |
| 173–174 | cohérentes : « 10 000 suffisent pour les deux » (5/5 partout) ; « 100 ne suffisent pas » (0/5) |
| 183 | hors sujet (« insuffisant » : affûtage des pointeurs d'I2) |
| 194–195, 1re moitié | cohérente : « ~10³ suffisent pour T-LONG à 100 chiffres » |
| **195, 2e moitié** | **⚠️ non soutenue** : « ~10⁴ sont nécessaires pour la règle complète ». Contre-exemple s4 = 102/102/102 à N = 1 000 ; contredit l. 176 ([HYPOTHÈSE], seuil entre 10³ et 10⁴, « non mesuré ») et l. 207–208 (« au plus 10 000 ») |
| hors motif, relues : 176, 207–208 | cohérentes (seuil déclaré hypothétique et non mesuré) |

Les autres affirmations [VÉRIFIÉ] de la section « Lecture » ne sont pas modifiées par le diff et ont été validées par R010/R011.

Remarque de forme (non bloquante) : la l. 196 dépasse 170 caractères, alors que le reste du fichier est coupé vers 100 colonnes.

### Axe 5 — Sécurité
```
$ git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 044545e -- research/   -> rc=1 (rien)
$ git ls-tree -r --name-only 044545e | grep -E '(^|/)\.env|raw\.jsonl$'   -> .env.example (préexistant, hors diff)
$ git diff a749c29 044545e | grep -E '^\+.*(/Users/|@domaine\.tld)'   -> rc=1
```

### Axe 6 — Hygiène git
```
044545e 1 | a749c29 1 | 3246ae8 1 | 42a1e69 1 | c4b3755 1 | 4fcbbd4 1 | 997d87f 1 | af281f5 1 | f073298 1 | b7ecc54 1 | 51725c5 1 | a2f703f 1   (autres Co-Authored-By : 0)
git diff --name-only 677b928 044545e : 16 research/experiments/E008-addition ; 18 research/experiments/E013-insecte
```

### Axe 7 — CLAUDE.md / rules
`git ls-tree -r --name-only 044545e | grep -iE '(^|/)CLAUDE\.md$|\.claude/rules/'` → rc = 1 ; même commande sur `origin/main` → rc = 1.

## Angles morts du re-doublage (non testés)
- Aucune inférence indépendante (numpy) refaite : le diff ne touche pas le code, et R010/R011 l'ont faite sur trois tirages.
- Les checkpoints rejoués sont ceux du disque de l'auteur, non suivis dans git. Ma copie contenait 44 dossiers : les 40 runs officiels plus 4 pilotes `I1-H4-s0-pilote-*` copiés par erreur (mon filtre `*-s0` ne les excluait pas). `adv_propag.py` ne lit que les runs officiels (JSON identique au publié), donc sans effet.
- ADV-PROPAG n'est toujours pas évalué sur I2 ; l'écart 18 / 20 % de rangs de propagation n'est toujours pas tranché (déclaré au README).
