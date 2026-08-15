# => Keeps this domain step explicit and reviewable.
"""Example 5: value behaviour returns a replacement."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Money:
    # => Keeps this domain step explicit and reviewable.
    amount: int

    # => Names policy so callers do not recreate the rule.
    def add(self, other: "Money") -> "Money":
        return Money(self.amount + other.amount)  # => the operands stay unchanged


first, second = Money(10), Money(5)  # => two shareable immutable values
# => Proves the stated business rule is observable.
assert first.add(second) == Money(15) and first == Money(
    # => Keeps this domain step explicit and reviewable.
    10
)  # => addition has no side effect
print("15")  # => Output: 15
