from database import create_connection, create_board_states_table_sql, create_table
import os


opponent_name = 'test_opponent'
opponent_char = 'X'


def create_db_and_table():
    """
    Create a test database and board_states table for test opponent
    (sqlite creates a db if it doesn't exist)
    :return: None
    """
    conn = create_connection('../sqlite/' + opponent_name + '_' + opponent_char + '.db')

    create_table(conn, create_board_states_table_sql)

    conn.close()


def destroy_table():
    """
    Destroy a database for opponent
    :return: None
    """
    conn = create_connection('../sqlite/' + opponent_name + '_' + opponent_char + '.db')

    cur = conn.cursor()
    cur.execute("DROP TABLE board_states")

    conn.close()


def destroy_db():
    """
    Destroy a test database
    (sqlite doesn't have a drop database command, so we delete the file itself)
    :return: None
    """
    db_filepath = '../sqlite/' + opponent_name + '_' + opponent_char + '.db'
    try:
        os.remove(db_filepath)
    except FileNotFoundError as err:
        print(f'Could not destroy db: {err})')


if __name__ == '__main__':
    # assert db is created
    create_db_and_table()
    assert os.path.exists('../sqlite/test_opponent_X.db')

    # assert table is created
    conn = create_connection('../sqlite/test_opponent_X.db')
    sql_tables_string = 'SELECT name FROM sqlite_master WHERE type=\'table\' AND name=\'board_states\''
    result = conn.cursor().execute(sql_tables_string).fetchall()
    print(f'result: {result}')
    assert len(result) == 1

    # assert table is destroyed
    destroy_table()
    result = conn.cursor().execute(sql_tables_string).fetchall()
    assert result == []

    conn.close()

    # assert db is destroyed
    destroy_db()
    assert not os.path.exists('../sqlite/test_opponent_X.db')
