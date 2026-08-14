# => Keeps this domain step explicit and reviewable.
"""Example 65: a conformist accepts the upstream model intentionally."""

# => Keeps the artifact runnable with explicit dependencies.
from dataclasses import dataclass


# => Uses generated value behaviour so policy is not duplicated.
@dataclass(frozen=True)
# => Gives domain rules a single, named home.
class ProviderPayment:
    # => Keeps this domain step explicit and reviewable.
    id: str
    status: str  # => downstream adopts provider's published shape


# => Names policy so callers do not recreate the rule.
def accepted(payment: ProviderPayment) -> bool:
    return payment.status == "paid"  # => no ACL translation occurs


# => Proves the stated business rule is observable.
assert accepted(ProviderPayment("p-1", "paid"))
