# => Keeps this domain step explicit and reviewable.
"""Example 13: quantity prevents negative stock movement."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Quantity:
    # => Keeps this domain step explicit and reviewable.
    value: int

    # => Names policy so callers do not recreate the rule.
    def __post_init__(self) -> None:
        # => Checks policy before a state change is allowed.
        if self.value < 0:
            raise ValueError("quantity cannot be negative")  # => local invariant


assert Quantity(0).value == 0  # => zero is a meaningful boundary value
# => Separates the expected failure path from valid flow.
try:
    # => Keeps this domain step explicit and reviewable.
    Quantity(-1)
# => Turns the rejected case into an explicit outcome.
except ValueError:
    print("rejected")  # => Output: rejected
