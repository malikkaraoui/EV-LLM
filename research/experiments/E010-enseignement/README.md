# E010 — « B » : enseigner la règle comme à l'école (brouillon de colonnes)

Mandat M0023, 2026-09-27, branche `exp/e010-enseignement` (depuis `origin/exp/e008-addition`
@ `af281f5`). Préenregistrement : [`PREREGISTREMENT.md`](PREREGISTREMENT.md) (amendement A1 :
lr et nombre de pas figés après pilote). Résultats bruts : [`resultats/`](resultats/)
(`summary.md` : tous les jeux, valeurs par graine ; `resultats.json` ; `courbe.csv`).

## Question

Un enfant ne découvre pas la retenue seul : on la lui **montre**. Pour le même petit transformer
qu'E008 (≈ 3,2 M paramètres, entraîné sur des opérandes de 1 à 5 chiffres), qu'apporte
l'enseignement explicite : **(Q1) combien d'exemples faut-il pour ≥ 95 % dans la distribution ?
(Q2) donne-t-il la généralisation en longueur (jusqu'à 100 chiffres) ?**

## Conditions

4 formats × 2 positions (absolues apprises / **NoPE**), mêmes exemples dans le même ordre pour
une graine donnée :

- **F0** réponse seule (format B-STD d'E008) ;
- **F1** brouillon de colonnes : pour chaque colonne depuis les unités, `aᵢ bᵢ cᵢ sᵢ cᵢ₊₁ ;`
  (chiffre de a, de b, retenue entrante, chiffre écrit, retenue sortante), puis `#` et la somme ;
- **F2** une ligne de règle constante en tête (« on additionne colonne par colonne depuis la
  droite, on reporte 1 si ≥ 10 ») puis F0 ;
- **F3** F1 avec la somme finale inversée (ablation).

### Budget de structure (ce qui est donné à la main)

| format | donné à la main | pas donné |
|---|---|---|
| F0 | format `a+b=`, un token par chiffre, fin | tout le reste |
| F1 | **l'algorithme entier en traces** : ordre des colonnes, chiffres recopiés, retenues, chiffre écrit ; nombre d'itérations implicite (une colonne par chiffre) | la **localité** : quel chiffre lire (ni index, ni alignement, ni position) |
| F2 | F0 + une phrase constante (zéro information propre à l'exemple) | idem F0 |
| F3 | F1 + réponse dans l'ordre du brouillon | idem F1 |
| abs / NoPE | abs : table de positions apprise ; NoPE : ordre porté par le seul masque causal | — |

## Protocole (résumé ; détails au préenregistrement)

- Entraînement : réserves de paires **uniques** (1–5 chiffres, longueurs uniformes), 1 000 pas
  × 256, AdamW lr 3e-3 (montée 150, cosinus), float32, MLX 0.29.3 sur M1 (GPU **partagé**
  avec une autre fenêtre). Réserve maximale 256 000 : chaque exemple vu une fois.
- Validation OOD (seule utilisée pour les choix) : 6, 7, 8 chiffres. **Test final intouché**,
  évalué une seule fois : 10, 16, 32, 64, 100 chiffres (200/L) + **adverses** (retenue en
  cascade `99…9 + 1`, pleins de zéros `10…02 + 10…03`, asymétriques L + 3 chiffres ; 20/type/L).
- Évaluateur **unique d'E008** (importé), exact-match sur la réponse finale ; décodage glouton
  avec cache clé/valeur (test : cache = sans cache).
- Graines officielles 1 et 2 (criblage) ; règle des 5 graines pour toute condition > 50 % à
  8 chiffres — **aucune ne l'a atteinte**, donc aucune extension. Pilote graine 0 exclu.
- Calcul consommé : entraînement officiel 153,8 min, pilote 26,3 min, test final 11,2 min,
  évaluations de criblage ≈ 1 min : **≈ 192 min** (budget 240).

## Validité

| contrôle | attendu | obtenu (tous jeux, 4 900 items) |
|---|---|---|
| C-ORACLE (retenue codée à la main) | 100 % | **100 %** partout |
| C-ORACLE-TRACE (brouillon F1/F3 de l'oracle relu par l'analyseur des modèles) | 100 % | **100 %** partout |
| C-PARCŒUR (table des 256 000 paires de la graine 1) | ≤ 1 % hors T-ID1 | **0 %** ; T-ID1 : 100 % (témoin) |

**TEST VALIDE** [VÉRIFIÉ] (`resultats/controles.json`, commit `7c83241`, avant tout modèle officiel).

## Résultats

### Test final (exact-match %, moyenne ± écart, graines 1 et 2 ; T-ID et V-OOD 500/L)

| condition | T-ID moy. 2–5 | T-ID 5 | V-OOD 6 | V-OOD 7 | V-OOD 8 | T-FIN 10–100 | adverses |
|---|---|---|---|---|---|---|---|
| F0-abs | 1,6 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| F0-NoPE | 33,1 | 6,3 ± 3,0 | 0,3 | 0,1 | 0,0 | 0,0 | 0,0 |
| **F1-abs** | **98,1** | 97,6 ± 1,1 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| **F1-NoPE** | **99,9** | 99,6 ± 0,0 | **33,1 ± 5,5** (29,2 / 37,0) | 0,0 | 0,0 | 0,0 | 0,0 |
| F2-abs | 1,2 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| F2-NoPE | 35,0 | 23,3 ± 33,0 (0,0 / 46,6) | 2,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| **F3-abs** | **100,0** | 100,0 | 0,0 | 0,0 | 0,0 | 0,0 | 0,0 |
| **F3-NoPE** | **99,7** | 98,9 ± 0,4 | 10,6 ± 13,9 (20,4 / 0,8) | 0,0 | 0,0 | 0,0 | 0,0 |

Graines « réussies » (≥ 90 % à 16 chiffres) : **0/2 pour les 8 conditions**. Aucune condition
« réussie ». Pour mémoire, E008 B-REF (NoPE + sortie inversée, 12 000 pas, 3,1 M exemples) :
91 % à 6 chiffres, 8 % à 7, 0 % dès 8 — budget 12 × plus grand, non comparable directement.

### Courbe d'efficacité (graine 1, 1 000 pas appariés, T-ID 200/L)

| exemples uniques | F0-abs | F0-NoPE | F1-abs | F1-NoPE |
|---|---|---|---|---|
| 1 000 | 0,5 | 0,1 | 30,6 | 46,0 |
| 10 000 | 2,1 | 33,4 | 91,1 | **99,9** |
| 100 000 | 2,3 | 65,8 | **99,9** | 100,0 |
| 256 000 | 1,6 | 35,1 | 97,1 | 100,0 |

(T-ID moyen 2–5, %. V-OOD 6 de F1-NoPE : 0 / 43,0 / 18,5 / 28,5 % ; V-OOD 7–8 : 0 partout.)

**Exemples uniques nécessaires pour T-ID ≥ 95 %** : F1-NoPE **10 000** ; F1-abs **100 000** ;
F0-NoPE et F0-abs : **jamais sur la grille (> 256 000)** dans ce budget de 1 000 pas.

### Diagnostics

- F1-NoPE, V-OOD 6 (2 graines) : la réponse recopie son propre brouillon dans **957 / 1 000**
  cas, mais le brouillon n'est entièrement juste que dans **345 / 1 000** : les erreurs sont
  **dans le brouillon** (lecture du bon chiffre, arrêt), pas dans la recopie. À 8 chiffres :
  307 / 1 000 non-réponses, et seulement 44 des 693 réponses fausses ont la bonne longueur.
- Au-delà de 10 chiffres, F1-NoPE ne produit presque jamais de réponse terminée (T-FIN 10 :
  397 / 400 abstentions, T-FIN 16 : 400 / 400) : le brouillon ne s'arrête pas / ne mène pas à `#`.
- « Faux et sûr » : F1-NoPE V-OOD 6 : **606 / 669** faux sont sûrs (≥ 0,8). La confiance
  préenregistrée porte sur la réponse finale seule, qui est une recopie du brouillon : elle
  mesure la sûreté de la recopie, pas celle du calcul — elle **ne détecte pas** l'erreur.
  Positions absolues (F0, F1, F2, F3-abs) : 24–74 % de faux sûrs à 6–8 chiffres ; F0-NoPE et
  F2-NoPE : 0 (erreurs peu sûres).
- T-ID1 (1 chiffre + 1 chiffre) est bas pour plusieurs conditions (F1-abs 74 %, F3-abs 18 %)
  alors que T-ID 2–5 ≈ 100 % : la réserve d'exemples **uniques** ne contient que 100 paires à
  1 + 1 chiffre sur 256 000 (conséquence assumée du dédoublonnage, §3 du préenregistrement).

### Prédictions préenregistrées

| | prédiction | verdict |
|---|---|---|
| P1 | F1-NoPE atteint 95 % avec ≥ 10 × moins d'exemples que F0-NoPE | **confirmée** : 10 000 contre jamais (> 256 000) — avec le biais de lr signalé (A1) |
| P2 | F2 ≈ F0 (± 5 pts, T-ID moyen et V-OOD 6) | **confirmée** (1,2 vs 1,6 ; 35,0 vs 33,1 ; V6 0 vs 0 ; 2,0 vs 0,3) — les deux près du plancher |
| P3 | F1-abs et F3-abs ≤ 10 % à V-OOD 8 | **confirmée** (0 %, et déjà 0 % à 6) |
| P4 | F1-NoPE > F0-NoPE de ≥ 20 pts à V-OOD 6 | **confirmée** (33,1 contre 0,3) |
| P5 | F3-NoPE ≥ F1-NoPE à V-OOD 8 | confirmée **à vide** (0 = 0) ; à V-OOD 6, F3-NoPE est **inférieur** (10,6 contre 33,1) |
| P6 | aucune condition « réussie » (≥ 90 % à 16) | **confirmée** (0/2 partout ; 0 % à 10 chiffres et au-delà) |

## Lecture — combien d'exemples l'enseignement fait-il gagner, et donne-t-il la généralisation en longueur ?

- [VÉRIFIÉ] **Dans la distribution, l'enseignement fait gagner beaucoup** : avec le brouillon
  de colonnes et NoPE, **10 000 exemples uniques** suffisent pour 99,9 % (1 000 pas) ; sans
  brouillon, le même modèle, les mêmes pas et les mêmes exemples plafonnent à 33–66 % avec
  10 000 à 256 000 exemples. Au moins **25 ×** moins d'exemples sur cette grille (borne basse :
  F0 n'atteint jamais 95 %). E008 donnait à F0 (B-STD) 98–100 % après 3,1 M exemples et
  12 000 pas : l'écart réel en exemples est donc de l'ordre de 10² à 10³ ×, **à budget de pas
  différent** [HYPOTHÈSE sur l'ordre de grandeur exact].
- [VÉRIFIÉ] **La règle énoncée seule (F2) n'apporte rien** mesurable : même niveau que F0, et
  instable (F2-NoPE : 0 % ou 47 % à 5 chiffres selon la graine). Une phrase constante n'est pas
  un enseignement pour un modèle qui ne lit pas la langue.
- [VÉRIFIÉ] **L'enseignement ne donne pas la généralisation en longueur** ici : meilleur cas
  F1-NoPE, 33 % à 6 chiffres (+1), **0 % à 7, 8, 10, 16, 32, 64, 100** et sur tous les
  adverses, sur les 2 graines. Avec positions absolues, le brouillon donne 98–100 % dans la
  distribution et **0 % dès 6 chiffres**.
- [VÉRIFIÉ] L'échec hors longueur est un échec de **localité**, pas de règle : le modèle
  applique la retenue et recopie correctement, mais ne sait plus **quel chiffre lire** ni
  **quand s'arrêter** — précisément la seule chose que la trace ne lui donne pas (budget de
  structure). Ce qui généralise dans la littérature (NPI, index hints, Abacus) donne justement
  cette localité à la main.
- [VÉRIFIÉ] L'ablation F3 (réponse inversée) n'aide pas : le goulot n'est pas la relecture du
  brouillon.
- [HYPOTHÈSE] Avec plus de pas (E008 : 12 000), F1-NoPE monterait probablement à 6 chiffres
  (comme B-REF de 58 % à 91 %) ; rien n'indique qu'il franchirait 8 chiffres.
- Aucune conclusion au-delà de : addition, ~3,2 M paramètres, 1 000 pas, ces formats, 2 graines.

## Limites

- **1 000 pas seulement** (budget 4 h sur M1 partagé) ; F0 n'a pas convergé dans la
  distribution — la comparaison Q1 porte sur « à pas égal », et le lr 3e-3 choisi sur V-OOD
  défavorise F0 (pilote : 57,5 % contre 37,5 % à T-ID 5 à 1e-3). Biais signalé avant les runs.
- Le point « 1 000 000 d'exemples uniques » demandé n'est pas atteint (256 000 au maximum).
- Courbe à une seule graine ; conditions finales à 2 graines (aucune n'a déclenché les 5).
- Brouillon en notation compacte (sans `+ = ,` constants) ; confiance sur la réponse finale
  seule (préenregistré) — mesure faible de l'autodiagnostic pour F1/F3.
- T-FIN 200 items / L, adverses 20 / type / L.

## Rejouer

```
PY=$HOME/.venvs/ev-llm-e008/bin/python        # mlx 0.29.3, numpy 2.0.2 (requirements.txt)
cd research/experiments/E010-enseignement
$PY -m unittest -v test_e010                   # 10 tests
$PY validite.py                                # controles -> resultats/controles.json
$PY entrainer.py --plan crible                 # relancer tant que finis < total (<= 8,8 min / invocation)
$PY entrainer.py --plan courbe                 # idem
$PY evaluation.py --run <runs...>              # criblage (T-ID, V-OOD 200/L)
$PY evaluation.py --final --run <runs N256000> # test final, une seule fois par run
$PY analyse.py                                 # resultats/resultats.json, summary.md, courbe.csv
```

Checkpoints et journaux item par item (`runs/`) hors git. GPU MLX non déterministe au bit.
