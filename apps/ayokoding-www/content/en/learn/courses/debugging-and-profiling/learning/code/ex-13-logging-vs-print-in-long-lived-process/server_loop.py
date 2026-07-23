"""Example 13: logging vs. print in a Long-Lived Process."""

from __future__ import annotations

import logging

logging.basicConfig(level=logging.DEBUG, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("orders")


def handle_order(order_id: str, item_count: int, unit_price: float) -> float:
    logger.debug(
        "handling order_id=%s item_count=%d unit_price=%.2f",
        order_id,
        item_count,
        unit_price,
    )
    subtotal = item_count * unit_price
    discount = (
        0.10 if item_count > 10 else 0.0
    )  # seeded bug: item_count == 10 should ALSO qualify (>=10)
    total = subtotal * (1 - discount)
    logger.info(
        "order_id=%s subtotal=%.2f discount=%.2f total=%.2f",
        order_id,
        subtotal,
        discount,
        total,
    )
    return total


if __name__ == "__main__":
    for oid, qty, price in [("A1", 3, 9.99), ("A2", 10, 5.00), ("A3", 15, 2.00)]:
        handle_order(oid, qty, price)
