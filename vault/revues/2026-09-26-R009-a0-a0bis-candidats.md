---
date: 2026-09-26
revue: R009
branche: exp/a0bis-candidat
tip: 1be4654fadc3eafd1e48fb05aecc39991f7948ec
verdict: RESERVE
---

# R009 — Doublage de exp/a0bis-candidat (A0 M0014 + A0-bis M0016)

Doubleur : F03 (Opus, indépendant des auteurs F05/M0014 et F04/M0016). Worktree détaché en lecture seule `.claude/worktrees/F03-R009` @ `1be4654`, rien modifié (`git status --porcelain` → 0 ligne). Rejeux écrits dans le scratchpad. Aucun appel API.

**Verdict global : RÉSERVE.** La mesure est juste : les deux exécutions officielles sont reproduites à l'octet près, et les deux verdicts ÉCHEC ACQUÉRIR (A0 1/4, A0-bis 0/4) sont recalculés indépendamment. Les chiffres et l'hygiène sont irréprochables (6 axes ✅). **La lecture de l'A0-bis (axe 4) doit être amendée sur un point** avant le merge : la conclusion « (c) le bruit MLE dégrade le résultat », étiquetée [VÉRIFIÉ], repose sur **un seul monde** (graine 19). Pas de merge.

## Tableau des axes

| # | axe | verdict | raison vérifiée (résumé) |
|---|---|---|---|
| 1 | Rejeu | ✅ GO | 16 tests A0 et 22 tests A0-bis OK. Les deux évaluateurs ont été rejoués sous `PYTHONHASHSEED=0` : `cmp` des deux `resultats.json` → identiques. ACQUÉRIR recalculé par un script indépendant : a0 1/4, a0bis 0/4, ÉCHEC, et aucun étalon ne réussit |
| 2 | Préenregistrement | ✅ GO | Chaque préenregistrement est committé seul (`c874e76`, `b67bcbd`), il est ancêtre du code (`c3591e2`, `71760c7`) et n'a jamais été modifié ensuite. Toutes les constantes préenregistrées sont identiques dans le code. Le seul paramètre non préenregistré (`ZERO_NUMERIQUE`) est sans effet. Le passage de mise au point n'entame pas la valeur de l'ÉCHEC (détail §2) |
| 3 | Chiffres | ✅ GO | 9 + 9 systèmes recalculés (M1, M3, M4, requêtes, exactitude, R, bits, séries par famille), plus les diagnostics internes (fautes attribuées, bruit appris, familles rangées et identifiées) : aucun écart |
| 4 | Lecture honnête | ⚠️ RÉSERVE | A0-bis : « (c) le bruit MLE dégrade le résultat » [VÉRIFIÉ] et « les compteurs d'A0 protègent mieux contre les cascades » reposent sur la seule graine 19. Hors graine 19, `a0bis` (−0.0074) fait **mieux** que `a0bis_sans_bruit_mle` (−0.0078). Or c'est sur cette lecture que repose le choix de base d'A0-ter. La lecture d'A0 est correcte |
| 5 | Sécurité dépôt public | ✅ GO | `git grep` des motifs sensibles → 0 résultat. Aucun `.env` ni `raw.jsonl` suivi. Seul `.env.example` est suivi : valeur vide, antérieur à la branche (`ad328dd`) |
| 6 | Hygiène git | ✅ GO | Trailer présent sur les 6 commits, sans autre trailer. Le diff depuis le merge-base `8a5b865` est limité à `research/candidats/A0/` et `research/candidats/A0bis/` |
| 7 | CLAUDE.md / rules `paths:` | ✅ GO | Aucun CLAUDE.md imbriqué ni `.claude/rules/`, ni au tip ni sur main |

## Gardes

