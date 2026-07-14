"""Kata 1 (after): a fresh list per instance, built inside __init__."""


class Cart:
    def __init__(self) -> None:
        self.items: list[str] = []  # a fresh list, built per instance

    def add(self, item: str) -> None:
        self.items.append(item)


a = Cart()
b = Cart()
a.add("apple")
print(b.items)
