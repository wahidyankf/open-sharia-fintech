"""Example 16: a lifecycle permits named legal transitions."""


class Order:
    def __init__(self) -> None:
        self.status = "draft"  # => new orders begin in one known state

    def place(self) -> None:
        if self.status != "draft":
            raise ValueError("not draft")  # => transition precondition
        self.status = "placed"  # => state becomes explicit

    def ship(self) -> None:
        if self.status != "placed":
            raise ValueError("not placed")  # => draft orders cannot ship
        self.status = "shipped"


order = Order()
order.place()
order.ship()  # => follows the legal path
assert order.status == "shipped"
