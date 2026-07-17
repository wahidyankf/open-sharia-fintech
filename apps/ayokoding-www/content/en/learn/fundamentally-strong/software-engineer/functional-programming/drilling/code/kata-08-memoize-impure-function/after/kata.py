"""Kata 8 (after): fix -- no memoization on an impure lookup; the function always reads the current state."""

prices: dict[str, float] = {"widget": 9.99}


def get_price(
    sku: str,
) -> float:  # => no @lru_cache -- this function depends on prices, not just sku
    return prices[sku]


first_lookup = get_price("widget")
print(first_lookup)
prices["widget"] = 14.99  # the underlying price table changes at runtime
second_lookup = get_price("widget")
print(
    second_lookup
)  # correctly reflects the updated price -- nothing was cached to go stale
