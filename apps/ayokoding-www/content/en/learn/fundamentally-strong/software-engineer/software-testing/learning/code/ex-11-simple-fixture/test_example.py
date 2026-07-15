# learning/code/ex-11-simple-fixture/test_example.py
"""Example 11: A Simple Fixture."""

import pytest  # => brings in the @pytest.fixture decorator (co-05)


@pytest.fixture
def sample_user() -> dict[
    str, str
]:  # => a fixture: reusable setup, injected by NAME (co-05)
    return {"name": "Ada", "role": "engineer"}  # => a fresh dict built fresh for each test  # fmt: skip


def test_fixture_is_injected_by_parameter_name(sample_user: dict[str, str]) -> None:
    # => pytest sees the parameter name "sample_user", matches it to the fixture ABOVE
    # => by name alone, calls the fixture function, and passes its return value in here
    assert sample_user["name"] == "Ada"  # => confirms the injected value is the real fixture output  # fmt: skip
    assert sample_user["role"] == "engineer"  # => a second field, same injected dict


def test_fixture_gives_a_fresh_copy_each_test(sample_user: dict[str, str]) -> None:
    sample_user["role"] = "mutated"  # => mutate the dict THIS test received
    assert (
        sample_user["role"] == "mutated"
    )  # => confirms the mutation stuck for this test only
    # => the test above never sees "mutated" -- pytest calls sample_user() again per test,
    # => by default (function scope), so each test gets its OWN independent dict instance
