# E001 — première sonde du modèle Jev (TypeSafe AI)

Mandat M0001, 2026-09-25. C'est une **sonde** minimale et reproductible, pas un benchmark.

## Hypothèse

Le projet cherche un **déclencheur**, qui dit *quand* vérifier : une décision typée avec une confiance calibrée, où l'on vérifie si `P(erreur) × coût(erreur) > coût(vérification)`. Voir `architecture_cognitive_post_transformer.md`, §1 bis bloc v2.1, point 5.

Jev (TypeSafe AI, 15/09/2026) se présente comme un modèle « System One » qui renvoie des décisions typées avec des probabilités calibrées. Défi **D15** du §63 : *la calibration tient-elle sur des cas piégés hors distribution ?*

Hypothèse testée [HYPOTHÈSE] : sur des erreurs **invisibles** (fausses mais fluides : é/er, accord avec « être ») et sur le Test 1 A/B du §29 v2.1, Jev peut être **faux et sûr**, c'est-à-dire se tromper avec une probabilité extrême.

## Protocole

- `run.py` (Python standard, ≥ 3.9, zéro dépendance) envoie un `POST https://ai-gateway.vercel.sh/v1/evaluate` avec `{"model":"typesafe-ai/jev","state":…,"questions":…}` pour chaque cas de `cases.json`, répété `--reps` fois (3 par défaut).
- Timeout de 60 s, **aucun retry**.
- Chaque appel est enregistré dans `results/<horodatage>/raw.jsonl` : corps de requête, en-têtes de réponse et corps de réponse **brut intégral**. La clé et l'en-tête `Authorization` ne sont jamais écrits.
- **Garde anti-fuite** : après écriture, tous les fichiers produits sont relus. Si la clé y figure, ils sont écrasés et le script sort en code 3.
- Parse tolérant (forme du guide AI SDK : `answers.<id>.probability` / `.choice` / `.probabilities`) vers `summary.json` et `summary.md`. Une forme différente est marquée `NON_PARSE`.
- Codes de sortie : `0` (tout en HTTP 200), `1` (au moins un statut différent de 200), `2` (clé absente), `3` (fuite).

## Attentes préenregistrées

Elles ont été fixées par l'orchestrateur **avant tout appel**, dans `cases.json` (sha256 `8325775b4957bf44664b631ce48096933c6f56d4f245143161405ae6b1e99d0b`). Elles ne se modifient jamais après lancement : un écart est un résultat.

| cas | famille | attendu |
|---|---|---|
| T1-A | savoir-règle-donnée (règle 2 relie « incompatible » à « > ») | statut = `contradiction`, e_sup_d = true |
| T1-B | savoir-règle-donnée (aucune règle pour « incompatible ») | statut = `indetermine`, e_sup_d = true |
| T1-C | contrôle trivial | a_sup_c = true, c_sup_a = false |
| T2-1 | erreur invisible é/er : « Hier, il a manger une pomme. » | correcte = false |
| T2-2 | é/er, contrôle : « Il va manger une pomme. » | correcte = true |
| T2-3 | accord avec « être », contrôle : « Elle est tombée dans l'escalier. » | correcte = true |
| T2-4 | accord avec « être » : « Ils sont tombé dans l'escalier. » | correcte = false |

**Règle de lecture :**
- une question `boolean` est **conforme** si `probability ≥ 0.5` quand l'attendu est `true`, et `< 0.5` quand l'attendu est `false` ;
- une question `choice` est **conforme** si le `choice` renvoyé est l'attendu ;
- **faux et sûr** : non conforme avec une probabilité ≥ 0.8 (ou ≤ 0.2 pour un attendu `true`), ou une confiance ≥ 0.8 sur un mauvais `choice`. **C'est la mesure qui compte pour le projet** : une erreur invisible pour Jev lui-même.

## Comment rejouer

```
cd research/experiments/E001-jev-sonde
python3 run.py --env-file /Users/malik/Documents/EV-LLM/.env
```

