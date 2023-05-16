# import pytest_helpers as h
# from database import create_connection
from .helpers import create_db_and_table, initialize_board_states, destroy_table, destroy_db, \
    get_connection, sample_config_2


def setup():
    # setup test db and test board_states table
    create_db_and_table()
    initialize_board_states()


def teardown():
    # drop test board_states table
    destroy_table()
    # destroy test db
    destroy_db()


class TestUpdateDbWeights:
    def test_updates_db_board_state(self):
        # TODO: get an existing board state based on config
        conn = get_connection()
        get_board_state_sql = "SELECT * FROM board_states WHERE config = '" + sample_config_2 + "'"
        print(f'get_board_state_sql: {get_board_state_sql}')
        conn.cursor().execute(get_board_state_sql)
        sample_board_state = conn.cursor().fetchone()
        print(f'sample_board_state: {sample_board_state}')
        conn.close()
        # TODO: update the weight of a position in the board state
        # TODO: assert that the weight of the position in the board state is updated
