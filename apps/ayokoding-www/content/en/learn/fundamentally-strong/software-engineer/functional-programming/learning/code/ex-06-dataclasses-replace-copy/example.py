"""Example 6: dataclasses.replace Produces a New Record."""

from dataclasses import (
    dataclass,
    replace,
)  # => replace: a shallow copy with fields overridden


@dataclass(
    frozen=True
)  # => frozen so "updating" MUST go through replace, not assignment
class Point:  # => the value object replace() will copy-with-overrides below
    x: int  # => first field -- the one this example overrides via replace
    y: int  # => second field -- left untouched, copied straight through by replace


original = Point(1, 2)  # => the record we will "update" without mutating
moved = replace(
    original, x=99
)  # => builds a NEW Point: x overridden, y copied unchanged
# => original itself is never touched by replace -- it only READS original's fields

print(original)  # => Output: Point(x=1, y=2) -- untouched
print(moved)  # => Output: Point(x=99, y=2) -- a distinct object with the new x
print(original == moved)  # => Output: False -- two different values now
print(original is moved)  # => Output: False -- two different objects, not aliases
