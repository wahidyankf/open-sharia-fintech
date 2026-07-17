"""Example 66: Strongly Connected Components via Kosaraju's Two-Pass DFS."""

# Kosaraju's algorithm (co-17, co-18) is a clever two-pass trick: DFS the
# ORIGINAL graph, recording finish order (like Example 36's topo sort);
# then DFS the TRANSPOSED graph (every edge reversed), processing nodes in
# REVERSE finish order -- each tree that DFS grows is exactly one SCC.


def transpose(graph: dict[str, list[str]]) -> dict[str, list[str]]:  # => reverses edges
    reversed_graph: dict[str, list[str]] = {node: [] for node in graph}
    for u in graph:
        for v in graph[u]:
            reversed_graph[v].append(u)  # => flips u->v into v->u
    return reversed_graph  # => same nodes, every edge direction reversed


def dfs_finish_order(
    graph: dict[str, list[str]],
) -> list[str]:  # => same idea as Ex. 36
    visited: set[str] = set()
    finish_order: list[str] = []

    def recurse(node: str) -> None:
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                recurse(neighbor)
        finish_order.append(node)  # => appended only after all descendants finish

    for node in graph:
        if node not in visited:
            recurse(node)
    return finish_order


def strongly_connected_components(
    graph: dict[str, list[str]],
) -> list[list[str]]:  # => Kosaraju's algorithm, O(V+E)
    finish_order = dfs_finish_order(graph)  # => PASS 1: DFS the original graph
    reversed_graph = transpose(graph)  # => build the transposed graph once
    visited: set[str] = set()
    components: list[list[str]] = []  # => each entry is one full SCC

    def recurse(node: str, component: list[str]) -> None:
        visited.add(node)
        component.append(node)  # => this node belongs to the CURRENT component
        for neighbor in reversed_graph.get(node, []):
            if neighbor not in visited:
                recurse(neighbor, component)  # => grows the same component further

    for node in reversed(
        finish_order
    ):  # => PASS 2: REVERSE finish order, on the reversed graph
        if node not in visited:
            component: list[str] = []  # => a fresh SCC, seeded by this unvisited node
            recurse(node, component)  # => the ENTIRE reachable set here is one SCC
            components.append(component)  # => records the completed component
    return components  # => every node's SCC, as a list of node lists


graph: dict[str, list[str]] = {  # => a known digraph with two clear SCCs
    "a": ["b"],
    "b": ["c"],
    "c": ["a", "d"],  # => a->b->c->a is a cycle: {a, b, c} form one SCC
    "d": ["e"],
    "e": ["d"],  # => d->e->d is a cycle: {d, e} form another SCC
}
components = strongly_connected_components(graph)  # => Kosaraju's SCC decomposition
component_sets = [set(c) for c in components]  # => order-independent comparison
print(len(components))  # => Output: 2

assert len(components) == 2  # => confirms exactly two SCCs were found
assert {"a", "b", "c"} in component_sets  # => confirms the first cycle is one SCC
assert {"d", "e"} in component_sets  # => confirms the second cycle is another SCC
print("ex-66 OK")  # => Output: ex-66 OK
