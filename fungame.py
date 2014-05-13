import sys, random

from curtsies.fmtfuncs import *

from curtsies.window import Window
from curtsies.terminal import Terminal
from curtsies.fsarray import FSArray

# def test_colors():
#     board = [
#                 [0,2,4,8],
#                 [16,32,64,128],
#                 [256,512,1024,2048],
#                 [0, 0, 0, 0]
#             ]


#     with Terminal(sys.stdin, sys.stdout) as tc:
#         with Window(tc) as t:
#             t.render_to_terminal(printBoard(board))
#             rows, columns = t.tc.get_screen_size()
#             c = t.tc.get_event()
                
            

def printBoard(board):
    colors = {
              2: lambda x: yellow(x),
              4: lambda x: red(x),
              8: lambda x: blue(x),
              16: lambda x: green(x),
              32: lambda x: bold(yellow(x)),
              64: lambda x: bold(red(x)),
              128: lambda x: bold(blue(x)),
              256: lambda x: bold(green(x)),
              512: lambda x: on_blue(bold(yellow(x))),
              1024: lambda x: on_green(bold(red(x))),
              2048: lambda x: on_red(bold(blue(x)))
             }
    ret = []
    for row in board:
        line = ''
        for cell in row:
            line += colors.get(cell, lambda x: '.' if x == '0' else x)(str(cell)).center(6)
        ret.append(line)
    return ret

def initBoard():
    board = [ [ 0 ] * 4 for _ in range(4) ]
    board[1][3] = 2
    board[3][2] = 2
    return board


def tilt_line(line):
    '''
    >>> tilt_line([0,0,0,0])
    [0, 0, 0, 0]
    >>> tilt_line([0,0,0,2])
    [2, 0, 0, 0]
    >>> tilt_line([0,2,0,2])
    [4, 0, 0, 0]
    >>> tilt_line([0,2,4,4])
    [2, 8, 0, 0]
    '''
    entries = [x for x in line if x]
    if not entries:
        return [0, 0, 0, 0]
    if len(entries) == 1:
        return [entries[0], 0, 0, 0]

    ret = []
    skip = False

    for curr, next in zip(entries[:-1], entries[1:]):
        if skip:
            skip = False
            continue
        if curr == next:
            ret.append(curr * 2)
            skip = True
        else:
            ret.append(curr)

    if not skip:
        ret.append(next)

    return (ret + [0,0,0,0])[:4]



def move_left(board):
    for line in board:
        line[:] = tilt_line(line)


def move_right(board):
    for line in board:
        line[:] = tilt_line(line[::-1])[::-1]

def move_up(board):
    tilted = []
    columns = zip(*board)
    for col in columns:
        tilted.append(tilt_line(col))
    for row, line in zip(zip(*tilted), board):
        line[:] = row

def move_down(board):
    board[:] = board[::-1]
    move_up(board)
    board[:] = board[::-1]

def get_new_tile():
    if random.random() > 0.9:
        return 4
    else:
        return 2

def choose_empty(board):
    spots = []
    for i, row in enumerate(board):
        for j, cell in enumerate(row):
            if not cell:
                spots.append([i,j])
    if not spots:
        raise ValueError("Game over. You lose.")
    return random.choice(spots)

def add_tile(board):
    i, j = choose_empty(board)
    board[i][j] = get_new_tile()


def main():
    # board = [
    #         [0,2,4,8],
    #         [16,32,64,128],
    #         [256,512,1024,2048],
    #         [0, 0, 0, 0]
    #     ]

    board = initBoard()

    moves = {'KEY_LEFT': move_left, 'KEY_RIGHT': move_right, 'KEY_UP': move_up, 'KEY_DOWN': move_down}

    with Terminal(sys.stdin, sys.stdout) as tc:
        with Window(tc) as t:
            rows, columns = t.tc.get_screen_size()
            while True:
                c = t.tc.get_event()
                if c == 'q':
                    return
                elif c in moves:
                    old_board = tuple([tuple(e) for e in board])
                    moves[c](board)

                    if old_board != tuple([tuple(e) for e in board]):
                        add_tile(board)

                t.render_to_terminal(printBoard(board))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
