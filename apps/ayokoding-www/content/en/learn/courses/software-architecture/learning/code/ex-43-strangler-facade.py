"""Worked Example 43: route a request through a controlled migration seam."""


def read_order(order_id: str, use_new: bool) -> str:
    if use_new:
        return f"new:{order_id}"
    return f"legacy:{order_id}"


print(read_order("order-1", use_new=True))
