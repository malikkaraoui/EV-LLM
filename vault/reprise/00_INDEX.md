---
date: 2026-09-25
tags: [reprise, sessions, tableau-de-bord]
maintenu_par: orchestrateur
derniere_maj: 2026-09-26T18:03:33+02:00
---

# Tableau de bord — sessions du projet ev-llm

<!-- rotation-index -->
> **Index court (rotation).** Seuls les derniers jours d'activité sont ici. L'historique complet
> est dans `vault/reprise/archive/index/00_INDEX-AAAA-MM.md` — le chercher par mots-clés, ne
> jamais le charger en entier. Le hook `pre-commit` livré avec ce scaffold refuse un commit qui
> ferait dépasser la limite d'octets à ce fichier, et imprime le remède : c'est le seul garde-fou
> contre un index de plusieurs centaines de kilo-octets relu à chaque démarrage de session.

<!--
CONVENTION D'ÉCRITURE — une entrée par mandat ou revue traité, ordre ANTI-CHRONOLOGIQUE
(le plus récent en tête, immédiatement sous ce bloc). Format d'une entrée :

## <horodatage ISO 8601 avec fuseau> — <Mxxxx|R0xx> (<Fxx>) : <verdict en UNE phrase>

- <fait vérifiable, avec son pointeur : rapport, branche, SHA — jamais un ressenti>
- <ce qui est mergé / non mergé, et ce qui bloque, nommé>
- <réserve ou trou assumé, s'il y en a un — l'absence de réserve se dit aussi>
- <leçon ou décision rattachée, par lien>

Règles :
- Le titre H2 porte le VERDICT, pas le sujet : il doit se lire seul, sans ouvrir le rapport.
- 2 à 4 puces, pas davantage : ce fichier est un index, pas un rapport.
- Jamais de narration : ce qui mérite d'être raconté va dans `vault/revues/`, et l'entrée pointe.
- Cette entrée est une DÉCLARATION, pas une preuve (voir `vault/runtime/README.md`).

Exemple (à supprimer à la première entrée réelle) :

## AAAA-MM-JJTHH:MM:SS+00:00 — <R0xx> (<Fxx>) doublage de <Mxxxx> : GO, mergé <sha court>

- Rapport : `vault/revues/AAAA-MM-JJ-<R0xx>-<slug>.md` ; branche `<branche>` (tip `<sha>`).
- Symptôme d'origine rejoué avant/après ; tests re-mesurés par le doubleur, pas repris du rapport d'auteur.
- Réserve non bloquante : <réserve nommée, ou « aucune »>.
-->

## 2026-09-26T18:03:33+02:00 — Vague 5 : **E005 mergé (R007 GO)** ; E006 en RÉSERVE (2 « faux et sûr » reclassés contestés) ; A0-bis échoue 0/4 ; défaut fournisseur E003 ; vague 6 posée

- R007 GO 7/7 → E005 mergé (`e1448c4`). R008 ⚠️ E006 : R-F4-04 et L-DIS1 **contestés** (question ambiguë dans un ensemble contradictoire) → compte honnête : **5 faux et sûr non contestés + 1 contesté** (et non 6) ; correctif README M0018.
- M0015 E003 `bbc50ae` : raw.public.jsonl + `.gitignore` pilot/. **Défaut orchestrateur** : aucun fournisseur imposé ni journalisé (gemini servi via Vertex) → backend non contrôlé ; M0019 (fournisseur imposé, 402 = arrêt), rejeu M0021.
- M0016 A0-bis `1be4654` : ÉCHEC ACQUÉRIR 0/4 ; coût marginal active 22.6 requêtes, exactitude 0.83, R̂_diff −0.0105 ; MLE de bruit biaisé (échantillon sélectionné).
- Vague 6 : M0018 E006 Lecture · M0019 E003 fournisseur · R009 doublage A0+A0-bis · **M0020 ACQUÉRIR atteignable ? (oracle) puis A0-ter** · M0017 E007 toujours en vol.

