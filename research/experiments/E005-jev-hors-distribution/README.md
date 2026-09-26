# E005 — Jev hors distribution : où se trompe-t-il, et le sait-il ?

Mandat M0009, 2026-09-26, branche `exp/e005-jev-hors-distribution` (partie de `origin/exp/e001-sonde-jev` @ `7e953a9`). Sonde, pas benchmark.

## Hypothèse (D15)

Un **déclencheur** (« quand vérifier ») n'est utile que si la confiance du système reste honnête sur les **erreurs invisibles** : fausses mais fluides (§63 D15 ; §1 bis v2.1 points 3 et 5 de `architecture_cognitive_post_transformer.md`).

E001 n'a observé que du « juste et sûr » (7 cas, fautes é/er et accord avec « être », fréquentes). Le « faux et sûr » n'y a jamais été exercé.

Hypothèse testée [HYPOTHÈSE] : sur des règles **rares** du français écrit (accord du participe passé hors cas scolaire, homophones moins fréquents, formes justes qui « sonnent faux ») et sur de la logique avec distracteurs ou à 4 pas, Jev se trompe, et au moins une partie de ces erreurs est **sûre** (P ≥ 0.8 du mauvais côté).

## Protocole

- **Corpus préenregistré** : [`cases.json`](cases.json) (32 cas, 38 questions), engendré par [`gen_cases.py`](gen_cases.py), sha256 `5f3790074e08446e40860a02d56773ae58bfe92cb8e3a046d3345fb3089d2032`. Même schéma qu'E001, plus un champ `justification` (règle en une ligne). Committé et poussé **avant le premier appel** (commit `719d4c0`, 16:16:47 ; premier appel 16:16:55).
- Familles (≈ moitié juste / moitié fausse, en **paires minimales** : une lettre change entre la phrase juste et la fausse) :
  - F1 accords rares (10) : COD antéposé avec « avoir », pronominaux à COI (« se laver les mains », « se parler », « se succéder »), « fait » + infinitif, « laissé » + infinitif, « il a fait » impersonnel ;
  - F2 homophones moins fréquents (8) : quel que / quelque, quelle / qu'elle, censé / sensé, près / prêt, a / à ;
  - F3 juste mais atypique (6) : « ci-joint » en tête, « marron » invariable, « se plaire » invariable — chacune avec sa faute fluide jumelle ;
  - F4 logique au format T1 (5) : distracteurs (fait redondant, règle non pertinente) sur les trois statuts, et une contradiction à 4 pas de transitivité (faits mélangés) avec sa variante cohérente ;
  - F5 contrôles triviaux (3).
