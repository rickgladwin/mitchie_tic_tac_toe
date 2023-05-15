import sys

from settings import settings

# empty_char = settings['blank_char']
empty_char = '\u2592'


def print_board_simple(board):
    """Prints a tic-tac-toe board (a popable object) to the console."""
    lasts = [2, 5, 8]
    space_afters = [0, 1, 3, 4, 6, 7]

    i = 0

    while i < 9:
        board_entry = board[i]
        if board_entry == settings['blank_char']:
            board_entry = empty_char
        sys.stdout.write(board_entry)
        if i in space_afters:
            sys.stdout.write(' ')
        if i in lasts:
            print('')
        i = i + 1


def print_game_thread(game_thread):
    """Prints the history of the game to the console."""
    for play in game_thread:
        print(play)


if __name__ == '__main__':
    blank = settings['blank_char']
    sample_board = [blank, blank, 'X', blank, 'O', 'X', blank, 'O', blank]
    print_board_simple(sample_board)
