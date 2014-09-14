import curses
import random
import unittest

import vcii.sheet as sheet
from vcii.display import *


class TestDisplay(unittest.TestCase):

    def setUp(self):
        self.sheets = [sheet.Sheet(), sheet.Sheet()]
        self.window = curses.initscr()

    def tearDown(self):
        curses.endwin()

    def test_draw(self):
        draw(self.window, self.sheets, self.sheets[0])

    def test_draw_tab_line(self):
        draw_tab_line(self.window, self.sheets, self.sheets[1])
        self.sheets += [sheet.Sheet() for i in range(100)]
        draw_tab_line(self.window, self.sheets, self.sheets[0])

    def test_draw_cells(self):
        for i in range(10):
            self.sheets[0].cursor = [(lambda: random.randint(0, 100))()] * 2
            self.sheets[0].append('x')
        draw_cells(self.window, self.sheets[0])

    def test_label_for_column(self):
        self.assertEqual(label_for_column(0), 'A')
        self.assertEqual(label_for_column(25), 'Z')
        self.assertEqual(label_for_column(51), 'AZ')
        self.assertEqual(label_for_column(676), 'ZA')

    def test_set_cursor(self):
        set_cursor(self.window, self.sheets[0])
        self.sheets[0].cursor = [100, 0]
        set_cursor(self.window, self.sheets[0])
        self.sheets[0].cursor = [0, 100]
        set_cursor(self.window, self.sheets[0])
