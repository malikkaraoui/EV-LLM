# E002-bis — Préenregistrement : réparer la mesure

Mandat M0007, 2026-09-26. **Figé avant tout code d'évaluation de ce dossier.** Rien ici ne se modifie après avoir vu un résultat : un écart entre ce texte et ce qu'on observe est un résultat, pas une correction.

## 0. Pourquoi un E002-bis

E002 (`research/experiments/E002-relations-opaques/`, tip `1cb586b`) reste **tel quel** : c'est un résultat. Son constat [VÉRIFIÉ, rapport M0005] : sous le bruit préenregistré (5–10 % d'observations fausses), le plafond « savoir » (oracle-propriétés) a R ≤ 0 sur 12 mondes sur 20. `R̂ = R / R_plafond` y est indéfini, donc le critère ACQUÉRIR d'E002 §3 est inopérant : aucun système ne peut réussir ni échouer de façon informative.

E002-bis répare **la mesure**, pas le banc :
- (a) une vitesse **toujours définie** : `R̂_diff = R − R_plafond` ;
- (b) un **plafond qui vérifie** ses prémisses par requête, et qui devrait rester R > 0 sous bruit (prédiction à tester, pas un acquis) ;
- **le bruit n'est pas baissé.**

## 1. Ce qui est repris d'E002 sans modification

Importé depuis `../E002-relations-opaques/` (ajout au `sys.path`, aucune copie de logique, **aucun fichier d'E002 modifié**) :
- générateur `monde.generer_monde` : mêmes paramètres (n = 8, k = 5, 96 observations en 2 phases, 60 atomes tenus à l'écart, 20 questions de révision, 3 d'exclusion) ;
- **même bruit** : taux uniforme dans [5 %, 10 %] par monde, dont une inversion ciblée en phase 2 (E002 §1.6) ;
- **mêmes graines : 1 à 20**, mêmes familles (`(graine − 1) // 5`), même ordre 1 → 20, même correction en fin de monde ;
- oracle, étiquettes attendues, exactitude, preuves valides (E002 §2) ;
- environnement interactif et coût d'une requête : `C_atome = log2 5 + 7 ≈ 9.32 bits`, une requête coûte comme une observation (E002 §1.7, §4) ;
- **R en bits** : bits économisés sur les 60 atomes tenus à l'écart contre le prédicteur de Laplace, divisés par les bits d'expérience requêtes comprises ; ε = 1/64 (E002 §4) ;
- étalons **aléatoire**, **oracle-propriétés** et **découvreur naïf**, tels quels (E002 §6) ;
- métriques par monde d'E002 §5 (calculées par `evaluer.evaluer_monde` d'E002).

## 2. Nouvel étalon : plafond-vérificateur

