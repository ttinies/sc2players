
"""
command-line interface to interact with the player repository
"""
from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from six import itervalues # python 2/3 compatibility

import sys
import time

from sc2players import constants as c
from sc2players.playerManagement import *


#################################################################################
if __name__=='__main__': # mini/unit test
    """
    PURPOSE: command-line interface for map information
    """
    from argparse import ArgumentParser
    usage_def = ""#usage:  %prog  <gameVersion>  <options>"
    parser = ArgumentParser(usage_def, description=__doc__)
    # main routine behavior
    #parser.add_argument("--list"        , default=None, action="store_true" , help="Display all known players.")
    #parser.add_argument("--path"        , default=None, action="store_true" , help="provide the absolute path to the file")
    #
    #parser.add_argument("--all"         , action="store_true"   , help="Display all known ladders.")
    
    actionOpts = parser.add_argument_group('player record action options (pick at most one)')
    actionOpts.add_argument("--add"         , action="store_true"               , help="Add settings as a new player definition. (Provide criteria)")
    actionOpts.add_argument("--update"      , type=str                          , help="update settings for selected record.")
    actionOpts.add_argument("--get"         , type=str                          , help="the specific player to highlight.")
    actionOpts.add_argument("--rm"          , type=str                          , help="the specific player to remove from the player database.")
    actionOpts.add_argument("--stale"       , type=float                        , help="select all stale player records (specify value in days)")
    actionOpts.add_argument("--rmstale"     , type=float                        , help="remove all stale player records (specify value in days)")
    filterOpts = parser.add_argument_group('player --get filter options')
    filterOpts.add_argument("--exclude"     , action="store_true"               , help="exclude players with names specified by --get.")
    filterOpts.add_argument("--best"        , action="store_true"               , help="match players that are closer with --get")
    #filterOpts.add_argument("--race"        
    criteriaOpts = parser.add_argument_group('critiera used when --add, --update OR select display options are specified')
    criteriaOpts.add_argument('criteria'    , nargs='*'                         , help="define additional criteria as key=value pairs") # the remaining arguments are processed together
    displayOpts = parser.add_argument_group('display options')
    displayOpts.add_argument("--details"    , default=None, action="store_true" , help="show details of each player identified.")
    displayOpts.add_argument("--summary"    , action="store_true"               , help="show an additional summary")
    displayOpts.add_argument("--matches"    , type=int                          , help="display the most recent X matches")
    displayOpts.add_argument("--apm"        , type=int                          , help="calculate the apm for the most recent X matches (0 = all matches)")
    #displayOpts.add_argument("--recent"     , type=int                          , help="display the recent RECENT matches")
    
    # player match filter options?
    # race
    # duration
    options = parser.parse_args()
    criteria= {} # translate options.args into a dictionary
    terms   = [a.split('=') for a in options.criteria]
    try:
        for i,(k,v) in enumerate(terms):
            criteria[k] = v
    except ValueError:
        print("ERROR: key '%s' must specify a value using '=' followed by a value (no whitespace)."%(terms[i][0]))
        sys.exit(1)
    action = True
    # identify which player records are desired/affected by the retrieval option
    if   options.stale:     records = getStaleRecords(limit=options.stale)
    elif options.rmstale:  records = removeStaleRecords(limit=options.rmstale)
    elif options.get:       records = [getPlayer(options.get)] ; options.nosummary=True # ensure the single record is a list
    elif options.add:       records = [addPlayer(criteria)]    ; options.nosummary=True
    elif options.update:    records = [updatePlayer(options.update, criteria)] ; options.nosummary=True
    elif options.rm:        records = [delPlayer(options.rm)]  ; options.nosummary=True 
    else:                   records = list(itervalues(getKnownPlayers(reset=True))); action=False
    # perform the desired action on them
    for r in records:
        printStr = "%15s : %s"
        print(r)
        if options.details:
            attrs = [("type", r.type)]
            if r.type in [c.BOT, c.AI]:
                attrs.append(("init command", r.initCmd))
            attrs.append(("total matches", len(r.matches)))
            attrs.append(("creation", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(r.created))))
            for k,v in attrs:#sorted(iteritems(attrs), reverse=True):
                print(printStr%(k, v))
        if options.apm:
            if options.matches: apm = r.apmRecent(maxMatches=options.matches, **criteria)
            else:               apm = r.apmAggregate(**criteria)
            print(printStr%("apm", apm))
        if options.matches:
            newCriteria = dict(criteria)
            newCriteria["maxMatches"] = options.matches
            foundMatches = r.recentMatches(**newCriteria)
            print(printStr%("recent matches", len(foundMatches)))
            for m in foundMatches:
                print(" "*12, m)
    if options.summary:
        print("num players(s)%s: %d"%(" affected by action" if action else "", len(records)))

