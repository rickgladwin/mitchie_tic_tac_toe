import random
from database import create_connection, create_board_states_table, insert_board_state, board_state_from_iterables, \
    forget_all_board_states
from gameplay import choose_next_play, play, player_wins, game_is_drawn, game_is_over, current_valid_plays, winning_play
from interaction import print_board_simple, print_game_thread, clear_screen
from learning import update_db_weights
from settings import settings


def main():
    rounds_to_play = 100000

    # print the game progress and states to the console?
    display_this_game = True

    # generate random plays for the human player?
    generate_random_plays = False

    while rounds_to_play > 0:
        game_loop(
            display_game=display_this_game,
            rounds_remaining=rounds_to_play,
            human_plays_randomly=generate_random_plays
        )
        rounds_to_play -= 1

    print('done')


def game_loop(display_game=False, rounds_remaining=1, human_plays_randomly=False):
    # print('starting new game...')

    # initialize opponent
    # opponent_name = 'opponent_1'  # trained against human
    # opponent_name = 'opponent_2'  # trained against (mostly) random
    # opponent_name = 'opponent_3'  # trained against random with "winning play" awareness, with upper weight limit 5000
    opponent_name = 'opponent_4'  # trained against random with "winning play" awareness, with upper weight limit float('inf')
    opponent_char = 'X'

    # initialize human
    human_char = 'O'

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
    # print(f'current (starting) board state:')
    # print_board_simple(current_board_config)

    # initialize game thread (a list of board states and plays)
    game_thread = []

    # clear_screen()
    # print_board_simple(current_board_config)
    # print_game_thread(game_thread)

    current_game_is_over = False

    while not current_game_is_over:
        # opponent plays first
        next_play = choose_next_play(opponent_name, opponent_char, current_board_config)
        new_board_config = play(next_play, opponent_name, opponent_char, current_board_config)

        # register opponent's play in game thread
        game_thread.append((current_board_config, opponent_name, opponent_char, next_play))

        current_board_config = new_board_config

        if display_game:
            clear_screen()
            print_board_simple(current_board_config)
            print_game_thread(game_thread)
            print(f'rounds_remaining: {rounds_remaining - 1}')

        # check for win or draw
        if game_is_over(current_board_config):
            current_game_is_over = True
            if display_game:
                print('@@@ Game over @@@')
            break

        # human plays next
        #  prompt for play position (rather than choose_next_play())
        #  everything else is the same
        valid_plays = current_valid_plays(current_board_config)
        input_is_valid = False
        while not input_is_valid:
            if display_game:
                print('Your turn. Enter a number from 1 to 9 to indicate your play position. Q to quit')
                print(f'Valid plays: {valid_plays}')
            if human_plays_randomly:
                play_for_win = winning_play(current_board_config, human_char)
                if play_for_win is not None:
                    player_input = play_for_win
                else:
                    player_input = valid_plays[random.randint(0, len(valid_plays) - 1)]
            else:
                player_input = input()
            if player_input == 'Q' or player_input == 'q':
                print('Thanks for playing!')
                return
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

        if display_game:
            clear_screen()
            print_board_simple(current_board_config)
            print_game_thread(game_thread)
            print(f'rounds_remaining: {rounds_remaining - 1}')

        # check for a win or draw
        if game_is_over(current_board_config):
            if display_game:
                print('@@@ Game over @@@')
            current_game_is_over = True

    winning_char = None

    # check winner, loser, or draw
    if player_wins(current_board_config, opponent_char):
        if display_game:
            print('You lose.')
        winning_char = opponent_char
    if player_wins(current_board_config, human_char):
        if display_game:
            print('You win!')
        winning_char = human_char
    if game_is_drawn(current_board_config):
        if display_game:
            print('Draw.')

    # update database weights with game results
    update_db_weights(opponent_name, opponent_char, game_thread, winning_char)

    if not display_game:
        clear_screen()
        print(f'rounds_remaining: {rounds_remaining - 1}')

    if not human_plays_randomly:
        input('Press any key to continue.')

    # end game or start new game
    # TODO: allow for ai to play first
    # TODO: ensure game_thread, board_states update, and learning works for ai playing first
    # TODO: display learning progress, game count, game results, etc.


if __name__ == "__main__":
    # play a single round
    # game_loop()

    # play until program is quit (calls game_loop() repeatedly)
    main()
