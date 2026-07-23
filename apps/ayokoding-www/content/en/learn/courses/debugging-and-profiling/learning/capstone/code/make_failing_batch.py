"""Capstone step 1: a 400-order batch that triggers the seeded correctness bug --
ONE order (buried in the middle) legitimately has no "discount" key, and uses a
customer_id that never appears elsewhere in the batch (so dedupe_customers does
not discard it before compute_total ever sees it).
"""

from __future__ import annotations  # => DD-39 hygiene -- unrelated to the batch itself


def make_failing_batch(
    n: int = 400,
) -> list[
    dict
]:  # => co-11: n=400 -- large enough to be realistic, small enough to minimize
    orders = [  # => co-11: 400 orders, only 50 distinct customer_id values -- LOTS of duplicates, all with "discount" set
        {
            "customer_id": f"cust-{i % 50}",
            "price": 9.99,
            "qty": (i % 5) + 1,
            "discount": float(i % 3),
        }  # => co-11: the normal shape
        for i in range(
            n
        )  # => co-11: builds the whole "healthy" batch first, before the one bad order below
    ]  # => co-11: closes the list comprehension -- every order here has a "discount" key
    orders[217] = {
        "customer_id": "cust-special-217",
        "price": 12.5,
        "qty": 2,
    }  # => co-11: NO discount key -- buried at index 217
    return orders  # => co-11: the batch this capstone's bisect + delta-debug steps both work against