```
$ git fetch origin ; git rev-parse origin/exp/a0bis-candidat
1be4654fadc3eafd1e48fb05aecc39991f7948ec
$ git log $(git merge-base origin/main 1be4654…)..origin/main -- research/candidats research/experiments/E002bis-mesure research/experiments/E002-relations-opaques
(vide)        # merge-base = 8a5b865a6d5de3b0af4bbb399f9ae94f351d17a0
$ ls vault/revues | grep R009 ; git ls-tree -r --name-only origin/main -- vault/revues | grep R009
(vide)
```

## Axe 1 — Rejeu [VÉRIFIÉ]

```
$ cd research/candidats/A0 && python3 -m unittest discover      → Ran 16 tests in 3.667s  OK
$ cd research/candidats/A0bis && python3 -m unittest discover   → Ran 22 tests in 8.645s  OK   (Python 3.9.6)
$ PYTHONHASHSEED=0 python3 evaluer_a0.py    --sortie <scratch>/a0      rc=0
$ PYTHONHASHSEED=0 python3 evaluer_a0bis.py --sortie <scratch>/a0bis   rc=0
$ cmp A0/results/2026-09-26T172136+0200/resultats.json    <scratch>/a0/…/resultats.json    → CMP_A0_IDENTIQUE
$ cmp A0bis/results/2026-09-26T174546+0200/resultats.json <scratch>/a0bis/…/resultats.json → CMP_A0BIS_IDENTIQUE
$ diff summary.md (×2) → seule la ligne 1 diffère (horodatage)
```

**Verdict ACQUÉRIR recalculé** par `recalc.py` (scratchpad), qui ne réutilise **aucun** code du dépôt. Définition relue dans `E002bis-mesure/PREREGISTREMENT.md` §4 : une famille accélère si `R̂_diff(5e) − R̂_diff(1er) ≥ 0.005` et si au moins 3 transitions sur 4 ont `Δ > 0`. Le système réussit s'il accélère dans au moins 3 familles sur 4. `R̂_diff` est recalculé comme `R − R_plafond` à graine égale ; écart maximal avec la valeur publiée : `0.0e+00`.

```
== A0 (results/2026-09-26T172136+0200)          plafond R>0 : 20/20
a0      ACQ=1/4 ECHEC  M1=-0.0110 M3=+0.0017 M4=2.00 req=0.0 exact=0.714 R=+0.0011
    fam 0: -0.0238 → -0.0138 → -0.0114 → -0.0106 → -0.0058 gain +0.0180 hausses 4/4 acc=True
    fam 1: -0.0031 → -0.0100 → -0.0207 → -0.0142 → -0.0132 gain -0.0101 hausses 2/4 acc=False
    fam 2: -0.0052 → -0.0042 → -0.0150 → -0.0095 → -0.0046 gain +0.0006 hausses 3/4 acc=False
    fam 3: -0.0079 → -0.0099 → -0.0188 → -0.0093 → -0.0095 gain -0.0015 hausses 1/4 acc=False
== A0bis (results/2026-09-26T174546+0200)       plafond R>0 : 20/20
a0bis   ACQ=0/4 ECHEC  M1=-0.0105 M3=+0.0021 M4=3.10 req=22.6 exact=0.829 R=+0.0017
    fam 0: -0.0076 → -0.0108 → -0.0091 → -0.0315 → -0.0028 gain +0.0048 hausses 2/4 acc=False
    fam 1: -0.0019 → -0.0018 → -0.0139 → +0.0002 → +0.0007 gain +0.0026 hausses 3/4 acc=False
    fam 2: -0.0006 → -0.0087 → -0.0258 → -0.0144 → -0.0004 gain +0.0001 hausses 2/4 acc=False
    fam 3: -0.0070 → -0.0004 → +0.0003 → -0.0687 → -0.0060 gain +0.0010 hausses 3/4 acc=False
contrôles (les deux exécutions) : aleatoire 1/4, oracle_proprietes 0/4, plafond 0/4, decouvreur_naif 0/4, a0_sans_memoire 1/4 → tous ÉCHEC
a0 (M0014) == a0 rejoué dans l'exécution A0-bis : True
```

## Axe 2 — Préenregistrement [VÉRIFIÉ sauf mention]

