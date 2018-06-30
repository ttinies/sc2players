
"""
convert PlayerRecord data into PlayerPreGame
"""

from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from sc2players.playerRecord import PlayerRecord
from sc2players import constants as c


################################################################################
class PlayerPreGame(PlayerRecord):
    ############################################################################
    def __init__(self, playerProfile, selectedRace=c.RANDOM, observe=False, playerID=0):
        if isinstance(playerProfile, PlayerPreGame): # copy constructor (ignore other params)
            self.selectedRace   = playerProfile.selectedRace#c.SelectRaces(playerProfile.selectedRace.type)
            self.isObserver     = playerProfile.isObserver
            self.playerID       = playerProfile.playerID
        else:
            self.selectedRace   = c.SelectRaces(selectedRace)
            self.isObserver     = observe
            self.playerID       = playerID
        super(PlayerPreGame, self).__init__(source=playerProfile) # could also specify a player's profile name
    ############################################################################
    def __repr__(self):
        #if control == c.COMPUTER:   return super(PlayerPreGame, self).__repr__() # already declared
        added = ""
        if not self.isObserver:
            if self.playerID:
                added += "#%d "%self.playerID
            added += "%s "%(self.race.type)
        return "<%s %s%s %s-%s>"%(self.__class__.__name__,
            added, self.control.type, self.type.type, self.name)
    ############################################################################
    @property
    def control(self):
        """the type of control this player exhibits"""
        if   self.isComputer:   value = c.COMPUTER
        elif self.isObserver:   value = c.OBSERVER # only possible for a pre-game player
        else:                   value = c.PARTICIPANT
        return c.PlayerControls(value)
    ############################################################################
    @property
    def race(self):
        """implemented to allow derived classes to define race identification differently"""
        return self.selectedRace

