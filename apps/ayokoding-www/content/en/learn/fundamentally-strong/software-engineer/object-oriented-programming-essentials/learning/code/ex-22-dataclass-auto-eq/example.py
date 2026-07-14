"""Example 22: A Dataclass's Auto-Generated __eq__."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass  # => generates __eq__ that compares EVERY field, field by field
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => a required dataclass field, part of the generated __init__


a: Point = Point(1, 2)  # => constructs a
b: Point = Point(1, 2)  # => a distinct object, but equal field values
print(
    a == b, a is b
)  # => == is True by VALUE; is remains False -- two different objects
# => Output: True False
# => A bare `@dataclass` gives value equality automatically
