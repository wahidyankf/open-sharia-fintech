from __future__ import annotations  # => DD-39 hygiene -- unrelated to either fix itself


def compute_total(
    order: dict,
) -> (
    float
):  # => co-01/co-03: the CORRECTNESS-fixed version, confirmed via step 2's pdb session
    # FIX (debugger-guided, test-first): default missing discount to 0.0,
    # confirmed via the pdb post-mortem session above -- order.get("discount")
    # was None on the failing case, not a missing feature, a missing default.
    return order["price"] * order["qty"] - order.get(
        "discount", 0.0
    )  # => co-03: .get() with a default, not bare indexing


def dedupe_customers(
    orders: list[dict],
) -> list[dict]:  # => co-13/co-23: the PERFORMANCE-fixed version, confirmed via step 4
    # FIX (performance): O(1) set-membership check instead of O(n) list scan.
    seen: set[str] = (
        set()
    )  # => co-23: a SET, not a list -- membership checks against it are O(1) each
    result: list[
        dict
    ] = []  # => co-23: preserves the SAME output order as the original, unbounded implementation
    for order in (
        orders
    ):  # => co-23: iterates every order exactly once -- O(n) total, not O(n^2)
        customer_id = order[
            "customer_id"
        ]  # => co-23: the SAME field used for deduplication as the original version
        if (
            customer_id not in seen
        ):  # => co-23: O(1) set lookup, replacing the original's O(n) list scan
            seen.add(
                customer_id
            )  # => co-23: marks this customer_id as seen -- O(1), not O(n) append+future-scan
            result.append(
                order
            )  # => co-23: keeps the FIRST order for each distinct customer_id, same as before
    return result  # => co-23: the deduplicated list -- identical CONTENTS to the original, produced O(n) instead of O(n^2)


def build_customer_report(
    orders: list[dict],
) -> list[dict]:  # => co-01/co-13: unchanged -- both fixes live entirely below it
    unique_customers = dedupe_customers(
        orders
    )  # => co-13: now O(n) -- the fix from step 4
    return [
        {"customer_id": o["customer_id"], "total": compute_total(o)}
        for o in unique_customers
    ]  # => co-01: uses the fixed compute_total
