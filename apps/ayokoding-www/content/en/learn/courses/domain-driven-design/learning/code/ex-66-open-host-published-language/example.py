"""Example 66: expose a stable versioned edge DTO."""

from dataclasses import dataclass


@dataclass(frozen=True)
class OrderPlacedV1:
    order_id: str
    total: int  # => consumers bind to this published language, not internal Order


assert OrderPlacedV1("o-1", 25).order_id == "o-1"
