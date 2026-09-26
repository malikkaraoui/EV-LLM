"""Rend importables les modules d'E002 et d'E002-bis (réutilisés sans copie ni modification)."""

import os
import sys

_RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
E002 = os.path.join(_RACINE, "experiments", "E002-relations-opaques")
E002BIS = os.path.join(_RACINE, "experiments", "E002bis-mesure")
for _d in (E002BIS, E002):
    if _d not in sys.path:
        sys.path.insert(0, _d)
