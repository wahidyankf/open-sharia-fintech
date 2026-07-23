# learning/code/ex-23-cycle-detection-dfs/cycle_detection.py
"""Example 23: Cycle Detection in a Directed Graph via DFS Colors."""  # => co-13: this file's own restated purpose, doubling as its module __doc__

from __future__ import annotations  # => DD-39 hygiene: postpones type-annotation evaluation, keeping this file interpreter-version-agnostic

WHITE, GRAY, BLACK = 0, 1, 2  # => co-13: unvisited, ON THE CURRENT DFS PATH, and fully-finished


def has_cycle(graph: dict[str, list[str]]) -> bool:  # => co-13: True iff a back-edge to a GRAY vertex is found
    """Detect a cycle in a directed graph using the classic white/gray/black DFS coloring."""  # => co-13: documents has_cycle's contract -- no runtime output, just sets its __doc__
    color: dict[str, int] = {v: WHITE for v in graph}  # => co-13: every vertex starts unvisited

    def visit(u: str) -> bool:  # => co-13: DFS from u -- returns True the instant a back-edge is found
        color[u] = GRAY  # => co-13: u is now ON the current recursion path (an "in-progress" vertex)
        for v in graph.get(u, []):  # => co-13: explore every outgoing edge from u
            if color[v] == GRAY:  # => co-13: v is an ANCESTOR on the current path -- this IS a back-edge
                return True  # => co-13: back-edge to a GRAY vertex means a cycle -- the defining test
            if color[v] == WHITE and visit(v):  # => co-13: recurse only into unvisited vertices
                return True  # => co-13: propagate a cycle found deeper in the recursion
        color[u] = BLACK  # => co-13: u is fully explored -- no path through it leads back to itself
        return False  # => co-13: no back-edge found anywhere below u

    return any(visit(v) for v in graph if color[v] == WHITE)  # => co-13: start DFS from every unvisited vertex


if __name__ == "__main__":  # => co-13: entry point -- this block runs only when the file executes directly, not on import
    cyclic_graph = {"A": ["B"], "B": ["C"], "C": ["A"]}  # => co-13: A -> B -> C -> A, a textbook 3-cycle
    acyclic_graph = {"A": ["B"], "B": ["C"], "C": []}  # => co-13: the SAME shape with the closing edge removed
    cyclic_result = has_cycle(cyclic_graph)  # => co-13: expect True -- the closing C->A edge is a back-edge
    acyclic_result = has_cycle(acyclic_graph)  # => co-13: expect False -- no path returns to an ancestor
    print(f"cyclic_graph {cyclic_graph} -> has_cycle = {cyclic_result}")  # => co-13: prints the cyclic case
    print(f"acyclic_graph {acyclic_graph} -> has_cycle = {acyclic_result}")  # => co-13: prints the acyclic case
    assert cyclic_result is True, "A->B->C->A must be flagged as cyclic"  # => co-13: the known cyclic case
    assert acyclic_result is False, "A->B->C (no closing edge) must NOT be flagged as cyclic"  # => co-13
    print(f"Cyclic graph flagged, acyclic graph not flagged: True")  # => co-13: both asserts above passed
    # => co-13: the asserts above ARE this example's test suite -- a silent, zero-exit run is the proof the concept holds
