# => Keeps this domain step explicit and reviewable.
"""Example 55: use a constructor for simple values and factory for roots."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class Money:
    amount: int  # => simple value construction is transparent


# => Gives domain rules a single, named home.
class Order:
    # => Uses generated value behaviour so policy is not duplicated.
    @classmethod
    # => Names policy so callers do not recreate the rule.
    def create(cls, product: str) -> dict[str, str]:
        # => Returns the domain result instead of leaking representation.
        return {
            # => Keeps this domain step explicit and reviewable.
            "status": "draft",
            # => Keeps this domain step explicit and reviewable.
            "product": product,
        }  # => factory coordinates defaults


# => Proves the stated business rule is observable.
assert Money(1).amount == 1 and Order.create("book")["status"] == "draft"
