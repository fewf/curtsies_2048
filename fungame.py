import sys

from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red

from curtsies.window import Window
from curtsies.terminal import Terminal
from curtsies.fsarray import FSArray

board = [ [ 0 ] * 4 for _ in range(4) ]

def printBoard(board):
    ret = []
    for row in board:
        line = ''
        for cell in row:
            line += str(cell).center(6)
        ret.append(line)
    return ret

def main():
    with Terminal(sys.stdin, sys.stdout) as tc:
        with Window(tc) as t:
            rows, columns = t.tc.get_screen_size()
            while True:
                c = t.tc.get_event()
                if c == 'q':
                    return
                t.render_to_terminal(printBoard(board))

if __name__ == '__main__':
    main()
