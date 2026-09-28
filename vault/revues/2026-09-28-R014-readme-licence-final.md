---
date: 2026-09-28
revue: R014
branche: docs/readme-2026-09-28
tip: f99553a89ff4af7fd4c873c232c06d4aaeef9887
verdict: RESERVE
---

# R014 — Redoublage du README racine + LICENSE (`docs/readme-2026-09-28`, tip f99553a)

**Verdict global : RÉSERVE, donc pas de merge.** Huit axes sur neuf sont ✅. Les six retouches de M0038 disent ce que disent leurs sources, à une nuance près (retouche 3, voir plus bas). Les 15 chiffres que j'ai tirés, tous différents de ceux de R013, sont présents et exacts au tip de leur branche. Les formules sont conformes symbole par symbole. Liens, statuts, LICENSE, sécurité et hygiène git sont sans défaut.

L'axe 5 étendu (la relecture des puces [VERIFIED] source par source) trouve **deux nouveaux cas de la classe de défaut qu'a relevée R013** : une puce [VERIFIED] qui affirme plus que ce que portent ses sources.

1. **l.191** `[VERIFIED — E012 X1, …] What did not get over it: blind evolution without alignment`. Dans E012, **X1 est la condition « binaire aligné (Lan) »** (E012 `0a33881` README l.40 : `| X1 binaire aligné (Lan) | 100 | **0/5** |`). La condition sans alignement est **X3 « décimal plat (E008) »** (l.43, 0/5). L'étiquette ne porte donc pas l'affirmation. Le défaut existait déjà dans la version française (`99ccc79` l.189 : `[VÉRIFIÉ — E012 X1, …] l'évolution aveugle sans alignement`). La traduction l'a gardé, et ni R013 ni M0038 ne l'ont vu.
2. **l.189** (retouche 3 de M0038) : `[VERIFIED — E008, …] Whenever the system must find on its own which digit to read, it fails beyond seen lengths … — the single exception being one seed out of five with a curriculum (E014 R0b …)`. Or E008, cité dans la même étiquette, donne pour B-REF **91,2 ± 6,2 % à 6 chiffres** (graines 90,2 / 97,8 / 85,6 ; E008 `af281f5` README l.78), au-delà des longueurs vues (1–5). L'entrée 11 du README racine le dit elle-même : « pushes the boundary out by one digit ». « The single exception » est une affirmation d'exclusivité **ajoutée par le correctif**, et sa propre étiquette la contredit.
   - [HYPOTHÈSE] On peut soutenir que B-REF (NoPE + sortie inversée) reçoit une partie de la structure de lecture et ne « trouve » donc pas seul. Mais la puce ne fait pas cette distinction, et le README d'E008 ne l'établit pas.

**Loi des deux patchs (§0-bis du mandat).** R013 a déjà demandé un correctif pour cette classe de défaut, et elle revient : une fois dans un texte d'origine resté inaperçu, une fois introduite par le correctif lui-même. **Je ne dicte pas de troisième correctif.** Recommandation : **relecture systématique, par un tiers, de toutes les puces de synthèse (étiquette → chaque source → chaque affirmation) avant tout nouveau README**, puis une seule passe de correction qui couvre l'ensemble des puces, et pas seulement ces deux-là.

## Tableau des axes

