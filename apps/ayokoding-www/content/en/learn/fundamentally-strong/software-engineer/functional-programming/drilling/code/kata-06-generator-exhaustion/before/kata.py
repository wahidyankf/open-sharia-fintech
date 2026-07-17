"""Kata 6 (before): a generator is iterated once, exhausted, then silently yields nothing again."""

from typing import Iterator


def squared(nums: list[int]) -> Iterator[int]:
    for n in nums:
        yield (
            n * n
        )  # => a lazy, single-use generator -- each value produced only on demand


values = squared(
    [1, 2, 3]
)  # SMELL: ONE generator object, about to be consumed twice below
total = sum(values)  # first pass -- fully consumes/exhausts the generator
print(total)
remaining = list(
    values
)  # BUG: the SAME exhausted generator -- nothing left to yield, no error raised
print(remaining)
