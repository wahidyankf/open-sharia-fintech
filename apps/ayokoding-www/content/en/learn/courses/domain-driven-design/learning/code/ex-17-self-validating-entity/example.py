"""Example 17: the entity refuses an illegal command."""


class Order:
    def __init__(self) -> None:
        self.placed = False

    def ship(self) -> None:
        if not self.placed:
            raise ValueError("place before shipping")  # => rule has one home


try:
    Order().ship()
except ValueError as error:
    print(str(error))  # => Output: place before shipping
