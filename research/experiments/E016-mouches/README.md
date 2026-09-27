# E016 — « mouches » : des agents aux codes privés incompatibles inventent-ils une langue commune pour un but commun ?

Mandat M0031, 2026-09-27, branche `exp/e016-mouches` (depuis `exp/e014-reperage` @ `fc698b4`).
Préenregistrement : [`PREREGISTREMENT.md`](PREREGISTREMENT.md) (poussé seul avant le code,
amendement A1 après le pilote). Code E008, E013, E014 importé, non modifié.

## En une phrase

**Non.** Trois « lecteurs » et trois « additionneurs » gelés, reliés par un canal de 48 symboles
sans sens et récompensés **uniquement** par le succès, n'inventent **aucune** langue commune (0 symbole
partagé par les trois émetteurs, 25 runs sur 25) : chaque graine voit **une ou deux paires isolées**
se forger un **code privé parfait** (idiolecte), et toutes les autres paires restent à 0. La règle
« tout-ou-rien collectif + tout le monde recommence » ne pousse pas vers une langue commune : dès que
l'équipe compte 3 paires, elle ne reçoit **plus jamais** de récompense et l'apprentissage s'arrête.
Ce qui marche, en revanche, marche très bien : chaque idiolecte appris sur 1–5 chiffres additionne
exactement jusqu'à 100 chiffres.

## Idée (Malik, 27/09) et en quoi E016 diffère de l'existant

« 3 mouches savent une chose (langage A), 3 une autre (langage B), un espace de discussion, un but
commun ; la récompense vient de réponses à tour de rôle puis en équipe ; si une se trompe, tout le
monde recommence. »

Veille (≈ 10 min, détail dans le préenregistrement §0) :

1. Lewis → communication émergente neuronale (Foerster 2016, Lazaridou 2017, Mordatch & Abbeel
   2018) : agents vierges, désigner un objet.
2. Populations (Tieleman 2019, Graesser 2019, Rita 2022 arXiv 2204.12982) : langue partagée contre
   idiolectes, avec une perception identique pour tous les agents.
3. **Déjà fait, contrairement à l'hypothèse de l'orchestrateur** [VÉRIFIÉ, veille] : Mahaut, Dessì,
   Franzon, Baroni (arXiv 2302.08913, TMLR 2025) : des réseaux visuels **pré-entraînés, gelés,
   hétérogènes** construisent un protocole commun, et un nouveau venu l'apprend facilement.
4. Ce qu'E016 ajoute [HYPOTHÈSE, veille courte] : des compétences gelées **procédurales**
   (lire en colonnes / additionner avec retenue), un calcul **coupé en deux** par le canal, un
   protocole appris sur 1–5 chiffres puis jugé jusqu'à 1 000, une récompense **par succès
   seulement** (REINFORCE) et la règle collective de Malik contre une récompense individuelle.
5. [VÉRIFIÉ par construction] Pour un émetteur ou un récepteur **tabulaire**, un code privé bijectif
   n'est qu'un renommage. Ce qu'il garantit : aucune convention n'est partagée au départ.

## Montage (préenregistré)

- **A1, A2, A3** : lecteurs E014 `R1L-s1`, `s3`, `s4` gelés (poser en colonnes depuis `a+b=`), sortie
  ré-étiquetée par une permutation privée π_i. **B1, B2, B3** : accumulateurs I1 H = 4 d'E013
  (graines 1, 2, 3) gelés, entrée lue à travers leur propre permutation σ_j.
- **Canal** : V = 48 symboles (assez pour 3 dialectes disjoints : une langue commune n'est **pas**
  forcée par la pénurie). Par colonne, A_i écrit 2 symboles (un par opérande), B_j les traduit dans
  son code. Seules les tables émetteur (11 × 48) et récepteur (48 × 11) apprennent, par REINFORCE
  (récompense 0/1, ligne de base = moyenne du lot par longueur), Adam lr 0,05, β = 0, 4 000 pas,
  128 tours par pas.
- **Phase 1 « à tour de rôle »** (pas 0–1 999) : 1 paire (A_i, B_j) tirée au hasard par tour.
  **Phase 2 « en équipe »** (2 000–3 999) : 3 paires par tour (appariement parfait aléatoire).
- **COLL (règle de Malik)** : récompense de tous = 1 ssi **toutes** les réponses du tour sont
  exactes ; un tour raté est **rejoué** (mêmes problèmes, nouveau tirage des paires), jusqu'à 4 fois.
  **IND (témoin a)** : récompense par paire, pas de rejeu. **COUPÉ (témoin b)** : le récepteur reçoit
  toujours le symbole 0. **DONNÉ (témoin c)** : interface exacte σ_j ∘ π_i⁻¹, aucun apprentissage.
