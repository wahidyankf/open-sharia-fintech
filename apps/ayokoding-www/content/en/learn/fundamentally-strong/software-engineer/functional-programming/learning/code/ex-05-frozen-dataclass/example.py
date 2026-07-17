"""Example 5: A Frozen Dataclass Rejects Mutation."""

from dataclasses import (
    FrozenInstanceError,
    dataclass,
)  # => frozen=True raises this on assignment


@dataclass(
    frozen=True
)  # => generates __init__/__repr__/__eq__ AND blocks attribute assignment
class Point:  # => an immutable value object -- once built, it cannot change
    x: int  # => a regular field, just frozen at the class level
    y: int  # => a second field -- @dataclass generates __init__(self, x, y) from both


p = Point(1, 2)  # => __init__ is allowed to set fields ONCE, during construction
print(p)  # => Output: Point(x=1, y=2)

try:  # => opens a block that expects the assignment below to raise
    p.x = 99  # type: ignore[misc]  # => any LATER assignment is rejected, not just during init
    raised = False  # => unreachable if FrozenInstanceError fires first, kept for completeness
except FrozenInstanceError:  # => the frozen dataclass's own guard fired
    raised = True  # => confirms mutation was actually blocked, not silently ignored
print(raised)  # => Output: True
print(p)  # => Output: Point(x=1, y=2) -- still the original values
