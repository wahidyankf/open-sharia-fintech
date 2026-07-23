"""Example 78: A Case Where Laziness Saves Work, and One Where It Hides a Cost."""

from typing import Iterator  # => Iterator types the lazy generator below

work_done: list[str] = []  # => records every "expensive" step actually performed


def expensive_step(n: int) -> int:  # => stands in for a slow computation
    work_done.append(f"computed {n}")  # => only runs when this step is ACTUALLY reached
    return n * n  # => the "expensive" result


def lazy_squares(numbers: range) -> Iterator[int]:  # => LAZY: nothing runs until pulled
    for n in numbers:  # => walks the range one value at a time, on demand
        yield expensive_step(n)  # => suspends here between pulls


def eager_squares(
    numbers: range,
) -> list[int]:  # => EAGER: computes EVERY value immediately
    return [
        expensive_step(n) for n in numbers
    ]  # => materializes the WHOLE list before returning


work_done.clear()  # => resets the log before Case 1
lazy_stream = lazy_squares(range(1, 1000))  # => nothing computed yet
first_over_50 = next(
    n for n in lazy_stream if n > 50
)  # => stops pulling the instant it finds one
lazy_work_count = len(work_done)  # => far fewer than 999

work_done.clear()  # => resets the log before Case 2
lazy_stream_2 = lazy_squares(range(1, 4))  # => a FRESH lazy generator
first_pass = list(lazy_stream_2)  # => first pass: 3 values computed
second_pass = list(
    lazy_stream_2
)  # => generator already EXHAUSTED -- silently yields nothing
hidden_cost_count = len(
    work_done
)  # => still 3, NOT 6 -- the second pass did nothing at all, silently

# => laziness is a trade-off, not a free win -- both sides of it matter
print(first_over_50)  # => Output: 64
print(
    lazy_work_count < 10
)  # => Output: True -- laziness saved most of the 999 possible computations
print(
    second_pass
)  # => Output: [] -- the SILENT trap: re-iterating an exhausted generator gives nothing
print(
    hidden_cost_count
)  # => Output: 3 -- proves the second pass computed NOTHING, not that it recomputed
