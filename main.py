import sys

null_board = [None for i in range(0, 10)]
example_board_config = [None, None, 'X', None, 'O', 'X', None, 'O', None]
example_board_weights = [24, 2, 0, 8, 0, 0, 8, 0, 16]


def print_board(board):
    vert = '|'
    horiz = '–'
    cross = '+'

    uprights = [1, 3, 11, 13, 21, 23]
    horizontals = [5, 7, 9, 15, 17, 19]
    crosses = [6, 8, 16, 18]

    # symbols = uprights + horizontals + crosses

    lasts = [4, 9, 14, 19]

    i = 0
    # print top row
    while i < 25:
        is_symbol = False
        if i in uprights:
            sys.stdout.write(vert)
            is_symbol = True
        if i in horizontals:
            sys.stdout.write(horiz)
            is_symbol = True
        if i in crosses:
            sys.stdout.write(cross)
            is_symbol = True
        if not is_symbol:
            board_entry = board.pop(0)
            if board_entry is None:
                board_entry = '#'
            sys.stdout.write(board_entry)
        if i in lasts:
            print('')
        i = i + 1


def print_board_simple(board):
    lasts = [2, 5, 8]

    i = 0

    while i < 9:
        board_entry = board.pop(0)
        if board_entry is None:
            board_entry = '#'
        sys.stdout.write(board_entry)
        if i in lasts:
            print('')
        i = i + 1


def main():
    print('starting...')
    print('starting with an untrained opponent...')
    # initialize opponent
    # TODO: get sqlite models etc. set up based on notes


if __name__ == "__main__":
    print('example board:')
    print_board_simple(example_board_config)
