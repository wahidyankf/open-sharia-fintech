# => Keeps this domain step explicit and reviewable.
"""Example 57: one word can mean different models in different contexts."""


# => Gives domain rules a single, named home.
class SalesCustomer:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, credit_limit: int) -> None:
        self.credit_limit = credit_limit  # => sales cares about credit


# => Gives domain rules a single, named home.
class ShippingCustomer:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, delivery_address: str) -> None:
        self.delivery_address = delivery_address  # => shipping cares about delivery


# => Proves the stated business rule is observable.
assert hasattr(SalesCustomer(10), "credit_limit") and hasattr(
    # => Keeps this domain step explicit and reviewable.
    ShippingCustomer("A"),
    # => Verifies shipping keeps its own concern instead of inheriting sales terms.
    "delivery_address",
    # => Keeps this domain step explicit and reviewable.
)
