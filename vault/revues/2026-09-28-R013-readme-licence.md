---
date: 2026-09-28
revue: R013
branche: docs/readme-2026-09-28
tip: 6812d1045c9973036c7054ed5091cc315e59e806
verdict: RESERVE
---

# R013 — Doublage du README racine + LICENSE (`docs/readme-2026-09-28`, tip 6812d10)

**Verdict global : RÉSERVE, donc pas de merge.** Le périmètre, les liens (31/31), les statuts de relecture, la LICENSE (identique mot pour mot au texte OSI), la sécurité et l'hygiène git sont irréprochables. Les 87 renvois « chiffre → ligne » vérifiés (21 entrées) se retrouvent tous au tip de leur branche. Deux défauts de **contexte** bloquent le GO (axe 2 et axe 5) :

1. **E012, formule du circuit (README l.141)** : `h = step(a + b + h − 9)`, `output = a + b + h − 10·h`. Les indices temporels ont disparu. Lue telle quelle, la sortie vaut `a + b − 9·h`, ce qui est faux. La source (E012 README l.28–29, tip 0a33881) écrit `h1 = marche(a + b + h1(t−1) − 9)` et `sortie = id(a + b + h1(t−1) − 10·h1)`. Le défaut existait déjà dans la version française (99ccc79 l.139) et la traduction l'a repris. **Correctif** : `h(t) = step(a + b + h(t−1) − 9)`, `output = a + b + h(t−1) − 10·h(t)`.
2. **Puce « What got over the wall » (README l.190)**, étiquetée [VERIFIED — E014, E015 ECH0, E016 DONNÉ] : « a given discrete symbolic interface … compose without loss up to 100 digits, and often up to 1,000 ».
   - Dans E015 ECH0, c'est le **câblage** qui est donné. L'**interface est à inventer** (E015 l.33, l.77), comme le dit correctement l'entrée 19 du README racine (l.166). ECH0 ne porte donc pas l'affirmation « interface donnée ».
   - « often up to 1,000 » est plus fort que les sources : E014 R1G 1/5 à 1 000 (l.63) ; E015 ECH0 2/5 (40,0 %, l.93) ; E016 DONNÉ 71,7 % à 1 000 (l.76), sous le seuil de 90 %. Aucune des trois ne franchit 1 000 chiffres sur la majorité de ses graines.
   - « without loss up to 100 digits » : vrai pour E014 (4/5) et DONNÉ (100 %), faux pour ECH0 (2/5 à 100).
   - **Correctif proposé** : retirer ECH0 de l'étiquette ou le citer à part (« wiring given, interface found by search: 2/5 ») ; remplacer « and often up to 1,000 » par « at 1,000 digits: 1/5 (E014), 71.7 % (E016 DONNÉ) ».

Les points ⚠️ mineurs ci-dessous (axe 5) sont à traiter dans la même passe, mais ne bloquent pas seuls.

## Tableau des axes

| # | Axe | Verdict | Raison vérifiée |
|---|---|---|---|
| 1 | Périmètre | ✅ GO | `git diff --name-only 10b8774 6812d10` = `LICENSE`, `README.md` |
| 2 | Chiffres | ⚠️ RÉSERVE | 87 renvois vérifiés sur les 21 entrées, 0 absent, 0 différent. Mais la formule d'E012 (l.141) est déformée : indices temporels perdus, sortie fausse telle qu'écrite |
| 3 | Statuts de relecture | ✅ GO | 21/21 conformes à `vault/revues/*` et `git branch -r --merged` (détail plus bas) |
| 4 | Liens | ✅ GO | 14 relatifs (13 sur `main`, `LICENSE` sur la branche) et 17 `tree/<branche>/<dossier>` : `git cat-file -e` OK pour les 31 |
| 5 | Honnêteté | ⚠️ RÉSERVE | Les échecs sont publiés comme des résultats, sans superlatif ni promesse. Mais la puce l.190 [VERIFIED] ne correspond pas à ses sources (ECH0, « often up to 1,000 ») ; 3 imprécisions mineures |
| 6 | Consignes Malik | ✅ GO | H1 exact ; anglais partout (résidus : citations « il a manger », « ils sont tombé », code `DONNÉ`, « doublage » glosé) ; méthode en tête (l.14) ; grep enfant : 3 occurrences de « son », toutes dans « sonde » ; section License = MIT + lien |
| 7 | LICENSE | ✅ GO | 21 lignes ; octet pour octet identique au texte MIT standard ; mot pour mot identique au texte de https://opensource.org/license/mit récupéré par `curl` (au remplacement près des guillemets typographiques du site) |
| 8 | Sécurité | ✅ GO | grep secrets : rc=1 ; grep adresse e-mail : rc=1 |
| 9 | Hygiène git | ✅ GO | 3/3 commits portent `Co-Authored-By: Malik & Claude` (le mandat en annonçait 4 : la branche en compte 3, `git rev-list --count origin/main..6812d10` = 3 ; le 4ᵉ, 5b977eb, est sur `main`) |

