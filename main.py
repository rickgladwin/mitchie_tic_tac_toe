import sys

from database import create_connection, create_game_states_table

null_board = [None for i in range(0, 10)]
example_board_config = [None, None, 'X', None, 'O', 'X', None, 'O', None]
example_board_weights = [24, 2, 0, 8, 0, 0, 8, 0, 16]


def main():
    print('starting...')
    print('starting with an untrained opponent...')

    # initialize opponent
    opponent_name = 'opponent_1'
    create_game_states_table(opponent_name)

    # initialize game with starting game state
    initial_config = ['.'] * 9
    initial_weights = [10] * 9
    initial_next = []

    # add initial game state to database





if __name__ == "__main__":
    # print('example board:')
    # print_board_simple(example_board_config)
    main()
