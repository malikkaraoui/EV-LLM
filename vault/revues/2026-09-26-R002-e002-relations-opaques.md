---
date: 2026-09-26
revue: R002
branche: exp/e002-relations-opaques
tip: 1cb586bd6976e17dd1169a7f3b192ad5e4c04c9e
verdict: GO
---

# R002 — Doublage indépendant de `exp/e002-relations-opaques`

Doubleur : fenêtre F02 (mandat R002), indépendante de l'auteur (F03, M0005). Worktree détaché en lecture seule au tip `1cb586b`, rejeux dans une copie `git archive` hors dépôt. Rapport d'auteur lu en entier : `vault/echanges/archive/2026-09-26-F03-M0005-e002-relations-opaques.md`.

## Gardes [VÉRIFIÉ]

- `git rev-parse origin/exp/e002-relations-opaques` → `1cb586bd6976e17dd1169a7f3b192ad5e4c04c9e` (= tip attendu).
- `git log $(merge-base = 7c453b1)..origin/main -- research/experiments/E002-relations-opaques` → vide.
- `vault/revues/` ne contenait que `.gitkeep` : pas de R002 antérieur.

## Verdicts par axe

| # | axe | verdict | raison vérifiée |
|---|---|---|---|
| 1 | Rejeu | ✅ GO | 22 tests OK ; `evaluer.py --graines 1-20` rejoué hors dépôt → `resultats.json` **identique octet à octet** (sha256 `778f9c24…6101ad` des deux côtés) ; `summary.md` identique hors ligne de titre (horodatage) ; écart R ≤ 0 du plafond déclaré (README, commit, rapport) |
| 2 | Préenregistrement | ✅ GO | `d8ef3a1` (prereg) ancêtre de `340f99d` (code) ; `git log --follow` : un seul commit touche `PREREGISTREMENT.md` ; `git diff d8ef3a1 tip -- PREREGISTREMENT.md` = 0 ligne. Aucun fichier d'attentes avec sha cité (N/A) |
| 3 | Chiffres | ✅ GO | 17 colonnes × 3 étalons recalculées depuis `resultats.json` : toutes égales au tableau ; 45/161 propriétés fausses dont 29 compositions recalculées contre la vérité du générateur ; 60–80 % de non-transitives recalculé |
| 4 | Lecture honnête | ✅ GO | chaque [VÉRIFIÉ] de la Lecture est soutenu (détail ci-dessous) ; seule inférence non triviale (« difficulté du banc ») étiquetée [HYPOTHÈSE] ; aucune conclusion générale. Deux remarques non bloquantes |
| 5 | Sécurité dépôt public | ✅ GO | `git grep` des motifs sensibles sur `research/` au tip → aucune ligne (rc=1) ; aucun `.env` ni `raw.jsonl` suivi (rc=1) |
| 6 | Hygiène git | ✅ GO | 3 commits, chacun porte exactement `Co-Authored-By: Malik & Claude` ; périmètre = 13 fichiers, tous sous `research/experiments/E002-relations-opaques/` |
| 7 | CLAUDE.md / rules `paths:` | ✅ GO | `git ls-tree -r` au tip : aucun `CLAUDE.md` ni `.claude/rules/` dans le dépôt → rien à mettre à jour |

**Verdict global : GO** (7/7 ✅).

## Preuves

### Axe 1 — rejeu

```
$ python3 -m unittest discover        # dans le worktree détaché
Ran 22 tests in 0.276s
OK

$ python3 evaluer.py --graines 1-20 --sortie <scratchpad>/sortie   # copie git archive du tip
$ cmp <scratchpad>/sortie/2026-09-26T161458+0200/resultats.json results/2026-09-26T160728+0200/resultats.json && echo OCTET_IDENTIQUE
OCTET_IDENTIQUE
778f9c24aa049b58a85f41092e7d44b7b46e8ccaaaa3f1eedbd66b9d9a6101ad  (rejeu)
778f9c24aa049b58a85f41092e7d44b7b46e8ccaaaa3f1eedbd66b9d9a6101ad  (committé)
$ diff <(tail -n +2 rejeu/summary.md) <(tail -n +2 committé/summary.md) && echo SUMMARY_IDENTIQUE_HORS_TITRE
SUMMARY_IDENTIQUE_HORS_TITRE
```

Diagnostic hors protocole rejoué : moyennes `-0.003 | 0.016 | -0.014 | -0.016` (identiques au README). Contrôle plus fort que celui de l'auteur : sans bruit, le plafond a R > 0 sur **20/20** mondes **et 0 `DÉDUIT` faux en vérité dans chacun des 20 mondes** — toutes ses erreurs avec bruit viennent donc bien de prémisses bruitées [VÉRIFIÉ].

L'écart au préenregistrement (R_plafond ≤ 0 sur 12/20 mondes → R̂ indéfini → critère ACQUÉRIR inopérant) est déclaré dans le README (§ Lecture, 2e point, en gras), dans le message de `1cb586b` et dans le rapport M0005, sans modification du préenregistrement. C'est un résultat honnêtement rapporté.

### Axe 2 — préenregistrement

```
1cb586b 2026-09-26 16:08:52 +0200 feat(e002): execution 20 mondes x 3 etalons + README
340f99d 2026-09-26 16:07:35 +0200 feat(e002): banc relations opaques -- ...
d8ef3a1 2026-09-26 16:00:06 +0200 docs(e002): preregistrement
$ git merge-base --is-ancestor d8ef3a1 340f99d && echo PREREG_ANCETRE_CODE
PREREG_ANCETRE_CODE
$ git log --follow --format='%h %s' 1cb586b -- .../PREREGISTREMENT.md
d8ef3a1 docs(e002): preregistrement
$ git diff d8ef3a1 1cb586b -- .../PREREGISTREMENT.md | wc -l
0
```

