"""Example 25: Sticky Mode and the list Command."""

from __future__ import annotations

RATES: dict[str, float] = {"bronze": 0.02, "silver": 0.05, "gold": 0.10}


def bronze_fee(amount: float) -> float:
    breakpoint()  # the bug REPORTED against bronze_fee -- but l/ll's window reveals a SECOND one
    return round(amount * (1 - RATES["bronze"]), 2)


def silver_fee(amount: float) -> float:
    return round(
        amount + RATES["silver"], 2
    )  # a SECOND, not-yet-reported bug: + instead of *


def gold_fee(amount: float) -> float:
    return round(amount * (1 - RATES["gold"]), 2)


if __name__ == "__main__":
    print(bronze_fee(100.0))
