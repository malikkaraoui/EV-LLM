# E014 — « repérage » : apprendre OÙ lire, puis composer avec l'accumulateur d'E013

Mandat M0028, 2026-09-27, branche `exp/e014-reperage` (depuis `exp/e013-insecte` @ `3246ae8`).
Préenregistrement : [`PREREGISTREMENT.md`](PREREGISTREMENT.md) (poussé seul avant le code,
amendement A1 après le pilote). Code E008 et E013 importé, non modifié.

## En une phrase

Un module qui a appris **seulement à poser l'opération en colonnes** (aucune addition dans sa
perte), branché **gelé** devant l'accumulateur **gelé** d'E013, fait l'addition exacte à
**16 et 100 chiffres sur 4 graines sur 5, sans aucun entraînement joint**. Appris de bout en bout,
le même mécanisme de lecture échoue (0/5), curriculum ou pas (1/5). La composition ne perd rien tant
que la lecture est juste. Ce qui casse à 1 000 chiffres, c'est la lecture, pas le calcul.

## Question

E013 : l'accumulateur I1 (2 à 4 unités d'état) additionne exactement jusqu'à 1 000 chiffres quand
on lui **donne** les chiffres alignés, poids faible d'abord. Sur l'entrée plate `a+b=` (I2, lecture
apprise de bout en bout), il échoue (0/5). E010 : chaque colonne est juste mais le modèle ne sait
plus quel chiffre lire. Hypothèse : **le verrou est le repérage**. Q1 : un mécanisme de lecture
appris généralise-t-il en longueur ? Q2 (transfert) : une compétence apprise ailleurs (la lecture)
se branche-t-elle telle quelle sur une autre (le calcul) ?

## Protocole (résumé)

Entraînement 1–5 chiffres (flux E008). VAL-OOD 6–8 (graine 3113), seul juge du checkpoint et des
hyperparamètres. TEST lu **une seule fois** : T-LONG 10 / 16 / 32 / 64 / 100 (500 paires) et 1 000
(200), T-ID 2–5, adverses ADV-CASCADE / ADV-ZEROS / ADV-ASYM à 10–1 000 chiffres (graines neuves
3114–3118, générateurs d'E013). 5 graines officielles (1–5), pilote graine 0 exclu. Exact-match de
la réponse entière par l'évaluateur E008. Réussite d'une graine : ≥ 90 % à 16 chiffres ; système
réussi : ≥ 4/5. Confiance = **min sur les colonnes** de la probabilité du chiffre émis (p_min).

Validité [VÉRIFIÉ] (`resultats/controles.json`) : C-ORACLE 100 % sur les 8 030 items (31 jeux × L) ;
C-PARCŒUR 0,000 partout (table de 1 602 579 paires vues par la graine 1) → **TEST VALIDE**.

## Systèmes et budget de structure (rien de caché)

Commun (donné) : vocabulaire de 14 symboles, sortie poids faible d'abord, **nombre de pas**
max(ℓa, ℓb) + 1, retrait d'un 0 de tête, contrôleur = cellule E013 (F = 32, H = 8), 2 têtes de
lecture, décalages locaux {−1, 0, +1}, clés de contenu sur 3 voisins. Aucun plongement de
position. **Non donné** : où sont les opérandes, qu'il faut reculer, quand un opérande est épuisé,
la retenue.

| système | ce qui est donné en plus |
|---|---|
| **R0a** — I2 d'E013 reproduit, de bout en bout | rien |
| **R0b** — I2 + curriculum (1–2 → 1–5 chiffres par quarts) | l'ordre des longueurs |
| **R1G** — lecteur (appris seul) gelé → I1 H = 4 d'E013 gelé, **aucun entraînement joint** | la tâche « poser en colonnes » (format aligné, sens, symbole « absent ») comme supervision du lecteur ; + le budget d'I1 dans E013 (alignement et sens donnés à son entraînement) |
| **R1J** — R1G + 1 000 pas d'ajustement joint (perte d'addition) | idem R1G |
| **R2** — I2 à pointeurs **durs** (un entier par tête, straight-through) | pointeur discret |

R1 : le lecteur est entraîné par entropie croisée sur les paires alignées (aₜ, bₜ), jamais sur la
somme ; son checkpoint est choisi sur l'exactitude de **lecture** VAL-OOD. Les poids I1 sont ceux
des runs E013 `I1-H4-s1…s5` (`i1_e013/`, `SHA256SUMS`) ; contrôle positif : lecture parfaite +
I1 gelé = 100 % sur les adverses (test `test_lecture_parfaite_plus_i1_gele`).

