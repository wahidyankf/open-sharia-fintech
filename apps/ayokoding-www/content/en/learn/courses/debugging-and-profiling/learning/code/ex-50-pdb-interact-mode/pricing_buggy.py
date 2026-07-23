"""Example 50: pdb's `interact` command opens a frame-scoped REPL at a breakpoint."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to interact mode itself


def compute_total(
    price: float, tax_rate: float, shipping: float
) -> float:  # => co-03: the function under test
    breakpoint()  # => co-03/co-07: land here with price/tax_rate/shipping already bound
    # BUG: tax applied to (price + shipping) instead of price alone -- confirmed via `interact` below
    total = (price + shipping) * (
        1 + tax_rate
    )  # => co-07: the WRONG formula -- interact tests the fix live
    return round(
        total, 2
    )  # => rounds to cents, same as every other pricing example in this tier


def main() -> (
    None
):  # => co-03: the entry point breakpoint() pauses INSIDE, one call deep
    result = compute_total(
        price=100.0, tax_rate=0.08, shipping=10.0
    )  # => fixed inputs -- reproducible every run
    print(
        f"total: {result}"
    )  # => prints the BUGGY total -- interact mode only experiments, never mutates this


if (
    __name__ == "__main__"
):  # => co-03: guards the module-level call so importing this file stays side-effect-free
    main()  # => co-03: the ONE call that reaches compute_total()'s breakpoint()
