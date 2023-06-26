import matplotlib.pyplot as plt
import numpy as np

from database import get_blank_weights, iterable_from_weights, get_blank_weights_from_history
from settings import settings

# def get_

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)
weights_string = get_blank_weights('opponent_7', 'X')
weights = iterable_from_weights(weights_string)
weights_sum = sum(weights)
print(f'weights_sum: {weights_sum}')

# x2 = np.linspace()


def draw_blank_weights_over_time(opponent_name, opponent_char) -> None:
    blank_weights_history = get_blank_weights_from_history(opponent_name, opponent_char)
    # add the initial (pre games) weights
    default_weights = [settings['init_weight'] for i in range(9)]
    default_weights_string = ','.join(list(map(str, default_weights)))
    blank_weights_history.insert(0, default_weights)

    x = range(0, len(blank_weights_history))
    y = weight_sums_from_history(blank_weights_history)

    fig, ax = plt.subplots()
    ax.plot(x, y)
    plt.show()


def weight_sums_from_history(blank_weights: list[iter]) -> list[int]:
    print(f'blank_weights: {blank_weights}')
    weight_sums = []
    for i in range(0, len(blank_weights)):
        weight_sums.append(sum(blank_weights[i]))
    return weight_sums


if __name__ == '__main__':
    opponent_name = 'opponent_8'
    opponent_char = 'X'

    draw_blank_weights_over_time(opponent_name, opponent_char)
    # fig, ax = plt.subplots()
    # ax.plot(x, y)
    # plt.show()
    # print(f'weights: {weights}')
