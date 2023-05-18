# mitchie_tic_tac_toe
![tests: 100% passing](https://img.shields.io/badge/tests-100%25%20passing-green)

A python implementation of Mitchie's Tic Tac Toe MENACE machine learning system

## Background
### Mitchie's MENACE
Donald Mitchie, a contemporary of Alan Turing, Max Newman and Jack Good, was working on artificial 
intelligence and machine learning starting in the late 1950s. At that time, it was not efficient to
implement a machine learning algorithm on a computer, so he developed a system that used matchboxes.

The system, created in 1961, was called **MENACE**, which stood for **Machine Educable Noughts And Crosses Engine**.

MENACE demonstrated that a computer could learn to improve its performance in carrying out a task, given
reinforcement and feedback.

https://en.wikipedia.org/wiki/Matchbox_Educable_Noughts_and_Crosses_Engine

### This repo
This repo is a python implementation of the algorithm and principles employed in MENACE, exploring methods for
storing the state of an AI's training in a persistence layer (a sqlite database, as of this writing),
efficient methods for making decisions based on the training, and methods for training the AI based on
game outcomes.

Internally, the game board is represented as a string or list of 9 characters, indexed as follows:

```
012
345
678
```
For usability, a human player is shown a 1-indexed board, rather than the 0-indexed board used internally.

For example, the following board:
```
XO.
.O.
..X
```
is represented internally as `XO..O...X` and represents a unique state of the game, and a unique
identifier in the database.

## Installation

### Prerequisites
* Python 3 (>= 3.11 recommended)
* conda (optional but recommended)

### Install
* clone this repo
* create a conda environment
```conda create --name ai_ml -f environment.yml```

## Usage
### Run the game
* activate the environment
  ```conda activate ai_ml```
* From the root of the repo, run
  ```python main.py```
### Review results
With a SQLite client, open the database file matching the name of the relevant opponent and their
player character ('X' or 'O')

Each record in the database represents a possible board state, including 
### Settings
#### System and learning settings
* change how the system learns by editing `settings.win_weight_delta`, 
`settings.loss_weight_delta`, etc. in ```settings.py```. _HINT: with `settings.weight_upper_limit` set,
all initial plays (from a blank board) will eventually have weights matching that maximum value, though
they will arrive at that value at different rates. Setting this upper limit to a lower value will result
in more of the possibility space of the board being explored earlier in the learning process. Setting
the value higher will allow the weights of that initial play to reflect relative real world outcomes
for longer._
#### Game settings
* to select which AI will be played against and trained, edit the `opponent_name` variable in `main.py@game_loop`
* to create a new AI opponent, add a new option for `opponent_name`. A new database will be created
for this AI automatically.
* to play against the AI manually, set `generate_random_plays` to `False` in `main.py@main`
* with `generate_random_plays` set to `True`, you will not be prompted to play. Instead, the system
will choose a valid move for you at random.
* to set how many rounds will be played before the program exits, edit `rounds_to_play` in `main.py@main`. This
is useful for letting the AI learn rapidly.
* to turn verbose console display of game progress on or off, edit `display_this_game` in `main.py@main`.
_NOTE: printing to the console is a major bottleneck in python programs. Set `display_this_game` to `False`
in order to speed up the learning process, and consider commenting out the "rounds remaining: ..." print
command at the end of the game loop._

## Testing
_NOTE: as of 2023-05-17, only unit-scoped tests are implemented, and they are not comprehensive. The purpose
of this repo, as of now, is to explore the algorithm and its implementation. Additionally, end-to-end
requirements are in flux, and it's not efficient to generate full test coverage for any spec that is
unstable._

_That said, PRs for additional tests are welcome!_

### Unit Tests
#### All tests, verbose
```pytest --verbose```
#### All tests, with console output, verbose
```pytest -s --verbose```

## Insights
* An AI trained against a random player seems more difficult to beat than an untrained AI, but
still fees very beatable. It fails to prioritize blocking the human player's win, expecting a random
play and still giving some priority to plays that have led to its own victories.
  * I'm adding a `winning_play()` function to the `gameplay` module, so that once a board state
  exists that would result in a win for the human player, the "generate random" player will
  play there. This will hopefully change the AI's prioritization to block imminent human wins.
