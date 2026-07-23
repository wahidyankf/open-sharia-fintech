"""Kata 3 (before): closure violation -- every closure in the list captures the SAME loop variable."""

from typing import Callable

thresholds = [10, 20, 30]
validators: list[Callable[[int], bool]] = []
for t in thresholds:
    validators.append(
        lambda x: x > t
    )  # SMELL: captures the VARIABLE t, not its value at this point

print(
    [v(15) for v in validators]
)  # every validator should differ; watch what actually happens