- Sélection sur VAL-OOD 6–8 chiffres seule (9 paires) ; TEST lu une fois : T-ID 2–5, T-LONG
  10/16/32/64/100/1 000, ADV-CASCADE / ZEROS / ASYM 10–1 000 (jeux E014 identiques), **les 9
  paires** de chaque graine. Graines 1–5 ; pilote graine 0 exclu (`resultats/pilote.json`).

Validité [VÉRIFIÉ] (`resultats/controles.json`) : C-ORACLE 100 % sur 8 030 items, C-PARCŒUR 0,000
(table de 1 120 645 paires, sur-ensemble du flux de la graine 1) → **TEST VALIDE**.

**Budget de structure** (donné à la main, pour tous) : la découpe (A lit, B calcule), le nombre de
pas, la synchronisation colonne par colonne, 2 symboles par colonne avec le même lexique pour a et b
(la « compositionnalité » par colonne est **imposée**), V = 48 ; plus le budget d'E014 (lecteur
supervisé sur « poser en colonnes ») et d'E013 (I1 : alignement donné). DONNÉ : en plus, la
traduction exacte. **Non donné** (COLL, IND) : quel symbole veut dire quoi, ni qu'il faut une
convention commune.

## Résultats (TEST, 5 graines × 9 paires, exact-match %) [VÉRIFIÉ]

`resultats/summary.md`, `resultats/resultats.json`, détail item par item `resultats/eval.tgz`.

| cond. | graines réussies (9 paires ≥ 90 % à 16) | paires ≥ 90 % à 16, par graine | 9 paires, T-LONG 16 | 100 | 1 000 |
|---|---|---|---|---|---|
| DONNÉ | **5/5** | 9 ; 9 ; 9 ; 9 ; 9 | 100,0 ± 0,0 | 100,0 | 71,7 |
| COLL | **0/5** | 1 ; 1 ; 1 ; 1 ; 2 | 13,3 ± 4,4 | 13,3 | 10,9 |
| IND | **0/5** | 0 ; 2 ; 2 ; 1 ; 2 | 15,6 ± 8,8 | 15,6 | 8,8 |
| COUPÉ | 0/5 | 0 ; 0 ; 0 ; 0 ; 0 | 0,0 | 0,0 | 0,0 |

(13,3 % = 6 paires parfaites sur 45, toutes les autres à 0 : aucune paire n'est « à moitié »
apprise.)

**Les paires qui ont appris généralisent** (moyenne sur les paires ≥ 90 % à 16) :

| cond. | n paires | T-ID 5 | 10 | 16 | 32 | 64 | 100 | 1 000 | CASCADE 100 / 1 000 | ZEROS 100 / 1 000 | ASYM 100 / 1 000 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| DONNÉ | 45 | 100 | 100 | 100 | 100 | 100 | 100 | 71,7 | 100 / 74,4 | 99,7 / 79,5 | 99,7 / 82,2 |
| COLL | 6 | 100 | 100 | 100 | 100 | 100 | 100 | 81,8 | 100 / 83,8 | 99,8 / 83,3 | 99,8 / 87,1 |
| IND | 7 | 100 | 100 | 100 | 100 | 100 | 100 | 56,4 | 100 / 59,4 | 99,4 / 74,1 | 99,4 / 74,0 |

Les 13 paires apprises restent ≥ 90 % à 100 chiffres (13/13). À 1 000 chiffres la limite est
celle du **lecteur** (DONNÉ, interface parfaite : 71,7 % ; E014 : lecture de `R1L-s1` à 28,5 % à
1 000) ; les moyennes COLL/IND dépendent de quel lecteur figure dans la paire apprise.

**Qui parle à qui ; lexique** (par graine, `C` = sens sur 11 où les 3 émetteurs utilisent le même
symbole ; « partagés » = sens où deux émetteurs coïncident) :

| cond. | g | paires apprises | après phase 1 → fin | C | partagés A1-A2 / A1-A3 / A2-A3 | tours réussis fin ph. 1 / ph. 2 (%) | problèmes uniques vus |
|---|---|---|---|---|---|---|---|
| COLL | 1 | A3B1 | 1 → 1 | 0/11 | 0 / 0 / 0 | 11,6 / 0,0 | 216 957 |
| COLL | 2 | A3B3 | 1 → 1 | 0/11 | 1 / 0 / 0 | 11,2 / 0,0 | 217 799 |
| COLL | 3 | A2B3 | 1 → 1 | 0/11 | 1 / 0 / 0 | 12,2 / 0,0 | 217 666 |
| COLL | 4 | A3B1 | 1 → 1 | 0/11 | 0 / 0 / 0 | 12,2 / 0,0 | 216 686 |
| COLL | 5 | A1B3, A3B1 | 2 → 2 | 0/11 | 0 / 0 / 0 | 22,4 / 0,1 | 224 681 |
| IND | 1 | — | 0 → 0 | 0/11 | 1 / 1 / 0 | 1,1 / 0,0 | 772 049 |
| IND | 2 | A1B1, A3B3 | 1 → 2 | 0/11 | 0 / 0 / 0 | 17,3 / 0,0 | 771 329 |
| IND | 3 | **A1B3, A2B3** | 2 → 2 | 0/11 | 3 / 0 / 0 | 22,5 / 0,0 | 771 169 |
| IND | 4 | A1B1 | 1 → 1 | 0/11 | 3 / 0 / 1 | 12,7 / 0,0 | 771 002 |
| IND | 5 | A1B1, A2B3 | 0 → 2 | 0/11 | 2 / 0 / 1 | 7,3 / 0,0 | 772 092 |
| COUPÉ | 1–5 | — | 0 → 0 | 0/11 | ≤ 2 (hasard) | 0,1 / 0,0 | — |

