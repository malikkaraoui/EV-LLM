# E002 — Préenregistrement : chambre aux relations opaques

Mandat M0005, 2026-09-26. **Figé avant tout code d'évaluation.** Rien ici ne se modifie après avoir vu un résultat : un écart entre ce texte et ce qu'on observe est un résultat, pas une correction à faire.

Références : `architecture_cognitive_post_transformer.md` §1 bis v2.1, §11 v2, §14 v2, §28 v2, §29 v2 et v2.1, §56 v2, §63 (D4, D6, D7, D14).

Ce banc est le **Test 2 — ACQUÉRIR** du §29 v2.1 : les propriétés des relations ne sont pas données, le système doit les découvrir, puis résoudre le monde suivant plus vite. Ce préenregistrement couvre le **banc** et les **trois étalons**. Il ne porte pas encore sur une architecture candidate.

---

## 1. Le monde

### 1.1 Taille

| paramètre | valeur |
|---|---|
| entités par monde | n = 8, noms opaques tirés à chaque monde (`o` + 3 chiffres) |
| relations par monde | k = 5, nommées `R1…R5` ; l'attribution nom → type est tirée à chaque monde |
| atomes possibles | k · n² = 320 (les atomes réflexifs `R(x,x)` en font partie) |

### 1.2 Propriétés possibles d'une relation

Elles sont **mesurées sur la vérité terrain** du monde, jamais supposées d'après le générateur.

