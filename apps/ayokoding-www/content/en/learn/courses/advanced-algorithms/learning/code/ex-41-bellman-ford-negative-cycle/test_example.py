"""Example 41: pytest verification for Negative Cycle Detection."""

from example import bellman_ford_with_cycle_check


def test_detects_a_genuine_negative_cycle() -> None:
    edges = [(0, 1, 1), (1, 2, -1), (2, 0, -1)]  # => 0->1->2->0 sums to -1
    _, has_cycle = bellman_ford_with_cycle_check(3, edges, start=0)
    assert has_cycle is True


def test_negative_edges_without_a_cycle_are_not_flagged() -> None:
    edges = [(0, 1, -5), (1, 2, -5)]  # => a simple path, both edges negative
    _, has_cycle = bellman_ford_with_cycle_check(3, edges, start=0)
    assert has_cycle is False


def test_all_positive_weights_never_flag_a_cycle() -> None:
    edges = [(0, 1, 2), (1, 2, 3), (2, 0, 4)]  # => a positive-weight cycle is fine
    _, has_cycle = bellman_ford_with_cycle_check(3, edges, start=0)
    assert has_cycle is False


# => Run: pytest -- Output: 3 passed
