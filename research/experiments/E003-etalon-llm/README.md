# E003 — étalon LLM sur les cas E001 (génère ou déduit ?)

Mandat M0006, 2026-09-26. **État : STOP avant évaluation** (HTTP 403 sur LLM-2 au pilote).
Aucun appel d'évaluation n'a été fait. Les colonnes LLM du tableau ci-dessous sont vides.

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

Rejouer (60 appels d'évaluation, plafond 68) :

```
cd research/experiments/E003-etalon-llm
python3 run_llm.py --env-file /Users/malik/Documents/EV-LLM/.env --pilot --max-calls 2   # pilote
python3 run_llm.py --env-file /Users/malik/Documents/EV-LLM/.env                         # évaluation
```

## Pilote — 2026-09-26 15:57:29 +0200 : STOP

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

## Tableau comparatif (à remplir au lancement d'évaluation)

Jev : E001 lancement 2 (M0002), **seul T1 est mesuré**. Case vide = non mesuré.

| cas | question | attendu | Jev obtenu (P) | LLM-1 obtenu (confiance) | LLM-2 obtenu (confiance) |
|---|---|---|---|---|---|
| T1-A | statut | contradiction | contradiction (0.71) | — | — |
| T1-A | e_sup_d | true | true (0.51) | — | — |
| T1-B | statut | indetermine | indetermine (0.72) | — | — |
| T1-B | e_sup_d | true | true (0.73) | — | — |
| T1-C | a_sup_c | true | true (0.97) | — | — |
| T1-C | c_sup_a | false | false (0.02) | — | — |
| T2-1 | correcte | false | — | — | — |
| T2-2 | correcte | true | — | — | — |
| T2-3 | correcte | true | — | — | — |
| T2-4 | correcte | false | — | — | — |

## Lecture

1. **T1-A et T1-B distingués ?** [VÉRIFIÉ] Pas de mesure LLM. Jev les distingue sur 3 répétitions sur 3 (E001).
2. **« Faux et sûr » : où ?** [VÉRIFIÉ] Pas de mesure LLM. Chez Jev, aucun cas sur les 6 questions T1 mesurées, et T2 n'est pas mesuré.
3. **La confiance verbalisée d'un LLM est-elle comparable à la probabilité de Jev ?** [HYPOTHÈSE] Non.
   - Le LLM écrit un nombre dans du texte généré, sous la consigne du prompt. Jev renvoie une probabilité par l'API.
   - Rien ne garantit que l'une ou l'autre soit calibrée.
   - Le seuil commun de 0.8 pour « faux et sûr » est une convention, pas une équivalence.
   - C'est une limite majeure de toute comparaison E001/E003.

## Limites

- 7 cas et 10 questions : aucune conclusion générale possible, même après le lancement.
- La confiance verbalisée n'est pas une probabilité (point 3 ci-dessus).
- `temperature: 0` et 3 répétitions mesurent la stabilité, pas la calibration.
- Le budget n'est pas égal au sens strict : Jev reçoit un appel par cas, les LLM un appel par question.
- Accès Gateway en free tier : le choix des modèles dépend du compte, pas seulement de la science.

## Prochaine étape proposée

1. Arbitrer LLM-2 : ouvrir des crédits payants, ou choisir un modèle de raisonnement accessible en free tier. Dans ce dernier cas, un seul pilote de vérification, et la modification est committée dans `PROTOCOLE.md` avant l'évaluation.
2. Lancer l'évaluation (60 appels, plafond 68) et remplir le tableau ci-dessus.
3. Rejouer E001-T2 sur Jev pour avoir enfin la colonne « faux et sûr » des erreurs invisibles.