## Résultats (TEST, 5 graines, exact-match %) [VÉRIFIÉ]

| système | graines ≥ 90 % à 16 / 100 / 1 000 | T-ID 5 | T-LONG 10 | 16 | 32 | 64 | 100 | 1 000 |
|---|---|---|---|---|---|---|---|---|
| R0a | 0/5 / 0/5 / 0/5 | 60,0 | 53,5 ± 44,4 | 26,3 ± 30,4 | 4,3 ± 8,6 | 0,0 | 0,0 | 0,0 |
| R0b | 1/5 / 1/5 / 0/5 | 80,0 | 59,8 ± 36,9 | 31,4 ± 37,0 | 20,0 ± 40,0 | 20,0 ± 39,9 | 20,0 ± 39,9 | 12,5 ± 25,0 |
| **R1G** (gelé, sans joint) | **4/5 / 4/5 / 1/5** | 96,7 | 82,4 ± 35,1 | 80,0 ± 40,0 | 80,0 ± 40,0 | 80,0 ± 40,0 | 79,7 ± 39,8 | 41,3 ± 40,7 |
| R1J (+ joint) | 4/5 / 3/5 / 1/5 | 98,8 | 85,8 ± 28,5 | 80,1 ± 39,7 | 79,8 ± 39,9 | 78,4 ± 39,3 | 74,7 ± 38,7 | 40,0 ± 42,8 |
| R2 | 0/5 / 0/5 / 0/5 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |

Par graine (T-LONG 16 / 100 / 1 000) :

