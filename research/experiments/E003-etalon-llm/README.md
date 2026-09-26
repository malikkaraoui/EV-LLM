# E003 — étalon LLM sur les cas E001 (génère ou déduit ?)

Mandats M0006, M0008 puis M0010, 2026-09-26. **État : mesure complète** (M0010). LLM-2 remplacé par
l'Amendement 1 ; `max_tokens` de LLM-2, rythme des appels et rejeu des manquants fixés par
l'Amendement 2 (`PROTOCOLE.md`). 10 questions sur 10 mesurées pour chaque LLM, 3 réponses parsées
par question, T2 compris.

## Question

§56 v2 du document d'architecture impose un étalon LLM à budget égal. Sur les **mêmes cas, mêmes
attentes** que E001 (`cases.json`, sha256 `8325775b4957bf44664b631ce48096933c6f56d4f245143161405ae6b1e99d0b`,
copié sans modification depuis `origin/exp/e001-sonde-jev`), des LLM génératifs :
1. distinguent-ils T1-A (contradiction) de T1-B (indéterminé) ?
2. sont-ils « faux et sûrs » sur T2 (erreurs invisibles) ?

## Protocole

Préenregistré dans [`PROTOCOLE.md`](PROTOCOLE.md), committé avant le premier appel
(commit `c3e8dd5`). Code : `run_llm.py` (Python standard, zéro dépendance). Tests hors ligne :
`python3 -m unittest -v test_run_llm` (27 tests : parse strict, conforme / faux et sûr,
garde anti-fuite, file de relances, plafond d'appels, rythmeur, sélection des manquants,
`max_tokens` de LLM-2).

Rejouer selon l'Amendement 2 (lancements de 8 appels au plus, 26 s entre deux appels, seuls les
éléments sans réponse 200 parsable dans les dossiers donnés) :

```
cd research/experiments/E003-etalon-llm
python3 run_llm.py --pilot --pilot-model google/gemini-2.5-flash --max-tokens-llm2 1200 --max-calls 1 --min-interval 26
python3 run_llm.py --max-tokens-llm2 1200 --min-interval 26 --max-calls 8 --only-missing results/<d1> results/<d2> ...
python3 run_llm.py --summarize-dirs results/<d1> results/<d2> ...   # zéro appel -> results/consolide/
```

`--env-file` vaut `/Users/malik/Documents/EV-LLM/.env` par défaut ; chaque lancement répète
`--only-missing` avec tous les dossiers `results/` déjà produits.

## Pilote M0006 — 2026-09-26 15:57:29 +0200 : STOP

Un appel par modèle, hors `cases.json` (« tout carré est un rectangle », attendu `true`).
Fichiers : [`pilot/2026-09-26T155729+0200/`](pilot/2026-09-26T155729+0200/).

| modèle | HTTP | réponse |
|---|---|---|
| LLM-1 `openai/gpt-4.1-mini` | 200 | `{"reponse": true, "confiance": 1}` : parse strict OK, 15 tokens de sortie, 0 de raisonnement, `finish_reason: stop` |
| LLM-2 `google/gemini-3.8-flash` | **403** | `no_providers_available` : « Free tier users do not have access to this model. Upgrade to paid credits… » |

- [VÉRIFIÉ] La mécanique fonctionne de bout en bout pour LLM-1 : la clé est acceptée, `temperature: 0` et `response_format: json_object` passent, et la réponse sort en JSON strict.
- [VÉRIFIÉ] Le compte est en « free tier » pour la Gateway. `google/gemini-3.8-flash` n'y est pas accessible.
- [HYPOTHÈSE] D'autres modèles de raisonnement du catalogue peuvent aussi être fermés au free tier. Le catalogue `/v1/models` ne dit pas lesquels le sont.
- Le mandat classe 403 en STOP. Aucun autre modèle n'a donc été essayé, et l'évaluation n'a pas été lancée.
- Appels consommés : **2 sur 70** (1×200, 1×403).
- Défaut mineur : `summary.md` du pilote affiche le sha256 de `cases.json` alors que le pilote n'utilise pas ce fichier.

## Amendement 1 (M0008) — pilotes de remplacement de LLM-2

Détail et justification : [`PROTOCOLE.md`](PROTOCOLE.md), section « Amendement 1 (26/09) »,
committée en `9526b7b` à 16:16:17 +0200, **avant** le premier appel d'évaluation (16:16:19).

