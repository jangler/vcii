import random
import unittest

from vcii.sheet import *


class TestSheet(unittest.TestCase):

    def test_key_to_indices(self):
        with self.assertRaises(ValueError):
            indices_from_label('1A')
        self.assertEqual(indices_from_label('A1'), (0, 0))
        self.assertEqual(indices_from_label('zz99'), (26**2 + 25, 98))

    def test_append(self):
        sheet = Sheet()
        sheet.cursor = [(lambda: random.randint(0, 10))()] * 2
        sheet.append('rain')
        self.assertEqual(sheet.active_cell.content, 'rain')
        self.assertTrue(sheet.modified)
        sheet.modified = False
        sheet.append('bow')
        self.assertEqual(sheet.active_cell.content, 'rainbow')
        self.assertTrue(sheet.modified)

    def test_backspace(self):
        sheet = Sheet()
        sheet.cursor = [(lambda: random.randint(0, 10))()] * 2
        sheet.backspace()
        self.assertFalse(sheet.modified)
        sheet.append('xy')
        sheet.modified = False
        sheet.backspace()
        self.assertEqual(sheet.active_cell.content, 'x')
        self.assertTrue(sheet.modified)
        sheet.backspace()
        self.assertEqual(sheet.active_cell.content, '')
        sheet.modified = False
        sheet.backspace()
        self.assertEqual(sheet.active_cell.content, '')
        self.assertFalse(sheet.modified)

    def test_expand(self):
        sheet = Sheet()
        self.assertEqual(sheet.size, (0, 0))
        max_size = 0, 0
        for i in range(10):
            coords = [(lambda: random.randint(0, 10))()] * 2
            sheet.expand(*coords)
            max_size = tuple(max(max_size[j], coords[j] + 1) for j in range(2))
            self.assertEqual(sheet.size, max_size)
            self.assertTrue(sheet.modified)

    def test_setitem(self):
        sheet = Sheet()
        sheet['C2'] = 'testing'
        self.assertEqual(sheet.cells[2][1].content, 'testing')
        self.assertEqual(sheet.size, (3, 2))
        self.assertTrue(sheet.modified)

    def test_move_cursor(self):
        sheet = Sheet()
        sheet.move_cursor(0, 0)
        self.assertEqual(sheet.cursor, [0, 0])
        sheet.move_cursor(-1, 1)
        self.assertEqual(sheet.cursor, [0, 1])
        sheet.move_cursor(1, -2)
        self.assertEqual(sheet.cursor, [1, 0])
        self.assertFalse(sheet.modified)
        sheet.expand(0, 0)
        sheet.modified = False
        sheet.move_cursor(-1, 0)
        self.assertEqual(sheet.cursor, [0, 0])
        self.assertFalse(sheet.modified)

    def test_column_width(self):
        sheet = Sheet()
        sheet.expand(1, 0)
        self.assertEqual(sheet.column_width(1), DEFAULT_COLUMN_WIDTH)
        self.assertEqual(sheet.column_width(2), DEFAULT_COLUMN_WIDTH)
        sheet.column_widths[1] = 5
        self.assertEqual(sheet.column_width(0), DEFAULT_COLUMN_WIDTH)
        self.assertEqual(sheet.column_width(1), 5)
