"""Kata 4 (before): reactive-programming violation -- a manually maintained derived value goes stale."""


class Cart:
    def __init__(self) -> None:
        self.items: list[int] = []
        self.total = 0  # SMELL: a derived value stored as a plain field, kept "in sync" by hand

    def add_item(self, price: int) -> None:
        self.items.append(price)
        self.total = sum(self.items)  # easy to forget this line at ANY future call site

    def remove_item(self, price: int) -> None:
        self.items.remove(price)  # BUG: forgot to also update self.total here


cart = Cart()
cart.add_item(10)
cart.add_item(20)
cart.remove_item(10)
print(cart.items)
print(cart.total)  # stale -- still reflects the removed item
