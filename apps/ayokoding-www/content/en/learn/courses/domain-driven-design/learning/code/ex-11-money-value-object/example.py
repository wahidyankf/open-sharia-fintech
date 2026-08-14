# => Keeps this domain step explicit and reviewable.
"""Example 11: money carries arithmetic's currency rule."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Money:
    # => Keeps this domain step explicit and reviewable.
    amount: int
    # => Keeps this domain step explicit and reviewable.
    currency: str

    # => Names policy so callers do not recreate the rule.
    def add(self, other: "Money") -> "Money":
        # => Checks policy before a state change is allowed.
        if self.currency != other.currency:
            raise ValueError("mixed currencies")  # => prevent nonsense
        return Money(self.amount + other.amount, self.currency)  # => preserve the unit


assert Money(2, "USD").add(Money(3, "USD")) == Money(5, "USD")  # => valid arithmetic
