"""Example 1: First Breakpoint with breakpoint()."""

from __future__ import annotations


def running_total(
    values: list[int],
) -> int:  # => co-01: the function this example steps through
    """Sum values one at a time -- seeded bug: subtracts instead of adds when a value is 3."""
    total = 0  # => the accumulator -- watch this value at each breakpoint() stop
    for (
        n
    ) in values:  # => co-01: ONE breakpoint() inside a loop fires once PER iteration
        breakpoint()  # => co-01: pauses HERE, before either branch runs -- next: `p n, total`
        if n == 3:  # => the ONE iteration that takes the buggy branch below
            total = (
                total - n
            )  # seeded bug: should be total + n, like every other branch
        else:
            total = total + n  # => the correct branch every other value takes
    return total


if __name__ == "__main__":
    print(
        running_total([1, 2, 3, 4])
    )  # => co-01: expected 10, actual 4 -- the bug breakpoint() reveals