```
PREREGISTREMENT A0    : c874e76 17:13:35  (1 fichier, 164 lignes) — seul commit du fichier (git log --follow)
PREREGISTREMENT A0bis : b67bcbd 17:36:56  (1 fichier, 199 lignes) — seul commit du fichier
git merge-base --is-ancestor c874e76 c3591e2 → vrai ; b67bcbd 71760c7 → vrai
a0.py, a0bis.py, evaluer_a0bis.py, test_a0bis.py : un seul commit chacun (c3591e2 / 71760c7)
exécutions officielles : 17:21:36 > commit du code 17:21:31 (A0) ; 17:45:46 > 17:45:33 (A0-bis)
```
- **Fichiers d'attentes avec sha256** : sans objet. Ni l'un ni l'autre candidat n'a de corpus d'attentes figé ni de sha cité (`git grep sha256|attentes` hors `resultats.json` → 0 résultat). Les attentes figées sont les critères et les prédictions du §8, inclus dans le préenregistrement.
- **Résultats hors du dossier officiel** : l'arbre ne contient qu'un seul dossier `results/` par candidat (`git ls-tree`). Les worktrees d'auteur (`F04-M0016`, `F05-M0014`) ne contiennent eux aussi que le dossier officiel, et `git status --ignored` y est vide.

**Point à trancher : le passage de mise au point sur les graines 1–20** (entre `b67bcbd` et `71760c7`).
1. *Ce qui est vérifiable.* Toutes les constantes que le préenregistrement fixe se retrouvent à l'identique dans le code :

   | constante | valeur | paramètre du préenregistrement |
   |---|---|---|
   | `D_MAX` | 2 | distance de rangement |
   | `SEUIL_IDENTIFICATION` | 0.5 | seuil d'identification d'une famille |
   | `PI_BAS, PI_ECART` | 0.1, 0.8 | a priori `π(r, i)` |
   | `MLE_MIN` | 5 | nombre minimal de vérifications du MLE |
   | `MLE_BORNES` | (0.01, 0.5) | bornes du MLE |
   | `BUDGET` | 150 | requêtes par monde |
   | `DELTA_PAS, DELTA_OUBLI` | 0.5, 0.1 | pas des marges `δ` |
   | `KAPPA_PAS, KAPPA_MAX` | 1.1, 4.0 | pas et plafond de `κ` |
   | `A_PRIORI_BRUIT` | Beta(1, 9), Beta(1, 9), Beta(1, 1) | a priori du bruit (A0 §3.2) |

   Le passage de mise au point ne pouvait donc régler aucun de ces paramètres sans laisser d'écart visible.
2. *Le seul paramètre non préenregistré* est `ZERO_NUMERIQUE = 1e-9` : une VOI de cet ordre compte comme nulle. Je l'ai mis à 0 en le patchant en mémoire (`sensib.py`) :
   ```
   officiel            M1=-0.01050 ACQ=0/4
   ZERO_NUMERIQUE=0    M1=-0.01051 ACQ=0/4
   ```
   L'effet est nul sur le verdict et de 1e-5 sur M1.
3. *Sens du biais.* Une mise au point sur les graines d'évaluation ne peut pousser que vers la **réussite** : l'auteur qui règle son candidat le règle pour qu'il accélère. Le résultat publié est un ÉCHEC. Pour qu'un tel passage l'ait fabriqué, il faudrait un réglage **vers** l'échec, que rien de ce qui est vérifiable n'indique. Contre-épreuve, exploratoire et hors protocole : les voisins de `D_MAX`, seul paramètre de structure discrétionnaire, donnent aussi un ÉCHEC.
   ```
   D_MAX=1   M1=-0.00863 ACQ=1/4
   D_MAX=3   M1=-0.01036 ACQ=0/4
   ```
   Le verdict ne tient donc pas à une valeur de réglage étroite.
