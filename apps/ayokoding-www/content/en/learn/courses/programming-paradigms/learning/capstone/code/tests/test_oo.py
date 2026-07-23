"""Tests for the OO Sequential Transaction Processor."""

from paradigms.oo import TransactionProcessor


def test_matches_the_shared_expected_result() -> None:
    processor = TransactionProcessor(starting_balance=100)
    balance, rejected = processor.process_all([50, -200, 30, -1000, 20])
    assert (balance, rejected) == (200, [1, 3])


def test_two_processors_have_independent_state() -> None:
    a = TransactionProcessor(starting_balance=10)
    b = TransactionProcessor(starting_balance=10)
    a.apply(0, -5)  # => mutate only a's state
    assert a.process_all([]) == (5, [])  # => a reflects its own mutation
    assert b.process_all([]) == (10, [])  # => b is untouched by a's mutation


def test_process_all_returns_a_defensive_copy_of_rejected() -> None:
    processor = TransactionProcessor(starting_balance=0)
    _, rejected = processor.process_all([-1])  # => rejected immediately
    rejected.append(999)  # => mutate the RETURNED list
    _, rejected_again = processor.process_all([])  # => query the processor's own state again
    assert rejected_again == [0]  # => the processor's internal list was never touched by the caller's mutation
