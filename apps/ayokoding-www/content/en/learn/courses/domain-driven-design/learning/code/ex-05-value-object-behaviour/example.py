"""Example 5: value behaviour returns a replacement."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int

    def add(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)  # => the operands stay unchanged


first, second = Money(10), Money(5)  # => two shareable immutable values
assert first.add(second) == Money(15) and first == Money(
    10
)  # => addition has no side effect
print("15")  # => Output: 15
