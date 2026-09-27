# E008 — addition : le test est-il juste, et où casse un transformer de base ? (palier 0)

Mandat M0021, 2026-09-26, branche `exp/e008-addition` (depuis `origin/main` @ `677b928`).
Sans Jev, sans API, sans mécanisme EV-LLM. Préenregistrement : [`PREREGISTREMENT.md`](PREREGISTREMENT.md)
(amendement A1 : pas figés après pilote). Résultats bruts agrégés : [`resultats/`](resultats/).

## Hypothèse

Cap du 26/09 : un modèle qui **apprend une procédure et non des exemples**. Premier palier :
l'addition entraînée sur des opérandes de 1 à 5 chiffres, testée sur des opérandes plus longs.
Avant de mesurer quoi que ce soit (leçon M0020), on prouve que le test est **juste** : réussi
à 100 % par un oracle, impossible à réussir par cœur. Ensuite on mesure deux références :

- **B-STD** : petit transformer au format standard (positions absolues apprises, somme poids
  fort d'abord) — la littérature prédit un effondrement au-delà des longueurs vues ;
- **B-REF** : même modèle, **NoPE + sortie inversée** — correctif connu, à faible « triche ».

## Protocole

- Format caractère, un token par chiffre (`0`–`9`, `+`, `=`, fin, remplissage) ; `a+b=` → somme.
- Entraînement : flux déterministe, longueurs d'opérandes **uniformes et indépendantes dans
  1–5**, 12 000 pas × 256 = 3 072 000 exemples ; toute paire de test (et sa paire échangée) est
  exclue du flux.
- Tests (les deux opérandes ont L chiffres) : **T-ID** L = 2–5 (500 / L, disjoint), **T-ID1**
  (les 100 paires à 1 chiffre, non disjoint par nécessité, rapporté à part), **T-OOD** L = 6, 7,
  8, 10, 12, 16 (500 / L), **T-CARRY** : retenue à *chaque* position (500 / L) + `99…9 + 1` et
  `1 + 99…9`, L = 2–16.
- Modèle : decoder-only pré-LN, d = 256, 4 couches, 4 têtes, FFN 1 024 ; 3 179 022 paramètres
  (B-STD) / 3 162 638 (B-REF, sans table de positions). AdamW, lr 1e-3 (montée 500, cosinus),
  wd 0,01, écrêtage 1,0, float32, MLX 0.29.3 sur Apple M1. Graines officielles 1, 2, 3 ; B-STD et
  B-REF de même graine voient exactement les mêmes exemples. Graine 0 = pilote, exclue.
- Un **évaluateur unique** (`evaluate.py`) pour les 4 systèmes ; décodage glouton ; exact-match
  sur la réponse entière ; confiance = produit des probabilités des tokens générés ;
  « faux et sûr » = faux avec confiance ≥ 0,8.

## Rejouer

```
python3 -m venv $HOME/.venvs/ev-llm-e008
$HOME/.venvs/ev-llm-e008/bin/pip install -r research/experiments/E008-addition/requirements.txt
cd research/experiments/E008-addition
PY=$HOME/.venvs/ev-llm-e008/bin/python
$PY -m unittest -v test_e008                 # 15 tests
$PY controles.py                             # C-ORACLE, C-PARCOEUR -> resultats/controles.json (~40 s)
for s in B-STD B-REF; do for g in 1 2 3; do
  $PY train.py --systeme $s --graine $g      # relancer tant que "fini": false (<= 8,5 min / invocation)
done; done
for s in B-STD B-REF; do for g in 1 2 3; do $PY evaluate.py --systeme $s --graine $g; done; done
$PY analyse.py                               # resultats/resultats.json, summary.md, courbe.csv
```

Checkpoints et journaux item par item (`runs/`) hors git. Le GPU MLX n'est **pas** reproductible
au bit près (écarts ~3e-8 après 20 pas, même graine, [VÉRIFIÉ] par `test_e008`) : un rejeu
donnera des chiffres très proches, pas forcément identiques à l'item près.

## Validité du test

| contrôle | attendu | obtenu |
|---|---|---|
| C-ORACLE (retenue codée à la main) | 100 % partout | **100 %** sur les 21 jeux × longueurs (10 120 items) |
| C-PARCŒUR (table des 2 100 191 paires distinctes vues, graine 1) | ≤ 1 % sur T-ID et T-OOD | **0 %** partout ; **100 %** sur T-ID1 (contrôle positif : la table marche) |

**Verdict : TEST VALIDE** [VÉRIFIÉ] (`resultats/controles.json`, commit `f073298`, publié avant
la lecture de tout modèle appris).

## Résultats

Exact-match (%), moyenne ± écart-type sur les graines 1, 2, 3 (valeurs par graine :
[`resultats/summary.md`](resultats/summary.md)).

| jeu | L | B-STD | B-REF |
|---|---|---|---|
| T-ID1 | 1 | 100,0 ± 0,0 | 100,0 ± 0,0 |
| T-ID | 2 | 100,0 ± 0,0 | 100,0 ± 0,0 |
| T-ID | 3 | 99,5 ± 0,6 | 100,0 ± 0,0 |
| T-ID | 4 | 98,8 ± 1,4 | 100,0 ± 0,0 |
| T-ID | 5 | 98,4 ± 1,4 | 100,0 ± 0,0 |
| T-OOD | 6 | **0,0 ± 0,0** | **91,2 ± 6,2** (90,2 / 97,8 / 85,6) |
| T-OOD | 7 | 0,0 ± 0,0 | 7,9 ± 3,3 |
| T-OOD | 8 | 0,0 ± 0,0 | 0,1 ± 0,2 |
| T-OOD | 10, 12, 16 | 0,0 | 0,0 |
| T-CARRY | 2 / 3 / 4 / 5 | 100,0 / 99,7 / 97,9 / 97,8 | 100,0 / 100,0 / 100,0 / 100,0 |
| T-CARRY | 6 / 7 / 8 | 0,0 / 0,0 / 0,0 | 87,7 ± 9,4 / 8,6 ± 3,4 / 0,7 ± 0,4 |
| T-CARRY | 10 / 12 / 16 | 0,0 / 0,0 / 0,0 | 0,2 / 0,0 / 0,0 |

**« Faux et sûr »** (faux avec confiance ≥ 0,8, parmi les faux, 3 graines cumulées) :

| jeu, L | B-STD | B-REF |
|---|---|---|
| T-ID 3–5 | 12 / 50 (24 %) | aucun faux |
| T-OOD 6 | 977 / 1 500 (65 %) | 107 / 132 (81 %) |
| T-OOD 7 | 1 015 / 1 500 (68 %) | 924 / 1 381 (67 %) |
| T-OOD 8 | 488 / 1 500 (33 %) | 413 / 1 498 (28 %) |
| T-OOD 10 / 12 / 16 | 21 % / 29 % / 35 % | 1,9 % / 0,1 % / 0,0 % |

**Courbe d'efficacité** (exact-match moyen, 100 premiers items ; CSV complet :
[`resultats/courbe.csv`](resultats/courbe.csv)) :

