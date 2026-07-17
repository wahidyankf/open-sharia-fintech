"""Kata 2 (after): structured-programming fix -- a per-iteration `continue` replaces the leaking flag."""


def process_orders(orders: list[dict]) -> list[str]:
    processed: list[str] = []
    for order in orders:
        if order["refunded"]:  # decision scoped to THIS iteration only -- nothing leaks to the next one
            continue
        processed.append(order["id"])
    return processed


orders = [
    {"id": "A", "refunded": False},
    {"id": "B", "refunded": True},
    {"id": "C", "refunded": False},
]
print(process_orders(orders))
