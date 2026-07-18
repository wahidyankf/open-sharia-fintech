"""Example 66: pytest verification for Kosaraju's SCC Algorithm."""

from example import strongly_connected_components


def test_two_disjoint_cycles_form_two_components() -> None:
    graph: dict[str, list[str]] = {
        "a": ["b"],
        "b": ["c"],
        "c": ["a", "d"],
        "d": ["e"],
        "e": ["d"],
    }
    components = strongly_connected_components(graph)
    sets = [set(c) for c in components]
    assert len(components) == 2
    assert {"a", "b", "c"} in sets
    assert {"d", "e"} in sets


def test_a_dag_has_every_node_as_its_own_singleton_component() -> None:
    graph: dict[str, list[str]] = {"x": ["y"], "y": ["z"], "z": []}
    components = strongly_connected_components(graph)
    assert len(components) == 3  # => no cycles at all -- every node is its own SCC


def test_a_fully_cyclic_graph_is_one_single_component() -> None:
    graph: dict[str, list[str]] = {"p": ["q"], "q": ["r"], "r": ["p"]}
    components = strongly_connected_components(graph)
    assert len(components) == 1
    assert set(components[0]) == {"p", "q", "r"}


# => Run: pytest -- Output: 3 passed