- R0a : s1 0/0/0 ; s2 0/0/0 ; s3 56,0/0/0 ; s4 5,4/0/0 ; s5 70,2/0/0 (E013 I2 : 27,8 ± 32,3 à 16 → reproduit)
- R0b : s1 10,8/0/0 ; **s2 100/99,8/62,5** ; s3 0/0/0 ; s4 5,8/0/0 ; s5 40,2/0/0
- R1G : **s1 100/100/23,0 ; s2 100/98,4/3,0 ; s3 100/100/89,5 ; s4 100/100/91,0** ; s5 0/0/0
- R1J : s1 99,8/99,6/11,0 ; s2 100/73,8/4,5 ; s3 100/100/95,0 ; s4 100/100/89,5 ; s5 0,6/0/0
- R2 : 0 partout, y compris T-ID (n'apprend pas même en distribution sur les 5 graines officielles)

**R1 — la composition suit la lecture** (R1G, addition vs lecture exacte du lecteur, T-LONG
10 / 16 / 32 / 64 / 100 / 1 000) :

| graine | addition (gelé, sans joint) | lecture seule |
|---|---|---|
| s1 | 100 / 100 / 100 / 100 / 100 / 23,0 | 100 / 100 / 100 / 100 / 100 / 28,5 |
| s2 | 100 / 100 / 100 / 100 / 98,4 / 3,0 | 100 / 100 / 100 / 100 / 99,2 / 3,0 |
| s3 | 100 / 100 / 100 / 100 / 100 / 89,5 | 100 / 100 / 100 / 100 / 100 / 94,5 |
| s4 | 100 / 100 / 100 / 100 / 100 / 91,0 | 100 / 100 / 100 / 100 / 100 / 92,0 |
| s5 | 12,2 / 0 / 0 / 0 / 0 / 0 | 18,8 / 0,2 / 0 / 0 / 0 / 0 |

Adverses (exact-match moyen %, L = 10 / 16 / 32 / 64 / 100 / 1 000) :

| système | ADV-CASCADE | ADV-ZEROS | ADV-ASYM |
|---|---|---|---|
| R0a | 54,0 / 26,4 / 6,8 / 0,6 / 0,6 / 0,4 | 59,8 / 53,9 / 24,6 / 11,5 / 0,2 / 0,0 | 48,5 / 28,5 / 14,1 / 9,5 / 9,7 / 0,0 |
| R0b | 55,7 / 28,9 / 21,4 / 20,6 / 20,6 / 14,8 | 78,2 / 70,9 / 43,0 / 31,5 / 25,7 / 15,8 | 79,0 / 68,7 / 60,2 / 52,5 / 51,5 / 19,2 |
| R1G | 83,5 / 80,6 / 80,0 / 79,4 / 78,8 / 44,1 | 92,5 / 86,1 / 81,4 / 79,0 / 77,4 / 61,4 | 91,7 / 84,0 / 79,8 / 79,2 / 79,2 / 50,3 |
| R1J | 86,2 / 80,4 / 79,8 / 78,6 / 73,6 / 40,0 | 82,8 / 86,1 / 79,8 / 78,6 / 77,6 / 62,6 | 91,3 / 79,8 / 71,5 / 68,7 / 70,5 / 41,6 |
| R2 | 0 partout | 0 partout | 0 partout |

(R1G/R1J : ≈ 80 % = 4 graines à ~100 % + la graine 5 à 0 jusqu'à 100 chiffres.)

**Autodiagnostic** (TEST hors T-ID, 5 graines, 22 650 items par système) :

| système | faux | faux et sûrs (p_min ≥ 0,8) | p_min médiane justes / faux | τ par graine (VAL-OOD) | abstention quand faux / quand juste |
|---|---|---|---|---|---|
| R0a | 18 776 | 978 | 0,984 / 0,426 | —, —, 0,6, 0,9, 0,99 | 45,7 % / 19,9 % |
| R0b | 14 904 | 1 608 | 1,000 / 0,515 | 0,6, 0,99, —, 0,8, 0,9 | 57,5 % / 7,1 % |
| R1G | 5 128 | 1 218 | 0,997 / 0,545 | 0,99 ×4, 0,7 | **77,3 % / 1,4 %** |
| R1J | 5 524 | 1 266 | 1,000 / 0,511 | 0,99 ×4, 0,6 | 74,8 % / 1,0 % |
| R2 | 22 650 | 0 | — / 0,107 | aucun (0 juste en VAL) | 0 % (pas de seuil) / — |

« — » : aucun τ possible (pas de réponse juste en VAL-OOD, ou plus de 5 % des justes sous 0,5) →
pas d'abstention. Faux et sûrs mesurés aussi avec le produit (définition E013) : 602 / 1 030 /
784 / 917 / 0.

Exemples uniques vus : R0a et R2 ≈ 1 120 000 (12 000 pas × 128) ; R0b ≈ 610 000 (curriculum :
beaucoup de doublons courts) ; lecteur R1 ≈ 591 000 (6 000 pas) ; ajustement R1J ≈ 110 000 en plus.
I1 (E013) ≈ 591 000 en plus, sur sa propre tâche.

### Prédictions (préenregistrées)

| | énoncé | verdict |
|---|---|---|
| P1 | R0a ≤ 1/5 | ✅ 0/5 |
| P2 | R0b ≤ 1/5 (le curriculum ne suffit pas) | ✅ 1/5 |
| P3 | lecteur exact ≥ 90 % à 16 sur ≥ 3/5 | ✅ 4/5 (100 %) |
| P4 | addition R1G ≥ lecture − 2 pts à chaque L | ❌ vrai de 10 à 100 chiffres pour les 4 graines qui lisent (écart ≤ 0,8 pt) ; **faux à 1 000** (s1 : 23,0 contre 28,5 ; s3 : 89,5 contre 94,5) et pour s5 à 10 chiffres (12,2 contre 18,8) |
| P5 | R1J ≥ R1G − 5 pts à 100 | ✅ de justesse (74,7 contre 79,7 : −5,0) |
| P6 | R2 > R0a en graines réussies | ❌ 0 = 0 |
| P7 | p_min médiane faux < justes | ✅ pour R0a, R0b, R1G, R1J (R2 : aucun juste) |

## Diagnostic exploratoire (post hoc, NON préregistré, sur 100 paires **tirées à neuf** par L, graine 3120 — pas sur TEST)

`diagnostic14.py`, `resultats/diagnostic.json` :

1. **L'échec de P4 à 1 000 chiffres vient de l'interface douce.** Si l'on passe à I1 l'argmax du
   lecteur (one-hot) au lieu de ses probabilités, l'addition égale exactement la lecture :
   s4 à 1 000 chiffres : lecture 0,95, addition interface douce 0,82, **interface dure 0,95** ;
   s1 : 0,21 / 0,12 / 0,21. À 1 000 chiffres, les probabilités du lecteur s'aplatissent (p de
   lecture min médiane 0,52 pour s1 contre 1,000 à 16) et I1, entraîné sur des one-hot exacts,
   dérive sur ces entrées floues.
2. **Graine 5 : le lecteur a appris une lecture non locale.** Sur 3 paires de 16 chiffres, la tête
   B recule correctement de 33 à 17, mais la tête A part du **premier** chiffre de a (position 1)
   puis son argmax saute de 3 à 34 (le `=`) : une solution qui marche jusqu'à 5 chiffres
   (lecture VAL-ID 100 % en distribution) et ne se transporte pas.
3. **Faux et sûrs de R1G : où et qui les détecte.** Ils sont à L = 1 000 pour s1–s4 (217 / 169 /
   29 / 32 sur 220 / 205 / 29 / 32) : I1 est sûr de sa somme, c'est la lecture qui est fausse.
   Ré-agrégé sur TEST (déjà lu, champs stockés) : en prenant min(p_min somme, p_min lecture) comme
   confiance, les faux et sûrs de R1G tombent de **1 218 à 227** (R1J : 1 266 → 222). La confiance
   de la lecture médiane vaut 0,9999 sur les lectures justes contre 0,437 sur les fausses.

## Lecture

- [VÉRIFIÉ] **Le repérage appris de bout en bout ne généralise pas** : R0a 0/5 (reproduit I2
  d'E013), curriculum R0b 1/5, pointeurs durs R2 0/5.
- [VÉRIFIÉ] **Le repérage s'apprend quand on l'enseigne comme une tâche à part** : le lecteur,
  supervisé sur « poser en colonnes », lit à ≥ 99 % jusqu'à 100 chiffres sur 4 graines sur 5
  (entraîné sur ≤ 5 chiffres).
- [VÉRIFIÉ] **Une compétence apprise ailleurs se réutilise telle quelle** : lecteur gelé + I1
  d'E013 gelé, **zéro pas d'entraînement joint**, = addition exacte à 16 et 100 chiffres sur
  4/5 graines. Sur 10–100 chiffres, pour ces 4 graines, l'addition composée suit la lecture à
  ≤ 0,8 pt près.
- [VÉRIFIÉ] L'ajustement joint court n'apporte rien et peut dégrader (s2 à 100 chiffres :
  98,4 → 73,8).
- [VÉRIFIÉ] À 1 000 chiffres, le maillon faible est la lecture (1/5 graine ≥ 90 %), pas le calcul.
- [HYPOTHÈSE, appuyée par le diagnostic exploratoire sur 100 paires] Une interface **discrète**
  (le lecteur transmet un chiffre, pas une distribution) rendrait la composition sans perte à
  toute longueur ; la limite restante serait l'aplatissement des pointeurs doux du lecteur sur les
  longues distances.
- [HYPOTHÈSE] Le prix payé est explicite : **quelqu'un a défini la tâche intermédiaire** (les
  colonnes). Le transfert marche parce que l'interface entre les deux compétences (paires
  alignées, poids faible d'abord, « absent ») est la même des deux côtés — c'est un contrat
  donné, pas découvert.
- [HYPOTHÈSE] R2 : l'échec (0 même en distribution sur 5/5 graines alors que la graine pilote
  atteint VAL-OOD 1,000) ressemble à une instabilité d'optimisation du straight-through, pas à
  une preuve contre les pointeurs relatifs ; non testé plus avant.
