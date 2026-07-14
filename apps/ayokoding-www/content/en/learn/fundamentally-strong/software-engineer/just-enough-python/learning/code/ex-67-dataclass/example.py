"""Example 67: dataclass."""

# @dataclass auto-generates __init__ and __repr__ from the annotated fields below.
from dataclasses import dataclass  # => imports the decorator that generates boilerplate


@dataclass  # => applies the decorator to the class defined right below it
class Point:  # => defines a plain data-holder class
    x: int  # => declares a field named x, typed int
    y: int  # => declares a field named y, typed int


print(Point(1, 2))  # => Output: Point(x=1, y=2) -- no __repr__ written by hand
