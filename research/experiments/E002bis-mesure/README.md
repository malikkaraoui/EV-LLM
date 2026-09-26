# E002-bis — réparer la mesure : R̂ en différence et plafond-vérificateur

Mandat M0007, 2026-09-26. Python standard (≥ 3.9), aucune dépendance, aucun appel réseau, aucun LLM.

E002 (`../E002-relations-opaques/`) reste **tel quel** : c'est un résultat. Son critère ACQUÉRIR était inopérant sous le bruit préenregistré. Le plafond « savoir » y avait R ≤ 0 sur 12 mondes sur 20, ce qui rendait `R̂ = R / R_plafond` indéfini. E002-bis répare **la mesure**, sans toucher au banc ni baisser le bruit.

## Hypothèse

[HYPOTHÈSE] Un plafond qui **sait** les propriétés **et** vérifie par requête les prémisses de chacune de ses déductions garde R > 0 sous 5 à 10 % de bruit. Avec `R̂_diff = R − R_plafond` (toujours défini), le critère ACQUÉRIR redevient mesurable.

## Protocole

Tout est figé dans [`PREREGISTREMENT.md`](PREREGISTREMENT.md), committé seul (`c790767`) **avant** le code.
- Mêmes générateur, oracle, interface, R en bits, étalons et graines 1–20 qu'E002, **importés** depuis `../E002-relations-opaques/` (`chemin_e002.py`). Aucune copie de logique, aucun fichier d'E002 modifié.
- **Même bruit** qu'E002.
- **Nouvel étalon plafond-vérificateur** : il répond comme l'oracle-propriétés, puis demande au monde toute prémisse non encore vérifiée de ses `DÉDUIT` et `CONTRADICTION`, et recommence jusqu'à ce qu'il n'en reste aucune.
- **`R̂_diff = R − R_plafond-vérificateur`.**
- **Accélération dans une famille** : gain de R̂_diff du 1er au 5e monde ≥ 0.005, et au moins 3 hausses sur 4.
- **Critère ACQUÉRIR** : au moins 3 familles sur 4 en accélération.
- **Échec de la mesure** : plafond-vérificateur avec R ≤ 0 sur au moins 5 mondes sur 20.

| fichier | rôle |
|---|---|
| `chemin_e002.py` | rend importables les modules d'E002 |
| `etalons_bis.py` | plafond-vérificateur ; liste des 4 étalons |
| `evaluer_bis.py` | suite de mondes via `evaluer.evaluer_monde` d'E002, R̂_diff, critères, `results/<horodatage>/` |
| `tests/` | 9 tests unittest |

## Comment rejouer

```sh
cd research/experiments/E002bis-mesure
python3 -m unittest discover   # 9 tests
python3 evaluer_bis.py         # graines 1-20, écrit results/<horodatage>/
```

**Déterminisme.** `evaluer_bis.py` se relance avec `PYTHONHASHSEED=0`. En effet, le chaînage d'E002 choisit la preuve d'un atome selon l'ordre d'itération d'ensembles de chaînes, et les prémisses que demande le vérificateur en dépendent.
- [VÉRIFIÉ] Ce défaut a été découvert au premier rejeu : les R du vérificateur variaient d'environ ±1 requête sur quelques mondes. Cette première exécution n'a pas été gardée.
- [VÉRIFIÉ] Sur 8 valeurs de `PYTHONHASHSEED` (0 à 7) :
  - verdict identique (0 monde sur 20 avec R ≤ 0) ;
  - R moyen de 0.01217 à 0.01218 ;
  - les trois autres étalons ne varient pas.
- [VÉRIFIÉ] Deux exécutions complètes donnent un `resultats.json` identique, l'une sous `PYTHONHASHSEED=5` ambiant. Un test le vérifie entre deux processus.

**Contrôle des tests.** Huit mutations ont été injectées une à une :
- vérifier seulement les `CONTRADICTION` ;
- un seul passage sans boucle ;
- valeur de requête inversée ;
- réponses sans les requêtes ;
- R̂ en quotient ;
- seuil de gain retiré ;
- `R < 0` au lieu de `R ≤ 0` ;
- relance sans hachage fixé.

Les huit font échouer la suite [VÉRIFIÉ].

## Résultats

Exécution officielle : `results/2026-09-26T161842+0200/` (moyennes sur 20 mondes, réponses de phase 2).

**Mesure (§5) : plafond-vérificateur avec R ≤ 0 sur 0 monde sur 20 → RÉPARÉE.**

| étalon | exactitude | DÉDUIT infondés | DÉDUIT faux (vérité) | preuves valides | requêtes | bits exp. | bits économisés | R | mondes R > 0 | R̂_diff | R − R_oracle-propriétés | critère ACQUÉRIR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| aléatoire | 0.328 | 0.767 | 9.1 | 0.000 | 0.0 | 909 | −33.3 | −0.0366 | 0/20 | −0.0488 | −0.0336 | ÉCHEC (1/4 familles) |
| oracle-propriétés | 1.000 | 0.000 | 4.7 | 1.000 | 0.0 | 909 | −2.8 | −0.0031 | 8/20 | −0.0152 | 0.0000 | ÉCHEC (0/4) |
| **plafond-vérificateur** | 1.000 | 0.000 | **0.0** | 1.000 | 36.5 | 1249 | **+15.2** | **+0.0122** | **20/20** | 0.0000 | +0.0152 | ÉCHEC (0/4) |
| découvreur naïf | 0.777 | 0.258 | 8.3 | 0.679 | 62.0 | 1487 | −21.7 | −0.0142 | 5/20 | −0.0263 | −0.0111 | ÉCHEC (0/4) |

