"""Example 8: addresses are values, customers are identities."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Address:
    street: str  # => two identical addresses are interchangeable values


@dataclass
class Customer:
    id: str  # => customers are tracked by an independent id


assert Address("Main") == Address("Main")  # => value equality
assert Customer("c-1").id == "c-1"  # => entity identity
print("choice made")  # => Output: choice made
