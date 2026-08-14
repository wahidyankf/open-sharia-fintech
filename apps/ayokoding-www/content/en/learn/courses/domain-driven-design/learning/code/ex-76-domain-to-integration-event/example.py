"""Example 76: publish a boundary event without internal fields."""

from dataclasses import dataclass


@dataclass(frozen=True)
class DomainOrderPlaced:
    order_id: str
    total: int
    internal_credit_score: int


@dataclass(frozen=True)
class IntegrationOrderPlaced:
    order_id: str
    total: int  # => foreign contexts do not receive internal detail


def publish(domain: DomainOrderPlaced) -> IntegrationOrderPlaced:
    return IntegrationOrderPlaced(domain.order_id, domain.total)


assert not hasattr(publish(DomainOrderPlaced("o-1", 20, 700)), "internal_credit_score")
