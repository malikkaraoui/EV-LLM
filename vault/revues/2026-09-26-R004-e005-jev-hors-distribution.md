---
date: 2026-09-26
revue: R004
branche: exp/e005-jev-hors-distribution
tip: 08d80f72265d36a56ad5e916c4097426bc93cc05
verdict: CASSE
---

# R004 — Doublage indépendant de `exp/e005-jev-hors-distribution` (E005, M0009)

Doubleur : fenêtre F02, 2026-09-26, worktree détaché `.claude/worktrees/F02-R004` au tip `08d80f7` (rien n'y a été modifié). L'API Jev n'a **pas** été appelée.

**Verdict : CASSE, donc pas de merge.** La règle du mandat est appliquée strictement : à l'axe 3, « tout écart = ⛔ ». Le seul écart porte sur les **totaux de statuts HTTP** du README : la ligne 54 et la Lecture §6 annoncent 8 × 503 et 109 × 429, alors que les données en donnent 7 et 110. Le **résultat clé est confirmé** : 6 questions « faux et sûr », 9 évaluations, aucune attente contestée. La correction tient en 2 à 3 lignes du README. Elle produira un nouveau tip, qui devra être redoublé.

## Tableau des axes

| # | axe | verdict | raison vérifiée |
|---|---|---|---|
| 1 | Rejeu + exactitude des attentes | ✅ GO | 11 tests OK ; `verifie_logique.py` 6/6, mutation détectée (code 1) ; `aggregate.py` et `analyse.py` rejoués à l'identique (seul `run_id` change) ; les 6 attentes « faux et sûr » sont confirmées par des sources de référence, 0 contestée |
| 2 | Préenregistrement | ✅ GO | sha256 `5f37…2032` au commit 719d4c0 et au tip ; 719d4c0 est ancêtre des commits de code ; poussé à 16:16:49, avant le premier appel (16:16:55) ; `cases.json` n'a qu'un seul commit |
| 3 | Chiffres | ⛔ CASSÉ | tableau par famille, liste « faux et sûr », 19/28 et calibration recalculés : **identiques**. Mais le total de statuts HTTP est faux : **7 × 503 / 110 × 429**, et non 8 / 109 (README l. 54) |
| 4 | Lecture honnête | ⚠️ réserve | Lecture §6 [VÉRIFIÉ] : « Les 8 × 503 » est faux (7) ; « aucun fournisseur tenté » est vrai pour 107 des 110 réponses 429, pas pour les 3 autres. Toutes les autres affirmations [VÉRIFIÉ] contrôlées sont exactes, et les généralisations sont étiquetées [HYPOTHÈSE] |
| 5 | Sécurité dépôt public | ✅ GO | grep du mandat : vide ; aucun `.env` ni `raw.jsonl` suivi |
| 6 | Hygiène git | ✅ GO | 4/4 commits portent le trailer ; le diff reste sous `research/experiments/E005-jev-hors-distribution/` |
| 7 | CLAUDE.md / rules `paths:` | ✅ GO | aucun CLAUDE.md imbriqué ni aucune rule dans l'arbre du tip |

## Preuves

### Gardes
```
git rev-parse origin/exp/e005-jev-hors-distribution → 08d80f72265d36a56ad5e916c4097426bc93cc05   ✅
merge-base 7e953a9b… ; git log MB..origin/main -- E005 E001 → (vide)                             ✅
vault/revues/ : R001, R002 seulement                                                              ✅
```

### Axe 1 — rejeu
```
E001$ python3 -m unittest test_aggregate   → Ran 11 tests … OK
E005$ python3 verifie_logique.py           → F4-01…F5-01 : 6 × OK, code=0
copie scratchpad, F4-04 statut muté en coherent → "F4-04 … -> ECART", exit=1
python3 gen_cases.py ; shasum cases.json   → 5f3790074e08446e40860a02d56773ae58bfe92cb8e3a046d3345fb3089d2032 (arbre resté propre)
aggregate.py --out-root <scratch> results/2026-*  → summary.json/.md identiques au committé, à part run_id (163939 contre 162249)
analyse.py --out <scratch>/analyse.md      → ANALYSE_MD_IDENTIQUE, ANALYSE_JSON_IDENTIQUE
```

### Axe 1 — exactitude des attentes grammaticales (bloquant)
Source primaire : Académie française, [Questions de langue](https://www.academie-francaise.fr/questions-de-langue), texte extrait par `curl` et cité mot pour mot.

| cas | attente | verdict | source |
|---|---|---|---|
| F1-04 « Elles se sont lavées les mains » | fausse | **non contestée** [VÉRIFIÉ] | AF, *Pronominaux* : « Si le complément d'objet direct est placé après le participe […] le participe ne varie pas : Elles se sont lavé les mains » |
| F1-05 « Ils se sont parlés » | fausse | **non contestée** [VÉRIFIÉ] | AF : « Elles se sont parlé (parler n'introduit pas un complément d'objet direct mais un complément d'objet indirect…) » |
| F1-08 « Les robes qu'elle a faites faire » | fausse | **non contestée** [VÉRIFIÉ] | AF, *Participe passé* : « le participe passé fait suivi d'un infinitif est quant à lui toujours invariable » |
| F3-02 « Ci-jointe la facture demandée. » | fausse | **non contestée** [VÉRIFIÉ] | voir ci-dessous |
| F4-01 `statut` | contradiction | **exacte** [VÉRIFIÉ] | recalcul à la main : E>A, A>C (fait redondant) → E>C ; C>D → E>D ; incompatible(D,E) + R2 → violation. La règle 3 ne se déclenche pas (aucun bleu) |
| F4-04 `a_sup_f` | true | **exacte** [VÉRIFIÉ] | A>B, B>C → A>C (1) ; C>D → A>D (2) ; D>E → A>E (3) ; E>F → A>F (4) ; incompatible(A,F) + R2 → contradiction, donc `statut` = contradiction est aussi exact |

**F3-02, le cas soupçonné par l'orchestrateur, est examiné en détail.**
- AF, *Ci-annexé, ci-inclus, ci-joint*, §2 : « elles demeurent invariables lorsqu'elles ont une valeur nettement adverbiale […] ce qui est le cas notamment lorsqu'elles sont placées : en tête d'une phrase sans verbe, devant un groupe nominal (**avec ou sans déterminant**) : […] Ci-joint l'expédition du jugement ; Ci-joint les deux quittances exigées. » La latitude du §3 (« l'usage n'est pas fixé ») concerne **seulement** le corps de la phrase, pas la tête.
- OQLF, [BDL « Emploi de ci-joint… »](https://vitrinelinguistique.oqlf.gouv.qc.ca/21484/la-grammaire/le-verbe/accord-du-participe-passe/sans-auxiliaire/emploi-de-ci-joint-ci-inclus-et-ci-annexe-comme-adjectifs-et-adverbes) : au début d'une phrase, ces locutions « sont adverbiales, donc invariables ». La page ne mentionne aucune tolérance.
- Grevisse, cité de seconde main sur le [forum etudes-litteraires](https://www.etudes-litteraires.com/forum/discussion/5507/accord-de-ci-joint) : « En tête d'une phrase averbale : invariabilité ». [HYPOTHÈSE] Les exemples littéraires d'accord (Stendhal, Hugo, Musset) relèvent du corps de la phrase ; je n'ai pas eu accès au texte du *Bon usage* lui-même.
- Conclusion [VÉRIFIÉ] : aucune source reconnue consultée n'admet l'accord en tête de phrase sans verbe. L'attente « fausse » tient, et **le soupçon n'est pas confirmé**.

Liste finale des « faux et sûr » non contestés : **6 questions sur 6** (F1-04, F1-05, F1-08, F3-02, F4-01 `statut`, F4-04 `a_sup_f`), 9 évaluations, soit ≥ 1. Remarque annexe : F1-09 « laissé partir » invariable est bien admis par l'AF (« D'après les Rectifications de l'orthographe de 1990, le participe laissé peut se comporter de même : […] Je les ai laissé partir »).

### Axe 2 — préenregistrement
```
git log --follow -- cases.json  → 719d4c0 2026-09-26T16:16:47+02:00 (commit unique)
git merge-base --is-ancestor 719d4c0 2585f0e → vrai
git diff --quiet 719d4c0 08d80f7 -- cases.json → inchangé
git show 719d4c0:…/cases.json | shasum -a 256 → 5f3790074e08446e40860a02d56773ae58bfe92cb8e3a046d3345fb3089d2032 (= valeur citée)
reflog origin/exp/e005… : 719d4c0 @ 2026-09-26 16:16:49 +0200 update by push
premier appel : raw.public.jsonl lancement 1, ligne 1, ts 16:16:55
```

### Axe 3 — recalcul indépendant (script `recalc.py` du scratchpad, sans `analyse.py`)
```
appels 151 {200: 34, 503: 7, 429: 110}          ← README l.54 : « 34 × 200, 8 × 503, 109 × 429 »  ⛔
F1 questions 10 eval 11 conf 6 fs 4             = README
F2 questions 8 eval 8 conf 8 fs 0               = README
F3 questions 6 eval 6 conf 4 fs 1               = README
F4-4pas questions 4 eval 6 conf 2 fs 2          = README
F4-dist questions 6 eval 8 conf 5 fs 2          = README
F5 questions 3 eval 3 conf 3 fs 0               = README
total eval 42 conf 28 fs 9                      = README
questions fs distinctes : F1-04, F1-05, F1-08, F3-02, F4-01/statut, F4-04/a_sup_f   = README
P>=0.8 conformes [19, 28]                       = README
calibration boolean : 0.0 [7,2,5] 0.2 [2,0,2] 0.4 [4,3,4] 0.6 [5,3,3] 0.8 [17,12,12] = README
```
Statuts par lancement, recomptés dans chaque `raw.public.jsonl` : {9,1,22}, {6,1,16}, {0,0,32}, {8,2,10}, {4,2,9}, {7,1,21} (200, 503, 429). Ils sont **identiques au tableau par lancement du README**, dont la somme donne 7 × 503 et 110 × 429. L'erreur se trouve donc seulement dans la ligne de total (l. 54) et dans la Lecture §6 (l. 120). Le rapport d'auteur M0009 reprend le même total faux.

### Axe 4 — lecture
- [VÉRIFIÉ] conformes au recalcul : 13/13 phrases justes conformes ; 6/13 phrases fausses conformes, et les 7 non conformes sont toutes jugées « correctes » ; 7/7 `statut` valent `coherent` ; `confidence` F4-01 0.82/0.84 et F4-04 0.36/0.33 ; `e_sup_d` 0.56–0.95 ; F5-01 0.98 ; tranche 0.4–0.6 : 4/6 ; les 503 viennent tous de `digitalocean` (7/7).
- ⚠️ Lecture §6 : « Les 8 × 503 » (il y en a 7) ; « aucun fournisseur tenté » est vrai pour 107 des 110 réponses 429 (`totalProviderAttemptCount` 0), mais 3 réponses 429 ont 1 tentative `digitalocean` (F2-06, F2-07, F3-06).
- Portée : les généralisations (« plausibilité de surface », calibration) sont étiquetées [HYPOTHÈSE], et les Limites disent « aucune conclusion générale ». Le titre « Jev répond "coherent" partout » repose sur 7 réponses et 5 cas ; il est borné par son [VÉRIFIÉ]. Ce n'est pas bloquant.

### Axe 5 — sécurité
```
git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 08d80f7 -- research/ → (vide), code 1
git ls-tree -r --name-only 08d80f7 | grep -E '(^|/)\.env$|(^|/)raw\.jsonl$' → (vide), code 1
```
Information : README l. 35 cite le chemin local `/Users/malik/Documents/EV-LLM/.env` (commande de rejeu). Ce n'est pas un secret, et l'identifiant apparaît déjà dans l'URL du dépôt.

### Axe 6 — hygiène
```
git log origin/main..08d80f7 → 4 commits (08d80f7, 6ddaab9, 2585f0e, 719d4c0), chacun avec la ligne exacte « Co-Authored-By: Malik & Claude »
git diff --name-only MB 08d80f7 → 29 fichiers, tous sous research/experiments/E005-jev-hors-distribution/
```

### Axe 7
`git ls-tree -r --name-only 08d80f7 | grep -E '(^|/)CLAUDE\.md$|\.claude/rules/'` → vide. Aucune règle concernée.

## Pour repasser en GO (proposition, à la charge de l'auteur)
1. README l. 54 : « 8 × 503, 109 × 429 » → « 7 × 503, 110 × 429 ».
2. README l. 120 : « Les 8 × 503 » → « Les 7 × 503 » ; « aucun fournisseur tenté » → « aucun fournisseur tenté dans 107 cas sur 110 ».
3. Nouveau tip, puis nouveau doublage : les 6 autres axes ont été vérifiés et pourront être rejoués rapidement.
