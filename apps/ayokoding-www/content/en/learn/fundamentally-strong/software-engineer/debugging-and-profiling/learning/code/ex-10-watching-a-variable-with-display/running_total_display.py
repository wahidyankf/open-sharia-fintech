"""Example 10: Watching a Variable with display."""

from __future__ import annotations


def running_total(values: list[int]) -> int:
    total = 0
    for n in values:
        total += n
    return total


if __name__ == "__main__":
    print(running_total([10, 20, 30]))
