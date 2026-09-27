# E015 — « écosystème » : une population de petits circuits évolue, garde ses champions, et s'assemble SEULE — préenregistrement

Mandat M0030, 2026-09-27, branche `exp/e015-ecosysteme` (depuis `origin/exp/e014-reperage` @
`fc698b4`). Ce document est committé et poussé **seul, avant toute ligne de code et toute
exécution**. Toute modification ultérieure est un amendement daté en fin de fichier, jamais une
réécriture.

## 0. Veille (≈ 15 min, 4 recherches) — ce qui existe de plus proche, et l'écart

1. **PathNet** (Fernando et al. 2017, arXiv 1701.08734) : un algorithme génétique choisit des
   chemins à travers des modules gelés d'une grille fixe. L'interface est **imposée** (couches de
   même forme, somme des activations) ; tâches de perception, pas de longueur.
2. **Modular meta-learning / BounceGrad** (Alet et al. 2018, arXiv 1806.10166) : recuit simulé sur
   des compositions de modules partagés, **dans un gabarit de composition donné**, modules
   co-entraînés sur la famille de tâches cibles.
3. **MAIN** (arXiv 2003.04227), **NPI** (arXiv 1511.06279) : un contrôleur enchaîne des modules en
   désignant des positions de bande, jusqu'à 100 chiffres ; la bande et les arguments sont
   conçus à la main, NPI est supervisé par des traces.
