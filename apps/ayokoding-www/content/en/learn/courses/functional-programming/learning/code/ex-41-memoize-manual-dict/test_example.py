"""Example 41: pytest verification for A Hand-Rolled Memoization Dict."""

from example import memoize


def test_second_call_is_served_from_cache() -> None:
    calls: list[int] = []

    def track(n: int) -> int:
        calls.append(n)
        return n * n

    memoized = memoize(track)
    assert memoized(4) == 16
    assert memoized(4) == 16
    assert calls == [4]  # => the second call never re-ran the underlying function


# => Run: pytest -- Output: 1 passed
