"""Example 21: DFS with Colors and Discovery/Finish Timestamps."""

# CLRS-style DFS (co-17) stamps each node with a discovery time (when first
# seen, color WHITE->GRAY) and a finish time (when fully explored, GRAY->
# BLACK). The parenthesis theorem: any two nodes' [disc, fin] intervals are
# either NESTED (one fully inside the other) or DISJOINT -- never partially
# overlapping, because a node can't finish before all its descendants do.
from enum import Enum, auto  # => Color is an Enum, not a bare string, for type safety


class Color(Enum):  # => the three DFS visitation states
    WHITE = auto()  # => not yet discovered
    GRAY = auto()  # => discovered, still exploring its neighbors
    BLACK = auto()  # => fully finished -- this node and all descendants are done


def dfs_timestamps(  # => CLRS-style DFS that stamps a discovery and finish tick per node
    graph: dict[str, list[str]],  # => the adjacency map to traverse
    start: str,  # => adjacency map plus the origin node
) -> tuple[dict[str, int], dict[str, int]]:  # => (discovery times, finish times)
    color: dict[str, Color] = {  # => opens the dict-comprehension initializing colors
        node: Color.WHITE
        for node in graph  # => every node starts undiscovered
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


def intervals_are_nested_or_disjoint(  # => checks all C(n,2) node pairs, O(n^2) total
    disc: dict[str, int],
    fin: dict[str, int],  # => the two timestamp maps to validate
) -> bool:  # => the parenthesis-theorem check itself
    nodes = list(disc.keys())  # => every DFS-visited node
    for i, u in enumerate(nodes):  # => compares every unordered PAIR of nodes once
        for v in nodes[i + 1 :]:  # => avoids comparing a node against itself or twice
            # => exactly one of the four shapes below must hold for a valid DFS run

            u_before_v = fin[u] < disc[v]  # => u's interval ends before v's even starts
            v_before_u = fin[v] < disc[u]  # => the mirror case: v ends before u starts
            u_contains_v = disc[u] < disc[v] and fin[v] < fin[u]  # => v nested in u
            v_contains_u = disc[v] < disc[u] and fin[u] < fin[v]  # => u nested in v
            if not (  # => opens the "none of the four valid shapes held" check
                u_before_v or v_before_u or u_contains_v or v_contains_u
            ):  # => none of the four valid shapes matched -- a partial overlap!
                return False  # => the parenthesis theorem was violated
    return True  # => every pair is cleanly nested or disjoint


graph: dict[str, list[str]] = {  # => a small directed graph with a branch and a merge
    "a": ["b", "c"],  # => the root -- branches into both "b" and "c"
    "b": ["d"],  # => "b"'s only outgoing edge merges back into "d"
    "c": ["d"],  # => "c" also merges into "d", after "b"'s subtree already finished
    "d": [],  # => the merge point -- a sink node with no outgoing edges
}  # => closes the adjacency map -- 4 nodes, one branch-and-merge diamond
# runs the full timestamped DFS from "a" once, producing both timestamp maps
disc, fin = dfs_timestamps(graph, "a")  # => runs the timestamped DFS from "a"
print(disc)  # => Output: {'a': 0, 'b': 1, 'd': 2, 'c': 5}
print(fin)  # => Output: {'d': 3, 'b': 4, 'c': 6, 'a': 7}

assert disc["a"] == 0  # => the start node is always discovered first, at tick 0
assert fin["a"] == max(  # => opens the "a finishes last" comparison
    fin.values()  # => every node's finish tick, to find the overall maximum
)  # => the start node's subtree covers everything -- it finishes LAST
assert intervals_are_nested_or_disjoint(  # => opens the parenthesis-theorem check
    disc,
    fin,  # => passes both timestamp maps collected during the DFS run above
)  # => confirms the parenthesis theorem holds for this DFS run
print("ex-21 OK")  # => Output: ex-21 OK
