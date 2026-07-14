"""Example 64: app.util -- a small helper imported by app.__main__."""


def shout(text: str) -> str:  # => a plain typed function, no dependency on __main__
    return text.upper() + "!"  # => uppercases text and appends an exclamation mark
