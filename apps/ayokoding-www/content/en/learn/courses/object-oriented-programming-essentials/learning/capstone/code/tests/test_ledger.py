"""Capstone: pytest coverage proving Ledger's composition refactor preserves LedgerNaive's behavior."""

from domain.ledger import Ledger
from domain.ledger_naive import LedgerNaive
from domain.money import Money


def test_ledger_naive_records_and_totals() -> None:
    ledger: LedgerNaive = LedgerNaive()
    ledger.record(Money(500))
    ledger.record(Money(300))
    assert (
        ledger.total() == 800
    )  # => baseline behavior, BEFORE the composition refactor


def test_ledger_naive_leaks_list_insert() -> None:
    ledger: LedgerNaive = LedgerNaive()
    ledger.record(Money(500))
    ledger.insert(
        0, Money(999)
    )  # => the SMELL: insert() was never meant to be part of a ledger's API
    assert (
        ledger.total() == 1499
    )  # => the leak actually mutated ledger state via a non-ledger method


def test_ledger_records_and_totals_matches_naive_behavior() -> None:
    ledger: Ledger = Ledger()
    ledger.record(Money(500))
    ledger.record(Money(300))
    assert (
        ledger.total() == 800
    )  # => SAME behavior as LedgerNaive -- tests still green after the refactor


def test_ledger_has_no_leaked_list_interface() -> None:
    ledger: Ledger = Ledger()
    assert not hasattr(
        ledger, "insert"
    )  # => the smell from LedgerNaive no longer exists on Ledger


# => Run: pytest -- Output: 4 passed
