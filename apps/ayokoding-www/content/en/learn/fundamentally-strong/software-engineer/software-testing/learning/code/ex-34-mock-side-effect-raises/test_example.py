# learning/code/ex-34-mock-side-effect-raises/test_example.py
"""Example 34: A Mock's side_effect Raises."""

from unittest.mock import MagicMock  # => same mock object, configured to RAISE instead of return (co-13, co-04)  # fmt: skip


def safe_fetch(client) -> str | None:  # => the unit under test -- must survive a network failure  # fmt: skip
    try:
        return client.fetch()  # => act: delegates to a collaborator that MIGHT fail
    except ConnectionError:  # => the specific failure mode this test wants to exercise
        return None  # => the unit's OWN recovery behavior -- degrade gracefully, don't crash


def test_mock_side_effect_simulates_a_real_failure() -> None:
    mock_client = MagicMock()  # => arrange: a bare mock, about to be configured to raise  # fmt: skip
    mock_client.fetch.side_effect = ConnectionError("network unreachable")  # => co-13: RAISES instead of returning  # fmt: skip
    # => side_effect set to an exception INSTANCE (or class) makes the mock RAISE it when
    # => called, rather than returning a value -- simulating a real collaborator's failure
    result = safe_fetch(mock_client)  # => act: fetch() raises, safe_fetch's except block catches it  # fmt: skip
    assert result is None  # => confirms safe_fetch's OWN error-handling logic, not the mock's  # fmt: skip
