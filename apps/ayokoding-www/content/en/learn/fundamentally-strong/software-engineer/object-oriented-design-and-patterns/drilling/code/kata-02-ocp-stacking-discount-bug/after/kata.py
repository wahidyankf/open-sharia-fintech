"""Kata 2 (after): OCP -- Strategy makes exactly one discount rule apply, with no chance of silent stacking."""

from typing import Protocol


class DiscountStrategy(Protocol):
    def apply(self, subtotal: float) -> float: ...


class NoDiscount:
    def apply(self, subtotal: float) -> float:
        return subtotal


class PremiumDiscount:
    def apply(self, subtotal: float) -> float:
        return subtotal * 0.90


class FirstOrderDiscount:
    def apply(self, subtotal: float) -> float:
        return subtotal * 0.90


def choose_discount(is_premium: bool, is_first_order: bool) -> DiscountStrategy:
    if is_premium:  # ONE explicit choice -- premium takes precedence, first-order never also fires
        return PremiumDiscount()
    if is_first_order:
        return FirstOrderDiscount()
    return NoDiscount()


def checkout_total(subtotal: float, is_premium: bool, is_first_order: bool) -> float:
    strategy = choose_discount(is_premium, is_first_order)  # exactly ONE strategy selected, never two
    return strategy.apply(subtotal)


print(checkout_total(100.0, is_premium=True, is_first_order=True))  # exactly one 10% discount now
