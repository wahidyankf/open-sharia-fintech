# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 41."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
log: list[str] = ["+1", "+2"]


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def apply(commands: list[str]) -> int:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return sum(int(command.removeprefix("+")) for command in commands)


# => Replay has no hidden time, random value, or external read.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert apply(log) == apply(log) == 3
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(apply(log))
