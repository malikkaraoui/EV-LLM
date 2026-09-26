# E003 — protocole préenregistré (étalon LLM sur les cas E001)

Mandat M0006, 2026-09-26. Ce fichier est committé **avant** le premier appel d'évaluation.
Il ne se modifie pas après résultats : un écart au protocole est un résultat, noté au README.

## Question

Sur les **mêmes cas, mêmes attentes** que E001 (`cases.json`, sha256
`8325775b4957bf44664b631ce48096933c6f56d4f245143161405ae6b1e99d0b`, copié tel quel depuis
`origin/exp/e001-sonde-jev`), des LLM génératifs :
1. distinguent-ils T1-A (contradiction) de T1-B (indéterminé) ?
2. sont-ils « faux et sûrs » sur T2 (erreurs invisibles é/er, accord avec « être ») ?

## Modèles (choisis dans `GET https://ai-gateway.vercel.sh/v1/models`, lu le 2026-09-26)

| rôle | identifiant | réglages | justification (une ligne) |
|---|---|---|---|
| LLM-1 petit/rapide | `openai/gpt-4.1-mini` | `temperature: 0`, pas de raisonnement | petit modèle sans raisonnement, `temperature` supportée, aucun token de raisonnement ne consomme les 400 tokens de sortie. |
| LLM-2 raisonnement récent | `google/gemini-3.8-flash` | `temperature: 0`, `reasoning: {"effort": "low"}` | modèle de raisonnement récent (catalogue : sortie 2026-09), autre fournisseur que LLM-1, `temperature` supportée, effort `low` pour tenir dans `max_tokens` 400. |

[HYPOTHÈSE] La forme `reasoning: {"effort": "low"}` est celle acceptée par l'API compatible
OpenAI de la Gateway (catalogue : `reasoning_options` = effort `low`/`high`). Elle est vérifiée
par l'appel pilote ci-dessous, pas par la documentation.

## Appel d'évaluation (fixe)

- `POST https://ai-gateway.vercel.sh/v1/chat/completions`, `Authorization: Bearer <AI_GATEWAY_API_KEY>`
  (clé chargée par le script depuis `--env-file`, jamais affichée ni écrite).
- Corps : `{"model", "messages": [{"role": "user", "content": <prompt>}], "temperature": 0,
  "max_tokens": 400, "response_format": {"type": "json_object"}}` (+ `reasoning` pour LLM-2).
- **Un appel par (modèle, cas, question, répétition)** : 2 × 10 × 3 = **60 appels**.
- Timeout 60 s.

### Prompt (identique pour les deux modèles ; `{…}` remplacés depuis `cases.json`)

```
Tu réponds à une question de raisonnement. Réponds UNIQUEMENT par un objet JSON strict, sans aucun texte autour et sans bloc de code, de la forme :
{"reponse": <valeur>, "confiance": <nombre entre 0 et 1>}

Énoncé :
{state}

Question :
{instructions}

{bloc_options}
"confiance" est ta probabilité (entre 0 et 1) que ta réponse soit correcte.
```

