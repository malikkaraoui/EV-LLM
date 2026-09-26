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

*(à remplir après les appels)*