On lui **donne** les vraies propriétés et la sémantique (comme à l'oracle-propriétés). Il ne garde rien d'un monde à l'autre. À chaque phase :

1. il ajoute les observations de la phase à ses faits connus ;
2. il répond à toutes les questions par le même chaînage de Horn que l'oracle (E002 §2.2), sur ses faits connus, la requête primant sur l'observation ;
3. il rassemble les **prémisses** (faits connus cités dans la preuve) de chacune de ses réponses `DÉDUIT` et `CONTRADICTION` ; toute prémisse qui n'a pas encore été demandée est **demandée** au monde (ordre trié, déterministe) ; la réponse du monde (vérité, sans bruit) remplace l'observation ;
4. il reprend en 2 tant qu'une prémisse citée n'a pas été vérifiée ; il rend les réponses du dernier passage.

Pas de budget de requêtes : au pire il redemande les 96 atomes observés. Les requêtes sont facturées au même prix qu'une observation. Toute prémisse d'une réponse `DÉDUIT`/`CONTRADICTION` rendue est donc un atome **demandé** (propriété du processus, testée — §6).

Conséquence connue d'avance, par construction : sur un monde **sans** bruit, il rend exactement les mêmes réponses que l'oracle-propriétés (les requêtes confirment les observations), donc les mêmes bits économisés ; son R y est plus bas, du seul coût de ses requêtes. « Jamais pire que le plafond sur un monde sans bruit » s'entend donc ainsi : **réponses identiques et bits économisés ≥** ceux de l'oracle-propriétés. C'est ce qui est testé.

## 3. Mesure de vitesse : R̂_diff

- **Plafond de référence** : le **plafond-vérificateur**. `R̂_diff(w) = R_système(w) − R_plafond-vérificateur(w)`, en bits économisés par bit d'expérience. Toujours défini. Négatif = en dessous du plafond.
- Rapporté en secondaire : `R − R_oracle-propriétés`.
- Le `R̂` quotient d'E002 n'est plus utilisé.

## 4. Critère ACQUÉRIR reformulé (courbe monde n → n+1 par famille)

- **Accélération dans une famille** (5 mondes consécutifs) : `R̂_diff(5e) − R̂_diff(1er) ≥ 0.005` **et** au moins 3 des 4 transitions n → n+1 ont `ΔR̂_diff > 0`.
  - Seuil 0.005 : environ un tiers du R moyen du plafond **sans bruit** mesuré dans E002 (+0.016, diagnostic hors protocole connu avant ce texte). Fixé ici, pas après.
- **Échec d'un système (ACQUÉRIR)** : moins de 3 familles sur 4 montrent une accélération.
- **Contrôle du critère** : les quatre étalons ne gardent rien d'un monde à l'autre ; ils **doivent** échouer. Si l'un réussit, le critère est déclaré trop permissif (constaté, **pas** corrigé). Le plafond-vérificateur a `R̂_diff ≡ 0` par définition : il échoue trivialement (aucune hausse).

## 5. Critère d'échec de la mesure elle-même

**Si le plafond-vérificateur a encore R ≤ 0 sur ≥ 5 mondes sur 20, la mesure est déclarée NON RÉPARÉE.** (R = 0 exactement compte comme R ≤ 0 : un plafond qui ne gagne rien n'est pas un plafond.) Dans ce cas, le verdict ACQUÉRIR des étalons est rapporté mais déclaré non informatif.

Sinon (≤ 4/20), la mesure est déclarée réparée **pour ce banc et ce jeu de paramètres**, et rien de plus.

## 6. Tests (unittest, stdlib)

- `R̂_diff` sur un exemple calculé à la main (R système et R plafond donnés) et critère d'accélération sur des séries écrites à la main ;
- plafond-vérificateur jamais pire que l'oracle-propriétés sur les 20 mondes **débruités** (réponses identiques, bits économisés ≥) ;
- processus : sur les mondes bruités, chaque prémisse de chaque `DÉDUIT`/`CONTRADICTION` rendu en phase 2 est un atome demandé ;
- déterminisme : deux exécutions de la suite donnent des résultats identiques.

## 7. Exécution

20 mondes × 4 étalons (aléatoire, oracle-propriétés, plafond-vérificateur, découvreur naïf), sorties `results/<horodatage>/resultats.json` et `summary.md`, committées.

## 8. Attentes (avant exécution)

- [HYPOTHÈSE] Plafond-vérificateur : 0 `DÉDUIT` faux en vérité (prémisses vraies + règles vraies) ; exactitude d'étiquette 1.000 par construction ; R > 0 sur au moins 16 mondes sur 20 ; mesure réparée au sens du §5. Risque identifié : un monde où il ne déduit **aucun** atome tenu à l'écart a R = 0 exactement.
- [HYPOTHÈSE] Son R moyen est inférieur au R sans bruit de l'oracle-propriétés dans E002 (+0.016), à cause du coût des requêtes.
- [HYPOTHÈSE] Oracle-propriétés et découvreur naïf : `R̂_diff` < 0 en moyenne. Aléatoire : le plus négatif.
- [HYPOTHÈSE] Aucun des quatre étalons ne montre d'accélération (§4).

## 9. Hors de ce préenregistrement

L'architecture candidate, un découvreur qui pèse la fiabilité des observations, les étalons LLM et réseau (§56 v2), toute modification du bruit ou du coût d'une requête.
