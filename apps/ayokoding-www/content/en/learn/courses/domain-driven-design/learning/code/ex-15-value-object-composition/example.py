# => Keeps this domain step explicit and reviewable.
"""Example 15: an order line composes meaningful values."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class OrderLine:
    product_id: str  # => an id is explicit instead of an anonymous primitive
    # => Keeps this domain step explicit and reviewable.
    quantity: int
    # => Keeps this domain step explicit and reviewable.
    unit_price: int

    # => Names policy so callers do not recreate the rule.
    def total(self) -> int:
        return self.quantity * self.unit_price  # => the line owns its arithmetic


assert OrderLine("book", 2, 15).total() == 30  # => Output: 30
