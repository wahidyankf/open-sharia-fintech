"""Example 15: an order line composes meaningful values."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderLine:
    product_id: str  # => an id is explicit instead of an anonymous primitive
    quantity: int
    unit_price: int

    def total(self) -> int:
        return self.quantity * self.unit_price  # => the line owns its arithmetic


assert OrderLine("book", 2, 15).total() == 30  # => Output: 30
