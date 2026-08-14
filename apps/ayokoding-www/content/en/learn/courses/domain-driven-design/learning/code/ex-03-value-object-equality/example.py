# => Keeps this domain step explicit and reviewable.
"""Example 3: value objects compare their attributes."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Money:
    amount: int  # => amount participates in value equality
    currency: str  # => currency also participates in value equality


assert Money(10, "USD") == Money(10, "USD")  # => equal values need no shared identity
# => Proves the stated business rule is observable.
assert Money(10, "USD") != Money(
    # => Keeps this domain step explicit and reviewable.
    10,
    # => Makes currency part of value meaning, not an incidental label.
    "EUR",
)  # => a different currency is a different value
print("value equality holds")  # => Output: value equality holds
