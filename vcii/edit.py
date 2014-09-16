# Module containing text editing functions. Each function takes the
# current string and cursor position as arguments, and returns the
# resulting string and cursor position.


def cursor_left(text, cursor):
    return text, max(0, cursor - 1)


def cursor_right(text, cursor):
    return text, min(len(text), cursor + 1)


def home(text, cursor):
    return text, 0


def end(text, cursor):
    return text, len(text)


def delete(text, cursor):
    return text[:cursor] + text[cursor + 1:], cursor


def rubout(text, cursor):
    return delete(text, cursor - 1) if cursor > 0 else (text, cursor)


def rubout_word(text, cursor):
    for check in (lambda ch: ch == ' ', lambda ch: ch != ' '):
        while cursor > 0 and check(text[cursor - 1]):
            text, cursor = rubout(text, cursor)
    return text, cursor


def kill_line(text, cursor):
    return text[:cursor], cursor


def backward_kill_line(text, cursor):
    return text[cursor:], 0


KEYS = {
    'KEY_LEFT': cursor_left,
    'KEY_RIGHT': cursor_right,
    'KEY_HOME': home,
    'KEY_END': end,
    'KEY_BACKSPACE': rubout,
    'KEY_DC': delete,
    '^A': home,
    '^B': cursor_left,
    '^D': delete,
    '^E': end,
    '^F': cursor_right,
    '^H': rubout,
    '^K': kill_line,
    '^U': backward_kill_line,
    '^W': rubout_word,
}
