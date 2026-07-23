"""Example 38: eq=False Falls Back to Identity Equality."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(
    eq=False
)  # => suppresses the generated __eq__ entirely -- object's default is used
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => a required dataclass field, part of the generated __init__


a: Point = Point(1, 2)  # => constructs a
b: Point = Point(1, 2)  # => equal field values, but no __eq__ was generated
print(a == b, a == a)  # => identity is the only equality left: only a == a is True
# => Output: False True
# => `eq=False` is the escape hatch when a dataclass genuinely needs identity semantics
