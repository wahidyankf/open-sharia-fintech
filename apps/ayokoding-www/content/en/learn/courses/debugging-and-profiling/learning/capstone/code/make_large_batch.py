"""Capstone step 3: a large, realistic batch for profiling the hot path (many
orders, moderate customer cardinality -- enough duplicates that dedupe_customers'
O(n^2) list-membership check actually dominates)."""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the batch itself


def make_large_batch(
    n: int = 60_000,
) -> list[
    dict
]:  # => co-13/co-19: large enough that the O(n^2) dedupe genuinely dominates
    return [  # => co-13: a moderate customer cardinality -- n // 20 distinct customers, LOTS of real duplicates
        {
            "customer_id": f"cust-{i % (n // 20 + 1)}",
            "price": 9.99,
            "qty": (i % 5) + 1,
            "discount": float(i % 3),
        }  # => co-13
        for i in range(
            n
        )  # => co-13: n orders total -- the size that makes O(n^2) vs O(n) actually visible in a profile
    ]  # => co-13: closes the list comprehension -- one dict per order, every field always present (discount included)
