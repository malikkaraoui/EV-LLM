# E003 — étalon LLM sur les cas E001 (génère ou déduit ?)

Mandats M0006 puis M0008, 2026-09-26. **État : STOP partiel** (plafond d'appels atteint pendant
l'évaluation, M0008). LLM-2 remplacé par l'Amendement 1 (`PROTOCOLE.md`). Évaluation mesurée
pour 5 questions T1 sur 10 chez LLM-1 et 1 sur 10 chez LLM-2 ; aucune mesure T2 côté LLM.

## Question

§56 v2 du document d'architecture impose un étalon LLM à budget égal. Sur les **mêmes cas, mêmes
attentes** que E001 (`cases.json`, sha256 `8325775b4957bf44664b631ce48096933c6f56d4f245143161405ae6b1e99d0b`,
copié sans modification depuis `origin/exp/e001-sonde-jev`), des LLM génératifs :
1. distinguent-ils T1-A (contradiction) de T1-B (indéterminé) ?
2. sont-ils « faux et sûrs » sur T2 (erreurs invisibles) ?

## Protocole

Préenregistré dans [`PROTOCOLE.md`](PROTOCOLE.md), committé avant le premier appel
(commit `c3e8dd5`). Code : `run_llm.py` (Python standard, zéro dépendance). Tests hors ligne :
`python3 -m unittest -v test_run_llm` (20 tests : parse strict, conforme / faux et sûr,
garde anti-fuite, file de relances, plafond d'appels).

Rejouer (60 appels d'évaluation, plafond 65 depuis l'Amendement 1) :

```
cd research/experiments/E003-etalon-llm
python3 run_llm.py --env-file /Users/malik/Documents/EV-LLM/.env --pilot --max-calls 2   # pilote
python3 run_llm.py --env-file /Users/malik/Documents/EV-LLM/.env                         # évaluation
```

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

## Tableau comparatif

Jev : E001 lancement 2 (M0002) pour T1, lancement 3 (M0003) pour T2. Cellule =
« obtenu (P ou confiance) · n réponses parsées / 3 ». « non mesuré » = aucun 200 exploitable ;
« tronqué » = 200 reçus mais tous coupés par `max_tokens` (`NON_PARSE`).

| cas | question | attendu | Jev (P) | LLM-1 `gpt-4.1-mini` (confiance) | LLM-2 `gemini-2.5-flash` (confiance) |
|---|---|---|---|---|---|
| T1-A | statut | contradiction | contradiction (0.71) · 3/3 | contradiction (1.00) · 3/3 | tronqué · 0/3 |
| T1-A | e_sup_d | true | true (0.51) · 3/3 | **false (1.00) · 3/3 — faux et sûr** | tronqué · 0/3 |
| T1-B | statut | indetermine | indetermine (0.72) · 3/3 | indetermine (0.90) · 3/3 | tronqué · 0/3 |
| T1-B | e_sup_d | true | true (0.73) · 3/3 | true (0.90) · 3/3 | tronqué · 0/3 |
| T1-C | a_sup_c | true | true (0.97) · 1/3 | true (1.00) · 3/3 | true (1.00) · 1/3 |
| T1-C | c_sup_a | false | false (0.02) · 1/3 | non mesuré | non mesuré |
| T2-1 | correcte | false | false (0.08) · 5 | non mesuré | non mesuré |
| T2-2 | correcte | true | true (0.96) · 4 | non mesuré | non mesuré |
| T2-3 | correcte | true | true (0.84) · 2 | non mesuré | non mesuré |
| T2-4 | correcte | false | false (0.08) · 2 | non mesuré | non mesuré |

Pour Jev, P est une probabilité renvoyée par l'API (pour `c_sup_a`, P(true) = 0.02). Pour les LLM,
c'est un nombre écrit par le modèle dans sa réponse (confiance verbalisée).

## Lecture

1. **T1-A et T1-B distingués ?**
   - [VÉRIFIÉ] Jev : oui, 3 répétitions sur 3 (contradiction contre indéterminé).
   - [VÉRIFIÉ] LLM-1 : oui, sur la question `statut`, 3 sur 3, avec une confiance de 1.00 et 0.90.
   - [VÉRIFIÉ] LLM-2 : non mesuré. Les 6 réponses `statut` sont tronquées avant la réponse.
2. **« Faux et sûr » : où ?**
   - [VÉRIFIÉ] Une seule occurrence dans les cellules mesurées : **LLM-1, T1-A `e_sup_d`**. Il répond `false` 3 fois, avec une confiance de 1, 1 et 0.9, alors que l'attendu préenregistré est `true` (E > A > B > C > D donne E > D par la règle 1).
   - [HYPOTHÈSE] LLM-1 semble lire la contradiction (règle 2) comme un interdit de déduire E > D. Le même modèle répond pourtant `contradiction` au `statut` du même cas. Il n'explique pas son raisonnement, donc cette lecture n'est pas vérifiable ici.
   - [VÉRIFIÉ] Jev : 0 « faux et sûr » sur les 10 questions (T1 en M0002, T2 en M0003). Sur T1-A `e_sup_d`, il est juste mais peu sûr (0.51).
   - [VÉRIFIÉ] LLM-2 : 0 sur la seule question mesurée (T1-C `a_sup_c`).
3. **T2 : fautes invisibles détectées ?**
   - [VÉRIFIÉ] Jev : oui sur les 2 fautes (T2-1 et T2-4 jugées incorrectes, P ≤ 0.10) et juste sur les 2 contrôles.
   - [VÉRIFIÉ] LLM-1 et LLM-2 : **aucune mesure T2**. Les appels T2 venaient en fin de file par modèle et n'ont reçu que des 429 avant le plafond.
4. **Limite majeure : la confiance verbalisée n'est pas une probabilité.** [HYPOTHÈSE]
   - Le LLM écrit un nombre sous la consigne du prompt. LLM-1 donne 1.00 à une réponse fausse et 1.00 à des réponses justes : sur ces cas, son nombre ne sépare pas le juste du faux.
   - Jev renvoie une probabilité de sortie. Rien ne garantit que l'une ou l'autre soit calibrée.
   - Le seuil commun de 0.8 est une convention de lecture, pas une équivalence.
5. **Coût et latence** (réponses 200 seulement, `usage.cost` renvoyé par la Gateway) :
   - [VÉRIFIÉ] LLM-1 : 15 réponses, coût total 0.00167, latence médiane 974 ms, 0 token de raisonnement.
   - [VÉRIFIÉ] LLM-2 : 13 réponses, coût total 0.01314, latence médiane 4 500 ms, 272 à 384 tokens de raisonnement par réponse. C'est environ 8 fois le coût de LLM-1 pour 1 réponse exploitable.
   - [VÉRIFIÉ] Jev : latence médiane de 415 à 727 ms en T1 et de 482 à 557 ms en T2 (E001). Le coût de Jev n'est pas relevé dans E001.
   - Unité du coût : [HYPOTHÈSE] dollars US (champ `cost` sans unité dans la réponse).

Aucune conclusion générale : 7 cas, 10 questions, et côté LLM au plus 5 questions mesurées.

## Limites

- 7 cas et 10 questions. Côté LLM, mesure partielle : 5 questions sur 10 pour LLM-1, 1 sur 10 pour LLM-2, et aucune question T2.
- La confiance verbalisée n'est pas une probabilité (point 4 ci-dessus).
- LLM-2 n'est pas un modèle récent (2025-03) : c'est le premier modèle de raisonnement accessible au compte free tier (Amendement 1). L'étalon ne mesure pas l'état de l'art.
- `max_tokens: 400` avec `reasoning.effort: low` est trop court pour LLM-2 sur T1-A et T1-B. Le NON_PARSE mesure la mécanique, pas le raisonnement.
- La limite de 5 requêtes par minute du compte et la relance sans attente font consommer le budget en 429.
- `temperature: 0` et 3 répétitions mesurent la stabilité, pas la calibration.
- Le budget n'est pas égal au sens strict : Jev reçoit un appel par cas, les LLM un appel par question.

## Prochaine étape proposée

1. Rédiger un Amendement 2, committé avant tout appel : `max_tokens` de LLM-2 à relever (ou effort `none`/budget de raisonnement fixé), avec un nouveau budget d'appels. Décision à l'orchestrateur, car le protocole change.
2. Rejouer les questions non mesurées en sous-lancements de 4 appels au plus, séparés par du travail, comme E001-T2 (M0003), pour rester sous 5 requêtes par minute.
3. Compléter le tableau, en priorité T2 (fautes invisibles) et T1-C `c_sup_a`, avant toute lecture comparative Jev/LLM.