| # | Axe | Verdict | Raison vérifiée |
|---|---|---|---|
| 1 | Périmètre | ✅ GO | `git diff --name-only $(git merge-base origin/main f99553a) f99553a` = `LICENSE`, `README.md`. `git diff --stat 6812d10 f99553a` = README.md seul, +6/−6, six zones `@@ -61`, `-141`, `-148`, `-180`, `-189,2` (189 et 190) |
| 2 | Chiffres | ✅ GO | 15 chiffres, choisis hors de la liste de R013 : 15/15 présents et exacts (liste plus bas) |
| 3 | Statuts de relecture | ✅ GO | Fusionnées : e001, e002, e002bis, e005 (= « Four … merged »). R005 tip 73cdc79 ancêtre d'e003 4e2b02b ; R008 tip 57e0e41 ancêtre d'e006 ad54bd4 ; R012 tip = e013 044545e, e008 af281f5 ancêtre d'e013. Aucune revue ne porte sur A0-ter, E007, E009–E016-A2 : R009 ne cite A0-ter que comme prochaine étape (l.22, l.162) |
| 4 | Liens | ✅ GO | 14 relatifs (13 sur `origin/main`, `LICENSE` sur la branche) et 17 `tree/<branche>/<dossier>` : `git cat-file -e` OK pour les 31 |
| 5 | Honnêteté (étendu) | ⚠️ RÉSERVE | Les échecs sont publiés comme des résultats, sans superlatif ni promesse. Les formules sont conformes. Mais 2 puces [VERIFIED] sur 6 ne sont pas portées par leurs sources (l.191 E012 X1, l.189 « single exception »). C'est la même classe de défaut que dans R013 |
| 6 | Consignes Malik | ✅ GO | H1 exact. Méthode en tête (l.14). Seul résidu français hors citations et codes : « ils sont tombé », qui est une citation. `grep -inE "son\|child\|kid\|fils\|enfant"` ne trouve que « sonde » (l.45, 48, 244) et aucune mention de l'enfant. Section License = MIT + lien `LICENSE` |
| 7 | LICENSE | ✅ GO | 21 lignes ; l.1 `MIT License`, l.3 `Copyright (c) 2026 Malik Karaoui`. Corps identique mot pour mot au texte de https://opensource.org/license/mit récupéré par `curl` (guillemets typographiques du site normalisés) ; inchangée depuis 6812d10 |
| 8 | Sécurité | ✅ GO | grep secrets : rc=1 ; grep adresse e-mail : rc=1 |
| 9 | Hygiène git | ✅ GO | `git rev-list --count origin/main..f99553a` = 4 ; les 4 commits (99ccc79, ebec0d3, 6812d10, f99553a) portent `Co-Authored-By: Malik & Claude` |

## Les six retouches de M0038 : source → avant → après

