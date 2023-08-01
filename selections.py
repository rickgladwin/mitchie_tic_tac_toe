import random


def range_starts(weights: list[int] | tuple[int, ...]) -> list:
    """Generate a list of range starts, given a list or tuple of weights"""
    starts = []
    if len(weights) > 0:
        starts.append(1)
        for i in range(0, len(weights) - 1):
            starts.append(weights[i] + starts[-1])

    return starts


def select_move(weights: list[int] | tuple[int, ...]) -> int | None:
    """Select an index from a list or tuple of weights, using a weighted random selection"""
    if sum(weights) == 0:
        return None
    starts = range_starts(weights)
    hit_index = 0
    roll = random.randint(1, sum(weights))
    for i in range(len(weights) - 1, 0, -1):
        if roll >= starts[i]:
            hit_index = i
            break

    return hit_index


# TODO: this algorithm could be optimized for larger n with a
#  different search algorithm (maybe) or with some pre-processing
#  It's already optimized enough for this use case (n = 9) though.
#  The thing is, since there's no way of knowing what the weights will be,
#  there's no way of predicting the distribution exactly, so it's hard to know
#  what search algorithm to use. You'd have to track what weights come in
#  over time for each use case, and optimize _for that use case_ based on what shows up.
#  A good candidate for AI optimization, or for data analysis.
