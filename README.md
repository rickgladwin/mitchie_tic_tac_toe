# mitchie_tic_tac_toe
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
`settings.loss_weight_delta`, etc. in ```settings.py```
#### Game settings
* to select which AI will be played against and trained, edit the `opponent_name` variable in `main.py@game_loop`
* to create a new AI opponent, add a new option for `opponent_name`. A new database will be created
for this AI automatically.
* to play against the AI manually, set `human_plays_randomly` to `False` in `main.py@game_loop`
* with `human_plays_randomly` set to `True`, you will not be prompted to play. Instead, the system
will choose a valid move for you at random.
* to set how many rounds will be played before the program exits, edit `rounds_to_play` in `main.py@main`. This
is useful for letting the AI learn rapidly.
* to turn verbose console display of game progress on or off, edit `display_this_game` in `main.py@main`.
_NOTE: printing to the console is a major bottleneck in python programs. Set `display_this_game` to `False`
in order to speed up the learning process, and consider commenting out the "rounds remaining: ..." print
command at the end of the game loop._

## Testing

### Unit Tests
#### All tests, verbose
```pytest --verbose```
#### All tests, with console output, verbose
```pytest -s --verbose```
