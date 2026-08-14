# => Keeps this domain step explicit and reviewable.
"""Example 58: Product differs when its purpose differs."""


# => Gives domain rules a single, named home.
class SalesProduct:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, price: int) -> None:
        self.price = price  # => sales language optimizes pricing


# => Gives domain rules a single, named home.
class ShippingProduct:
    # => Establishes valid state before callers can rely on it.
    def __init__(self, weight: int) -> None:
        self.weight = weight  # => shipping language optimizes handling


# => Proves the stated business rule is observable.
assert not issubclass(
    # => Keeps this domain step explicit and reviewable.
    SalesProduct,
    # => Proves similar names do not force a shared model across contexts.
    ShippingProduct,
)  # => no artificial shared class masks different meaning
