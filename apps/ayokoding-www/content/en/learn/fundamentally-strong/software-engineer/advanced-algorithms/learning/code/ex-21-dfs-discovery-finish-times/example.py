"""Example 21: DFS with Colors and Discovery/Finish Timestamps."""

# CLRS-style DFS (co-17) stamps each node with a discovery time (when first
# seen, color WHITE->GRAY) and a finish time (when fully explored, GRAY->
# BLACK). The parenthesis theorem: any two nodes' [disc, fin] intervals are
# either NESTED (one fully inside the other) or DISJOINT -- never partially
# overlapping, because a node can't finish before all its descendants do.
from enum import Enum, auto


class Color(Enum):  # => the three DFS visitation states
    WHITE = auto()  # => not yet discovered
    GRAY = auto()  # => discovered, still exploring its neighbors
    BLACK = auto()  # => fully finished -- this node and all descendants are done


def dfs_timestamps(
    graph: dict[str, list[str]], start: str
) -> tuple[dict[str, int], dict[str, int]]:  # => (discovery times, finish times)
    color: dict[str, Color] = {
        node: Color.WHITE for node in graph
    }  # => everyone starts WHITE
    disc: dict[str, int] = {}  # => node -> the tick it was first discovered
    fin: dict[str, int] = {}  # => node -> the tick it was fully finished
    clock = [0]  # => a one-element list used as a mutable counter inside the closure

    def recurse(node: str) -> None:  # => the recursive DFS visit itself
        color[node] = Color.GRAY  # => marks node as "in progress"
        disc[node] = clock[0]  # => stamps the CURRENT tick as node's discovery time
        clock[0] += 1  # => advances the shared clock
        for neighbor in graph.get(node, []):  # => tries every outgoing edge
            if (
                color[neighbor] == Color.WHITE
            ):  # => only recurse into undiscovered nodes
                recurse(neighbor)  # => explores neighbor fully before returning
        color[node] = Color.BLACK  # => marks node as "fully explored"
        fin[node] = clock[0]  # => stamps the CURRENT tick as node's finish time
        clock[0] += 1  # => advances the shared clock again

    recurse(start)  # => kicks off the timestamped DFS
    return disc, fin  # => both timestamp maps, ready for the nesting check below


def intervals_are_nested_or_disjoint(
    disc: dict[str, int], fin: dict[str, int]
) -> bool:  # => the parenthesis-theorem check itself
    nodes = list(disc.keys())  # => every DFS-visited node
    for i, u in enumerate(nodes):  # => compares every unordered PAIR of nodes once
        for v in nodes[i + 1 :]:  # => avoids comparing a node against itself or twice
            u_before_v = fin[u] < disc[v]  # => u's interval ends before v's even starts
            v_before_u = fin[v] < disc[u]  # => the mirror case: v ends before u starts
            u_contains_v = disc[u] < disc[v] and fin[v] < fin[u]  # => v nested in u
            v_contains_u = disc[v] < disc[u] and fin[u] < fin[v]  # => u nested in v
            if not (
                u_before_v or v_before_u or u_contains_v or v_contains_u
            ):  # => none of the four valid shapes matched -- a partial overlap!
                return False  # => the parenthesis theorem was violated
    return True  # => every pair is cleanly nested or disjoint


graph: dict[str, list[str]] = {  # => a small directed graph with a branch and a merge
    "a": ["b", "c"],
    "b": ["d"],
    "c": ["d"],
    "d": [],
}
disc, fin = dfs_timestamps(graph, "a")  # => runs the timestamped DFS from "a"
print(disc)  # => Output: {'a': 0, 'b': 1, 'd': 2, 'c': 5}
print(fin)  # => Output: {'d': 3, 'b': 4, 'c': 6, 'a': 7}

assert disc["a"] == 0  # => the start node is always discovered first, at tick 0
assert fin["a"] == max(
    fin.values()
)  # => the start node's subtree covers everything -- it finishes LAST
assert intervals_are_nested_or_disjoint(
    disc, fin
)  # => confirms the parenthesis theorem holds for this DFS run
print("ex-21 OK")  # => Output: ex-21 OK