`{bloc_options}` :
- question `choice` :
  ```
  "reponse" doit être exactement une de ces chaînes :
  - "<clé>" : <critère>
  ```
  (une ligne par clé de `criteria`, dans l'ordre de `cases.json`)
- question `boolean` : `"reponse" doit être le booléen JSON true ou false.`

## Parse (strict, jamais corrigé à la main)

Une réponse est **parsée** si et seulement si :
- HTTP 200 et `choices[0].message.content` est une chaîne ;
- `json.loads(content.strip())` réussit (un bloc ```` ``` ```` ou du texte autour = échec) ;
- le résultat est un objet dont les clés sont **exactement** `reponse` et `confiance` ;
- `reponse` est un booléen JSON (question `boolean`) ou une des clés de `criteria` (question `choice`) ;
- `confiance` est un nombre (pas un booléen) dans [0, 1].

Sinon : `NON_PARSE` (raison notée dans `summary.json`).

## Règle de lecture (même colonnes que E001)

Par (modèle, cas, question), sur les répétitions parsées :
- **obtenu** = réponse majoritaire. Égalité entre réponses différentes → `INSTABLE`
  (conforme = false, faux et sûr = false). Aucune répétition parsée → `NON_PARSE`
  (conforme et faux et sûr = —).
- **P ou confiance** = médiane des `confiance` des répétitions qui ont donné la réponse majoritaire ;
  **stabilité** = min–max des `confiance` de toutes les répétitions parsées (+ répartition si >1 réponse).
- **conforme** = obtenu == attendu préenregistré.
- **faux et sûr** = non conforme **et** P ≥ 0.8. Compté aussi répétition par répétition
  (`n_faux_et_sur_reps` dans `summary.json`).

Attention : la « confiance » est **verbalisée** par le LLM (un nombre qu'il écrit), pas une
probabilité de sortie. Pour Jev, E001 lit une probabilité renvoyée par l'API. Les deux ne
sont pas comparables sans étude de calibration (limite écrite au README).

## Appel pilote (hors évaluation)

Avant le lancement, **un** appel par modèle avec exactement les mêmes réglages et le même
gabarit de prompt, sur un énoncé qui n'est **pas** dans `cases.json` :
- énoncé : `Faits : tout carré est un rectangle. X est un carré.`
- question (`boolean`) : `Peut-on déduire que X est un rectangle ?`

But : vérifier que les réglages sont acceptés (HTTP 200), que la réponse se parse et combien
de tokens de raisonnement sont consommés. Le pilote ne sert qu'à valider la mécanique ; ses
réponses ne sont pas des résultats. Si un réglage est refusé (HTTP 400), il est retiré pour ce
modèle, et ce retrait est noté ici **avant** le lancement d'évaluation.

## Budget et erreurs

- **Budget dur : ≤ 70 appels au total** (2 pilotes + 60 évaluations + au plus 8 relances).
  Le script refuse tout appel au-delà de son plafond `--max-calls`.
- 429/503 : l'élément est remis en fin de file (la relance est espacée par les autres appels,
  jamais par une attente), **au plus 2 relances** par élément, puis abandon (STOP partiel).
- 401/403/404 : arrêt immédiat du lancement (STOP).
- Erreur réseau : notée, pas relancée.
- Journal `results/<horodatage>/raw.jsonl` : corps de requête, statut, latence, et de la
  réponse **seulement** `model`, `choices[0].message.content`, `finish_reason`, `usage`
  (ou le corps d'erreur). Aucun en-tête n'est enregistré.
- Garde anti-fuite (comme E001) : relecture de tous les fichiers produits ; si la clé y figure,
  ils sont écrasés et le script sort en code 3.

## Amendement 1 (26/09) — remplacement de LLM-2

Mandat M0008. Committé **avant** tout appel d'évaluation. Seul LLM-2 change : `cases.json`, le
prompt, les réglages (`temperature: 0`, `max_tokens: 400`, `response_format: json_object`,
`reasoning: {"effort": "low"}`), le parse et la règle conforme / faux et sûr sont **inchangés**.

**Raison.** [VÉRIFIÉ] Au pilote M0006 (2026-09-26 15:57:30 +0200), `google/gemini-3.8-flash` a
répondu HTTP 403 `no_providers_available` : « Free tier users do not have access to this model ».
Décision de l'orchestrateur : option (b), un modèle de raisonnement accessible au compte.

**Méthode de choix.** Jusqu'à 4 pilotes (1 appel chacun, même énoncé pilote que ci-dessus, hors
`cases.json`, mêmes réglages que LLM-2), sur des modèles « de raisonnement » (tag `reasoning` de
`GET /v1/models`, `temperature` et `response_format` supportés, effort `low` proposé), d'éditeurs
différents. Premier en HTTP 200 avec une réponse qui passe le parse strict = retenu.
Option `--pilot-model <id>` ajoutée à `run_llm.py` pour cela (LLM-2 seul, mêmes réglages).

| # | modèle candidat | éditeur | HTTP | parse | dossier |
|---|---|---|---|---|---|
| 1 | `alibaba/qwen3.8-flash` (2026-08) | Alibaba | 403 `no_providers_available` (free tier) | — | `pilot/2026-09-26T161527+0200/` |
| 2 | `zai/glm-5.3-flash` (2026-08) | Z.ai | 403 `no_providers_available` (free tier) | — | `pilot/2026-09-26T161530+0200/` |
| 3 | `google/gemini-2.5-flash` (2025-03) | Google | **200** | OK : `{"reponse": true, "confiance": 1}`, `finish_reason: stop`, 204 tokens de raisonnement sur 223 de sortie | `pilot/2026-09-26T161543+0200/` |

Le 4ᵉ pilote n'a pas été utilisé.

**LLM-2 retenu : `google/gemini-2.5-flash`**, `temperature: 0`, `reasoning: {"effort": "low"}`.
Modèle de raisonnement (tag `reasoning`, effort réglable), accessible au compte, autre éditeur
que LLM-1.

- [HYPOTHÈSE] Le free tier semble ouvrir les modèles anciens (2025) et fermer les récents (2026).
  Trois points ne suffisent pas à l'établir.
- [HYPOTHÈSE] Au pilote, le raisonnement a pris 204 des 400 tokens de sortie. Sur les cas plus
  longs de `cases.json`, une réponse peut être tronquée (`finish_reason: length`) : elle compte
  alors `NON_PARSE`, sans correction.
- LLM-2 n'est plus « récent » (2025-03) : l'étalon compare Jev à un modèle de raisonnement
  accessible, pas à l'état de l'art. Limite écrite au README.

**Budget.** 2 appels M0006 + 3 pilotes = 5 consommés. Évaluation : 60 appels, plafond
`--max-calls 65` (total ≤ 70, budget initial ; ≤ 66 pour l'évaluation, consigne M0008).
Plafond atteint → STOP partiel.
