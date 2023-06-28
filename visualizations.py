import matplotlib.pyplot as plt

from database import get_blank_weights, iterable_from_weights, get_blank_weights_from_history
from settings import settings


def draw_blank_weights_over_time(opponent_name, opponent_char) -> None:
    blank_weights_history = get_blank_weights_from_history(opponent_name, opponent_char)
    # add the initial (pre games) weights
    default_weights = [settings['init_weight'] for i in range(9)]
    blank_weights_history.insert(0, default_weights)

    x = range(0, len(blank_weights_history))
    y = weight_sums_from_history(blank_weights_history)

    fig, ax = plt.subplots()
    ax.set_title(f'{opponent_name}_{opponent_char} learning progress (proxy)')
    ax.set_xlabel('game number')
    ax.set_ylabel('blank state weights sum')
    ax.plot(x, y)
    plt.show()


def weight_sums_from_history(blank_weights: list[iter]) -> list[int]:
    weight_sums = []
    for i in range(0, len(blank_weights)):
        weight_sums.append(sum(blank_weights[i]))
    return weight_sums


if __name__ == '__main__':
    # opponent_name = 'opponent_8'
    test_opponent_name = 'opponent_9'
    test_opponent_char = 'X'

    draw_blank_weights_over_time(test_opponent_name, test_opponent_char)

