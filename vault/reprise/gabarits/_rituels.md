## Rituels

DÉBUT : `statut: en-cours` à la racine du frontmatter de CE fichier, avant tout.

FIN, dans l'ordre :
1. Rapport appendé sous `## Rapport <mandat_id>` (preuves collées).
2. `vault/reprise/<Fxx>.md` (état + prochaine étape) — à la racine.
3. Une ligne `vault/runtime/events.jsonl` (`src: "fenetre"`, `type: "RAPPORT_RENDU"`, `f`, `mandat`, `note` ≤ 200 car.) + `windows.<Fxx>` dans `vault/runtime/state.json` — hors git, jamais committés. **state.json : lecture JSON → modification de la SEULE clé `windows.<Fxx>` → réécriture ; toutes les autres clés (`schema_version`, `next_mandat_id`, `next_revue_id`, `projet`, autres fenêtres) sont conservées à l'identique. Vérifie après écriture que `next_mandat_id` est toujours présent (incident du 26/09 : state.json écrasé).** Toute ligne `events.jsonl` porte `ts` (horloge réelle `TZ=Europe/Paris date +%Y-%m-%dT%H:%M:%S%:z`).
4. Commit de `vault/reprise/<Fxx>.md` sur `main` à la racine (vault seul) + push + `git ls-remote origin refs/heads/main` collé.
5. Ta branche (s'il y en a une) poussée + `git ls-remote origin refs/heads/<branche>` collé.
6. Footer de statut, toute dernière ligne du rapport :
```
<mandat_id>
Implementation      ✅/❌
Tests               ✅/❌
Commit              ✅/❌
Branch push         ✅/❌
Review              ❌
Merge main          ❌
Main push           ✅/❌   (vault seul)
TASK STATUS         <READY_FOR_INTEGRATION | BLOCKED>
PROJECT STATUS      NOT_INTEGRATED
```
7. EN DERNIER GESTE : `statut: reponse-disponible`.