| # | candidat | HTTP | parse strict |
|---|---|---|---|
| 1 | `alibaba/qwen3.8-flash` | 403 `no_providers_available` (free tier) | — |
| 2 | `zai/glm-5.3-flash` | 403 `no_providers_available` (free tier) | — |
| 3 | `google/gemini-2.5-flash` | **200** | OK (`{"reponse": true, "confiance": 1}`, 204 tokens de raisonnement) |

LLM-2 retenu : `google/gemini-2.5-flash`, `reasoning: {"effort": "low"}`, mêmes autres réglages.

## Évaluation M0008 — 2026-09-26 16:16:19 → 16:17:50 +0200 : STOP partiel (plafond)

`python3 run_llm.py --env-file …/.env --max-calls 65`, `cases.json` sha256 inchangé
(`8325775b…`). Fichiers : [`results/2026-09-26T161619+0200/`](results/2026-09-26T161619+0200/)
(`raw.jsonl` sans en-têtes, `summary.json`, `summary.md`). Sortie : `arret: budget` (code 5).

- [VÉRIFIÉ] **65 appels : 28 × HTTP 200, 37 × HTTP 429.** Par modèle : LLM-1 15 × 200 et 20 × 429 ; LLM-2 13 × 200 et 17 × 429.
- [VÉRIFIÉ] Les 429 disent « this team's limit of 5 requests per minute (per region) was reached ». La limite du compte est de 5 requêtes par minute.
  - La file relance les 429 sans attendre (le protocole interdit `sleep`). Chaque relance est donc repartie aussitôt dans la même minute et a refait un 429.
  - Le plafond de 65 a été atteint avant la fin de la file.
- [VÉRIFIÉ] **LLM-2 : 12 réponses 200 sur 13 sont tronquées** (`finish_reason: length`).
  - Le raisonnement consomme 380 à 384 des 400 tokens de sortie. Le contenu s'arrête sur `{` ou `{"reponse":`.
  - Ces 12 réponses sont `NON_PARSE` (« pas du JSON strict »), sans correction. Le risque était écrit en [HYPOTHÈSE] dans l'Amendement 1 : il s'est réalisé sur T1-A et T1-B.
- Lecture de `summary.md` : une ligne `NON_PARSE` **sans raison** dans `summary.json` (`n_parses: 0`, `non_parse_raisons: []`) veut dire **non mesuré**. La question n'a reçu que des 429 non définitifs avant le plafond. Ce n'est pas une réponse illisible.
- Budget total E003 : 2 (M0006) + 3 (pilotes) + 65 (évaluation) = **70**, soit le budget initial épuisé.

## Amendement 2 (M0010) — 2026-09-26 16:40 → 16:59 +0200 : mesure complète

Détail : [`PROTOCOLE.md`](PROTOCOLE.md), section « Amendement 2 (26/09) ».

- **Pilote** hors évaluation, LLM-2 à `max_tokens` 1200 (`pilot/2026-09-26T164042+0200/`) : [VÉRIFIÉ] HTTP 200, `finish_reason: stop`, `{"reponse": true, "confiance": 1}` passe le parse strict, 204 tokens de raisonnement sur 223.
- **Ordre** : [VÉRIFIÉ] amendement committé en `0da60ac` à 16:41:12 +0200 ; premier appel d'évaluation à 16:41:16 (`results/2026-09-26T164116+0200/raw.jsonl`).
- **Lancements** : 6 lancements rythmés (5 × 8 appels + 1 × 4), dossiers `results/2026-09-26T164116+0200/` à `results/2026-09-26T165817+0200/`. Seuls les 44 éléments manquants ont été joués (LLM-1 15, LLM-2 29), puis la file s'est vidée (code 0).
- [VÉRIFIÉ] **44 appels d'évaluation : 44 × HTTP 200, 0 × 429.** Avec le pilote, 45 appels nouveaux sur un budget de 50.
- [VÉRIFIÉ] **Intervalles entre débuts d'appels** (`interval_s`) : min 26,0 s, médiane 26,0 s. Le seul intervalle hors série (1 406 s) sépare le premier appel M0010 du dernier appel M0008.
- [VÉRIFIÉ] **LLM-2 non tronqué** : 29 réponses sur 29 en `finish_reason: stop`, raisonnement de 274 à 767 tokens. En M0008, la limite de 400 coupait le raisonnement à 380–384 tokens ; il en fallait jusqu'à 767 sur T1-A et T1-B.
- `cases.json` inchangé (sha256 `8325775b…`), règle inchangée, code non modifié après le premier appel.
- **Résumé consolidé** : [`results/consolide/summary.md`](results/consolide/summary.md) (M0008 + M0010 ; 109 appels : 72 × 200, 37 × 429 tous en M0008). Les 12 réponses tronquées de LLM-2 en M0008 y figurent comme raisons `NON_PARSE` historiques ; chaque question a 3 réponses parsées.

