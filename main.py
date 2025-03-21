import datetime
import random
import time
import emoji
from enum import Enum

from database import create_connection, create_board_states_table, insert_board_state, board_state_from_iterables, \
    forget_all_board_states, create_game_history_table, select_board_state, count_seen_states
from gameplay import choose_next_play, play, player_wins, game_is_drawn, game_is_over, current_valid_plays, \
    winning_play, choose_next_human_play
from interaction import print_board_simple, print_game_thread, clear_screen
from learning import update_db_weights, update_game_history
from settings import settings


class GameResults(str, Enum):
    WIN = 'win',
    LOSS = 'loss',
    DRAW = 'draw',


def main():
    rounds_to_play = 100
    total_rounds = rounds_to_play

    # print the game progress and states to the console?
    # this will show more information, but printing slows the process.
    # if training AI players against each other, it is faster to set this to False.
    # if set to false, the console will display a periodic update on the remaining
    # number of rounds.
    display_this_game = True

    # use an AI or automated strategy in place of the human player?
    # generate_random_plays = True will use a nonhuman player
    # the strategy used by the nonhuman player is determined in the choose_next_play() call
    generate_random_plays = True

    alternate_who_plays_first = True

    start_time = datetime.datetime.now()

    # Determine who plays first in a new set of rounds
    # This value will alternate if alternate_who_plays_first is True and there are
    # multiple rounds
    opponent_1_goes_first = True

    # add a delay of x seconds before the display is refreshed
    # after each play (0 for no delay)
    delay_before_display_refresh: float = 0.2

    while rounds_to_play > 0:
        game_loop(
            display_game=display_this_game,
            rounds_remaining=rounds_to_play,
            automate_player_2=generate_random_plays,
            opponent_1_goes_first=opponent_1_goes_first,
            display_sleep=delay_before_display_refresh
        )
        rounds_to_play -= 1
        if alternate_who_plays_first:
            opponent_1_goes_first = not opponent_1_goes_first

    print('done')
    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time
    print(f'time for {total_rounds} rounds: {elapsed_time}')


