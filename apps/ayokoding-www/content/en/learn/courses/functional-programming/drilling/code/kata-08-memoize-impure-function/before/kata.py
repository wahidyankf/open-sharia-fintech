"""Kata 8 (before): @lru_cache applied to an IMPURE function -- the cache freezes a stale value."""

from functools import lru_cache

prices: dict[str, float] = {"widget": 9.99}


@lru_cache  # SMELL: memoization is only safe on a PURE function -- this one reads mutable module state
def get_price(sku: str) -> float:
    return prices[
        sku
    ]  # BUG: depends on `prices`, not just on `sku` -- not actually pure


first_lookup = get_price("widget")
print(first_lookup)
prices["widget"] = (
    14.99  # the underlying price table changes at runtime, as real price tables do
)
second_lookup = get_price("widget")
print(
    second_lookup
)  # BUG: still 9.99 -- the cache never learns the price actually changed
