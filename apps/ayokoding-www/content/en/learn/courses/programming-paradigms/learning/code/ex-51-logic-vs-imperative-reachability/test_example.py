"""Example 51: pytest verification for Logic vs Imperative Reachability."""

from example import reachable_via_bfs, reachable_via_inference


def test_both_approaches_agree_on_a_cyclic_graph() -> None:
    edges = {"a": ["b", "c"], "b": ["d"], "c": [], "d": ["a"], "e": []}  # => same graph as the demo
    # => the a->b->d->a cycle makes "a" reachable from itself -- both approaches must agree it's included
    assert reachable_via_inference("a", edges) == reachable_via_bfs("a", edges) == {"a", "b", "c", "d"}


def test_isolated_node_reaches_nothing_in_both_approaches() -> None:
    edges = {"a": ["b", "c"], "b": ["d"], "c": [], "d": ["a"], "e": []}  # => same graph
    assert reachable_via_inference("e", edges) == reachable_via_bfs("e", edges) == set()


# => Run: pytest -- Output: 2 passed
