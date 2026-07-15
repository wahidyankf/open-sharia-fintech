"""Example 26: tbreak: a One-Shot Breakpoint."""

from __future__ import annotations


def attempt(n: int) -> bool:
    return n >= 3  # succeeds only from the 3rd attempt onward


def retry_until_success(max_attempts: int) -> int:
    for n in range(1, max_attempts + 1):
        if attempt(n):
            return n
    return -1


if __name__ == "__main__":
    print(retry_until_success(5))
