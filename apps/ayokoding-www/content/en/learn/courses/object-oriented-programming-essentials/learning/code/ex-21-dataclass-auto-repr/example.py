"""Example 21: A Dataclass's Auto-Generated __repr__."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass  # => generates __repr__ too -- no hand-written __repr__ anywhere in this file
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => a required dataclass field, part of the generated __init__


p: Point = Point(1, 2)  # => constructs p
print(repr(p))  # => the generated __repr__ names every field explicitly
# => Output: Point(x=1, y=2)
# => `@dataclass`'s generated `__repr__` always shows `ClassName(field=value, ...)` for every declared field, in declaration order
