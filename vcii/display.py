import curses


SHORTCUTS = {
    '^X': 'Exit',
}


def draw(window, sheets, current_sheet):
    window.erase()
    draw_tab_line(window, sheets, current_sheet)
    draw_row_and_column_labels(window, current_sheet)
    draw_cells(window, current_sheet)
    draw_status_line(window)
    draw_shortcut_lines(window)
    window.refresh()
    set_cursor(window, current_sheet)


def draw_tab_line(window, sheets, current_sheet):
    max_x = window.getmaxyx()[1]
    max_len = max_x // len(sheets) - 4
    x = 0
    for sheet in sheets:
        format_str = ' + {} ' if sheet.modified else ' {} '
        title = sheet.title if sheet.title else '[No Name]'
        title = title[-max_len:]
        tab_label = format_str.format(title)[0:max_x - x]
        attr = curses.A_REVERSE if sheet == current_sheet else curses.A_NORMAL
        if x < max_x:
            window.addstr(0, x, tab_label, attr)
        x += len(tab_label)


def draw_row_and_column_labels(window, sheet):
    max_y, max_x = window.getmaxyx()
    max_y -= 3
    margin = get_margin(window, sheet)
    for y in range(2, max_y):
        window.addstr(y, 0, str(y - 1).ljust(margin - 1), curses.A_REVERSE)
    column_header = ' ' * margin
    i = 0
    while len(column_header) < max_x:
        column_header += label_for_column(i).center(sheet.column_width(i))
        i += 1
    window.addstr(1, 0, column_header[:max_x], curses.A_REVERSE)


def draw_cells(window, sheet):
    max_y, max_x = window.getmaxyx()
    max_y -= 3
    x = get_margin(window, sheet)
    for column_index, column in enumerate(sheet.cells):
        y = 2
        for row_index, cell in enumerate(column):
            if y < max_y and x < max_x:
                window.addstr(y, x, cell.content[:max_x - x])
            y += sheet.row_heights[row_index]
        x += sheet.column_widths[column_index]


def draw_status_line(window):
    max_y, max_x = window.getmaxyx()
    status = 'Testing status line'
    text = '[ {} ]'.format(status)
    window.addstr(max_y - 3, max_x // 2 - len(text) // 2, text,
                  curses.A_REVERSE)


def draw_shortcut_lines(window):
    max_y, max_x = window.getmaxyx()
    width = max_x // max(1, len(SHORTCUTS) // 2)
    y = max_y - 2
    x = 0
    for key, value in SHORTCUTS.items():
        window.addstr(y, x, key, curses.A_REVERSE)
        window.addstr(y, x + 3, value)
        y = (y + 1) % 2
        x = x + width if y == 0 else x


def get_margin(window, sheet):
    return len(str(window.getmaxyx()[0] - 5)) + 1


def label_for_column(index):
    label = ''
    while index > 0 or len(label) == 0:
        index_offset = 1 if len(label) > 0 else 0
        label = chr(65 + (index - index_offset) % 26) + label
        if len(label) > 1:
            index -= 1
        index //= 26
    return label


def set_cursor(window, sheet):
    max_y, max_x = window.getmaxyx()
    margin = get_margin(window, sheet)
    cursor_y = sheet.cursor[1] + 2
    cursor_x = (sheet.text_cursor + margin +
                sum(sheet.column_width(i) for i in range(sheet.cursor[0])))
    window.move(min(max_y - 4, cursor_y), min(max_x - 1, cursor_x))