R par monde et courbes R̂_diff par famille : [`summary.md`](results/2026-09-26T161842+0200/summary.md).

## Lecture

- [VÉRIFIÉ] **La mesure est réparée au sens du critère (e), pour ce banc et ce jeu de paramètres.**
  - Le plafond-vérificateur a R > 0 sur les 20 mondes : minimum +0.0067, moyenne +0.0122.
  - Il ne rend aucun `DÉDUIT` faux en vérité, un test le vérifie monde par monde.
  - Un second test vérifie le processus : chaque prémisse de chaque réponse `DÉDUIT`/`CONTRADICTION` rendue est un atome demandé.
  - Le prix : 28 à 45 requêtes par monde (+37 % de bits d'expérience).
  - Ce R reste sous le +0.016 de l'oracle-propriétés sans bruit (diagnostic E002), comme prévu (§8).
- [VÉRIFIÉ] **Le verdict ACQUÉRIR est maintenant informatif, et les quatre étalons échouent comme ils le doivent** : ils ne gardent rien d'un monde à l'autre.
  - L'aléatoire « accélère » dans **une** famille par pur hasard : famille 0, gain +0.040, 3 hausses sur 4.
  - L'écart-type de R̂_diff d'un monde à l'autre est de 0.013 pour l'aléatoire et de 0.020 pour le découvreur, soit 3 à 4 fois le seuil de 0.005.
  - [HYPOTHÈSE] Le test à l'échelle d'une famille est donc permissif pour un système bruité. C'est l'exigence de 3 familles sur 4 qui protège le critère. Constaté, pas corrigé (§4).
- [VÉRIFIÉ] **L'écart entre plafond-vérificateur et découvreur est de 0.026 bit par bit en moyenne.** Le vérificateur fait mieux dans 20 mondes sur 20. Le R̂_diff du découvreur va de −0.081 à −0.002.
- [VÉRIFIÉ] **Le plafond-vérificateur n'est pas une borne supérieure stricte.** L'oracle-propriétés, qui ne paie aucune requête, le dépasse dans 3 mondes (graines 3, 8, 13), où le bruit ne l'a pas trompé. Un système peut donc avoir R̂_diff > 0 par chance ou par une vérification plus économe. `R̂_diff` se lit comme un écart à un étalon fort, pas comme une fraction d'un maximum.
- [HYPOTHÈSE] **Ce que ça impose à la future architecture candidate** (sur 20 mondes, un seul jeu de paramètres, rien de général) :
  1. **Savoir les règles ne suffit pas.** Sans vérifier ses prémisses, le « savoir » perd 0.015 bit par bit sous bruit. L'architecture doit porter une hiérarchie de confiance (§11 v2) : une conclusion hérite de la fiabilité de ses prémisses, et une prémisse observée seulement est à vérifier avant un `DÉDUIT`.
  2. **La vérification a un coût en bits, et il compte dans R.** Vérifier moins mais mieux (seulement les prémisses des déductions qui portent sur des atomes jamais vus, ou pondérer par le taux de bruit appris) est un levier de R distinct de l'acquisition des propriétés.
  3. **Pour réussir ACQUÉRIR, l'architecture doit faire monter son R̂_diff d'au moins 0.005 dans 3 familles sur 4.** Elle part du niveau du découvreur (≈ −0.026) et doit converger vers 0, donc acquérir **et** vérifier.

## Limites

- **Exactitude tautologique.** Le plafond-vérificateur partage le moteur de l'oracle : son exactitude de 1.000 l'est par construction. Seul son R est informatif.
- **Déterminisme.** Il repose sur un `PYTHONHASHSEED` fixé, parce que le choix de la preuve dans le chaînage d'E002 n'est pas canonique. Corriger E002 était hors mandat.
- **Seuil de gain.** Le seuil 0.005 est ancré sur un diagnostic d'E002 hors protocole ; il est du même ordre que la variabilité d'un monde à l'autre (voir Lecture).
- **Paramètres inchangés depuis E002.** Coût d'une requête égal à celui d'une observation, ε = 1/64, familles 1 et 3 sans composition.
- **Portée.** 20 mondes, un seul jeu de paramètres : aucune conclusion générale.

## Prochaine étape proposée

1. **Deuxième étalon « acquérir »** qui teste les propriétés **et** vérifie ses prémisses (découvreur-vérificateur) : c'est le vrai point de comparaison sans mémoire, sous R̂_diff.
2. **Architecture candidate** (mémoire entre les mondes) branchée sur l'interface d'E002, mesurée par R̂_diff contre le plafond-vérificateur.
3. **Canonicaliser le choix de preuve** dans un E002-ter si la reproductibilité sans `PYTHONHASHSEED` est exigée.
