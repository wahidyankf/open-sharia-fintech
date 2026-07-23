"""Example 43: Dataflow Topological Execute."""

from collections.abc import Callable  # => types every node's compute formula stored below

Node = str  # => a type alias -- node names are just strings
graph: dict[Node, list[Node]] = {  # => DAG of value dependencies: node -> nodes it depends on
    "c": ["a", "b"],  # => c depends on a and b
    "b": ["a"],  # => b depends on a
    "a": [],  # => a has no dependencies -- a source node
}  # => closes the dependency graph declaration
formulas: dict[Node, Callable[[dict[Node, int]], int]] = {  # => how to compute each node, given results so far
    "a": lambda results: 1,  # => a is a constant
    "b": lambda results: results["a"] + 1,  # => b = a + 1
    "c": lambda results: results["a"] + results["b"],  # => c = a + b
}  # => closes the per-node formula table


def topological_order(deps: dict[Node, list[Node]]) -> list[Node]:  # => order respecting every dependency
    visited: set[Node] = set()  # => nodes already placed in the order
    order: list[Node] = []  # => the order being built

    def visit(node: Node) -> None:  # => depth-first visit: dependencies before the node itself
        if node in visited:  # => already placed -- nothing to do
            return  # => stops the recursion for this branch -- a node is never appended twice
        visited.add(node)  # => mark BEFORE recursing to guard against revisiting a node mid-traversal
        for dep in deps[node]:  # => every dependency must appear in the order first
            visit(dep)  # => recurse into the dependency
        order.append(node)  # => only append AFTER all dependencies are already in `order`

    for node in deps:  # => make sure every node gets visited, regardless of starting point
        visit(node)  # => already-visited nodes short-circuit immediately via the check above
    return order  # => a valid topological order: every dependency precedes its dependents


order = topological_order(graph)  # => compute the execution order
print(order)  # => a must come before b and c; b must come before c
# => Output: ['a', 'b', 'c']

results: dict[Node, int] = {}  # => accumulate computed values as we execute in order
for node in order:  # => execute strictly in topological order
    results[node] = formulas[node](results)  # => by the time we reach a node, its deps are already computed
print(results)  # => a=1, b=1+1=2, c=1+2=3
# => Output: {'a': 1, 'b': 2, 'c': 3}
