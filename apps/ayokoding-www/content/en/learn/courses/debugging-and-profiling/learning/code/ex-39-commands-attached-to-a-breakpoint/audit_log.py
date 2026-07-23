"""Example 39: commands Attached to a Breakpoint."""

from __future__ import annotations


def audit(entry: int) -> int:
    return entry * 2


if __name__ == "__main__":
    for entry in range(10):
        audit(entry)
    print("done")
