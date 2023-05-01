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


def insert_game_state(conn, game_state):
    """
    Add a new game_state to the game_states table
    :param conn:
    :param game_state:
    :return: game_state id
    """

    config, weights, nexts = game_state
    sql = ''' INSERT INTO game_states(config,weights,nexts)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, game_state)
    return cur.lastrowid


create_game_states_table_sql = """
CREATE TABLE IF NOT EXISTS game_states (
    config blob UNIQUE PRIMARY KEY, -- status of each space on the board, X, O, or None 
    weights blob, -- probability weighting for each space on the board
    nexts blob -- list of ids for possible states one play after this one
);
"""


def create_game_states_table(opponent_name):
    conn = create_connection('sqlite/' + opponent_name + '.db')
    create_table(conn, create_game_states_table_sql)
    conn.close()


if __name__ == '__main__':
    connection = create_connection('./sqlite/db_1.db')
    create_table(connection, create_game_states_table_sql)
