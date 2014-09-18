import unittest

from vcii.edit import *


class TestApp(unittest.TestCase):

    def test_cursor_left(self):
        self.assertEqual(cursor_left('hi', 0), ('hi', 0))
        self.assertEqual(cursor_left('hi', 2), ('hi', 1))

    def test_cursor_right(self):
        self.assertEqual(cursor_right('hi', 0), ('hi', 1))
        self.assertEqual(cursor_right('hi', 2), ('hi', 2))

    def test_home(self):
        self.assertEqual(home('hi', 0), ('hi', 0))
        self.assertEqual(home('hi', 2), ('hi', 0))

    def test_end(self):
        self.assertEqual(end('hi', 0), ('hi', 2))
        self.assertEqual(end('hi', 2), ('hi', 2))

    def test_delete(self):
        self.assertEqual(delete('hi', 0), ('i', 0))
        self.assertEqual(delete('hi', 2), ('hi', 2))

    def test_rubout(self):
        self.assertEqual(rubout('hi', 0), ('hi', 0))
        self.assertEqual(rubout('hi', 2), ('h', 1))

    def test_rubout_word(self):
        self.assertEqual(rubout_word('hi', 0), ('hi', 0))
        self.assertEqual(rubout_word('hi', 2), ('', 0))
        self.assertEqual(rubout_word('hi there', 2), (' there', 0))
        self.assertEqual(rubout_word('hi there', 8), ('hi ', 3))
        self.assertEqual(rubout_word('hi there', 6), ('hi re', 3))
        self.assertEqual(rubout_word('hi there  sir', 10), ('hi sir', 3))

    def test_kill_line(self):
        self.assertEqual(kill_line('hi', 0), ('', 0))
        self.assertEqual(kill_line('hi', 2), ('hi', 2))

    def test_backward_kill_line(self):
        self.assertEqual(backward_kill_line('hi', 0), ('hi', 0))
        self.assertEqual(backward_kill_line('hi', 2), ('', 0))

    def test_tab_complete(self):
        self.assertEqual(tab_complete('READ', 4), ('README.txt', 10))
        self.assertEqual(tab_complete('READ', 3), ('README.txtD', 10))
        self.assertEqual(tab_complete('bin', 3), ('bin/', 4))
        self.assertEqual(tab_complete('bin/', 4), ('bin/vcii', 8))
        self.assertEqual(tab_complete('nonmatch', 8), ('nonmatch', 8))
        self.assertEqual(tab_complete('fake/dir', 8), ('fake/dir', 8))
