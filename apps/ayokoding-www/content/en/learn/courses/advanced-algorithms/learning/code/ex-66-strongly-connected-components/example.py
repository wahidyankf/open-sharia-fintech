"""Example 66: Strongly Connected Components via Kosaraju's Two-Pass DFS."""

# Kosaraju's algorithm (co-17, co-18) is a clever two-pass trick: DFS the
# ORIGINAL graph, recording finish order (like Example 36's topo sort);
# then DFS the TRANSPOSED graph (every edge reversed), processing nodes in
# REVERSE finish order -- each tree that DFS grows is exactly one SCC.


def transpose(graph: dict[str, list[str]]) -> dict[str, list[str]]:  # => reverses edges
    reversed_graph: dict[str, list[str]] = {
        node: [] for node in graph
    }  # => same nodes, no edges yet
    for u in graph:  # => scans every node's outgoing edges
        for v in graph[u]:  # => each original edge u->v
            reversed_graph[v].append(u)  # => flips u->v into v->u
    return reversed_graph  # => same nodes, every edge direction reversed


def dfs_finish_order(  # => PASS 1: records DFS finish order over the ORIGINAL graph
    graph: dict[str, list[str]],  # => the original adjacency-list graph
) -> list[str]:  # => same idea as Ex. 36
    visited: set[str] = set()  # => nodes already fully explored
    finish_order: list[str] = []  # => nodes in the order their DFS subtree COMPLETES

    def recurse(node: str) -> None:  # => explores node's subtree before recording it
        visited.add(node)  # => marks node as being explored
        for neighbor in graph.get(node, []):  # => tries every outgoing edge
            if neighbor not in visited:  # => only recurse into UNEXPLORED neighbors
                recurse(neighbor)  # => fully explores that neighbor's subtree first
        finish_order.append(node)  # => appended only after all descendants finish

    for node in graph:  # => ensures every node gets visited, even disconnected ones
        if node not in visited:  # => starts a fresh DFS from any unvisited node
            recurse(node)  # => explores that node's entire reachable subtree
    return finish_order  # => PASS 1's output: nodes ordered by DFS finish time


def strongly_connected_components(  # => the two-pass Kosaraju driver
    graph: dict[str, list[str]],  # => the original adjacency-list graph
) -> list[list[str]]:  # => Kosaraju's algorithm, O(V+E)
    finish_order = dfs_finish_order(graph)  # => PASS 1: DFS the original graph
    reversed_graph = transpose(graph)  # => build the transposed graph once
    visited: set[str] = set()  # => nodes already assigned to a component
    components: list[list[str]] = []  # => each entry is one full SCC

    def recurse(node: str, component: list[str]) -> None:  # => grows one component
        visited.add(node)  # => marks node as assigned
        component.append(node)  # => this node belongs to the CURRENT component
        for neighbor in reversed_graph.get(node, []):  # => tries every REVERSED edge
            if neighbor not in visited:  # => only recurse into UNASSIGNED neighbors
                recurse(neighbor, component)  # => grows the same component further

    for node in reversed(  # => opens the reverse-finish-order iteration
        finish_order  # => PASS 1's output, walked back to front
    ):  # => PASS 2: REVERSE finish order, on the reversed graph
        if node not in visited:  # => this node starts a BRAND NEW component
            component: list[str] = []  # => a fresh SCC, seeded by this unvisited node
            recurse(node, component)  # => the ENTIRE reachable set here is one SCC
            components.append(component)  # => records the completed component
    return components  # => every node's SCC, as a list of node lists


graph: dict[str, list[str]] = {  # => a known digraph with two clear SCCs
    "a": ["b"],  # => a points to b
    "b": ["c"],  # => b points to c
    "c": ["a", "d"],  # => a->b->c->a is a cycle: {a, b, c} form one SCC
    "d": ["e"],  # => d points to e
    "e": ["d"],  # => d->e->d is a cycle: {d, e} form another SCC
}  # => closes the graph literal
components = strongly_connected_components(graph)  # => Kosaraju's SCC decomposition
component_sets = [set(c) for c in components]  # => order-independent comparison
print(len(components))  # => Output: 2

assert len(components) == 2  # => confirms exactly two SCCs were found
assert {"a", "b", "c"} in component_sets  # => confirms the first cycle is one SCC
assert {"d", "e"} in component_sets  # => confirms the second cycle is another SCC
print("ex-66 OK")  # => Output: ex-66 OK
