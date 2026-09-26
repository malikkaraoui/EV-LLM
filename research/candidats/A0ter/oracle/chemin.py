"""Rend importables A0-bis, A0, E002 et E002-bis (réutilisés sans copie ni modification)."""

import os
import sys

_RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
A0BIS = os.path.join(_RACINE, "candidats", "A0bis")
A0 = os.path.join(_RACINE, "candidats", "A0")
E002 = os.path.join(_RACINE, "experiments", "E002-relations-opaques")
E002BIS = os.path.join(_RACINE, "experiments", "E002bis-mesure")
for _d in (A0, A0BIS, E002BIS, E002):
    if _d not in sys.path:
        sys.path.insert(0, _d)