(« tours réussis » en phase 2 = les 3 paires justes ; en IND ce n'est pas la récompense, seulement
la mesure. Problèmes uniques : COLL en voit 3,5 fois moins qu'IND parce que les tours rejoués
occupent le lot.)

- **Idiolectes, pas de langue commune** : C = 0/11 dans les 25 runs. Un seul cas de récepteur
  **bilingue** : IND graine 3, B3 comprend A1 **et** A2, qui ne partagent que 3 symboles sur 11 (2, 3
  et 7) — B3 a appris deux dialectes (synonymie), pas une langue commune.
- **Stabilité** : le lexique argmax du meilleur checkpoint ne change plus sur les 1 000 derniers pas
  en COLL (0 à 1 changement de checkpoint à checkpoint) ; en IND il bouge encore un peu (2 à 4 des
  4 checkpoints précédents diffèrent du final), sans créer de paire nouvelle hormis IND s2 et s5.
- **Vitesse** (premier checkpoint où une paire passe 90 % VAL-OOD, résolution 250 pas) : COLL
  750–1 500 pas (médiane 1 000) ; IND 500–1 500 (médiane 1 500 ; graine 1 jamais).
- **Effondrement des politiques** (diagnostic, pas une mesure préenregistrée) : entropie moyenne
  des émetteurs au meilleur checkpoint 0,07–0,23 nat (COLL) et 0,03–0,16 (IND), contre 3,87 pour
  l'uniforme ; même les émetteurs dont **aucun** partenaire ne comprend le code l'ont figé.

### Autodiagnostic (TEST hors T-ID, 9 paires × 5 graines = 203 850 items par condition)

| cond. | faux | faux et sûrs (≥ 0,8) | confiance médiane justes / faux | τ par graine | abstention quand faux / quand juste |
|---|---|---|---|---|---|
| DONNÉ | 5 535 | 5 535 | 0,997 / 0,996 | 0,99 ×5 | 0 % / 0 % |
| COLL | 176 981 | 25 668 | 0,997 / 0,573 | 0,99 ×5 | **99,6 % / 0,8 %** |
| IND | 172 820 | 59 510 | 0,998 / 0,545 | 0,99, 0,99, 0,9, 0,9, 0,99 | 85,2 % / 0,1 % |
| COUPÉ | 203 850 | 898 | — / 0,382 | aucun (0 juste en VAL) | 0 % / — |

