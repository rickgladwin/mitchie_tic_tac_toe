import database as db
import os


opponent_name = 'test_opponent'
opponent_char = 'X'
sample_config_1 = '.........'
sample_weights_1 = '10,10,10,10,10,10,10,10,10'
sample_config_2 = 'XO.OX....'
sample_weights_2 = '0,0,10,0,0,10,10,10,10'
sample_config_3 = 'XO.OX..XO'
sample_weights_3 = '0,0,23,0,0,5,6,0,0'

sample_board_states = [
    ('.........', '10,14,18,5,16,10,20,8,20', ''),  # initial board state (all games)
    # ('......X..', '10,16,14,5,16,10,0,5,20', ''),  # game 1 play 1
    ('O.....X..', '0,11,14,7,18,10,0,5,20', ''),  # game 1 play 2
    # ('O.....XX.', '0,9,16,7,18,10,0,0,20', ''),  # game 1 play 3
    ('O.....XXO', '0,7,18,8,22,13,0,0,0', ''),  # game 1 play 4
    # ('O.X...XXO', '0,7,0,10,21,13,0,0,0', ''),  # game 1 play 5
    ('O.X...XXO', '0,7,0,10,50,13,0,0,0', ''),  # game 1 play 6 (O wins with position 4)
    ('..X....O.', '10,10,0,10,14,20,10,0,10', ''),  # game 2 play pair 1
    ('.XX....OO', '10,0,0,10,16,18,10,0,0', ''),  # game 2 play pair 2
    ('.XXXO..OO', '50,0,0,0,0,18,10,0,0', ''),  # game 2 final board state (X wins with position 0)
    ('XO.OX....', '0,0,10,0,0,10,10,10,10', ''),
    ('XO.OX..XO', '0,0,23,0,0,5,6,0,0', ''),
]

# sample_game_thread = [
#     (['.', '.', '.', '.', '.', '.', '.', '.', '.'], 'test_opponent', 'X', 6),  # initial board state (all games)
#     (['.', '.', '.', '.', '.', '.', 'X', '.', '.'], 'test_opponent', 'O', 0),  # game 1 play 1
#     (['O', '.', '.', '.', '.', '.', 'X', '.', '.'], 'test_opponent', 'X', 7),  # game 1 play 2
#     (['O', '.', '.', '.', '.', '.', 'X', 'X', '.'], 'test_opponent', 'O', 8),  # game 1 play 3
#     (['O', '.', '.', '.', '.', '.', 'X', 'X', 'O'], 'test_opponent', 'X', 2),  # game 1 play 4
#     (['O', '.', 'X', '.', '.', '.', 'X', 'X', 'O'], 'test_opponent', 'O', 4),  # game 1 play 5 (O wins with position 4)
# ]

file_string = os.getcwd() + '/sqlite/' + opponent_name + '_' + opponent_char + '.db'


def create_db_and_table(db_filepath=file_string):
    """
    Create a test database and board_states table for test opponent
    (sqlite creates a db if it doesn't exist)
    :return: None
    """
    # print(f'db_filepath: {db_filepath}')
    # if os.path.exists(db_filepath):
    #     print('file exists')
    # else:
    #     print('file does not exist')

    conn = db.create_connection(db_filepath)

    db.create_table(conn, db.create_board_states_table_sql)

    conn.close()


def initialize_board_states(db_filepath=file_string):
    """
    Initialize board_states table with sample board states
    :return: None
    """
    conn = db.create_connection(db_filepath)

    cur = conn.cursor()

    for board_state in sample_board_states:
        cur.execute("INSERT OR IGNORE INTO board_states VALUES ('" + board_state[0] + "', '" + board_state[1] + "', '" + board_state[2] + "')")

    # cur.execute("INSERT OR IGNORE INTO board_states VALUES ('" + sample_config_1 + "', '" + sample_weights_1 + "', '')")
    # cur.execute("INSERT OR IGNORE INTO board_states VALUES ('" + sample_config_2 + "', '" + sample_weights_2 + "', '')")
    # cur.execute("INSERT OR IGNORE INTO board_states VALUES ('" + sample_config_3 + "', '" + sample_weights_3 + "', '')")

    conn.commit()
    conn.close()


def destroy_table(db_filepath=file_string):
    """
    Destroy a database for opponent
    :return: None
    """
    conn = db.create_connection(db_filepath)

    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS board_states")

    conn.close()


def get_connection(db_filepath=file_string):
    return db.create_connection(db_filepath)


def destroy_db(db_filepath=file_string):
    """
    Destroy a test database
    (sqlite doesn't have a drop database command, so we delete the file itself)
    :return: None
    """
    try:
        os.remove(db_filepath)
    except FileNotFoundError as err:
        print(f'Could not destroy db: {err})')


if __name__ == '__main__':

    # assert db is created
    db_file_string = os.getcwd() + '/../sqlite/' + opponent_name + '_' + opponent_char + '.db'
    create_db_and_table(db_file_string)
    assert os.path.exists(db_file_string)

    # assert table is created
    db_conn = db.create_connection(db_file_string)
    sql_tables_string = 'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'board_states\''
    result = db_conn.cursor().execute(sql_tables_string).fetchall()
    print(f'result: {result}')
    print(f'result type: {type(result)}')
    print(f'result[0] type: {type(result[0])}')
    assert len(result) == 1
    assert len(result[0]) == 1

    # assert table is destroyed
    destroy_table(db_file_string)
    result = db_conn.cursor().execute(sql_tables_string).fetchall()
    assert result == []

    db_conn.close()

    # assert db is destroyed
    destroy_db(db_file_string)
    assert not os.path.exists(db_file_string)
