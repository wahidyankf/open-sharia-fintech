"""Example 40: A Custom __iter__ Walks a Binary Tree In Order."""

from collections.abc import Iterator  # => imports Iterator from collections.abc


class Node:  # => a single binary tree node -- NOT itself iterable
    def __init__(self, value: int, left: "Node | None" = None, right: "Node | None" = None) -> None:  # => the constructor
        self.value = value  # => stores value on this instance
        self.left = left  # => stores left on this instance
        self.right = right  # => stores right on this instance


class BinaryTree:  # => the CONTAINER -- exposes iteration without exposing Node internals
    def __init__(self, root: Node | None) -> None:  # => the constructor
        self.root = root  # => stores root on this instance

    def __iter__(self) -> Iterator[int]:  # => makes `for v in tree` work directly
        yield from self._in_order(self.root)  # => delegates to a recursive generator helper

    def _in_order(self, node: Node | None) -> Iterator[int]:  # => LEFT, self, RIGHT
        if node is None:  # => the recursion's base case -- nothing to yield
            return  # => stops this generator branch cleanly
        yield from self._in_order(node.left)  # => everything smaller, first
        yield node.value  # => this node's own value, in the middle
        yield from self._in_order(node.right)  # => everything larger, last


#        4
#       / \
#      2   6
#     / \   \
#    1   3   7
tree: BinaryTree = BinaryTree(Node(4, Node(2, Node(1), Node(3)), Node(6, None, Node(7))))  # => a small, deliberately unbalanced tree
values: list[int] = [v for v in tree]  # => a plain for-loop -- no BinaryTree internals exposed
print(values)  # => in-order traversal yields values in SORTED order for a binary search tree
# => Output: [1, 2, 3, 4, 6, 7]
# => `__iter__` returning a generator lets `for v in tree` walk arbitrarily deep structure lazily
