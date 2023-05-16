def update_db_weights(opponent_name, opponent_char, game_thread):
    """
    Update weights of playable positions in board_states based on game_thread
    :param opponent_name: db identifier for opponent
    :param opponent_char: char used by opponent
    :param game_thread: list of board_states and plays
    :return: None
    """
    # TODO: get winner/loser/draw from last board_state in game_thread
    # TODO: update weights of board_states in game_thread based on winner/loser/draw using
    #   each each game_thread element
    # TODO: create an update function that takes a weight delta based on settings and win/loss/draw


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
    target_weights[position] += weight_delta
    target_weights = ','.join(list(map(str, target_weights)))
    conn.cursor().execute("UPDATE board_states SET weights=? WHERE config=?", (target_weights, config,))
    conn.commit()