## Axe 5 — imprécisions mineures (⚠️, non bloquantes seules)
- l.189 [VERIFIED] « **Every time** the system must find on its own which digit to read, it fails beyond seen lengths » : E014 R0b a 1/5 graine exacte à 16 et 100 chiffres (E014 l.62). « Fails » est vrai au sens du critère préenregistré (≥ 4/5), pas au sens « à chaque fois ». Proposer : « fails the preregistered criterion ».
- l.180 « Senders freeze even faster (entropy 0.002 nat) » suit « 1 pair out of 9 in both cases » : 0,002 nat est la valeur d'IND-dense seule. IND-01-curric donne 0,018 (E016 tip e016-a2 l.234–235, l.256–257).
- l.61 « The 13 correct sentences are judged correct » : la source compte 13 **évaluations** de phrases justes (E005 l.108).
- l.148 « pure carry propagation drops to 52.9 % (1 seed out of 5) » : c'est une moyenne ± 40,5 à 1 000 chiffres (E013 l.100, l.172). Préciser « mean, at 1,000 digits ».

## Axe 2 — chiffres vérifiés (README d'expérience au tip de sa branche, ligne)
Choisis par moi, sur les 21 entrées. Aucun absent, aucun différent.
1. E001 : 6/6 conformes → E001 l.143 ; 3/3 répétitions T1-A/T1-B → l.150 ; 4/4 T2, 13/13 appels → l.120–121 ; 0 faux et sûr → l.123 ; 21/21 HTTP 403 → l.62.
2. E003 : Jev 10/10, gpt-4.1-mini 9/10, gemini 10/10 → E003 l.160 ; 3/3, confiance 1, 1, 0,9 → l.169.
3. E005 : 151 appels, 34 × 200 → E005 l.54 ; 9/42, 6 questions → l.104 ; 13/13, 7 évaluations → l.108 ; 19/28 au-dessus de 0,8 → l.119 ; 32 cas → l.15.
4. E006 : 103 appels → E006 l.39 ; 0,73/0,34/0,14/0,08 → l.74, l.103 ; −0,005 → l.86 ; 5/5 → l.47–51 ; contesté → l.52.
5. E007 : 0,84–0,86 → 0,05–0,09 → E007 l.101 ; 0,77 → 0,34 et 0,95 → 0,28 → l.77, l.80 ; 0,70 et 0,90 (règle retirée) → l.77, l.80 ; « partiellement » → l.83.
6. E002 : 5 à 10 % → E002 l.20 ; −0,003, 8/20 → l.69 ; 12/20 → l.70 ; +0,016 20/20 → l.64.
7. E002-bis : 20/20, +0,0122, minimum +0,0067 → E002bis l.75 ; 28 à 45 requêtes → l.78.
8. A0 : 1/4, −0,0110 → A0 l.79, l.115.
9. A0-bis : 22,6 → A0bis l.75, l.119 ; −0,0076 → l.78 ; −0,0105 → l.75 ; 0/4 → l.75.
10. A0-ter : 2/4 → A0ter l.53.
11. E008 : 91,2 / 7,9 → E008 l.78–79 ; 0,0 sur 3 graines → l.123 ; 65–68 % → l.127 ; 2 h 11 → l.115 ; ~3,2 M → l.149.
12. E009 : 50–110 k, 512 000 → E009 l.7 ; ≤ 3 % → l.10.
13. E009-bis : 96,8 (moyenne T-ID) → E009bis l.30 ; 17,3 → l.44 ; 3 h 52 → l.127 ; 10 000 pas, largeur 128 → l.8, l.18–20.
14. E010 : 99,9 % à 10 000 → E010 l.86, l.126 ; 256 000, ≥ 25× → l.127–128 ; 33,1 → l.71 ; 0 % dès 7 → l.136 ; 606/669 → l.103.
15. E011 : 22 paramètres → E011 l.40 ; L1 λ = 1 2/5 → l.14 ; 206 → 204 → l.15, l.77 ; différentiable 4/5 → l.16, l.76 ; ~4 min → l.6.
16. E012 : ≲ 0,6 % → E012 l.11 ; 0/5 binaire → l.14 ; 4/5 à 1 000 exemples → l.19, l.42 ; plat 0/5 → l.21 ; ~204 min → l.5 ; formule → l.28–29 (⚠️, voir plus haut).
17. E013 : 1 131 → E013 l.163 ; 99,3 → l.64, l.165 ; H = 2 100 % à 1 000, 5/5 → l.65, l.165–166 ; 98,6 → l.71 ; 52,9, 1/5 → l.100 ; I2 0/5 → l.68 ; 28 % → l.115, l.186 ; 65 min → l.121.
18. E014 : 4/5 / 4/5 / 1/5 → E014 l.63 ; R0a 0/5, R0b 1/5, R2 0/5 → l.61–65 ; 77,3 % / 1,4 % → l.104.
19. E015 : 1,100 → E015 l.163 ; 0,004–0,050 et 0,39–0,45 → l.164 ; 2/5 ECH0 → l.93 ; 400 000 → l.208 ; ≈ 1 h → l.273.
20. E016 : 25 runs sur 25 → E016 l.11 ; COLL 0/5, 1;1;1;1;2 → l.77 ; 13/13 → l.92 ; 0,0–0,1 % → l.169 ; 3,5× → l.174.
21. E016-A2 : 1/9 ×2, 0,002 → E016 (tip e016-a2) l.234–235 ; ≈ 3 min → l.245.

