"""Example 58: Product differs when its purpose differs."""


class SalesProduct:
    def __init__(self, price: int) -> None:
        self.price = price  # => sales language optimizes pricing


class ShippingProduct:
    def __init__(self, weight: int) -> None:
        self.weight = weight  # => shipping language optimizes handling


assert not issubclass(
    SalesProduct, ShippingProduct
)  # => no artificial shared class masks different meaning
