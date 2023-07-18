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

![Antique robots playing a board game](assets/antique_game_players_1.jpg)

_"I belong in a museum, not playing against this idiot."_

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
* determine the way the game will run (waiting for human player input, running/training
against an automated algorithm, number of rounds, etc. – See Settings below) by updating
the relevant parts of `main.py`
* From the root of the repo, run
  ```python main.py```
### Review results
With a SQLite client, open the database file matching the name of the relevant opponent and their
player character ('X' or 'O')

Each record in the database represents a possible board state, including all states that the AI has experienced.

The records in the database may not represent all possible board states, as some board states closer to
the possibility space for losing games may never be encountered by the AI given a finite training run.
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
will choose a valid move for you, either at random, using a function that finds and completes two in a row,
or using another AI running a learning algorithm.
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
* How an AI is trained, and the progression of that training, matters very much with respect to
the final behaviour of the AI!
* An AI trained against a random player seems more difficult to beat than an untrained AI, but
still fees very beatable. It fails to prioritize blocking the human player's win, expecting a random
play and still giving some priority to plays that have led to its own victories.
  * I added a `winning_play()` function to the `gameplay` module, so that once a board state
  exists that would result in a win for the human player, the "generate random" player will
  play there. This will hopefully change the AI's prioritization to block imminent human wins.
  * Before adding `winning_play()` to the random opponent's game loop, the AI trained against a random
  player was more likely to make its first play in a corner, and unlikely to play in the middle of
  a side or in the centre position. After adding `winning_play()`, the AI is more likely to play in
  the centre position. Tic-tac-toe being a solved game which can always be played to a win or draw, the
  first play in the centre matches the optimal strategy for the first player.
  * After adding `winning_play()`, the AI feels much more difficult to beat.
* Setting a finite maximum weight for the plays results in a set of weights for the initial
play that favours any play that isn't strictly detrimental, rather than favouring the centre.
  * Setting the maximum weight to `float('inf')` results in the centre position being favoured continuously (though
we should be careful to account for the maximum float value for the hardware or language)
* Setting a minimum weight of 1 for the plays means there is still some small chance of the AI
playing in a suboptimal position, and so some randomness remains in the game. Setting a minimum
weight of 0 will result in those moves being eliminated from the possible plays after losing
<initial weight> games that included that play.
* Training the AI against a purely random opponent resulted in a database that included over 2400
configs after a high number of training rounds, whereas training it against a random opponent
that prioritized completing a 2-in-a-row for the win resulted in a database with over 1900. 
  * This has interesting implications for the relationship between "well-trained" AIs and AIs trained using
a faulty method: a "better trained" AI doesn't necessarily have a larger or more complex brain state.
  * The caveat here is that, in the case of this repo, the "better trained" AI will simply see
fewer possible board states, since games will end earlier in general. But this kind of effect
may still show up in other examples of AI and machine learning, especially once we consider the
complexity of convolutional neural networks, ANNs with hidden layers and exotic architectures,
and other more complex models – the complexity may be overkill in some situations, e.g. in
CNNs that are overtrained with too many hidden layers.

## Next Steps:
- <span style="color: lightgreen;">✓</span> create visualizations for the state of the AI's training over time
- create visualizations for the gameplay itself (currently outputs to the console)
- <span style="color: lightgreen">✓</span> create visualizations for the training and visited board states 
- <span style="color: cyan;">⧖</span> create visualizations for the trained model itself – a tree in 3D space with
nodes to represent unique board states and color/opacity for weights
- <span style="color: lightgreen;">✓</span> make two AIs play against each other, and see how their strategies evolve
- <span style="color: cyan;">⧖</span> study the ways in which the asymmetries in the weights on the blank config emerge under
different training conditions, algorithms, and methods
- create a neural network with board position statuses as inputs, see if there's an ANN architecture that
will result in a successful AI
- explore generating a decision tree model from the tic-tac-toe AI's training and game history. Explore ways
to generalize this process for generating decision tree models with human-readable labels and
visualizations.

## Assets
assets/antique_game_players_1.jpg

Imagine V4 Prompt: _an antique robot made of brass and copper sits at a small games table. 
On the table is a tic tac toe game. The robot is looking at the game. Across from the robot 
is a small human child. The child is waiting for the robot to play._ 
