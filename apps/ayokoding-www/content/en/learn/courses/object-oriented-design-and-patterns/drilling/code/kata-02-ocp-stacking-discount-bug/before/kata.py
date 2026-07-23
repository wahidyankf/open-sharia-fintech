"""Kata 2 (before): OCP violation -- unrelated `if` checks (not elif) let two discounts silently stack."""


def checkout_total(subtotal: float, is_premium: bool, is_first_order: bool) -> float:
    total = subtotal
    if is_premium:  # discount #1
        total = total * 0.90
    if is_first_order:  # discount #2 -- added LATER, as a separate `if`, not connected to the first
        total = total * 0.90
    return total


print(checkout_total(100.0, is_premium=True, is_first_order=True))  # customer meant to get ONE 10% discount
