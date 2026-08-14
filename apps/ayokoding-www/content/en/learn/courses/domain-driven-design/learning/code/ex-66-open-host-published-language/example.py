# => Keeps this domain step explicit and reviewable.
"""Example 66: expose a stable versioned edge DTO."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class OrderPlacedV1:
    # => Keeps this domain step explicit and reviewable.
    order_id: str
    total: int  # => consumers bind to this published language, not internal Order


# => Proves the stated business rule is observable.
assert OrderPlacedV1("o-1", 25).order_id == "o-1"
