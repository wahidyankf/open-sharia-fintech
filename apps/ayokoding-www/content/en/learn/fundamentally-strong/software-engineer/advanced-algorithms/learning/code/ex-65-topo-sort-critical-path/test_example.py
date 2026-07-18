"""Example 65: pytest verification for Critical Path DP."""

from example import critical_path_length


def test_matches_a_hand_computed_schedule() -> None:
    graph: dict[str, list[str]] = {
        "design": ["build_a", "build_b"],
        "build_a": ["test"],
        "build_b": ["test"],
        "test": [],
    }
    durations: dict[str, int] = {"design": 3, "build_a": 5, "build_b": 2, "test": 4}
    total, finishes = critical_path_length(graph, durations)
    assert total == 12
    assert finishes["build_a"] == 8


def test_single_chain_sums_durations_exactly() -> None:
    graph: dict[str, list[str]] = {"a": ["b"], "b": ["c"], "c": []}
    durations: dict[str, int] = {"a": 1, "b": 2, "c": 3}
    total, _ = critical_path_length(graph, durations)
    assert total == 6  # => a single chain: no branching, just a straight sum


def test_task_with_no_predecessors_starts_at_time_zero() -> None:
    graph: dict[str, list[str]] = {"solo": []}
    durations: dict[str, int] = {"solo": 7}
    total, finishes = critical_path_length(graph, durations)
    assert total == 7
    assert finishes["solo"] == 7


# => Run: pytest -- Output: 3 passed
