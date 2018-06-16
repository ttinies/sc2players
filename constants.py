
"""
constants that are applicable only to sc2players package
"""

from sc2common.constants import *
from sc2common.types     import *

import os

################################################################################
class InvalidPlayerTypeException(Exception): pass
class InvalidRaceException(      Exception): pass
class InvalidDifficultyException(Exception): pass

################################################################################
PLAYERS_FOLDER      = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataPlayers")
DEFAULT_TIME_LIMIT  = 90 # days
NO_ACTIVITY_LIMIT   = 10 # days
RECENT_MATCHES      = 15 # number of matches

