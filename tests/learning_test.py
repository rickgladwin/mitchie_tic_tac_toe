import unittest

from learning import update_db_board_state
from .helpers import create_db_and_table, initialize_board_states, destroy_table, destroy_db, \
    get_connection, sample_config_2, sample_weights_2, opponent_name, opponent_char


# def setup():
#     print('\n---- setup: creating db and table, initializing board_states...')
#     # setup test db and test board_states table
#     create_db_and_table()
#     initialize_board_states()
#     print('---- setup: done.')
#
#
# def teardown():
#     print('\n---- teardown: destroying table, destroying db...')
#     # drop test board_states table
#     destroy_table()
#     # destroy test db
#     destroy_db()
#     print('---- teardown: done.')


def setup():
    print('\n---- setup: creating db and table, initializing board_states...')


def teardown():
    print('\n---- teardown: destroying table, destroying db...')
    # drop test board_states table
    destroy_table()
    # destroy test db
    destroy_db()
    print('---- teardown: done.')


class TestUpdateDbWeights(unittest.TestCase):
    # setup test db and test board_states table
    create_db_and_table()
    initialize_board_states()
    print('---- setup: done.')

    def test_updates_db_board_state(self):
        # regression test for helper constants match (see helpers.py for duplicate variable)
        assert sample_weights_2 == '0,0,10,0,0,10,10,10,10'

        conn = get_connection()
        get_board_state_sql = "SELECT * FROM board_states WHERE config = '" + sample_config_2 + "'"
        sample_config, sample_weights, sample_nexts = conn.cursor().execute(get_board_state_sql).fetchone()
        assert sample_weights == sample_weights_2

        update_db_board_state(conn, sample_config, 5, 2)

        sample_config, sample_weights, sample_nexts = conn.cursor().execute(get_board_state_sql).fetchone()

        assert sample_weights == '0,0,10,0,0,12,10,10,10'

        conn.close()

    def test_updates_db_board_state_with_negative_weight_delta(self):
        # regression test for helper constants match (see helpers.py for duplicate variable)
        assert sample_weights_2 == '0,0,10,0,0,10,10,10,10'

        conn = get_connection()
        get_board_state_sql = "SELECT * FROM board_states WHERE config = '" + sample_config_2 + "'"
        sample_config, sample_weights, sample_nexts = conn.cursor().execute(get_board_state_sql).fetchone()
        assert sample_weights == sample_weights_2

        update_db_board_state(conn, sample_config, 5, -2)

        sample_config, sample_weights, sample_nexts = conn.cursor().execute(get_board_state_sql).fetchone()

        assert sample_weights == '0,0,10,0,0,8,10,10,10'

        conn.close()
