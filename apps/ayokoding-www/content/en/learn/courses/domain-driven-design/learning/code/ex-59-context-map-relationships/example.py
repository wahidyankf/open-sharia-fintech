# => Keeps this domain step explicit and reviewable.
"""Example 59: a context map makes relationship direction explicit."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class ContextEdge:
    # => Keeps this domain step explicit and reviewable.
    upstream: str
    # => Keeps this domain step explicit and reviewable.
    downstream: str
    relationship: str  # => names the integration agreement


# => Keeps scenario data close to the rule it exercises.
edge = ContextEdge("orders", "shipping", "customer-supplier")
# => Proves the stated business rule is observable.
assert edge.relationship == "customer-supplier"
