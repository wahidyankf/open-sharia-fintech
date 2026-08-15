# => Keeps this domain step explicit and reviewable.
"""Example 43: a domain event records a meaningful past fact."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass

# => Keeps the artifact runnable with explicit dependencies.
from datetime import datetime, timezone


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class OrderPlaced:
    order_id: str  # => identity makes the event actionable
    occurred_at: datetime  # => time distinguishes a fact from a command


# => Keeps scenario data close to the rule it exercises.
event = OrderPlaced("o-1", datetime.now(timezone.utc))
# => Proves the stated business rule is observable.
assert event.order_id == "o-1"
