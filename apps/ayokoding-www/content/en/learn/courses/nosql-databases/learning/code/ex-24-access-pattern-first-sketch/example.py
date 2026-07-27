"""Example 24: Access-Pattern-First Sketch."""  # => co-08: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

from typing import Any  # => co-08: a sketch's document shape genuinely varies -- a plain Mapping is the honest type

# Step 1 (co-08): write the two queries this schema MUST answer, BEFORE drawing
# any entity diagram -- "user profile + 3 most recent orders" and "user's
# lifetime spend total" are named here first, as plain English, not as SQL.
QUERY_1 = "fetch a user's profile plus their 3 most recent orders"  # => co-08: dominant read #1, stated up front
QUERY_2 = "fetch a user's lifetime total spend"  # => co-08: dominant read #2, stated up front

# Step 2 (co-08): derive ONE document shape that answers BOTH queries with a
# single fetch each -- recent orders and a running total are embedded directly
# on the user document, not left in a separate collection requiring a join.
USER_STORE: dict[str, dict[str, Any]] = {  # => co-08,co-09: the access-pattern-derived shape, an in-memory stand-in for a real store
    "user:1": {  # => ONE document holds everything BOTH dominant queries need -- no join, no second collection
        "name": "Ada",  # => the profile half of QUERY_1's answer
        "recent_orders": [  # => co-08: satisfies QUERY_1 -- no separate "orders" fetch needed
            {"order_id": "o-103", "amount": 42.50},  # => most recent order -- kept first, matching "3 most recent"
            {"order_id": "o-102", "amount": 19.00},  # => second most recent order
            {"order_id": "o-101", "amount": 75.25},  # => third most recent order -- exactly 3, not the FULL order history
        ],  # => closes the embedded array -- all 3 orders travel WITH the profile in one document
        "lifetime_spend": 136.75,  # => co-08: satisfies QUERY_2 -- a maintained running total, not a live SUM() join
    }  # => closes user:1's document -- profile, recent orders, and running total, all in ONE place
}  # => closes the whole in-memory store -- a real document store would hold this shape per-user, identically


def fetch_profile_with_recent_orders(user_id: str) -> dict[str, Any]:  # => co-08: answers QUERY_1 with ONE fetch
    """Answer QUERY_1 (profile + 3 most recent orders) with a single document read."""  # => documents contract
    user = USER_STORE[user_id]  # => co-08: ONE lookup -- name and recent_orders arrive together, already embedded
    return {"name": user["name"], "recent_orders": user["recent_orders"]}  # => no second query against an "orders" collection


def fetch_lifetime_spend(user_id: str) -> float:  # => co-08: answers QUERY_2 with ONE fetch
    """Answer QUERY_2 (lifetime spend) with a single document read."""  # => documents the contract
    return USER_STORE[user_id]["lifetime_spend"]  # => co-08: ONE lookup -- no SUM() aggregation across an orders collection


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    print(f"Query 1: {QUERY_1}")  # => Output: Query 1: fetch a user's profile plus their 3 most recent orders
    print(f"Query 2: {QUERY_2}")  # => Output: Query 2: fetch a user's lifetime total spend

    profile = fetch_profile_with_recent_orders("user:1")  # => runs QUERY_1's single-fetch answer
    assert len(profile["recent_orders"]) == 3  # => co-08: exactly the 3 recent orders QUERY_1 asked for, one fetch
    print(
        f"Query 1 result (1 fetch): {profile}"
    )  # => Output: Query 1 result (1 fetch): {'name': 'Ada', 'recent_orders': [{'order_id': 'o-103', 'amount': 42.5}, {'order_id': 'o-102', 'amount': 19.0}, {'order_id': 'o-101', 'amount': 75.25}]}

    spend = fetch_lifetime_spend("user:1")  # => runs QUERY_2's single-fetch answer
    assert spend == 136.75  # => co-08: matches the maintained running total exactly, no live aggregation needed
    print(f"Query 2 result (1 fetch): {spend}")  # => Output: Query 2 result (1 fetch): 136.75
    print("Both dominant queries answered with exactly one fetch each -- the shape was derived FROM them")  # => Output line


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
