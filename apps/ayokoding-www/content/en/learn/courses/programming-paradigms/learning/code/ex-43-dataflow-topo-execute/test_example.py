"""Example 43: pytest verification for Dataflow Topological Execute."""

from collections.abc import Callable

from example import topological_order


def test_order_respects_every_dependency() -> None:
    graph = {"c": ["a", "b"], "b": ["a"], "a": []}  # => same graph as the module-level demo
    order = topological_order(graph)
    assert order.index("a") < order.index("b")  # => a must precede b
    assert order.index("a") < order.index("c")  # => a must precede c
    assert order.index("b") < order.index("c")  # => b must precede c


def test_result_matches_the_documented_formulas() -> None:
    graph = {"c": ["a", "b"], "b": ["a"], "a": []}
    formulas: dict[str, Callable[[dict[str, int]], int]] = {
        "a": lambda r: 1,
        "b": lambda r: r["a"] + 1,
        "c": lambda r: r["a"] + r["b"],
    }
    order = topological_order(graph)
    results: dict[str, int] = {}
    for node in order:
        results[node] = formulas[node](results)
    assert results == {"a": 1, "b": 2, "c": 3}  # => matches example.py's own Output exactly


# => Run: pytest -- Output: 2 passed