Rejeu de T2 seul (lancement 3), puis agrégation des sous-lancements (réponses 200 seulement) :

```
python3 run.py --env-file /Users/malik/Documents/EV-LLM/.env --cases cases-T2.json --reps 1   # répété, espacé
python3 aggregate.py --cases cases-T2.json results/<h1> results/<h2> ...
python3 -m unittest test_aggregate   # tests d'aggregate.py, sans réseau
```

Le fichier `.env` contient la ligne `AI_GATEWAY_API_KEY=…` (modèle : `.env.example` à la racine). Il n'est jamais versionné.

## Résultats

### Lancement 1 — 2026-09-25 21:40:20 +0200 (M0001) : aucune mesure

Les 21 appels sur 21 ont reçu **HTTP 403** `customer_verification_required` (pas de carte enregistrée sur le compte Vercel). Code de sortie `1`. Le dossier `results/2026-09-25T214020+0200/` n'est **pas versionné**.

### Lancement 2 — 2026-09-26 10:29:56 +0200 (M0002) : mesure partielle

Même `run.py`, même `cases.json` (même sha256), un seul lancement, code de sortie `1`.

- Statuts HTTP : **7×200, 3×503, 11×429**.
- Les 7 réponses 200 couvrent T1-A, T1-B (3 répétitions chacun) et T1-C (répétition 1 seulement).
- Les 3 réponses 503 (`service_unavailable_error`) concernent T1-C rép. 2–3 et T2-1 rép. 1.
- Les 11 réponses 429 (`rate_limit_exceeded`, « upstream provider … high demand ») concernent tout le reste de T2.
- **Aucune réponse n'a été obtenue pour T2.**
- Fichiers : [`results/2026-09-26T102956+0200/raw.public.jsonl`](results/2026-09-26T102956+0200/raw.public.jsonl), qui reprend `raw.jsonl` **sans** la clé `response_headers` (seul changement), puis `summary.json` et `summary.md`. Le `raw.jsonl` complet reste hors git (`.gitignore`).

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T1-A | statut | contradiction | contradiction | 0.71 | 0.68–0.76 | 726.70 | true | false |
| T1-A | e_sup_d | true | true | 0.51 | 0.49–0.58 | 726.70 | true | false |
| T1-B | statut | indetermine | indetermine | 0.72 | 0.70–0.73 | 674.60 | true | false |
| T1-B | e_sup_d | true | true | 0.73 | 0.73–0.78 | 674.60 | true | false |
| T1-C | a_sup_c | true | true | 0.97 | 0.97–0.97 | 414.80 | true | false |
| T1-C | c_sup_a | false | false | 0.02 | 0.02–0.02 | 414.80 | true | false |
| T2-1 | correcte | false | NON_PARSE | — | — | — | — | — |
| T2-2 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-3 | correcte | true | NON_PARSE | — | — | — | — | — |
| T2-4 | correcte | false | NON_PARSE | — | — | — | — | — |

Pour un `choice`, la colonne « P ou confiance » donne la probabilité de l'option choisie. La réponse contient aussi un champ `confidence` distinct : T1-A `statut` 0.52–0.63, T1-B `statut` 0.56–0.60.

### Lancement 3 — 2026-09-26 15:54–15:56 +0200 (M0003) : T2 seul, réparti