| propriété | définition |
|---|---|
| réflexive | ∀x R(x,x) |
| symétrique | ∀x,y R(x,y) ⇒ R(y,x) |
| antisymétrique | ∀x≠y ¬(R(x,y) ∧ R(y,x)) |
| transitive | ∀x,y,z R(x,y) ∧ R(y,z) ⇒ R(x,z) |
| composition | `Ri∘Rj = Rk` (égalité exacte sur la vérité, i, j, k distincts, Ri∘Rj non vide) |
| **aucune** | aucune des quatre premières (et n'entre dans aucune composition) |

### 1.3 Générateurs (types)

| type | propriétés visées | construction | piège ? |
|---|---|---|---|
| `ORDRE` | transitive, antisymétrique | DAG aléatoire (arête i→j, i<j dans un rang tiré, p = 0.35) puis fermeture transitive ; ordre partiel | non |
| `ORDRE_LARGE` | réflexive, transitive, antisymétrique | `ORDRE` + diagonale | non |
| `EQUIVALENCE` | réflexive, symétrique, transitive | partition aléatoire en 2 à 4 classes | non |
| `SYM_PIEGE` (« ami de », « adjacent à ») | symétrique, non transitive | graphe non orienté aléatoire, p = 0.35, sans boucle | **oui** |
| `CYCLE_PIEGE` (pierre-feuille-ciseaux) | antisymétrique, non transitive | classes mod 3 ; R(x,y) ⇔ classe(y) = classe(x) + 1 mod 3 | **oui** |
| `AUCUNE_PIEGE` | aucune | relation aléatoire p = 0.3, retirée jusqu'à n'avoir aucune des 4 propriétés | **oui** |
| `COMPOSEE` | celles que la vérité donne | `R_slot5 = R_i ∘ R_j`, i ≠ j parmi les 4 premières | selon vérité |

Validité d'une instance (sinon nouveau tirage, déterministe) : chaque relation est non vide et non pleine ; chaque piège a un **témoin de non-transitivité** dans la vérité ; une `COMPOSEE` est non vide et différente de ses composantes ; en variante A (§1.5), la relation d'ordre désignée a au moins 3 paires incomparables.

### 1.4 Familles, profils, graines

- **Graines : 1 à 20.** Famille `f = (graine − 1) // 5` : graines 1–5 → famille 0, 6–10 → 1, 11–15 → 2, 16–20 → 3.
- Le **profil** d'une famille (multiset des 5 types, structure de la composition, variante de sémantique) est tiré avec la graine `1000 + f`. Les **instances** (entités, graphes, noms, observations, bruit, questions) sont tirées avec la graine du monde.
- Donc, au sein d'une famille, les 5 mondes ont **les mêmes propriétés sous d'autres noms** : c'est la définition opératoire du **transfert** (§3).
- Tirage du profil : 4 types de base uniformes parmi les 6 types non composés ; 5e emplacement : `COMPOSEE` avec probabilité 0.5, sinon un 6e type uniforme. Contrainte : **au moins 2 pièges sur 5 (40 %)**, profil retiré sinon.
- **Proportion minimale de relations non transitives : ≥ 30 %**, vérifiée sur la vérité monde par monde (et donc sur la suite).

### 1.5 Sémantique écrite : l'exclusion

Chaque monde publie au système 3 faits `exclut(x,y)` (paires non ordonnées, x ≠ y) et **une sémantique écrite**, donnée au système en clair :

- **Variante A** (familles 0 et 2) : « `exclut(x,y) ⇒ ni Ro(x,y) ni Ro(y,x)` », où `Ro` est une relation de type `ORDRE` ou `ORDRE_LARGE` nommée dans la sémantique. Le profil d'une famille A contient forcément un tel type. Les paires exclues sont tirées parmi les paires **incomparables** de `Ro` dans la vérité : le monde vrai est cohérent.
- **Variante B** (familles 1 et 3) : « aucune règle ne relie `exclut` aux relations `R1…R5` ». Paires tirées uniformément.

C'est le Test 1 A/B du §29 v2.1 plongé dans la chambre : mêmes types de faits, les réponses **doivent** différer.

La sémantique écrite fait partie de l'**a priori** (budget « génome », D8) : elle ne coûte pas de bits d'expérience.

### 1.6 Observations, bruit, questions

- Les 320 atomes sont mélangés. Les **60 premiers** forment l'ensemble **tenu à l'écart** (questions de prédiction). Ils ne sont jamais observés et **ne peuvent pas être demandés** (requête refusée, journalisée, non facturée).
- Les **96 suivants (30 %)** sont observés avec leur valeur (vrai/faux) : 64 en **phase 1**, 32 en **phase 2** (information tardive, §29 « E > A »).
- **Bruit** : taux tiré uniformément dans **[5 %, 10 %]** par monde ; `round(taux × 96)` observations ont leur valeur inversée. **Une** de ces inversions est **ciblée** et placée en phase 2 : elle est choisie (ordre déterministe) pour créer une contradiction dérivable avec les vraies propriétés (en variante A, de préférence sur une paire exclue). Les autres sont uniformes. Les observations bruitées sont étiquetées **dans l'oracle seulement**.
- **Questions posées au système** (fixées à la création du monde, identiques aux deux phases) :
  1. les 60 atomes tenus à l'écart ;
  2. 20 atomes **de révision** pris parmi les observés : tous les atomes observés impliqués dans une contradiction (au plus 5), complétés au hasard ;
  3. 3 questions d'**exclusion** : « `exclut(x,y)` est-il compatible avec ce que tu sais ? ».

### 1.7 Requêtes

Le système peut demander `Ri(x,y) ?` à tout moment. Le monde répond **la vérité, sans bruit**. Une réponse à une requête **prime** sur une observation du même atome : le monde vérifie (§11 v2, piste 1).

---

## 2. Les réponses et leur vérité attendue

### 2.1 Les quatre étiquettes

Toute réponse porte exactement une étiquette :

| étiquette | contenu obligatoire | sens |
|---|---|---|
| `DÉDUIT` | valeur (vrai/faux) + **preuve** : prémisses (faits connus) et règles citées | découle des faits connus et de règles |
| `HYPOTHÈSE` | valeur + probabilité `p_vrai` | pari assumé, non démontré |
| `CONTRADICTION` | **règle violée citée** + prémisses | les faits connus et les règles imposent à la fois l'atome et sa négation |
| `INDÉTERMINÉ` | **ce qui manque** (texte non vide) | rien ne permet de trancher |

Pour une question d'exclusion, la « valeur » vaut *compatible*.

### 2.2 Ce que l'oracle attend

L'attendu est calculé à partir des **faits connus du système** (observations reçues jusqu'à la phase courante + réponses à ses requêtes, la requête primant) et des **vraies propriétés** : c'est ce qu'un système qui aurait parfaitement acquis les propriétés pourrait dire, **pas** la vérité terrain. La vérité terrain sert à R (§4).

