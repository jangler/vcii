import curses

from vcii.sheet import Sheet


class App:

    def __init__(self):
        self.sheets = [Sheet()]
        self.sheet = self.sheets[0]

    def key_command(self, ch, keyname):
        if ch in (curses.KEY_DOWN, ord('\n')):
            self.sheet.move_cursor(0, 1)
        elif ch == curses.KEY_UP:
            self.sheet.move_cursor(0, -1)
        elif ch == curses.KEY_LEFT:
            self.sheet.move_cursor(-1, 0)
        elif ch in (curses.KEY_RIGHT, ord('\t')):
            self.sheet.move_cursor(1, 0)
        elif ch == curses.KEY_BACKSPACE:
            self.sheet.backspace()
        elif keyname == '^X':
            return False
        elif len(keyname) == 1:
            self.sheet.append(keyname)

        return True
