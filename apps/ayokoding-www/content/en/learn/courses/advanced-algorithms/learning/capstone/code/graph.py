"""Capstone: algorithm workbench -- DAG model, BFS/DFS, and topological sort.

Time/space complexity per routine (n = nodes, e = edges), all O(n) extra space
unless noted:

- ``build_graph``: O(n + e) -- one pass to seed every node, one pass per edge.
- ``bfs_order`` / ``dfs_order``: O(n + e) each -- every node visited once,
  every edge relaxed at most once.
- ``reachable_nodes``: O(n + e) -- a thin wrapper over ``bfs_order``.
- ``topological_sort`` (Kahn's algorithm): O(n + e); a cycle is detected as a
  by-product of the SAME pass, at O(1) marginal cost (the length check at the
  end) -- no separate cycle-detection algorithm is needed.
"""

from __future__ import annotations

from collections import deque

Graph = dict[str, list[str]]


class GraphCycleError(Exception):
    """Raised when topological_sort is asked to order a graph containing a cycle."""


def build_graph(nodes: list[str], edges: list[tuple[str, str]]) -> Graph:
    """Build a directed adjacency-list graph -- O(n + e).

    Every node in `nodes` gets a key, even one with zero out-edges -- so
    isolated nodes are never silently dropped. That is what lets
    `topological_sort` handle a disconnected graph correctly.
    """
    graph: Graph = {
        node: [] for node in nodes
    }  # => O(n): every node present, even isolated ones
    for src, dst in edges:  # => O(e): one pass over the edge list
        if (
            src not in graph or dst not in graph
        ):  # => O(1) average dict membership check
            raise KeyError(f"edge ({src!r}, {dst!r}) references an unknown node")
        graph[src].append(dst)  # => src -> dst, a directed "must run before" edge
    return graph


def bfs_order(graph: Graph, start: str) -> list[str]:
    """Breadth-first visit order reachable from `start` -- O(n + e)."""
    visited: set[str] = {
        start
    }  # => marks start visited BEFORE enqueueing, so it is never re-enqueued
    order: list[str] = []
    queue: deque[str] = deque([start])
    while queue:  # => drains the queue; every node enqueued at most once
        node = queue.popleft()  # => FIFO: nodes come out nearest-hop-count-first
        order.append(node)
        for neighbor in graph[node]:  # => O(e) total across the whole traversal
            if neighbor not in visited:
                visited.add(neighbor)  # => mark visited on DISCOVERY, not on dequeue
                queue.append(neighbor)
    return order


def dfs_order(graph: Graph, start: str) -> list[str]:
    """Depth-first visit order reachable from `start`, iterative -- O(n + e).

    Uses an explicit stack instead of recursion, so it never risks Python's
    recursion-depth limit on a long dependency chain.
    """
    visited: set[str] = set()
    order: list[str] = []
    stack: list[str] = [start]
    while (
        stack
    ):  # => LIFO: nodes are visited depth-first, unlike bfs_order's breadth-first
        node = stack.pop()
        if (
            node in visited
        ):  # => a node can be pushed more than once before it is popped
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(
            graph[node]
        ):  # => reversed so the FIRST-listed neighbor is popped FIRST
            if neighbor not in visited:
                stack.append(neighbor)
    return order


def reachable_nodes(graph: Graph, start: str) -> set[str]:
    """The set of nodes reachable from `start` -- O(n + e); built on `bfs_order`."""
    return set(
        bfs_order(graph, start)
    )  # => reuses bfs_order; reachability itself never needs the visit ORDER


def topological_sort(graph: Graph) -> list[str]:
    """Kahn's algorithm: a valid dependency order, or `GraphCycleError` -- O(n + e).

    An empty graph returns `[]`. Isolated nodes and disconnected components are
    both handled correctly -- Kahn's algorithm only tracks in-degree, never
    connectivity, so a graph with two unrelated components still produces one
    combined valid order.
    """
    in_degree: dict[str, int] = {node: 0 for node in graph}  # => O(n) init
    for node in graph:  # => O(n) outer pass
        for neighbor in graph[node]:  # => O(e) total
            in_degree[neighbor] += 1
    ready: deque[str] = deque(
        sorted(node for node in graph if in_degree[node] == 0)
    )  # => sorted so ties among equally-ready nodes are DETERMINISTIC (test-stable)
    order: list[str] = []
    while ready:  # => each node enqueued/dequeued at most once, O(n) total
        node = ready.popleft()
        order.append(node)
        for neighbor in graph[node]:  # => O(e) total across the whole sort
            in_degree[neighbor] -= 1
            if (
                in_degree[neighbor] == 0
            ):  # => neighbor's LAST unresolved dependency just cleared
                ready.append(neighbor)
    if len(order) != len(
        graph
    ):  # => O(1): fewer emissions than nodes means a cycle exists
        stuck = sorted(
            node for node in graph if node not in order
        )  # => diagnostics only
        raise GraphCycleError(f"cycle detected among: {', '.join(stuck)}")
    return order
