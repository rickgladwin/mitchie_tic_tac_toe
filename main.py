import sys

from database import create_connection, create_board_states_table, insert_board_state

null_board = ['.' for i in range(0, 10)]
example_board_config = ['.', '.', 'X', '.', 'O', 'X', '.', 'O', '.']
example_board_weights = [24, 2, 0, 8, 0, 0, 8, 0, 16]


def main():
    print('starting...')
    print('starting with an untrained opponent...')

    # initialize opponent
    opponent_name = 'opponent_1'
    create_board_states_table(opponent_name)

    # initialize game with starting game state
    initial_config = ['.'] * 9
    initial_weights = [10] * 9
    initial_next = []

    # add initial game state to database
    initial_board_state = (initial_config, initial_weights, initial_next)
    connection = create_connection('sqlite/' + opponent_name + '.db')
    insert_board_state(connection, initial_board_state)


if __name__ == "__main__":
    # print('example board:')
    # print_board_simple(example_board_config)
    main()