Toutes les règles sont des clauses de Horn : réflexivité (fait), symétrie, transitivité, composition (sens `Ri∘Rj ⊆ Rk` seulement ; le sens `⊇` est existentiel et n'est pas utilisé), antisymétrie (clause négative), observation négative (clause négative), exclusion A (clause négative). Soit `M` le plus petit modèle des faits positifs connus par chaînage avant, et `V(M)` l'ensemble des clauses négatives violées dans `M`.

- **atome q** :
  - q ∈ M et q figure dans une clause violée de `V(M)` → `CONTRADICTION` (règle de cette clause) ;
  - q ∈ M sinon → `DÉDUIT vrai` ;
  - q ∉ M et `V(M ∪ {q})` contient une violation absente de `V(M)` → `DÉDUIT faux` ;
  - sinon → `INDÉTERMINÉ`.
- **exclusion `exclut(x,y)`** :
  - variante A : `Ro(x,y)` ou `Ro(y,x)` ∈ M → `CONTRADICTION` (règle d'exclusion A) ; sinon `DÉDUIT compatible` ;
  - variante B : `INDÉTERMINÉ` (« il manque une règle reliant `exclut` à `R1…R5` »).

Cas de référence (tests unitaires, écrits à la main) : A>B, B>C, C>D, E>A avec `>` transitif et antisymétrique. Avec `exclut(E,D)` : en variante A, la question d'exclusion attend `CONTRADICTION` (preuve E>A>B>C>D) et l'atome `>(E,D)` attend `CONTRADICTION` ; en variante B, la question d'exclusion attend `INDÉTERMINÉ` et l'atome `>(E,D)` attend `DÉDUIT vrai`.

### 2.3 Exactitude d'une réponse

- attendu `DÉDUIT v` : juste ssi réponse `DÉDUIT v` ;
- attendu `CONTRADICTION` : juste ssi réponse `CONTRADICTION` ;
- attendu `INDÉTERMINÉ` : juste ssi réponse `INDÉTERMINÉ` **ou** `HYPOTHÈSE` (un pari déclaré comme tel n'est pas une faute d'étiquette ; sa valeur est jugée par R).
- **`DÉDUIT` infondé** (l'erreur invisible du §1 bis) : réponse `DÉDUIT` alors que l'attendu n'est pas `DÉDUIT` de même valeur.
- **Preuve valide** (`DÉDUIT`, `CONTRADICTION`) : toutes les prémisses sont des faits connus du système, toutes les règles citées sont de vraies propriétés du monde, et la conclusion découle des seules prémisses et règles citées selon §2.2.

---

## 3. Transfert et critère d'échec

- **Transfert** : le monde n+1 d'une famille réutilise **les mêmes propriétés** que le monde n, sous d'autres noms de relations, d'autres entités, d'autres graphes. Le système est **un seul objet** qui traverse les 20 mondes dans l'ordre 1 → 20 ; il reçoit à la fin de chaque monde une **correction** (valeur vraie et étiquette attendue de chaque question). Il peut s'en servir ou non.
- **Mesure de vitesse** : `R̂(w) = R_système(w) / R_plafond(w)` (fraction du plafond « savoir » atteinte, ce qui neutralise la difficulté propre du monde). Secondaire : bits de requêtes consommés.
- **Accélération dans une famille** : `R̂(5e) − R̂(1er) ≥ 0.05` **et** au moins 3 des 4 transitions n → n+1 ont `ΔR̂ > 0`.
- **Critère d'échec d'un système (ACQUÉRIR)** : moins de 3 familles sur 4 montrent une accélération. Autrement dit, un système échoue dès que deux séries de 5 mondes consécutifs ne s'accélèrent pas.
- **Contrôle du critère** : les trois étalons ne gardent rien d'un monde à l'autre ; ils **doivent** échouer. Si l'un d'eux réussit, le critère est déclaré trop permissif (constaté au rapport, **pas** corrigé après coup).

---

## 4. Métrique R en bits (§28 v2)

- **Coût d'un atome d'expérience** (observation **ou** réponse à une requête) : `C_atome = log2(k) + 2·log2(n) + 1 = log2 5 + 7 ≈ 9.32 bits` (quel atome, puis sa valeur). Une requête coûte autant qu'une observation : choix conservateur, le journal d'expérience décrit les deux de la même façon.
- **Coût d'un fait d'exclusion** : `log2(n(n−1)/2) = log2 28 ≈ 4.81 bits`.
- **Bits d'expérience** = observations (2 phases) + requêtes acceptées + exclusions.
- **Prédicteur de référence** (« sans structure ») : pour la relation r, `p_ref(r) = (positifs observés + 1) / (observés + 2)` sur les observations bruitées (Laplace).
- **Probabilité du système** sur un atome tenu à l'écart, réponse de phase 2 : `DÉDUIT v` → `1 − ε` pour v (ε = 1/64, soit 6 bits de pénalité en cas d'erreur) ; `HYPOTHÈSE` → `p_vrai` fourni, borné à [ε, 1 − ε] ; `INDÉTERMINÉ` et `CONTRADICTION` → `p_ref`.
- **Bits économisés** = Σ sur les 60 atomes tenus à l'écart de `[−log2 p_ref(vérité)] − [−log2 p_sys(vérité)]`. Peut être négatif.
- **R = bits économisés / bits d'expérience.**

Déduire mille évidences ne rapporte rien ici : seuls comptent les atomes jamais vus, jamais demandables.

---

## 5. Métriques rapportées par monde et par système

Exactitude par étiquette attendue ; précision et rappel de `CONTRADICTION` et de `INDÉTERMINÉ` ; taux de `DÉDUIT` infondés ; taux de preuves valides ; exactitude sur les questions d'exclusion (A/B) ; requêtes (nombre, bits) ; bits d'expérience ; bits économisés ; R ; R̂ ; **révision** : parmi les questions dont l'attendu change entre phase 1 et phase 2, part où le système donne la bonne réponse en phase 2 (**révision requise**) ; parmi celles dont l'attendu ne change pas, part où le système change quand même de réponse (**sur-révision**) ; propriétés crues vs vraies quand le système les expose.

---

## 6. Étalons (§56 v2)

1. **Aléatoire** (plancher) : étiquette uniforme parmi les 4, valeur uniforme, `p_vrai` uniforme. Aucune requête.
2. **Oracle-propriétés** (plafond « savoir ») : on lui **donne** les vraies propriétés et la sémantique ; il raisonne sur ses observations par le même chaînage de Horn que l'oracle. Aucune requête. Ses étiquettes égalent l'attendu **par construction** : son rôle est de fixer le plafond de R, pas de prouver quoi que ce soit.
3. **Découvreur naïf** (premier étalon « acquérir ») : ne connaît pas les propriétés. Pour chaque relation, il teste par **requêtes seulement** (pas d'observation dans la décision, pour ne pas hériter du bruit) : réflexivité sur 3 entités ; symétrie et antisymétrie à partir de 3 paires observées positives (il redemande la paire et son inverse) ; transitivité sur 3 chaînes observées (il redemande les 3 atomes) ; composition pour les triplets soutenus par les observations (3 chaînes). Une propriété est **réfutée au premier contre-exemple** et **acceptée après 3 confirmations** sans contre-exemple ; sinon, inconnue et non utilisée. Budget : 150 requêtes par monde. Il raisonne ensuite comme le plafond avec **ses** propriétés crues, et cite ces propriétés dans ses preuves. **Il ne garde rien** d'un monde à l'autre.

---

## 7. Attentes (avant exécution)

- [HYPOTHÈSE] Plafond : 100 % d'exactitude d'étiquette par construction ; R > 0 ; 0 requête.
- [HYPOTHÈSE] Aléatoire : R < 0 (ses `DÉDUIT` faux coûtent 6 bits chacun).
- [HYPOTHÈSE] Découvreur naïf : R entre les deux ; des `DÉDUIT` infondés quand il accepte une propriété fausse après 3 confirmations chanceuses ; plus de bits d'expérience que le plafond (ses requêtes).
- [HYPOTHÈSE] Aucun des trois étalons ne montre d'accélération au sens du §3 : ce sont les points de comparaison d'un système **sans mémoire**.

## 8. Ce qui est hors de ce préenregistrement

L'architecture candidate, un étalon LLM et un étalon réseau (TRM/GNN) du §56 v2, les valeurs N, X, Y, Z du §56 v2 (décision de Malik).