Remarque [HYPOTHÈSE] : git prouve l'ordre des **commits**, pas l'ordre d'**écriture** (7 min entre prereg et code de 13 fichiers). De plus, l'horodatage de l'exécution officielle (`16:07:28`) précède de 7 s le commit du code (`16:07:35`). Le rejeu octet-identique depuis le code committé montre que les résultats publiés correspondent bien à ce code [VÉRIFIÉ].

### Axe 3 — chiffres (script ad hoc sur `resultats.json`)

```
aleatoire          exact=0.328 dedinf=0.767 dedFauxV=9.1 precC=0.070 rapC=0.282 excl=1.05 req=0.0 bitsExp=909 eco=-33.3 R=-0.037 R>0=0/20 rev=44/275 sur=1105/1385 ECHEC 0/4
decouvreur_naif    exact=0.777 dedinf=0.258 dedFauxV=8.3 precC=0.383(n=15) rapC=0.889(n=9) excl=3.00 req=62.0 bitsExp=1487 eco=-21.7 R=-0.014 R>0=5/20 rev=177/222 sur=284/1438 ECHEC 0/4
oracle_proprietes  exact=1.000 dedinf=0.000 dedFauxV=4.7 precC=1.000 rapC=1.000 excl=3.00 req=0.0 bitsExp=909 eco=-2.8 R=-0.003 R>0=8/20 rev=275/275 sur=0/1385 ECHEC 0/4
R_plafond<=0: 12   R_chapeau None (plafond): 12   (découvreur): 12
decouvreur : acceptees=161 fausses=45 dont_compositions=29   (vérité = monde.regles_du_monde, graines régénérées)
non transitives par monde : [4 ×15, 3 ×5] → 60 % à 80 %
précision INDÉT : 0.505 / 0.916 / 1.000
```

Tous égaux au tableau du README. 1487/909 = 1.64 (« 1.6 fois plus ») ✔.

### Axe 4 — lecture honnête

| affirmation [VÉRIFIÉ] du README | contrôle |
|---|---|
| plafond R = −0.003, positif 8/20 | ✔ recalculé |
| erreurs du plafond = prémisses bruitées | ✔ renforcé : 0 `DÉDUIT` faux sans bruit sur 20/20 |
| R̂ indéfini 12/20 | ✔ recalculé |
| écart plafond/découvreur (1.000/0.777 ; 0/25.8 % ; 1.000/0.383 ; ×1.6) | ✔ |
| 45/161 propriétés fausses, 29 compositions | ✔ recalculé contre la vérité |
| découvreur R sans bruit −0.016 | ✔ rejoué |
| Test 1 A/B : 3/3 dans les 20 mondes, hasard 1.05 | ✔ (moyenne 3.00 = 3/3 partout) |
| découvreur sans mémoire, testé | ✔ `tests/test_e002.py:262` (« même monde, même résultat, quel que soit l'historique ») |

Remarques non bloquantes :
1. **Dénominateur non déclaré.** Le tableau annonce « moyennes sur 20 mondes », mais la précision et le rappel de CONTRADICTION du découvreur sont des moyennes sur les mondes où ils sont définis : **15** et **9** mondes (`evaluer.py:172` écarte les `None`). Les valeurs poolées (0.340 et 0.941 sur 17 contradictions attendues au total) restent proches : l'écart ne change aucune lecture. À préciser dans un prochain README.
2. **Trou de test mineur.** Mutation de `est_symetrique` (ignorer les paires issues de l'entité 0) : la suite reste verte. Le mutant produit un `resultats.json` identique octet à octet sur les 20 mondes : il est sans effet sur les résultats publiés. Une mutation témoin de signe de R, elle, fait échouer la suite (`FAILED (failures=1)`).

### Axe 5 — sécurité

```
$ git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 1cb586b -- research/
rc=1   (aucune ligne)
$ git ls-tree -r --name-only 1cb586b | grep -E '(^|/)\.env$|(^|/)raw\.jsonl$'
rc=1   (aucun fichier)
```

### Axe 6 — hygiène git

```
1cb586b 1   340f99d 1   d8ef3a1 1     (nombre de lignes « Co-Authored-By: Malik & Claude »)
$ git diff --name-only 7c453b1 1cb586b
research/experiments/E002-relations-opaques/{PREREGISTREMENT.md, README.md, diagnostic_sans_bruit.py, etalons.py,
evaluer.py, interface.py, monde.py, oracle.py, raisonneur.py, results/2026-09-26T160728+0200/{resultats.json,summary.md},
tests/__init__.py, tests/test_e002.py}
```

### Axe 7

`git ls-tree -r --name-only 1cb586b | grep -iE '(^|/)CLAUDE\.md$|\.claude/rules/'` → vide.

## Portée

[VÉRIFIÉ] ce doublage établit la reproductibilité, l'intégrité du préenregistrement et l'exactitude des chiffres publiés. Il ne valide pas le banc comme mesure d'ACQUÉRIR : l'auteur a lui-même montré que le critère n'est pas mesurable en l'état (R̂ indéfini sur 12/20), et la décision E002-bis (options a–d du rapport M0005) reste à l'orchestrateur.
