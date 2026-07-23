"""Kata 5 (after): DIP -- ReportService depends on an injected Repository protocol, testable with a fake."""

from typing import Protocol


class Repository(Protocol):
    def fetch_total(self) -> float: ...


class FakeRepository:  # => a lightweight, INJECTABLE stand-in -- no real database needed
    def fetch_total(self) -> float:
        return 42.0


class ReportService:
    def __init__(self, repository: Repository) -> None:  # => injected, not constructed internally
        self.repository = repository

    def total(self) -> float:
        return self.repository.fetch_total()


service = ReportService(FakeRepository())  # => the fake substitutes cleanly, no database required
print(service.total())
