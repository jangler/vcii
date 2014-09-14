import curses

import vcii.display as display
from vcii.app import App, MODE_QUIT


def input_loop(window):
    curses.use_default_colors()
    curses.raw()
    try:
        app = App()
        while app.mode != MODE_QUIT:
            display.draw(window, app.sheets, app.sheet, app.mode)
            ch = window.getch()
            keyname = curses.keyname(ch).decode('utf8')
            if app.key_command(ch, keyname):
                app.key_command(None, '')
    except Exception as ex:
        curses.noraw()
        raise ex


curses.wrapper(input_loop)
