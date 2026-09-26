# A0-bis — Préenregistrement : coût marginal, mémoire par famille, bruit par maximum de vraisemblance

Mandat M0016, 2026-09-26. **Figé avant tout code de ce dossier.** Ce texte ne se modifie pas après avoir vu un résultat : un écart entre ce qu'il annonce et ce qu'on observe est un résultat, pas une correction.

A0 (`research/candidats/A0/`, branche `exp/a0-candidat` @ `8a60250`, issue #18) reste publié tel quel : **ÉCHEC ACQUÉRIR (1/4 familles)**. A0-bis est un **nouveau** candidat, préenregistré à part. Il importe A0, E002 et E002-bis sans en modifier ni en copier aucun fichier.

## 0. Pourquoi A0-bis

Le rapport M0014 nomme trois défauts d'A0 :
1. [VÉRIFIÉ, M0014] **0 requête dans les 20 mondes.** Le déclencheur comparait un gain au coût **absolu** d'une requête (`C_atome ≈ 9.32 bits`), alors que R est un **rapport**. Aucune vérification ni aucun test n'est jamais rentable : les pièces « vérifier » et « tester » sont inertes.
2. [HYPOTHÈSE, M0014] **Mémoire globale.** A0 apprend de la prudence générale, pas un a priori propre à une famille. Le gain est acquis dans la famille 0, puis plafonne.
3. [VÉRIFIÉ, M0014] **Bruit appris surestimé** : 0.21 à 0.42, contre 5 à 10 % en vrai. Deux causes : l'autodiagnostic ajoute 2 erreurs par faute attribuée à une prémisse (35 sur 40), et les atomes observés révélés par la correction sont surtout des questions de révision, choisies parmi les atomes en cause.

A0-bis corrige chacun de ces défauts par une pièce, et chaque pièce a son ablation (§4).

Transparence : l'auteur de ce texte a lu le code public du banc (`monde.py`), donc la liste des profils des familles. A0-bis ne reçoit ni le numéro de famille, ni les types, ni les propriétés : il ne lit que la vue publique (`vue_publique`), ses observations, ses requêtes et la correction de fin de monde.

## 1. Repris sans modification

- **De E002 et E002-bis** : banc, bruit, oracle, coût d'une requête, R, `evaluer_bis.evaluer_suite`, critère ACQUÉRIR, étalons. Tout est repris comme dans A0 §1.
- **De A0 (`a0.py`, importé)**, sauf ce que §3 remplace :
  - règles candidates et instances (§3.1 d'A0) ;
  - croyance en log-cote ;
  - bibliothèque de profils ;
  - `q_type` ;
  - a priori des compositions ;
  - autodiagnostic (§3.3 d'A0) ;
  - réponses par chaînage de Horn ;
  - budget de 150 requêtes par monde ;
  - catégories de prémisses `phase1`, `phase2`, `violation` ;
  - `κ` et `δ` avec les mêmes pas.

## 2. Séquence, graines, bruit, critères : ceux d'A0 et d'E002-bis

- **Graines 1 à 20, dans cet ordre**, familles `(graine − 1) // 5`. Même bruit (5–10 % par monde, une inversion ciblée en phase 2). **Aucune graine n'est ajoutée.**
- Un seul objet traverse les 20 mondes, avec son état conservé.
- Mesure : `R̂_diff = R − R_plafond-vérificateur` (E002-bis), non modifiée.
- Critère ACQUÉRIR, non modifié. Une famille est en accélération si `R̂_diff(5e) − R̂_diff(1er) ≥ 0.005` et si au moins 3 transitions sur 4 ont `ΔR̂_diff > 0`. Il faut au moins 3 familles sur 4.
- Métriques M1 à M4, définies comme dans A0 §5 :
  - M1 : R̂_diff moyen ;
  - M2 : familles accélérées ;
  - M3 : gain moyen du 1er au 5e monde ;
  - M4 : `DÉDUIT` faux en vérité par monde.
- `PYTHONHASHSEED=0` pour l'évaluateur (leçon M0007).

## 3. Les trois pièces d'A0-bis

### 3.1 (a) Déclencheur en coût marginal sur R

**Dérivation : quand une requête augmente-t-elle R ?** Dans un monde, `R = E / B`, où :
- `E` est le total des bits économisés sur les atomes tenus à l'écart ;
- `B` est le total des bits d'expérience : `B = (n_obs + n_req)·C + n_excl·C_excl`, avec `C = C_atome`.

Une requête ajoute `C` à `B` et change `E` d'une quantité `ΔE`, son gain espéré en bits sur les atomes tenus à l'écart. Pour `B > 0` :

```
(E + ΔE) / (B + C) > E / B   ⇔   B·ΔE > E·C   ⇔   ΔE > (E / B)·C = R·C
```

Une requête augmente R **si et seulement si** `ΔE > R·C`. Le coût marginal d'une requête, en bits de gain, est donc `R·C`, et non `C`. Si R est proche de 0, c'est une fraction de bit.

**Garde-fou anti-dilution.** Si `R < 0`, la dérivation dit qu'une requête de gain nul augmente R : elle dilue un R négatif. A0-bis n'exploite pas cette dilution. Il utilise `R̂₊ = max(0, R̂)`, et une requête n'est faite que si son gain espéré est **strictement positif et strictement supérieur** à `R̂₊·C`.

**Estimation de R̂.**
- A0-bis ne connaît pas `E` pendant le monde, car il ne connaît pas la vérité.
- `R̂` est la **moyenne des R réalisés sur les mondes passés** de la famille identifiée (§3.2).
- Si la famille est inconnue, c'est la moyenne sur tous les mondes passés.
- S'il n'y a aucun monde passé, `R̂ = 0`.
- Le R réalisé d'un monde passé est recalculé par A0-bis en fin de monde, avec ses seules informations publiques :
  - atomes des questions non observés ;
  - vérité révélée par la correction ;
  - `p_ref` de Laplace ;
  - ses propres réponses de phase 2 ;
  - `B` calculé depuis ses observations, ses requêtes acceptées et les exclusions de la vue.
- `R̂` est figé pour tout le monde courant.

**Règle de requête** : `coût_marginal = R̂₊ · C_atome`. On demande l'atome dont la **valeur de l'information** (VOI, en bits sur les questions non observées) est maximale, si `VOI > coût_marginal`. Puis on recalcule, et on recommence jusqu'à ce qu'aucune requête ne soit rentable ou que le budget de 150 soit atteint.

- **Vérifier un fait-prémisse `f`** d'un `DÉDUIT`. Notations d'A0 §3.2 : `p = P(erreur de f)`, `ΣG_f`, `ΣL_f`, `κ`.
  - La requête révèle `f` sans bruit, donc c'est une information parfaite :
    `VOI_f = (1−p)·ΣG_f − max((1−p)·ΣG_f − p·κ·ΣL_f, 0) = min(p·κ·ΣL_f, (1−p)·ΣG_f)`.
  - Pour un fait prémisse d'un `CONTRADICTION` : `VOI_f = p·ΣG_c`, avec `G_c` le plus petit des deux gains, comme dans A0.
  - On retient le maximum des deux.
- **Tester une règle `ρ`**, par une requête sur le conséquent inconnu d'une instance.
  - A0 prenait `P(mauvaise décision)·coût`, qui est la valeur d'une information **parfaite** sur la règle. Une instance n'en donne qu'une partie. Avec un coût proche de 0, cette surestimation lancerait des tests sans valeur. A0-bis prend donc la **VOI myope d'une instance**.
  - Utilité d'utiliser la règle : `U(b) = max(0, b·ΣG + (1−b)·(q·ΣG − (1−q)·ΣL))`. Les sommes sont celles d'A0 §3.1 (questions non observées ajoutées à la fermeture).
  - Soit `m'` le nombre d'antécédents non sûrs de l'instance testée, et `η_m' = 1 − (1−η)^m'`. Le conséquent demandé devient sûr.
  - Deux issues :
    - confirmation : `P_c = b·(1−η_m') + (1−b)·q`, et `b_c = b·(1−η_m') / P_c` ;
    - violation : `P_v = 1 − P_c`, et `b_v = b·η_m' / P_v`. Si `m' = 0`, alors `b_v = 0`.
  - `VOI_ρ = P_c·U(b_c) + P_v·U(b_v) − U(b)`.
  - L'instance testée est celle d'A0 : on préfère les antécédents sûrs.
- Ordre : les tests de règles d'abord (étape 1 d'A0), puis les faits-prémisses (étape 2), comme dans A0. L'option INDÉTERMINÉ d'A0 est conservée : un fait est écarté si `0 > (1−p)·ΣG_f − p·κ·ΣL_f`.

### 3.2 (b) Mémoire indexée par famille, avec repli global

**Signature d'un monde.** C'est une grandeur structurelle et observable, sans nom : `(variante, profil)`.
- `variante` ∈ {A, B} se lit dans la vue publique (`semantique.variante`). C'est le type de règle sémantique, pas un nom de relation.
- `profil` est le multiensemble trié des 5 vecteurs `(réfl, sym, antisym, trans)`, estimés en fin de monde comme dans A0.

**Familles apprises.**
- En fin de monde, le monde est rangé dans la famille apprise de même variante dont le profil représentant est à la plus petite **distance de Hamming**. Cette distance est minimisée sur les 120 bijections, sur les 20 bits du profil.
- Le rangement se fait si la distance est `≤ D_MAX = 2`, avec départage par l'ordre de création.
- Sinon, une nouvelle famille est créée, et son représentant est ce profil.
- Les familles sont numérotées par ordre d'apparition. Ce numéro n'a aucun lien avec celui du banc.

**Identification au début de chaque phase**, sur les seules observations.
- Pour chaque famille apprise de même variante, on calcule la log-vraisemblance des observations. C'est la moyenne sur les profils de ses mondes de la somme sur les 120 bijections, avec la vraisemblance d'A0 §3.1.
- On la compare au composant « nouveau » d'A0 : propriétés indépendantes, fréquences globales.
- Poids a priori égaux. Si la famille de plus grand poids a une probabilité a posteriori **≥ 0.5**, elle est identifiée.
- Sinon, la famille est inconnue et A0-bis se replie sur la mémoire globale, qui se comporte exactement comme A0.

**Ce qui est indexé par famille** (chaque famille garde sa propre copie ; la mémoire globale agrège tous les mondes) :
- les profils ;
- `q_type` ;
- l'a priori des compositions ;
- les marges `δ` ;
- les R réalisés (§3.1).

Le bruit (§3.3) et `κ` restent **globaux**. Le bruit du banc est tiré par monde, pas par famille. Cela se lit dans le code public, et A0-bis n'a de toute façon pas assez de vérifications pour l'estimer par famille.

**A priori avec affectation.** Si une famille est identifiée, l'a priori de la propriété `i` de la relation `r` est
`π(r, i) = 0.1 + 0.8 · Σ_{profil, bijection} w · vecteur[bijection(r)][i]`,
où les poids `w` sont proportionnels à la vraisemblance des observations. Il dépend donc de la relation : c'est le défaut n°2 d'A0 (« profil sans affectation »). Si la famille est inconnue, l'a priori est la marginale d'A0, la même pour toutes les relations.

**Mise à jour en fin de monde.** Profils, `q`, compositions, `δ` et R réalisé vont dans la famille où le monde est rangé **et** dans la mémoire globale. L'autodiagnostic met à jour le `δ` de la famille identifiée pendant le monde (à défaut, celui de la mémoire globale) et le `δ` global.

### 3.3 (c) Bruit par maximum de vraisemblance sur les vérifications

- Pour chaque catégorie `c` ∈ {`phase1`, `phase2`, `violation`}, A0-bis compte :
  - `n_c`, le nombre de faits **observés** qu'il a lui-même demandés (vérifications) ;
  - `k_c`, le nombre de ceux dont la valeur observée était fausse.
- Les vérifications des mondes passés et celles du monde en cours sont cumulées.
- Estimation par maximum de vraisemblance d'une loi de Bernoulli : `η̂_c = k_c / n_c`, bornée à [0.01, 0.5].
  - Si `n_c < 5` : on prend `η̂` sur les trois catégories cumulées, si le total atteint 5.
  - Sinon, on prend la valeur a priori d'A0 : 0.1 pour `phase1` et `phase2`, 0.5 pour `violation`.
- `η` (§3.1 d'A0) est l'estimation cumulée sur `phase1` et `phase2`, avec le même repli.
- **Ne compte pas** :
  - les fautes attribuées par l'autodiagnostic. La branche « prémisse bruitée » ne touche plus au bruit : elle est enregistrée, sans effet ;
  - les vérités révélées par la correction, car les questions de révision sont choisies parmi les atomes en cause.

## 4. Configurations (préenregistrées)

| nom | (a) coût | (b) mémoire | (c) bruit |
|---|---|---|---|
| `a0bis` | marginal `R̂₊·C` | par famille + repli global | MLE sur vérifications |
| `a0bis_sans_cout_marginal` | `C` absolu (règle d'A0) | par famille | MLE |
| `a0bis_sans_memoire_famille` | marginal | globale seule (comme A0), R̂ global | MLE |
| `a0bis_sans_bruit_mle` | marginal | par famille | compteurs Beta d'A0 (révélations + 2 erreurs par faute attribuée) |

- Dans `a0bis_sans_cout_marginal`, seul le coût change : la VOI des tests reste celle de §3.1.
- Sont rejoués en rappel, dans la même exécution :
  - `a0`, importé sans modification ;
  - les quatre étalons d'E002-bis : aléatoire, oracle-propriétés, plafond-vérificateur, découvreur naïf.

## 5. Critères

- **Réussite d'A0-bis** : `a0bis` satisfait ACQUÉRIR (au moins 3 familles sur 4 en accélération).
- **Échec** : `a0bis` échoue ACQUÉRIR. Le résultat est publié tel quel, en nommant la pièce suspecte.
- **Attribution du gain.** Une pièce **porte** une part du gain si son ablation fait strictement moins bien qu'`a0bis` sur M1. Elle ne le porte pas si l'ablation fait au moins aussi bien sur M1 et sur M2. Ce jugement est descriptif ; aucun test statistique n'est préenregistré.
- **Contrôle** : les quatre étalons ne gardent rien et **doivent** échouer ACQUÉRIR. Sinon, le critère est déclaré trop permissif sur ce banc, et c'est constaté sans être corrigé.

## 6. Tests (unittest, stdlib) et mutations

- **Coût marginal à la main.**
  - Cas `E = 10`, `B = 1000`, `C = 9.32` : `R·C = 0.0932`. Une requête de gain `ΔE = 0.1` augmente R, une requête de gain `0.09` le diminue. On le vérifie aussi par calcul direct de `(E+ΔE)/(B+C)`.
  - `R̂ < 0` donne un coût marginal nul, et une VOI nulle ne déclenche rien.
  - VOI d'une instance sur un cas chiffré à la main.
- **Aucune fuite de nom** : l'état appris, sérialisé après plusieurs mondes, ne contient aucun `R\d` ni `o\d{3}`. Renommer les relations et les entités d'un monde laisse l'état identique.
- **MLE du bruit** :
  - sur des vérifications synthétiques connues (par exemple 3 fausses sur 40, soit 0.075), l'estimation est exacte ;
  - les fautes attribuées par l'autodiagnostic ne la changent pas ;
  - le repli se déclenche sous 5 vérifications.
- **Famille** : deux profils à distance ≤ 2 sont rangés ensemble, à distance 3 ils sont séparés, et une variante différente les sépare toujours.
- **Déterminisme** : deux processus sous des `PYTHONHASHSEED` ambiants différents donnent des résultats identiques.
- **Mutations** : au moins 5, injectées une à une, et chacune doit faire échouer la suite.

## 7. Exécution

`evaluer_a0bis.py` : les 4 configurations A0-bis, `a0` et les 4 étalons, sur les graines 1–20.
- Sorties : `results/<horodatage>/resultats.json` et `summary.md`, committées.
- Le rejeu déterministe est prouvé par `cmp`.

## 8. Prédictions chiffrées (écrites avant toute exécution)

- [HYPOTHÈSE] **Nombre moyen de requêtes par monde de `a0bis` > 0.** Prédiction ponctuelle : ≈ 40, intervalle attendu [10, 100]. Référence : le plafond-vérificateur en fait 36.5, `a0_verifie_toujours` 23.1.
- [HYPOTHÈSE] `a0bis_sans_cout_marginal` fait **0 requête** en moyenne (< 1), comme A0.
- [HYPOTHÈSE] `a0bis` a un R̂_diff moyen supérieur à celui d'`a0` (−0.0110). Probabilité subjective : 60 %.
- [HYPOTHÈSE] `η̂` de `phase1` et `phase2`, en fin de séquence, entre 0.03 et 0.15. Pour `a0bis_sans_bruit_mle`, il est supérieur à 0.2, comme dans A0.
- [HYPOTHÈSE] Probabilité subjective que `a0bis` réussisse ACQUÉRIR : **≤ 25 %**. La variabilité d'un monde à l'autre (environ 0.005) est du même ordre que le seuil, et 3 hausses sur 4 restent difficiles.
- [HYPOTHÈSE] Si une pièce porte le gain, ce sera d'abord (a), le coût marginal : c'est elle qui rend les requêtes possibles.

## 9. Hors de ce préenregistrement

- Toute retouche de ce texte après résultats. Une envie de retouche est écrite au rapport, pas appliquée.
- La modification d'A0, d'E002 ou d'E002-bis.
- Les séquences entrelacées de familles.
- L'émission d'`HYPOTHÈSE` probabilistes.
- Les étalons LLM.