## Tableau comparatif

Jev : E001 (README sur `origin/main`), lancement 2 (M0002) pour T1, lancement 3 (M0003) pour T2.
LLM : résumé consolidé M0008 + M0010. Cellule = « obtenu (P ou confiance) · n réponses utiles ».

| cas | question | attendu | Jev (P) | LLM-1 `gpt-4.1-mini` (confiance) | LLM-2 `gemini-2.5-flash` (confiance) |
|---|---|---|---|---|---|
| T1-A | statut | contradiction | contradiction (0.71) · 3/3 | contradiction (1.00) · 3/3 | contradiction (1.00) · 3/3 |
| T1-A | e_sup_d | true | true (0.51) · 3/3 | **false (1.00) · 3/3 — faux et sûr** | true (0.90) · 3/3 |
| T1-B | statut | indetermine | indetermine (0.72) · 3/3 | indetermine (0.90) · 3/3 | indetermine (1.00) · 3/3 |
| T1-B | e_sup_d | true | true (0.73) · 3/3 | true (0.90) · 3/3 | true (1.00) · 3/3 |
| T1-C | a_sup_c | true | true (0.97) · 1/3 | true (1.00) · 3/3 | true (1.00) · 3/3 |
| T1-C | c_sup_a | false | false (0.02) · 1/3 | false (1.00) · 3/3 | false (1.00) · 3/3 |
| T2-1 | correcte | false | false (0.08) · 5 | false (0.99) · 3/3 | false (1.00) · 3/3 |
| T2-2 | correcte | true | true (0.96) · 4 | true (0.99) · 3/3 | true (1.00) · 3/3 |
| T2-3 | correcte | true | true (0.84) · 2 | true (0.95) · 3/3 | true (1.00) · 3/3 |
| T2-4 | correcte | false | false (0.08) · 2 | false (0.95) · 3/3 | false (1.00) · 3/3 |

Sens des nombres : pour Jev, P est une probabilité renvoyée par l'API, P(true) pour une question
booléenne (0.08 sur T2-1 = « incorrecte » à 0.92). Pour les LLM, c'est la confiance **verbalisée**
dans la réponse donnée (0.99 sur T2-1 = « false, sûr à 0.99 »). Les deux colonnes ne se lisent
donc pas de la même façon.

Conformité : Jev 10/10, LLM-1 9/10, LLM-2 10/10 (médiane ou majorité des répétitions).

## Lecture

1. **T1-A et T1-B distingués ?**
   - [VÉRIFIÉ] Oui pour les trois systèmes, 3 répétitions sur 3 : `contradiction` quand la règle 2 est donnée, `indetermine` quand elle est absente.
   - [VÉRIFIÉ] Confiances : Jev 0.71 / 0.72, LLM-1 1.00 / 0.90, LLM-2 1.00 / 1.00.
   - Sur ces deux cas, aucun des trois ne montre l'indice « génère au lieu de déduire » (même réponse aux deux variantes).
