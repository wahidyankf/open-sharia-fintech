"""Example 34: reference another aggregate by id."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CustomerId:
    value: str  # => identity is a value at this aggregate boundary


@dataclass
class Order:
    customer_id: CustomerId  # => no Customer object crosses into the order


assert Order(CustomerId("c-1")).customer_id.value == "c-1"
