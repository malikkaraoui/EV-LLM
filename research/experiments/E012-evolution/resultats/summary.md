# E012 -- resume des resultats (test final, graines 1-5)

## X1 ({'base': 2, 'format': 'aligne', 'n_train': 100}) -- 0/5 graines exactes, 0 >= 90 % a 16, verdict : non

| graine | exacte | preuve | cachees | connexions | biais | \|G\| | \|D:G\| | generations | enfants | evaluations | 1re decouverte (evaluations) | s | arret |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | non | FAUX | 0 | 2 | 1 | 47 | 308.1 | 12000 | 19200000 | 9696643 | - | 3337 | budget de generations |
| 2 | non | FAUX | 0 | 2 | 1 | 47 | 308.1 | 12000 | 19200000 | 9666212 | - | 3324 | budget de generations |
| 3 | non | FAUX | 0 | 2 | 1 | 47 | 308.1 | 12000 | 19200000 | 9664247 | - | 3325 | budget de generations |
| 4 | non | FAUX | 0 | 2 | 1 | 47 | 308.1 | 12000 | 19200000 | 9656757 | - | 3322 | budget de generations |
| 5 | non | FAUX | 0 | 2 | 1 | 47 | 313.8 | 12000 | 19200000 | 9624069 | - | 3312 | budget de generations |

Evaluations jusqu'a la decouverte : []

| jeu | moyenne | ecart | min | faux surs (total) |
|---|---|---|---|---|
| A-ASYM|10 | 25.0 % | 0.0 | 25.0 % | 0 |
| A-ASYM|16 | 34.0 % | 0.0 | 34.0 % | 0 |
| A-ASYM|32 | 30.0 % | 0.0 | 30.0 % | 0 |
| A-ASYM|64 | 26.0 % | 0.0 | 26.0 % | 0 |
| A-ASYM|100 | 24.0 % | 0.0 | 24.0 % | 0 |
| A-ASYM|1000 | 29.0 % | 0.0 | 29.0 % | 0 |
| A-CASCADE|10 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|16 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|32 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|64 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|100 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|1000 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|10 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|16 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|32 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|64 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|100 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|1000 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|10 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|16 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|32 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|64 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|100 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|1000 | 0.0 % | 0.0 | 0.0 % | 0 |
| V-OOD|6 | 0.0 % | 0.0 | 0.0 % | 0 |
| V-OOD|7 | 0.0 % | 0.0 | 0.0 % | 0 |
| V-OOD|8 | 0.0 % | 0.0 | 0.0 % | 0 |

## X2-100 ({'base': 10, 'format': 'aligne', 'n_train': 100}) -- 2/5 graines exactes, 2 >= 90 % a 16, verdict : parfois

| graine | exacte | preuve | cachees | connexions | biais | \|G\| | \|D:G\| | generations | enfants | evaluations | 1re decouverte (evaluations) | s | arret |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | non | FAUX | 0 | 3 | 0 | 50 | 2060.0 | 3739 | 5982400 | 4673087 | - | 2701 | budget mur |
| 2 | oui | PROUVE | 2 | 8 | 0 | 144 | 0.0 | 775 | 1240000 | 1107380 | 484642 | 1033 | arret anticipe (exact train+val, MDL stable) |
| 3 | oui | PROUVE | 1 | 7 | 0 | 116 | 0.0 | 3025 | 4840000 | 3909606 | 2973842 | 2566 | arret anticipe (exact train+val, MDL stable) |
| 4 | non | FAUX | 0 | 3 | 0 | 50 | 2000.0 | 3764 | 6022400 | 4721070 | - | 2700 | budget mur |
| 5 | non | FAUX | 0 | 3 | 0 | 50 | 2720.0 | 3761 | 6017600 | 4699908 | - | 2700 | budget mur |

Evaluations jusqu'a la decouverte : [484642, 2973842]

