import sys

from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red

from curtsies.window import Window
from curtsies.terminal import Terminal
from curtsies.fsarray import FSArray



def printBoard(board):
    ret = []
    for row in board:
        line = ''
        for cell in row:
            line += str(cell).center(6)
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
    '''
    entries = [x for x in line if x]
    if not entries:
        return [0, 0, 0, 0]
    if len(entries) == 1:
        return [entries[0], 0, 0, 0]
    if len(entries) == 2:
        if entries[0] == entries[1]:
            return [entries[0] * 2, 0, 0, 0]
        else:
            return [entries[0], entries[1], 0, 0]

def move_left(board):
    pass

def main():
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
                    moves[c]()
                t.render_to_terminal(printBoard(board))
                print(c)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    main()
