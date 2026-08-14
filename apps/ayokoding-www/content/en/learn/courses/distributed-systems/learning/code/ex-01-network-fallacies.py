# => This keeps the modeled rule explicit so its trade-off can be inspected.
"""Runnable artifact for distributed-systems Example 1."""

# => This keeps the modeled rule explicit so its trade-off can be inspected.
from __future__ import annotations

# => This keeps the modeled rule explicit so its trade-off can be inspected.
fallacies: dict[str, str] = {
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    "reliable": "a packet is lost",
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
    "zero latency": "a reply is late",
    # => This keeps the modeled rule explicit so its trade-off can be inspected.
}
# => Each reassuring assumption names an observable counterexample.
# => This keeps the modeled rule explicit so its trade-off can be inspected.
assert all(fallacies.values())
# => This keeps the modeled rule explicit so its trade-off can be inspected.
print(fallacies)
