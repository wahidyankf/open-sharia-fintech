"""Example 37: A Frozen Dataclass Is Hashable by Default."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(
    frozen=True
)  # => frozen=True (with the default eq=True) auto-generates __hash__ too
class Point:  # => begins the Point class body
    x: int  # => a required dataclass field, part of the generated __init__
    y: int  # => a required dataclass field, part of the generated __init__


lookup: dict[Point, str] = {
    Point(1, 2): "origin-ish"
}  # => works as a dict key -- it is hashable
members: set[Point] = {
    Point(1, 2),
    Point(1, 2),
}  # => equal frozen instances deduplicate
print(
    lookup[Point(1, 2)], len(members)
)  # => a NEW equal Point still finds the same entry
# => Output: origin-ish 1
# => `@dataclass(frozen=True)` is the shortest path to a fully correct, hashable value object
