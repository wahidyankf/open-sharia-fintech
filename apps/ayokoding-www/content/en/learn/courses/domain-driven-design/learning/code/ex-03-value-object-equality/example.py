"""Example 3: value objects compare their attributes."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int  # => amount participates in value equality
    currency: str  # => currency also participates in value equality


assert Money(10, "USD") == Money(10, "USD")  # => equal values need no shared identity
assert Money(10, "USD") != Money(
    10, "EUR"
)  # => a different currency is a different value
print("value equality holds")  # => Output: value equality holds
