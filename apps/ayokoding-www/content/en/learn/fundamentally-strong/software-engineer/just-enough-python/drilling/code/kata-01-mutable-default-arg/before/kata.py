"""Kata 1 (before): a shared, mutable default argument."""


def add_item(item: str, cart: list[str] = []) -> list[str]:
    cart.append(item)
    return cart


print(add_item("apple"))
print(add_item("banana"))
