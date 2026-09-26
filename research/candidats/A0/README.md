# A0 — premier système candidat « ACQUÉRIR »

Mandat M0014, 2026-09-26. Python standard (≥ 3.9), aucune dépendance, aucun appel réseau, aucun LLM. E002 et E002-bis sont importés sans modification.

**Verdict préenregistré : ÉCHEC.** A0 n'accélère que dans 1 famille sur 4, il en faudrait 3. Le résultat est publié tel quel.

## Hypothèse

[HYPOTHÈSE] (§1 bis v2.1 de l'architecture) L'intelligence au sens du projet est la **boucle savoir ↔ acquis**. Un système qui garde d'un monde à l'autre des *règles* sur les propriétés, un *déclencheur* qui décide quand vérifier, et un *autodiagnostic* qui attribue chaque faute à une pièce, doit résoudre le monde n+1 plus vite que le monde n. Aucun des quatre étalons d'E002-bis n'y arrive.

## Mécanismes

Tout est détaillé dans [`PREREGISTREMENT.md`](PREREGISTREMENT.md) §3. Chaque pièce est désactivable.

1. **Mémoire inter-mondes des propriétés.** Elle ne contient aucun nom de relation ni d'entité, ce qu'un test vérifie.
   - Bibliothèque de *profils* : multiensembles de vecteurs (réflexive, symétrique, antisymétrique, transitive), pondérés par la vraisemblance des observations d'un nouveau monde.
   - Taux `q` auquel une règle fausse de chaque type « confirme » quand même.
   - A priori des compositions.
   - Compteurs de bruit par catégorie de prémisse.
2. **Déclencheur calibré.** Pour chaque fait-prémisse d'un `DÉDUIT`, A0 choisit `conclure | vérifier | INDÉTERMINÉ` par la règle `P(erreur)·κ·coût(erreur) > coût(vérification)`, avec `coût(vérification) = C_atome ≈ 9.32 bits`. `P(erreur)` vient des compteurs appris. La même règle décide des tests de propriétés.
3. **Autodiagnostic.** Chaque `DÉDUIT` faux révélé par la correction est attribué à une seule pièce, qui est la seule mise à jour :
   - propriété mal acceptée → marge `δ` du type ;
   - prémisse bruitée non vérifiée → +2 erreurs au compteur de sa catégorie ;
   - sinon → seuil `κ`.

## Protocole

[`PREREGISTREMENT.md`](PREREGISTREMENT.md) a été committé seul (`c874e76`, 17:13), **avant** le code (`c3591e2`) et avant toute exécution.
- Graines 1–20 dans l'ordre, 4 familles de 5 mondes, bruit d'E002.
- A0 ne reçoit pas le numéro de famille.
- Mesure : `R̂_diff = R − R_plafond-vérificateur`, via `evaluer_bis.evaluer_suite`, non modifié.
- Critère ACQUÉRIR inchangé : au moins 3 familles sur 4 en accélération.
- Métriques de comparaison des ablations :
  - M1 : R̂_diff moyen ;
  - M2 : nombre de familles accélérées ;
  - M3 : gain moyen du 1er au 5e monde ;
  - M4 : `DÉDUIT` faux en vérité.

| fichier | rôle |
|---|---|
| `chemin.py` | rend importables E002 et E002-bis |
| `a0.py` | le système et ses 4 ablations |
| `evaluer_a0.py` | 5 configurations + 4 étalons, verdict du candidat, `results/<horodatage>/` |
| `tests/test_a0.py` | 16 tests unittest |

## Rejouer

```sh
cd research/candidats/A0
python3 -m unittest discover   # 16 tests, ~4 s
python3 evaluer_a0.py          # graines 1-20, ~3 s, écrit results/<horodatage>/
```

- [VÉRIFIÉ] **Rejeu déterministe.** `evaluer_a0.py` se relance avec `PYTHONHASHSEED=0` (leçon M0007). Un second rejeu, lancé sous `PYTHONHASHSEED=7` ambiant, donne un `resultats.json` identique octet pour octet (`cmp`). Le `summary.md` est identique à la ligne d'horodatage près. Un test vérifie la même chose entre deux processus.
- [VÉRIFIÉ] **Contrôle des tests.** Dix mutations ont été injectées une à une, et chacune fait échouer la suite :
  1. un nom de relation mémorisé ;
  2. coût de vérification divisé par 2 ;
  3. `κ` ignoré ;
  4. prémisse fautive toujours rangée en `phase1` ;
  5. sans-mémoire qui garde la mémoire ;
  6. vérifie-toujours limité aux `CONTRADICTION` ;
  7. autodiagnostic jamais coupé ;
  8. marge appliquée à tous les types ;
  9. relance sans `PYTHONHASHSEED` ;
  10. profil non trié, donc dépendant des noms.

  La 10ᵉ n'a été détectée qu'après correction du test de renommage, qui ne retriait pas les relations renommées.

## Résultats

Exécution officielle : [`results/2026-09-26T172136+0200/`](results/2026-09-26T172136+0200/summary.md). Moyennes sur 20 mondes, réponses de phase 2.

| système | exactitude | DÉDUIT faux (vérité) | requêtes | bits économisés | R | mondes R > 0 | R̂_diff | ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|
| aléatoire | 0.328 | 9.1 | 0.0 | −33.3 | −0.0366 | 0/20 | −0.0488 | ÉCHEC (1/4) |
| oracle-propriétés | 1.000 | 4.7 | 0.0 | −2.8 | −0.0031 | 8/20 | −0.0152 | ÉCHEC (0/4) |
| plafond-vérificateur | 1.000 | 0.0 | 36.5 | +15.2 | +0.0122 | 20/20 | 0 | ÉCHEC (0/4) |
| découvreur naïf | 0.777 | 8.3 | 62.0 | −21.7 | −0.0142 | 5/20 | −0.0263 | ÉCHEC (0/4) |
| **a0** | 0.714 | **2.0** | **0.0** | **+1.0** | **+0.0011** | 16/20 | **−0.0110** | **ÉCHEC (1/4)** |
| a0 sans mémoire | 0.729 | 3.3 | 0.0 | −1.5 | −0.0017 | 10/20 | −0.0138 | ÉCHEC (1/4) |
| a0 vérifie toujours | 0.753 | 1.0 | 23.1 | −0.8 | −0.0006 | 14/20 | −0.0127 | ÉCHEC (1/4) |
| a0 vérifie jamais | 0.725 | 3.1 | 0.0 | −1.4 | −0.0016 | 12/20 | −0.0137 | ÉCHEC (1/4) |
| a0 sans autodiagnostic | 0.711 | 4.2 | 0.0 | −4.3 | −0.0047 | 10/20 | −0.0169 | ÉCHEC (1/4) |

Métriques préenregistrées (§5) :

| configuration | M1 R̂_diff moyen | M2 familles | M3 gain 1er→5e | M4 DÉDUIT faux | pire qu'a0 sur |
|---|---|---|---|---|---|
| a0 | −0.0110 | 1 | +0.0017 | 2.00 | — |
| a0 sans mémoire | −0.0138 | 1 | −0.0079 | 3.30 | M1, M3, M4 |
| a0 vérifie toujours | −0.0127 | 1 | +0.0010 | 1.00 | M1, M3 |
| a0 vérifie jamais | −0.0137 | 1 | −0.0066 | 3.15 | M1, M3, M4 |
| a0 sans autodiagnostic | −0.0169 | 1 | −0.0051 | 4.15 | M1, M3, M4 |

Courbe R̂_diff d'`a0`, monde par monde, par famille :

```text
famille 0 : -0.0238 → -0.0138 → -0.0114 → -0.0106 → -0.0058   gain +0.0180, hausses 4/4 → accélération OUI
famille 1 : -0.0031 → -0.0100 → -0.0207 → -0.0142 → -0.0132   gain -0.0101, hausses 2/4 → non
famille 2 : -0.0052 → -0.0042 → -0.0150 → -0.0095 → -0.0046   gain +0.0006, hausses 3/4 → non (gain < 0.005)
famille 3 : -0.0079 → -0.0099 → -0.0188 → -0.0093 → -0.0095   gain -0.0015, hausses 1/4 → non
```

Les courbes des ablations et des étalons sont dans le [`summary.md`](results/2026-09-26T172136+0200/summary.md).

## Lecture

- [VÉRIFIÉ] **A0 n'accélère pas au sens préenregistré : ÉCHEC d'ACQUÉRIR, 1 famille sur 4.**
  - Il n'accélère que dans la famille 0, celle où il part d'une mémoire vide : 4 hausses sur 4, R̂_diff de −0.024 à −0.006.
  - Dans les familles 1 à 3, le premier monde n'est pas plus bas que les suivants : −0.003, −0.005 et −0.008.
  - Moyenne des mondes 1–5 : −0.0131. Moyenne des mondes 6–20 : −0.0103, avec un écart-type de 0.0051.
  - [HYPOTHÈSE] Ce qu'A0 apprend est surtout **global** (calibration du bruit, marges) et non propre à une famille. Le gain est acquis pendant la première famille, puis il plafonne. Le critère, qui mesure une accélération **à l'intérieur** de chaque famille, ne le voit pas.
- [VÉRIFIÉ] **Contrôle du critère.** Aucun contrôle ne réussit ACQUÉRIR : ni les quatre étalons, ni `a0_sans_memoire`. L'aléatoire et `a0_sans_memoire` « accélèrent » chacun dans une famille, comme dans E002-bis. Le critère n'est donc pas déclaré trop permissif.
- [VÉRIFIÉ] **A0 est le meilleur système sans propriétés données, mais il reste sous le plafond-vérificateur.**
  - R̂_diff moyen : −0.0110, contre −0.0263 pour le découvreur naïf et −0.0152 pour l'oracle-propriétés.
  - A0 fait mieux que l'oracle-propriétés, **à qui on donne les vraies propriétés**, dans 12 mondes sur 20. R moyen : +0.0011 contre −0.0031.
  - Ce gain vient de l'abstention : A0 ne rend que 2.0 `DÉDUIT` faux par monde, contre 4.7. Son exactitude d'étiquette est bien plus basse (0.714) : il dit `INDÉTERMINÉ` là où une déduction était attendue.
  - A0 a R̂_diff < 0 dans 20 mondes sur 20.
- [VÉRIFIÉ] **Le déclencheur calibré ne vérifie jamais, et A0 ne teste jamais une propriété : 0 requête dans les 20 mondes.**
  - Avec `coût(vérification) = 9.32 bits` fixé au préenregistrement, un fait ne vaut d'être vérifié que s'il soutient à peu près ΣL ≥ 9.32 / p bits de déductions. Aucun fait n'atteint ce seuil sur ce banc.
  - Le déclencheur n'agit donc que par son option **INDÉTERMINÉ**, en écartant des prémisses. C'est elle qui sépare `a0` de `a0_verifie_jamais` : 2.0 contre 3.15 `DÉDUIT` faux.
  - La partie « ordre de test le plus rentable en bits » de la mémoire est **inerte** sur ce banc.
- [VÉRIFIÉ] **Quelle pièce porte le gain ?** Formellement, chaque ablation fait moins bien qu'`a0` sur au moins une métrique, sur M1 notamment. Mais A0 échoue ACQUÉRIR, donc le critère de réussite du candidat n'est pas atteint.
  - L'écart de M1 le plus net est celui de l'**autodiagnostic** : −0.0169 sans lui, contre −0.0110.
  - Monde par monde, les écarts sont fragiles. `a0` bat chaque ablation dans 7 à 13 mondes sur 20 seulement, et les écarts de M1 (0.002 à 0.006) sont de l'ordre de l'écart-type d'un monde à l'autre (0.005).
  - [HYPOTHÈSE] Mécanisme de l'autodiagnostic : sur 40 fautes attribuées, 35 le sont à une « prémisse bruitée » et 5 à une « propriété ». Aucune n'est attribuée au seuil, et `κ` reste à 1.
  - Les +2 erreurs par faute gonflent le taux de bruit appris : 0.21 en phase 1, 0.28 en phase 2, 0.42 pour la catégorie `violation`, alors que le bruit réel est de 5 à 10 %. S'y ajoute un biais d'échantillon : les atomes observés révélés sont les questions de révision, choisies parmi les atomes en cause.
  - A0 devient donc **plus méfiant** et écarte plus. Il ne *comprend* pas mieux : il s'abstient mieux.
- [HYPOTHÈSE] **Pièce suspecte n°1 : la règle de coût du déclencheur.** R est un *rapport* : bits économisés / bits d'expérience. Une requête améliore R dès que son gain en bits dépasse `R × C_atome`. Avec R proche de 0, c'est une fraction de bit, pas 9.32 bits.
  - Le préenregistrement a fixé `coût(vérification) = C_atome` en valeur absolue, ce qui rend toute vérification et tout test non rentables.
  - C'est cohérent avec le plafond-vérificateur, qui gagne +0.015 de R sur l'oracle-propriétés **en payant** 36.5 requêtes.
  - Ce n'est **pas** corrigé ici : le préenregistrement est figé. Voir le rapport M0014.
- [HYPOTHÈSE] **Pièce suspecte n°2 : l'a priori de profil**, qui ignore l'affectation. A0 ne transfère qu'une fréquence de chaque propriété dans le profil, pas « quelle relation ressemble à quel emplacement ». C'est un transfert faible, ce qui est cohérent avec l'absence de chute au premier monde de chaque famille.

## Limites

- **Un seul jeu de paramètres, 20 mondes, 4 familles.** Aucune conclusion générale.
- **Les écarts entre ablations sont petits** devant la variabilité d'un monde à l'autre. Aucun test statistique n'était préenregistré, et aucun n'est fait.
- **L'estimation du bruit est biaisée par construction du banc** : les atomes observés révélés par la correction sont surtout des atomes en cause. Ce biais pèse sur la calibration du déclencheur.
- **Exactitude d'étiquette basse (0.71)** : l'abstention d'A0 améliore R et dégrade l'exactitude. Le préenregistrement ne jugeait pas l'exactitude.
- **Hérités d'E002-bis** : `PYTHONHASHSEED` fixé ; plafond-vérificateur qui n'est pas une borne stricte ; seuil de 0.005 du même ordre que la variabilité.

## Prochaine étape

1. **A0-bis préenregistré** : coût de vérification exprimé en R marginal (`R̂ × C_atome`) au lieu de `C_atome`. On testera si les pièces « vérifier » et « tester » deviennent actives et si l'accélération apparaît.
2. **Profil avec affectation** (a priori joint relation ↔ emplacement), pour que la mémoire transfère *quoi tester* et non seulement *combien*.
3. **Séquence entrelacée de familles** (préenregistrée), pour distinguer l'apprentissage global de l'apprentissage propre à une famille.
