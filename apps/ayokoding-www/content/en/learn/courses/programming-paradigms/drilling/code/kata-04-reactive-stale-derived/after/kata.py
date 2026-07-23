"""Kata 4 (after): reactive fix -- total is a computed property, impossible to forget updating."""


class Cart:
    def __init__(self) -> None:
        self.items: list[int] = []

    @property
    def total(self) -> int:
        return sum(self.items)  # ALWAYS current -- there is no separate field that could go stale

    def add_item(self, price: int) -> None:
        self.items.append(price)

    def remove_item(self, price: int) -> None:
        self.items.remove(price)


cart = Cart()
cart.add_item(10)
cart.add_item(20)
cart.remove_item(10)
print(cart.items)
print(cart.total)
