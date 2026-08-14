# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Worked Example 43: route a request through a controlled migration seam."""


# => This keeps the modeled rule explicit so its trade-off can be inspected.
def read_order(order_id: str, use_new: bool) -> str:
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    if use_new:
        # => This keeps the modeled rule explicit so its trade-off can be inspected.
        return f"new:{order_id}"
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    return f"legacy:{order_id}"


# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(read_order("order-1", use_new=True))
