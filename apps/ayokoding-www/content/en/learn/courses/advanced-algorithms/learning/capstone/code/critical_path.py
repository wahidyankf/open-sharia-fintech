"""Capstone: critical-path DP over the DAG `graph.py`'s topological_sort produces.

Time/space complexity (n = nodes, e = edges):

- ``critical_path``: O(n + e) -- one `topological_sort` pass (O(n + e)) plus
  one DP pass that visits every node once and every predecessor edge once.
"""

from __future__ import annotations

from graph import Graph, topological_sort


def critical_path(
    graph: Graph, durations: dict[str, int]
) -> tuple[int, dict[str, int], dict[str, int]]:
    """DP longest path (the "critical path") over a DAG -- O(n + e).

    Returns `(project_length, earliest_start, earliest_finish)`. An empty
    graph returns `(0, {}, {})`. Propagates `GraphCycleError` (from
    `graph.py`) unchanged if the input graph is not actually a DAG.
    """
    order = topological_sort(
        graph
    )  # => O(n + e); every predecessor precedes its dependents
    if not order:  # => O(1): the empty-graph edge case
        return 0, {}, {}

    predecessors: dict[str, list[str]] = {node: [] for node in graph}  # => O(n) init
    for node in graph:  # => O(n) outer pass
        for neighbor in graph[node]:  # => O(e) total, reverses each edge exactly once
            predecessors[neighbor].append(node)  # => node feeds INTO neighbor

    earliest_start: dict[str, int] = {}
    earliest_finish: dict[str, int] = {}
    for node in order:  # => the DP pass itself, strictly in topological order
        earliest_start[node] = (
            max(  # => can't start before EVERY predecessor has finished
                (earliest_finish[pred] for pred in predecessors[node]), default=0
            )
        )  # => default=0: no predecessors means this node can start at time 0
        earliest_finish[node] = earliest_start[node] + durations[node]
    project_length = max(earliest_finish.values())  # => the longest finish time overall
    return project_length, earliest_start, earliest_finish