## 2026-09-26T17:32:59+02:00 — Vague 4 : **E006 réplique les 6 « faux et sûr » de Jev** ; A0 échoue ACQUÉRIR (cause trouvée) ; doc v2.2 mergée ; vague 5 posée

- M0011 E006 `57e0e41` : 6/6 répliqués (5/5 appels) ; forme **correcte** notée plus bas que la forme fautive sur 2/3 paires ; T1-A perd la contradiction dès 1 distracteur ; pas de pente 2–6 pas ; contamination disjointe nulle (|écart| ≤ 0.012). 103×200 à 26 s.
- M0014 A0 `8a60250` : ÉCHEC ACQUÉRIR (1/4) ; meilleur système sans propriétés données (R̂_diff −0.011) ; déclencheur inerte (coût absolu vs R rapport) → A0-bis.
- R006 GO → doc v2.2 + GENESE mergées (réserve : GENESE cite l'enfant de Malik — décision de Malik). R005 ⚠️ (raw.jsonl suivis) → M0015. M0013 → E005 corrigé `15487b0`.
- Vague 5 : R007 (E005) · M0015 (E003) · R008 (E006, merge après E005) · M0016 A0-bis · M0017 E007 « Jev lit-il les règles ? ».

## 2026-09-26T17:08:23+02:00 — Vague 3 : E002-bis mergé (R003 GO), E005 CASSÉ sur un total (R004), E003 complet, doc v2.2 prête ; vague 4 posée

- R003 GO → E002-bis mergé (`main` contient d35af60). R004 ⛔ : totaux HTTP du README E005 faux (7×503/110×429) — **les 6 « faux et sûr » de Jev sont confirmés par sources (0 contesté)** ; correctif M0013.
- M0010 E003 `73cdc79` : 60/60 mesuré, 0×429 grâce au rythme 26 s ; seul « faux et sûr » : gpt-4.1-mini sur T1-A `e_sup_d` (contamination ?).
- M0012 doc `bcfb722` : GENESE +11 entrées, architecture v2.2 (D17–D21).
- Vague 4 : M0013 correctif E005 · R005 doublage E003 · R006 doublage doc v2.2 · **M0014 A0, premier candidat ACQUÉRIR** · (M0011 E006 toujours en vol).

## 2026-09-26T16:38:48+02:00 — Vague 2 rendue : E001+E002 mergés (GO), mesure E002 réparée, **premiers « faux et sûr » de Jev** ; vague 3 posée

- R001 GO → E001 mergé ; R002 GO → E002 mergé (`main` contient 7e953a9 et 1cb586b ; `main` = df79ad6).
- M0007 E002-bis `d35af60` : plafond-vérificateur R > 0 sur 20/20 — mesure réparée. M0008 E003 `01f3c8f` partiel : 429 = **limite passerelle 5 req/min/équipe** ; LLM-2 tronqué ; LLM-1 faux et sûr sur T1-A `e_sup_d`.
- **M0009 E005 `08d80f7` : Jev faux et sûr sur 6 questions** (accords pronominaux, « fait faire », « ci-jointe » à confirmer, contradiction masquée par distracteurs, chaîne de 4 pas) — 1 à 2 réponses chacune, à répliquer.
- Vague 3 : R003 (E002-bis), R004 (E005 + vérif grammaticale), M0010 (E003 rythmé), M0011 (E006 réplication + contamination E004), M0012 (doc v2.2 + GENESE).

## 2026-09-26T16:14:20+02:00 — Vague 1 rendue (M0003–M0006) ; vague 2 posée (R001, R002, M0007–M0009)

- M0003 ✅ T2 : 4/4 conforme, 0 « faux et sûr » (fautes fréquentes) — `exp/e001-sonde-jev` 7e953a9. M0004 ✅ 17 issues (#1–#17) + index `vault/notes/2026-09-26-issues-github.md`.
- M0005 ✅ E002 banc (22 tests) — plafond R ≤ 0 sur 12/20 sous bruit : mesure à réparer (E002-bis). M0006 ⛔ STOP 403 free tier LLM-2 — 2/70 appels.
- Incident : `state.json` écrasé par une fenêtre (compteurs perdus) — reconstruit depuis `events.jsonl` ; garde ajoutée aux rituels.
- Vague 2 : R001 (doublage+merge E001), R002 (doublage+merge E002), M0007 E002-bis, M0008 E003 relance, M0009 E005 Jev hors distribution.

## 2026-09-26T15:53:49+02:00 — M0003–M0006 (F01–F04) posés en parallèle : rejeu T2, issues GitHub, E002, E003

- Décision Malik 26/09 15:50 : rejeu T2 avant doublage ; enchaîner les pistes en parallèle ; issues GitHub pour ne rien oublier.
- F01/M0003 `exp/e001-sonde-jev` (T2 seul, réparti) · F02/M0004 `main` (labels + 17 issues + `vault/notes/2026-09-26-issues-github.md`) · F03/M0005 `exp/e002-relations-opaques` (banc « acquérir » + 3 étalons, sans réseau) · F04/M0006 `exp/e003-etalon-llm` (2 LLM via AI Gateway, ≤ 70 appels).
- Branches et fichiers disjoints ; F01 et F04 appellent la même passerelle (risque 429 partagé, assumé).

## 2026-09-26T10:46:10+02:00 — M0002 (F01) : première mesure Jev partielle — T1 6/6 conforme, T2 non servi (429/503)

- Rapport : `vault/echanges/F01.md` § Rapport M0002 ; branche `exp/e001-sonde-jev` tip `08672e4` (non doublée, non mergée) ; `main` = `7c453b1`.
- 21 appels : 7×200, 3×503 (digitalocean), 11×429 (passerelle) — vérifié par l'orchestrateur dans `raw.public.jsonl`.
- T1-A « contradiction » / T1-B « indéterminé » distingués, stables 3/3 ; `e_sup_d` affaibli en présence de contradiction (0.49–0.58 vs 0.73–0.78) [hypothèse].
- Bloquant scientifique : T2 (erreurs invisibles) entièrement non mesuré. Décision Malik attendue : rejeu T2 seul avant doublage R001.

## 2026-09-26T10:28:42+02:00 — M0002 (F01) posé : rejeu E001 après carte Vercel, en attente de rendu

- Mandat : `vault/echanges/F01.md` ; branche `exp/e001-sonde-jev` (tip `2719279`), même worktree ; `cases.json` figé (sha256 `8325775b…`).
- Publication : `raw.public.jsonl` sans en-têtes de réponse ; `raw.jsonl` gitignoré.
- Archive M0001 : `vault/echanges/archive/2026-09-25-F01-M0001-e001-sonde-jev.md`.

## 2026-09-25T21:46:59+02:00 — M0001 (F01) : BLOCKED propre, sonde Jev construite mais 403 facturation Vercel sur 21/21 appels

- Rapport : `vault/echanges/F01.md` § Rapport M0001 ; branche `exp/e001-sonde-jev` tip `2719279` (non doublée, non mergée).
- Livré : `.env` ignoré par `.gitignore`, `run.py` stdlib + garde anti-fuite testée hors ligne, `cases.json` sha256 `8325775b…` figé.
- Bloquant : `customer_verification_required` — carte à enregistrer sur Vercel (geste Malik), puis rejeu à l'identique (nouveau dossier results/).
- Réserve orchestrateur : l'accès réel n'a pas été testé à la pose (contradiction « Free » / « $0.042 » vue et non creusée).

## 2026-09-25T21:30:40+02:00 — M0001 (F01) posé : sonde Jev e001, en attente de rendu

- Mandat : `vault/echanges/F01.md` ; branche à créer `exp/e001-sonde-jev` depuis `origin/main` = `343e839`.
- Périmètre : ignorer `.env` (dépôt public), script Python stdlib `research/experiments/E001-jev-sonde/run.py`, 7 cas préregistrés, sortie brute conservée.
- Décision : GO de Malik 25/09 21:30 (« Lance !! »).
