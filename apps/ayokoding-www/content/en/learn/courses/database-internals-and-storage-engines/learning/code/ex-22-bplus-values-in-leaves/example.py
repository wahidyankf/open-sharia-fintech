"""Example 22: B+-Tree -- Values Live Only in Leaves."""

from dataclasses import dataclass  # => plain, typed records for both node kinds


@dataclass
class LeafNode:  # => the ONLY place a key-value pair actually lives
    entries: dict[int, str]  # => key -> value, the real data this tree stores


@dataclass
class InternalNode:  # => carries ROUTING keys only -- no values, ever
    keys: list[int]  # => separator keys used to pick which child to descend into
    children: list["InternalNode | LeafNode"]  # => one more child than there are keys


# A B+-tree keeps values EXCLUSIVELY in leaves; internal nodes hold only
# routing keys used to steer a search downward (co-07) -- unlike a classical
# B-tree, which may store a value at any node, including internal ones.
leaf1 = LeafNode(entries={10: "row-10", 20: "row-20"})  # => the LEFT leaf's real data
leaf2 = LeafNode(entries={30: "row-30", 40: "row-40"})  # => the RIGHT leaf's real data
root = InternalNode(
    keys=[30], children=[leaf1, leaf2]
)  # => keys route; children hold the real data


def has_any_value(
    node: "InternalNode | LeafNode",
) -> bool:  # => walks the whole tree checking the rule
    if isinstance(
        node, LeafNode
    ):  # => base case: a leaf either has entries or it doesn't
        return len(node.entries) > 0
    return any(
        has_any_value(child) for child in node.children
    )  # => recurse: true if ANY child has values


assert not hasattr(
    root, "entries"
)  # => the internal node has NO entries field -- values physically can't live there
assert has_any_value(
    root
)  # => but the tree AS A WHOLE does hold values -- all of them inside its leaves
print(root.keys)  # => Output: [30]
print(leaf1.entries)  # => Output: {10: 'row-10', 20: 'row-20'}
# => root.keys routes a search; leaf1.entries and leaf2.entries hold the actual rows
print("ex-22 OK")  # => Output: ex-22 OK
