"""Shared test: all four paradigm implementations must agree on the identical result.

This is the capstone's step-1 requirement -- one test asserting the expected output, checked
against every implementation. AMOUNTS/STARTING_BALANCE/EXPECTED are the single source of truth
every paradigm-specific test file (test_imperative.py, test_oo.py, test_functional.py,
test_reactive.py) also checks its own implementation against.
"""

from paradigms.functional import process_transactions_functional
from paradigms.imperative import process_transactions_imperative
from paradigms.oo import TransactionProcessor
from paradigms.reactive import process_transactions_reactive

AMOUNTS = [50, -200, 30, -1000, 20]  # => the ONE shared problem input, used by all four paradigms
STARTING_BALANCE = 100
EXPECTED_BALANCE = 200
EXPECTED_REJECTED = [1, 3]  # => -200 (index 1) and -1000 (index 3) both would have gone negative


def test_all_four_paradigms_agree_on_the_expected_result() -> None:
    imperative_result = process_transactions_imperative(list(AMOUNTS), starting_balance=STARTING_BALANCE)
    oo_result = TransactionProcessor(starting_balance=STARTING_BALANCE).process_all(list(AMOUNTS))
    functional_balance, functional_rejected = process_transactions_functional(tuple(AMOUNTS), starting_balance=STARTING_BALANCE)
    reactive_result = process_transactions_reactive(list(AMOUNTS), starting_balance=STARTING_BALANCE)

    expected = (EXPECTED_BALANCE, EXPECTED_REJECTED)  # => the ONE expected shape every paradigm must match
    assert imperative_result == expected
    assert oo_result == expected
    assert (functional_balance, list(functional_rejected)) == expected
    assert reactive_result == expected


def test_a_stub_implementation_would_fail_this_shared_test() -> None:
    # => proves the shared test is meaningful (not vacuously true): a deliberately wrong stub,
    # => shaped like the real functions but always accepting every transaction, fails the check
    def stub_always_accepts(amounts: list[int], starting_balance: int) -> tuple[int, list[int]]:
        return starting_balance + sum(amounts), []  # => never rejects anything -- the wrong behavior

    stub_result = stub_always_accepts(list(AMOUNTS), starting_balance=STARTING_BALANCE)
    assert stub_result != (EXPECTED_BALANCE, EXPECTED_REJECTED)  # => the stub is provably NOT a valid solution


def test_all_four_paradigms_agree_on_a_second_independent_sample() -> None:
    amounts = [10, -5, -50, 100, -200]  # => a different transaction sequence
    starting_balance = 20
    # => trace: 20+10=30(ok), 30-5=25(ok), 25-50=-25 rejected(stays 25), 25+100=125(ok), 125-200=-75 rejected(stays 125)
    expected = (125, [2, 4])

    imperative_result = process_transactions_imperative(list(amounts), starting_balance=starting_balance)
    oo_result = TransactionProcessor(starting_balance=starting_balance).process_all(list(amounts))
    functional_balance, functional_rejected = process_transactions_functional(tuple(amounts), starting_balance=starting_balance)
    reactive_result = process_transactions_reactive(list(amounts), starting_balance=starting_balance)

    assert imperative_result == expected
    assert oo_result == expected
    assert (functional_balance, list(functional_rejected)) == expected
    assert reactive_result == expected