4. *Ce qui n'est pas vérifiable* [HYPOTHÈSE] : qu'aucun choix d'implémentation non préenregistré (ordre de parcours, départages) n'ait changé *avant* le commit `71760c7`. L'historique git ne voit pas ce qui précède un commit.
   - Portée : cela touche au plus les attributions des ablations (§5), pas le verdict ÉCHEC.
   - L'auteur l'a déclaré lui-même, au rapport et dans les Limites du README.

**Conclusion axe 2 : ✅.** Le passage de mise au point n'entame pas la valeur du préenregistrement pour le verdict ACQUÉRIR.

## Axe 3 — Chiffres [VÉRIFIÉ]

Au-delà du tableau (voir axe 1 : M1, M3, M4, requêtes, exactitude, R et bits de chaque système, identiques au README), recalcul depuis `resultats.json` :

```
A0 : R̂_diff<0 20/20 ; R>0 16/20 ; bat oracle-propriétés (R) 12/20 ; M1 mondes 1-5 -0.0131, 6-20 -0.0103 (sd 0.0051)
A0 : bat sans_memoire 9, verifie_toujours 13, verifie_jamais 7, sans_autodiagnostic 10  → « 7 à 13 mondes » ✓
a0bis bat a0 : 15/20 ; a0bis R_diff<0 : 17/20 ; sd a0bis 0.0158
hors g4,g19 M1 a0bis=-0.0061 a0=-0.0112
deduits faux g4, g19 : 9 18 ; R_diff g4 g19 : -0.0315 -0.0687
a0bis bat sans_memoire_famille 14/20
a0bis fin : eta 0.1232 ; phase1 19/153 = 0.124 ; sans_bruit_mle eta fin 0.1827
cout marginal min/max 0.000 0.134 ; nuls graines [1, 5, 6, 15, 20]
sans_cout_marginal : vérifications {'violation': [0, 5]} → p_bruit 0.01 partout ; g19 sans_bruit_mle : 2 DÉDUIT faux
```

Les diagnostics internes, absents de `resultats.json`, ont été vérifiés par `diag.py`. Il rejoue `evaluer_monde` d'E002 et lit l'état des objets.

```
a0    fautes attribuées 40 {'propriete': 5, 'premisse': 35} ; bruit A0 phase1 0.207 phase2 0.282 violation 0.417 ; kappa 1.0
a0bis fautes attribuées 62 {'premisse': 23, 'propriete': 39}
  rangées     : [0, 0, 1, 0, 2, 3, 3, 3, 3, 3, 4, 5, 4, 5, 5, 6, 6, 6, 6, 6]
  identifiées : [None, 0, 0, 1, 0, None, 3, None, 3, 3, 1, None, 4, None, 4, 3, 6, 6, 6, 6]
```

Ces valeurs sont identiques au tableau « familles apprises » du README : 7 familles, et identifications croisées aux graines 11 et 16. Écarts d'arrondi seulement à l'affichage : 6.55 → 6.5, 3.25 → 3.2 et 3.15 → 3.1, par l'arrondi au pair de Python. Aucun écart ⛔.

## Axe 4 — Lecture honnête : ⚠️ RÉSERVE

**A0 (README M0014) : ✅.** Chaque [VÉRIFIÉ] est soutenu par les données. Les écarts entre ablations sont qualifiés de « fragiles » (7 à 13 mondes sur 20, écart-type 0.005). Les mécanismes sont étiquetés [HYPOTHÈSE]. La section Limites refuse toute conclusion générale.

**A0-bis (README M0016).** La plupart des lectures sont justes et prudentes : échec, requêtes activées, confusion (a)×(c) signalée, identification imparfaite, et exploratoire « hors g4 et g19 » déclaré non probant. **Un point est à amender** :

