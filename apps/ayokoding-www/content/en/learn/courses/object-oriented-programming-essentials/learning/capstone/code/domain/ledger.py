"""Capstone: Ledger -- the composition-over-inheritance refactor of LedgerNaive.

co-13 (composition over inheritance): Ledger HOLDS a list[Money] instead of BEING one --
`record`/`total` behave identically to LedgerNaive, but `insert`, `sort`, `reverse`, and
every other list method LedgerNaive accidentally exposed are simply not here anymore.
"""

from __future__ import annotations

from domain.money import Money


class Ledger:  # => has-a list[Money] -- never subclasses list
    def __init__(
        self,
    ) -> None:  # => the constructor -- runs once, automatically, per instantiation
        self._entries: list[
            Money
        ] = []  # => a private collaborator, not an inherited interface

    def record(self, entry: Money) -> None:  # => defines the record() method
        self._entries.append(
            entry
        )  # => delegates to the list, but does not EXPOSE the list

    def total(self) -> int:  # => defines the total() method
        return sum(
            entry.amount for entry in self._entries
        )  # => same computation as LedgerNaive.total

    def __len__(self) -> int:  # => defines the __len__() method
        return len(
            self._entries
        )  # => len(ledger) still works -- deliberately re-exposed, not leaked
