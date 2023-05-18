import unittest

from gameplay import winning_play


class TestWinningPlay(unittest.TestCase):
    def test_finds_no_winning_play_from_initial_board(self):
        sample_board_config = [
            '.', '.', '.',
            '.', '.', '.',
            '.', '.', '.',
        ]
        assert winning_play(sample_board_config, 'X') is None
        assert winning_play(sample_board_config, 'O') is None

    def test_finds_winning_play_on_first_diagonal_top_left(self):
        sample_board_config = [
            '.', 'X', '.',
            '.', 'O', 'X',
            '.', 'X', 'O',
        ]
        assert winning_play(sample_board_config, 'O') == '1'

    def test_finds_winning_play_on_first_diagonal_middle(self):
        sample_board_config = [
            'O', 'X', '.',
            '.', '.', 'X',
            '.', 'X', 'O',
        ]
        assert winning_play(sample_board_config, 'O') == '5'

    def test_finds_winning_play_on_first_diagonal_bottom_right(self):
        sample_board_config = [
            'O', 'X', '.',
            '.', 'O', 'X',
            '.', 'X', '.',
        ]
        assert winning_play(sample_board_config, 'O') == '9'

    def test_finds_winning_play_on_second_diagonal_top_right(self):
        sample_board_config = [
            '.', 'X', '.',
            '.', 'O', 'X',
            'O', 'X', '.',
        ]
        assert winning_play(sample_board_config, 'X') is None
        assert winning_play(sample_board_config, 'O') == '3'

    def test_finds_winning_play_on_second_diagonal_middle(self):
        sample_board_config = [
            '.', 'X', 'O',
            '.', '.', 'X',
            'O', 'X', '.',
        ]
        assert winning_play(sample_board_config, 'O') == '5'

    def test_finds_winning_play_on_second_diagonal_bottom_left(self):
        sample_board_config = [
            '.', 'X', 'O',
            '.', 'O', 'X',
            '.', 'X', '.',
        ]
        assert winning_play(sample_board_config, 'X') is None
        assert winning_play(sample_board_config, 'O') == '7'

    def test_finds_winning_play_on_first_row_first(self):
        sample_board_config = [
            '.', 'X', 'X',
            'X', 'O', 'O',
            '.', 'O', '.',
        ]
        assert winning_play(sample_board_config, 'X') == '1'

    def test_finds_winning_play_on_first_row_second(self):
        sample_board_config = [
            'X', '.', 'X',
            'O', 'X', 'O',
            'O', '.', '.',
        ]
        assert winning_play(sample_board_config, 'X') == '2'

    def test_finds_winning_play_on_first_row_last(self):
        sample_board_config = [
            'X', 'X', '.',
            'O', 'X', 'O',
            '.', 'O', '.',
        ]
        assert winning_play(sample_board_config, 'X') == '3'

    def test_finds_winning_play_on_second_row_first(self):
        sample_board_config = [
            'O', 'X', 'O',
            '.', 'X', 'X',
            'O', 'O', '.',
        ]
        assert winning_play(sample_board_config, 'X') == '4'

    def test_finds_winning_play_on_second_row_middle(self):
        sample_board_config = [
            'O', 'X', 'O',
            'X', '.', 'X',
            'O', 'O', '.',
        ]
        assert winning_play(sample_board_config, 'X') == '5'

    def test_finds_winning_play_on_second_row_last(self):
        sample_board_config = [
            'O', 'X', 'O',
            'X', 'X', '.',
            'O', 'O', '.',
        ]
        assert winning_play(sample_board_config, 'X') == '6'

    def test_finds_winning_play_on_third_row_first(self):
        sample_board_config = [
            'O', 'X', 'O',
            'O', 'O', '.',
            '.', 'X', 'X',
        ]
        assert winning_play(sample_board_config, 'X') == '7'

    def test_finds_winning_play_on_third_row_middle(self):
        sample_board_config = [
            'O', 'X', 'O',
            'O', 'O', '.',
            'X', '.', 'X',
        ]
        assert winning_play(sample_board_config, 'X') == '8'

    def test_finds_winning_play_on_third_row_last(self):
        sample_board_config = [
            'O', 'X', 'O',
            'O', 'O', '.',
            'X', 'X', '.',
        ]
        assert winning_play(sample_board_config, 'X') == '9'

    def test_finds_winning_play_on_first_column_first(self):
        sample_board_config = [
            '.', 'O', '.',
            'X', 'O', 'X',
            'X', '.', 'O',
        ]
        assert winning_play(sample_board_config, 'X') == '1'

    def test_finds_winning_play_on_first_column_middle(self):
        sample_board_config = [
            'X', 'O', '.',
            '.', 'O', 'X',
            'X', '.', 'O',
        ]
        assert winning_play(sample_board_config, 'X') == '4'

    def test_finds_winning_play_on_first_column_last(self):
        sample_board_config = [
            'X', 'O', '.',
            'X', 'O', 'X',
            '.', '.', 'O',
        ]
        assert winning_play(sample_board_config, 'X') == '7'

    def test_finds_winning_play_on_second_column_first(self):
        sample_board_config = [
            '.', '.', '.',
            'O', 'X', 'X',
            'O', 'X', 'O',
        ]
        assert winning_play(sample_board_config, 'X') == '2'

    def test_finds_winning_play_on_second_column_middle(self):
        sample_board_config = [
            'O', 'X', '.',
            '.', '.', 'X',
            'O', 'X', 'O',
        ]
        assert winning_play(sample_board_config, 'X') == '5'

    def test_finds_winning_play_on_second_column_last(self):
        sample_board_config = [
            'O', 'X', '.',
            'O', 'X', 'X',
            '.', '.', 'O',
        ]
        assert winning_play(sample_board_config, 'X') == '8'

    def test_finds_winning_play_on_third_column_first(self):
        sample_board_config = [
            '.', '.', '.',
            'O', 'X', 'X',
            'O', 'O', 'X',
        ]
        assert winning_play(sample_board_config, 'X') == '3'

    def test_finds_winning_play_on_third_column_middle(self):
        sample_board_config = [
            'O', 'X', 'X',
            '.', '.', '.',
            'O', 'O', 'X',
        ]
        assert winning_play(sample_board_config, 'X') == '6'

    def test_finds_winning_play_on_third_column_last(self):
        sample_board_config = [
            'O', 'X', 'X',
            'O', 'X', 'X',
            '.', 'O', '.',
        ]
        assert winning_play(sample_board_config, 'X') == '9'
