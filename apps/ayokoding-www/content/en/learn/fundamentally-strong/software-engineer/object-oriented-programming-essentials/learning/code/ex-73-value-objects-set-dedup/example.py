"""Example 73: Value Objects Deduplicate Inside a Set."""

from dataclasses import dataclass  # => imports dataclass from dataclasses


@dataclass(
    frozen=True
)  # => frozen gives consistent __eq__ AND __hash__ together, for free
class Money:  # => begins the Money class body
    amount: int  # => a required dataclass field, part of the generated __init__
    currency: str  # => a required dataclass field, part of the generated __init__


payments: list[Money] = [  # => a list that deliberately contains one exact duplicate
    Money(500, "USD"),  # => the first, original entry
    Money(500, "USD"),  # => a genuine duplicate value
    Money(100, "USD"),  # => a distinct amount -- never collides with the entries above
    Money(500, "EUR"),  # => same amount, different currency -- NOT a duplicate
]  # => closes the payments list
unique: set[Money] = set(
    payments
)  # => relies on __eq__ + __hash__ working together, correctly
print(len(unique))  # => three distinct (amount, currency) pairs survive
# => Output: 3
# => `set(payments)` deduplicates by value, not identity, because `Money`'s generated `__eq__`/`__hash__` pair compares and hashes `(amount, currency)` together
