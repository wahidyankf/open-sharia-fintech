"""Example 38: pytest verification for the Vending Machine State Machine."""

import pytest

from example import VendingMachine


def test_legal_transitions_move_through_both_states() -> None:
    machine: VendingMachine = VendingMachine()
    assert machine.insert_coin() == "coin accepted"  # => NoCoin -> HasCoin
    assert machine.dispense() == "item dispensed"  # => HasCoin -> NoCoin


def test_illegal_dispense_without_a_coin_is_rejected() -> None:
    machine: VendingMachine = VendingMachine()
    with pytest.raises(ValueError):  # => dispensing with no coin must raise, not succeed
        machine.dispense()


def test_illegal_double_coin_insert_is_rejected() -> None:
    machine: VendingMachine = VendingMachine()
    machine.insert_coin()  # => now in HasCoinState
    with pytest.raises(ValueError):  # => a second coin insert must raise, not succeed
        machine.insert_coin()


# => Run: pytest -- Output: 3 passed