| jeu | moyenne | ecart | min | faux surs (total) |
|---|---|---|---|---|
| A-ASYM|10 | 48.4 % | 42.1 | 14.0 % | 258 |
| A-ASYM|16 | 50.2 % | 40.7 | 17.0 % | 249 |
| A-ASYM|32 | 55.0 % | 36.7 | 25.0 % | 225 |
| A-ASYM|64 | 48.4 % | 42.1 | 14.0 % | 258 |
| A-ASYM|100 | 45.4 % | 44.6 | 9.0 % | 273 |
| A-ASYM|1000 | 47.8 % | 42.6 | 13.0 % | 261 |
| A-CASCADE|10 | 40.0 % | 49.0 | 0.0 % | 6 |
| A-CASCADE|16 | 40.0 % | 49.0 | 0.0 % | 6 |
| A-CASCADE|32 | 40.0 % | 49.0 | 0.0 % | 6 |
| A-CASCADE|64 | 40.0 % | 49.0 | 0.0 % | 6 |
| A-CASCADE|100 | 40.0 % | 49.0 | 0.0 % | 6 |
| A-CASCADE|1000 | 40.0 % | 49.0 | 0.0 % | 6 |
| A-ZEROS|10 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|16 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|32 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|64 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|100 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|1000 | 100.0 % | 0.0 | 100.0 % | 0 |
| T-OOD|10 | 40.2 % | 48.8 | 0.4 % | 1494 |
| T-OOD|16 | 40.0 % | 49.0 | 0.0 % | 1500 |
| T-OOD|32 | 40.0 % | 49.0 | 0.0 % | 1500 |
| T-OOD|64 | 40.0 % | 49.0 | 0.0 % | 1500 |
| T-OOD|100 | 40.0 % | 49.0 | 0.0 % | 1500 |
| T-OOD|1000 | 40.0 % | 49.0 | 0.0 % | 600 |
| V-OOD|6 | 41.8 % | 47.5 | 3.0 % | 1455 |
| V-OOD|7 | 40.6 % | 48.5 | 1.0 % | 1485 |
| V-OOD|8 | 40.2 % | 48.8 | 0.4 % | 1494 |

## X2-1000 ({'base': 10, 'format': 'aligne', 'n_train': 1000}) -- 4/5 graines exactes, 4 >= 90 % a 16, verdict : decouvre

| graine | exacte | preuve | cachees | connexions | biais | \|G\| | \|D:G\| | generations | enfants | evaluations | 1re decouverte (evaluations) | s | arret |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | oui | NON_PROUVABLE | 4 | 12 | 3 | 239 | 0.0 | 700 | 1120000 | 1033112 | 540514 | 2520 | arret anticipe (exact train+val, MDL stable) |
| 2 | oui | NON_PROUVABLE | 5 | 13 | 0 | 244 | 0.0 | 945 | 1512000 | 1341971 | 1120456 | 2703 | budget mur |
| 3 | oui | PROUVE | 2 | 9 | 2 | 176 | 0.0 | 820 | 1312000 | 1226115 | 511836 | 2702 | budget mur |
| 4 | non | FAUX | 0 | 3 | 0 | 50 | 22600.0 | 1683 | 2692800 | 2165248 | - | 2700 | budget mur |
| 5 | oui | PROUVE | 1 | 7 | 1 | 117 | 0.0 | 816 | 1305600 | 1210362 | 210546 | 2702 | budget mur |

Evaluations jusqu'a la decouverte : [540514, 1120456, 511836, 210546]

