"""Example 7: Mutating a Variable to Confirm a Hypothesis."""

from __future__ import annotations

RATE_PER_KG: dict[str, float] = {"local": 2.0, "regional": 3.5, "international": 6.0}


def compute_shipping_cost(weight_kg: float, zone: str) -> float:
    zone_key = (
        zone  # seeded bug: caller passes the abbreviation "intl", not the real key
    )
    breakpoint()
    rate = RATE_PER_KG.get(zone_key, 0.0)  # unknown key silently falls back to 0.0
    return round(weight_kg * rate, 2)


if __name__ == "__main__":
    print(compute_shipping_cost(4.0, "intl"))
