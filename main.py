from database import create_connection, create_board_states_table, insert_board_state, board_state_from_iterables, \
    forget_all_board_states
from gameplay import choose_next_play, play, player_wins, game_is_drawn, game_is_over
from interaction import print_board_simple, print_game_thread
from settings import settings


def main():
    print('starting...')
    print('starting with an untrained opponent...')

    # initialize opponent
    opponent_name = 'opponent_1'
    opponent_char = 'X'
    human_char = 'O'
    valid_plays = ['1', '2', '3', '4', '5', '6', '7', '8', '9']

    # reset opponent
    # forget_all_board_states(opponent_name, opponent_char)

    create_board_states_table(opponent_name, opponent_char)

    # initialize game with starting game state
    initial_config = [settings['blank_char']] * 9
    initial_weights = [settings['init_weight']] * 9
    initial_next = []

    # add initial game state to database
    connection = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    insert_board_state(connection, board_state_from_iterables(initial_config, initial_weights, initial_next))

    # get initial game state
    current_board_config = initial_config
    print(f'current (starting) board state:')
    print_board_simple(current_board_config)

    # initialize game thread (a list of board states and plays)
    game_thread = []

    print_game_thread(game_thread)

    # TODO: game loop is AI then human (or vice versa), with db and game state updates, until there's a win or draw
    #  (or until the human quits)
    #  then update the weights based on the outcome and the game thread
    #  then start a new game

    current_game_is_over = False

    while not current_game_is_over:
        # opponent plays first
        next_play = choose_next_play(opponent_name, opponent_char, current_board_config)
        new_board_config = play(next_play, opponent_name, opponent_char, current_board_config)

        # register opponent's play in game thread
        game_thread.append((current_board_config, opponent_name, opponent_char, next_play))
        print(f'game thread: {game_thread}')
        print(f'current board state:')
        print_board_simple(new_board_config)

        current_board_config = new_board_config

        # check for win or draw
        if game_is_over(current_board_config):
            current_game_is_over = True
            print('@@@ Game over @@@')
            break

        # human plays next
        #  prompt for play position (rather than choose_next_play())
        #  everything else is the same
        input_is_valid = False
        while not input_is_valid:
            print('Your turn. Enter a number from 1 to 9 to indicate your play position. Q to quit')
            player_input = input()
            if player_input == 'Q' or player_input == 'q':
                print('Thanks for playing!')
                return
            # TODO: update valid_plays, removing plays that have already been made
            if player_input not in valid_plays:
                print('Invalid input.')
                continue
            # player input is 1-indexed, but the board config is 0-indexed
            next_play = int(player_input) - 1
            input_is_valid = True

        new_board_config = play(next_play, opponent_name, human_char, current_board_config)
        # update the db with the new board state (after AI and human play) – NOTE: choose_next_play() does this,
        #  and we don't need to train the AI on *ITS* opponent's moves.
        #  Although we could. Maybe as a next version. Let the AI learn what the human did to win.
        game_thread.append((current_board_config, opponent_name, human_char, next_play))
        current_board_config = new_board_config

        print(f'game thread: {game_thread}')
        print_board_simple(current_board_config)

        # check for a win or draw
        if game_is_over(current_board_config):
            print('@@@ Game over @@@')
            current_game_is_over = True

    # check winner, loser, or draw
    if player_wins(current_board_config, opponent_char):
        print('You lose.')
    if player_wins(current_board_config, human_char):
        print('You win!')
    if game_is_drawn(current_board_config):
        print('Draw.')
    # update database weights with game results
    # TODO: update weights based on game results
    # TODO: update game thread after final play
    # TODO: update database after final play

    # end game or start new game


if __name__ == "__main__":
    # print('example board:')
    # print_board_simple(example_board_config)
    main()
