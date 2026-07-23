# pyright: strict
"""Kata 4 (after): track_clean() runs immediately at LOAD time, before the caller ever
gets a chance to mutate the object -- so the snapshot is a genuine "before" state (co-17)."""

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
        self._tracked[customer.id] = customer
        self._snapshots[customer.id] = dataclasses.asdict(customer)

    def dirty_objects(self) -> list[Customer]:
        return [c for pk, c in self._tracked.items() if dataclasses.asdict(c) != self._snapshots[pk]]


def load(pk: int, name: str, email: str) -> Customer:  # simulates a real load -- returns a FRESH object
    return Customer(id=pk, name=name, email=email)


uow = UnitOfWork()
customer = load(1, "Ada", "ada@example.com")
uow.track_clean(customer)  # THE FIX: snapshot taken IMMEDIATELY at load time, before any mutation
customer.email = "ada@newmail.com"  # mutated AFTER the snapshot -- now genuinely detectable
print(uow.dirty_objects())