## Axe 3 — statuts
- Fusionnées (`git branch -r --merged origin/main`) : e001, e002, e002bis, e005 (+ doc/v2.2). Le README dit « Four have been reviewed and merged » : ✅.
- E001 R001 GO ; E002 R002 GO ; E002-bis R003 GO ; E005 R004 CASSE (total HTTP 8/109 contre 7/110, R004 l.13) puis R007 GO : ✅.
- E003 R005 RESERVE, tip 73cdc79 ancêtre du tip actuel 4e2b02b → correctifs non relus : ✅. E006 R008 RESERVE, 57e0e41 ancêtre de ad54bd4 : ✅.
- A0 / A0-bis : R009 RESERVE couvre les deux (titre « A0 M0014 + A0-bis M0016 » ; la réserve porte sur la lecture d'A0-bis, graine 19) : ✅.
- E008 / E013 : R010–R012 RESERVE, branche e013-insecte ; af281f5 (tip e008) en est l'ancêtre ; tests E008 rejoués dans R011–R012 : ✅.
- A0-ter, E007, E009 à E016-A2 : aucune revue ne les cite (`grep -liE` sur `vault/revues/` → vide) → « not yet reviewed » : ✅.

## Preuves brutes
```
$ git rev-parse origin/docs/readme-2026-09-28
6812d1045c9973036c7054ed5091cc315e59e806
$ git ls-tree origin/main README.md LICENSE          → (vide)
$ git diff --name-only $(git merge-base origin/main 6812d10) 6812d10
LICENSE
README.md
$ wc -l LICENSE → 21 ; diff LICENSE <MIT standard, Copyright (c) 2026 Malik Karaoui> → identique
$ git grep -nIiE 'set-cookie|x-vercel-id|cf-ray|bearer [a-z0-9]{8}|sk-[a-z0-9]{10}|team_[a-z0-9]{6}' 6812d10 -- README.md LICENSE → rc=1
$ head -n1 README.md → # 🧠🐜 EV-LLM — a public research log
$ grep -inE "son|child|kid|fils|enfant" README.md → l.45, l.48 (« E001-jev-sonde »), l.244 : « sonde » seulement
$ git show 99ccc79:README.md | grep -n 'marche('   → l.139 : `h = marche(a + b + h − 9)`, `sortie = a + b + h − 10·h`
$ git show origin/exp/e012-evolution:…/E012-evolution/README.md l.28–29
h1     = marche(a + b + h1(t−1) − 9)            # 1 ssi a + b + retenue ≥ 10 : la RETENUE
sortie = id(a + b + h1(t−1) − 10·h1)            # (a + b + retenue) mod 10
```

## Suite
Un mandat de correction de 2 à 6 lignes sur `docs/readme-2026-09-28` (l.141 et l.190 obligatoires, l.61, l.148, l.180, l.189 recommandées), puis un redoublage court limité à ce diff. Aucune autre partie n'est à revoir.

[VÉRIFIÉ] pour tout ce qui précède, commandes rejouables. Aucune conclusion générale.
