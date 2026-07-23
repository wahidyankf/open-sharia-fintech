"""Kata 3 (after): closure fix -- a default argument binds EACH closure's own value at creation time."""

from typing import Callable

thresholds = [10, 20, 30]
validators: list[Callable[[int], bool]] = []
for t in thresholds:
    validators.append(
        lambda x, t=t: x > t
    )  # => t=t binds THIS iteration's value, not the variable

print([v(15) for v in validators])  # each validator now uses its own captured threshold
