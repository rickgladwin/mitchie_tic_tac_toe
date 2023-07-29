import unittest

from learning import update_db_board_state, update_db_weights
from settings import settings
from .helpers import create_db_and_table, initialize_board_states, destroy_table, destroy_db, \
    get_connection, sample_config_2, sample_weights_2, opponent_name, opponent_char


def setup():
    print('\n---- setup: creating db and table, initializing board_states...')
    # setup test db and test board_states table
    create_db_and_table()
    initialize_board_states()
    print('---- setup: done.')


def teardown():
    print('\n---- teardown: destroying table, destroying db...')
    # drop test board_states table
    destroy_table()
    # destroy test db
    destroy_db()
    print('---- teardown: done.')


sample_game_thread = [
    (['.', '.', '.', '.', '.', '.', '.', '.', '.'], 'test_opponent', 'X', 6),  # initial board state (all games)
    (['.', '.', '.', '.', '.', '.', 'X', '.', '.'], 'test_opponent', 'O', 0),  # game 1 play 1
    (['O', '.', '.', '.', '.', '.', 'X', '.', '.'], 'test_opponent', 'X', 7),  # game 1 play 2
    (['O', '.', '.', '.', '.', '.', 'X', 'X', '.'], 'test_opponent', 'O', 8),  # game 1 play 3
    (['O', '.', '.', '.', '.', '.', 'X', 'X', 'O'], 'test_opponent', 'X', 2),  # game 1 play 4
    (['O', '.', 'X', '.', '.', '.', 'X', 'X', 'O'], 'test_opponent', 'O', 4),  # game 1 play 5 (O wins with position 4)
]


class TestUpdateDbWeights(unittest.TestCase):
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
        teardown()

    def test_updates_db_board_state_with_negative_weight_delta(self):
        setup()

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

        teardown()

    def test_updates_a_set_of_db_board_states(self):
        setup()
        conn = get_connection()
        target_opponent_name = 'test_opponent'
        target_opponent_char = 'X'

        for game_state in sample_game_thread:
            print(game_state)

        # get set of board states matching game thread
        game_board_configs = list(map(lambda x: x[0], filter(lambda x: x[2] == 'X', sample_game_thread)))
        game_board_configs = list(map(lambda x: ''.join(x), game_board_configs))
        print(f'game_board_configs: {game_board_configs}')

        # get set of weights matching game_board_configs
        game_weights_before = conn.cursor().execute(
            "SELECT weights FROM board_states WHERE config IN ('" + "','".join(game_board_configs) + "')").fetchall()
        game_weights_before = list(map(lambda x: x[0], game_weights_before))
        print(f'game_weights_before: {game_weights_before}')

        # update weights based on game thread
        update_db_weights(target_opponent_name, target_opponent_char, sample_game_thread, 'O')

        # assert that weights are updated correctly
        game_weights_after = conn.cursor().execute(
            "SELECT weights FROM board_states WHERE config IN ('" + "','".join(game_board_configs) + "')").fetchall()
        game_weights_after = list(map(lambda x: x[0], game_weights_after))
        print(f'game_weights_after:  {game_weights_after}')

        # In the sample game thread, X loses, so
        # X plays should have matching weights reduced by the loss weight delta
        for game_state in sample_game_thread:
            if game_state[2] == target_opponent_char:
                target_game_weights_before = game_weights_before[game_board_configs.index(''.join(game_state[0]))]
                target_game_weights_before_iterable = list(map(lambda x: int(x), target_game_weights_before.split(',')))
                target_game_weights_after = game_weights_after[game_board_configs.index(''.join(game_state[0]))]
                target_game_weights_after_iterable = list(map(lambda x: int(x), target_game_weights_after.split(',')))
                for i in range(0, len(target_game_weights_before_iterable)):
                    if i != game_state[3]:
                        assert target_game_weights_after_iterable[i] == target_game_weights_before_iterable[i]
                    else:
                        assert target_game_weights_after_iterable[i] == target_game_weights_before_iterable[i] + \
                               settings['loss_weight_delta']

        conn.close()
        # teardown()
