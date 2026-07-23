"""Example 24: default_factory for a Mutable Default."""

from dataclasses import (
    dataclass,
    field,
)  # => field() lets a mutable default be per-instance


@dataclass  # => generates boilerplate methods from the field list below
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => a required dataclass field, part of the generated __init__
    tags: list[str] = field(
        default_factory=list
    )  # => calls list() FRESH for every instance
    # => a bare `tags: list[str] = []` would raise ValueError -- @dataclass forbids it outright


a: Point = Point(1, 2)  # => constructs a
b: Point = Point(3, 4)  # => constructs b
a.tags.append("origin")  # => mutates ONLY a's own list
print(
    a.tags, b.tags
)  # => b's list is untouched -- proves each instance got its own list
# => Output: ['origin'] []
# => `field(default_factory=list)` calls the factory function once per instance construction
