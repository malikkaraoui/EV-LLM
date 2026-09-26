# A0-ter, Mission 1 — étalon « acquéreur-oracle » : le critère ACQUÉRIR est-il atteignable ?

Mandat M0020, 2026-09-26. Python standard (≥ 3.9), aucune dépendance, aucun appel réseau, aucun LLM. A0, A0-bis, E002 et E002-bis sont importés sans modification.

**Verdict préenregistré : le critère ACQUÉRIR n'est PAS atteignable sur ce banc.** Un système qui reçoit la connaissance exacte de chaque famille après son 1er monde n'accélère que dans **2 familles sur 4** (il en faut 3). Le contrôle amnésique : 0/4. Conformément au préenregistrement (§4), **la Mission 2 (candidat A0-ter) n'est pas lancée** : aucun candidat ne peut réussir un critère que l'acquisition parfaite ne réussit pas.

## Hypothèse

[HYPOTHÈSE de l'orchestrateur, M0020] A0 (1/4) et A0-bis (0/4) échouent ACQUÉRIR, et aucun étalon ne le réussit. On en avait déduit que le critère n'est pas trop permissif ; on n'avait jamais vérifié qu'il est **atteignable**. Si même une acquisition parfaite n'accélère pas au sens du critère, les échecs précédents ne disent rien des candidats : c'est la mesure qui est à réparer.

## Protocole

[`PREREGISTREMENT-oracle.md`](PREREGISTREMENT-oracle.md) a été committé et poussé seul (`fdf960a`, 18:07:23) **avant** le code (`7aaaffb`, 18:11:26). L'exécution officielle ([`oracle/results/2026-09-26T181138+0200/`](oracle/results/2026-09-26T181138+0200/summary.md)) a eu lieu après le commit du code. Aucune exécution sur les graines 1–20 n'a eu lieu avant elle ; les tests n'utilisent que les graines 1, 2, 3, 4 et 6.

- **`oracle_acquereur`** hérite d'`A0Bis`. Au 1er monde d'une famille, il **est** `a0bis`. À la fin de ce monde, il reçoit par un canal d'évaluateur la connaissance exacte de la famille, `K_f` : les vecteurs de propriétés vraies des 5 relations et les compositions vraies, sans aucun nom. Dans les 4 mondes suivants, `K_f` est placée sur les relations du monde par la bijection d'accord maximal (identification parfaite) et appliquée comme règles certaines ; plus aucun test de règle. Le reste est celui d'`a0bis` : déclencheur en coût marginal, bruit MLE, autodiagnostic.
- **`oracle_amnesique`** (contrôle) : le même, avec toute sa mémoire remise à zéro à chaque monde. C'est donc `a0bis` sans aucune mémoire.
- **`oracle_exact`** (diagnostic) : applique les propriétés vraies du monde courant au lieu de `K_f`. Il ne diffère de l'acquéreur qu'en graine 4, seul monde où les propriétés diffèrent de celles du 1er monde de la famille (la relation composée y est réflexive).
- Même banc, graines 1–20, 4 familles de 5 mondes, `evaluer_bis.evaluer_suite`, `R̂_diff = R − R_plafond-vérificateur`, critère ACQUÉRIR **inchangé** : `R̂_diff(5e) − R̂_diff(1er) ≥ 0.005` et au moins 3 hausses sur 4, dans au moins 3 familles sur 4.

| fichier | rôle |
|---|---|
| `oracle/chemin.py` | rend importables A0-bis, A0, E002 et E002-bis |
| `oracle/acquereur_oracle.py` | les 3 oracles, le canal d'évaluateur, `K_f` sans nom, la bijection |
| `oracle/evaluer_oracle.py` | 3 oracles + `a0bis` + 4 étalons, verdict §4, diagnostic §6, `results/<horodatage>/` |
| `oracle/tests/test_oracle.py` | 15 tests unittest |
| `oracle/tests/mutations.py` | 11 mutations injectées une à une dans une copie hors dépôt |

## Rejouer

```sh
cd research/candidats/A0ter/oracle
python3 -m unittest discover             # 15 tests, ~6 s
python3 evaluer_oracle.py                # graines 1-20, ~9 s, écrit results/<horodatage>/
python3 tests/mutations.py <scratch> "$(cd ../../.. && pwd)"   # 11 mutations
```

- [VÉRIFIÉ] **Rejeu déterministe.** Relancé sous `PYTHONHASHSEED=7` ambiant (le script se relance à 0), `resultats.json` est identique octet pour octet (`cmp`) ; `summary.md` ne diffère que par la ligne d'horodatage.
- [VÉRIFIÉ] **Contrôle de cohérence.** La ligne `a0bis` de cette exécution est celle de M0016 : M1 −0.0105, 22.6 requêtes, 0/4, même courbe par famille.
- [VÉRIFIÉ] **Tests** : temporalité de `K_f` (aucune règle d'oracle pendant les deux phases du 1er monde de chaque famille ; présente dès le 2e ; journal d'accès au canal) ; égalité avec `a0bis` au 1er monde ; `K_f` vient du 1er monde (graine 4) ; `K_f` sans nom ; bijection à la main ; départage par la composition ; amnésique sans mémoire (graine 2 seule = graine 2 après graine 1) ; seuils du verdict ; déterminisme entre deux processus.
- [VÉRIFIÉ] **11 mutations, toutes détectées** : `K_f` créée au début du monde ; amnésique qui garde la mémoire `a0bis` ; amnésique qui garde `K_f` ; pas de bijection ; acquéreur qui applique la vérité courante ; compositions ignorées dans la bijection ; règles d'oracle non utilisées ; seuil amnésique à 1 ; `K_f` qui garde les noms ; relance sans `PYTHONHASHSEED=0` ; seuil acquéreur à 2.

## Résultats

Moyennes sur 20 mondes, phase 2.

| système | exactitude | DÉDUIT faux (vérité) | requêtes | R | R̂_diff (M1) | familles accélérées | M3 gain 1er→5e |
|---|---|---|---|---|---|---|---|
| plafond-vérificateur | 1.000 | 0.00 | 36.5 | +0.0122 | 0 | 0/4 | — |
| oracle-propriétés | 1.000 | 4.70 | 0.0 | −0.0031 | −0.0152 | 0/4 | — |
| découvreur naïf | 0.777 | 8.30 | 62.0 | −0.0142 | −0.0263 | 0/4 | — |
| aléatoire | 0.328 | 9.10 | 0.0 | −0.0366 | −0.0488 | 1/4 | — |
| a0bis (M0016, rejoué) | 0.829 | 3.10 | 22.6 | +0.0017 | −0.0105 | 0/4 | +0.0021 |
| **oracle_acquereur** | **0.964** | **0.90** | 18.3 | **+0.0124** | **+0.0003** | **2/4** | **+0.0062** |
| oracle_amnesique | 0.788 | 2.55 | 26.9 | +0.0032 | −0.0090 | 0/4 | −0.0063 |
| oracle_exact (diagnostic) | 0.964 | 0.90 | 18.2 | +0.0124 | +0.0003 | 2/4 | +0.0062 |

Courbe R̂_diff d'`oracle_acquereur` par famille, avec le diagnostic préenregistré (§6) :

```text
                                                              gain    hausses  écart_1  σ(2–5)   moy(2–5)
famille 0 : -0.0076 → +0.0006 → +0.0023 → -0.0014 → +0.0013   +0.0088  3/4     +0.0083  0.0015  +0.0007  → OUI
famille 1 : -0.0018 → +0.0013 → +0.0023 → +0.0011 → +0.0017   +0.0035  3/4     +0.0034  0.0006  +0.0016  → non (gain < 0.005)
famille 2 : -0.0022 → +0.0019 → +0.0012 → +0.0025 → +0.0012   +0.0033  2/4     +0.0039  0.0006  +0.0017  → non (gain et hausses)
famille 3 : -0.0071 → +0.0017 → +0.0033 → +0.0011 → +0.0018   +0.0089  3/4     +0.0091  0.0009  +0.0020  → OUI
```

`écart_1` = moyenne des mondes 2–5 moins le 1er monde ; σ(2–5) = écart-type des mondes 2–5.

`K_f` appliquée égale les propriétés vraies du monde courant dans 15 mondes sur 16, toutes sauf la graine 4.

## Prédictions préenregistrées (§5) contre observé

| prédiction | observé | tenue ? |
|---|---|---|
| mandat : `oracle_acquereur` ≥ 3/4 | 2/4 | **non** |
| mandat : `oracle_amnesique` ≤ 1/4 | 0/4 | oui |
| auteur : P(oracle ≥ 3/4) = 30 % | 2/4 | l'échec était le cas jugé le plus probable |
| M1 oracle > M1 `a0bis` (−0.0105) | +0.0003 | oui |
| M4 oracle < M4 `a0bis` (3.1) | 0.90 | oui |
| `oracle_exact` et `oracle_acquereur` : même nombre de familles | 2 et 2 | oui |

## Lecture

- [VÉRIFIÉ] **Le critère ACQUÉRIR n'est pas atteignable sur ce banc, au sens préenregistré** : l'acquisition parfaite ne réussit que 2 familles sur 4. `oracle_exact`, qui reçoit en plus les propriétés exactes du monde courant, fait de même (2/4) : l'échec ne vient pas de l'instabilité de la famille 0 (graine 4).
- [VÉRIFIÉ] **L'acquisition parfaite a un effet énorme, que le critère ne voit pas.** M1 passe de −0.0105 (`a0bis`) à +0.0003 ; les `DÉDUIT` faux, de 3.1 à 0.9 par monde ; l'exactitude, de 0.829 à 0.964. Dans les mondes 2 à 5, l'oracle **dépasse le plafond-vérificateur** dans 15 mondes sur 16 : mêmes propriétés, mais 18 requêtes au lieu de 36.5.
- [VÉRIFIÉ] **Le 1er monde domine tout.** Tout le gain se fait à la transition 1→2 (`écart_1` de +0.0034 à +0.0091) ; ensuite la courbe est plate (σ de 0.0006 à 0.0015, moyenne des mondes 2–5 entre +0.0007 et +0.0020). Le gain 1er→5e est donc borné par la distance du 1er monde au plafond, `−R̂_diff(1er)`, plus le petit excès au-dessus du plafond.
  - Familles 1 et 2 : le 1er monde est déjà à −0.0018 et −0.0022. Même parfaite, l'acquisition ne peut pas y gagner 0.005 : gains +0.0035 et +0.0033.
  - Familles 0 et 3 : le 1er monde est à −0.0076 et −0.0071, il y a de la marge : gains +0.0088 et +0.0089, accélération.
  - Le seuil de gain ne mesure donc pas l'acquisition. Il mesure **à quel point le 1er monde d'une famille était raté**.
- [VÉRIFIÉ] **La condition « 3 hausses sur 4 » exige un progrès continu qu'une acquisition parfaite ne produit pas.** Une fois `K_f` reçue, les mondes 2–5 ont tous la même connaissance ; le sens des transitions 2→3, 3→4 et 4→5 est du bruit : 7 hausses sur 12, soit 2, 2, 1 et 2 par famille. La famille 2 échoue aussi pour cette raison (2/4).
  - [HYPOTHÈSE] Le critère mesure un **apprentissage progressif** au fil des 5 mondes, pas une acquisition. Un acquéreur en un coup, qui est le cas idéal, y est pénalisé.
- [VÉRIFIÉ] **La variance d'un monde à l'autre ne noie pas le gain de l'oracle** (σ ≤ 0.0015, contre un `écart_1` ≥ 0.0034). Elle noie en revanche celui des systèmes qui ne savent pas : σ(2–5) de 0.007 à 0.033 pour `a0bis`, de 0.002 à 0.010 pour l'amnésique.
- [VÉRIFIÉ] **Contrôle.** L'amnésique échoue (0/4) et aucun étalon ne réussit (aléatoire 1/4). Le critère n'est pas trop permissif, mais il n'est pas atteignable : il ne discrimine rien.
- [VÉRIFIÉ] **Constat annexe.** L'amnésique (M1 −0.0090) fait mieux qu'`a0bis` (−0.0105) : la mémoire d'`a0bis`, telle qu'elle est, coûte en moyenne plus qu'elle ne rapporte sur ces 20 mondes. Les écarts sont petits devant la variabilité ; aucun test statistique n'était préenregistré.
- **Conséquence pour A0 et A0-bis.** [HYPOTHÈSE] Leurs échecs à ACQUÉRIR (1/4, 0/4) ne peuvent pas être lus comme « ces candidats n'acquièrent pas » : même un acquéreur parfait échoue. Leurs autres résultats (M1, M4, requêtes) restent valables.

## Réparation proposée du critère (NON appliquée)

Le préenregistrement interdit de l'appliquer ici. Elle passerait par un nouveau préenregistrement du **critère**, calibré sur ces étalons **avant** tout nouveau candidat.

1. **Contraste apparié avec un jumeau amnésique**, au lieu de la pente 1er→5e. Pour chaque famille : `Δ_f = moyenne R̂_diff(mondes 2–5 du système) − moyenne R̂_diff(mondes 2–5 de son jumeau amnésique)`. Le jumeau est le même système avec sa mémoire remise à zéro à chaque monde. La famille est « acquise » si `Δ_f ≥ s`. Ce contraste isole causalement ce que la mémoire apporte, sur les mêmes mondes. Il ne dépend ni de la chance du 1er monde, ni d'un progrès continu.
   - Exploratoire, calculé après résultats, **ne vaut pas résultat** : `Δ_f` vaut +0.0107, +0.0129, +0.0119 et +0.0107 pour l'oracle (4/4 à `s = 0.005`), et −0.0035, +0.0076, −0.0021 et −0.0100 pour `a0bis` (1/4).
2. **Seuil `s` calibré sur le bruit** avant tout candidat : par exemple un multiple de l'écart-type inter-mondes de jumeaux amnésiques, ou d'une permutation de l'ordre des mondes dans une famille. Le cas `a0bis`, famille 1 (+0.0076 avec une dispersion d'environ 0.007), montre qu'un seuil absolu de 0.005 laisserait passer du bruit.
3. **Plus de familles ou de graines par famille** : 4 familles donnent au verdict une granularité de 25 %. Le critère devrait être évalué sur au moins 8 familles, avec un contrôle de puissance sur l'oracle et l'amnésique.
4. **Garder l'étalon oracle comme test d'atteignabilité** de toute nouvelle version du critère : l'oracle doit réussir, l'amnésique doit échouer, avant de juger un candidat.

