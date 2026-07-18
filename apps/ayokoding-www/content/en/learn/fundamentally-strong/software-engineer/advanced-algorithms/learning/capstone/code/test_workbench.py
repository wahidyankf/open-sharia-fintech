"""pytest coverage for workbench.py -- the full topo + DP + Dijkstra pipeline, end to end."""

from workbench import run_workbench


def test_run_workbench_matches_example_80s_hand_verified_numbers() -> None:
    order, project_length, earliest_start, travel_time, feasible = run_workbench()

    assert set(order) == {"design", "build_a", "build_b", "test"}
    assert order.index("design") < order.index(
        "build_a"
    )  # => dependency order respected
    assert order.index("design") < order.index("build_b")
    assert order.index("build_a") < order.index("test")
    assert order.index("build_b") < order.index("test")

    assert (
        project_length == 12
    )  # => matches Example 80's hand-verified critical path length
    assert earliest_start == {"design": 0, "build_a": 3, "build_b": 3, "test": 8}
    assert travel_time["L3"] == 5.0  # => matches Example 80's Dijkstra answer
    assert feasible is True
