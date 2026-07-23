"""Example 39: slots=True Drops Per-Instance __dict__."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(
    slots=True
)  # => added in Python 3.10 -- generates __slots__ from the field list
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => a required dataclass field, part of the generated __init__


p: Point = Point(1, 2)  # => constructs p
print(hasattr(p, "__dict__"))  # => slots instances have NO per-instance __dict__ at all
# => Output: False
try:  # => the block below is expected to raise
    p.z = 3  # type: ignore  # => z was never declared as a field -- slots rejects undeclared attributes (static checkers flag it too)
except AttributeError as exc:  # => catches the AttributeError raised above
    print(type(exc).__name__)  # => confirms the exact exception type
# => Output: AttributeError
# => `slots=True` trades attribute flexibility for a smaller memory footprint per instance
