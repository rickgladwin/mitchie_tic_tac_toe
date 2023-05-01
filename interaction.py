import sys


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


if __name__ == '__main__':
    sample_board = [None, None, 'X', None, 'O', 'X', None, 'O', None]
    print_board_simple(sample_board)
