"""Example 20: A Basic Dataclass."""

from dataclasses import (
    dataclass,
)  # => imports the decorator that generates boilerplate methods


@dataclass  # => auto-generates __init__, __repr__, and __eq__ from the fields below
class Point:  # => begins the Point class body
    x: int  # => a required positional/keyword field
    y: int  # => a second required field


p: Point = Point(1, 2)  # => the auto-generated __init__ accepts fields positionally
print(p.x, p.y)  # => confirms both fields were actually set by the generated __init__
# => Output: 1 2
# => `@dataclass` turns typed field declarations into a working `__init__`, `__repr__`, and `__eq__` with no hand-written method bodies
