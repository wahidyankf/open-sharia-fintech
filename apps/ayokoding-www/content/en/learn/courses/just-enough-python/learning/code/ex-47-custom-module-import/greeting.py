"""Example 47: sibling module -- greeting.py, imported by example.py."""


def shout(name: str) -> str:  # => a typed, importable function -- no name guard needed
    return f"HELLO, {name.upper()}!"  # => uppercases name and wraps it in HELLO, ...!