2. **« Faux et sûr » : où ?**
   - [VÉRIFIÉ] Une seule question sur 30 (3 systèmes × 10) : **LLM-1, T1-A `e_sup_d`**, `false` 3 fois sur 3, confiance 1, 1 et 0.9 (3 répétitions « faux et sûr »). L'attendu préenregistré est `true` (E > A > B > C > D donne E > D par la règle 1).
   - [VÉRIFIÉ] Jev : 0 sur 10. LLM-2 : 0 sur 10.
   - [VÉRIFIÉ] Sur la même question, Jev est juste mais à P = 0.51 (0.49–0.58), contre 0.73 sur T1-B où la déduction est identique. LLM-2 est juste à 0.90 sur T1-A, contre 1.00 sur T1-B.
   - [HYPOTHÈSE] Même contamination que chez Jev (issue #5, E004) : la contradiction présente dans l'état pèse sur une déduction qui n'en dépend pas. Chez Jev, elle baisse P sans la faire basculer ; chez LLM-1, elle fait basculer la réponse ; chez LLM-2, elle baisse la confiance verbalisée de 1.00 à 0.90. Trois systèmes, une question, 3 répétitions : cela ne l'établit pas. Seules des paires contrôlées (E004) le peuvent.
   - [HYPOTHÈSE] Autre lecture possible pour LLM-1 : il traite la règle 2 comme un interdit de déduire. Il ne justifie pas sa réponse, donc les deux lectures ne se départagent pas ici.
3. **T2 : fautes invisibles détectées ?**
   - [VÉRIFIÉ] Oui pour les trois systèmes : T2-1 (« il a manger ») et T2-4 (« ils sont tombé ») jugées incorrectes, T2-2 et T2-3 jugées correctes, 3 répétitions sur 3 pour chaque LLM.
   - [VÉRIFIÉ] Sur T2, aucune erreur donc aucun « faux et sûr », pour aucun des trois.
   - [HYPOTHÈSE] Ces deux fautes sont fréquentes en français et ne piègent aucun des trois systèmes. T2 ne départage donc pas Jev des LLM ; il faudrait des fautes plus rares ou ambiguës (proposition E001).
4. **Limite majeure : la confiance verbalisée n'est pas une probabilité.** [HYPOTHÈSE]
   - [VÉRIFIÉ] LLM-1 écrit 1.00 sur sa réponse fausse comme sur des réponses justes. LLM-2 écrit 1.00 sur 9 questions sur 10. Sur ces cas, le nombre verbalisé ne sépare pas le juste du faux.
   - [VÉRIFIÉ] Les confiances des LLM restent toutes entre 0.90 et 1.00. Jev est le seul des trois à descendre nettement sur un cas où il a raison (0.51 sur T1-A `e_sup_d`, 0.84 sur T2-3).
   - Rien ne garantit que l'une ou l'autre sorte soit calibrée ; le seuil commun de 0.8 est une convention de lecture, pas une équivalence.
5. **Coût et latence** (réponses parsées, `usage.cost` de la Gateway, M0008 + M0010) :
   - [VÉRIFIÉ] LLM-1 : 30 réponses, coût 0.00294 au total (≈ 0.000098 par réponse), latence médiane 989 ms (767–3 076).
   - [VÉRIFIÉ] LLM-2 : 30 réponses, coût 0.0358 (≈ 0.0012 par réponse), latence médiane 5 038 ms (2 932–8 549). Avec les 12 réponses tronquées de M0008, 0.0482 dépensés au total pour LLM-2.
   - [VÉRIFIÉ] LLM-2 coûte environ 12 fois LLM-1 par réponse exploitable et répond environ 5 fois plus lentement ; son raisonnement prend 274 à 767 tokens.
   - [VÉRIFIÉ] Jev : latence médiane 415 à 727 ms en T1, 482 à 557 ms en T2 ; coût observé ≈ 0.00002 par appel (E001, `gateway.cost`), un appel couvrant toutes les questions d'un cas.
   - Unité du coût : [HYPOTHÈSE] dollars US (champ `cost` sans unité).

Aucune conclusion générale : 7 cas, 10 questions, 3 répétitions à `temperature: 0`.

## Limites

- 7 cas et 10 questions, états en français.
- La confiance verbalisée n'est pas une probabilité (point 4 ci-dessus).
- LLM-2 n'est pas un modèle récent (2025-03) : c'est le premier modèle de raisonnement accessible au compte free tier (Amendement 1). L'étalon ne mesure pas l'état de l'art.
- La réponse LLM-2 de T1-C `a_sup_c` répétition 1 date de M0008 (`max_tokens` 400, non tronquée) ; les 29 autres réponses LLM-2 sont à `max_tokens` 1200 (Amendement 2).
- Les réponses LLM viennent de deux mandats (M0008, M0010) ; LLM-1 a les mêmes réglages dans les deux.
- `temperature: 0` et 3 répétitions mesurent la stabilité, pas la calibration.
- Le budget n'est pas égal au sens strict : Jev reçoit un appel par cas, les LLM un appel par question. Jev T1-C et T2-3/T2-4 reposent sur 1 ou 2 réponses (E001).

## Prochaine étape proposée

1. E004 (issue #5) : paires contrôlées pour la contamination d'une déduction indépendante par une contradiction, avec Jev, LLM-1 et LLM-2 — seul cas où les trois systèmes se séparent ici.
2. T2 élargi à des fautes rares ou ambiguës (préenregistré), où un « faux et sûr » a une chance d'apparaître.
3. Pour les LLM, une mesure de confiance non verbalisée (log-probabilités si l'API les expose) avant toute comparaison de calibration avec Jev.
