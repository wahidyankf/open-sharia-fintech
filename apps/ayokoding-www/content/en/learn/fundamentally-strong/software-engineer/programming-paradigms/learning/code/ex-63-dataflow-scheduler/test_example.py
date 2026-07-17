"""Example 63: pytest verification for Dataflow Scheduler (Parallel-Ready Batches)."""

import pytest

from example import schedule_batches


def test_correct_order_under_a_dependency_chain() -> None:
    graph = {"d": ["b", "c"], "c": ["a"], "b": ["a"], "a": []}  # => same graph as the module-level demo
    batches = schedule_batches(graph)
    assert batches == [["a"], ["b", "c"], ["d"]]  # => three waves, b and c genuinely parallel-ready together


def test_every_node_in_a_batch_has_no_unmet_dependency_within_that_batch() -> None:
    graph = {"d": ["b", "c"], "c": ["a"], "b": ["a"], "a": []}
    batches = schedule_batches(graph)
    scheduled: set[str] = set()  # => nodes scheduled in EARLIER batches only
    for batch in batches:
        for node in batch:
            assert set(graph[node]).issubset(scheduled)  # => every dependency already ran in a prior wave
        scheduled.update(batch)


def test_a_cyclic_graph_raises_instead_of_hanging() -> None:
    cyclic = {"x": ["y"], "y": ["x"]}  # => x depends on y and y depends on x -- no valid schedule exists
    with pytest.raises(ValueError):
        schedule_batches(cyclic)


# => Run: pytest -- Output: 3 passed
