# => Keeps this domain step explicit and reviewable.
"""Example 60: an ACL translates a legacy DTO at the edge."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class SalesCustomer:
    # => Keeps this domain step explicit and reviewable.
    id: str
    name: str  # => clean downstream domain model


# => Names policy so callers do not recreate the rule.
def translate(legacy: dict[str, str]) -> SalesCustomer:
    # => Returns the domain result instead of leaking representation.
    return SalesCustomer(
        # => Keeps this domain step explicit and reviewable.
        legacy["client_id"],
        # => Terminates the legacy field name at the translation boundary.
        legacy["full_name"],
    )  # => legacy names end at this function


# => Proves the stated business rule is observable.
assert translate({"client_id": "c-1", "full_name": "Ada"}).name == "Ada"
