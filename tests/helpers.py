import database as db
import os


opponent_name = 'test_opponent'
opponent_char = 'X'
sample_config_1 = '.........'
sample_config_2 = 'XO.OX....'
sample_config_3 = 'XO.OX..XO'

file_string = os.getcwd() + '/sqlite/' + opponent_name + '_' + opponent_char + '.db'


def create_db_and_table(db_filepath=file_string):
    """
    Create a test database and board_states table for test opponent
    (sqlite creates a db if it doesn't exist)
    :return: None
    """
    # conn = db.create_connection('../sqlite/' + opponent_name + '_' + opponent_char + '.db')
    # file_string = os.getcwd() + '/sqlite/' + opponent_name + '_' + opponent_char + '.db'
    print(f'db_filepath: {db_filepath}')
    if os.path.exists(db_filepath):
        print('file exists')
    else:
        print('file does not exist')

    conn = db.create_connection(db_filepath)

    db.create_table(conn, db.create_board_states_table_sql)

    conn.close()


def initialize_board_states(db_filepath=file_string):
    """
    Initialize board_states table with sample board states
    :return: None
    """
    # file_string = os.getcwd() + '/sqlite/' + opponent_name + '_' + opponent_char + '.db'
    conn = db.create_connection(db_filepath)

    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO board_states VALUES ('" + sample_config_1 + "', '10,10,10,10,10,10,10,10,10', '')")
    cur.execute("INSERT OR IGNORE INTO board_states VALUES ('" + sample_config_2 + "', '0,0,10,0,0,10,10,10,10', '')")
    cur.execute("INSERT OR IGNORE INTO board_states VALUES ('" + sample_config_3 + "', '0,0,23,0,0,5,6,0,0', '')")

    conn.commit()
    conn.close()


def destroy_table(db_filepath=file_string):
    """
    Destroy a database for opponent
    :return: None
    """
    # file_string = os.getcwd() + '/sqlite/' + opponent_name + '_' + opponent_char + '.db'
    conn = db.create_connection(db_filepath)

    cur = conn.cursor()
    cur.execute("DROP TABLE board_states")

    conn.close()


def get_connection(db_filepath=file_string):
    # file_string = os.getcwd() + '/sqlite/' + opponent_name + '_' + opponent_char + '.db'
    return db.create_connection(db_filepath)


def destroy_db(db_filepath=file_string):
    """
    Destroy a test database
    (sqlite doesn't have a drop database command, so we delete the file itself)
    :return: None
    """
    # file_string = os.getcwd() + '/sqlite/' + opponent_name + '_' + opponent_char + '.db'
    # db_filepath = '/sqlite/' + opponent_name + '_' + opponent_char + '.db'
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
