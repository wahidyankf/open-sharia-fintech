"""Example 36: A Frozen Dataclass Rejects Field Assignment."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(frozen=True)  # => frozen=True makes every field read-only after construction
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => a required dataclass field, part of the generated __init__


p: Point = Point(1, 2)  # => constructs p
try:  # => the block below is expected to raise
    p.x = 99  # type: ignore  # => assignment to a frozen field always raises (static checkers also flag it as read-only)
except (
    Exception
) as exc:  # => dataclasses.FrozenInstanceError, a subclass of AttributeError
    print(type(exc).__name__)  # => confirms the exact exception type raised
# => Output: FrozenInstanceError
# => `dataclasses.FrozenInstanceError` (a subclass of `AttributeError`) fires on every attempted field assignment after construction
