"""Kata 1 (before): a shared, mutable class-level list attribute."""


class Cart:
    items: list[str] = []  # declared on the CLASS -- shared by every instance

    def add(self, item: str) -> None:
        self.items.append(item)


a = Cart()
b = Cart()
a.add("apple")
print(b.items)
