"""Example 54: the same tiny target used from both CLI pdb and Neovim's DAP UI,
so the two tools can be checked against each other at the identical line/value.
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to DAP itself


def compute_shipping_cost(
    weight_kg: float, distance_km: float
) -> float:  # => co-01/co-06: the ONE function both tools stop inside
    base_rate = 2.5  # => a fixed constant -- both pdb and DAP will read this same value from locals
    cost = (
        base_rate * weight_kg + 0.01 * distance_km
    )  # => co-01/co-06: BOTH tools break AFTER this line runs
    return round(cost, 2)  # => rounds to cents -- the value the caller below prints


def main() -> None:  # => co-01: the entry point, one call deep from the breakpoint line
    result = compute_shipping_cost(
        weight_kg=12.0, distance_km=430.0
    )  # => fixed inputs -- reproducible in BOTH tools
    print(
        f"shipping cost: {result}"
    )  # => prints AFTER the debugger session releases control (pdb `c`, DAP terminate)


if (
    __name__ == "__main__"
):  # => co-01: guards the module-level call so importing this file stays side-effect-free
    main()  # => co-01/co-06: the ONE call both pdb and the headless nvim-dap session launch into
