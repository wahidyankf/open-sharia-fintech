# pyright: strict
"""Kata 4 (before): taking the dirty-tracking snapshot AFTER the caller already mutated
the object means the snapshot matches the live state from the start -- nothing is EVER
detected as dirty, no matter what actually changed (co-17)."""

import dataclasses
from typing import Any


@dataclasses.dataclass
class Customer:
    id: int
    name: str
    email: str


class UnitOfWork:
    def __init__(self) -> None:
        self._snapshots: dict[int, dict[str, Any]] = {}
        self._tracked: dict[int, Customer] = {}

    def track_clean(self, customer: Customer) -> None:
        # BUG: this is called AFTER the mutation below already happened, so the "snapshot"
        # captures the ALREADY-changed state -- there is nothing left to compare against.
        self._tracked[customer.id] = customer
        self._snapshots[customer.id] = dataclasses.asdict(customer)

    def dirty_objects(self) -> list[Customer]:
        return [c for pk, c in self._tracked.items() if dataclasses.asdict(c) != self._snapshots[pk]]


uow = UnitOfWork()
customer = Customer(id=1, name="Ada", email="ada@example.com")
customer.email = "ada@newmail.com"  # mutated BEFORE track_clean() ever ran
uow.track_clean(customer)  # the snapshot now matches the ALREADY-mutated state
print(uow.dirty_objects())
