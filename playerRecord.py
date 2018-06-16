"""
PURPOSE: manage records of all known players, both local and remote
"""

from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from builtins import str as text # python 2/3 compatibility
from six import iteritems # python 2/3 compatibility

import json
import os
import time

from sc2players import constants as c
from sc2matchHistory import getPlayerHistory


################################################################################
class PlayerRecord(object):
    """manage the out-of-game meta data of a given player"""
    AVAILABLE_KEYS = [
        "name",
        "type",
        "difficulty",
        "initCmd",
        "rating",
    ]
    ############################################################################
    def __init__(self, source=None, **override):
        # define default values and their type
        self.name                   = ""
        self.type                   = c.PlayerDesigns(c.HUMAN)
        self.difficulty             = c.ComputerDifficulties(None) # only matters if type is a computer
        self.initCmd                = "" # only used if self.type is an AI or bot
        self.rating                 = 500
        self.created                = time.time() # origination timestamp
        self._matches               = [] # match history
        # initialize with new values
        if   isinstance(source, text):          self.load(source) # assume a player file to load
        elif isinstance(source, dict):          self.update(source) # assume attribute dictionary
        elif isinstance(source, PlayerRecord):  self.update(source.__dict__) # copy constructor
        self.update(override)
        if not self.name:
            raise ValueError("must define 'name' parameter as part of %s source settings"%(self.__class__.__name__))
        if self.type in [c.BOT, c.AI] and not self.initCmd:
            raise ValueError("must provide initCmd attribute when specifying type=%s"%self.type)
    ############################################################################
    def __str__(self): return self.__repr__()
    def __repr__(self):
        if self.isComputer: diff = "-%s"%self.difficulty.type 
        elif self.rating:   diff = "-%d"%self.rating
        else:               diff = "" 
        return "<%s %s %s%s>"%(self.__class__.__name__, self.name, self.type.type, diff)
    ############################################################################
    def __call__(self, attrs, **kwargs):
        """update internals according to parameters"""
        self.update(attrs) # allow a dictionary to be passed
        self.update(kwargs)
        return self
    ############################################################################
    @property
    def isAI(self):         return self.type == c.AI
    ############################################################################
    @property
    def isBot(self):        return self.type == c.BOT # an AI with pre-defined, scripted actions
    ############################################################################
    @property
    def isHuman(self):      return self.type == c.HUMAN
    ############################################################################
    @property
    def isComputer(self):   return self.type == c.COMPUTER
    ############################################################################
    @property
    def isMulti(self):      return self.type == c.ARCHON
    ############################################################################
    @property
    def isStoredLocal(self):
        """determine whether this player can be run locally"""
        raise NotImplementedError("TODO -- determine whether this player is an already known player")
    ############################################################################
    @property
    def filename(self):
        """return the absolute path to the object's filename"""
        return os.path.join(c.PLAYERS_FOLDER, "player_%s.json"%(self.name))
    ############################################################################
    @property
    def attrs(self):
        """provide a copy of this player's attributes as a dictionary"""
        ret = dict(self.__dict__) # obtain copy of internal __dict__
        del ret["_matches"] # match history is specifically distinguished from player information (and stored separately)
        if self.type != c.COMPUTER: # difficulty only matters for computer playres
            del ret["difficulty"]
        return ret
    ############################################################################
    @property
    def simpleAttrs(self):
        """provide a copy of this player's attributes as a dictionary, but with objects flattened into a string representation of the object"""
        simpleAttrs = {}
        for k,v in iteritems(self.attrs):
            if k in ["_matches"]: continue # attributes to specifically ignore
            try:    simpleAttrs[k] = v.type
            except: simpleAttrs[k] = v
        return simpleAttrs
    ############################################################################
    @property
    def matches(self):
        """retrieve the match history for this player from the matchHistory repo and cache the result"""
        if not self._matches: # load match History applicable to this player
            self._matches = getPlayerHistory(self.name)
        return self._matches
    ############################################################################
    def _validateAttrs(self, keys):
        """prove that all attributes are defined appropriately"""
        badAttrsMsg = ""
        for k in keys:
            if k not in self.__dict__:
                badAttrsMsg += "Attribute key '%s' is not a valid attribute"%(k)
        if not keys: return # is iterable, but didn't contain any keys
        if badAttrsMsg:
            raise ValueError("Encountered invalid attributes.  ALLOWED: %s%s%s"\
                %(list(self.__dict__), os.linesep, badAttrsMsg))
    ############################################################################
    def load(self, playerName=None):
        """retrieve the PlayerRecord settings from saved disk file"""
        if playerName: # switch the PlayerRecord this object describes
            self.name = playerName # preset value to load self.filename
        try:
            with open(self.filename, "rb") as f:
                data = f.read()
        except Exception:
            raise ValueError("invalid profile, '%s'. file does not exist: %s"%(self.name, self.filename))
        self.update(json.loads(data))
        self._matches = [] # mandate match history be recalculated for this newly loaded player
    ############################################################################
    def save(self):
        """save PlayerRecord settings to disk"""
        data = str.encode( json.dumps(self.simpleAttrs, indent=4, sort_keys=True) )
        with open(self.filename, "wb") as f:
            f.write(data)
    ############################################################################
    def update(self, attrs):
        """update attributes initialized with the proper type"""
        self._validateAttrs(attrs)
        for k,v in iteritems(attrs):
            typecast = type( getattr(self, k) )
            if typecast==bool and v=="False":   newval = False # "False" evalued as boolean is True because its length > 0
            elif "<" in str(v) or v==None:      newval = typecast(v)
            else:                               newval = typecast(str(v).lower())
            setattr(self, k, newval)
        if self.isComputer: pass
        elif "difficulty" in attrs and attrs["difficulty"]!=None: # the final state of this PlayerRecord cannot be a non-computer and specify a difficulty
            raise ValueError("%s type %s=%s does not have a difficulty"%(
                self.__class__.__name__, self.type.__class__.__name__, self.type.type))
        else: self.difficulty = None
    ############################################################################
    def matchSubset(**kwargs):
        """extract matches from player's entire match history given matching criteria kwargs"""
        ret = []
        for m in self.matches:
            allMatched = True
            for k,v in iteritems(kwargs):
                mVal = getattr(m, k)
                try:
                    if v == mVal or v in mVal: continue # this check passed
                except Exception: pass # if attempting to check __contains__ and exception is raised, it's assumed to be false
                allMatched = False
                break
            if allMatched: ret.append(m)
        return ret
    ############################################################################
    def apmRecent(self, maxMatches=c.RECENT_MATCHES, **criteria):
        """collect recent match history's apm data to report player's calculated MMR"""
        if not self.matches: return 0 # no apm information without match history
        #try:        maxMatches = criteria["maxMatches"]
        #except:     maxMatches = c.RECENT_MATCHES
        apms = [m.apm(self) for m in self.recentMatches(maxMatches=maxMatches, **criteria)]
        return sum(apms) / len(apms)
    ############################################################################
    def apmAggregate(self, **criteria):
        """collect all match history's apm data to report player's calculated MMR"""
        apms = [m.apm(self) for m in self.matchSubset(**criteria)]
        if not apms: return 0 # no apm information without match history
        return sum(apms) / len(apms)
    ############################################################################
    def recentMatches(self, **criteria):
        """identify all recent matches for player given optional, additional criteria"""
        if not self.matches: return [] # no match history
        try: # maxMatches is a specially handled parameter (not true criteria)
            maxMatches = criteria["maxMatches"]
            del criteria["maxMatches"]
        except AttributeError:
            maxMatches = c.RECENT_MATCHES
        alLMatches = self.matchSubset(**criteria)
        matchTimes = [(m.endTime, m) for m in matches]
        selMatches = sorted(matchTimes)[:maxMatches] # slice off X most recet matches
        retMatches = [m for endTime,m in selMatches] # extract matches only
        return retMatches
        
