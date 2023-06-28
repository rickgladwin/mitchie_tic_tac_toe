from datetime import datetime

from database import create_connection, config_from_iterable
from settings import settings


def update_db_weights(opponent_name, opponent_char, game_thread, winning_char=None):
    """
    Update weights of playable positions in board_states based on game_thread
    :param str opponent_name: db identifier for opponent
    :param str opponent_char: char used by opponent
    :param list game_thread: list of board_states and plays
    :param str winning_char: char of winning player (default None for a draw)
    :return: None
    """
    if winning_char is None:
        weight_delta = settings['draw_weight_delta']
    elif winning_char == opponent_char:
        weight_delta = settings['win_weight_delta']
    else:
        weight_delta = settings['loss_weight_delta']

    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')

    for game_state in game_thread:
        if game_state[2] == opponent_char:
            target_config = config_from_iterable(game_state[0])
            target_position = game_state[3]
            update_db_board_state(conn, target_config, target_position, weight_delta)

    conn.close()


def update_db_board_state(conn, config, position, weight_delta):
    """
    Update weight of board_state in database
    :param conn: db connection
    :param config: board_state config (primary key)
    :param position: board_state position to update
    :param weight_delta: change to target weight
    :return: None
    """
    target_weights = conn.cursor().execute("SELECT weights FROM board_states WHERE config=?", (config,)).fetchone()[0]
    target_weights = target_weights.split(',')
    target_weights = list(map(int, target_weights))
    if settings['weight_upper_limit'] >= (target_weights[position] + weight_delta) >= settings['weight_lower_limit']:
        target_weights[position] += weight_delta
    target_weights = ','.join(list(map(str, target_weights)))
    conn.cursor().execute("UPDATE board_states SET weights=? WHERE config=?", (target_weights, config,))
    conn.commit()


def update_game_history(opponent_name, opponent_char, opponent_game_result, final_blank_weights) -> None:
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    conn.cursor().execute("INSERT INTO game_history (blank_weights, result, created_at) VALUES ('" + final_blank_weights + "', '" + opponent_game_result + "', '" + str(datetime.now()) + "')")
    conn.commit()
    conn.close()
