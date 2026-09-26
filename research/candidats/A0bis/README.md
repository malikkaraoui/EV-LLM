# A0-bis — coût marginal, mémoire par famille, bruit par maximum de vraisemblance

Mandat M0016, 2026-09-26. Python standard (≥ 3.9), aucune dépendance, aucun appel réseau, aucun LLM. A0, E002 et E002-bis sont importés sans modification.

**Verdict préenregistré : ÉCHEC d'ACQUÉRIR.** `a0bis` n'accélère dans **aucune** famille sur 4 (A0 : 1 sur 4). Le résultat est publié tel quel. A0 reste publié tel quel sur `exp/a0-candidat` (issue #18).

## Hypothèse

[HYPOTHÈSE] A0 a échoué pour trois raisons que son auteur a nommées (rapport M0014). Si on les corrige, les pièces « vérifier » et « tester » deviennent actives, et la mémoire transfère un a priori **propre à la famille**. Le monde n+1 devrait alors se résoudre plus vite que le monde n.

## Mécanismes

Tout est détaillé dans [`PREREGISTREMENT.md`](PREREGISTREMENT.md) §3. Chaque pièce est désactivable.

1. **(a) Coût marginal.** R = E / B, donc une requête augmente R **si et seulement si** `ΔE > R·C`.
   - Coût d'une requête : `R̂₊·C_atome`, avec `R̂₊ = max(0, moyenne des R réalisés des mondes passés)`.
   - Le `max(0, ·)` est un garde-fou : on ne dilue pas un R négatif avec des requêtes sans valeur.
   - Tests de règles : A0 prenait la valeur de l'information parfaite ; A0-bis prend la valeur de l'information d'**une** instance.
2. **(b) Mémoire par famille.** La signature `(variante, profil de propriétés)` est structurelle, sans nom.
   - Une famille est apprise quand un monde ne ressemble à aucune famille connue.
   - Elle est identifiée sur les observations dès que sa probabilité a posteriori atteint 0.5. Sinon, A0-bis se replie sur la mémoire globale, qui se comporte comme A0.
   - A priori **par relation** : on estime, bijection comprise, quelle relation ressemble à quel emplacement.
3. **(c) Bruit estimé par maximum de vraisemblance** sur les seuls faits observés qu'A0-bis a lui-même vérifiés, et non plus sur les fautes attribuées ni sur les révélations biaisées de la correction.

## Protocole

[`PREREGISTREMENT.md`](PREREGISTREMENT.md) a été committé seul (`b67bcbd`, 17:36:56) **avant** le code (`71760c7`, 17:45:33). Il a été poussé à 17:37.
- Graines 1–20, 4 familles de 5 mondes, bruit d'E002, `R̂_diff` et critère ACQUÉRIR d'E002-bis, métriques M1–M4 d'A0. Rien de tout cela n'est modifié.
- 4 configurations : `a0bis` et 3 ablations, une par pièce.
- Rappel : `a0` et les 4 étalons, rejoués dans la même exécution.

| fichier | rôle |
|---|---|
| `chemin.py` | rend importables A0, E002 et E002-bis |
| `a0bis.py` | le système (hérite d'`A0`) et ses 3 ablations |
| `evaluer_a0bis.py` | 4 configurations + `a0` + 4 étalons, verdict, `results/<horodatage>/` |
| `tests/test_a0bis.py` | 22 tests unittest |

## Rejouer

```sh
cd research/candidats/A0bis
python3 -m unittest discover   # 22 tests, ~8 s
python3 evaluer_a0bis.py       # graines 1-20, ~10 s, écrit results/<horodatage>/
```

- [VÉRIFIÉ] **Rejeu déterministe.** `evaluer_a0bis.py` se relance avec `PYTHONHASHSEED=0`. Un rejeu lancé sous `PYTHONHASHSEED=7` ambiant donne un `resultats.json` identique octet pour octet (`cmp`). `summary.md` ne diffère que par la ligne d'horodatage.
- [VÉRIFIÉ] **13 mutations injectées une à une, toutes détectées** :
  1. coût toujours absolu ;
  2. sans garde anti-dilution ;
  3. VOI avec `1−q` à la place de `q` ;
  4. faute attribuée comptée dans le bruit ;
  5. MLE sans seuil de 5 ;
  6. nom de relation mémorisé ;
  7. `D_MAX = 3` ;
  8. rangement qui ignore la variante ;
  9. R réalisé qui compte les atomes observés ;
  10. profil non trié ;
  11. vérification jamais comptée fausse ;
  12. R̂ non figé ;
  13. relance sans `PYTHONHASHSEED`.

  Au premier passage, les mutations 3 et 12 n'étaient pas détectées : le cas calculé à la main avait `q = 0.5`, et le gel de R̂ n'était pas testé. Deux tests ont été ajoutés, puis les 13 mutations ont été rejouées.

## Résultats

Exécution officielle : [`results/2026-09-26T174546+0200/`](results/2026-09-26T174546+0200/summary.md). Moyennes sur 20 mondes, phase 2.

| système | exactitude | DÉDUIT faux (vérité) | requêtes | bits économisés | R | R̂_diff (M1) | familles accélérées | M3 gain 1er→5e |
|---|---|---|---|---|---|---|---|---|
| plafond-vérificateur | 1.000 | 0.0 | 36.5 | +15.2 | +0.0122 | 0 | 0/4 | 0 |
| oracle-propriétés | 1.000 | 4.7 | 0.0 | −2.8 | −0.0031 | −0.0152 | 0/4 | — |
| découvreur naïf | 0.777 | 8.3 | 62.0 | −21.7 | −0.0142 | −0.0263 | 0/4 | — |
| a0 (M0014) | 0.714 | 2.0 | 0.0 | +1.0 | +0.0011 | −0.0110 | 1/4 | +0.0017 |
| **a0bis** | **0.829** | 3.1 | **22.6** | +1.5 | +0.0017 | **−0.0105** | **0/4** | +0.0021 |
| a0bis sans coût marginal | 0.685 | 6.5 | 0.3 | −13.4 | −0.0144 | −0.0266 | 0/4 | −0.0017 |
| a0bis sans mémoire par famille | 0.737 | 3.2 | 17.4 | −3.1 | −0.0016 | −0.0137 | 0/4 | −0.0113 |
| a0bis sans bruit MLE | 0.831 | 2.4 | 22.4 | +4.9 | +0.0046 | **−0.0076** | 0/4 | +0.0001 |

L'aléatoire (−0.0488, 1/4) est dans le `summary.md`.

Courbe R̂_diff d'`a0bis`, monde par monde, par famille :

```text
famille 0 : -0.0076 → -0.0108 → -0.0091 → -0.0315 → -0.0028   gain +0.0048, hausses 2/4 → non
famille 1 : -0.0019 → -0.0018 → -0.0139 → +0.0002 → +0.0007   gain +0.0026, hausses 3/4 → non (gain < 0.005)
famille 2 : -0.0006 → -0.0087 → -0.0258 → -0.0144 → -0.0004   gain +0.0001, hausses 2/4 → non
famille 3 : -0.0070 → -0.0004 → +0.0003 → -0.0687 → -0.0060   gain +0.0010, hausses 3/4 → non
```

Familles apprises par `a0bis` (graine : famille du banc → identifiée pendant le monde → rangée en fin de monde) :

```text
banc 0 : g1 —→0   g2 0→0   g3 0→1   g4 1→0   g5 0→2
banc 1 : g6 —→3   g7 3→3   g8 —→3   g9 3→3   g10 3→3
banc 2 : g11 1→4  g12 —→5  g13 4→4  g14 —→5  g15 4→5
banc 3 : g16 3→6  g17 6→6  g18 6→6  g19 6→6  g20 6→6
```

## Prédictions préenregistrées (§8) contre observé

| prédiction | observé | tenue ? |
|---|---|---|
| requêtes moyennes d'`a0bis` > 0 ; ≈ 40, dans [10, 100] | 22.6 | oui (> 0, dans l'intervalle, sous la valeur ponctuelle) |
| `a0bis_sans_cout_marginal` < 1 requête | 0.3 | oui |
| `a0bis` a un M1 supérieur à celui d'`a0` (probabilité 60 %) | −0.0105 contre −0.0110 | oui, d'un écart négligeable |
| η̂ de fin dans [0.03, 0.15] | 0.123 | oui |
| η de `a0bis_sans_bruit_mle` > 0.2 | 0.183 | **non** |
| ACQUÉRIR, probabilité ≤ 25 % | ÉCHEC, 0/4 | l'échec était le cas attendu |
| s'il y a une pièce porteuse, c'est d'abord (a) | voir Lecture | en partie |

## Lecture

- [VÉRIFIÉ] **A0-bis n'accélère pas : ÉCHEC d'ACQUÉRIR, 0 famille sur 4.** A0 en avait 1.
  - Aucune famille n'atteint à la fois un gain ≥ 0.005 et 3 hausses sur 4. La famille 1 a 3 hausses, mais un gain de 0.0026 seulement. La famille 0 a un gain de 0.0048, mais 2 hausses seulement.
  - Moyenne des mondes 1–5 : −0.0123. Moyenne des mondes 6–20 : −0.0099.
  - Contrôle : aucun étalon ne réussit ACQUÉRIR, donc le critère n'est pas trop permissif.
- [VÉRIFIÉ] **Le coût marginal rend les pièces « vérifier » et « tester » actives.**
  - 22.6 requêtes par monde, contre 0 pour A0. Le coût marginal va de 0 à 0.134 bit, contre 9.32 bits en coût absolu.
  - L'exactitude d'étiquette passe de 0.714 à 0.829 : A0-bis conclut là où A0 s'abstenait.
  - Mais le R moyen bouge à peine : M1 vaut −0.0105 contre −0.0110.
  - `a0bis` bat `a0` dans 15 mondes sur 20, mais son écart-type d'un monde à l'autre est de 0.0158, contre environ 0.005 pour A0. Deux mondes pèsent lourd :
    - graine 4 : R̂_diff −0.0315, 9 `DÉDUIT` faux ;
    - graine 19 : R̂_diff −0.0687, 18 `DÉDUIT` faux.
  - [HYPOTHÈSE] En concluant davantage, A0-bis s'expose à des cascades de déductions fausses, quand une règle mal acceptée est utilisée sur tout un monde. L'autodiagnostic attribue 39 fautes sur 62 à une propriété, contre 5 sur 40 dans A0.
- **Quelle pièce porte le gain ?** Critère §5 : une pièce porte le gain si son ablation est strictement pire sur M1.
  - [VÉRIFIÉ] **(a) le coût marginal porte, au sens préenregistré** : −0.0266 sans lui. Mais cette ablation ne retire pas une seule pièce. Avec 0.3 requête par monde, le MLE du bruit n'a que 5 vérifications (toutes de la catégorie `violation`, et toutes justes). Il tombe à la borne de 0.01 dans toutes les catégories, ce qui donne 6.5 `DÉDUIT` faux par monde. [HYPOTHÈSE] L'écart mesure surtout l'**interaction** (a)×(c) : un MLE sans vérifications est pire que l'a priori.
  - [VÉRIFIÉ] **(b) la mémoire par famille porte, au sens préenregistré** : −0.0137 sans elle. M3 vaut −0.0113 sans elle, contre +0.0021 avec. `a0bis` la bat dans 14 mondes sur 20. Mais l'identification est imparfaite :
    - 7 familles apprises pour 4 familles du banc. Les familles 0 et 2 du banc sont fragmentées : leur profil estimé varie de plus de 2 bits d'un monde à l'autre ;
    - 2 identifications croisées : la graine 11 (banc 2) est identifiée à une famille apprise sur le banc 0 ; la graine 16 (banc 3), à une famille apprise sur le banc 1.
  - [VÉRIFIÉ] **(c) le bruit MLE ne porte pas le gain : il le dégrade.** Sans lui, M1 vaut **−0.0076**, le meilleur de tous les systèmes sans propriétés données, avec 2.4 `DÉDUIT` faux et une exactitude de 0.831. Par le critère §5, c'est « ne porte pas ».
    - Le MLE sur 153 vérifications de `phase1` donne η̂ = 0.124, pour un bruit réel de 5 à 10 %. [HYPOTHÈSE] Les vérifications ne sont pas un échantillon neutre : A0-bis vérifie les prémisses des déductions qui comptent et des contradictions, où le bruit se concentre.
    - Les compteurs d'A0, plus méfiants (0.15 à 0.22), protègent mieux contre les cascades : 2 `DÉDUIT` faux sur la graine 19, contre 18.
- [VÉRIFIÉ] **Comparaison avec le plafond-vérificateur.** Tous les systèmes restent en dessous : R̂_diff < 0 dans 17 mondes sur 20 pour `a0bis`. `a0bis` paie 22.6 requêtes, contre 36.5 pour le plafond, et économise +1.5 bit, contre +15.2.
  - [HYPOTHÈSE] Le plafond vérifie **toute** prémisse avec les vraies propriétés. A0-bis vérifie moins, mais sur des règles qu'il a lui-même inférées : l'écart vient des règles, pas du nombre de vérifications.
- Exploratoire, non préenregistré : hors graines 4 et 19, M1 vaudrait −0.0061 pour `a0bis` et −0.0112 pour `a0`. Ce calcul sert seulement à situer l'effet des cascades ; il ne vaut pas résultat.

## Envies de modification du préenregistrement (NON appliquées)

1. **`D_MAX = 2` fragmente les familles.** Il donne 7 familles apprises pour 4. Il aurait fallu un seuil appris, ou une distance pondérée par la confiance de chaque bit du profil.
2. **Le MLE est fait sur des vérifications sélectionnées.** Il aurait fallu un petit budget de vérifications **tirées au hasard** parmi les observations (échantillon neutre), ou un modèle de la sélection.
3. **R̂ tombe à 0 après un seul mauvais monde** (graines 5, 6, 15 et 20 : coût marginal nul). Il aurait fallu une moyenne robuste, par exemple une médiane.

Aucune n'est appliquée ici. Toute retouche passerait par un nouveau préenregistrement.

## Limites

- **20 mondes, 4 familles, un seul jeu de paramètres.** Aucune conclusion générale.
- **Les écarts de M1 entre `a0`, `a0bis` et les ablations** (0.0005 à 0.003) sont petits devant l'écart-type d'`a0bis` (0.0158). Aucun test statistique n'était préenregistré.
- **L'ablation −coût-marginal confond deux pièces**, (a) et (c), par l'effondrement du MLE sans vérifications. Le préenregistrement ne l'avait pas anticipé.
- **Un passage de mise au point** a tourné sur les graines 1–20, après le préenregistrement et avant les tests. Il a servi à vérifier que le code s'exécutait et que le R réalisé recalculé égalait le R du banc. Aucun paramètre n'a été changé ensuite : `a0bis.py` committé (`71760c7`) est identique à celui de ce passage, et ses R par monde sont ceux de l'exécution officielle.
- **Hérités d'A0 et d'E002-bis** : `PYTHONHASHSEED` fixé ; plafond-vérificateur qui n'est pas une borne stricte ; seuil de 0.005 du même ordre que la variabilité.

## Prochaine étape

1. **A0-ter préenregistré** : a0bis sans bruit MLE comme base (M1 −0.0076), avec un **échantillon de vérification neutre** pour estimer le bruit, et un garde-fou contre les cascades (budget de `DÉDUIT` par règle nouvellement acceptée).
2. **Signature de famille robuste** (distance pondérée par la confiance), mesurée d'abord seule : pureté et nombre de familles apprises.
3. **Séquence entrelacée de familles** (préenregistrée), pour séparer l'apprentissage global de l'apprentissage propre à une famille.
