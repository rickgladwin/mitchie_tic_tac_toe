from database import create_connection, create_board_states_table, insert_board_state, board_state_from_iterables, \
    forget_all_board_states
from gameplay import choose_next_play, play
from interaction import print_board_simple
from settings import settings


def main():
    print('starting...')
    print('starting with an untrained opponent...')

    # initialize opponent
    opponent_name = 'opponent_1'
    opponent_char = 'X'

    # reset opponent
    # forget_all_board_states(opponent_name, opponent_char)

    create_board_states_table(opponent_name, opponent_char)

    # initialize game with starting game state
    initial_config = ['.'] * 9
    initial_weights = [settings['init_weight']] * 9
    initial_next = []

    # add initial game state to database
    initial_board_state = (initial_config, initial_weights, initial_next)
    connection = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    insert_board_state(connection, board_state_from_iterables(initial_config, initial_weights, initial_next))

    # get initial game state
    current_board_state = initial_config
    print(f'current board state:')
    print_board_simple(current_board_state)

    # initialize game thread (a list of board states and plays)
    game_thread = []

    current_play = (current_board_state, opponent_name, opponent_char)
    game_thread.append(current_play)

    # opponent plays first
    next_play = choose_next_play(opponent_name, opponent_char, current_board_state)
    new_board_state = play(next_play, opponent_name, opponent_char, current_board_state)

    # register opponent's play in game thread

    # get next board state based on play (create the db record if it doesn't exist)
    # other player goes
    # loop until game is over
    # update weights based on game outcome and game thread



if __name__ == "__main__":
    # print('example board:')
    # print_board_simple(example_board_config)
    main()
