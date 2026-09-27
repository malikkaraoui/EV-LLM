# E015 — « écosystème » : des champions évolués séparément s'assemblent-ils SEULS pour une tâche nouvelle ?

Mandat M0030, 2026-09-27, branche `exp/e015-ecosysteme` (depuis `exp/e014-reperage` @ `fc698b4`).
Préenregistrement : [`PREREGISTREMENT.md`](PREREGISTREMENT.md) (poussé seul avant le code ;
amendement A1 après le pilote, avant les runs officiels). Code E008 / E013 importé, non modifié.

## En une phrase

**Non : la machine n'a pas assemblé seule ses compétences** (0/5 graines sur les trois tâches
nouvelles, que la recherche parte de zéro ou d'une interface déjà trouvée). Elle y parvient
seulement quand on lui **donne le câblage** et qu'il ne reste qu'à choisir le champion et
**inventer l'interface symbole à symbole**. Dans ce cas, 2 graines sur 5 trouvent une addition
exacte **jusqu'à 1 000 chiffres**, avec une interface différente de celle qu'on aurait écrite. Les
3 autres graines inventent des interfaces fausses mais astucieuses : elles détournent le circuit
de **soustraction** en additionneur sans retenue. Il suffit qu'il manque **une seule** instruction
au câblage pour tomber à 0/5.

## Veille (§0 du mandat) et ce qui est nouveau

Plus proche (détail au préenregistrement §0) :
- PathNet : chemins évolués à travers des modules gelés, interface imposée ;
- modular meta-learning / BounceGrad : gabarit de composition donné ;
- MAIN et NPI : bande et arguments conçus, traces supervisées pour NPI ;
- model stitching : adaptateur appris sur les activations d'une couche cible connue ;
- neural Harvard computers : un seul contrôleur évolué.

Aucun de ces travaux ne demande à la fois de **découvrir** quels modules gelés enchaîner, l'ordre
des manipulations de flux **et** l'interface symbole à symbole, avec pour seul signal
l'exact-match d'un juge fixe, puis de mesurer la généralisation en longueur du composé et la
réutilisation de l'interface. [HYPOTHÈSE : la veille a duré 15 min.]

Nouveau ici, et [VÉRIFIÉ] sur 5 graines :
1. Une **échelle de câblage** montre où la découverte casse. Avec le câblage entier donné (ECH0),
   2/5 graines réussissent. Sans l'INV final (ECH1) ou sans le cœur du câblage (ECH2), c'est 0/5.
   Partir de zéro (EVO) donne aussi 0/5.
2. L'interface découverte est **réelle et lisible**, mais n'est pas la nôtre : ABSENT est lu « 0 »
   sur un port et « absent » sur l'autre.
3. Les interfaces fausses sont **des optimums locaux sémantiques** : négation modulaire,
   décalages qui se compensent. Elles convertissent un champion d'une autre tâche en quasi-solution.
4. La **réutilisation n'a aucune prise** : un programme N1 exact, appliqué à N2 ou N3, ne vaut pas
   mieux au juge que « répondre a ».

## Protocole (résumé ; tout est au préenregistrement)

**Phase A — écosystème.**
- 5 mini-tâches sur des flux alignés, poids faible d'abord, opérandes de 1 à 5 chiffres :
  COPIE, COMPL (9 − x), SUCC (x + 1), SOMME (a + b), DIFF (a − b mod 10 par colonne, sans
  emprunt). Aucune mini-tâche n'est « lire la phrase », « poser en colonnes », ni une soustraction.
- Circuits : cellule d'E013 à largeur variable.
- Génome (H, F, lr). Vie : 300 pas d'Adam. Hérédité lamarckienne. Juge : VAL 6–8 de la mini-tâche.
- 18 vies par mini-tâche. Archive MAP-Elites (mini-tâche × taille), soit **10 champions gelés** par
  graine, gardés quel que soit leur score.
