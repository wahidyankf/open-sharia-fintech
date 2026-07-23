"""Capstone Step 1: OrderEngineSmelly -- the deliberately smelly baseline this capstone refactors away.

Kept only as a reference and a pinning-test target: `domain/order_engine.py`'s `OrderEngine`
is the SOLID-plus-patterns fix that replaces it, preserving every behavior pinned here.

Smells, on purpose:
  - SRP violation: pricing AND notification are mixed into one class.
  - OCP violation: adding a new discount means editing the if/elif chain in checkout().
  - No abstraction over "who gets notified" -- notifications is a hard-coded list, not an
    injectable collaborator.
"""

from __future__ import annotations


class OrderEngineSmelly:
    """A god object: item management, pricing, AND notification, all in one class."""

    def __init__(self) -> None:
        self.items: dict[str, float] = {}
        self.notifications: list[str] = []  # => stands in for a hard-coded print() side effect

    def add_item(self, name: str, price: float) -> None:
        self.items[name] = price

    def checkout(self, discount_type: str) -> float:
        subtotal = sum(self.items.values())
        if discount_type == "none":  # => SMELL: every new discount means editing this chain (OCP violation)
            total = subtotal
        elif discount_type == "ten_percent":
            total = subtotal * 0.90
        elif discount_type == "bogo":
            total = subtotal * 0.50
        else:
            raise ValueError(f"unknown discount type {discount_type!r}")
        self.notifications.append(f"order checked out: total {total:.2f}")  # => SMELL: notification hard-coded here
        return total