4. **Model stitching** (dont « stitching for neuroevolution ») : une couche d'adaptation apprise
   entre réseaux gelés, entraînée à **imiter les activations d'une couche cible connue**
   (supervision d'alignement), en continu, sans question de longueur.
5. **Neural Harvard computers** (évolution + abstraction) : généralisation algorithmique d'**un**
   contrôleur évolué avec une interface mémoire donnée.

**Écart (notre question)** : les champions sont évolués **séparément sur des mini-tâches sans
rapport avec la tâche cible**, puis gelés ; pour une tâche **nouvelle** (addition depuis la phrase
brute, addition de trois nombres, soustraction), le système doit trouver **à la fois** quels
champions enchaîner, dans quel ordre de manipulations de flux, **et** l'interface symbole à symbole
entre eux (adaptateurs discrets), avec pour seul signal l'exact-match d'un juge fixe sur des
nombres de 1 à 5 chiffres. On mesure (a) la généralisation en longueur du composé (10–1 000),
(b) le nombre d'essais, (c) si l'interface découverte **se réutilise** (départ « chaud » vs
« froid » sur une 2ᵉ et 3ᵉ tâche). Dans E014 c'est **nous** qui avions écrit le contrat
(colonnes alignées, symbole « absent ») ; ici rien de tel n'est écrit. [HYPOTHÈSE] Nous n'avons
pas trouvé ce montage dans la littérature en 20 min de veille ; la veille est courte.

## 1. Question

Q1 — La machine **assemble-t-elle seule** des compétences gelées pour une tâche nouvelle, de
façon qui généralise en longueur ? Q2 — Avec combien d'essais (appels au juge) ? Q3 — L'interface
qu'elle invente est-elle **réutilisable** (moins d'essais sur une tâche suivante quand on part
d'elle) ? Q4 — Qu'apportent l'évolution (vs tirage aléatoire) et l'apprentissage de vie (vs
mutation seule) ?

## 2. Phase A — l'écosystème (évolution + apprentissage de vie)

**Circuit** : cellule d'E013 réécrite à largeur variable (z = relu(W1 [x ; h]),
h' = tanh(Wh z), logits = Wo z → 10 chiffres), k ports d'entrée de 11 symboles (0–9, ABSENT),
flux **alignés poids faible d'abord**, **max(ℓ) + 1 pas** (même convention qu'I1 d'E013).

**Mini-tâches** (entraînement : chaque opérande de 1 à 5 chiffres, longueurs indépendantes) :

| mini-tâche | ports | sortie par pas t |
|---|---|---|
| M-COPIE | 1 | x_t (0 au pas final) |
| M-COMPL | 1 | 9 − x_t (0 au pas final) |
| M-SUCC | 1 | chiffres de x + 1 |
| M-SOMME | 2 | chiffres de a + b |
| M-DIFF | 2 | (a_t − b_t) mod 10, ABSENT lu 0, **sans emprunt** (0 au pas final) |

Aucune mini-tâche n'est « lire la phrase », « poser en colonnes », ni une soustraction.

**Génome** d'un circuit : H ∈ {1, 2, 3, 4, 6, 8}, F ∈ {8, 16, 32}, log10(lr) ∈ [−3 ; −1,5].
**Vie** : 300 pas d'Adam, lot 128, entropie croisée sur tous les pas (flux de la mini-tâche).
**Hérédité lamarckienne** : l'enfant part des poids du parent si (H, F) inchangés, sinon d'une
initialisation neuve. **Juge** : exact-match sur la VAL de la mini-tâche (6–8 chiffres,
100 items par L, graine 3213), seul critère de sélection.
**Évolution** par mini-tâche : population 6 → 5 générations (garder les 3 meilleurs, 3 mutants
par génération), soit 18 vies par mini-tâche, 90 par graine.
**Archive (MAP-Elites)** : niche = (mini-tâche, taille H ≤ 2 « petit » / H ≥ 3 « grand ») ;
l'élite de chaque niche entre dans la **bibliothèque**, **quel que soit son score** (≤ 10 champions,
dont des médiocres : c'est au compositeur de choisir). La bibliothèque est gelée.

## 3. Phase B — l'assemblage autonome

**Programme** (génome de composition) : liste de ≤ 12 instructions sur des registres de flux de
symboles (0–9 chiffres, 10 `+`, 11 `=`, 12 `-`, 13 ABSENT). r0 = la phrase brute (poids fort
d'abord, sans symbole de début). Instructions :
- `DECOUPE(r, v)` → 2 registres : avant / après la première occurrence du symbole v (v évolué,
  0–13 ; si v absent : tout / vide) ;
- `INV(r)` : flux renversé ; `TRONQUE(r)` : flux sans son dernier symbole ;
- `CHAMP(c, r₁…r_k, A₁…A_k)` : champion c de la bibliothèque sur ses k ports, chaque port
  précédé d'un **adaptateur** A = table 14 symboles → 11 (0–9, ABSENT), appliqué **après** le
  bourrage ABSENT du port ; sortie = argmax par pas (interface **discrète**, leçon E014).
- gène `sortie` = registre lu à la fin.
**Décodage (donné)** : tout symbole non chiffre → réponse invalide ; retrait de **tous** les 0 de
tête ; flux vide → invalide.

**Juge (fixe, hors génome)** : sur un lot de 64 exemples d'entraînement **tirés à neuf à chaque
génération**, score = taux d'exact-match + 0,1 × exactitude par chiffre alignée à droite.
Un **essai** = un appel au juge.
**Vie** (apprentissage) : 30 propositions de montée locale sur les adaptateurs (un port, un
symbole vu sur ce port, une nouvelle valeur ; gardée si le score ne baisse pas) ; les adaptateurs
appris sont hérités (lamarckien).
**Évolution** : (μ + λ), μ = λ = 20, parent par tournoi de 2, 1 à 3 mutations (op, registre,
v, champion, entrée d'adaptateur, insertion / suppression d'instruction, sortie).
Population initiale : programmes aléatoires de 3 à 8 instructions, adaptateurs aléatoires.
**Budget** : 60 000 essais par run (fixé définitivement après pilote, amendement A1).
**Panthéon** : tout programme à exact 1,0 sur son lot est rejugé sur 256 exemples neufs ; s'il
reste à 1,0 il est « candidat ». Fin : les 5 meilleurs candidats (à défaut les 5 meilleurs scores)
passent la **VAL-OOD 6–8** ; retenu = meilleur VAL, puis programme le plus court.

**Tâches nouvelles** (jamais vues par l'écosystème) :
- **N1 ADD** : `a+b=` → a + b (flux E008, graine s : `paires_du_pas`) ;
- **N2 ADD3** : `a+b+c=` → a + b + c ;
- **N3 SOUS** : `a-b=` → a − b, avec a ≥ b.

**Conditions** (graines 1–5, pilote graine 0 exclu) :
| condition | tâche | ce qui change |
|---|---|---|
| EVO | N1 | évolution + vie |
| ALEA | N1 | même budget d'essais, programmes aléatoires + vie, **aucune sélection** |
| SANS-VIE | N1 | évolution, **0 proposition de vie** (λ ajusté, même budget d'essais) |
| FROID-N2, FROID-N3 | N2, N3 | EVO, population aléatoire |
| CHAUD-N2, CHAUD-N3 | N2, N3 | EVO, population initiale = gagnant EVO-N1 de la même graine + 19 de ses mutants |

La bibliothèque de la graine s sert à toutes les conditions de la graine s.

## 4. Budget de structure (ce qui est donné à la main — rien de caché)

Donné : l'alphabet des flux et le symbole ABSENT ; la convention des champions (flux alignés poids
faible d'abord, bourrage ABSENT, max(ℓ) + 1 pas) ; les 5 mini-tâches et leur supervision ;
les opérations de flux génériques DECOUPE / INV / TRONQUE ; la sortie discrète (argmax) ; le
décodage (retrait de tous les zéros de tête) ; la forme des programmes (≤ 12 instructions).
**Non donné** : quels champions utiliser, dans quel ordre, sur quels registres, où couper (v),
qu'il faut renverser, la table de correspondance entre symboles (l'interface), ni le rôle de `=`,
`+`, `-`, ABSENT à l'entrée des champions. [HYPOTHÈSE assumée] INV est indispensable : un circuit à
état fini ne peut pas renverser un flux ; c'est la part d'« alignement » que E014 faisait
apprendre au lecteur — elle est ici **donnée** comme opération générique, et dite.

## 5. Données, validation, test

- Entraînement N1 : flux E008 (`paires_du_pas(graine, pas, exclues, 64)`), 1–5 chiffres. N2 / N3 :
  même tirage (`e008.tire_nombre`), `default_rng([50 000 + s, g])` / `[60 000 + s, g]`, items de
  VAL/TEST exclus.
- **VAL-OOD** : opérandes de 6, 7, 8 chiffres, 500 items par L (N1 graine 3313, N2 3323,
  N3 3333) — seul jeu de choix.
- **TEST** (une seule fois, à la fin) : T-LONG L = 10, 16, 32, 64, 100 (500) et 1 000 (200) ;
  T-ID 2–5 ; adverses, 100 items (+ cas spéciaux) par L ∈ {10, 16, 32, 64, 100, 1 000} :
  N1 : ADV-CASCADE, ADV-ZEROS, ADV-ASYM (générateurs E013), **ADV-PROPAG** (a + b = 10^L,
  leçon R010) ; N2 : ADV-CASCADE3 (trois nombres à retenues), ADV-PROPAG3 (a + b + c = 10^L),
  ADV-ASYM3 ; N3 : ADV-EMPRUNT (10^(L−1) − petit, emprunts en cascade), ADV-EGAUX (a = b),
  ADV-ASYM (L chiffres − 1–5 chiffres). Graines TEST 3314–3339.
- **Critère** : exact-match de la chaîne entière (fonction d'évaluation E008 généralisée à une
  référence par tâche, mêmes champs, même seuil « sûr » 0,8).
- **Validité** : C-ORACLE (algorithme en colonnes écrit sur les chaînes, sans `+`/`-` Python sur
  les entiers) = 100 % sur tous les jeux ; C-PARCŒUR (table des items d'entraînement jugés par la
  graine 1, toutes conditions) = 0 % (≤ 1 % exigé hors T-ID) ; sinon **TEST NON VALIDE**.

## 6. Mesures

- Par graine : exact-match TEST par jeu × L ; **réussite d'une graine = ≥ 90 % à T-LONG 16** ;
  système réussi : ≥ 4/5 graines. Moyenne ± écart-type (ddof = 0) **et** nombre de graines réussies.
- **Essais** : jusqu'au premier candidat ; jusqu'au premier candidat qui passe la VAL-OOD à ≥ 0,99
  (mesure post hoc sur les candidats journalisés) ; **exemples uniques** jugés.
- **Interface** : le programme retenu, écrit lisiblement (instructions, adaptateurs réduits aux
  symboles effectivement rencontrés) ; pour CHAUD, part des instructions du gagnant N1 conservées.
- **Confiance** : p_min = minimum, sur tous les pas de tous les champions exécutés, de la
  probabilité du chiffre émis. Faux et sûrs (p_min ≥ 0,8). Abstention : τ = plus grand seuil de
  {0,5 ; 0,6 ; 0,7 ; 0,8 ; 0,9 ; 0,99} laissant ≤ 5 % des justes de VAL-OOD sous τ ; taux
  d'abstention quand faux / quand juste sur TEST.
- **Triche (reward hacking)** : aucun génome ne peut toucher au juge ni aux données ; on journalise
  (a) les programmes qui atteignent ≥ 0,5 d'exact au lot mais < 0,1 en VAL (raccourcis de courte
  longueur), (b) les programmes à score > 0 **sans aucun champion** (recopie de l'entrée).
- Référence (pas un but) : E014 R1G (interface donnée) = 4/5 graines ≥ 90 % à 16.

## 7. Prédictions (préenregistrées)

- **P1** EVO-N1 réussit sur ≥ 3/5 graines.
- **P2** Quand un programme EVO-N1 atteint VAL-OOD ≥ 0,99, il est exact à ≥ 99 % à T-LONG 100
  (la composition discrète ne perd rien : leçon E014).
- **P3** ALEA ≤ EVO en graines réussies, et ALEA trouve moins de candidats.
- **P4** SANS-VIE ≤ EVO en graines réussies.
- **P5** CHAUD-N2 : médiane des essais jusqu'au premier candidat ≤ la moitié de FROID-N2.
- **P6** N3 (soustraction : demande de découvrir le complément à 9 dans l'adaptateur et un
  successeur) : FROID-N3 ≤ 2/5 ; CHAUD-N3 ≥ FROID-N3.
- **P7** L'interface N1 retenue a des adaptateurs identité sur les chiffres rencontrés et renvoie
  `=` (s'il atteint un champion) vers ABSENT ou 0.

## 8. Calcul et ordre

CPU seul (numpy ; MLX sur CPU pour la vie des circuits de la phase A), ≤ 4 h ; invocations
≤ 9 min avec reprise sur point de contrôle ; aucune tâche de fond. Pilote = graine 0 (exclue) :
vérifie que la phase A apprend (VAL mini-tâche) et mesure la vitesse ; seuls les budgets
(essais, vies) peuvent être ajustés par l'amendement A1, avant les runs officiels. Ordre des
commits : ce préenregistrement (poussé seul) < code < valeurs figées après pilote < résultats.

## Amendement A1 — 2026-09-27, après pilote (graine 0, exclue), AVANT tout run officiel

Pilote (journaux `runs/pilote1`, `runs/pilote2`, hors git ; chiffres recopiés ici) :
- Phase A : les 10 niches atteignent VAL mini-tâche 0,993–1,000 en 64 s. L'écosystème apprend.
- Phase B, réglage préenregistré (vie = 30 propositions aléatoires, 60 000 essais) : **0 candidat**
  dans les 5 conditions ; toutes convergent vers `r1,r2 = DECOUPE(r0,'+') ; sortie = r1`
  (répondre a ; score ≈ 0,05). Même résultat avec 400 000 essais et la vie ci-dessous
  (EVO, SANS-VIE, FROID-N3 : 0 candidat).
- Diagnostic : un champion mal adapté vaut moins que la recopie de a ; 30 propositions
  aléatoires ne réparent jamais ~20 entrées d'adaptateur ; la bonne structure N1 exige 6
  instructions coordonnées, qu'un tirage aléatoire produit avec une probabilité de l'ordre de
  10⁻¹², et aucune structure partielle n'est mieux notée que la recopie.

Changements (écart assumé : le préenregistrement ne permettait d'ajuster que les budgets ; le
juge, lui, **n'est pas touché** — le modifier pour récompenser les structures partielles
reviendrait à donner la solution) :
1. **Vie** = balayage par coordonnées des adaptateurs : ordre aléatoire des couples (port,
   symbole vu) ; pour chacun, les 10 autres valeurs sont essayées, la meilleure est gardée si
   elle améliore strictement le score ; **≤ 200 essais par vie**.
2. **Budget** : 150 000 essais par run (temps de calcul).
3. SANS-VIE : μ = λ = 20 inchangés, plus de générations pour le même budget d'essais (et non
   « λ ajusté »).
4. **Échelle d'échafaudage** (conditions ajoutées, tâche N1, population initiale = 20 copies de
   l'échafaudage avec adaptateurs aléatoires, puis EVO normal) :
   - **ECH0** : câblage N1 donné (DECOUPE `+`, DECOUPE `=`, INV, INV, CHAMP à 2 ports, INV) ;
     **à trouver** : quel champion (tiré au hasard parmi ceux à 2 ports, évolué ensuite parmi les 10)
     et l'interface (les adaptateurs) ;
   - **ECH1** : ECH0 sans l'INV final (il manque une instruction) ;
   - **ECH2** : seulement les deux DECOUPE (il manque INV, INV, CHAMP, INV).
   Budget de structure : ECH0 reçoit tout le câblage ; c'est la mesure « interface seule ».
5. **CHAUD-N2 / CHAUD-N3** partent du gagnant **ECH0-N1** de la même graine (et non EVO-N1, qui
   a échoué au pilote). Q3 devient : une interface trouvée (ECH0) se réutilise-t-elle ?
6. Pilote graine 0 avec ces réglages (chiffres informatifs, exclus) : ECH0 3 candidats, premier
   à 71 260 essais, VAL 1,000 ; ECH1 et ECH2 0 candidat ; CHAUD-N2 et CHAUD-N3 0 candidat.

Prédictions ajoutées (informées par le pilote, dit ici) : **P8** ECH0 ≥ 4/5 graines réussies ;
**P9** ECH1 ≤ 1/5 et ECH2 ≤ 1/5 ; **P10** EVO, ALEA, SANS-VIE, FROID-N2, FROID-N3 = 0/5.
P5 et P6 sont maintenues avec la nouvelle source de CHAUD.
