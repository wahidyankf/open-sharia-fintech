"""Worked Example 34: apply logging outside domain policy."""

from collections.abc import Callable


def with_log(action: Callable[[int], int]) -> Callable[[int], int]:
    def wrapped(value: int) -> int:
        print("start")
        return action(value)

    return wrapped


@with_log
def double(value: int) -> int:
    return value * 2


print(double(3))
