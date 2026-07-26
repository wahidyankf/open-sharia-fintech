"""Example 22: pytest verification for B+-Tree Values-in-Leaves."""

from example import InternalNode, LeafNode, has_any_value


def test_internal_node_has_no_entries_attribute() -> None:
    node = InternalNode(keys=[5], children=[])
    assert not hasattr(node, "entries")


def test_values_are_reachable_through_leaves() -> None:
    leaf = LeafNode(entries={1: "one"})
    root = InternalNode(keys=[1], children=[leaf])
    assert has_any_value(root) is True


# => Run: pytest -- Output: 2 passed
