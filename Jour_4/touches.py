import curses

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(1)

while True:
    c = stdscr.getch()
    stdscr.refresh()
    if c != -1:
        stdscr.addstr(0, 0, str(c) + ' => ' )#+ chr(c))
    elif c == curses.KEY_LEFT:
        stdscr.addstr(0, 0, 'Gauche     ')
    elif c == curses.KEY_RIGHT:
        stdscr.addstr(0, 0, 'Droite     ')
    elif c == 27:
        stdscr.keypad(False)
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        break

print('Au revoir...')
