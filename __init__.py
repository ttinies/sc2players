"""
Copyright (c) 2018 Versentiedge LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS-IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


types of player profiles
    in-game PlayerAgent
        limited knowledge
        data applies to the single, specific game only
        differentiates between self / ally / opponent
            self includes additional control abilities
            ally provides perfect unit knowledge, but poses no threat
            opponent has imperfect knowledge, requires extrapolation/prediction
    out-of-game PlayerRecord
        player name / ID
        type of player
            AI / bot / human
            launch/init command (if AI or bot)
        match history record (IP address(es))
            use sc2matchHistory to log player name/IDs and selected/actual races

dependencies:
    sc2common (types, constants)

"""

from __future__ import absolute_import
from __future__ import division       # python 2/3 compatibility
from __future__ import print_function # python 2/3 compatibility

from sc2players.playerManagement  import addPlayer, updatePlayer, getPlayer, \
            delPlayer, buildPlayer, getKnownPlayers, getBlizzBotPlayers, \
            getStaleRecords, removeStaleRecords
from sc2players.playerRecord      import PlayerRecord
from sc2players.playerPreGame     import PlayerPreGame



