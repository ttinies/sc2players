
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
    def __init__(self, playerProfile, selectedRace=c.RANDOM, observe=False):
        if isinstance(playerProfile, PlayerPreGame): # copy constructor (ignore other params)
            self.selectedRace   = playerProfile.selectedRace#c.SelectRaces(playerProfile.selectedRace.type)
            self.isObserver     = playerProfile.isObserver
        else:
            self.selectedRace   = c.SelectRaces(selectedRace)
            self.isObserver     = observe
        super(PlayerPreGame, self).__init__(source=playerProfile) # could also specify a player's profile name
    ############################################################################
    def __repr__(self):
        control = self.control()
        if control == c.COMPUTER:   return super(PlayerPreGame, self).__repr__() # already declared
        added = "" if self.isObserver else "%s "%(self.selectedRace.type)
        return "<%s %s%s %s-%s>"%(self.__class__.__name__,
            added, control.type, self.type.type, self.name)
    ############################################################################
    #@property
    def control(self):
        if   self.type == c.COMPUTER:   value = c.COMPUTER
        elif self.isObserver:           value = c.OBSERVER
        else:                           value = c.PARTICIPANT
        return c.PlayerControls(value)

