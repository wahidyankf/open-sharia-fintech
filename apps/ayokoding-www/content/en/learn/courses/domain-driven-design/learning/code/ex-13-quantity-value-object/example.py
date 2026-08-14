"""Example 13: quantity prevents negative stock movement."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Quantity:
    value: int

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError("quantity cannot be negative")  # => local invariant


assert Quantity(0).value == 0  # => zero is a meaningful boundary value
try:
    Quantity(-1)
except ValueError:
    print("rejected")  # => Output: rejected
