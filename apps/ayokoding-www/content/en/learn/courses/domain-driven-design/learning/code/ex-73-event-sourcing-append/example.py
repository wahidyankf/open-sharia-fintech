# => Keeps this domain step explicit and reviewable.
"""Example 73: append facts instead of overwriting a row."""

events: list[dict[str, object]] = []  # => the event stream is append-only history
# => Keeps this domain step explicit and reviewable.
events.append(
    # => Keeps this domain step explicit and reviewable.
    {"type": "OrderPlaced", "order_id": "o-1"}
)  # => transition becomes a durable fact
# => Keeps this domain step explicit and reviewable.
events.append(
    # => Keeps this domain step explicit and reviewable.
    {"type": "OrderPaid", "order_id": "o-1"}
)  # => later fact retains the earlier one
# => Proves the stated business rule is observable.
assert len(events) == 2