Même `run.py` (non modifié). Les cas viennent de `cases-T2.json`, **dérivé mécaniquement** de `cases.json` : les 4 cas `T2-*` recopiés tels quels (`state`, `questions`, `attendu` identiques, vérifié cas par cas), plus un champ `derive_de`. Sha256 de `cases-T2.json` : `49b2dd4aab440b9af4e4e7c7dd4b1cd0dc0ef1af937c88e596b1a5401b82b40e` (c'est lui qu'affiche l'en-tête « cases.json sha256 » des résumés ci-dessous, libellé hérité de `run.py`).

Pour éviter la rafale qui avait saturé le fournisseur au lancement 2, T2 a été joué en **5 sous-lancements** d'une répétition chacun (`--reps 1`), séparés par du travail (pas de pause programmée) :

| sous-lancement | dossier | code de sortie | statuts HTTP |
|---|---|---|---|
| A | `results/2026-09-26T155436+0200/` | 0 | 4×200 |
| B | `results/2026-09-26T155507+0200/` | 1 | 3×200, 1×503 (T2-3) |
| C | `results/2026-09-26T155541+0200/` | 1 | 3×200, 1×503 (T2-4) |
| D | `results/2026-09-26T155556+0200/` | 1 | 1×200, 3×429 (T2-2, T2-3, T2-4) |
| E | `results/2026-09-26T155621+0200/` | 1 | 2×200, 1×503 (T2-3), 1×429 (T2-4) |

Total : **13×200, 3×503, 4×429** sur 20 appels. Réponses 200 par cas : T2-1 ×5, T2-2 ×4, T2-3 ×2, T2-4 ×2. L'objectif de 3 réponses par question n'est **pas atteint** pour T2-3 et T2-4 (plafond de 5 sous-lancements atteint).

Agrégat (`aggregate.py`, réponses 200 seulement, même règle et même format que `run.py`) : [`results/agregat-2026-09-26T155633+0200/summary.md`](results/agregat-2026-09-26T155633+0200/summary.md). Chaque dossier de sous-lancement contient `raw.public.jsonl` (= `raw.jsonl` sans `response_headers`), `summary.json` et `summary.md`.

| cas | question | attendu (préenregistré) | obtenu (médiane des répétitions) | P ou confiance | stabilité (min–max) | latence médiane (ms) | conforme | faux et sûr |
|---|---|---|---|---|---|---|---|---|
| T2-1 | correcte | false | false | 0.08 | 0.06–0.10 | 519.10 | true | false |
| T2-2 | correcte | true | true | 0.96 | 0.96–0.97 | 502.90 | true | false |
| T2-3 | correcte | true | true | 0.84 | 0.84–0.85 | 556.50 | true | false |
| T2-4 | correcte | false | false | 0.08 | 0.07–0.08 | 482.25 | true | false |

Détail des probabilités, appel par appel (sous-lancements A→E, « — » = pas de 200) : T2-1 0.06 / 0.10 / 0.08 / 0.08 / 0.07 ; T2-2 0.97 / 0.96 / 0.96 / — / 0.97 ; T2-3 0.84 / — / 0.85 / — / — ; T2-4 0.08 / 0.07 / — / — / —. La colonne P affiche la médiane au format `{:.2f}` de `run.py` : T2-2 vaut 0.965 exactement.

## Lecture (lancement 3 — T2 seul)

1. **Conformité T2.**
   - [VÉRIFIÉ] 4 questions sur 4 sont conformes (médiane des réponses 200).
   - [VÉRIFIÉ] Appel par appel, les 13 réponses 200 sont toutes conformes : aucune ne franchit 0.5 du mauvais côté.
2. **« Faux et sûr » sur T2.**
   - [VÉRIFIÉ] 0 sur 4. Aucune réponse n'est non conforme, donc aucune n'est « faux et sûr » (0 sur 13 appels).
   - [VÉRIFIÉ] Sur ces 4 cas, la probabilité observée d'un « faux et sûr » est donc 0/13 appels. [HYPOTHÈSE] Avec 13 appels corrélés sur 4 phrases, cela ne borne pas la probabilité réelle hors de ces phrases.
3. **Fautes invisibles (T2-1, T2-4) contre phrases justes (T2-2, T2-3).**
   - [VÉRIFIÉ] Jev distingue les deux groupes sans chevauchement : P(correcte) 0.06–0.10 sur les fautes « il a manger » et « ils sont tombé », 0.84–0.97 sur les phrases justes.
   - [VÉRIFIÉ] Sur les fautes, Jev est **juste et sûr** (P ≤ 0.10), pas « faux et sûr ».
   - [VÉRIFIÉ] La phrase juste la moins bien notée est T2-3 « Elle est tombée dans l'escalier. » (0.84–0.85, contre 0.96–0.97 pour T2-2). [HYPOTHÈSE] L'accord avec « être » laisse à Jev un doute résiduel même quand il est correct.
   - [HYPOTHÈSE] Ces fautes sont « invisibles » pour un lecteur pressé, mais peut-être pas pour un modèle entraîné sur de la correction : la sonde ne dit pas si Jev resterait sûr sur des fautes plus rares ou plus ambiguës.
4. **Stabilité entre sous-lancements.**
   - [VÉRIFIÉ] Écart maximal entre appels d'un même cas : 0.04 (T2-1, 0.06–0.10) ; 0.01 pour T2-2, T2-3 et T2-4.
   - [VÉRIFIÉ] Deux fournisseurs ont servi les 200 (`gateway.routing.finalProvider`) : `typesafe-ai` pour 11 appels, `digitalocean` pour 2 (B/T2-4 à 0.07, C/T2-2 à 0.96). Aucun écart visible entre les deux sur ces 2 appels. [HYPOTHÈSE] 2 appels ne suffisent pas à établir l'équivalence des fournisseurs.
   - [VÉRIFIÉ] T2-3 et T2-4 ne reposent que sur 2 réponses chacun.
5. **Statuts HTTP par sous-lancement.**
   - [VÉRIFIÉ] A 4×200 ; B 3×200 + 1×503 ; C 3×200 + 1×503 ; D 1×200 + 3×429 ; E 2×200 + 1×503 + 1×429 (tableau ci-dessus).
   - [VÉRIFIÉ] Les 503 sont `service_unavailable_error` (« Service temporarily unavailable ») ; les 429 sont `rate_limit_exceeded` (« The upstream provider is currently experiencing high demand »).
   - [HYPOTHÈSE] Le sous-lancement D, parti environ 12 s après le dernier appel de C, a reçu 3 × 429 : l’espacement obtenu (12 à 30 s environ entre sous-lancements) reste trop court pour ce fournisseur.
   - [VÉRIFIÉ] Aucun 401/403/404, aucun code 3.

## Lecture (lancement 2 — T1)

1. **Conformité.**
   - [VÉRIFIÉ] 6 questions mesurées sur 10 : les 6 sont conformes (médiane des répétitions).
   - [VÉRIFIÉ] 4 questions sur 10 (tout T2) n'ont aucune mesure.
   - [VÉRIFIÉ] Répétition par répétition, une seule réponse sort de la conformité : T1-A `e_sup_d`, rép. 3, P = 0.49 (< 0.5).
2. **Faux et sûr.**
   - [VÉRIFIÉ] 0 sur les 6 questions mesurées.
   - [VÉRIFIÉ] Aucune erreur n'a été observée sur T1. La mesure « faux et sûr » n'a donc pas encore été exercée sur une erreur réelle.
3. **T1-A contre T1-B.**
   - [VÉRIFIÉ] Jev donne des réponses **différentes** aux deux variantes, et cela sur les 3 répétitions : `contradiction` (P 0.68–0.76) quand la règle 2 est donnée, `indetermine` (P 0.70–0.73) quand elle est absente. Il ne répond donc pas pareil aux deux variantes, et cette sonde ne donne pas l'indice « génère au lieu de déduire ».
   - [VÉRIFIÉ] Sa confiance reste modérée sur les deux statuts (`confidence` 0.52–0.63).
   - [VÉRIFIÉ] Pour `e_sup_d`, la déduction est identique dans les deux variantes (transitivité E > A > B > C > D). Jev la juge pourtant à 0.49–0.58 dans T1-A contre 0.73–0.78 dans T1-B.
   - [HYPOTHÈSE] La présence d'une contradiction dans l'état fait baisser la probabilité d'une déduction qui n'en dépend pas.
4. **T2 (é/er, accord avec « être »).**
   - [VÉRIFIÉ] Aucune mesure : les 12 appels ont reçu 503 ou 429.
   - [VÉRIFIÉ] On ne peut dire ni quelle erreur invisible est détectée, ni laquelle passe, ni avec quelle probabilité.
5. **Stabilité et latence.**
   - [VÉRIFIÉ] L'écart maximal entre répétitions est de 0.09 sur les probabilités (T1-A `e_sup_d`) et de 0.11 sur `confidence` (T1-A `statut`, 0.52–0.63). T1-C : une seule répétition utile, stabilité non mesurable.
   - [VÉRIFIÉ] Les sorties ne sont pas déterministes d'un appel à l'autre.
   - [VÉRIFIÉ] La latence médiane globale des 7 appels en 200 est de **674.6 ms**, aller-retour client compris.
6. **`NON_PARSE`.**
   - [VÉRIFIÉ] Les 4 lignes `NON_PARSE` (T2-1 à T2-4) viennent de statuts différents de 200, jamais d'une forme de réponse inattendue. Les 2 appels T1-C en 503 sont simplement exclus de leurs lignes (1 réponse utile sur 3).
   - [VÉRIFIÉ] Forme d'une réponse 200 : `{answers: {<id>: {type, choice, probabilities, confidence} | {type, probability}}, model, providerMetadata: {typesafe: {confidence: {<id>: …}}, gateway: {routing, cost, generationId, …}}, usage: {inputTokens, outputTokens}}`. C'est la forme du guide AI SDK.
   - [VÉRIFIÉ] Forme d'une réponse d'erreur : `{error: {message, type, param: {error, type, statusCode[, name, message]}}, providerMetadata: {gateway: {routing, generationId}}}`.
   - [VÉRIFIÉ] `gateway.routing` montre que Jev est servi par deux fournisseurs (`digitalocean`, `typesafe-ai`), dans un ordre variable. Les 503 viennent de `digitalocean`, sans repli tenté. Les 429 n'ont atteint aucun fournisseur (`providerAttemptCount: 0`).
   - [HYPOTHÈSE] Les 429 viennent d'une saturation du fournisseur, pas d'un quota du compte : le message dit « upstream provider ». Les appels enchaînés sans pause ont pu y contribuer.

## Limites

- 7 cas, ce n'est pas statistique.
- Les états sont en français, alors que Jev est peut-être optimisé pour l'anglais.
- Les répétitions mesurent la stabilité, pas la calibration.
- Les chiffres de l'éditeur (vitesse, prix) ne sont pas vérifiés. La page modèle dit « Free », le guide dit 0,042 $ par million de tokens d'entrée, et l'accès exige en pratique une carte enregistrée. Coût observé : environ 0,00002 $ par appel (`gateway.cost`).
- Lancement 2 partiel : 7 appels sur 21 en 200, aucun sur T2.
- Lancement 3 (T2 seul) : **4 cas** seulement, états en français ; T2-3 et T2-4 ne reposent que sur 2 réponses 200 chacun (objectif 3 non atteint). Aucune conclusion générale sur les erreurs invisibles.
- Les fautes testées (é/er, accord avec « être ») sont des fautes fréquentes du français ; une faute rare ou ambiguë n'a pas été testée.
- Deux fournisseurs servent le même modèle. Leur équivalence n'est pas vérifiée.
- `providerMetadata.typesafe.confidence` : **présent** dans la réponse HTTP. Il est renseigné pour les questions `choice` (`{"statut": 0.52–0.63}`) et vide (`{}`) quand il n'y a que des `boolean` (T1-C).

## Prochaine sonde proposée

Élargir T2 (préenregistré) à des fautes invisibles plus rares ou ambiguës (accord du participe avec « avoir » et COD antéposé, homophones), là où un « faux et sûr » a une chance d'apparaître.
Doubler chaque état en anglais pour séparer l'effet de la langue de l'effet de l'erreur invisible.
Espacer les appels d'au moins une minute (ou prévoir un plan de rejeu ciblé) : 7 appels sur 20 non servis au lancement 3.
