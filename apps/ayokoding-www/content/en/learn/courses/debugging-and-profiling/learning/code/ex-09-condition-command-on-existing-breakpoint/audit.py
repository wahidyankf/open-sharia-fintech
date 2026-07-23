"""Example 9: The condition Command on an Existing Breakpoint."""

from __future__ import annotations


def audit_value(x: int) -> int:
    processed = x * 2
    return processed


if __name__ == "__main__":
    for v in [5, 10, -3, 8, -1, 2]:
        audit_value(v)
    print("done")
