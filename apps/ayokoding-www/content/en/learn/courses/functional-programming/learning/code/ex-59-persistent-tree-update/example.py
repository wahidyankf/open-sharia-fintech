"""Example 59: A Persistent Binary Tree With a Structural-Sharing Update."""

from __future__ import (
    annotations,
)  # => enables the quoted 'Tree | None' forward references below

from dataclasses import (
    dataclass,
)  # => @dataclass(frozen=True) builds the immutable Tree node


@dataclass(frozen=True)  # => an immutable binary search tree node
class Tree:  # => the node type itself
    value: int  # => this node's own value
    left: "Tree | None"  # => the left subtree, or None
    right: "Tree | None"  # => the right subtree, or None


def insert(
    tree: "Tree | None", value: int
) -> Tree:  # => builds a NEW path, reuses the rest
    if tree is None:  # => base case: an empty spot becomes a new leaf
        return Tree(value=value, left=None, right=None)  # => the freshly-created leaf
    if value < tree.value:  # => goes left -- only the LEFT spine gets rebuilt
        return Tree(
            value=tree.value, left=insert(tree.left, value), right=tree.right
        )  # => right subtree REUSED
    if value > tree.value:  # => goes right -- only the RIGHT spine gets rebuilt
        return Tree(
            value=tree.value, left=tree.left, right=insert(tree.right, value)
        )  # => left subtree REUSED
    return tree  # => value already present -- no change needed, return the SAME node


def to_sorted_list(
    tree: "Tree | None",
) -> list[int]:  # => in-order walk, for verification only
    if tree is None:  # => base case: an empty subtree contributes nothing
        return []  # => an empty list, the recursion's base result
    return (
        to_sorted_list(tree.left) + [tree.value] + to_sorted_list(tree.right)
    )  # => left, self, right


root_a = insert(insert(insert(None, 5), 3), 8)  # => builds {5: left=3, right=8}
root_b = insert(root_a, 1)  # => inserts 1, which goes LEFT of 3

# => persistent trees generalize the persistent list's O(1)-sharing idea to branching structures
print(to_sorted_list(root_a))  # => Output: [3, 5, 8]
print(to_sorted_list(root_b))  # => Output: [1, 3, 5, 8]
print(
    root_b.right is root_a.right
)  # => Output: True -- the untouched right subtree (8) is REUSED
