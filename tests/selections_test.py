import math
from selections import range_starts, select_move


class TestRangeStarts:
    def test_builds_with_basic_weights(self):
        test_weights = [50, 50]
        expected_range_starts = [1, 51]
        result = range_starts(test_weights)
        assert (result == expected_range_starts)

    def test_builds_with_basic_weights_using_tuple(self):
        test_weights = (50, 50)
        expected_range_starts = [1, 51]
        result = range_starts(test_weights)
        assert (result == expected_range_starts)

    def test_builds_with_weights_including_zeroes(self):
        test_weights = [50, 0, 10, 0, 50]
        expected_range_starts = [1, 51, 51, 61, 61]
        result = range_starts(test_weights)
        assert (result == expected_range_starts)

    def test_builds_with_weights_including_trailing_zero(self):
        test_weights = [50, 0, 10, 0, 50, 5, 0]
        expected_range_starts = [1, 51, 51, 61, 61, 111, 116]
        result = range_starts(test_weights)
        assert (result == expected_range_starts)

    def test_builds_with_weights_including_leading_zero(self):
        test_weights = [0, 0, 50, 0, 10, 0, 0, 50, 5, 0, 0]
        expected_range_starts = [1, 1, 1, 51, 51, 61, 61, 61, 111, 116, 116]
        result = range_starts(test_weights)
        assert (result == expected_range_starts)

    def test_builds_with_all_zeros(self):
        test_weights = [0, 0, 0, 0, 0]
        expected_range_starts = [1, 1, 1, 1, 1]
        result = range_starts(test_weights)
        assert (result == expected_range_starts)

    def test_builds_with_empty_weights(self):
        test_weights = []
        expected_range_starts = []
        result = range_starts(test_weights)
        assert (result == expected_range_starts)

    def test_builds_with_empty_weights_using_tuple(self):
        test_weights = ()
        expected_range_starts = []
        result = range_starts(test_weights)
        assert (result == expected_range_starts)


class TestMoveSelection:
    def test_selects_no_move_when_weights_are_all_zeros(self):
        test_weights = [0, 0, 0]
        expected_result = None
        result = select_move(test_weights)
        assert (result == expected_result)

    def test_selects_no_move_when_weights_are_empty(self):
        test_weights = []
        expected_result = None
        result = select_move(test_weights)
        assert (result == expected_result)

    def test_never_selects_move_0_when_weight_0_is_zero(self):
        test_weights = [0, 50, 50]
        # call select_move 100 times and check that it never returns 0
        for i in range(0, 100):
            result = select_move(test_weights)
            assert (result != 0)

    def test_never_selects_move_1_when_weight_1_is_zero(self):
        test_weights = [50, 0, 50]
        # call select_move 100 times and check that it never returns 1
        for i in range(0, 100):
            result = select_move(test_weights)
            assert (result != 1)

    def test_never_selects_last_move_when_last_weight_is_zero(self):
        test_weights = [50, 50, 0]
        # call select_move 100 times and check that it never returns 2
        for i in range(0, 100):
            result = select_move(test_weights)
            assert (result != 2)

    def test_only_selects_the_nonzero_move(self):
        test_weights = [0, 0, 0, 0, 345, 0]
        # call select_move 100 times and check that it only returns 4
        for i in range(0, 100):
            result = select_move(test_weights)
            assert (result == 4)

    def test_never_selects_first_or_last_2_moves_when_first_last_2_weights_are_zero(self):
        test_weights = [0, 50, 26, 0, 0]
        # call select_move 100 times and check that it never returns 0, 3, or 4
        for i in range(0, 100):
            result = select_move(test_weights)
            assert (result != 0)
            assert (result != 3)
            assert (result != 4)

    def test_never_selects_first_2_or_last_2_moves_when_first_2_last_2_weights_are_zero(self):
        test_weights = [0, 0, 50, 26, 0, 0]
        # call select_move 100 times and check that it never returns 0, 3, or 4
        for i in range(0, 100):
            result = select_move(test_weights)
            assert (result != 0)
            assert (result != 1)
            assert (result != 4)
            assert (result != 5)

    def test_never_selects_either_move_with_weight_zero(self):
        test_weights = [50, 0, 10, 0, 50]
        # call select_move 100 times and check that it never returns 2
        for i in range(0, 100):
            result = select_move(test_weights)
            assert (result != 1)
            assert (result != 3)

    def test_selects_moves_with_rates_matching_weights(self):
        test_weights = [0, 0, 50, 24, 0, 50, 0, 10, 5, 60, 7]
        results = [0] * len(test_weights)
        total_trials = 1000
        print(f'\ntotal_trials: {total_trials}')

        target_counts = []
        for i in range(0, len(test_weights)):
            target_counts.append(round(test_weights[i] / sum(test_weights) * total_trials))

        result_deviation_threshold_percent = 5
        result_deviation_threshold = result_deviation_threshold_percent / math.sqrt(total_trials)
        print(f'result_deviation_threshold: {result_deviation_threshold}')
        for i in range(0, total_trials):
            results[select_move(test_weights)] += 1

        print(f'test_weights:  {test_weights}')
        print(f'target_counts: {target_counts}')
        print(f'results:       {results}')

        # check that each result is within the threshold of the expected rate based on the weights
        for i in range(0, len(test_weights)):
            # expected result count for this index as a fraction
            expected_rate = test_weights[i] / sum(test_weights)
            # result count for this index as a fraction
            actual_rate = results[i] / total_trials
            assert (abs(expected_rate - actual_rate) < result_deviation_threshold)
