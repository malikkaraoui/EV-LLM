# E007 — Jev lit-il les règles ? (ablation de règles + plausibilité de surface)

Mandat M0017, 2026-09-26, branche `exp/e007-regles` (partie de `origin/exp/e006-replication-frontiere` @ `57e0e41`). Sonde, pas benchmark.

## Hypothèse

[HYPOTHÈSE] (issue d'E006) **Jev juge la plausibilité de surface de l'état, pas l'application des règles écrites.** Indices d'E006 : sur 2 paires minimales sur 3, la forme correcte reçoit une P(correcte) plus basse que la forme fautive ; la contradiction de T1-A disparaît dès un fait redondant ; F4-04 s'effondre quand la règle 2 porte sur les variables de la question.

Si Jev **lit** les règles : (A) sa réponse change quand on retire, inverse ou remplace la règle qui porte la réponse, et ne change pas quand on ajoute une phrase hors sujet ; (B) un fait redondant ou une règle non pertinente ne change pas le statut ; (C) énoncer la règle d'accord fait passer la forme correcte au-dessus de la forme fautive.

## Protocole

- **Corpus préenregistré** : [`cases.json`](cases.json) (27 cas, 36 questions, 90 réponses 200 visées), engendré par [`gen_cases.py`](gen_cases.py). Committé et poussé **avant le premier appel** (sha256 et heures dans Résultats). Même schéma qu'E001/E005/E006 (+ `groupe`, `cible`, `justification`).
  - **D — contrôles** (4 cas, cible 3) : A > C en 1 pas (vrai), C > A (faux), « Les enfants mange du pain » (fautive), « Le chat dort sur le canapé » (correcte).
  - **C — règle d'accord écrite dans l'état** (6 cas, cible 5) : les 3 paires minimales d'E006 (F1-04 « se sont lavé(es) les mains », F1-05 « se sont parlé(s) », F1-08 « a fait(es) faire »), formes fautive et correcte, avec **une phrase de règle** placée avant « Phrase ecrite par un eleve : … » (le reste de l'état est celui d'E006, octet pour octet). Source citée dans `justification` (règle standard d'accord du participe passé : Grevisse & Goosse, *Le Bon Usage* ; Bescherelle). + **rappel sans règle** des 3 formes correctes (états identiques à E006, cible 2) pour contrôler la dérive depuis E006. Question identique à E006.
  - **A — ablation** (10 cas, cible 3), deux bases :
    - **A1** = T1-A d'E001 (contradiction par R2, E > D déduit) ; on manipule **R2**. Questions `statut`, `e_sup_d`.
    - **A2** = chaîne A > B > C > D ; on manipule **R1**. Question « peut-on déduire A > D ».
    - Variantes : (i) règle présente ; (ii) retirée ; (iii) **inversée** (R2 : « si incompatible(X, Y) alors X > Y ou Y > X » ; R1 : « … alors Z > X ») ; (iv) **remplacée**, à la même place, par une phrase hors sujet de même longueur en caractères (« Regle 2 : le marche du hameau ouvre chaque samedi matin. », 56 car. ; « Regle 1 : la gare ferme chaque dimanche. », 40 car.) ; (v) règle présente **+** phrase hors sujet ajoutée.
  - **B — distracteurs** (4 cas, cible 3), autour de T1-A (référence = A1-i) : + fait redondant A > C (= L-DIS1 d'E006, assertion) ; + autre fait redondant B > D ; + règle 3 non pertinente seule (sans fait) ; + fait non pertinent `couleur(A, rouge)` seul (sans règle).
- **Attentes logiques recalculées sans Jev** : [`verifie_logique.py`](verifie_logique.py) (chaque règle reconnue par son texte exact, hors-sujet sans effet ; R1, R1 inversée, R2, R2 inversée, R3) → 16/16 ; `--mutation` détecte une attente inversée (code 1).
- **Appels** : [`run_e007.py`](run_e007.py) importe `run_paced.py` d'E006 **tel quel** (qui importe lui-même `run.call` d'E001) ; seuls changent l'ordre des groupes (**D, C, A, B**, fixé avant tout appel ; dans un groupe : le cas qui a le moins de réponses 200, égalité = ordre du fichier), le corpus, le dossier et le budget dur (**100 appels**, statuts non 200 compris). Hérité : départs espacés d'au moins **26 s** (le mandat exige ≥ 15 s) mesuré aussi entre invocations, **≤ 8 appels par invocation** (mandat ≤ 10), arrêt sur 401/403/404 ou 3 échecs consécutifs, garde anti-fuite, `raw.public.jsonl` = `raw.jsonl` sans en-têtes. Tests : [`test_run_e007.py`](test_run_e007.py) (4) + `test_run_paced.py` d'E006 rejoué (12).
- **Agrégat** : `aggregate.py` d'E001, non modifié. **Analyse** : [`analyse.py`](analyse.py) → [`results/analyse.md`](results/analyse.md), appel par appel.

