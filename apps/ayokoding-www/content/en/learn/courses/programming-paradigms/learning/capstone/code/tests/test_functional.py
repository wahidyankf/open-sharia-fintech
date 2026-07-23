"""Tests for the functional Sequential Transaction Processor."""

from paradigms.functional import process_transactions_functional


def test_matches_the_shared_expected_result() -> None:
    balance, rejected = process_transactions_functional((50, -200, 30, -1000, 20), starting_balance=100)
    assert (balance, list(rejected)) == (200, [1, 3])


def test_pure_fold_never_mutates_its_input_tuple() -> None:
    amounts = (10, -5, 3)  # => fresh immutable input
    process_transactions_functional(amounts, starting_balance=0)  # => call once, discard the result
    assert amounts == (10, -5, 3)  # => provably unchanged -- tuples can't be mutated in place anyway,
    # => but this documents the deliberate no-mutation contract the fold was written to satisfy


def test_calling_twice_with_the_same_arguments_returns_the_same_result() -> None:
    first = process_transactions_functional((5, -10), starting_balance=0)  # => call #1
    second = process_transactions_functional((5, -10), starting_balance=0)  # => call #2, identical arguments
    assert first == second  # => referential transparency: no hidden state anywhere
