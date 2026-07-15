"""Example 83: Steps That Share State via a Context Fixture -- Set in Given, Asserted in Then."""
# A plain pytest fixture named "context" -- an ordinary mutable dict -- is requested by all three
# step functions below: Given writes to it, When mutates it, Then reads it -- ONE instance, shared.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from collections.abc import Iterator  # => types the yield-based fixture's return below  # fmt: skip

import pytest  # => co-05: provides the @pytest.fixture decorator this example builds on  # fmt: skip
from pytest_bdd import given, scenario, then, when  # => co-30: pytest-bdd's binding decorators  # fmt: skip
from pytest_bdd.parsers import parse  # => co-30: extracts the TYPED {amount:d} placeholders below  # fmt: skip


@pytest.fixture
def context() -> Iterator[dict[str, int]]:  # => co-05/co-30: ONE mutable dict, shared by EVERY step  # fmt: skip
    """A plain pytest fixture -- pytest-bdd steps can request ordinary fixtures like this one too."""  # fmt: skip
    yield {}  # => co-30: starts EMPTY -- each step below reads/writes the SAME dict instance  # fmt: skip


@scenario(
    "features/account_balance.feature", "Withdrawing less than the balance succeeds"
)
def test_withdrawing_less_than_the_balance_succeeds() -> None: ...  # => co-30: the bound scenario  # fmt: skip


@given(parse("an account with a balance of {amount:d}"))  # => co-30: {amount:d} parses an INT  # fmt: skip
def an_account_with_a_balance(
    context: dict[str, int], amount: int
) -> None:  # => co-30: requests "context"
    context["balance"] = amount  # => co-30: WRITES into the SHARED context -- this is the "set" half  # fmt: skip


@when(parse("{amount:d} is withdrawn from the account"))  # => co-30: a SECOND typed parameter  # fmt: skip
def withdraw_from_the_account(context: dict[str, int], amount: int) -> None:  # => the SAME context  # fmt: skip
    context["balance"] -= amount  # => co-30: MUTATES the value the Given step wrote, in place  # fmt: skip


@then(parse("the account balance is {expected:d}"))  # => co-30: the THEN reads what changed  # fmt: skip
def the_account_balance_is(
    context: dict[str, int], expected: int
) -> None:  # => the SAME context AGAIN
    assert context["balance"] == expected  # => co-30: the value set in Given, mutated in When, is  # fmt: skip
    # => now asserted in Then -- ONE dict instance, flowing through all three step functions  # fmt: skip
