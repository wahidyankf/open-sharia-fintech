"""Example 80: pytest verification for the Threaded Mini Scheduler."""

from example import critical_path_schedule, dijkstra_shortest_paths, topological_order


def test_topological_order_respects_every_dependency_edge() -> None:
    graph: dict[str, list[str]] = {"a": ["b", "c"], "b": ["d"], "c": ["d"], "d": []}
    order = topological_order(graph)
    assert order.index("a") < order.index("b")  # => "a" MUST come before its dependents
    assert order.index("a") < order.index("c")
    assert order.index("b") < order.index("d")
    assert order.index("c") < order.index("d")


def test_critical_path_schedule_matches_a_hand_computed_project() -> None:
    graph: dict[str, list[str]] = {"a": ["b"], "b": ["c"], "c": []}
    durations: dict[str, int] = {"a": 2, "b": 3, "c": 1}
    total, starts, finishes = critical_path_schedule(graph, durations)
    assert total == 6  # => a single chain: 2 + 3 + 1
    assert starts == {"a": 0, "b": 2, "c": 5}
    assert finishes == {"a": 2, "b": 5, "c": 6}


def test_dijkstra_shortest_paths_finds_the_cheaper_of_two_routes() -> None:
    graph: dict[str, list[tuple[str, int]]] = {
        "start": [("mid", 1), ("end", 10)],
        "mid": [("start", 1), ("end", 1)],
        "end": [("mid", 1), ("start", 10)],
    }
    distances = dijkstra_shortest_paths(graph, "start")
    assert (
        distances["end"] == 2
    )  # => via "mid" (1+1), cheaper than the direct edge (10)


# => Run: pytest -- Output: 3 passed
