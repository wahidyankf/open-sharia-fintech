"""Example 57: one word can mean different models in different contexts."""


class SalesCustomer:
    def __init__(self, credit_limit: int) -> None:
        self.credit_limit = credit_limit  # => sales cares about credit


class ShippingCustomer:
    def __init__(self, delivery_address: str) -> None:
        self.delivery_address = delivery_address  # => shipping cares about delivery


assert hasattr(SalesCustomer(10), "credit_limit") and hasattr(
    ShippingCustomer("A"), "delivery_address"
)