Confiance = min sur les colonnes des probabilités des choix (symbole, jeton, chiffre d'I1) ; elle
**n'inclut pas le lecteur** : les 5 535 faux de DONNÉ (erreurs de lecture à 1 000 chiffres) sont
donc tous « sûrs » — même angle mort qu'E014 §3 du diagnostic. En COLL/IND, un seuil τ = 0,99 fait
s'abstenir sur presque toutes les paires qui ne se comprennent pas.

### Prédictions (préenregistrées)

| | énoncé | verdict |
|---|---|---|
| P1 | COLL ≥ 4/5 graines réussies | ❌ 0/5 (1 à 2 paires sur 9) |
| P2 | IND atteint 90 % VAL plus vite que COLL | ❌ médiane IND 1 500 contre COLL 1 000 pas (n = 5, graine IND 1 jamais) |
| P3 | graines réussies : C ≥ 9/11 et C(COLL) ≥ C(IND) | ❌ sans objet pour « réussies » (aucune) ; C = 0/11 partout |
| P4 | graines réussies : 9 paires ≥ 90 % à 100 | sans objet ; **les 13 paires apprises** : 13/13 ≥ 90 % à 100 |
| P5 | COUPÉ 0/5, ≤ 1 % à 16 | ✅ 0/5, 0,0 % |
| P6 | DONNÉ 9 paires ≥ 99 % à 16 | ✅ 100 % (45/45) |
| P7 | confiance médiane faux < justes (COLL, IND) | ✅ 0,573 < 0,997 ; 0,545 < 0,998 |

## Exploratoire (post hoc, NON préenregistré, graines 1–2, 12 000 pas)

`resultats/exploratoire_12k.json` : trois fois plus de pas (phase 1 = 6 000) ne changent pas le
régime. COLL s1 : 2 paires (A1B2, A3B1), s2 : 1 (A3B3), rien d'ajouté en phase 2 ; IND s1 : 0 ;
IND s2 : 2 paires après la phase 1, **3** à la fin (A1B1, A2B3, A3B3 : B3 devient bilingue). C = 0/11
partout. Le test « nouveau venu » (§6 du préenregistrement) n'a **pas** été fait : il était
conditionné à une graine COLL réussie, il n'y en a aucune.

## Lecture

- [VÉRIFIÉ] **Aucune langue commune n'a émergé** : 0/5 graines en COLL comme en IND, C = 0/11 dans
  les 25 runs officiels et les 4 exploratoires. Ce qui émerge, ce sont des **idiolectes de paire** :
  une ou deux paires par graine se forgent un code parfait, les autres paires restent à exactement 0.
- [VÉRIFIÉ] **La règle « tout-ou-rien + tout le monde recommence » gèle l'apprentissage en
  équipe** : en phase 2, 0,0–0,1 % de tours réussis en COLL sur les 5 graines, et aucune paire gagnée
  (1 → 1, 2 → 2). Mécanisme : avec 3 paires dont au plus 1 ou 2 fonctionnent, un appariement complet
  ne réussit jamais, la récompense de tous vaut 0, REINFORCE n'a plus de gradient. La récompense
  individuelle (IND) continue d'apprendre un peu en phase 2 (IND s2 : 1 → 2 ; s5 : 0 → 2). La pression
  sociale telle que formulée **n'a pas fabriqué de pont** ; elle a coupé le signal.
- [VÉRIFIÉ] Le rejeu collectif a un coût caché : COLL voit **3,5 fois moins** de problèmes neufs
  qu'IND (≈ 217 000 contre ≈ 771 000) — le lot est rempli de tours rejoués.
- [VÉRIFIÉ] **Ce qui a été appris généralise en longueur** : les 13 paires apprises sur 1–5 chiffres
  additionnent exactement à 16, 32, 64 et 100 chiffres et sur les adverses à 100 (≥ 99,4 %). Le
  protocole émergent est par colonne et sans longueur ; la procédure est portée par les modules gelés.
  C'est, à notre connaissance limitée (veille de 10 min), la partie **nouvelle** : un code inventé par
  récompense seule entre deux compétences gelées se transporte à 20 fois la longueur d'entraînement.
- [VÉRIFIÉ] Témoins : canal coupé 0 % ; interface donnée 100 % à 16 et 100 chiffres (9 paires × 5
  graines), 71,7 % à 1 000 (limite du lecteur).
- [HYPOTHÈSE] Pourquoi une seule paire : le succès exact d'une addition entière est rare au départ
  (≈ 0,05 % des tours), la première paire qui décroche par hasard sur des problèmes courts renforce
  ses choix ; avec β = 0 et une ligne de base moyenne, **tous** les émetteurs et récepteurs se figent
  vite (entropie ≈ 0,1 nat), y compris ceux qui n'ont pas de partenaire. Un agent figé sur un code
  que personne ne comprend n'explore plus : l'idiolecte est un **verrouillage précoce**, pas un choix.
  Le pilote a montré que le bonus d'entropie (β = 0,01) empêche au contraire tout décollage (0 %).
- [HYPOTHÈSE] Ce qui manque, par rapport à Mahaut et al. (protocole commun obtenu entre réseaux
  gelés hétérogènes) : un signal **dense** (jeu référentiel, perte différentiable ou récompense par
  symbole) plutôt qu'un succès tout-ou-rien sur une addition entière. E016 ne dit rien de ce qui se
  passerait avec un tel signal : non testé.
- Limites : 3 + 3 agents fixes, un seul jeu d'hyperparamètres (lr à la borne basse de la grille
  pilote), récepteurs et émetteurs tabulaires, 5 graines. Aucune conclusion générale sur la
  « pression sociale » : une seule formulation de la règle a été testée.

## Reproduire

```bash
source $HOME/.venvs/ev-llm-e008/bin/activate
cd research/experiments/E016-mouches
python test_e016.py                                           # 8 tests
python entraine16.py --conds COLL IND COUPE --graines 1 2 3 4 5  # reprise : relancer
python controles16.py
python evalue16.py --conds DONNE COLL IND COUPE --graines 1 2 3 4 5
python analyse16.py
```

Calcul : ≈ 1 h 10 au total (pilote 6 min, 15 runs officiels ≈ 33 min, exploratoire ≈ 19 min,
évaluation 5 min, analyse 6 min), GPU partagé avec d'autres fenêtres.
