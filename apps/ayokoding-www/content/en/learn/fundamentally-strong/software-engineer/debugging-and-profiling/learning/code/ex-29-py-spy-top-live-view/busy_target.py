"""Example 29: a long-running target process -- what py-spy top would attach to."""

from __future__ import annotations

import time


def hot_loop() -> None:
    total = 0
    for i in range(200_000_000):
        total += i * i


def main() -> None:
    end = time.monotonic() + 3.0
    while time.monotonic() < end:
        hot_loop()


if __name__ == "__main__":
    main()
