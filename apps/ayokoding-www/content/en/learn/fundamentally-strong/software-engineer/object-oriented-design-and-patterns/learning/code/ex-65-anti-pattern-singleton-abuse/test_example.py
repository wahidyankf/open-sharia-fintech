"""Example 65: pytest verification that singleton state leaks silently between tests."""

from example import RequestCounter, handle_request_a, handle_request_b


def test_state_leaks_across_two_unrelated_looking_functions() -> None:
    RequestCounter._instance = None  # => manual reset required BECAUSE the singleton has no other reset mechanism
    a_result = handle_request_a()  # => no parameter reveals this depends on shared state
    b_result = handle_request_b()  # => a DIFFERENT function, yet its result depends on what ran before it
    assert a_result == 1  # => first increment anywhere
    assert b_result == 2  # => the "hidden coupling" pain: b's result depends on a having run first


def test_forgetting_the_manual_reset_leaks_state_into_the_next_test() -> None:
    # => this test intentionally does NOT reset _instance first, demonstrating the isolation cost directly
    leaked_start = RequestCounter().count  # type: ignore[attr-defined]  # => count is whatever the PREVIOUS test left
    assert leaked_start > 0  # => proof: state from test_state_leaks_across_two_unrelated_looking_functions survived


# => Run: pytest -q -- Output: 2 passed
