"""Example 60: an ACL translates a legacy DTO at the edge."""

from dataclasses import dataclass


@dataclass(frozen=True)
class SalesCustomer:
    id: str
    name: str  # => clean downstream domain model


def translate(legacy: dict[str, str]) -> SalesCustomer:
    return SalesCustomer(
        legacy["client_id"], legacy["full_name"]
    )  # => legacy names end at this function


assert translate({"client_id": "c-1", "full_name": "Ada"}).name == "Ada"
