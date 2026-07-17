"""Example 38: A Lazy map/filter Pipeline Pulled by next."""

from typing import Iterator  # => Iterator types the lazy generator below

pulled_from_source: list[
    int
] = []  # => tracks exactly which SOURCE values were ever touched


def logged_source() -> Iterator[
    int
]:  # => a generator that records every value it produces
    for n in range(1, 1000):  # => a LARGE range -- but nothing runs until pulled
        pulled_from_source.append(
            n
        )  # => only executes when this generator is actually advanced
        yield n  # => suspends here until the consumer pulls the NEXT value


doubled = map(
    lambda n: n * 2, logged_source()
)  # => LAZY: wraps the source, still nothing runs
evens_only = filter(
    lambda n: n % 4 == 0, doubled
)  # => LAZY: a second lazy stage on top of the first

first_three = [
    next(evens_only),
    next(evens_only),
    next(evens_only),
]  # => pulls JUST enough

# => laziness (co-15) means the pipeline computes ONLY what the caller demands
print(first_three)  # => Output: [4, 8, 12]
print(
    len(pulled_from_source) < 10
)  # => Output: True -- far fewer than 999 source values were touched
