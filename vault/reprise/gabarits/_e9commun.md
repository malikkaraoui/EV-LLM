## Cadre commun E009–E011 (décision Malik 27/09 : explorer A et B à fond)
- Question de fond : un système peut-il **apprendre la procédure** de l'addition sur des nombres courts et la généraliser à toute longueur, comme un enfant ? Palier 0 (E008, branche `exp/e008-addition`, tip `af281f5`, lire README + `vault/echanges/archive/2026-09-26-F01-M0021-e008-addition-palier0.md`) : transformer standard 0 % dès 6 chiffres ; sortie inversée + NoPE 91 % à 6, 8 % à 7, 0 % dès 8.
- **Réutilise** le code E008 (données, évaluateur unique, contrôles) **par import depuis ta branche créée à partir de `origin/exp/e008-addition`**, sans modifier `research/experiments/E008-addition/`.
- **Protocole durci (revue critique orchestrateur, sources arXiv 2108.12284, 2402.09371, 1611.00736)** — obligatoire, préenregistré :
  1. Entraînement : opérandes 1–5 chiffres (comme E008). **Validation OOD séparée : 6–8 chiffres**, seule autorisée pour choisir checkpoint/hyperparamètres. **Test final intouché : 10, 16, 32, 64, 100 chiffres**, évalué une seule fois à la fin.
  2. **Tests adverses** (en plus) : retenues en cascade (99…9 + 1), nombres pleins de zéros (100…002 + 100…003), **longueurs asymétriques** (100 chiffres + 3 chiffres).
  3. **≥ 5 graines** pour tout système déclaré « réussi » ; exact-match séquence entière, moyenne ± écart **et** nombre de graines réussies (≥ 90 % à 16 chiffres).
  4. **Exemples uniques ≠ pas d'optimisation** : journaliser le nombre d'exemples **uniques** vus.
  5. C-ORACLE = 100 % et C-PARCŒUR = 0 % recalculés sur tous les nouveaux jeux (validité, leçon M0020).
  6. **Budget de structure** : pour chaque système, une ligne qui dit ce qui est donné à la main (format, localité, nombre d'itérations, traces) — rien de caché.
  7. « Faux et sûr » (faux avec confiance ≥ 0,8) et, si le système s'abstient, taux d'abstention quand il a tort (autodiagnostic).
- Machine : Mac M1 16 Go, MLX (venv `$HOME/.venvs/ev-llm-e008`, réutilisable ; ajoute des paquets seulement si justifié). **Plusieurs fenêtres entraînent en parallèle** : budget **≤ 4 h de calcul** pour ton mandat ; si le partage du GPU ralentit trop, réduis (moins de pas / de variantes) et écris-le, ne dépasse pas. Entraînement par invocations ≤ 9 min avec reprise sur checkpoint ; aucune tâche de fond, aucun `sleep`.
- Ordre des commits : préenregistrement (poussé seul) < code < valeurs figées après pilote (pilote = graine 0, exclue) < résultats.