| jeu | moyenne | ecart | min | faux surs (total) |
|---|---|---|---|---|
| A-ASYM|10 | 82.8 % | 34.4 | 14.0 % | 86 |
| A-ASYM|16 | 83.4 % | 33.2 | 17.0 % | 83 |
| A-ASYM|32 | 85.0 % | 30.0 | 25.0 % | 75 |
| A-ASYM|64 | 82.8 % | 34.4 | 14.0 % | 86 |
| A-ASYM|100 | 81.8 % | 36.4 | 9.0 % | 91 |
| A-ASYM|1000 | 82.6 % | 34.8 | 13.0 % | 87 |
| A-CASCADE|10 | 80.0 % | 40.0 | 0.0 % | 2 |
| A-CASCADE|16 | 80.0 % | 40.0 | 0.0 % | 2 |
| A-CASCADE|32 | 80.0 % | 40.0 | 0.0 % | 2 |
| A-CASCADE|64 | 80.0 % | 40.0 | 0.0 % | 2 |
| A-CASCADE|100 | 80.0 % | 40.0 | 0.0 % | 2 |
| A-CASCADE|1000 | 80.0 % | 40.0 | 0.0 % | 2 |
| A-ZEROS|10 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|16 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|32 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|64 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|100 | 100.0 % | 0.0 | 100.0 % | 0 |
| A-ZEROS|1000 | 100.0 % | 0.0 | 100.0 % | 0 |
| T-OOD|10 | 80.1 % | 39.8 | 0.4 % | 498 |
| T-OOD|16 | 80.0 % | 40.0 | 0.0 % | 500 |
| T-OOD|32 | 80.0 % | 40.0 | 0.0 % | 500 |
| T-OOD|64 | 80.0 % | 40.0 | 0.0 % | 500 |
| T-OOD|100 | 80.0 % | 40.0 | 0.0 % | 500 |
| T-OOD|1000 | 80.0 % | 40.0 | 0.0 % | 200 |
| V-OOD|6 | 80.6 % | 38.8 | 3.0 % | 485 |
| V-OOD|7 | 80.2 % | 39.6 | 1.0 % | 495 |
| V-OOD|8 | 80.1 % | 39.8 | 0.4 % | 498 |

## X3 ({'base': 10, 'format': 'plat', 'n_train': 100}) -- 0/5 graines exactes, 0 >= 90 % a 16, verdict : non

| graine | exacte | preuve | cachees | connexions | biais | \|G\| | \|D:G\| | generations | enfants | evaluations | 1re decouverte (evaluations) | s | arret |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | non | SANS_OBJET | 1 | 4 | 1 | 87 | 5873.5 | 229 | 366400 | 218502 | - | 2703 | budget mur |
| 2 | non | SANS_OBJET | 1 | 6 | 1 | 115 | 5568.6 | 133 | 212800 | 163792 | - | 2705 | budget mur |
| 3 | non | SANS_OBJET | 2 | 5 | 1 | 107 | 6013.9 | 114 | 182400 | 147064 | - | 2703 | budget mur |
| 4 | non | SANS_OBJET | 1 | 4 | 2 | 92 | 5668.8 | 169 | 270400 | 180489 | - | 2718 | budget mur |
| 5 | non | SANS_OBJET | 1 | 2 | 1 | 51 | 6018.1 | 108 | 172800 | 139454 | - | 2706 | budget mur |

Evaluations jusqu'a la decouverte : []

| jeu | moyenne | ecart | min | faux surs (total) |
|---|---|---|---|---|
| A-ASYM|10 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ASYM|16 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ASYM|32 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ASYM|64 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ASYM|100 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ASYM|1000 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|10 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|16 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|32 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|64 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|100 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-CASCADE|1000 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|10 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|16 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|32 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|64 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|100 | 0.0 % | 0.0 | 0.0 % | 0 |
| A-ZEROS|1000 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|10 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|16 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|32 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|64 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|100 | 0.0 % | 0.0 | 0.0 % | 0 |
| T-OOD|1000 | 0.0 % | 0.0 | 0.0 % | 0 |
| V-OOD|6 | 0.0 % | 0.0 | 0.0 % | 0 |
| V-OOD|7 | 0.0 % | 0.0 | 0.0 % | 0 |
| V-OOD|8 | 0.0 % | 0.0 | 0.0 % | 0 |
