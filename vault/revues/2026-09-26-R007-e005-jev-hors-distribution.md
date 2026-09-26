---
date: 2026-09-26
revue: R007
branche: exp/e005-jev-hors-distribution
tip: 15487b062d8e9a319c8ee945c0e2c8a3399aea22
verdict: GO
---

# R007 — Re-doublage de `exp/e005-jev-hors-distribution` (E005, M0009 + correctif M0013)

Doubleur : fenêtre F01, 2026-09-26, worktree détaché `.claude/worktrees/F01-R007` au tip `15487b0` (rien n'y a été modifié, `git status` vide après les tests). L'API Jev n'a **pas** été appelée ; `.env` n'a pas été ouvert.

**Verdict : GO.** Le correctif M0013 (`08d80f7..15487b0`) ne touche que le README. Tous les totaux du README corrigé concordent avec mon recomptage indépendant des 6 `raw.public.jsonl`. Le défaut CASSÉ de R004 (8 × 503 / 109 × 429) est résorbé.

## Tableau des axes

| # | axe | verdict | raison vérifiée |
|---|---|---|---|
| 1 | Rejeu (re-doublage en chaîne) | ✅ GO | diff `08d80f7..15487b0` = README seul ; `cases.json` inchangé (diff 0 ligne) ; 11 tests `test_aggregate` OK ; `verifie_logique.py` 6/6 OK, code 0 ; **tous** les totaux du README recomptés = données |
| 2 | Préenregistrement | ✅ GO | sha256 `5f37…2032` identique à 719d4c0 et au tip ; `cases.json` n'a qu'un seul commit (719d4c0), ancêtre des 4 commits suivants ; inchangé jusqu'au tip ; 1er appel 16:16:55, après le commit (16:16:47). L'heure du push (16:16:49) est reprise de R004 |
| 3 | Chiffres | ✅ GO | recalcul indépendant (`recompte_r007.py`) : statuts par lancement et totaux (151 / 34 / 7 / 110), 107/110, tableau par famille, 6 « faux et sûr » / 9 évaluations, 19/28, calibration, couverture 37/38 : **tous identiques** au README |
| 4 | Lecture honnête | ✅ GO | les lignes modifiées (l. 54, 56, 122, 128) sont exactes ; les autres [VÉRIFIÉ], inchangés depuis R004, sont recontrôlés par mon script (13/13, 6/13, 7 jugées correctes, 7/7 `coherent`, `confidence`, 19/28) ; les généralisations restent [HYPOTHÈSE] ; « aucune conclusion générale » est dit en Limites |
| 5 | Sécurité dépôt public | ✅ GO | grep du mandat au tip : vide (code 1) ; aucun `.env` ni `raw.jsonl` suivi (code 1) |
| 6 | Hygiène git | ✅ GO | 5/5 commits portent la ligne exacte `Co-Authored-By: Malik & Claude` ; diff depuis le merge-base : 28 fichiers ajoutés, tous sous `research/experiments/E005-jev-hors-distribution/` |
| 7 | CLAUDE.md / rules `paths:` | ✅ GO | aucun `CLAUDE.md` imbriqué ni aucune `.claude/rules/` dans l'arbre du tip |

## Preuves

### Gardes
```
git rev-parse origin/exp/e005-jev-hors-distribution → 15487b062d8e9a319c8ee945c0e2c8a3399aea22   ✅
MB = 7e953a9b0197abfe0dd60137343da9a6e308c6c3 ; git log MB..origin/main -- E005 E001 → (vide)     ✅
ls vault/revues | grep R007 → (vide)                                                               ✅
```

### Axe 1 — rejeu
```
git diff --name-only 08d80f7 15487b0 → research/experiments/E005-jev-hors-distribution/README.md
git diff --stat 08d80f7 15487b0      → README.md | 8 +++++---  (1 file, 5+, 3-)
git diff 08d80f7 15487b0 -- cases.json | wc -l → 0
E001$ python3 -m unittest test_aggregate → Ran 11 tests in 0.013s / OK
E005$ python3 verifie_logique.py         → F4-01, F4-02, F4-03, F4-04, F4-05, F5-01 : 6 × OK, code=0
```
Attentes grammaticales : confirmées par R004 (sources AF / OQLF). `cases.json` n'a pas changé, donc ce contrôle reste valable sans refaire la recherche.

### Axes 1 et 3 — recomptage indépendant (`scratchpad/recompte_r007.py`, stdlib, lit seulement `cases.json` et `results/*/raw.public.jsonl` ; il vérifie aussi que `state`/`questions` de chaque appel 200 = corpus)
```
2026-09-26T161655+0200 appels 32 {200: 9, 429: 22, 503: 1}
2026-09-26T161811+0200 appels 23 {200: 6, 429: 16, 503: 1}
2026-09-26T161845+0200 appels 32 {429: 32}
2026-09-26T161956+0200 appels 20 {200: 8, 429: 10, 503: 2}
2026-09-26T162058+0200 appels 15 {200: 4, 429: 9, 503: 2}
2026-09-26T162237+0200 appels 29 {200: 7, 429: 21, 503: 1}
TOTAL appels 151 {200: 34, 429: 110, 503: 7}
429 totalProviderAttemptCount=0 : 107 / 110 ; autres : [('F2-06', 1, ['digitalocean']), ('F2-07', 1, ['digitalocean']), ('F3-06', 1, ['digitalocean'])]
503 fournisseurs tentes : {'digitalocean': 7}
F1 questions 10 eval 11 conf 6 fs 4
F2 questions 8 eval 8 conf 8 fs 0
F3 questions 6 eval 6 conf 4 fs 1
F4-4pas questions 4 eval 6 conf 2 fs 2
F4-dist questions 6 eval 8 conf 5 fs 2
F5 questions 3 eval 3 conf 3 fs 0
total questions 37 eval 42 conf 28 fs 9
fs distinctes [('F1-04', 'correcte'), ('F1-05', 'correcte'), ('F1-08', 'correcte'), ('F3-02', 'correcte'), ('F4-01', 'statut'), ('F4-04', 'a_sup_f')]
P>=0.8 conformes [19, 28]
calibration boolean [n, att_true, conf]: {'0.0': [7, 2, 5], '0.2': [2, 0, 2], '0.4': [4, 3, 4], '0.6': [5, 3, 3], '0.8': [17, 12, 12]} n_bool 35
cas 32 questions 38 >=1: 37 >=2: [F1-04/correcte, F4-01/e_sup_d, F4-01/statut, F4-04/a_sup_f, F4-04/statut] 0: [F5-03/correcte]
F4 statut: F4-01 coherent 0.88 (conf 0.82) ; F4-02 0.98 ; F4-03 0.76 ; F4-04 0.57 (0.36) ; F4-05 0.92 ; F4-01 0.89 (0.84) ; F4-04 0.55 (0.33)
phrases justes conf 13 / 13 ; fausses conf 6 / 13 ; fausses non conf jugees correctes 7
```
Confrontation, total par total, au README du tip :

| README | écrit | recompté | |
|---|---|---|---|
| l. 15 / 60 | 32 cas, 38 questions ; 37 ≥ 1, 5 à 2 réponses, F5-03 à 0 | idem | ✅ |
| l. 47-52 | tableau par lancement | idem, ligne par ligne | ✅ |
| l. 54 | 151 appels, 34 × 200, 7 × 503, 110 × 429 | 151, 34, 7, 110 | ✅ |
| l. 56 | 107 des 110 à `totalProviderAttemptCount` = 0 | 107/110 | ✅ |
| l. 64-72 | tableau par famille, total 37 / 42 / 28 / 9 | idem | ✅ |
| l. 76-85 | 6 questions « faux et sûr », 9 évaluations | idem | ✅ |
| l. 89-99 | calibration (35 boolean) ; 19/28 | idem | ✅ |
| l. 108 | 13/13 ; 6/13 ; 7 jugées correctes | idem | ✅ |
| l. 114 | 7 `statut` = `coherent` | 7/7 | ✅ |
| l. 122 | 0 à 9 réponses 200 par lancement ; 107/110 ; F2-06, F2-07, F3-06 ; 7 × 503 `digitalocean` | 0–9 ; idem | ✅ |
| l. 128 | `totalProviderAttemptCount: 0` pour 107 des 110 | idem | ✅ |

Règle de lecture appliquée dans mon script : celle du README, l. 27. Seuil de conformité boolean : P > 0.5. Aucune P ne vaut exactement 0.5, donc aucun cas ambigu.

### Axe 2 — préenregistrement
```
git show 15487b0:…/cases.json | shasum -a 256 → 5f3790074e08446e40860a02d56773ae58bfe92cb8e3a046d3345fb3089d2032
git show 719d4c0:…/cases.json | shasum -a 256 → 5f3790074e08446e40860a02d56773ae58bfe92cb8e3a046d3345fb3089d2032 (= valeur citée l. 15)
git log --follow -- cases.json → 719d4c0 2026-09-26T16:16:47+02:00 (commit unique)
git merge-base --is-ancestor 719d4c0 {2585f0e, 6ddaab9, 08d80f7, 15487b0} → vrai ×4
git diff --quiet 719d4c0 15487b0 -- cases.json → inchangé
raw.public.jsonl lancement 1, ligne 1 → ts 2026-09-26T16:16:55+02:00
```

### Axe 5 — sécurité
```
git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 15487b0 -- research/ → (vide), code 1
git ls-tree -r --name-only 15487b0 | grep -E '(^|/)\.env$|(^|/)raw\.jsonl$' → (vide), code 1
```

### Axe 6 — hygiène
```
git log origin/main..15487b0 → 15487b0, 08d80f7, 6ddaab9, 2585f0e, 719d4c0 (5 commits)
grep -cx 'Co-Authored-By: Malik & Claude' → 5
git diff --name-status 7e953a9 15487b0 → 28 × A, 0 hors research/experiments/E005-jev-hors-distribution/
```
Information : R004 comptait « 29 fichiers » au tip `08d80f7`. Je recompte 28 à `08d80f7` comme à `15487b0`. L'écart vient du rapport R004, pas de la branche. Il n'a aucun effet sur le verdict.

### Axe 7
`git ls-tree -r --name-only 15487b0 | grep -E '(^|/)CLAUDE\.md$|\.claude/rules/'` → vide, code 1.

### Tests sur le résultat du merge (scratch `F01-merge`, `a70b907` = merge --no-ff de 15487b0 sur cd4e9bc)
```
E001$ python3 -m unittest test_aggregate → Ran 11 tests in 0.014s / OK
E005$ python3 verifie_logique.py         → 6 × OK, code=0
recompte_r007.py → TOTAL 151 {200: 34, 429: 110, 503: 7} ; 37/42/28/9 ; 6 fs distinctes (identique)
```

## Portée
- [VÉRIFIÉ] Ce doublage certifie la conformité du README aux données publiées et l'intégrité du préenregistrement. Il ne certifie pas une propriété générale de Jev.
- [HYPOTHÈSE] 3 des 6 « faux et sûr » reposent sur un seul appel. La réplication proposée par le README (Prochaine étape §1) reste nécessaire avant d'en tirer une conclusion.
