import curses

from vcii.app import MODE_OPEN, MODE_QUIT, MODE_SAVE


SHORTCUTS_NORMAL = (
    ('^Q', 'Quit'),
    ('^T', 'Tab over'),
    ('^O', 'Open'),
    ('^S', 'Save'),
)
SHORTCUTS_INPUT = (
    ('^C', 'Cancel'),
)
SHORTCUTS_YESNO = (
    ('Y', 'Yes'),
    ('N', 'No'),
)


def cursor_bounds(window, sheet):
    maxyx = window.getmaxyx()
    margin = len(str(sheet.scroll[1] + window.getmaxyx()[0] - 5)) + 1
    return (margin, 2), (maxyx[1] - 1, maxyx[0] - 4)


def cursor_coordinates(window, sheet):
    margin = cursor_bounds(window, sheet)[0][0]
    cursor_y = sheet.cursor[1] + 2 - sheet.scroll[1]
    if sheet.cursor[0] >= sheet.scroll[0]:
        cursor_x = (sheet.text_cursor + margin +
                    sum(sheet.column_width(i)
                        for i in range(sheet.scroll[0], sheet.cursor[0])))
    else:
        cursor_x = -1
    return cursor_x, cursor_y


def draw(window, sheets, current_sheet, mode):
    window.erase()
    draw_tab_line(window, sheets, current_sheet)
    scroll_sheet(window, current_sheet)
    draw_row_and_column_labels(window, current_sheet)
    draw_cells(window, current_sheet)
    draw_status_line(window, current_sheet)
    draw_shortcut_lines(window, mode)
    window.refresh()
    set_cursor(window, current_sheet)


def draw_tab_line(window, sheets, current_sheet):
    max_x = window.getmaxyx()[1]
    max_len = max_x // len(sheets) - 4
    x = 0
    for sheet in sheets:
        format_str = ' + {} ' if sheet.modified else ' {} '
        title = sheet.ui_title[-max_len:]
        tab_label = format_str.format(title)[0:max_x - x]
        attr = curses.A_REVERSE if sheet == current_sheet else curses.A_NORMAL
        if x < max_x:
            window.addstr(0, x, tab_label, attr)
        x += len(tab_label)


def draw_row_and_column_labels(window, sheet):
    bounds = cursor_bounds(window, sheet)
    for y in range(bounds[0][1], bounds[1][1] + 1):
        window.addstr(y, 0,
                      str(y - 1 + sheet.scroll[1]).ljust(bounds[0][0] - 1),
                      curses.A_REVERSE)
    column_header = ' ' * bounds[0][0]
    i = sheet.scroll[0]
    while len(column_header) < bounds[1][0]:
        column_header += label_for_column(i).center(sheet.column_width(i))
        i += 1
    window.addstr(1, 0, column_header[:bounds[1][0] + 1], curses.A_REVERSE)


def draw_cells(window, sheet):
    bounds = cursor_bounds(window, sheet)
    x = bounds[0][0]
    for column_index in range(sheet.scroll[0], sheet.size[0]):
        y = 2
        for row_index in range(sheet.scroll[1], sheet.size[1]):
            if y <= bounds[1][1] and x <= bounds[1][0]:
                cell = sheet.cells[column_index][row_index]
                window.addstr(y, x, cell.content[:bounds[1][0] + 1 - x])
            y += sheet.row_heights[row_index]
        x += sheet.column_widths[column_index]


def draw_status_line(window, sheet):
    if sheet.status:
        max_y, max_x = window.getmaxyx()
        text = '[ {} ]'.format(sheet.status)
        window.addstr(max_y - 3, max(0, max_x // 2 - len(text) // 2),
                      text[:max_x], curses.A_REVERSE)


def draw_shortcut_lines(window, mode):
    max_y, max_x = window.getmaxyx()
    shortcuts = SHORTCUTS_NORMAL
    if mode in (MODE_OPEN, MODE_SAVE):
        shortcuts = SHORTCUTS_INPUT
    elif mode == MODE_QUIT:
        shortcuts = SHORTCUTS_YESNO
    width = max_x // ((len(shortcuts) + 1) // 2)
    key_width = max(len(x[0]) for x in shortcuts) + 1
    y = 0
    x = 0
    for key, value in shortcuts:
        window.addstr(max_y - 2 + y, x, key, curses.A_REVERSE)
        window.addstr(max_y - 2 + y, x + key_width, value)
        y = (y + 1) % 2
        x = x + width if y == 0 else x


def label_for_column(index):
    label = ''
    while index > 0 or len(label) == 0:
        index_offset = 1 if len(label) > 0 else 0
        label = chr(65 + (index - index_offset) % 26) + label
        if len(label) > 1:
            index -= 1
        index //= 26
    return label


def scroll_sheet(window, sheet):
    cursor = cursor_coordinates(window, sheet)
    bounds = cursor_bounds(window, sheet)
    for i in range(2):
        while cursor[i] < bounds[0][i]:
            sheet.scroll[i] -= 1
            cursor = cursor_coordinates(window, sheet)
        while cursor[i] > bounds[1][i]:
            sheet.scroll[i] += 1
            cursor = cursor_coordinates(window, sheet)


def set_cursor(window, sheet):
    max_y, max_x = window.getmaxyx()
    margin = cursor_bounds(window, sheet)[0][0]
    cursor_x, cursor_y = cursor_coordinates(window, sheet)
    window.move(min(max_y - 4, cursor_y), min(max_x - 1, cursor_x))
