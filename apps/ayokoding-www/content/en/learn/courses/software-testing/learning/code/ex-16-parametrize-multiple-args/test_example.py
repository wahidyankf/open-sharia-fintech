# learning/code/ex-16-parametrize-multiple-args/test_example.py
"""Example 16: Parametrize Multiple Arguments."""

import pytest  # => same parametrize mark, now stacking TWO separate decorators (co-06)


def format_greeting(
    name: str, punctuation: str
) -> str:  # => the unit under test, two inputs
    return f"Hello, {name}{punctuation}"  # => combines both parameters into one string


@pytest.mark.parametrize("name", ["Ada", "Grace"])  # => axis 1: two possible names  # fmt: skip
@pytest.mark.parametrize("punctuation", ["!", "."])  # => axis 2: two possible punctuation marks  # fmt: skip
def test_greeting_over_every_combination(name: str, punctuation: str) -> None:
    # => STACKING two @parametrize decorators multiplies the axes: 2 names x 2 punctuation
    # => marks = 4 total test runs, one per (name, punctuation) COMBINATION (co-06)
    result = format_greeting(
        name, punctuation
    )  # => act: build the actual greeting string
    assert result.startswith(
        "Hello, "
    )  # => assert 1: the fixed prefix is always present
    assert result.endswith(punctuation)  # => assert 2: the LAST character is always this row's mark  # fmt: skip
    assert (
        name in result
    )  # => assert 3: this row's name appears somewhere in the middle
