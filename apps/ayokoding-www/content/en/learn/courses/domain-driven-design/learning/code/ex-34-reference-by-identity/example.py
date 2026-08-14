# => Keeps this domain step explicit and reviewable.
"""Example 34: reference another aggregate by id."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class CustomerId:
    value: str  # => identity is a value at this aggregate boundary


# => Uses generated value behaviour so policy is not duplicated.
@dataclass
# => Gives domain rules a single, named home.
class Order:
    customer_id: CustomerId  # => no Customer object crosses into the order


# => Proves the stated business rule is observable.
assert Order(CustomerId("c-1")).customer_id.value == "c-1"
