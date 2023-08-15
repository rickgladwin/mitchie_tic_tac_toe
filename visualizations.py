import matplotlib.pyplot as plt
import numpy as np
from vpython import *

from database import get_blank_weights, iterable_from_weights, get_blank_weights_from_history, \
    get_seen_states_from_history, select_board_state, select_board_state_from_string
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
        # TODO: update uses of drawn_states to record 3D position
        self.drawn_states: {str: vector} = {}
        self.opponent_name = opponent_name
        self.opponent_char = opponent_char
        self.biggest_weight = 0
        self.dy = 10
        self.horiz_scale = 1
        self.root_radius = 1
        self.branch_radius_ratio = 0.8
        # index 0..9 matches board position
        # tuple (x, z) indicates vector multipliers to use depending on board position
        # e.g.
        # 0 (top left) -> x = -1, z = -1
        # 6 (middle right) -> x = 1, z = 0
        self.position_vector_map: list[tuple] = [
            (-1, -1),
            (0, -1),
            (1, -1),
            (-1, 0),
            (0, 0),
            (1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
        ]
        # set up canvas
        canvas(width=1024, height=500, title='State Tree', caption='caption')

    def draw_state_tree(self, root_state: str, root_position: vector = vector(0, 0, 0), branch_radius: float = None,
                        max_depth=float('inf')) -> None:
        print(f'---- draw_state_tree called with {root_state=}, {root_position=}, {branch_radius=} ----')
        if branch_radius is None:
            branch_radius = self.root_radius
        # (memoize)
        print(f'self.drawn_state_roots: {self.drawn_states}')
        if root_state not in self.drawn_states.keys():
            board_state = select_board_state_from_string(self.opponent_name, self.opponent_char, root_state)
            print(f'### {board_state=}')
            # don't draw a branch for an unseen state
            if board_state is None:
                print(f'### no branch for {root_state}')
                return None

            # FIXME: record each branch's state and position, not just the roots,
            #  so we can use this data for un-branching nodes for common states
            self.drawn_states[root_state] = root_position
            board_config, weights_string, _ = board_state

            print(f'{board_config=}, {weights_string=}')
            print(f'{state_tree.drawn_states=}')
            # find root state in db
            # (memoized) draw vectors from root_position to each position with a nonzero weight
            weights = iterable_from_weights(weights_string)
            self.update_biggest_weight(weights)
            print(f'{self.biggest_weight=}')
            for index, weight in enumerate(weights):
                print(f'{index=} {weight=}')
                if weight > 0:
                    new_x: int = (root_position.x + self.position_vector_map[index][0]) * self.horiz_scale
                    new_y: int = root_position.y + self.dy
                    new_z: int = (root_position.z + self.position_vector_map[index][1]) * self.horiz_scale

                    new_root = vector(new_x, new_y, new_z)
                    # new_root = vector(1,2,3)
                    print(f'{new_root=}')
                    print(f'{new_root.x=}')
                    print(f'{new_root.y=}')
                    print(f'{new_root.z=}')

                    # TODO: use a different function for relative weight, either only taking
                    #  into account the current play number in the game, OR some mix of the
                    #  current play number weights and the absolute biggest weight.
                    relative_weight = max(weight / self.biggest_weight, 0.25)

                    # TODO: find a way to represent branches that represent state transitions that
                    #  don't involve decisions on behalf of the represented player (i.e. the other
                    #  player plays, which creates branches from the current state, but the branches
                    #  don't have a weight since they're not decisions. Maybe use a colour for decision
                    #  branches and grey/translucent for decision-free transitions?
                    new_branch = cylinder(pos=root_position,
                                          axis=new_root,
                                          radius=0.25,
                                          color=color.white,
                                          opacity=relative_weight)
                    root_state_iter_o = list(root_state)
                    root_state_iter_x = list(root_state)
                    # FIXME: It's more complicated than this. Three cases need to be explored (board_states table needs
                    #  to be checked for:
                    #  - equal number of X and O? draw with an X and an O in each position (NOTE: two root branches in
                    #  order to cover cases where X vs O goes first, without overlapping positions in the tree?
                    #  Can this be done from any root state in the tree?
                    #  - more X than O? draw with an O
                    #  - more O than X? draw with an X
                    #  Find a way to alternate the character being added and checked? This will avoid needing to
                    #   compare the count of X and O each time.
                    # root_state_iter[index] = self.opponent_char
                    root_state_iter_o[index] = 'O'
                    branch_end_state_o = ''.join(root_state_iter_o)
                    self.draw_state_tree(root_state=branch_end_state_o, root_position=new_root,
                                         branch_radius=root_position.y * self.branch_radius_ratio)
                    label(pos=new_root, text=branch_end_state_o, xoffset=0.5, yoffset=0.5, box=False, opacity=0)
                # TODO: find an efficient way to determine the biggest weight in the tree after root
                #  and use that to set the opacity etc. for each branch as it's drawn or redrawn
            # (memoized) recursive call from each resulting vector as new root
                    root_state_iter_x[index] = 'X'
                    branch_end_state_x = ''.join(root_state_iter_x)
                    self.draw_state_tree(root_state=branch_end_state_x, root_position=new_root,
                                         branch_radius=root_position.y * self.branch_radius_ratio)
                    # label(pos=new_root, text=branch_end_state_x, xoffset=0.5, yoffset=0.5, box=False, opacity=0)

    def update_biggest_weight(self, weights: iter):
        for weight in weights:
            self.biggest_weight = max(self.biggest_weight, weight)


if __name__ == '__main__':
    # opponent_name = 'opponent_8'
    # test_opponent_name = 'opponent_13'
    # test_opponent_char = 'X'

    test_opponent_name = 'new_opponent_1'
    test_opponent_char = 'X'

    test_config = '.........'
    test_expected_weights = '0,11,16,7,0,0,0,14,29'

    state_tree = StateTree(test_opponent_name, test_opponent_char)
    state_tree.draw_state_tree(test_config)

    print(f'&&& done. &&&')

    while True:
        rate(60)

    # draw_blank_weights_over_time(test_opponent_name, test_opponent_char)

    # draw_seen_states_count_over_time(test_opponent_name, test_opponent_char)
