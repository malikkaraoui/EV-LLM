# E002 — chambre aux relations opaques : banc et étalons

Mandat M0005, 2026-09-26. Python standard (≥ 3.9), aucune dépendance, aucun appel réseau, aucun LLM.

C'est le **Test 2 — ACQUÉRIR** du §29 v2.1 de `architecture_cognitive_post_transformer.md` : la règle n'est pas donnée, le système doit découvrir les propriétés des relations, puis résoudre le monde suivant plus vite. Ce mandat construit le **banc** et trois **étalons**. Ce n'est **pas** encore l'architecture candidate.

## Hypothèse

[HYPOTHÈSE] Un banc où les propriétés des relations sont cachées, bruitées et piégées (≥ 30 % de relations non transitives) sépare trois niveaux :
- un système qui **sait** (on lui donne les propriétés) ;
- un système qui **acquiert naïvement** (il teste chaque monde depuis zéro) ;
- le hasard.

Il fournit ainsi le point de comparaison « sans mémoire » dont une architecture qui prétend **accélérer** d'un monde à l'autre (§28 v2, §56 v2) aura besoin.

## Protocole

Tout est figé dans [`PREREGISTREMENT.md`](PREREGISTREMENT.md), committé (`d8ef3a1`) **avant** le code (`340f99d`). En bref :
- 20 mondes (graines 1–20) répartis en 4 familles de 5. Au sein d'une famille, les propriétés sont les mêmes, sous d'autres noms.
- Chaque monde : 8 entités, 5 relations `R1…R5`, 96 observations en 2 phases, 5 à 10 % de bruit (dont une inversion ciblée en phase 2), 60 atomes tenus à l'écart, 20 questions de révision, 3 questions d'exclusion (variante A ou B du Test 1).
- Quatre étiquettes : `DÉDUIT` avec preuve, `HYPOTHÈSE`, `CONTRADICTION` avec règle citée, `INDÉTERMINÉ` avec manque.
- R en bits : bits économisés sur les atomes tenus à l'écart, par rapport à un prédicteur de fréquence, divisés par les bits d'expérience (requêtes comprises).

| fichier | rôle |
|---|---|
| `monde.py` | générateur déterministe par graine, sérialisable JSON |
| `raisonneur.py` | chaînage avant de Horn avec provenance ; vérificateur de preuve |
| `oracle.py` | étiquettes attendues, vérité terrain, coût en bits, R |
| `interface.py` | environnement interactif : observations par phase, requêtes facturées, journal |
| `etalons.py` | aléatoire, oracle-propriétés (plafond), découvreur naïf |
| `evaluer.py` | suite de mondes, métriques, courbe par famille, `results/<horodatage>/` |
| `tests/` | 22 tests unittest |
| `diagnostic_sans_bruit.py` | diagnostic **hors protocole** (voir Lecture) |

## Comment rejouer

```sh
cd research/experiments/E002-relations-opaques
python3 -m unittest discover        # 22 tests
python3 evaluer.py                  # graines 1-20, écrit results/<horodatage>/
python3 diagnostic_sans_bruit.py    # hors protocole
```

L'exécution est déterministe [VÉRIFIÉ] : deux passages donnent un `resultats.json` identique, à l'horodatage près.

Pour contrôler les tests eux-mêmes, dix mutations du code ont été injectées une à une dans une copie : antisymétrie, appartenance à une clause violée, règle « violation nouvelle », refus des atomes tenus à l'écart, priorité de la requête, exactitude d'une `HYPOTHÈSE`, probabilité d'un `DÉDUIT`, signe de R, générateur `CYCLE_PIEGE`, symétrie. Les dix font échouer la suite [VÉRIFIÉ]. Trois d'entre elles passaient au premier essai, ce qui a conduit à renforcer les tests correspondants avant l'exécution officielle.

## Résultats

Exécution officielle : `results/2026-09-26T160728+0200/` (moyennes sur 20 mondes, réponses de phase 2).

| étalon | exactitude d'étiquette | `DÉDUIT` infondés | `DÉDUIT` faux en vérité / monde | preuves valides | précision CONTRA | rappel CONTRA | exclusions justes /3 | requêtes | bits d'expérience | bits économisés | R | révisions requises justes | sur-révisions | critère ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aléatoire | 0.328 | 0.767 | 9.1 | 0.000 | 0.070 | 0.282 | 1.05 | 0 | 909 | −33.3 | −0.037 | 44/275 | 1105/1385 | ÉCHEC (0/4) |
| oracle-propriétés | 1.000 | 0.000 | 4.7 | 1.000 | 1.000 | 1.000 | 3.00 | 0 | 909 | −2.8 | −0.003 | 275/275 | 0/1385 | ÉCHEC (0/4) |
| découvreur naïf | 0.777 | 0.258 | 8.3 | 0.679 | 0.383 | 0.889 | 3.00 | 62 | 1487 | −21.7 | −0.014 | 177/222 | 284/1438 | ÉCHEC (0/4) |

R par monde, courbes R̂ par famille : [`summary.md`](results/2026-09-26T160728+0200/summary.md).

