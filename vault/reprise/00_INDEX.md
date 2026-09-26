---
date: 2026-09-25
tags: [reprise, sessions, tableau-de-bord]
maintenu_par: orchestrateur
derniere_maj: 2026-09-26T16:14:20+02:00
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
