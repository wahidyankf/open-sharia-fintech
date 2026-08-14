"""Example 73: append facts instead of overwriting a row."""

events: list[dict[str, object]] = []  # => the event stream is append-only history
events.append(
    {"type": "OrderPlaced", "order_id": "o-1"}
)  # => transition becomes a durable fact
events.append(
    {"type": "OrderPaid", "order_id": "o-1"}
)  # => later fact retains the earlier one
assert len(events) == 2
