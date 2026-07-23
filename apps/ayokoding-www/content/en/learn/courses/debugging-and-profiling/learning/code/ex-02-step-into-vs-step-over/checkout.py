"""Example 2: Step Into vs. Step Over."""

from __future__ import annotations


def apply_discount(price: float, rate: float) -> float:
    """A small helper -- the callee this example steps into or over."""
    discounted = price * (1 - rate)
    return round(discounted, 2)


def compute_line_total(price: float, qty: int, rate: float) -> float:
    breakpoint()
    unit_price = apply_discount(price, rate)  # step target: s enters this, n skips it
    return round(unit_price * qty, 2)


if __name__ == "__main__":
    print(compute_line_total(19.99, 3, 0.10))
