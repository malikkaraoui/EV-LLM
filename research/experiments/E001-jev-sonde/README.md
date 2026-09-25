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

Le fichier `.env` contient la ligne `AI_GATEWAY_API_KEY=…` (modèle : `.env.example` à la racine). Il n'est jamais versionné.

## Résultats

**Lancement du 2026-09-25 à 21:40:20 +0200 : aucune mesure.** Les 21 appels sur 21 ont reçu **HTTP 403**, code de sortie `1`.

Le corps d'erreur, identique pour les 21 appels, est de type `customer_verification_required`. L'AI Gateway exige une carte bancaire enregistrée sur le compte Vercel pour servir les requêtes et débloquer les crédits gratuits.

Conformément au mandat (un 403 sur tous les appels est un STOP), **`results/` n'est pas committé**. Le `summary.md` produit ne contient que des `NON_PARSE`.

## Lecture

- [VÉRIFIÉ] L'endpoint `POST /v1/evaluate` existe et authentifie la requête : la réponse est un refus de facturation (403), pas un 404 ni un 401.
- [HYPOTHÈSE] La clé est valide. Seule la vérification de paiement du compte bloque. À confirmer au prochain lancement.
- [VÉRIFIÉ] Aucune donnée sur Jev n'a été obtenue. Rien ne peut être dit sur sa calibration.

## Limites

- 7 cas, ce n'est pas statistique.
- Les états sont en français, alors que Jev est peut-être optimisé pour l'anglais.
- Les répétitions mesurent la stabilité, pas la calibration.
- Les chiffres de l'éditeur (vitesse, prix) ne sont pas vérifiés. La page modèle dit « Free », le guide dit 0,042 $ par million de tokens d'entrée, et l'accès exige en pratique une carte enregistrée.
- La forme exacte de la réponse HTTP de `/v1/evaluate` n'est toujours pas observée : le parse suit la forme du guide AI SDK.

## Prochaine sonde proposée

Une fois la carte enregistrée par Malik, relancer E001 à l'identique, avec les mêmes `cases.json` et le même sha256, puis lire la colonne « faux et sûr ».
Ensuite, doubler chaque état en anglais pour séparer l'effet de la langue de l'effet de l'erreur invisible.
