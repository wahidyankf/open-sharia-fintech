"""Example 6: pytest verification for dataclasses.replace Produces a New Record."""

from dataclasses import replace

from example import Point


def test_replace_leaves_original_untouched() -> None:
    original = Point(1, 2)
    moved = replace(original, x=99)  # => a NEW record, y copied unchanged
    assert original == Point(1, 2)  # => original never mutated
    assert moved == Point(99, 2)  # => new record has the overridden field
    assert original is not moved  # => two distinct objects


# => Run: pytest -- Output: 1 passed
