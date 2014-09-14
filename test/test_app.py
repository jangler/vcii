import curses
import unittest

from vcii.app import *


class TestApp(unittest.TestCase):

    def setUp(self):
        self.window = curses.initscr()

    def tearDown(self):
        curses.endwin()

    def test_key_command(self):
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
        app.key_command(None, 'unknown')
        self.assertFalse(app.key_command(None, '^X'))
