"""Example 41: pytest verification for LRU-K vs Plain LRU."""

from example import simulate_lru, simulate_lru_k


def test_plain_lru_evicts_the_hot_page_during_a_scan() -> None:
    accesses = ["hot", "hot", "a", "b", "c", "d"]
    result = simulate_lru(accesses, capacity=2)
    assert "hot" not in result


def test_lru_k_keeps_the_hot_page_during_the_same_scan() -> None:
    accesses = ["hot", "hot", "a", "b", "c", "d"]
    result = simulate_lru_k(accesses, capacity=2, k=2)
    assert "hot" in result


# => Run: pytest -- Output: 2 passed
