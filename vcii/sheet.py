import re

DEFAULT_COLUMN_WIDTH = 10

CELL_ID_PATTERN = re.compile(r'([a-zA-Z]+)(\d+)')


def indices_from_label(label):
    match = CELL_ID_PATTERN.fullmatch(label)
    if not match:
        raise ValueError

    column = 0
    for i, ch in enumerate(reversed(match.group(1))):
        ord_a = 65 if ch.isupper() else 97
        column += (ord(ch) - ord_a + (1 if i > 0 else 0)) * (26 ** i)
    row = int(match.group(2)) - 1

    return (column, row)


class Cell:

    def __init__(self, content=''):
        self.content = content


class Sheet:

    def __init__(self):
        self.column_widths = []
        self.row_heights = []
        self.cells = []
        self.scroll = [0, 0]
        self.cursor = [0, 0]
        self.text_cursor = 0
        self.title = None
        self.modified = False
        self.status = None

    @property
    def num_columns(self):
        return len(self.column_widths)

    @property
    def num_rows(self):
        return len(self.row_heights)

    @property
    def size(self):
        return len(self.column_widths), len(self.row_heights)

    @property
    def ui_title(self):
        return self.title if self.title else '[No name]'

    def expand(self, x, y):
        while x >= self.num_columns:
            self.cells.append([Cell() for i in range(self.num_rows)])
            self.column_widths.append(DEFAULT_COLUMN_WIDTH)
            self.modified = True
        while y >= self.num_rows:
            for column in self.cells:
                column.append(Cell())
            self.row_heights.append(1)
            self.modified = True

    def expand_to_cursor(self):
        self.expand(self.cursor[0], self.cursor[1])

    def __setitem__(self, key, value):
        indices = indices_from_label(key)
        self.expand(indices[0], indices[1])
        self.cells[indices[0]][indices[1]].content = str(value)
        self.modified = True

    @property
    def active_cell(self):
        return self.cells[self.cursor[0]][self.cursor[1]]

    def append(self, text):
        self.expand_to_cursor()
        self.active_cell.content += text
        self.text_cursor = len(self.active_cell.content)
        self.modified = True

    def backspace(self):
        if self.cursor_in_bounds():
            if len(self.active_cell.content) > 0:
                self.modified = True
            self.active_cell.content = self.active_cell.content[:-1]
            self.text_cursor = len(self.active_cell.content)

    def cursor_in_bounds(self):
        return (
            self.cursor[0] < self.num_columns and
            self.cursor[1] < self.num_rows
        )

    def move_cursor(self, x_offset, y_offset):
        self.cursor[0] = max(0, self.cursor[0] + x_offset)
        self.cursor[1] = max(0, self.cursor[1] + y_offset)
        if self.cursor_in_bounds():
            self.text_cursor = len(self.active_cell.content)
        else:
            self.text_cursor = 0

    def column_width(self, index):
        if index < self.num_columns:
            return self.column_widths[index]
        return DEFAULT_COLUMN_WIDTH

    def resize_column(self, column, row):
        self.expand(column, row)
        self.column_widths[column] = len(self.cells[column][row].content) + 2
