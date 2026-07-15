"""Example 42: a long-running Python 3.14 process we will try to attach pdb to by PID."""

from __future__ import annotations

import time


def handle_tick(counter: int) -> int:
    return counter + 1


def main() -> None:
    counter = 0
    while True:
        counter = handle_tick(counter)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