Option écartée : un seuil relatif (« le système comble au moins la moitié de l'écart entre le 1er monde et le plafond »). Il est instable quand le 1er monde est déjà proche du plafond (familles 1 et 2), et l'oracle dépasse ce plafond.

## Limites

- **20 mondes, 4 familles, un seul jeu de paramètres.** « Non atteignable » est un constat sur **ce** banc et **ce** critère, pas une conclusion générale.
- **2/4 contre un seuil de 3/4** : un verdict à une famille près. Deux causes indépendantes sont vérifiées (la marge du 1er monde, les hausses après saturation), mais un autre tirage de familles aurait pu donner 3/4 par chance ; ce serait alors une réussite de hasard, pas un critère sain.
- **L'oracle hérite d'`a0bis`**, y compris son déclencheur et son bruit MLE. Un oracle bâti sur une autre base aurait un autre 1er monde, donc une autre marge : le diagnostic « le 1er monde domine » en dépend.
- **Le plafond-vérificateur n'est pas une borne** (déjà noté par E002-bis et A0) : l'oracle le dépasse.
- **Le canal d'évaluateur** donne à l'oracle le monde courant pour la bijection (identification parfaite). C'est voulu (étalon), et c'est journalisé et testé.

## Prochaine étape

1. **Préenregistrer un critère ACQUÉRIR-v2** (contraste apparié avec un jumeau amnésique, seuil calibré sur le bruit, plus de familles), le **valider sur l'oracle et l'amnésique d'abord**, puis seulement rejuger A0, A0-bis et un éventuel A0-ter.
2. **A0-ter** (échantillon de vérification neutre, garde-fou anti-cascade) : à préenregistrer **après** le critère v2, pas avant.
