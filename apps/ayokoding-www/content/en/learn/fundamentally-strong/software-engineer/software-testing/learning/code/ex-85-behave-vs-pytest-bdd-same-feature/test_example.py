"""Example 85 (pytest-bdd half): the SAME features/calculator.feature, bound a SECOND way."""
# Run this file's scenario with pytest, and run the identical features/calculator.feature with
# behave (see features/steps/calculator_steps.py) -- both tools parse the SAME Gherkin text and
# both report the SAME scenario green, via two entirely independent binding mechanisms (co-29,
# co-30). A TypeScript project would reach for Cucumber.js (@cucumber/cucumber 13.1.0) to run
# this same .feature file instead -- not exercised here, since this repo's pinned BDD stack for
# the actually-run half is Python-only (pytest-bdd + behave).

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

import pytest  # => co-05: provides the plain @pytest.fixture below, alongside pytest-bdd's own API
from pytest_bdd import given, scenario, then, when  # => co-30: pytest-bdd's OWN, DIFFERENT binding API  # fmt: skip
from pytest_bdd.parsers import (
    parse,
)  # => co-30: extracts the TYPED {value:d}/{expected:d} placeholders


@pytest.fixture
def numbers() -> list[int]:  # => co-30: a PLAIN pytest fixture -- mutated in place by BOTH the  # fmt: skip
    return []  # => Given AND the And step below, exactly like behave's "context" list did  # fmt: skip


@scenario("features/calculator.feature", "Add two positive numbers")  # => co-29: the SAME .feature file  # fmt: skip
def test_add_two_positive_numbers() -> (
    None
): ...  # => co-30: pytest-bdd's binding, independent of behave's


@given(parse("the number {value:d}"))  # => co-29/co-30: pytest-bdd binds this SAME pattern to BOTH  # fmt: skip
def the_number(value: int, numbers: list[int]) -> None:  # => "Given the number 4" AND "And the number 5"  # fmt: skip
    numbers.append(value)  # => co-30: mutates the SHARED "numbers" fixture in place, called TWICE  # fmt: skip


@when("the numbers are added", target_fixture="result")  # => co-30: pytest-bdd's @when  # fmt: skip
def the_numbers_are_added(numbers: list[int]) -> int:  # => co-30: requests the SAME "numbers" fixture  # fmt: skip
    return sum(numbers)  # => co-30: published as "result" for the THEN step to request below  # fmt: skip


@then(parse("the result is {expected:d}"))  # => co-30: pytest-bdd's @then  # fmt: skip
def the_result_is(result: int, expected: int) -> None:  # => co-30: requests the WHEN step's "result"  # fmt: skip
    assert result == expected  # => co-30: the SAME outcome behave's step_then_result() checked too  # fmt: skip
