"""Example 49: an application service coordinates without owning policy."""


class Order:
    def __init__(self) -> None:
        self.placed = False

    def place(self) -> None:
        self.placed = True  # => business transition belongs in the root


def place_order(order: Order, saved: list[Order]) -> None:
    order.place()
    saved.append(order)  # => application layer coordinates state and persistence


saved: list[Order] = []
place_order(Order(), saved)
assert saved[0].placed
