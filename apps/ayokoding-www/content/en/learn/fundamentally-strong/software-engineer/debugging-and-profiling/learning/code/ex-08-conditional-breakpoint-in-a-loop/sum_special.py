"""Example 8: A Conditional Breakpoint in a Loop."""

from __future__ import annotations


def sum_special(n: int) -> int:
    total = 0
    for i in range(n):
        total += i
    return total


if __name__ == "__main__":
    print(sum_special(100))