### Règles de lecture (fixées avant tout appel)

Conforme / « faux et sûr » : règles d'E001/E005/E006. Mesure principale : la **médiane** de P par cas (P(true) pour un booléen ; P(contradiction) pour `statut`). « Change » = |Δ médiane| ≥ 0.30 ; « ne change pas » = |Δ| < 0.15 ; entre les deux : « ambigu ».

- **A** (par base) : Jev **lit la règle** si (ii), (iii) et (iv) changent par rapport à (i) dans le sens attendu (P(contradiction) baisse pour A1, P(true) baisse pour A2) ET (v) ne change pas. **Ne la lit pas** si aucune de (ii)/(iii)/(iv) ne change. Sinon : **partiellement**.
  - **Écart au mandat, décidé avant tout appel** : le mandat dit « sa réponse doit changer avec (ii)/(iii) et PAS avec (iv) ». Or (iv) *remplace* la règle : logiquement la règle est absente, la bonne réponse est celle de (ii). J'ai gardé (iv) tel que défini (remplacement, attente = (ii)) : si Jev répond comme en (i) sous (iv), c'est un signe de **surface** (une phrase « Regle 2 : … » de même longueur à la même place suffit). Et j'ai ajouté (v) (règle présente + hors sujet) pour tester l'intention du mandat : une phrase hors sujet ne doit **pas** changer la réponse.
  - A1 (ii) et (iv) : `incompatible(D, E)` reste un fait sans règle ; attente `coherent` (critère « aucune règle donnée n'est violée »), mais `indetermine` est défendable. La lecture porte donc sur **P(contradiction)**, pas sur le choix.
- **B** : un distracteur « tue » la contradiction si la médiane de P(contradiction) < 0.5 (choix majoritaire ≠ `contradiction`).
- **C** (par paire) : écart = médiane P(correcte) avec règle − sans règle (sans règle = rappel C0 pour la forme correcte ; E006 pour la forme fautive, 5 appels, dispersion ≤ 0.04). Jev **corrige son jugement** sur une paire si, avec la règle, la forme correcte a P ≥ 0.5 ET la forme fautive P < 0.5 (les deux conformes).

## Rejouer

```
cd research/experiments/E007-regles
python3 gen_cases.py && python3 verifie_logique.py     # corpus + attentes (16/16)
python3 verifie_logique.py --mutation                  # doit sortir en code 1
python3 -m unittest test_run_e007                      # 4 tests, zero reseau
(cd ../E006-replication-frontiere && python3 -m unittest test_run_paced)   # 12 tests
python3 run_e007.py                                    # <= 8 appels, a relancer jusqu'au code 5
python3 ../E001-jev-sonde/aggregate.py --cases cases.json --out-root results results/2026-*
python3 analyse.py
```

## Résultats

### Appels (2026-09-26, 17:37:20 → 18:15:55)

Corpus committé et poussé avant le premier appel : commit `7e4284a` (17:37:13), `cases.json` sha256 `d1680d7e0e52f951b6f1aead9406b46567e91f995f3c4a69d0d0fb1d0cd0b004` ; premier appel 17:37:20. 12 invocations de `run_e007.py` (11 × 8 + 1 × 2), puis code 5 (« rien à faire »). **90 appels, 90 × HTTP 200** (budget 100) ; aucun 429, 503, 401/403/404 ; aucune fuite (garde anti-fuite à chaque invocation). Intervalles entre départs : **n = 89, min 26,0 s, max 26,0 s**. Fournisseur final : `typesafe-ai` × 80, `digitalocean` × 10. 117 évaluations, 0 NON_PARSE. Toutes les cibles atteintes.

Agrégat `aggregate.py` : [`results/agregat-2026-09-26T181559+0200/summary.md`](results/agregat-2026-09-26T181559+0200/summary.md). Analyse appel par appel : [`results/analyse.md`](results/analyse.md) (+ `analyse.json`).

### D — contrôles : 12/12 conformes

A > C 0.98 ; C > A 0.02 ; « Les enfants mange » 0.08 ; « Le chat dort » 0.97 (médianes, 3 appels chacun).

### C — règle d'accord écrite (5 appels par cas)

| paire | forme | P(correcte) sans règle (E006, méd.) | rappel C0 E007 (méd.) | **avec règle** (méd., étendue) | Δ avec − sans |
|---|---|---|---|---|---|
| « se sont lavé(es) les mains » | fautive | 0.84 | — | **0.09** (0.08–0.09) | −0.75 |
| | correcte | 0.61 | 0.54 | **0.86** (0.86–0.90) | +0.25 |
| « se sont parlé(s) » | fautive | 0.84 | — | **0.05** (0.05–0.06) | −0.79 |
| | correcte | 0.90 | 0.92 | **0.93** (0.92–0.93) | +0.03 |
| « a fait(es) faire » | fautive | 0.86 | — | **0.09** (0.08–0.09) | −0.77 |
| | correcte | 0.67 | 0.74 | **0.88** (0.86–0.88) | +0.21 |

Écart correcte − fautive : sans règle −0.23 / +0.06 / −0.19 ; **avec règle +0.77 / +0.88 / +0.79**. Critère préenregistré « corrige son jugement » : **3/3 paires**. 30/30 conformes avec règle.

### A — ablation (3 appels par variante ; médianes)

| base, mesure | (i) présente | (ii) retirée | (iii) inversée | (iv) remplacée hors sujet | (v) présente + hors sujet |
|---|---|---|---|---|---|
| A1 (T1-A, R2) — P(contradiction) | 0.77 | 0.70 (Δ −0.07) | **0.34 (Δ −0.43)** | 0.63 (Δ −0.14) | 0.70 (Δ −0.07) |
| A1 — choix `statut` | contradiction ×3 | contradiction ×3 | coherent ×3 | contradiction ×3 | contradiction ×3 |
| A1 — P(E > D), attendu true | 0.59 | 0.65 | 0.63 | 0.70 | 0.54 |
| A2 (A > D, R1) — P(true) | 0.95 | 0.90 (Δ −0.05) | **0.28 (Δ −0.67)** | 0.85 (Δ −0.10) | 0.96 (Δ +0.01) |
| attendu | vrai / contradiction | faux / coherent | faux / coherent | faux / coherent | vrai / contradiction |

Verdict préenregistré, par base : **partiellement** (A1 et A2) — (iii) change, (ii) et (iv) ne changent pas, (v) ne change pas.

### B — distracteur isolé (T1-A, 3 appels ; médianes)

| distracteur | choix `statut` | P(contradiction) | tue (< 0.5) | P(E > D) |
|---|---|---|---|---|
| aucun (A1-i) | contradiction ×3 | 0.77 | non | 0.59 |
| fait redondant A > C (= L-DIS1 E006) | coherent ×2, contradiction ×1 | 0.34 | **oui** | 0.19 |
| fait redondant B > D | contradiction ×3 | 0.78 | non | 0.43 |
| règle 3 non pertinente seule | coherent ×3 | 0.38 | **oui** | 0.62 |
| fait `couleur(A, rouge)` seul | coherent ×2, contradiction ×1 | 0.49 | **oui** (pile au seuil) | 0.73 |
| phrase hors sujet ajoutée (A1-v) | contradiction ×3 | 0.70 | non | 0.54 |

## Lecture

**Jev lit-il les règles ? Partiellement.** Il suit une règle écrite quand elle s'oppose à ce qu'il ferait par défaut ; il ne se limite pas aux règles données.

1. **Une règle d'accord écrite corrige les trois paires.**
   - [VÉRIFIÉ] Avec la règle placée avant la phrase, la forme fautive tombe de 0.84–0.86 à 0.05–0.09 et la forme correcte monte à 0.86–0.93, sur les 3 paires (5 appels chacune, 30/30 conformes). Les deux paires où Jev préférait la forme fautive (E006) sont inversées.
   - [HYPOTHÈSE] Cela montre que Jev *utilise* le texte de la règle. Cela ne montre pas qu'il *l'applique* : la règle nomme le cas (« se laver les mains », « se parler », « fait » + infinitif) et dit « ne s'accorde pas ». Une correspondance de mots suffirait. E007 n'a pas testé une règle **fausse** ni une règle formulée sans l'exemple.
2. **Une règle inversée est suivie ; une règle absente est remplacée par la règle attendue.**
   - [VÉRIFIÉ] Inverser R2 fait passer T1-A de `contradiction` (0.77) à `coherent` (P(contradiction) 0.34) ; inverser R1 fait tomber P(A > D) de 0.95 à 0.28. Jev lit ces deux règles.
   - [VÉRIFIÉ] Retirer la règle ne change presque rien : sans R1, Jev « déduit » encore A > D (0.90, 0/3 conformes) ; sans R2, il voit encore une contradiction (0.70, 0/3). Même chose quand la règle est remplacée par une phrase hors sujet de même longueur (0.85 ; 0.63).
   - [HYPOTHÈSE] Jev complète l'état avec le sens usuel de « > » (transitif) et de « incompatible ». La consigne « uniquement à partir des faits et règles donnés » n'est pas respectée. Ce n'est pas de la plausibilité de surface au sens « longueur ou forme de l'état » : (ii), sans phrase, et (iv), avec phrase, donnent le même résultat.
   - [VÉRIFIÉ] Ajouter une phrase hors sujet à côté de la règle ne change pas la réponse (A1 : 0.70 contre 0.77 ; A2 : 0.96 contre 0.95).
3. **Distracteurs : ce n'est pas « n'importe quel ajout ».**
   - [VÉRIFIÉ] Le fait redondant A > C tue encore la contradiction (0.34, identique à L-DIS1 d'E006) et fait retomber P(E > D) à 0.19. L'autre fait redondant, B > D, ne la tue pas (0.78). La règle 3 seule, non pertinente, la tue (0.38, coherent ×3). Le fait `couleur(A, rouge)` seul est au seuil (0.49). Une phrase hors sujet ne la tue pas (0.70).
   - [HYPOTHÈSE] L'effet dépend de l'élément ajouté, pas de sa seule présence : A > C touche la chaîne E → A → … → D, B > D non. Ce n'est établi que sur 4 distracteurs, un seul ordre, 3 appels chacun.
4. **Sur l'hypothèse de départ.** [HYPOTHÈSE] « Jev juge la plausibilité de surface, pas les règles » est **trop forte** sous cette forme. Plus précis sur ces 27 cas : Jev part d'un a priori (sens usuel des symboles, forme d'une phrase qui « a l'air » soignée) ; une règle écrite qui contredit cet a priori le fait bouger fortement ; une règle absente ne l'empêche pas d'appliquer son a priori.

**Attente que j'aurais eu envie de discuter après avoir vu Jev (non modifiée)** : A2-ii et A2-iv (attendu `false`). On peut soutenir que « > » porte conventionnellement la transitivité, donc que A > D « se déduit » même sans R1. L'attente `false` est conservée : la consigne dit « uniquement à partir des faits et règles donnés ». Mais la réponse de Jev a une lecture défendable, ce qui affaiblit ce point comme preuve d'erreur. Le même argument vaut pour A1-ii / A1-iv (`incompatible` a un sens usuel).

## Limites

- 27 cas, 2 à 5 appels par cas : **aucune conclusion générale**. Deux bases seulement pour l'ablation ; trois paires pour la grammaire.
- Les réponses répétées sont très stables (souvent ±0.02) : les appels mesurent la reproductibilité, pas la robustesse à la reformulation.
- C : la règle cite l'exemple même de la phrase ; la comparaison « sans règle » vient d'E006 (≈ 1 h plus tôt). Le rappel C0 montre une dérive ≤ 0.07 (0.61 → 0.54 ; 0.90 → 0.92 ; 0.67 → 0.74), bien plus petite que les écarts mesurés (≥ 0.21 sauf F1-05 correcte, déjà à 0.90).
- A : une seule forme d'inversion par règle ; les phrases hors sujet ont la même longueur en caractères, pas en jetons.
- B : un seul ordre, une seule position de distracteur.
- Écart au mandat sur (iv) : voir « Règles de lecture ».
- Fournisseurs non distingués (`typesafe-ai` ×80, `digitalocean` ×10).

## Prochaine étape

1. **Règle fausse écrite** (grammaire et logique) : une règle d'accord erronée mais plausible, et une règle logique non standard sans rapport avec l'a priori (ex. « si X > Y alors Y > X »). Si Jev la suit, il applique le texte ; sinon, il ne s'en sert que quand elle confirme la bonne réponse.
2. **Règle sans l'exemple** : même règle d'accord formulée de façon générale, sans citer le verbe de la phrase, pour séparer application et correspondance de mots.
3. **Consigne « règles données seulement »** : variantes (ii) avec une consigne renforcée (« n'utilise aucune propriété de > qui n'est pas écrite »), pour savoir si l'a priori se laisse désactiver.
4. **Distracteurs** : même distracteur à plusieurs positions et faits redondants touchant ou non la chaîne de la question.
