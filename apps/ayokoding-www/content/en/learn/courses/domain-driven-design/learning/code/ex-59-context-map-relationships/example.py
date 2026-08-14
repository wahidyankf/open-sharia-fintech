"""Example 59: a context map makes relationship direction explicit."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ContextEdge:
    upstream: str
    downstream: str
    relationship: str  # => names the integration agreement


edge = ContextEdge("orders", "shipping", "customer-supplier")
assert edge.relationship == "customer-supplier"
