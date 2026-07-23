"""Example 50: the real fix, with the experiment's corrected formula copied in verbatim."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the fix itself


def compute_total(
    price: float, tax_rate: float, shipping: float
) -> float:  # => the SAME signature as pricing_buggy.py
    # FIX: tax applies to price only; shipping is added post-tax (the formula
    # verified interactively via `interact` at the breakpoint in pricing_buggy.py)
    total = (
        price * (1 + tax_rate) + shipping
    )  # => co-03/co-07: the CORRECTED formula, copied straight from interact
    return round(
        total, 2
    )  # => rounds to cents, matching pricing_buggy.py's own rounding exactly


def main() -> (
    None
):  # => co-07: the SAME inputs as pricing_buggy.py, so the two totals are directly comparable
    result = compute_total(
        price=100.0, tax_rate=0.08, shipping=10.0
    )  # => identical call to the buggy version
    print(
        f"total: {result}"
    )  # => co-07: prints 118.0 -- the value `interact` already predicted


if (
    __name__ == "__main__"
):  # => co-03: keeps this file importable without running main() as a side effect
    main()  # => co-03: the one call that produces the corrected total
