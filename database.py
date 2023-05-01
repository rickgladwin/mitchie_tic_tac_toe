import sqlite3


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
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

    config_string = ''.join(list(map(str, config)))
    weights_string = ','.join(list(map(str, weights)))
    nexts_string = ','.join(list(map(str, nexts)))

    board_state = (config_string, weights_string, nexts_string)

    print(f'board_state: {board_state}')

    return board_state


def insert_board_state(conn, board_state):
    """
    Add a new board_state to the board_states table
    :param conn:
    :param board_state tuple of (config, weights, nexts)
    """
    config, weights, nexts = board_state
    sql = ''' INSERT INTO board_states(config,weights,nexts)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    try:
        cur.execute(sql, board_state)
    except sqlite3.IntegrityError as e:
        print(e)
        print(f'board_state: {board_state}')
        print(f'config: {config}')
        print(f'weights: {weights}')
        print(f'nexts: {nexts}')
    except sqlite3.InterfaceError as e:
        print(e)
        print('Did you remember to convert the iterables to strings?')
    conn.commit()

    print(f'cur.lastrowid: {cur.lastrowid}')


create_board_states_table_sql = """
CREATE TABLE IF NOT EXISTS board_states (
    config blob UNIQUE PRIMARY KEY, -- status of each space on the board, X, O, or None 
    weights blob, -- probability weighting for each space on the board
    nexts blob -- list of ids for possible states one play after this one
);
"""


def create_board_states_table(opponent_name):
    conn = create_connection('sqlite/' + opponent_name + '.db')
    create_table(conn, create_board_states_table_sql)
    conn.close()


if __name__ == '__main__':
    # connection = create_connection('./sqlite/db_1.db')
    # create_table(connection, create_board_states_table_sql)
    opponent_name = 'test_opponent'
    create_board_states_table(opponent_name)

    # initialize game with starting game state
    initial_config = ['.'] * 9
    initial_weights = [10] * 9
    initial_next = []

    # initial_board_state = (initial_config, initial_weights, initial_next)

    connection = create_connection('sqlite/' + opponent_name + '.db')

    insert_board_state(connection, board_state_from_iterables(initial_config, initial_weights, initial_next))

    connection.close()

