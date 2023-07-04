import sqlite3

from settings import settings


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print(sqlite3.version)
    except sqlite3.Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def board_state_from_iterables(config, weights, nexts):
    """
    Create a board_state from iterable objects
    :param config: iterable board position statuses
    :param weights: iterable board position probability weights
    :param nexts: iterable next possible board states
    :return: board_state
    """

    config_string = config_from_iterable(config)
    weights_string = weights_from_iterable(weights)
    nexts_string = nexts_from_iterable(nexts)

    board_state = (config_string, weights_string, nexts_string)

    return board_state


def insert_board_state(conn, board_state):
    """
    Add a new board_state to the board_states table
    :param conn: connection object
    :param board_state: tuple of (config, weights, nexts)
    """
    config, weights, nexts = board_state
    sql = ''' INSERT INTO board_states(config,weights,nexts)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, board_state)
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            # print(f'board_state exists: {board_state}')
            pass
        else:
            print(e)
            print(f'board_state: {board_state}')
    except sqlite3.InterfaceError as e:
        print(e)
        print('Did you remember to convert the iterables to strings?')
    conn.commit()


def insert_fresh_board_state(opponent_name, opponent_char, config):
    """
    Add a new board_state to the board_states table with default weights and nexts
    :param opponent_name: db identifier for opponent
    :param opponent_char: char used by opponent
    :param config: iterable board position statuses
    """
    config_string = config_from_iterable(config)
    state_weights = list(map(lambda x: 0 if x != settings['blank_char'] else settings['init_weight'], config))

    # print(f'state_weights: {state_weights}')
    initial_weights = weights_from_iterable(state_weights)
    initial_next = nexts_from_iterable([])
    board_state = (config_string, state_weights, initial_next)

    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    insert_board_state(conn, board_state)


def config_from_iterable(config):
    config_string = ''.join(list(map(str, config)))
    return config_string


def weights_from_iterable(weights):
    weights_string = ','.join(list(map(str, weights)))
    return weights_string


def iterable_from_weights(weights: str):
    iterable = [int(x) for x in weights.split(',')]
    return iterable


def nexts_from_iterable(nexts):
    nexts_string = ','.join(list(map(str, nexts)))
    return nexts_string


def select_board_state(opponent_name, opponent_char, config):
    """
    Query board_states table for a board_state with a given config
    :param opponent_name: db identifier for opponent
    :param opponent_char: char used by opponent
    :param config: string of board position statuses
    :return: board_state
    """
    config_string = config_from_iterable(config)

    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')

    cur = conn.cursor()
    cur.execute("SELECT * FROM board_states WHERE config=?", (config_string,))

    board_state = cur.fetchone()

    if not board_state:
        state_weights = list(map(lambda x: 0 if x != settings['blank_char'] else settings['init_weight'], config))
        # initial_weights = weights_from_iterable([10] * 9)
        state_weights = weights_from_iterable(state_weights)
        initial_next = nexts_from_iterable([])
        board_state = (config_string, state_weights, initial_next)

        insert_board_state(conn, board_state)

    conn.close()

    return board_state


create_board_states_table_sql = """
CREATE TABLE IF NOT EXISTS board_states (
    config blob UNIQUE PRIMARY KEY, -- status of each space on the board, X, O, or None 
    weights blob, -- probability weighting for each space on the board
    nexts blob -- list of ids for possible states one play after this one
);
"""


create_game_history_table_sql = """
CREATE TABLE IF NOT EXISTS game_history (
    game_number INTEGER PRIMARY KEY, 
    blank_weights blob, -- value of 'weights' column for '.........' config
    seen_states_count int, -- number of board states seen at this point in history
    result text, -- 'win', 'loss', 'draw' for this player
    created_at timestamp 
);
"""


def get_blank_weights(opponent_name, opponent_char) -> str:
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    weights = conn.execute("SELECT weights FROM board_states WHERE config like '.........'").fetchone()[0]
    print(f'weights: {weights}')
    conn.close()
    return weights


def get_last_blank_weights(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    weights = conn.execute("SELECT blank_weights FROM game_history ORDER BY game_number DESC LIMIT 1").fetchone()[0]
    print(f'most recent weights: {weights}')
    conn.close()
    return weights


def get_blank_weights_from_history(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    weights = conn.execute("SELECT blank_weights FROM game_history").fetchall()
    conn.close()
    # convert weights strings to iterables
    weights_iterables = []
    for weights_tuple in weights:
        weights_string = weights_tuple[0]
        weights_iterable = iterable_from_weights(weights_string)
        weights_iterables.append(weights_iterable)

    return weights_iterables


def get_seen_states_from_history(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    seen_states_counts = conn.execute("SELECT seen_states_count FROM game_history").fetchall()
    conn.close()
    # convert seen states counts to iterable
    seen_states = [int(x[0]) for x in seen_states_counts]

    return seen_states


def create_board_states_table(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    create_table(conn, create_board_states_table_sql)
    conn.close()


def create_game_history_table(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    create_table(conn, create_game_history_table_sql)
    conn.close()


def forget_all_board_states(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM board_states')
    conn.commit()
    conn.close()


def forget_all_game_history(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM game_history')
    conn.commit()
    conn.close()


def count_seen_states(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    seen_states = conn.execute("SELECT count(*) FROM board_states").fetchone()[0]
    return seen_states


if __name__ == '__main__':
    # connection = create_connection('./sqlite/db_1.db')
    # create_table(connection, create_board_states_table_sql)
    opp_name = 'test_opponent'
    opp_char = 'X'
    create_board_states_table(opp_name, opp_char)

    # initialize game with starting game state
    initial_config = [settings['blank_char']] * 9
    init_weights = [10] * 9
    init_next = []

    # initial_board_state = (initial_config, initial_weights, initial_next)

    connection = create_connection('sqlite/' + opp_name + '_' + opp_char + '.db')

    insert_board_state(connection, board_state_from_iterables(initial_config, init_weights, init_next))

    connection.close()

    test_opponent_name = 'opponent_13'
    test_opponent_char = 'X'

    result = get_seen_states_from_history(test_opponent_name, test_opponent_char)
    print(f'last seen_states: {list(set(result))[-10:]}')
