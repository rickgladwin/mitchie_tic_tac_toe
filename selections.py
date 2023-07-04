import random


def range_starts(weights):
    """Generate a list of range starts, given a list of weights"""
    starts = []
    if len(weights) > 0:
        starts.append(1)
        for i in range(0, len(weights) - 1):
            starts.append(weights[i] + starts[-1])

    return starts


def select_move(weights):
    """Select an index from a list of weights, using a weighted random selection"""
    if sum(weights) == 0:
        return None
    starts: iter = range_starts(weights)
    hit_index = 0
    roll = random.randint(1, sum(weights))
    for i in range(len(weights) - 1, 0, -1):
        # print(f'checking range_starts[{i}]...')
        if roll >= starts[i]:
            hit_index = i
            break

    # print(f'roll {roll} is in index {hit_index} of weights_list (weighting {weights_list[hit_index]})')
    return hit_index


# weights_list = [50, 50]  # total 100
# range_starts = [1, 51]

# weights_list = [25, 50, 10, 15]  # total 100
# range_starts = [1, 26, 76, 86]  # TODO: confirm that this yields the correct number of spaces for each

# weights_list = [50, 0, 10, 50]  # total 110
# range_starts = [1, 51, 51, 61]  # hit_index should never be 1

# weights_list = [50, 0, 10, 0, 50]  # total 110
# range_starts = [1, 51, 51, 61, 61]  # hit_index should never be 1 or 3

# weights_list =  [50, 0,  10, 0,  50, 5,   0]  # total 115
# range_starts = [1,  51, 51, 61, 61, 111, 116]  # hit_index should never be 1, 3, or 6

# weights_list =  [0, 50, 0,  10, 0,  50, 5,   0]  # total 115
# range_starts = [1, 1,  51, 51, 61, 61, 111, 116]  # hit_index should never be 0, 2, 4, or 7

# TODO: deal with case starting with one and ending with two zeros
# weights_list =  [0, 50, 0,  10, 0,  50, 5,   0,   0]  # total 115
# range_starts = [1, 1,  51, 51, 61, 61, 111, 116, 116]  # hit_index should never be 0, 2, 4, 7, or 8

# TODO: deal with case starting with two and ending with two zeros
# weights_list =  [0, 0, 50, 0,  10, 0,  50, 5,   0,   0]  # total 115
# range_starts = [1, 1, 1,  51, 51, 61, 61, 111, 116, 116]  # hit_index should never be 0, 1, 3, 5, 8, or 9

# TODO: deal with case starting with two and ending with two zeros with multiple zeros within
# weights_list =  [0, 0, 50, 0,  10, 0,  0,  50, 5,   0,   0]  # total 115
# range_starts = [1, 1, 1,  51, 51, 61, 61, 61, 111, 116, 116]  # hit_index should never be 0, 1, 3, 5, 6, 9, or 10

# TODO: deal with all zeroes case
# weights_list =  [0, 0, 0]  # total 0
# range_starts = [1, 1, 1]  # hit_index should not be 0, 1, or 2

# TODO: deal with all zeroes but one case
# weights_list =  [0, 1, 0]  # total 1
# range_starts = [1, 1, 2]  # hit_index should not be 0 or 2

# prob_mapping = [(1, 50), (51, 100)]

# TODO: this algorithm could be optimized for larger n with a
#  different search algorithm or with some pre-processing
#  It's already optimized for this use case (n = 9) though, maybe.
#  The thing is, since there's no way of knowing what the weights will be,
#  there's no way of predicting the distribution exactly, so it's hard to know
#  what search algorithm to use. You'd have to track what weights come in
#  over time for each use case, and optimize _for that use case_ based on what shows up.
#  A good candidate for AI optimization, or for data analysis.
