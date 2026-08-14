# => Keeps this domain step explicit and reviewable.
"""Example 76: publish a boundary event without internal fields."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class DomainOrderPlaced:
    # => Keeps this domain step explicit and reviewable.
    order_id: str
    # => Keeps this domain step explicit and reviewable.
    total: int
    # => Keeps this domain step explicit and reviewable.
    internal_credit_score: int


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class IntegrationOrderPlaced:
    # => Keeps this domain step explicit and reviewable.
    order_id: str
    total: int  # => foreign contexts do not receive internal detail


# => Names policy so callers do not recreate the rule.
def publish(domain: DomainOrderPlaced) -> IntegrationOrderPlaced:
    # => Returns the domain result instead of leaking representation.
    return IntegrationOrderPlaced(domain.order_id, domain.total)


# => Proves the stated business rule is observable.
assert not hasattr(publish(DomainOrderPlaced("o-1", 20, 700)), "internal_credit_score")