| système | exemples vus | T-ID 2 | T-ID 5 | T-OOD 6 | T-OOD 8 |
|---|---|---|---|---|---|
| B-STD | 256 000 | 91 | 12 | 0 | 0 |
| B-STD | 1 024 000 | 98 | 73 | 0 | 0 |
| B-STD | 3 072 000 | 100 | 97 | 0 | 0 |
| B-REF | 256 000 | 92 | 27 | 6 | 0 |
| B-REF | 1 024 000 | 100 | 98 | 39 | 0 |
| B-REF | 2 048 000 | 100 | 100 | 58 | 0 |
| B-REF | 3 072 000 | 100 | 100 | 91 | 0 |

**Prédictions préenregistrées** : P1 (B-STD T-ID ≥ 95 %) **confirmée** ; P2 (B-STD T-OOD 8
≤ 10 %) **confirmée** ; P3 (B-REF T-ID ≥ 95 %) **confirmée** ; P4 (B-REF T-OOD 6 ≥ B-STD + 10
pts) **confirmée** (91,2 contre 0,0) ; P5 (T-CARRY < T-ID à L = 2–5 pour les deux modèles)
**infirmée** : B-REF est à 100 % sur les deux, B-STD à égalité à L = 2 (inférieur à L = 4–5).

Durée de calcul des 6 entraînements officiels : 1 332 / 1 316 / 1 307 s (B-STD), 1 318 /
1 290 / 1 295 s (B-REF), soit **7 858 s ≈ 2 h 11** (budget 3 h). Évaluations : 21–29 s chacune.

## Lecture

- [VÉRIFIÉ] Le test est juste au sens du critère préenregistré : l'oracle passe partout, la
  mémoire pure échoue partout hors T-ID1. Tout score non nul d'un modèle appris sur T-ID/T-OOD
  exige donc autre chose que la consultation des paires vues.
