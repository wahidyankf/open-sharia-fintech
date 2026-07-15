"""Example 23: Rubber-Duck Hypothesis Writing.

Expected vs. actual:
  - Expected: apply_member_discount(50.0, tier="gold") == 42.50  (15% off for gold)
  - Actual:   apply_member_discount(50.0, tier="gold") == 45.00  (only 10% off applied)

Hypothesis (falsifiable): TIER_DISCOUNTS["gold"] is set to 0.10 instead of 0.15 --
a single wrong constant, not a logic error in apply_member_discount() itself.
"""

from __future__ import annotations

TIER_DISCOUNTS: dict[str, float] = {
    "silver": 0.05,
    "gold": 0.10,
    "platinum": 0.20,
}  # seeded bug: gold should be 0.15


def apply_member_discount(price: float, tier: str) -> float:
    breakpoint()  # ONE stop: confirms or refutes the hypothesis above, nothing more
    rate = TIER_DISCOUNTS[tier]
    return round(price * (1 - rate), 2)


if __name__ == "__main__":
    print(apply_member_discount(50.0, "gold"))
