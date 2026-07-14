"""Example 58: Depth-First Search over a Graph."""

# DFS plunges as deep as possible down ONE path before backtracking -- the
# recursive call stack itself acts as the "stack" (co-21, co-17, co-09).
graph: dict[str, list[str]] = {  # => the same 4-node graph as Example 56
    "a": ["b", "c"],  # => a's neighbors
    "b": ["a", "d"],  # => b's neighbors
    "c": ["a", "d"],  # => c's neighbors
    "d": ["b", "c"],  # => d's neighbors
}  # => four keys total, each mapping to its own neighbor list


# Visits node, then recurses fully into the FIRST unvisited neighbor before any other.
def dfs(
    graph: dict[str, list[str]], node: str, visited: set[str], order: list[str]
) -> None:
    visited.add(node)  # => marks node as seen -- prevents infinite loops on cycles
    order.append(node)  # => records visit order for inspection
    for neighbor in graph[node]:  # => tries each neighbor in listed order
        if neighbor not in visited:  # => O(1) average membership check
            dfs(
                graph, neighbor, visited, order
            )  # => RECURSIVE CASE: plunge deeper first


visited: set[str] = (
    set()
)  # => shared across the whole traversal via the same set object
order: list[str] = []  # => shared across the whole traversal via the same list object
dfs(
    graph, "a", visited, order
)  # => a -> b (first neighbor) -> d (b's unvisited neighbor) -> c
print(order)  # => Output: ['a', 'b', 'd', 'c']

assert order == ["a", "b", "d", "c"]  # => confirms the exact depth-first visit order
assert visited == {"a", "b", "c", "d"}  # => confirms every node was eventually visited
print("ex-58 OK")  # => Output: ex-58 OK
