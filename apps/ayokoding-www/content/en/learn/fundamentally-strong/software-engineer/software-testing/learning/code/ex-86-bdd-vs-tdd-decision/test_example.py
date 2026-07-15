"""Example 86: One Change, Two Changes -- Which One Earns a TDD Unit Test, Which One a BDD Scenario."""
# round_to_cents() is internal -- low risk, engineer-only audience -- so it gets a fast TDD unit
# test. calculate_late_fee() charges real members real money -- higher risk, and a librarian
# needs to read and confirm it -- so it gets a Gherkin scenario instead (co-32's framework).

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from pytest_bdd import given, scenario, then, when  # => co-28/co-30: only Change B below needs this  # fmt: skip
from pytest_bdd.parsers import parse  # => co-30: extracts Change B's typed {days:d}/{expected:f}  # fmt: skip

# =============================================================================
# Change A: round_to_cents() -- an INTERNAL utility. co-32 decision: unit TDD.
#
# Risk: low, contained to one pure function. Audience: only engineers ever read
# or care about this code's internals -- a librarian has no opinion on IEEE-754
# rounding. A Gherkin scenario here would translate a math detail into fake
# "ubiquitous language" nobody outside engineering would ever actually read.
# =============================================================================


def round_to_cents(
    amount: float,
) -> float:  # => co-17: unit-TDD'd -- see Run block for red->green
    return round(amount, 2)  # => co-17: Python's OWN banker's rounding -- the behavior under test  # fmt: skip


def test_unit_round_to_cents_handles_floating_point_noise() -> (
    None
):  # => co-01/co-17: fast, isolated
    assert round_to_cents(1.005) == 1.0  # => co-17: pins down a KNOWN float-rounding edge case  # fmt: skip


def test_unit_round_to_cents_leaves_exact_values_unchanged() -> (
    None
):  # => co-01: a second, boring case
    assert round_to_cents(2.50) == 2.50  # => co-17: confirms an already-exact value stays untouched  # fmt: skip


# =============================================================================
# Change B: the "late fee" RULE -- a business policy. co-32 decision: BDD scenario.
#
# Risk: getting the RULE wrong charges (or fails to charge) real members real
# money -- a librarian/product owner MUST be able to read and confirm this
# exact behavior without reading Python. That is precisely BDD's audience
# argument (co-28): the .feature file IS the shared, readable spec.
# =============================================================================


def calculate_late_fee(
    days_overdue: int, rate_per_day: float = 0.50
) -> float:  # => co-28: the RULE
    return round(days_overdue * rate_per_day, 2)  # => co-28: the exact math a librarian never reads  # fmt: skip


@scenario(
    "features/late_fee.feature", "A book returned 3 days late accrues a fee"
)  # => co-28: bound
def test_a_book_returned_3_days_late_accrues_a_fee() -> None: ...  # => co-32: THIS is the acceptance  # fmt: skip


# => test a librarian could review by reading the .feature file alone, never opening this .py file


@given(parse("a book is {days:d} days overdue"), target_fixture="days_overdue")  # => co-28: the GIVEN  # fmt: skip
def a_book_is_days_overdue(days: int) -> int:  # => co-30: captures the typed {days:d} placeholder  # fmt: skip
    return days  # => co-30: published as "days_overdue" for the WHEN step below to request  # fmt: skip


@when("the late fee is calculated", target_fixture="fee")  # => co-28: the WHEN -- the action itself  # fmt: skip
def the_late_fee_is_calculated(days_overdue: int) -> float:  # => co-30: requests the GIVEN's fixture  # fmt: skip
    return calculate_late_fee(days_overdue)  # => co-32: the SAME rule the unit tier could ALSO test  # fmt: skip
    # => directly -- but the STAKEHOLDER-FACING contract lives here, in Gherkin, not in a unit test


@then(parse("the fee is {expected:f}"))  # => co-28: the THEN -- the librarian-readable outcome check  # fmt: skip
def the_fee_is(
    fee: float, expected: float
) -> None:  # => co-30: requests the WHEN step's "fee" fixture
    assert fee == expected  # => co-28: ties the Gherkin scenario's outcome to a real Python assertion  # fmt: skip
