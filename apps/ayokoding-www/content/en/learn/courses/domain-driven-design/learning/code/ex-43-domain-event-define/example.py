"""Example 43: a domain event records a meaningful past fact."""

from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass(frozen=True)
class OrderPlaced:
    order_id: str  # => identity makes the event actionable
    occurred_at: datetime  # => time distinguishes a fact from a command


event = OrderPlaced("o-1", datetime.now(timezone.utc))
assert event.order_id == "o-1"