- Bibliothèques officielles : 49/50 niches ≥ 0,977 en VAL. Une élite M-DIFF « petit » vaut 0,003
  (graine 3) ; elle est gardée.

**Phase B — assemblage.**
- Un programme compte au plus 12 instructions sur des registres de flux. Instructions possibles :
  DECOUPE(r, v), INV(r), TRONQUE(r), et CHAMP(c, registres, adaptateurs).
- Un adaptateur est une table 14 symboles → 11 : c'est **l'interface**.
- Juge fixe : sur un lot de 64 items neufs par génération, exact + 0,1 × exactitude par chiffre.
- Vie (A1) : balayage par coordonnées des adaptateurs, ≤ 200 essais.
- Évolution (μ + λ) = (20 + 20). Budget : 150 000 essais par run.
- Choix du programme : VAL-OOD 6–8 seule. TEST lu **une fois** : 10 / 16 / 32 / 64 / 100 / 1 000
  chiffres, plus les adverses, dont la propagation pure a + b = 10^L.
- 5 graines officielles, pilote graine 0 exclu.

**Budget de structure.**
- Donné :
  - l'alphabet et le symbole ABSENT ;
  - la convention des champions (alignés, poids faible d'abord, max(ℓ) + 1 pas) ;
  - les 5 mini-tâches ;
  - les opérations génériques DECOUPE / INV / TRONQUE ;
  - la sortie discrète ;
  - le décodage (retrait des zéros de tête).
- Non donné : les champions à utiliser, l'ordre, les registres, le symbole de coupe, la table
  d'interface.
- Conditions de l'échelle (A1) : ECH0 reçoit **tout le câblage** N1. ECH1 le reçoit moins l'INV
  final. ECH2 reçoit seulement les deux DECOUPE.
- CHAUD-N2 et CHAUD-N3 partent du gagnant ECH0-N1 de la même graine.

**Validité** [VÉRIFIÉ] (`resultats/controles.json`) :
- C-ORACLE (colonnes sur chaînes) : 100 % sur 22 266 items (N1 8 642, N2 6 812, N3 6 812) ;
- C-PARCŒUR (items jugés par la graine 1, toutes conditions) : 0,000 partout, T-ID compris ;
- **TEST VALIDE**.

## Résultats (TEST, 5 graines, exact-match %, moyenne ± écart-type ddof = 0) [VÉRIFIÉ]

| condition | graines ≥ 90 % à 16 | T-LONG 10 | 16 | 100 | 1 000 | candidats | essais → 1er candidat |
|---|---|---|---|---|---|---|---|
| EVO-N1 (partir de zéro) | **0/5** | 0 | 0 | 0 | 0 | 0 | — |
| ALEA-N1 (sans sélection) | 0/5 | 0 | 0 | 0 | 0 | 0 | — |
| SANS-VIE-N1 | 0/5 | 0 | 0 | 0 | 0 | 0 | — |
| **ECH0-N1** (câblage donné) | **2/5** | 42,8 ± 46,9 | 40,8 ± 48,3 | 40,0 ± 49,0 | 40,0 ± 49,0 | 1, 0, 1, 0, 0 | 32 594 ; 20 108 |
| ECH1-N1 (manque l'INV final) | 0/5 | 0 | 0 | 0 | 0 | 0 | — |
| ECH2-N1 (seulement les DECOUPE) | 0/5 | 0 | 0 | 0 | 0 | 0 | — |
| FROID-N2 (a+b+c) | 0/5 | 0 | 0 | 0 | 0 | 0 | — |
| CHAUD-N2 (depuis ECH0-N1) | 0/5 | 0 | 0 | 0 | 0 | 0 | — |
| FROID-N3 (a−b) | 0/5 | 0 | 0 | 0 | 0 | 0 | — |
| CHAUD-N3 (depuis ECH0-N1) | 0/5 | 0 | 0 | 0 | 0 | 0 | — |

Tableau complet (32 / 64, T-ID, VAL, adverses, par graine) : `resultats/resultats.md`.

**ECH0 par graine**, T-LONG 16 / 100 / 1 000, puis ADV-PROPAG à 1 000 :

| graine | T-LONG 16 / 100 / 1 000 | ADV-PROPAG 1 000 |
|---|---|---|
| s1 | **100 / 100 / 100** | 100 (tous les adverses à 100 % à toutes les longueurs) |
| s3 | **100 / 100 / 100** | 27,5 (propagation pure : 98 → 87 → 27,5 % de 16 à 1 000) |
| s2 | 4,2 / 0 / 0 | — |
| s4 | 0 / 0 / 0 | — |
| s5 | 0 / 0 / 0 | — |

Exemples uniques jugés, moyenne par run :

| condition | exemples uniques |
|---|---|
| EVO | 8 345 |
| ALEA | 3 488 |
| SANS-VIE | 199 823 (beaucoup de générations courtes) |
| ECH0 | 3 085 |
| ECH1 | 15 941 |
| ECH2 | 20 518 |
| FROID / CHAUD | 8 111 à 13 265 |

## L'interface qui a émergé (inspectée)

Gagnant ECH0-N1, identique en s1 et s3 (champion M-SOMME « grand » choisi parmi les 10) :

```
r1,r2 = DECOUPE(r0, '+')            # donné (ECH0)
r3,r4 = DECOUPE(r2, '=')            # donné
r5 = INV(r1) ; r6 = INV(r3)         # donné
r7 = M-SOMME|grand(r5[0>0 … 9>9  ABSENT>0],  r6[0>0 … 9>9  ABSENT>ABSENT])   # TROUVÉ
r8 = INV(r7) ; sortie = r8          # donné
```

- [VÉRIFIÉ] Les chiffres sont en identité sur les deux ports (P7 ✅). `=` et `+` n'atteignent jamais
  le champion : les DECOUPE les retirent.
- [VÉRIFIÉ] Le « bourrage » (ABSENT) est traduit en **0 sur le port a et laissé absent sur le
  port b**. Ce contrat asymétrique, nous ne l'aurions pas écrit. Le champion l'accepte parce qu'il
  lit 0 et ABSENT de la même façon.

Interfaces fausses trouvées (optimums locaux, VAL ≤ 29 %) :

| graine | champion | interface |
|---|---|---|
| s5 | M-DIFF | a → a, **b → −b mod 10** : la soustraction sans emprunt devient une addition sans retenue |
| s4 | M-DIFF | a → a + 4, b → 4 − b : même chose, avec un décalage qui se compense |
| s2 | M-SOMME | a → a + 1, b → b − 1 : la somme par colonne est juste, la retenue est fausse |

[VÉRIFIÉ] Sur un lot neuf de 1 024 items (post hoc) :
- s4 et s5 sont justes **exactement** sur les items sans retenue (325/325 et 341/341) et faux sur
  tous les autres ;
- s2 est juste sur 380 items, dont 238 avec retenue : son décalage casse la retenue seulement dans
  certains cas ;
- s5 est **faux et sûr sur 4 606 erreurs sur 4 606** (TEST).

## Diagnostic (post hoc, NON préenregistré, lots d'entraînement neufs de 1 024 items, pas TEST)

`diagnostic15.py` → `resultats/diagnostic.json`. Leçon L-E012-2 : calculer l'objectif sur la
solution connue avant d'accuser l'objectif.

- [VÉRIFIÉ] Pour **les 30 runs N1**, la solution connue vaut **1,100** au juge (exact 1,000).
  - Programmes rendus : 0,004–0,050 pour EVO, ALEA, SANS-VIE, ECH1 et ECH2 ; 0,39–0,45 pour les
    ECH0 en échec.
  - **C'est la recherche qui échoue, pas l'objectif.**
- [VÉRIFIÉ] Les échecs EVO, SANS-VIE, ECH1 et ECH2 convergent tous vers
  `DECOUPE(r0,'+') ; sortie = a`, qui répond a et marque ≈ 0,04.
- [VÉRIFIÉ] **Pourquoi la réutilisation échoue.** Le gagnant ECH0-N1, appliqué tel quel :
  - à N2, il marque 0,010–0,020 (répondre a : 0,010–0,013 ; solution connue : 1,100) ;
  - à N3, il marque ≈ 0,005 ; avec la coupe changée en `-`, 0,016–0,105 (répondre a :
    0,062–0,081 ; solution connue : 1,100).
  - Le programme N1 n'est **pas mieux noté** qu'une recopie. La sélection le perd dès les
    premières générations (CHAUD retombe sur « répondre a » à toutes les graines).

## Prédictions (préenregistrées)

| | énoncé | verdict |
|---|---|---|
| P1 | EVO-N1 ≥ 3/5 | ❌ 0/5 |
| P2 | VAL ≥ 0,99 ⇒ T-LONG 100 ≥ 99 % | sans objet pour EVO ; ✅ pour ECH0 (s1, s3 : 100 %) |
| P3 | ALEA ≤ EVO | ✅ 0 = 0 (non départagé) |
| P4 | SANS-VIE ≤ EVO | ✅ 0 = 0 (non départagé) |
| P5 | CHAUD-N2 : ≤ ½ des essais de FROID-N2 | ❌ aucun candidat dans les deux |
| P6 | FROID-N3 ≤ 2/5 ; CHAUD-N3 ≥ FROID-N3 | ✅ 0/5 et 0 = 0 (trivial) |
| P7 | interface N1 identité sur les chiffres | ✅ (s1, s3) ; ABSENT → 0 / ABSENT (non prédit) |
| P8 (A1) | ECH0 ≥ 4/5 | ❌ 2/5 |
| P9 (A1) | ECH1 ≤ 1/5, ECH2 ≤ 1/5 | ✅ 0/5, 0/5 |
| P10 (A1) | EVO, ALEA, SANS-VIE, FROID-N2, FROID-N3 = 0/5 | ✅ |

## Lecture

- [VÉRIFIÉ] **Assemblage autonome : non**, sur N1, N2 et N3, en partant de zéro (0/5 chacun).
- [VÉRIFIÉ] **Interface seule : oui, parfois.**
  - Quand le câblage est donné, la recherche choisit le bon champion et invente une interface
    exacte dans 2 cas sur 5. Il lui faut 20 000 à 33 000 essais et ~3 000 items de 1 à 5 chiffres.
  - Le composé généralise ensuite jusqu'à 1 000 chiffres. La composition discrète ne perd rien :
    leçon E014 confirmée.
  - À 1 000 chiffres, la limite de s3 est la qualité du champion en propagation pure, pas
    l'interface.
- [VÉRIFIÉ] **Le câblage est le mur.** Il suffit qu'il manque une instruction (ECH1) pour passer
  à 0/5. Aucune structure partielle n'est mieux notée que « répondre a ». C'est un paysage en
  aiguille : la sélection n'a rien à suivre, et l'évolution ne fait pas mieux que le hasard
  (0 = 0).
- [VÉRIFIÉ] **La réutilisation n'est pas automatique.** Une interface exacte pour N1 ne donne
  aucune avance mesurable sur N2 ou N3. Cette avance n'existerait que si le juge notait les
  sous-résultats, ce qui reviendrait à écrire l'interface à la place de la machine.
- [HYPOTHÈSE] Le levier manquant n'est ni plus d'essais (pilote : 400 000 essais, même attracteur)
  ni l'apprentissage de vie. Il manque un **signal intermédiaire que la machine se donne
  elle-même**, par exemple la cohérence entre champions ou la prédiction de ses propres flux, au
  lieu du seul verdict final. C'est la question suivante, non testée ici.
- [HYPOTHÈSE] Les interfaces fausses (négation modulaire) montrent un système capable de
  **détourner** une compétence, un pas vers la créativité. Il se trompe alors avec assurance
  (s5 : 100 % de ses erreurs sont sûres). Il faut une confiance sur l'**interface**, pas seulement
  sur les champions.

**Comparaison avec E014 (référence, pas un but).** R1G, dont l'interface était **écrite par nous**,
obtenait 4/5 graines ≥ 90 % à 16. Ici :
- ECH0 (interface inventée, câblage donné) obtient 2/5 ;
- l'assemblage libre obtient 0/5.

## Autodiagnostic [VÉRIFIÉ]

- Faux et sûrs (p_min ≥ 0,8) : ECH0 7 673 sur 13 783 faux.
- Pour les programmes **sans champion** (« répondre a »), p_min vaut 1 par construction : aucun
  circuit n'émet de probabilité. Tous leurs faux sont donc comptés « sûrs », par définition. Ce
  chiffre ne dit rien sur le système.
- Abstention ECH0, τ choisi en VAL :

  | graine | τ | abstention quand faux | abstention quand juste |
  |---|---|---|---|
  | s1 | 0,9 | — (0 faux) | 0,02 % |
  | s2 | 0,5 | 20,9 % | 1,2 % |
  | s3 | 0,9 | 100 % (97 faux, tous en ADV-PROPAG de 16 à 1 000 chiffres ; 17 sûrs) | 1,5 % |
  | s4 | 0,7 | 32,0 % | 0 % |
  | s5 | 0,8 | 0 % | 0 % |

## Triche (reward hacking)

Aucun génome n'a accès au juge ni aux données : le juge est une fonction hors génome, et les lots
sont tirés à neuf à chaque génération. Journalisé :
- raccourcis (candidat ≥ 0,5 au lot mais < 0,1 en VAL) : **0** ;
- programmes sans champion à score > 0 : jusqu'à 23–48 par run ECH0 et des milliers pour EVO ;
  c'est l'attracteur « répondre a ».

Ce n'est pas une triche du juge. C'est une stratégie triviale légitime qui exploite les items où
b = 0 ou petit (≈ 2–3 % d'exact).

## Écarts et limites

- **Amendement A1** : écart au préenregistrement, qui ne permettait d'ajuster que les budgets.
  Changements : vie par balayage, budget 150 000 essais, conditions ECH0–ECH2, CHAUD depuis ECH0.
  Motif : 0 candidat partout au pilote. Les prédictions P8–P10 sont informées par le pilote, et
  c'est dit.
- La phase A n'a qu'un rôle de fournisseur. Ses champions sont presque tous parfaits sur leurs
  mini-tâches : la question d'une co-évolution écosystème ↔ assemblage n'est pas testée.
- INV est donné comme opération générique. C'est la part d'alignement que E014 faisait apprendre.
- 5 graines. ECH0 à 2/5 ne permet aucune loi générale.
- Le diagnostic est post hoc, sur des lots d'entraînement neufs.

## Calcul

CPU seul (numpy ; MLX sur CPU pour la phase A), 7 processus, sur le M1 partagé. Durées murales :

| étape | durée |
|---|---|
| Phase A | 1 min (pilote) + 2 min (officiel) |
| Pilotes phase B | ≈ 18 min |
| Runs N1 | 18 min |
| Runs N2 / N3 | 17 min |
| TEST, contrôles, diagnostic | ≈ 5 min |

Total ≈ 1 h de mur, budget de 4 h respecté.

## Reproduire

```
export PYTHONDONTWRITEBYTECODE=1
python -m unittest test_e015                                   # 11 tests
python ecosysteme.py --graines 1 2 3 4 5
python compose.py --proc 7 --runs {ECH0,EVO,ALEA,SANSVIE,ECH1,ECH2}-N1-s{1..5}   # relancer jusqu'à FILE TERMINEE
python compose.py --proc 7 --runs {FROID,CHAUD}-N{2,3}-s{1..5}
python controles15.py
python evalue15.py --runs …            # TEST, une seule fois par run
python analyse15.py && python diagnostic15.py
```
