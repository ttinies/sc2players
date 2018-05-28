"""
PURPOSE: manage records of all known players, both local and remote
"""

from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from six import iteritems, itervalues # python 2/3 compatibility

import glob
import os
import time

from sc2players import constants as c
from sc2players.playerRecord import PlayerRecord

################################################################################
playerCache = {} # mapping of player names to PlayerRecord objects


################################################################################
def addPlayer(settings):
    """define a new PlayerRecord setting and save to disk file"""
    for k,v in iteritems(settings): # restrict valid passed params
        if k == "created":  raise ValueError("parameter 'created' is expected to be automatmically generated.")
        if k == "_matches": raise ValueError("matches are declared after playing matches, not during init.")
    player = PlayerRecord(settings)
    player.save()
    getKnownPlayers()[player.name] = player
    return player


################################################################################
def updatePlayer(name, settings):
    """update an existing PlayerRecord setting and save to disk file"""
    player = delPlayer(name) # remove the existing record
    for k,v in iteritems(settings): # restrict valid passed params
        if k == "created":  raise ValueError("parameter 'created' is expected to be automatmically generated.")
        if k == "_matches": raise ValueError("matches are declared after playing matches, not during init.")
    player.update(settings)
    player.save()
    getKnownPlayers()[player.name] = player
    return player


################################################################################
def getPlayer(name):
    """obtain a specific PlayerRecord settings file"""
    if isinstance(name, PlayerRecord): return name
    try:    return getKnownPlayers()[name.lower()]
    except KeyError:
        raise ValueError("given player name '%s' is not a known player definition"%(name))


################################################################################
def delPlayer(name):
    """forget about a previously defined PlayerRecord setting by deleting its disk file"""
    player = getPlayer(name)
    try:    os.remove(player.filename) # delete from disk
    except IOError: pass # shouldn't happen, but don't crash if the disk data doesn't exist
    try:    del getKnownPlayers()[player.name] # forget object from cache
    except: pass
    return player # leave it to the caller to process further or allow deallocation 


################################################################################
def getKnownPlayers(reset=False):
    """identify all of the currently defined players"""
    global playerCache
    if not playerCache or reset:
        jsonFiles = os.path.join(c.PLAYERS_FOLDER, "*.json")
        for playerFilepath in glob.glob(jsonFiles):
            filename = os.path.basename(playerFilepath)
            name = filename.rstrip("\.json").lstrip("player_")
            player = PlayerRecord(name)
            playerCache[player.name] = player
    return playerCache


################################################################################
def getStaleRecords(limit=c.DEFAULT_TIME_LIMIT):
    ret     = []
    now     = time.time()
    seconds = float(limit) * 24 * 60 * 60 # convert days to seconds
    maxNoAct= min(seconds, c.NO_ACTIVITY_LIMIT * 24 * 60 * 60) # convert days to seconds
    for player in itervalues(getKnownPlayers()):
        if player.matches: # can only determine time since last match if matches exist
            sinceLastMatch, match = sorted( # player's last match is the shortest time since now 
                [(now - m.endTime, m) for m in player.matches])[0]
            if sinceLastMatch > seconds:
                ret.append(player)
        else: # if no matches, verify player's time since creation for sufficient time to play a match
            sinceCreation = now - player.created
            if sinceCreation > maxNoAct: # players created > 10 days ago without any recorded matches are identifed as stale
                ret.append(player)
    return ret


################################################################################
def removeStaleRecords(**kwargs):
    """identify all currently stale records and remove them"""
    return [delPlayer(record) for record in getStaleRecords(**kwargs)]


################################################################################
__all__ = ["addPlayer", "getPlayer", "delPlayer", "getKnownPlayers",
           "updatePlayer", "getStaleRecords", "removeStaleRecords"]

