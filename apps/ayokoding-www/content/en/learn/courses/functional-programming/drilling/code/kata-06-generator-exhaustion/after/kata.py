"""Kata 6 (after): fix -- materialize a list when the SAME data is genuinely needed more than once."""

from typing import Iterator


def squared(nums: list[int]) -> Iterator[int]:
    for n in nums:
        yield n * n


values = list(
    squared([1, 2, 3])
)  # => a list, not a generator -- safe to iterate as many times as needed
total = sum(values)  # first pass over the materialized list
print(total)
remaining = list(
    values
)  # second pass -- the list still has every element, nothing was consumed
print(remaining)
