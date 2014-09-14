import os
import unittest

from vcii.format_csv import *
from vcii.sheet import Sheet


FILENAME = 'TEST.csv'

TEST_TEXT = """
a,2,,delta
two words,,"a, comma",
""".lstrip()


class TestFormatCSV(unittest.TestCase):

    def test_default_dialect(self):
        with open(FILENAME, 'w') as f:
            f.write('')
        sheet = read(FILENAME)
        self.assertEqual(sheet.size, (0, 0))

    def test_read(self):
        with open(FILENAME, 'w') as f:
            f.write(TEST_TEXT)
        sheet = read(FILENAME)
        self.assertEqual(sheet.cells[0][0].content, 'a')
        self.assertEqual(sheet.cells[1][0].content, '2')
        self.assertEqual(sheet.cells[2][0].content, '')
        self.assertEqual(sheet.cells[3][0].content, 'delta')
        self.assertEqual(sheet.cells[0][1].content, 'two words')
        self.assertEqual(sheet.cells[1][1].content, '')
        self.assertEqual(sheet.cells[2][1].content, 'a, comma')
        self.assertEqual(sheet.cells[3][1].content, '')
        os.remove(FILENAME)

    def test_write(self):
        sheet = Sheet()
        sheet.append('a')
        sheet.cursor = [1, 0]
        sheet.append('2')
        sheet.cursor = [3, 0]
        sheet.append('delta')
        sheet.cursor = [0, 1]
        sheet.append('two words')
        sheet.cursor = [2, 1]
        sheet.append('a, comma')
        write(sheet, FILENAME)
        with open(FILENAME) as f:
            self.assertEqual(f.read(), TEST_TEXT)
        os.remove(FILENAME)
