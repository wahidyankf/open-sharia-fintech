"""Kata 1 (after): purity fix -- builds and returns NEW records, the caller's input is never touched."""

from dataclasses import dataclass, replace


@dataclass  # => still a plain mutable record -- the FIX is in apply_discount, not the type
class CartItem:
    name: str
    price: float


def apply_discount(cart: list[CartItem], rate: float) -> list[CartItem]:
    return [
        replace(item, price=item.price * rate) for item in cart
    ]  # => new CartItem per element


cart = [CartItem("pen", 10.0), CartItem("mug", 20.0)]
first_pass = apply_discount(cart, 0.9)
second_pass = apply_discount(
    cart, 0.9
)  # cart itself was never mutated, so this is a FRESH discount
print([item.price for item in second_pass])
print(
    first_pass is second_pass
)  # different objects, and cart's own prices are untouched
