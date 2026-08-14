"""Runnable artifact for distributed-systems Example 1."""

from __future__ import annotations

fallacies: dict[str, str] = {
    "reliable": "a packet is lost",
    "zero latency": "a reply is late",
}
# => Each reassuring assumption names an observable counterexample.
assert all(fallacies.values())
print(fallacies)
