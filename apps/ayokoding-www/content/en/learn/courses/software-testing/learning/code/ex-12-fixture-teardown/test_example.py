# learning/code/ex-12-fixture-teardown/test_example.py
"""Example 12: Fixture Teardown with yield."""

import pytest  # => same @pytest.fixture decorator, this time using yield instead of return

teardown_log: list[str] = []  # => module-level list -- proves teardown genuinely ran, in order  # fmt: skip


@pytest.fixture
def managed_resource():  # => a fixture with SETUP before yield, TEARDOWN after it (co-05)
    teardown_log.append(
        "setup"
    )  # => runs BEFORE the test body -- setup half of the fixture
    resource = {"open": True}  # => the value the test body actually receives
    yield resource  # => pytest pauses HERE, hands `resource` to the test, resumes after the test returns  # fmt: skip
    # => everything below this yield is teardown -- it runs even if the test body raised
    resource["open"] = False  # => simulates closing/releasing the resource
    teardown_log.append(
        "teardown"
    )  # => proves this line genuinely executed, and in what order


def test_resource_is_open_during_the_test(managed_resource: dict[str, bool]) -> None:
    assert managed_resource["open"] is True  # => teardown has NOT run yet -- test body sees "open"  # fmt: skip
    assert teardown_log == ["setup"]  # => confirms setup ran, teardown has not, at this exact point  # fmt: skip


def test_teardown_ran_after_the_previous_test() -> None:
    # => this SECOND test runs after the FIRST test's fixture instance has already
    # => been torn down (function-scoped fixtures tear down before the next test starts)
    assert teardown_log == ["setup", "teardown"]  # => "teardown" is now present, appended after the yield  # fmt: skip
