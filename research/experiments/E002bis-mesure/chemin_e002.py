"""Rend importables les modules d'E002 (réutilisés sans copie ni modification)."""

import os
import sys

E002 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "E002-relations-opaques")
if E002 not in sys.path:
    sys.path.insert(0, E002)
