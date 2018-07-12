
# Define human or AI players to compete in Starcraft 2 matches

### Purpose

Various Starcraft 2 processes rely on understanding players and differentiating this.  This package provides capability to
define them such that matches can be started, identify the player(s) within the match and act as a key for performance
across matches.

# Usage

### Installation

On a command line, perform the intended query or operation.  All queries are performed on the user's local machine.
(To query remote player definitions, use the [sc2gameLobby](https://github.com/ttinies/sc2gameLobby).

> EXAMPLE: `python sc2players <options>`

To view the complete and up-to-date options and how to use them, review the --help documentation.

> EXAMPLE: `python sc2players --help`

### Command line operation

For general use, the intent is to utilize this package's interface.  Unless incorporated into external python code, the
command-line interface is the primary means to acquire player information.  After specifying the command to invoke this
package, the remaining parameters specify the operation to be performed and any parameters for that operation.  (NOTE:
specifying no arguments after the package name simply displays all known players.)

> EXAMPLE: `python -m sc2players <operation> <parameters>`

### Create your own human player



### Create your own AI bot definition


