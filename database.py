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

    # print(f'board_state: {board_state}')

    return board_state


def insert_board_state(conn, board_state):
    """
    Add a new board_state to the board_states table
    :param conn: connection object
    :param board_state: tuple of (config, weights, nexts)
    """
    # FIXME: insert_board_state is getting a list of weights that ignore
    #  the played spaces on the board. Look at uses of this function, trace the
    #  arguments.
    config, weights, nexts = board_state
    print(f'inserting board_state: {board_state}')
    sql = ''' INSERT INTO board_states(config,weights,nexts)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, board_state)
        print(f'----- inserted board_state: {board_state}')
    except sqlite3.IntegrityError as e:
        if 'UNIQUE constraint failed' in str(e):
            print(f'board_state exists: {board_state}')
        else:
            print(e)
            print(f'board_state: {board_state}')
    except sqlite3.InterfaceError as e:
        print(e)
        print('Did you remember to convert the iterables to strings?')
    conn.commit()

    # print(f'cur.lastrowid: {cur.lastrowid}')


def insert_fresh_board_state(opponent_name, opponent_char, config):
    """
    Add a new board_state to the board_states table with default weights and nexts
    :param opponent_name: db identifier for opponent
    :param opponent_char: char used by opponent
    :param config: iterable board position statuses
    """
    config_string = config_from_iterable(config)
    # FIXME: all weights in new board_state records are 10 (init_weight)
    #  so this method isn't currently working, or these aren't being applied
    state_weights = list(map(lambda x: 0 if x != settings['blank_char'] else settings['init_weight'], config))
    # state_weights = list(lambda x: 0 if x != settings['blank_char'] else settings['init_weight'] for x in config)

    print(f'state_weights: {state_weights}')
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

    print(f'board_state: {board_state}')

    conn.close()

    return board_state


create_board_states_table_sql = """
CREATE TABLE IF NOT EXISTS board_states (
    config blob UNIQUE PRIMARY KEY, -- status of each space on the board, X, O, or None 
    weights blob, -- probability weighting for each space on the board
    nexts blob -- list of ids for possible states one play after this one
);
"""


def create_board_states_table(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    create_table(conn, create_board_states_table_sql)
    conn.close()


def forget_all_board_states(opponent_name, opponent_char):
    conn = create_connection('sqlite/' + opponent_name + '_' + opponent_char + '.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM board_states')
    conn.commit()
    conn.close()


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