- Consigne `boolean` identique à E001 : « Cette phrase est-elle orthographiquement correcte en francais ? ».
- **Appels** : `run.py` d'E001, **non modifié**, `--reps 1`, `--cases` vers ce corpus ou vers un **sous-corpus dérivé mécaniquement** ([`derive.py`](derive.py) : cas recopiés à l'identique, assertion champ par champ ; même précédent que `cases-T2.json` d'E001). `run.py` écrit dans `E001-jev-sonde/results/` : chaque dossier produit a été **déplacé** tel quel dans `E005-jev-hors-distribution/results/` (aucun fichier suivi d'E001 modifié, `git status` vide sur E001 après chaque lancement).
- Politique 429/503 : au plus 6 lancements, ≥ 60 s entre deux départs (mesuré), budget dur 200 appels.
- **Agrégation** : `aggregate.py` d'E001, non modifié (`--out-root results`), qui revérifie que chaque appel correspond au cas du corpus.
- **Analyse** : [`analyse.py`](analyse.py) (stdlib, importe `run.extract` d'E001) → [`results/analyse.md`](results/analyse.md), **appel par appel**.
- Règle de lecture : celle d'E001 (conforme ; « faux et sûr » = non conforme avec P ≥ 0.8 pour un attendu `false`, P ≤ 0.2 pour un attendu `true`, ou P(choix) ≥ 0.8 sur un mauvais `choice`).

## Rejouer

```
cd research/experiments/E005-jev-hors-distribution
python3 gen_cases.py                                  # regenere cases.json (sha256 identique)
python3 derive.py /tmp/sous.json F1-04 F1-05 ...      # sous-corpus optionnel
python3 ../E001-jev-sonde/run.py --env-file /Users/malik/Documents/EV-LLM/.env --cases cases.json --reps 1
mv ../E001-jev-sonde/results/<horodatage> results/
python3 ../E001-jev-sonde/aggregate.py --cases cases.json --out-root results results/2026-*
python3 analyse.py
```

## Résultats

### Lancements (2026-09-26, `run.py` d'E001 non modifié, `--reps 1`)

| # | dossier | départ | écart mesuré depuis le départ précédent | appels | statuts HTTP |
|---|---|---|---|---|---|
| 1 | `results/2026-09-26T161655+0200/` | 16:16:55 | — | 32 (corpus entier) | 9×200, 1×503, 22×429 |
| 2 | `results/2026-09-26T161811+0200/` | 16:18:11 | 76 s | 23 | 6×200, 1×503, 16×429 |
| 3 | `results/2026-09-26T161845+0200/` | 16:18:45 | **34 s** (écart de protocole, voir Limites) | 32 | 32×429 |
| 4 | `results/2026-09-26T161956+0200/` | 16:19:56 | 71 s | 20 | 8×200, 2×503, 10×429 |
| 5 | `results/2026-09-26T162058+0200/` | 16:20:58 | 62 s | 15 | 4×200, 2×503, 9×429 |
| 6 | `results/2026-09-26T162237+0200/` | 16:22:37 | 99 s | 29 | 7×200, 1×503, 21×429 |

Total : **151 appels** (budget 200), **34 × 200**, 8 × 503, 109 × 429. Aucun 401/403/404, aucun code 3. Les lancements 2 à 6 portent sur des sous-corpus dérivés (`derive.py`), dans un ordre de priorité fixé avant chaque lancement : cas sans réponse d'abord, puis réplication des non-conformités, puis le reste.

Chaque dossier contient `raw.public.jsonl` (= `raw.jsonl` sans la clé `response_headers`, égalité vérifiée ligne à ligne), `summary.json`, `summary.md`. Agrégat `aggregate.py` (médianes, règle d'E001) : [`results/agregat-2026-09-26T162249+0200/summary.md`](results/agregat-2026-09-26T162249+0200/summary.md). Analyse appel par appel : [`results/analyse.md`](results/analyse.md) (+ `analyse.json`).

**Couverture** : 37 questions sur 38 ont au moins une réponse 200 ; **5 seulement en ont 2** (F1-04, F4-01 × 2 questions, F4-04 × 2 questions) ; F5-03 n'en a aucune. L'objectif « ≥ 2 réponses 200 par question » **n'est pas atteint**.

### Par famille (appel par appel)

| famille | questions mesurées | évaluations | conformes | faux et sûr |
|---|---|---|---|---|
| F1 accords rares | 10 | 11 | 6/11 | 4 |
| F2 homophones | 8 | 8 | 8/8 | 0 |
| F3 juste atypique | 6 | 6 | 4/6 | 1 |
| F4 distracteurs | 6 | 8 | 5/8 | 2 |
| F4 4 pas | 4 | 6 | 2/6 | 2 |
| F5 contrôles | 3 | 3 | 3/3 | 0 |
| **total** | 37 | 42 | 28/42 | 9 |

### « Faux et sûr » — le résultat clé

6 questions distinctes, 9 évaluations. L'agrégat par médiane (`aggregate.py`, règle d'E001) marque exactement les mêmes 6 questions.

| cas | phrase / question | attendu | Jev (par appel) |
|---|---|---|---|
| F1-04 | « Elles se sont lavées les mains avant le repas. » | fausse | P(correcte) 0.84 / 0.85 |
| F1-05 | « Ils se sont parlés pendant des heures. » | fausse | 0.80 (pile au seuil) |
| F1-08 | « Les robes qu'elle a faites faire sont superbes. » | fausse | 0.86 |
| F3-02 | « Ci-jointe la facture demandée. » | fausse | 0.86 |
| F4-01 | `statut` (T1-A + fait redondant + règle non pertinente) | contradiction | coherent 0.88 / 0.89 (`confidence` 0.82 / 0.84) |
| F4-04 | `a_sup_f` (A > F en 4 pas, faits mélangés) | true | P 0.15 / 0.19 |

Non-conformités non sûres : F1-10 « chaleurs qu'il a faites » (0.67), F3-06 « se sont plues » (0.77), F4-03 `statut` coherent (0.76), F4-04 `statut` coherent (0.57 / 0.55).

### Calibration grossière (questions `boolean`, 35 évaluations)

| P(true) renvoyée | n | part d'attendus true | conformes |
|---|---|---|---|
| 0.0–0.2 | 7 | 2/7 | 5/7 |
| 0.2–0.4 | 2 | 0/2 | 2/2 |
| 0.4–0.6 | 4 | 3/4 | 4/4 |
| 0.6–0.8 | 5 | 3/5 | 3/5 |
| 0.8–1.0 | 17 | 12/17 | 12/17 |

Toutes questions, probabilité de la réponse renvoyée ≥ 0.8 : 19 conformes sur 28 (voir `results/analyse.md`, tableau b).

## Lecture

1. **Le « faux et sûr » existe sur ce corpus.**
   - [VÉRIFIÉ] 9 évaluations « faux et sûr » sur 42, portant sur 6 questions sur 37 mesurées. E001 n'en avait aucune.
   - [VÉRIFIÉ] 3 d'entre elles sont répliquées sur 2 appels, avec un écart ≤ 0.04 : F1-04 (0.84 / 0.85), F4-01 `statut` (0.88 / 0.89), F4-04 `a_sup_f` (0.15 / 0.19). Les 3 autres reposent sur 1 appel.
   - [VÉRIFIÉ] F1-05 est à 0.80, exactement au seuil ; un seuil à 0.81 le sortirait de la liste.
2. **Phrases : les erreurs vont toutes dans le même sens.**
   - [VÉRIFIÉ] Les 13 évaluations de phrases justes sont conformes (13/13). Sur les phrases fausses : 6/13 conformes. Les 7 évaluations non conformes consistent toutes à juger **correcte** une phrase fautive.
   - [VÉRIFIÉ] Les fautes détectées sont les fautes fréquentes ou visibles (F1-02 « qu'il a mangé » 0.27, F2 « quelque soit » 0.15, « qu'elle heure » 0.15, « près à partir » 0.17). Les fautes non détectées sont des accords savants : pronominal à COI (« se sont lavées les mains », « se sont parlés »), « fait » + infinitif, « il a fait » impersonnel, « se plaire », « ci-joint » en tête.
   - [HYPOTHÈSE] Jev juge la plausibilité de surface (une forme accordée « a l'air » soignée) plutôt que la règle ; sur ces règles rares, sa probabilité ne signale pas qu'il ne sait pas.
3. **F2 (homophones moins fréquents) : aucune erreur.**
   - [VÉRIFIÉ] 8/8 conformes, 1 appel chacun. Sur ce corpus, la famille n'a pas piégé Jev.
4. **Logique : Jev répond « coherent » partout.**
   - [VÉRIFIÉ] Les 7 réponses `statut` de F4 (5 cas) sont toutes `coherent`, quel que soit l'attendu. Les 2 conformités (F4-02, F4-05) ne montrent donc pas une déduction.
   - [VÉRIFIÉ] Ajouter un fait redondant et une règle non pertinente à T1-A fait passer Jev de `contradiction` (E001, P 0.68–0.76) à `coherent` (P 0.88–0.89, `confidence` 0.82–0.84). La déduction E > D reste pourtant acceptée (P 0.56–0.64) : Jev admet la prémisse de la contradiction mais ne voit pas la violation.
   - [VÉRIFIÉ] À 4 pas, Jev nie la déduction A > F (P 0.15–0.19), alors qu'il accepte la transitivité en 1 pas (F5-01, 0.98) et en 2 à 3 pas (F4-01/02/03 `e_sup_d`, 0.56–0.95).
   - [VÉRIFIÉ] `providerMetadata.typesafe.confidence` est **bas** sur F4-04 `statut` (0.33–0.36, faux mais incertain) et **haut** sur F4-01 `statut` (0.82–0.84, faux et sûr). Ce champ ne signale donc pas l'erreur de F4-01.
5. **Calibration.**
   - [VÉRIFIÉ] Au-dessus de 0.8 de probabilité sur sa réponse, Jev est conforme 19 fois sur 28 (68 %). Dans la tranche 0.4–0.6, il l'est 4 fois sur 6. La confiance ne sépare pas ici le juste du faux.
   - [HYPOTHÈSE] Avec 42 évaluations tirées d'un corpus construit pour piéger, ce n'est pas une courbe de calibration du modèle, seulement un indice : sur ce type de cas, une P haute ne suffirait pas à décider de ne pas vérifier (§1 bis v2.1, point 5).
6. **Statuts HTTP.**
   - [VÉRIFIÉ] Le fournisseur sert 0 à 9 réponses 200 par lancement, puis renvoie des 429 en rafale (`rate_limit_exceeded`, « upstream provider … high demand », aucun fournisseur tenté). Les 8 × 503 viennent tous de `digitalocean`.
   - [HYPOTHÈSE] Une autre fenêtre (F04, E003) appelait la même passerelle jusque vers 16:20 ; une limite partagée a pu contribuer aux 429.

## Limites

- 32 cas, 1 à quelques réponses 200 par question : **aucune conclusion générale**. Une paire minimale ne représente pas sa règle.
- Le fournisseur sature après ~6 à 9 appels enchaînés (429 `rate_limit_exceeded`, « upstream provider … high demand », `providerAttemptCount: 0`) ; les 503 viennent tous de `digitalocean`. L'objectif « ≥ 2 réponses 200 par question » n'est pas atteint partout (tableau de couverture ci-dessus).
- L'ordre des cas dans les lancements 3 à 6 a été choisi **après** avoir vu les premières réponses (priorité : cas sans réponse, puis réplication des non-conformités). Cela change **quels** cas ont 2 réponses, jamais les attentes ni la règle de lecture ; mais les cas répliqués sont surreprésentés parmi les non-conformités.
- Lancement 3 parti **34 s** après le lancement 2 (< 60 s exigé) : écart de protocole de la fenêtre, 32 appels perdus en 429. Garde bloquante ajoutée ensuite (refus prouvé à 31 s et 51 s).
- La consigne demande si la phrase est « orthographiquement correcte ». [HYPOTHÈSE] Jev peut juger une autre notion (plausibilité, fluidité) ; c'est précisément ce que la sonde cherche à exposer, mais la frontière n'est pas mesurée.
- F1-09 (« laissé » + infinitif) est juste depuis les rectifications de 1990, pas selon la règle traditionnelle.
- États en français ; Jev est peut-être optimisé pour l'anglais.
- `providerMetadata.typesafe.confidence` n'est renseigné que pour les `choice` (5 cas F4) ; pour les `boolean`, seule la probabilité existe.
- Deux fournisseurs (`typesafe-ai`, `digitalocean`) servent le modèle ; leur équivalence n'est pas vérifiée.

## Prochaine étape

1. **Répliquer** les 6 « faux et sûr » et les 4 non-conformités non sûres (≥ 3 réponses 200 chacune), en sous-lancements de 4 à 6 appels séparés de plusieurs minutes. Aujourd'hui, 3 des 6 « faux et sûr » reposent sur un seul appel.
2. **Élargir les deux familles qui ont piégé Jev** (préenregistré, nouveau corpus) : F1 pronominaux à COI et participes suivis d'un infinitif, avec plusieurs verbes par règle ; F4 contradiction à 2, 3, 4 et 5 pas, avec et sans distracteurs. Le but est de voir si l'erreur suit la règle ou la phrase.
3. Tester si le biais « coherent » de F4 tient quand l'ordre des critères du \`choice\` est permuté.
4. Doubler chaque état en anglais, pour séparer l'effet de la langue.
