"""Example 55: use a constructor for simple values and factory for roots."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    amount: int  # => simple value construction is transparent


class Order:
    @classmethod
    def create(cls, product: str) -> dict[str, str]:
        return {
            "status": "draft",
            "product": product,
        }  # => factory coordinates defaults


assert Money(1).amount == 1 and Order.create("book")["status"] == "draft"
