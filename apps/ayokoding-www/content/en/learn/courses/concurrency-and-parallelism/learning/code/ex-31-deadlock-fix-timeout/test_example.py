"""Example 31: pytest verification for `acquire(timeout=...)` + Back-Off."""

from example import resolves_via_timeout


def test_timeout_and_backoff_eventually_makes_progress() -> None:
    a_tries, b_tries = resolves_via_timeout()
    assert a_tries >= 1  # => both threads eventually acquired both locks and returned
    assert b_tries >= 1


# => Run: pytest -- Output: 1 passed
