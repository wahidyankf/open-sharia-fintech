"""Example 11: money carries arithmetic's currency rule."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int
    currency: str

    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("mixed currencies")  # => prevent nonsense
        return Money(self.amount + other.amount, self.currency)  # => preserve the unit


assert Money(2, "USD").add(Money(3, "USD")) == Money(5, "USD")  # => valid arithmetic
