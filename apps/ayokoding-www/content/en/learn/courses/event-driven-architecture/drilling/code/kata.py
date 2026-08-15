"""Drilling kata: apply one idempotent order-status projection."""

from __future__ import annotations


def apply_once(
    processed: set[str],
    projection: dict[str, str],
    message_id: str,
    order_id: str,
    status: str,
) -> bool:
    """Apply a message exactly once from this consumer's point of view."""
    if message_id in processed:
        return False
    processed.add(message_id)
    projection[order_id] = status
    return True


if __name__ == "__main__":
    seen: set[str] = set()
    orders: dict[str, str] = {}
    print(apply_once(seen, orders, "m-1", "o-1", "paid"))
    print(apply_once(seen, orders, "m-1", "o-1", "paid"))
    print(orders)
