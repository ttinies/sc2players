[![PyPI](https://img.shields.io/pypi/v/sc2players.svg)](https://pypi.org/project/sc2players/)
[![Build Status](https://travis-ci.org/ttinies/sc2players.svg?branch=master)](https://travis-ci.org/ttinies/sc2players)
[![Coverage Status](https://coveralls.io/repos/github/ttinies/sc2players/badge.svg?branch=master)](https://coveralls.io/github/ttinies/sc2players?branch=master)
![Crates.io](https://img.shields.io/crates/l/rustc-serialize.svg)

# Define human or AI players to compete in Starcraft 2 matches

### Purpose

Various Starcraft 2 processes rely on understanding players and differentiating this.  This package provides capability to
define them such that matches can be started, identify the player(s) within the match and act as a key for performance
across matches.

## Installation

On a command line, perform the intended query or operation.  All queries are performed on the user's local machine.
(To query remote player definitions, use the [sc2gameLobby](https://github.com/ttinies/sc2gameLobby).

> EXAMPLE: `python sc2players <options>`

To view the complete and up-to-date options and how to use them, review the --help documentation.

> EXAMPLE: `python sc2players --help`

## Usage

#### Command line operation

For general use, the intent is to utilize this package's interface.  Unless incorporated into external python code, the
command-line interface is the primary means to acquire player information.  After specifying the command to invoke this
package, the remaining parameters specify the operation to be performed and any parameters for that operation.  (**NOTE:**
specifying no arguments after the package name simply displays all known players.)

> EXAMPLE: `python -m sc2players <operation> <parameters>`

> EXAMPLE: `python -m sc2players --help`

#### Create your own human player

Only two parameters must be supplied to create a human player.  Name your player and specify its `type` as `human`.
Each new player that joins the ladder starts with a 500 rating which helps distinguish how well the player performs
by winning ladder matches.

> EXAMPLE: `python -m sc2players --add name=foreverbronze type=human`

#### Create your own AI bot definition

Similar to creating a human player, name and type must be supplied.  However, an additional parameter must be specified,
`initCmd`.  Details for this additional paremeter depend on whether you are running a python-based bot or something
else.  Also, instead of `type=human`, your type value can be either `ai` or `bot`.
* If you're using code to understand data and make decisions (e.g. if `<condition>` then `<perform action>`), set the
type as `bot`.
* Otherwise if your code uses machine learning in some form to make its decisions, set the type as `ai`.

**NOTE**: in realtime mode, it is possible to skip gameloop values and also possible to receive multiple copies of the
same observation, depending on how busy the Starcraft 2 game client is, latency associated with data transfer, etc. 

##### python AI / bot

The `initCmd` format must be followed strictly. The format is `<your_package_name>` followed by each additional
package/module/attribute needed to access your initializing function.  First, your package will be imported.  Then each
subsequent accessor is accessed until the presumed initializtion routine can be invoked.  The initialization routine is
called without any parameters.  The return value from this function (callable) must be a list (an indexable iterable).
The first value (index 0) in this list must be a callback function.  Each time a game state observation is received from
the connected Starcraft 2 client, your callback function is invoked and the observation is passed as a parameter.  Any
additional indexes in the returned list can contain python objects of any kind that you wish to persist over the course
of the game. Additional indexes are optional and subject to your own implementation.

> `initCmd` format EXAMPLE: "cheeseBot.source.initFunction"

In this example, your bot is defined in the `cheeseBot` package (which must be available in your environment).  It's 
submodule `source` is accessed and ultimately your `initFunction` is accessed then called.  The return value from
`initFunction` must be a list whose first index is a callback function. The callback function is invoked initially once
to pass the absolute filepath of the json game configuration.  This callback function is then subsequently invoked each
time a new observation is received.

> EXAMPLE: `python -m sc2players -add name=cheesebot type=bot initCmd="cheeseBot.source.initFunction"`

##### non-python AI / bot

The `initCmd` format for non-python bots is fairly loose.  Whatever you put into this command will be executed verbatim.
Because you specify the command content and the command ultimately runs locally on your machine, this is safe.  It is
highly recommended that you supply the `__CFG_DATA__` keyword as a placeholder for the filepath name of the file that
contains the json data for the game configuration.  Interpreting that game configuration data for your bot appropriately
is important.

> EXAMPLE: `python -m sc2players -add name=cheesebot type=bot initCmd="runbot.exe --cfg=__CFG_DATA__"`

Also, by running your own instance, additional expectations are placed on you (or at least your framework).
* Interpret the json game data configuration appropriately.
* Launch the Starcraft 2 game client process.
* Construct and run the s2clientprotocol to create/join the game.
* Run the main game loop that acquires observations, interprets the game state and issues unit commands.
* Upload results and replay information ( [example <lines ~200-209>](https://github.com/ttinies/sc2gameLobby/blob/master/sc2gameLobby/launcher.py) )
to the ladder server following the end of the match.

**NOTE:** The [sc2gameLobby for non-python](https://github.com/ttinies/sc2gameLobby/blob/master/USAGE_NON_PYTHON.md) may
provide additional, useful information to you how this parameter value will be interpreted.