- Autodiagnostic [VÉRIFIÉ] : la confiance par colonne sépare bien justes et faux (P7), et avec un
  seuil fixé sur VAL-OOD, R1G s'abstient sur 77 % de ses erreurs pour 1,4 % de ses réponses
  justes. Mais une confiance prise sur le seul calcul laisse passer les erreurs de lecture
  (leçon E010 confirmée et précisée : il faut la confiance de **chaque** étape, lecture comprise).

## Limites

- 5 graines ; conclusions sur 4 graines réussies, pas une loi générale.
- VAL-OOD 6–8 saturé (1,000) pour la plupart des runs : le checkpoint retenu est presque toujours
  le dernier (limite écrite en A1 avant les runs).
- R2 est notre interprétation de « pointeurs relatifs » (I2 avait déjà des décalages relatifs) ;
  elle a échoué pour une raison d'optimisation, la question « relatif vs absolu » reste ouverte.
- Le diagnostic 1–3 est post hoc, sur 100 paires par L ; à confirmer par une expérience
  préenregistrée (interface dure).

## Calcul

Entraînement ≈ 74 min (pilote ≈ 21 min compris), évaluation TEST ≈ 8,5 min, contrôles et
diagnostic ≈ 5 min, sur M1 partagé avec d'autres fenêtres. Budget 4 h respecté, aucune réduction.

## Reproduire

```
export PYTHONDONTWRITEBYTECODE=1                      # leçon E013 (.pyc obsolètes)
python -m unittest test_e014                          # 10 tests
python entraine14.py --configs R1L R1J R0a R0b R2 --graines 1 2 3 4 5   # relancer jusqu'à FILE TERMINEE
python controles14.py
python evalue14.py --runs R1G-s1 … R2-s5              # TEST, une seule fois
python analyse14.py && python diagnostic14.py
```
