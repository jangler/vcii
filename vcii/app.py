import curses
import os.path

import vcii.format_csv as format_csv
from vcii.sheet import Sheet


MODE_EXIT = -1
MODE_NORMAL = 0
MODE_QUIT = 1
MODE_OPEN = 2
MODE_SAVE = 3


class App:

    def __init__(self):
        self.sheets = [Sheet()]
        self.sheet = self.sheets[0]
        self.mode = MODE_NORMAL
        self.string_buffer = ''

    def close_tab(self):
        index = self.sheets.index(self.sheet)
        self.sheets.remove(self.sheet)
        if len(self.sheets) > 0:
            self.sheet = self.sheets[index % len(self.sheets)]

    def key_command(self, ch, keyname, parameters=None):
        previous_mode = self.mode
        previous_sheet = self.sheet
        previous_status = self.sheet.status

        if self.mode == MODE_NORMAL:
            if ch in (curses.KEY_DOWN, ord('\n')):
                self.sheet.move_cursor(0, 1)
            elif ch == curses.KEY_UP:
                self.sheet.move_cursor(0, -1)
            elif ch in (curses.KEY_LEFT, curses.KEY_BTAB):
                self.sheet.move_cursor(-1, 0)
            elif ch in (curses.KEY_RIGHT, ord('\t')):
                self.sheet.move_cursor(1, 0)
            elif ch == curses.KEY_BACKSPACE:
                self.sheet.backspace()
            elif keyname == '^O':
                self.mode = MODE_OPEN
                self.string_buffer = ''
            elif keyname == '^Q':
                if self.sheet.modified:
                    self.mode = MODE_QUIT
                else:
                    self.close_tab()
                if len(self.sheets) == 0:
                    self.mode = MODE_EXIT
            elif keyname == '^S':
                self.mode = MODE_SAVE
                if self.sheet.title:
                    self.string_buffer = self.sheet.title
                else:
                    self.string_buffer = ''
            elif keyname == '^T':
                index = self.sheets.index(self.sheet)
                self.sheet = self.sheets[(index + 1) % len(self.sheets)]
                self.sheet.status = 'Editing {}'.format(self.sheet.ui_title)
            elif len(keyname) == 1:
                self.sheet.append(keyname)
            elif ch:
                self.sheet.status = 'Unknown key: {} {}'.format(ch, keyname)
        elif self.mode in (MODE_OPEN, MODE_SAVE):
            prompt = 'Open file:' if self.mode == MODE_OPEN else 'Save as:'
            self.sheet.status = '{} {}'.format(prompt, self.string_buffer)
            previous_buffer = self.string_buffer
            if ch == ord('\n'):
                if self.mode == MODE_OPEN:
                    self.open_file()
                else:
                    self.save_file()
                self.mode = MODE_NORMAL
            elif ch == curses.KEY_BACKSPACE:
                self.string_buffer = self.string_buffer[:-1]
            elif keyname == '^C':
                self.mode = MODE_NORMAL
                self.sheet.status = 'Cancelled'
            elif len(keyname) == 1:
                self.string_buffer += keyname

            if self.string_buffer != previous_buffer:
                self.sheet.status = '{} {}'.format(prompt, self.string_buffer)
        elif self.mode == MODE_QUIT:
            self.sheet.status = 'Discard changes?'
            if keyname.lower() in ('y', 'n'):
                if keyname.lower() == 'y':
                    self.close_tab()
                self.mode = MODE_NORMAL if len(self.sheets) > 0 else MODE_EXIT

        return (previous_mode != self.mode or
                previous_sheet != self.sheet or
                previous_status != self.sheet.status)

    def new_sheet(self):
        sheet = Sheet()
        if self.string_buffer:
            sheet.title = self.string_buffer
        sheet.status = 'New file'
        return sheet

    def open_sheet(self, sheet):
        index = self.sheets.index(self.sheet)
        if self.sheet.modified or self.sheet.title:
            self.sheets.insert(index + 1, sheet)
            self.sheet = sheet
        else:
            self.sheets[index] = sheet
            self.sheet = sheet

    def open_file(self):
        if len(self.string_buffer) == 0:
            self.open_sheet(self.new_sheet())
        elif self.string_buffer.lower().endswith('.csv'):
            try:
                if os.path.isfile(self.string_buffer):
                    read_sheet = format_csv.read(self.string_buffer)
                else:
                    read_sheet = self.new_sheet()
                self.open_sheet(read_sheet)
            except Exception as ex:
                self.sheet.status = str(ex)
        else:
            self.sheet.status = 'Unsupported file format'

    def save_file(self):
        if self.string_buffer.lower().endswith('.csv'):
            try:
                format_csv.write(self.sheet, self.string_buffer)
            except Exception as ex:
                self.sheet.status = str(ex)
        else:
            self.sheet.status = 'Unsupported file format'
