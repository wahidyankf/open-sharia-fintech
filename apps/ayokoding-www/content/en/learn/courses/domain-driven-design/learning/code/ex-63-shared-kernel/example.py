# => Keeps this domain step explicit and reviewable.
"""Example 63: a shared kernel is a deliberate, small contract."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Money:
    # => Keeps this domain step explicit and reviewable.
    amount: int
    currency: str  # => billing and payroll may share this stable value


# => Names policy so callers do not recreate the rule.
def bill(value: Money) -> str:
    # => Returns the domain result instead of leaking representation.
    return value.currency


# => Names policy so callers do not recreate the rule.
def pay(value: Money) -> str:
    # => Returns the domain result instead of leaking representation.
    return value.currency


# => Proves the stated business rule is observable.
assert bill(Money(1, "USD")) == pay(Money(2, "USD"))
