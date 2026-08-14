"""Runnable artifact for distributed-systems Example 41."""

from __future__ import annotations

log: list[str] = ["+1", "+2"]


def apply(commands: list[str]) -> int:
    return sum(int(command.removeprefix("+")) for command in commands)


# => Replay has no hidden time, random value, or external read.
assert apply(log) == apply(log) == 3
print(apply(log))
