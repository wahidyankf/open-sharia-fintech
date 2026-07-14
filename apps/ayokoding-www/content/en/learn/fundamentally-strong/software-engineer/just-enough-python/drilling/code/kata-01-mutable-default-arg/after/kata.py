"""Kata 1 (after): a fresh list per call, built inside the function body."""


def add_item(item: str, cart: list[str] | None = None) -> list[str]:
    if cart is None:
        cart = []
    cart.append(item)
    return cart


print(add_item("apple"))
print(add_item("banana"))
