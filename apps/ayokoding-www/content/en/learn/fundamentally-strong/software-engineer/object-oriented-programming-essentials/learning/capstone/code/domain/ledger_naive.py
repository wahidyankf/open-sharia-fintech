"""Capstone: LedgerNaive -- the naive "is-a list" version this capstone refactors away.

Kept only as a reference: `domain/ledger.py`'s Ledger is the composition-based fix that
replaces it, with identical `record`/`total` behavior and none of the leaked interface.
"""

from __future__ import annotations

from domain.money import Money


class LedgerNaive(
    list[Money]
):  # => is-a list[Money] -- inherits EVERY list method, wanted or not
    def record(self, entry: Money) -> None:  # => defines the record() method
        self.append(
            entry
        )  # => reuses list.append -- convenient, but see the leak below

    def total(self) -> int:  # => defines the total() method
        return sum(
            entry.amount for entry in self
        )  # => sums every recorded entry's amount
