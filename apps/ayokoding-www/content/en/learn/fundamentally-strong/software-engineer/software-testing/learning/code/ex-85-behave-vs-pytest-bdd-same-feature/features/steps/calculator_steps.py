"""Example 85 (behave half): step definitions for features/calculator.feature, behave-style."""
# behave auto-discovers THIS file from features/steps/ -- no explicit @scenario binding call
# anywhere, unlike pytest-bdd's half of this same example, further down in the same .feature file.

from __future__ import (
    annotations,
)  # => enables modern union/generic syntax under this pinned Python

from behave import given, then, when  # => co-30: behave 1.3.3's OWN decorator API, not pytest-bdd's  # fmt: skip
from behave.runner import (
    Context,
)  # => co-30: behave passes "context" as the FIRST arg to every step


@given("the number {value:d}")  # => co-29/co-30: behave ALSO supports typed {value:d} parsing  # fmt: skip
def step_given_number(context: Context, value: int) -> None:  # => co-30: "context" carries state  # fmt: skip
    if not hasattr(context, "numbers"):  # => co-30: context PERSISTS across every step in a scenario  # fmt: skip
        context.numbers = []  # type: ignore[attr-defined]  # => co-30: initialized ONCE, on the FIRST Given
    context.numbers.append(value)  # type: ignore[attr-defined]  # => co-30: "And" reuses this SAME @given  # fmt: skip


@when("the numbers are added")  # => co-30: behave's own @when decorator  # fmt: skip
def step_when_added(context: Context) -> None:  # => co-30: reads the numbers the Given steps built up  # fmt: skip
    context.result = sum(context.numbers)  # type: ignore[attr-defined]  # => co-30: WRITES to context  # fmt: skip


@then("the result is {expected:d}")  # => co-30: behave's own @then decorator  # fmt: skip
def step_then_result(
    context: Context, expected: int
) -> None:  # => co-30: the SAME context, final read
    assert context.result == expected  # type: ignore[attr-defined]  # => co-30: READS from context  # fmt: skip
