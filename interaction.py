import sys

# empty_char = '.'
empty_char = '\u2592'


def print_board_simple(board):
    """Prints a tic-tac-toe board (a popable object) to the console."""
    lasts = [2, 5, 8]
    space_afters = [0, 1, 3, 4, 6, 7]

    i = 0

    while i < 9:
        board_entry = board.pop(0)
        if board_entry is '.':
            board_entry = empty_char
        sys.stdout.write(board_entry)
        if i in space_afters:
            sys.stdout.write(' ')
        if i in lasts:
            print('')
        i = i + 1


if __name__ == '__main__':
    sample_board = ['.', '.', 'X', '.', 'O', 'X', '.', 'O', '.']
    print_board_simple(sample_board)
