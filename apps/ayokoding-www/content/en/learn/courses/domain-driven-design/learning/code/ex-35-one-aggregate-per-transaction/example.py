"""Example 35: queue work for the other aggregate."""


class Order:
    def __init__(self) -> None:
        self.placed = False

    def place(self) -> str:
        self.placed = True  # => this transaction changes only the order root
        return (
            "inventory-reservation-requested"  # => the second update becomes a message
        )


assert Order().place() == "inventory-reservation-requested"
