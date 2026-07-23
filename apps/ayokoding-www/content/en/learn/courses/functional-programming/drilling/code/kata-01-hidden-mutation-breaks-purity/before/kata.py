"""Kata 1 (before): purity violation -- a function that looks pure secretly mutates its input."""

from dataclasses import dataclass


@dataclass  # => NOT frozen -- a mutable record, which is exactly what makes the bug below possible
class CartItem:
    name: str
    price: float


def apply_discount(cart: list[CartItem], rate: float) -> list[CartItem]:
    for item in cart:
        item.price *= rate  # SMELL: mutates each CartItem IN PLACE -- the caller's own data changes
    return cart


cart = [CartItem("pen", 10.0), CartItem("mug", 20.0)]
first_pass = apply_discount(cart, 0.9)
second_pass = apply_discount(
    cart, 0.9
)  # meant to apply a FRESH 0.9 discount a second time
print([item.price for item in second_pass])
print(
    first_pass is second_pass
)  # BUG: same object -- the discount compounded onto itself