Diagnostic **hors protocole** (`diagnostic_sans_bruit.py`, mêmes mondes, observations remises à la vérité) :

| | R moyen avec bruit | R moyen sans bruit | mondes avec R > 0 sans bruit |
|---|---|---|---|
| oracle-propriétés | −0.003 | +0.016 | 20/20 |
| découvreur naïf | −0.014 | −0.016 | — |

## Lecture

- [VÉRIFIÉ] **Le plafond « savoir » ne bat pas le prédicteur de fréquence avec le bruit préenregistré.** Son R moyen vaut −0.003, et il n'est positif que dans 8 mondes sur 20. Toutes ses erreurs en vérité (4.7 `DÉDUIT` faux par monde) ont une prémisse bruitée : c'est vérifié sur les graines 6, 7 et 9, et le diagnostic sans bruit le confirme sur les 20 mondes (R > 0 partout). Déduire correctement à partir d'une observation fausse propage la faute, et chaque `DÉDUIT` faux coûte 6 bits alors qu'un `DÉDUIT` juste en rapporte moins de 1.
- [VÉRIFIÉ] **Conséquence : R̂ = R / R_plafond est indéfini dans 12 mondes sur 20.** La courbe de transfert du §3 n'est donc pas mesurable en l'état. Les trois verdicts « ÉCHEC » viennent en partie de cette indéfinition, pas d'une absence d'accélération constatée. C'est le constat principal de ce banc : **un écart au préenregistrement, rapporté et non corrigé.**
- [VÉRIFIÉ] **Écart entre le plafond et le découvreur :**
  - exactitude d'étiquette : 1.000 contre 0.777 ;
  - `DÉDUIT` infondés (l'erreur invisible du §1 bis) : 0 contre 25.8 % ;
  - précision de `CONTRADICTION` : 1.000 contre 0.383 ;
  - bits d'expérience : 1.6 fois plus pour le découvreur (62 requêtes par monde).
- [VÉRIFIÉ] **La cause principale des erreurs du découvreur :** sur 161 propriétés acceptées, 45 sont fausses, dont 29 compositions. Trois confirmations ne suffisent pas à établir `Ri∘Rj = Rk` : il ne teste que le sens `⊆`, sur des chaînes qu'il a lui-même choisies. Sans bruit, son R reste négatif (−0.016) : ce ne sont pas les observations qui le trompent, c'est sa manière d'accepter une règle.
- [VÉRIFIÉ] **Le Test 1 A/B tient dans la chambre.** Le plafond et le découvreur répondent juste aux 3 questions d'exclusion dans les 20 mondes : `CONTRADICTION` ou `DÉDUIT compatible` en variante A, `INDÉTERMINÉ` en variante B. Le hasard en réussit 1.05 sur 3.
- [VÉRIFIÉ] **Le découvreur ne s'accélère pas, par construction :** il repart de zéro à chaque monde, et un test le vérifie (même monde, même R, quel que soit l'historique). C'est le point de comparaison voulu pour la future architecture. La mesure de l'accélération, elle, reste à réparer (voir le point sur R̂).
- [HYPOTHÈSE] **Sur la difficulté du banc :** il est difficile dans un sens utile, car savoir les propriétés ne suffit pas quand 5 à 10 % des observations sont fausses. Pour gagner des bits, il faut **aussi** peser la fiabilité d'une observation (hiérarchie de confiance du §11 v2) et vérifier par requête avant de déduire. Aucun des trois étalons ne le fait. Ce n'est pas une conclusion générale : 20 mondes, un seul jeu de paramètres.

## Limites

- Le plafond partage le moteur de l'oracle : son exactitude de 1.000 est **tautologique**, comme le préenregistrement l'annonçait. Le moteur est contrôlé contre un point fixe naïf écrit autrement (test `FermetureIndependante`, 60 cas aléatoires) et contre des cas écrits à la main.
- **Composition :** seul le sens `Ri∘Rj ⊆ Rk` sert à déduire (le sens `⊇` est existentiel).
- **Proportion de pièges :** le tirage des profils a donné 3 à 4 relations non transitives sur 5 (60 à 80 %). C'est conforme au minimum de 30 %, mais plus que visé. Les familles 1 et 3 n'ont aucune composition.
- **Coût d'une requête :** aligné sur celui d'une observation (9.32 bits), un choix conservateur. Une requête facturée 1 bit changerait le R du découvreur.
- **Étalons manquants :** le LLM et le réseau (TRM/GNN) du §56 v2 ne sont pas encore construits.

## Prochaine étape proposée

1. **Préenregistrement E002-bis**, décision de l'orchestrateur : mesurer R̂ contre un plafond qui peut être battu (par exemple R − R_plafond, ou un plafond « savoir + vérifie ses prémisses par requête »), et figer ε.
2. **Deuxième étalon « acquérir »** qui pèse la fiabilité des observations (hiérarchie de confiance, §11 v2) et exige plus de 3 confirmations pour une composition.
3. **Brancher ensuite l'architecture candidate** (une mémoire entre les mondes) sur `interface.py` sans toucher au banc, et mesurer enfin la courbe n → n+1.
