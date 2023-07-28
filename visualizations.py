import matplotlib.pyplot as plt
import numpy as np
from vpython import *

from database import get_blank_weights, iterable_from_weights, get_blank_weights_from_history, \
    get_seen_states_from_history, select_board_state
from settings import settings


def draw_blank_weights_over_time(opponent_name, opponent_char) -> None:
    blank_weights_history = get_blank_weights_from_history(opponent_name, opponent_char)
    # add the initial (pre games) weights
    default_weights = [settings['init_weight'] for i in range(9)]
    blank_weights_history.insert(0, default_weights)

    x = range(0, len(blank_weights_history))
    y = weight_sums_from_history(blank_weights_history)

    fig, ax = plt.subplots()
    ax.set_title(f'{opponent_name}_{opponent_char} learning progress (proxy)')
    ax.set_xlabel('game number')
    ax.set_ylabel('blank state weights sum')
    ax.plot(x, y)

    # draw line of best fit for last N points
    latest_range = 100
    x_best = np.array(list(x)[-latest_range:])
    y_best = np.array(y[-latest_range:])
    a, b = np.polyfit(x=x_best, y=y_best, deg=1)
    print(f'last x_best: {x_best[-10:]}')
    print(f'last y_best: {y_best[-10:]}')
    print(f'a,b: {a}, {b}')
    plt.plot(x, a * x + b, label=f'slope of last {latest_range} points: {round(a, 2)}')
    plt.legend()

    plt.show()


def weight_sums_from_history(blank_weights: list[iter]) -> list[int]:
    weight_sums = []
    for i in range(0, len(blank_weights)):
        weight_sums.append(sum(blank_weights[i]))
    return weight_sums


def draw_seen_states_count_over_time(opponent_name, opponent_char) -> None:
    seen_states_history = get_seen_states_from_history(opponent_name, opponent_char)
    # add the initial (pre games) weights

    x = np.array(range(0, len(seen_states_history)))
    y = np.array(seen_states_history)

    fig, ax = plt.subplots()
    ax.set_title(f'{opponent_name}_{opponent_char} seen board states')
    ax.set_xlabel('game number')
    ax.set_ylabel('seen board states')
    ax.plot(x, y)

    plt.show()


# example game_thread:
# (['.', '.', '.', '.', '.', '.', '.', '.', '.'], 'opponent_13', 'X', 4)
# (['.', '.', '.', '.', 'X', '.', '.', '.', '.'], 'human', 'O', 0)
# (['O', '.', '.', '.', 'X', '.', '.', '.', '.'], 'opponent_13', 'X', 2)
# (['O', '.', 'X', '.', 'X', '.', '.', '.', '.'], 'human', 'O', 6)
# (['O', '.', 'X', '.', 'X', '.', 'O', '.', '.'], 'opponent_13', 'X', 3)
# (['O', '.', 'X', 'X', 'X', '.', 'O', '.', '.'], 'human', 'O', 5)
# (['O', '.', 'X', 'X', 'X', 'O', 'O', '.', '.'], 'opponent_13', 'X', 7)
# (['O', '.', 'X', 'X', 'X', 'O', 'O', 'X', '.'], 'human', 'O', 1)
# (['O', 'O', 'X', 'X', 'X', 'O', 'O', 'X', '.'], 'opponent_13', 'X', 8)

# game state visualization:
## method 1: draw state space from board_states table - trace vectors forward, starting from blank state (pro: no redundant data, con: slow)
## method 2: draw state space one play at a time during gameplay - trace vectors at runtime (con: would have to reconstruct games from board_states table in order to build full tree outside of gametime)
## method 3: add "from states" to board_states table and record during method 1 or 2 (pro: preprocesses visualization data, con: redundant information in db)
# TODO: implement method 1, then method 3 if it makes sense (method 2 is less useful, and a subfeature of 1)
# TODO: find a way to add a vector after every play, then update vector weights from the game history at the end of each round.
# NOTE: Bonus feature: feed the tree drawing function a root state (not necessarily the blank state) so that the subtree can be
#  can be drawn from there.

class StateTree:
    def __init__(self, opponent_name: str, opponent_char: str):
        self.drawn_state_roots: [str] = []
        self.opponent_name = opponent_name
        self.opponent_char = opponent_char

    def draw_state_tree(self, root_state: str, root_position: vector = vector(0,0,0), max_depth = float('inf')) -> None:
        pass
        # (memoize)
        if root_state not in self.drawn_state_roots:
            self.drawn_state_roots.append(root_state)
            board_state = select_board_state(self.opponent_name, self.opponent_char, )
        # find root state in db
        # (memoized) draw vectors from root_position to each position with a nonzero weight
        # (memoized) recursive call from each resulting vector as new root





if __name__ == '__main__':
    # opponent_name = 'opponent_8'
    # test_opponent_name = 'opponent_13'
    # test_opponent_char = 'X'

    test_opponent_name = 'new_opponent_2'
    test_opponent_char = 'O'

    draw_blank_weights_over_time(test_opponent_name, test_opponent_char)

    draw_seen_states_count_over_time(test_opponent_name, test_opponent_char)