| # | Ligne | Source (tip) | Verdict |
|---|---|---|---|
| 1 | l.141 E012 | `0a33881` l.28–29 `h1 = marche(a + b + h1(t−1) − 9)`, `sortie = id(a + b + h1(t−1) − 10·h1)` | ✅ `h(t) = step(a + b + h(t−1) − 9)`, `output = a + b + h(t−1) − 10·h(t)`. Le `h1` sans indice de la source est h1(t), ce qui est conforme |
| 2 | l.190 interface | E014 `fc698b4` l.63 (R1G 4/5 / 4/5 / 1/5, critère ≥ 90 %), l.71 (s2 98,4 à 100) ; E015 `58abf67` l.33, l.75–77 (câblage donné, table d'interface non donnée), l.93 (ECH0 2/5), l.107–108 (s1, s3 100/100/100) ; E016 `867ccaf` l.76 (DONNÉ 5/5, 9 ×5, 100,0, 71,7), l.92–93 (limite = lecteur) | ✅ porté, affirmation par affirmation |
| 3 | l.189 | E014 l.62 (R0b 1/5 / 1/5 / 0/5), l.70 (s2 100/99,8/62,5) | ⚠️ Le chiffre R0b est exact. Mais « the single exception » est contredit par E008 l.78 (B-REF 91,2 % à 6 chiffres), qui figure dans la même étiquette |
| 4 | l.180 A2 | `1c98601` E016 README l.234 (IND-dense 0,002), l.235 (IND-01-curric 0,018) ; `867ccaf` l.125–126 (0,07–0,23 COLL, 0,03–0,16 IND) | ✅ Nuance : A2 mesure l'entropie « fin » de run (en-tête l.232) et E016 la mesure « au meilleur checkpoint ». La comparaison vient de la source elle-même (A2 l.257), donc elle est portée |
| 5 | l.61 E005 | `15487b0` l.108 « Les 13 évaluations de phrases justes sont conformes (13/13) » | ✅ |
| 6 | l.148 E013 | `044545e` l.100 `I3 N = 1 000 … 52,9 ± 40,5 … 1/5`, jeu ADV-PROPAG (l.89–93), s4 102/102/102 | ✅ « on average (± 40.5) at 1,000 digits, with 1 seed out of 5 above 90 % » |

## Axe 5 étendu : formules

- l.141, E012 : voir la retouche 1. ✅
- l.88, E002-bis : « measure as a difference (R − R_ceiling) » → E002-bis `d35af60` l.17 `R̂_diff = R − R_plafond-vérificateur`. ✅
- l.135, E011 : « L2 penalty λ = 1: 0/5; L1 λ = 1: 2/5 » → E011 `994c77b` l.14–15. ✅
- l.67, E006 : « P(contradiction) 0.73 → 0.34 → 0.14 → 0.08 » → E006 `ad54bd4` l.74 (médianes). ✅ Le README ne précise pas « median », mais les valeurs sont identiques.
- l.179, E016-A2 : « reward = fraction of correct columns » → A2 l.227, l.234. ✅

## Axe 5 étendu : puces [VERIFIED — …], puce → source:ligne → porté / non porté

1. **l.188** [E011, E012, E013] « Computing is easy… »
   - Carry trouvée par évolution, une unité cachée → E012 l.24–29 : porté.
   - 1 131 paramètres → E013 l.19 : porté.
   - « 100 to 10,000 examples » → E012 l.17 (100 ex., 2/5) et E013 l.72 (10 000, 100 %) : porté.
   - Stable sous entropie croisée → E011 l.12 (5/5 jusqu'à 1 000 bits) : porté.
   - Tient jusqu'à 1 000 chiffres → E012 l.42, l.50 et E013 l.65 : porté.
   - **Porté.**
2. **l.189** [E008, E009-bis, E010, E013 I2, E014 R0] « The wall is locating… »
   - E009-bis 17,3 / 0 (l.44) ; E010 33,1 / 0 dès 7 (l.71, l.136) ; E013 I2 0/5 (l.68) ; E014 R0b 1/5 (l.62) : portés.
   - « ~1,900 to ~3.2 million » → E013 l.20 et E008 l.28 : porté.
   - **« the single exception » : non porté.** E008 l.78 donne B-REF 91,2 ± 6,2 à L = 6.
   - **⚠️**
3. **l.190** [E014, E015 ECH0, E016 DONNÉ] : voir la retouche 2. **Porté.**
4. **l.191** [E012 X1, E015, E016, E016-A2] « What did not get over it »
   - « blind evolution without alignment » ← E012 X1 : **non porté**. X1 = binaire **aligné**, E012 l.40. La condition sans alignement est X3, l.43.
   - « free assembly » → E015 l.9–10, l.90 (0/5) : porté.
   - « all-or-nothing social pressure » → E016 l.9–14, l.77 : porté.
   - « a dense scalar signal » → A2 l.234 : porté.
   - **⚠️**
5. **l.192** [E005, E006, E008, E010, E013, E015] « Misplaced confidence is blind »
   - E005 9/42 (l.104) ; E006 5/5 (l.47–51) ; E008 65–68 % (l.127) : portés.
   - « the copy » → E010 606/669, l.103 : porté.
   - « the computation without the reading » → E013 28 % faux et sûrs (l.186), avec une confiance calculée sur les chiffres émis (l.107–108) : porté.
   - « the champions without the interface » → E015 l.214, l.224 (7 673 / 13 783) : porté. Nuance : E015 l.226 précise que les champions n'émettent pas de probabilité, donc leurs faux sont « sûrs » par définition.
   - « separates much better (E014) » → E014 l.104 (R1G 77,3 % / 1,4 %) : porté.
   - **Porté.**
6. **l.224** [VERIFIED — sources listed in the note] → `origin/main:vault/notes/2026-09-27-anteriorite-signal-intermediaire-e015-a2.md` l.16–24 (Lehman, Schmidhuber, HOUDINI…), l.33 « Partiellement fait. Chaque brique existe séparément ». **Porté.**
7. La 7ᵉ occurrence de `VERIFIED` (l.31) est la définition de l'étiquette, sans affirmation.

## Axe 2 — 15 chiffres vérifiés (README d'expérience au tip de sa branche, ligne), aucun repris de R013

1. E001 « 7 preregistered cases » (l.46) → E001 `7e953a9` l.170 « 7 cas ». ✅
2. E006 « P between 0.85 and 0.97 » (l.67) → E006 `ad54bd4` l.66, l.99. ✅
3. E006 « 1 response reclassified as contested » → E006 l.52, l.92. ✅
4. E007 « corrects all 3 pairs » → E007 `0436a8a` l.71 (3/3 paires). ✅
5. A0 « 3 were required » → A0 `8a60250` l.32 (≥ 3 familles sur 4). ✅
6. A0 « 0 queries over 20 worlds » → A0 l.119. ✅
7. E008 « 0.1 % at 8 » → E008 `af281f5` l.80. ✅
8. E008 / méthode « MLX 0.29.3 » → E008 l.30. ✅
9. E009-bis « 1 run out of 5 » → E009bis `e489db9` l.8. ✅
10. E010 « never 95 % with up to 256,000 » → E010 `19f7f0d` l.116. ✅
11. E011 « 5/5 up to 1,000 bits » → E011 `994c77b` l.12. ✅
12. E012 « aligned decimal 2/5 with 100 examples » → E012 `0a33881` l.17, l.41. ✅
13. E013 « 100 % from 16 to 100 digits (5/5), 99.3 % at 1,000 » → E013 `044545e` l.64 ; « with 10,000, 100 % everywhere » → l.72, l.86. ✅
14. E015 « 0/5 on three new tasks » → E015 `58abf67` l.9–10 ; « 0.004 and 0.45 » → l.164. ✅
15. E016 « 0 symbols shared » + « one or two pair idiolects » → E016 `867ccaf` l.10–11, l.167. ✅
16. (en plus) E016-A2 « 0.018 » → A2 l.235 ; « 0.03–0.16 for IND » → E016 l.125–126. ✅
17. (en plus) Méthode « Mac M1 16 GB » → `origin/main:vault/notes/2026-09-27-genese-suite.md` l.21. ✅

## Preuves brutes
```
$ git rev-parse origin/docs/readme-2026-09-28
f99553a89ff4af7fd4c873c232c06d4aaeef9887
$ git ls-tree origin/main README.md LICENSE           → (vide)
$ ls vault/revues/ | grep -i R014                     → (vide, rc=1)
$ git diff --name-only $(git merge-base origin/main f99553a) f99553a
LICENSE
README.md
$ git diff --stat 6812d10 f99553a
 README.md | 12 ++++++------
$ git show 0a33881:research/experiments/E012-evolution/README.md | sed -n '40p;43p'
| X1 binaire aligné (Lan) | 100 | **0/5** | 0 | — | — | — (rendu : 0 / 2 / 1, MDL 355) | — |
| X3 décimal plat (E008) | 100 | **0/5** | 0 | sans objet | — | — | — |
$ git show af281f5:research/experiments/E008-addition/README.md | sed -n 78p
| T-OOD | 6 | **0,0 ± 0,0** | **91,2 ± 6,2** (90,2 / 97,8 / 85,6) |
$ git show 99ccc79:README.md | sed -n 189p
- [VÉRIFIÉ — E012 X1, E015, E016, E016-A2] **Ce qui ne l'a pas franchi :** l'évolution aveugle sans alignement, …
$ git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' f99553a -- README.md LICENSE → rc=1
$ curl -sL https://opensource.org/license/mit → corps MIT identique à LICENSE (python, espaces normalisés) : True
$ git branch -r --merged origin/main | grep exp/
  origin/exp/e001-sonde-jev  origin/exp/e002-relations-opaques  origin/exp/e002bis-mesure  origin/exp/e005-jev-hors-distribution
```

## Suite
- Pas de merge.
- Recommandation (loi des deux patchs) : **relecture systématique, par un tiers, de toutes les puces de synthèse** du README (l.188–192, l.224), étiquette par étiquette et source par source, avant tout nouveau README. Ensuite, une seule passe de correction qui couvre l'ensemble des puces, puis un redoublage.
- Les corrections vers lesquelles pointent les sources, à confirmer par ce tiers et non dictées ici :
  - l.191 : citer E012 **X3** (plat, 0/5) pour « sans alignement », ou reformuler X1 comme le piège « hésitant » en binaire aligné ;
  - l.189 : retirer « single » ou mentionner E008 B-REF (6 chiffres).
- Leçon, candidate transverse (R5) : un correctif qui ajoute une clause d'**exclusivité** (« seul », « unique exception ») doit être vérifié contre **toutes** les sources de l'étiquette, pas seulement contre celle qui motive le correctif.

[VÉRIFIÉ] pour tout ce qui précède, sauf l'[HYPOTHÈSE] signalée (B-REF). Commandes rejouables. Aucune conclusion générale.
