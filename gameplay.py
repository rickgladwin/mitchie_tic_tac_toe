from database import create_connection, select_board_state, insert_fresh_board_state
from selections import select_move


def iterable_from_config(config):
    return list(map(int, config))


def iterable_from_weights(weights):
    return list(map(int, weights.split(',')))


def choose_next_play(opponent_name, opponent_char, current_board_config):
    # look up current board state in database
    # opponent_conn = create_connection('sqlite/' + opponent_name + '.db')
    current_board_state = select_board_state(opponent_name, opponent_char, current_board_config)

    # if it's not there, add it and initialize its weights
    if not current_board_state:
        insert_fresh_board_state(opponent_name, opponent_char, current_board_config)
        current_board_state = select_board_state(opponent_name, opponent_char, current_board_config)

    config, weights, nexts = current_board_state

    # select a next play based on the weights
    print(f'%% current board state: {current_board_state}')
    play_selection = select_move(iterable_from_weights(weights))
    print(f'%% play selection: {play_selection}')
    # return the next play (the index where the opponent will play)
    return play_selection


def play(placement, opponent_name, opponent_char, current_board_state):
    print(f'@@@ playing at {placement} character {opponent_char} @@@')
    pass
