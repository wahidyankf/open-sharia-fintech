"""Kata 2 (before): structured-programming violation -- a goto-style flag leaks past its intended scope."""


def process_orders(orders: list[dict[str, object]]) -> list[str]:
    processed: list[str] = []
    skip = False  # SMELL: this flag is meant to skip ONE refunded order, but nothing ever resets it
    for order in orders:
        if order["refunded"]:
            skip = True  # goto-style: "jump past" this one order
        if skip:
            continue  # BUG: skip is never turned back off, so every order AFTER the first refund is also skipped
        processed.append(str(order["id"]))
    return processed


orders: list[dict[str, object]] = [
    {"id": "A", "refunded": False},
    {"id": "B", "refunded": True},
    {"id": "C", "refunded": False},  # should still be processed -- it was never refunded
]
print(process_orders(orders))
