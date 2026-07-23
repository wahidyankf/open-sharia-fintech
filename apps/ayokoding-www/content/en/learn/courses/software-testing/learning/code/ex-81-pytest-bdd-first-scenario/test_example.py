"""Example 81: One Given/When/Then Scenario, Bound to pytest-bdd Step Definitions."""
# The .feature file below is not documentation ABOUT this test -- pytest-bdd PARSES it and
# @scenario binds it, so the plain-language Gherkin genuinely IS the executable test.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from pytest_bdd import given, scenario, then, when  # => co-28/co-30: pytest-bdd 8.1.0's binding API  # fmt: skip
from pytest_bdd.parsers import (
    parse,
)  # => co-30: extracts the QUOTED "Ada" straight from the step text


@scenario("features/greeting.feature", "Say hello to a named visitor")  # => co-30: binds ONE  # fmt: skip
def test_say_hello_to_a_named_visitor() -> (
    None
):  # => co-02/co-28: the pytest TEST this scenario becomes
    """pytest-bdd generates the test body from the .feature file -- this docstring is just labeling."""  # fmt: skip


@given(parse('a visitor named "{name}"'), target_fixture="visitor_name")  # => co-30: captures {name}  # fmt: skip
def a_visitor_named(name: str) -> str:  # => co-28: the GIVEN -- establishes context  # fmt: skip
    return name  # => co-30: target_fixture publishes this AS a fixture later steps can request  # fmt: skip


@when("the app greets the visitor", target_fixture="greeting")  # => co-28: the WHEN -- the action  # fmt: skip
def the_app_greets_the_visitor(visitor_name: str) -> str:  # => co-30: requests the GIVEN's fixture  # fmt: skip
    return f"Hello, {visitor_name}!"  # => co-28: the action's OWN result, published as "greeting"  # fmt: skip


@then(parse('the greeting is "{expected}"'))  # => co-28: the THEN -- the outcome check  # fmt: skip
def the_greeting_is(greeting: str, expected: str) -> None:  # => co-30: requests the WHEN's fixture  # fmt: skip
    assert greeting == expected  # => co-28: ties the Gherkin scenario's outcome to a real assertion  # fmt: skip
