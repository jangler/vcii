import curses

import vcii.display as display
from vcii.app import App


def input_loop(window):
    curses.use_default_colors()
    app = App()
    while True:
        display.draw(window, app.sheets, app.sheet)
        ch = window.getch()
        keyname = curses.keyname(ch).decode('ascii')
        if not app.key_command(ch, keyname):
            break


curses.wrapper(input_loop)
