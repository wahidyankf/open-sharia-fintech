# => Keeps this domain step explicit and reviewable.
"""Example 8: addresses are values, customers are identities."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Address:
    street: str  # => two identical addresses are interchangeable values


# => Uses generated value behaviour so policy is not duplicated.
@dataclass
# => Gives domain rules a single, named home.
class Customer:
    id: str  # => customers are tracked by an independent id


assert Address("Main") == Address("Main")  # => value equality
assert Customer("c-1").id == "c-1"  # => entity identity
print("choice made")  # => Output: choice made
