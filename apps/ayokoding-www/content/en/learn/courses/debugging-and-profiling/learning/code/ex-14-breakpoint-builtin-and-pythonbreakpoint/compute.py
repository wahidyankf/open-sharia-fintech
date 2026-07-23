"""Example 14: The breakpoint() Builtin and PYTHONBREAKPOINT."""

from __future__ import annotations


def compute() -> int:
    breakpoint()  # honors the PYTHONBREAKPOINT environment variable
    return 42


if __name__ == "__main__":
    print(compute())
