"""Example 65: pytest verification for A Memoization Decorator With a Bounded maxsize."""

from example import bounded_memoize


def test_lru_eviction_forces_a_recompute_for_the_oldest_key() -> None:
    calls: list[int] = []

    @bounded_memoize(maxsize=1)
    def track(n: int) -> int:
        calls.append(n)
        return n

    track(1)  # => miss
    track(2)  # => miss, evicts 1 (maxsize=1)
    track(1)  # => 1 was evicted -- miss again
    assert calls == [1, 2, 1]


# => Run: pytest -- Output: 1 passed