- Le README écrit : « [VÉRIFIÉ] **(c) le bruit MLE ne porte pas le gain : il le dégrade.** Sans lui, M1 vaut −0.0076, le meilleur de tous les systèmes sans propriétés données », puis : « Les compteurs d'A0, plus méfiants, protègent mieux contre les cascades : 2 `DÉDUIT` faux sur la graine 19, contre 18. »
- Ce que disent les données (`resultats.json`, recalcul du doubleur) :
  ```
  diff (sans_mle − a0bis) par graine : g19 +0.0649, g13 +0.0172, g4 +0.0152 ; g3 −0.0232, g15 −0.0079, g9 −0.0075 …
  moyenne diff +0.0029   médiane −0.0001
  sans_mle meilleur dans 9/20 ; pire dans 11/20
  hors g19      : M1 a0bis −0.0074  sans_mle −0.0078
  hors g4, g19  : M1 a0bis −0.0061  sans_mle −0.0073
  médiane M1    : a0bis −0.0065  sans_mle −0.0061
  ```
- Tout l'écart de M1 (+0.0029) vient de la graine 19 (+0.0649 / 20 = +0.0032). **Sans ce seul monde, le sens s'inverse.** Et `a0bis` bat son ablation dans 11 mondes sur 20.
- Le verdict « ne porte pas » **au sens du §5** (M1 de l'ablation ≥ M1 et M2 ≥ M2) reste exact et doit rester. En revanche :
  1. « **il le dégrade** » est une conclusion causale générale tirée d'un seul cas. Elle doit passer en [HYPOTHÈSE], ou être reformulée : « l'écart de M1 est porté par la seule graine 19 ; hors elle, `a0bis` fait mieux (−0.0074 contre −0.0078) ».
  2. « Les compteurs d'A0 protègent mieux contre les cascades » ne repose que sur la graine 19 (1 monde). Même traitement : [HYPOTHÈSE], en citant le cas unique.
  3. La **Prochaine étape n°1** (« A0-ter : a0bis sans bruit MLE comme base, M1 −0.0076 ») et le rapport M0016 reposent sur cette lecture. Le README doit dire que ce choix de base tient à un seul monde, ou le présenter comme une option parmi d'autres.
- Pour la même raison, la mention « M1 −0.0076, le meilleur de tous les systèmes sans propriétés données » est **descriptivement exacte**. Elle devrait être suivie de la même précision (porté par la graine 19).

Aucune donnée, aucun code ni aucun résultat n'est à toucher : **README de A0bis seul**.

## Axe 5 — Sécurité dépôt public [VÉRIFIÉ]

```
$ git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 1be4654… -- research/
(rien)  rc=1
$ git ls-tree -r --name-only 1be4654… | grep -E '(^|/)\.env($|\.)|(^|/)raw\.jsonl$'
.env.example          # antérieur (ad328dd), hors périmètre de la branche, clé à valeur vide
```

## Axe 6 — Hygiène git [VÉRIFIÉ]

```
trailer « Co-Authored-By: Malik & Claude » (count) : 1be4654 1 · 71760c7 1 · b67bcbd 1 · 8a60250 1 · c3591e2 1 · c874e76 1 ; aucun autre co-authored
git diff --name-only 8a5b865 1be4654 | grep -vE '^research/candidats/(A0|A0bis)/'   → (vide)
```

Les 18 fichiers sont tous sous `research/candidats/A0/` et `research/candidats/A0bis/`. E002 et E002-bis sont importés via `chemin.py`, sans copie.

## Axe 7 — CLAUDE.md imbriqués / rules [VÉRIFIÉ]

`git ls-tree -r --name-only` au tip et sur `origin/main` : aucun `CLAUDE.md` et aucun `.claude/rules/`. Sans objet.

## Suite demandée

Poser un mandat « correctif README A0-bis » sur `exp/a0bis-candidat` pour les 3 points de l'axe 4, sans toucher aux données ni au code. Puis faire un doublage court de l'axe 4 et le merge. Le verdict ÉCHEC ACQUÉRIR des deux candidats est **confirmé** et n'est pas en cause.

Scripts du doubleur (scratchpad, non committés) : `recalc.py` (ACQUÉRIR et métriques, indépendant du dépôt), `diag.py` (diagnostics internes), `sensib.py` (`ZERO_NUMERIQUE`, voisins de `D_MAX`, patch en mémoire seulement).
