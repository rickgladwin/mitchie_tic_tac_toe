from database import create_connection, select_board_state, insert_fresh_board_state
from selections import select_move
from settings import settings


def iterable_from_config(config):
    return list(map(int, config))


def iterable_from_weights(weights):
    return list(map(int, weights.split(',')))


# TODO: make an equivalent function for human player, where move choice is provided rather than selected,
#  and/or extract the check and update to the board_states table.
# TODO: ensure current_board_config is updated before choosing the play (ensure that the weight for any played
#  position is updated to 0)
def choose_next_play(opponent_name, opponent_char, current_board_config):
    # look up current board state in database
    # opponent_conn = create_connection('sqlite/' + opponent_name + '.db')
    current_board_state = select_board_state(opponent_name, opponent_char, current_board_config)

    # if it's not there, add it and initialize its weights
    if not current_board_state:
        print(f'%% no board state found for {current_board_config}. Inserting...')
        insert_fresh_board_state(opponent_name, opponent_char, current_board_config)
        current_board_state = select_board_state(opponent_name, opponent_char, current_board_config)

    config, weights, nexts = current_board_state

    # select a next play based on the weights
    print(f'%% choosing play based on current board state: {current_board_state}')
    play_selection = select_move(iterable_from_weights(weights))
    print(f'%% play selection: {play_selection + 1}')
    # return the next play (the index where the opponent will play)
    return play_selection


def play(placement, opponent_name, opponent_char, current_board_state):
    """Add a new play to the game
    :param int placement: index of the play
    :param str opponent_name: db identifier for opponent
    :param str opponent_char: char used by opponent
    :param current_board_state: iterable board position statuses"""
    print(f'@@@ playing at {placement + 1} character {opponent_char} @@@')
    new_board_state = list(current_board_state)
    # plays are 1-indexed, but board config is 0-indexed
    new_board_state[placement] = opponent_char
    return new_board_state


def game_is_over(current_board_state):
    """Check if the game is over
    :param current_board_state: iterable board position statuses"""
    # game is over if:
    # - X wins
    # - O wins
    # - board is full
    # There are 8 possible winning configurations for each character
    # (3 rows, 3 columns, 2 diagonals)
    if player_wins(current_board_state, 'X'):
        return True
    if player_wins(current_board_state, 'O'):
        return True
    if board_is_full(current_board_state):
        return True

    return False


def player_wins(current_board_state, player_char):
    """Check if the player wins
    :param current_board_state: iterable board position statuses
    :param str player_char: char used by player
    :returns: bool"""
    # There are 8 possible winning configurations for each character
    # (3 rows, 3 columns, 2 diagonals)
    if current_board_state[0] == current_board_state[1] == current_board_state[2] == player_char:
        return True
    if current_board_state[3] == current_board_state[4] == current_board_state[5] == player_char:
        return True
    if current_board_state[6] == current_board_state[7] == current_board_state[8] == player_char:
        return True
    if current_board_state[0] == current_board_state[3] == current_board_state[6] == player_char:
        return True
    if current_board_state[1] == current_board_state[4] == current_board_state[7] == player_char:
        return True
    if current_board_state[2] == current_board_state[5] == current_board_state[8] == player_char:
        return True
    if current_board_state[0] == current_board_state[4] == current_board_state[8] == player_char:
        return True
    if current_board_state[2] == current_board_state[4] == current_board_state[6] == player_char:
        return True
    return False


def board_is_full(current_board_state):
    """Check if the board is full
    :param current_board_state: iterable board position statuses
    :returns: bool"""
    played_positions = [position for position in current_board_state if position != settings['blank_char']]
    return len(played_positions) == 9


def game_is_drawn(current_board_state):
    """Check if the game is drawn
    :param current_board_state: iterable board position statuses
    :returns: bool"""
    return board_is_full(current_board_state) and not player_wins(current_board_state, 'X') and not player_wins(
        current_board_state, 'O')


def current_valid_plays(current_board_state):
    """Return a list of valid plays
    :param current_board_state: iterable board position statuses
    :returns: list"""
    return [index for index, position in enumerate(current_board_state) if position == settings['blank_char']]


# TODO: consider making a game state or gameplay state function?
#  This would return "X wins", "Y wins", "draw", or "in progress"
#  (matching a game state enum) and could be checked in the main loop.
#  It's a pure function since it only checks state.
