import curses
import unittest

import os

from vcii.app import *


class TestApp(unittest.TestCase):

    def setUp(self):
        self.window = curses.initscr()

    def tearDown(self):
        curses.endwin()

    def test_key_command_normal(self):
        app = App()
        app.key_command(curses.KEY_DOWN, 'KEY_DOWN')
        self.assertEqual(app.sheet.cursor, [0, 1])
        app.key_command(curses.KEY_RIGHT, 'KEY_RIGHT')
        self.assertEqual(app.sheet.cursor, [1, 1])
        app.key_command(curses.KEY_LEFT, 'KEY_LEFT')
        self.assertEqual(app.sheet.cursor, [0, 1])
        app.key_command(curses.KEY_UP, 'KEY_UP')
        self.assertEqual(app.sheet.cursor, [0, 0])
        app.key_command(ord('x'), 'x')
        self.assertEqual(app.sheet.active_cell.content, 'x')
        app.key_command(curses.KEY_BACKSPACE, 'KEY_BACKSPACE')
        self.assertEqual(app.sheet.active_cell.content, '')
        app.mode = MODE_NORMAL
        app.key_command(None, '^O')
        self.assertEqual(app.mode, MODE_OPEN)
        app.mode = MODE_NORMAL
        app.key_command(None, '^Q')
        self.assertEqual(app.mode, MODE_QUIT)
        app.mode = MODE_NORMAL
        app.key_command(None, '^R')
        self.assertEqual(app.sheet.column_width(0), 2)
        app.key_command(None, '^S')
        self.assertEqual(app.mode, MODE_SAVE)
        app.mode = MODE_NORMAL
        app.sheet.title = 'title.csv'
        app.key_command(None, '^S')
        self.assertEqual(app.mode, MODE_SAVE)
        app.mode = MODE_NORMAL
        app.sheets.append(app.new_sheet())
        app.key_command(None, '^T')
        self.assertEqual(app.sheet, app.sheets[1])
        app.key_command(1, 'unknown')
        app.key_command(None, 'not even unknown')
        app.sheet = app.sheets[1]
        app.key_command(None, '^Q')
        self.assertEqual(app.mode, MODE_NORMAL)
        self.assertEqual(len(app.sheets), 1)
        app.sheets[0].modified = False
        app.key_command(None, '^Q')
        self.assertEqual(app.mode, MODE_EXIT)

    def test_key_command_input(self):
        app = App()
        app.mode = MODE_OPEN
        app.key_command(1, 'unknown')
        app.key_command(ord('\n'), '')
        self.assertEqual(app.mode, MODE_NORMAL)
        app.mode = MODE_SAVE
        app.key_command(ord('\n'), '')
        self.assertEqual(app.mode, MODE_NORMAL)
        app.mode = MODE_OPEN
        app.key_command(ord('a'), 'a')
        self.assertEqual(app.string_buffer, 'a')
        app.key_command(curses.KEY_BACKSPACE, 'KEY_BACKSPACE')
        self.assertEqual(app.string_buffer, '')
        app.key_command(None, '^C')
        self.assertEqual(app.mode, MODE_NORMAL)

    def test_key_command_quit(self):
        app = App()
        app.sheet.modified = True
        app.mode = MODE_QUIT
        app.key_command(ord('a'), 'a')
        self.assertEqual(len(app.sheets), 1)
        self.assertEqual(app.mode, MODE_QUIT)
        app.key_command(ord('n'), 'n')
        self.assertEqual(len(app.sheets), 1)
        self.assertEqual(app.mode, MODE_NORMAL)
        app.mode = MODE_QUIT
        app.key_command(ord('y'), 'y')
        self.assertEqual(len(app.sheets), 0)
        self.assertEqual(app.mode, MODE_EXIT)

    def test_key_command_other(self):
        app = App()
        app.mode = MODE_EXIT
        app.key_command(ord('a'), 'a')

    def test_open_file(self):
        app = App()
        app.string_buffer = 'unsupported.format'
        app.open_file()
        self.assertEqual(len(app.sheets), 1)
        self.assertEqual(app.sheet.title, None)
        app.string_buffer = 'new.csv'
        app.open_file()
        self.assertEqual(len(app.sheets), 1)
        self.assertEqual(app.sheet.title, 'new.csv')
        with open('old.csv', 'w') as f:
            f.write('a,b,c')
        app.string_buffer = 'old.csv'
        app.open_file()
        os.remove('old.csv')
        self.assertEqual(len(app.sheets), 2)
        self.assertEqual(app.sheet.title, 'old.csv')
        self.assertEqual(app.sheet, app.sheets[1])
        with open('inaccessible.csv', 'w') as f:
            f.write('d,e,f')
        os.chmod('inaccessible.csv', 0o222)
        app.string_buffer = 'inaccessible.csv'
        app.open_file()
        os.remove('inaccessible.csv')
        self.assertEqual(len(app.sheets), 2)
        self.assertEqual(app.sheet.title, 'old.csv')

    def test_save_file(self):
        app = App()
        app.string_buffer = 'unsupported.format'
        app.save_file()
        self.assertEqual(os.path.isfile('unsupported.format'), False)
        app.string_buffer = 'save.csv'
        app.save_file()
        self.assertEqual(os.path.isfile('save.csv'), True)
        os.remove('save.csv')
        app.string_buffer = '/inaccessible.csv'
        app.save_file()
