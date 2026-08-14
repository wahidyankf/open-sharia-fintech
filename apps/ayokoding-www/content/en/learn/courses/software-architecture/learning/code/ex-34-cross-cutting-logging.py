# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 34: apply logging outside domain policy."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from collections.abc import Callable


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def with_log(action: Callable[[int], int]) -> Callable[[int], int]:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    def wrapped(value: int) -> int:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        print("start")
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        return action(value)

    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return wrapped


# => This keeps the modeled rule explicit so its trade-off can be inspected.
@with_log
# => This keeps the modeled rule explicit so its trade-off can be inspected.
def double(value: int) -> int:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return value * 2


# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(double(3))