def game_loop(display_game=False, rounds_remaining=1, automate_player_2=False, opponent_1_goes_first=True, display_sleep=0.0):
    # To create a new AI player with a blank brain state (no information about game states
    # or successful/unsuccessful plays based on each state), add a new 'opponent_name' value
    # below. The system will automatically create a new SQLite database for any name it doesn't
    # recognize when the game initializes.
    # When training AI players against each other, declare a value for 'opponent_2_name' as well.
    # To reuse existing opponents, uncomment one of the existing 'opponent_name' declarations.
    # initialize opponent
    # opponent_name = 'opponent_1'  # trained against human
    # opponent_name = 'opponent_2'  # trained against (mostly) random
    # opponent_name = 'opponent_3'  # trained against random with "winning play" awareness, with upper weight limit 5000
    # opponent_name = 'opponent_4'  # trained against random with "winning play" awareness, with upper weight limit float('inf')
    # opponent_name = 'opponent_5'  # trained 100 + 30_000 rounds against random with "winning play" awareness, with upper weight limit float('inf')
    # opponent_name = 'opponent_7'  # trained against random with "winning play" awareness, with upper weight limit float('inf')
    # opponent_name = 'opponent_8'  # trained against random with "winning play" awareness, with upper weight limit float('inf')
    # opponent_name = 'opponent_6'  # trained 100 + 30_000 rounds against random with "winning play" awareness, with upper weight limit float('inf')
    # opponent_name = 'opponent_9'  # trained against random with "winning play" awareness, with upper weight limit float('inf')
    # opponent_char = 'X'

    # opponent_name = 'opponent_12'  # trained against fresh opponent AI
    # opponent_char = 'X'

    # initialize opponent 2
    # opponent_2_name = 'opponent_10'  # trained against opponent AI, 11 rounds
    # opponent_2_char = 'O'

    # opponent_2_name = 'opponent_11'  # trained against fresh opponent AI
    # opponent_2_char = 'O'

    # opponent_name = 'opponent_13'  # trained against fresh opponent AI
    # opponent_char = 'X'

    # opponent_2_name = 'opponent_14'  # trained against fresh opponent AI (126_000 games)
    # opponent_2_char = 'O'

    # opponent_name = 'baby_opponent'  # a stupid baby
    # opponent_char = 'X'

    # opponent_name = 'long_opponent_1'  # a stupid baby
    # opponent_char = 'X'
    #
    # opponent_2_name = 'long_opponent_2'  # a stupid baby
    # opponent_2_char = 'O'

    # opponent_name = 'new_opponent_1'  # a stupid baby
    # opponent_char = 'X'

    # opponent_2_name = 'new_opponent_2'  # a stupid baby
    # opponent_2_char = 'O'

    # opponent_2_name = 'another_baby_opponent'  # another dumb baby
    # opponent_2_char = 'O'

    # opponent_name = 'ally_mcbeans'
    # opponent_char = 'X'

    # opponent_2_name = 'cat_blevins'
    # opponent_2_name = 'long_trainer_2'
    opponent_2_name = 'short_trainer_2'
    opponent_2_char = 'O'

    # opponent_name = 'jubal_early'
    # opponent_name = 'long_trainer_1'
    opponent_name = 'short_trainer_1'
    opponent_char = 'X'

    # initialize human
    human_name = 'human'  # you, you friggin champion
    human_char = 'O'

    # reset opponent
    # forget_all_board_states(opponent_name, opponent_char)

    # set up AI databases if they don't exist
    create_board_states_table(opponent_name, opponent_char)
    create_game_history_table(opponent_name, opponent_char)

    if automate_player_2:
        create_board_states_table(opponent_2_name, opponent_2_char)
        create_game_history_table(opponent_2_name, opponent_2_char)

    # initialize game with starting game state
    initial_config: iter = [settings['blank_char']] * 9
    initial_weights: iter = [settings['init_weight']] * 9
    initial_next = []

    # add initial game state to database
    connection = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    insert_board_state(connection, board_state_from_iterables(initial_config, initial_weights, initial_next))

    if automate_player_2:
        connection_2 = create_connection('sqlite/' + opponent_2_name + '_' + opponent_2_char + '.db')
        insert_board_state(connection_2, board_state_from_iterables(initial_config, initial_weights, initial_next))

    # get initial game state
    current_board_config = initial_config

    # initialize game thread (a list of board states and plays)
    game_thread = []

    current_game_is_over = False

    if automate_player_2:
        player_2_name = opponent_2_name
        player_2_char = opponent_2_char
    else:
        player_2_name = human_name
        player_2_char = human_char

    # game loop (each pair of plays)
    while not current_game_is_over:

        # uncomment to throttle the frequency of plays
        # time.sleep(0.75)

        if opponent_1_goes_first:
            player_1_name = opponent_name
            player_1_char = opponent_char

            player_2_name = opponent_2_name
            player_2_char = opponent_2_char
        else:
            # TODO: accommodate human player in this
            player_1_name = opponent_2_name
            player_1_char = opponent_2_char

            player_2_name = opponent_name
            player_2_char = opponent_char

        # opponent plays first
        next_play = choose_next_play(player_1_name, player_1_char, current_board_config)
        new_board_config = play(next_play, player_1_name, player_1_char, current_board_config)

        # register opponent's play in game thread
        game_thread.append((current_board_config, player_1_name, player_1_char, next_play))

        current_board_config = new_board_config

        if display_game:
            time.sleep(display_sleep)
            clear_screen()
            print_board_simple(current_board_config)
            print_game_thread(game_thread)
            print(f'rounds_remaining: {rounds_remaining - 1}')

        # check for win or draw
        if game_is_over(current_board_config):
            current_game_is_over = True
            if display_game:
                checkered_flag = emoji.emojize(':chequered_flag:')
                print(f"{checkered_flag} Game over {checkered_flag}")
            break

        if automate_player_2:
            next_play = choose_next_play(player_2_name, player_2_char, current_board_config)
        else:
            # human plays next
            #  prompt for play position (rather than choose_next_play())
            #  everything else is the same
            valid_plays = current_valid_plays(current_board_config)
            next_play = choose_next_human_play(valid_plays, player_2_name, player_2_char, current_board_config, display_game, automate_player_2)

        new_board_config = play(next_play, player_2_name, player_2_char, current_board_config)
        # update the db with the new board state (after AI and human play) – NOTE: choose_next_play() does this,
        #  and we don't need to train the AI on *ITS* opponent's moves.
        #  Although we could. Maybe as a next version. Let the AI learn what the human did to win.
        game_thread.append((current_board_config, player_2_name, player_2_char, next_play))
        current_board_config = new_board_config

        if display_game:
            time.sleep(display_sleep)
            clear_screen()
            print_board_simple(current_board_config)
            print_game_thread(game_thread)
            print(f'rounds_remaining: {rounds_remaining - 1}')

        # check for a win or draw
        if game_is_over(current_board_config):
            if display_game:
                checkered_flag = emoji.emojize(':chequered_flag:')
                print(f"{checkered_flag} Game over {checkered_flag}")
                # print('@@@ Game over @@@')
            current_game_is_over = True

    winning_char = None

    # check winner, loser, or draw
    if player_wins(current_board_config, player_1_char):
        if display_game:
            print(f'{player_1_char} wins.')
        winning_char = player_1_char
        player_1_game_result = GameResults.WIN.value
        player_2_game_result = GameResults.LOSS.value
    if player_wins(current_board_config, player_2_char):
        if display_game:
            print(f'{player_2_char} wins.')
        winning_char = player_2_char
        player_1_game_result = GameResults.LOSS.value
        player_2_game_result = GameResults.WIN.value
    if game_is_drawn(current_board_config):
        if display_game:
            print('Draw.')
        player_1_game_result = GameResults.DRAW.value
        player_2_game_result = GameResults.DRAW.value

    # update database weights with game results
    update_db_weights(player_1_name, player_1_char, game_thread, winning_char)
    if automate_player_2:
        update_db_weights(player_2_name, player_2_char, game_thread, winning_char)

    # add game to game history
    blank_board_state = select_board_state(player_1_name, player_1_char, '.........')
    _, blank_weights, _ = blank_board_state
    seen_board_states_count = count_seen_states(player_1_name, player_1_char)
    update_game_history(player_1_name, player_1_char, player_1_game_result, blank_weights, seen_board_states_count)

    if automate_player_2:
        blank_board_state_2 = select_board_state(player_2_name, player_2_char, '.........')
        _, blank_weights_2, _ = blank_board_state_2
        seen_board_states_count_2 = count_seen_states(player_2_name, player_2_char)
        update_game_history(player_2_name, player_2_char, player_2_game_result, blank_weights_2, seen_board_states_count_2)

    if rounds_remaining % 256 == 0 and not display_game:
        clear_screen()
        print(f'rounds_remaining: {rounds_remaining} or fewer')

    if not automate_player_2:
        input('Press any key to continue.')

    # end game or start new game
    # TODO: ensure game_thread, board_states update, and learning works for ai playing first
    # TODO: display learning progress, game count, game results, etc.


# def play_ai_round(opponent_name: str, opponent_char: str, current_board_config: iter) -> None:
#     # opponent plays first
#     next_play = choose_next_play(opponent_name, opponent_char, current_board_config)
#     new_board_config = play(next_play, opponent_name, opponent_char, current_board_config)
#
#     # register opponent's play in game thread
#     game_thread.append((current_board_config, opponent_name, opponent_char, next_play))
#
#     current_board_config = new_board_config


if __name__ == "__main__":
    # play a single round
    # game_loop()

    # play until program is quit (calls game_loop() repeatedly)
    main()