- [VÉRIFIÉ] B-STD apprend l'addition **dans** la distribution (98–100 %) et tombe à **0,0 %
  dès 6 chiffres**, sur les 3 graines, sans exception (3 000 items T-OOD par graine). Ses
  réponses hors distribution sont presque toujours **trop courtes** (graine 1, L = 6 : 486 / 500
  réponses d'un seul chiffre ; bonne longueur de réponse : 0 / 500 à L = 6, 5 / 500 à L = 8) : l'échec n'est pas une erreur de retenue, c'est une sortie qui
  ne ressemble plus à une addition.
- [VÉRIFIÉ] Et il se trompe **avec assurance** : 65–68 % de ses erreurs à 6–7 chiffres ont une
  confiance ≥ 0,8, et encore 21–35 % à 10–16 chiffres. Sa confiance ne signale donc pas qu'il
  est sorti de son domaine.
- [VÉRIFIÉ] B-REF (NoPE + sortie inversée) tient à **91 % à 6 chiffres** (+1 chiffre au-delà de
  l'entraînement), puis **8 % à 7** et **≈ 0 % à partir de 8**. Ses réponses ont la bonne
  longueur (graine 1 : 500 / 500 à L = 6, 499 / 500 à L = 7, 494 / 500 à L = 8) ; les erreurs portent sur des chiffres internes.
  Le correctif « connu, faible triche » repousse donc la frontière d'**un chiffre**, pas plus,
  dans ce budget.
- [VÉRIFIÉ] À grande longueur (10–16), B-REF devient **peu sûr** de ses erreurs (≤ 2 % de faux
  et sûrs), contrairement à B-STD. À 6–8 chiffres en revanche, ses erreurs sont aussi souvent
  sûres que celles de B-STD (28–81 %).
- [HYPOTHÈSE] La courbe de B-REF à 6 chiffres monte encore en fin d'entraînement (58 % à
  2,0 M exemples → 91 % à 3,1 M) : avec plus de pas, 6 chiffres pourrait saturer ; rien
  n'indique que 8 chiffres suivrait (0 % à tous les jalons).
- [HYPOTHÈSE] Le tableau par longueur de chaîne de retenue (`summary.md`) est confondu avec la
  longueur : les chaînes ≥ 6 n'existent que hors distribution. Il ne permet pas de dire si les
  retenues longues sont difficiles *en soi* ; T-CARRY dans la distribution (≥ 97,8 %) dit que
  non, à ces longueurs.
- Aucune conclusion au-delà de : cette tâche, ~3 M paramètres, 3 M exemples, ce format.

## Limites

- Une seule tâche (addition d'entiers positifs), une seule taille (~3,2 M), un seul budget
  (12 000 pas, réduit de 20 000 après pilote pour tenir 3 h sur M1), un seul jeu
  d'hyperparamètres, non réglé par système.
- T-ID à 1 chiffre non disjoint (100 paires possibles) : rapporté à part.
- Longueurs de test « égales » seulement (les deux opérandes ont L chiffres), sauf
  `99…9 + 1`.
- B-REF n'inverse que la **sortie** ; les opérandes restent en ordre standard (choix du
  préenregistrement ; d'autres variantes de la littérature inversent aussi les opérandes).
- GPU non déterministe au bit ; 3 graines seulement (écart-type de 6 à 9 points à L = 6 pour
  B-REF).

## Ce que le palier 1 doit battre

Sans injecter l'alignement des chiffres à la main (pas d'index hints, pas de position coupling,
pas d'Abacus, pas d'opérandes pré-alignés), avec le même flux d'entraînement (1–5 chiffres,
≤ 3,1 M exemples) et le même évaluateur :

| cible | B-STD | B-REF (à battre) |
|---|---|---|
| T-ID 2–5 | 98,4–100 % | 100 % (à conserver) |
| T-OOD 6 | 0,0 % | **91,2 ± 6,2 %** |
| T-OOD 7 | 0,0 % | **7,9 ± 3,3 %** |
| T-OOD 8 | 0,0 % | **0,1 ± 0,2 %** |
| T-OOD 10 / 12 / 16 | 0,0 % | **0,0 %** |
| T-CARRY 6 / 7 / 8 | 0,0 % | 87,7 / 8,6 / 0,7 % |
| « faux et sûr » T-OOD 6–8 | 33–68 % des faux | 28–81 % des faux |

Un mécanisme qui « apprend la procédure » devrait se voir à **L ≥ 8**, là où les deux
références sont à 0, et avec des erreurs **non sûres** quand il échoue.
