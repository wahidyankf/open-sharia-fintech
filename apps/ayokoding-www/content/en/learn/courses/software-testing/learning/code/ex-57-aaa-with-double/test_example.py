# learning/code/ex-57-aaa-with-double/test_example.py
"""Example 57: Arrange-Act-Assert with a Double."""

from unittest.mock import MagicMock  # => the double this AAA test arranges and later asserts on (co-13)  # fmt: skip


def charge_customer(payment_gateway, amount: float) -> str:  # => the unit under test  # fmt: skip
    success = payment_gateway.charge(amount)  # => delegates to a collaborator -- outcome AND call both matter  # fmt: skip
    return "charged" if success else "failed"  # => the unit's OWN decision logic based on the collaborator's reply  # fmt: skip


def test_charge_customer_result_and_interaction() -> None:
    # --- Arrange: build the double AND configure its canned behavior ---
    mock_gateway = MagicMock()  # => arrange, part 1: the double itself (co-01, co-13)
    mock_gateway.charge.return_value = True  # => arrange, part 2: configures what charge() hands back  # fmt: skip

    # --- Act: call the ONE thing under test, exactly once ---
    result = charge_customer(mock_gateway, 50.0)  # => act -- the single call being tested  # fmt: skip

    # --- Assert: check BOTH the RESULT and the INTERACTION with the double ---
    assert result == "charged"  # => assert 1: the unit's own decision logic, based on the mocked outcome  # fmt: skip
    mock_gateway.charge.assert_called_once_with(50.0)  # => assert 2: the EXACT interaction that happened (co-13)  # fmt: skip
    # => this is AAA (ex-03) combined with a double (ex-31/32): the Assert phase now
    # => checks two DIFFERENT things -- what the unit returned, and how it used its collaborator
