"""Example 65: a conformist accepts the upstream model intentionally."""

from dataclasses import dataclass


@dataclass(frozen=True)
class ProviderPayment:
    id: str
    status: str  # => downstream adopts provider's published shape


def accepted(payment: ProviderPayment) -> bool:
    return payment.status == "paid"  # => no ACL translation occurs


assert accepted(ProviderPayment("p-1", "paid"))
