"""Example 15: A Plain BST Degenerates into an O(n) Chain on Sorted Input."""

# Insert already-sorted keys and every new node becomes the PREVIOUS node's
# right child -- the tree never branches (co-12, co-01). Height becomes n-1,
# and search degrades from the hoped-for O(log n) to a linked-list-like O(n).
from __future__ import annotations


class Node:  # => same minimal BST node shape as Example 14
    def __init__(self, value: int) -> None:  # => constructs a leaf with no children yet
        self.value = value  # => this node's key
        self.left: Node | None = None  # => never used when input arrives pre-sorted
        self.right: Node | None = None  # => every new node lands here instead


def insert(root: Node | None, value: int) -> Node:  # => identical logic to Example 14
    if root is None:  # => base case: empty subtree becomes a new leaf
        return Node(value)  # => this value has no tree yet -- it IS the tree now
    if value < root.value:  # => sorted input means this branch is NEVER taken here
        root.left = insert(root.left, value)  # => would recurse left, but unreachable
    elif value > root.value:  # => sorted input means EVERY insert takes this branch
        root.right = insert(root.right, value)  # => always attaches to the right side
    return root  # => the (unchanged) root reference, propagated back up the recursion


def height(root: Node | None) -> int:  # => longest path from root to a leaf, in edges
    if root is None:  # => an empty (sub)tree has height -1 by convention
        return -1  # => makes a single-node tree height 0, matching graph-theory height
    return 1 + max(  # => opens the "1 + taller subtree" recursive height formula
        height(root.left),
        height(root.right),  # => recurses into BOTH children
    )  # => 1 + the taller child's height


sorted_keys: list[int] = list(range(20))  # => 0, 1, 2, ..., 19 -- ALREADY SORTED
degenerate_root: Node | None = None  # => starts empty
for k in sorted_keys:  # => inserting in ascending order is the worst case for a BST
    degenerate_root = insert(  # => rebinds root each time, in case the tree was empty
        degenerate_root,
        k,  # => k is always larger than every key inserted so far
    )  # => each new key attaches on the right

tree_height = height(degenerate_root)  # => how many edges from root to the deepest leaf
n = len(sorted_keys)  # => n = 20
print(tree_height)  # => Output: 19
print(n - 1)  # => Output: 19 -- height matches n-1 exactly: a straight chain

assert tree_height == n - 1  # => confirms the tree degenerated into a single chain
depth = 0  # => counts how many right-child hops it takes to walk the whole chain
walker: Node | None = degenerate_root  # => starts the walk at the root -- possibly None
while walker is not None and walker.right is not None:  # => follows right children only
    walker = walker.right  # => every node's ONLY child is its right child
    depth += 1  # => one more hop down the chain
assert depth == n - 1  # => confirms every node really is a straight right-only chain
print("ex-15 OK")  # => Output: ex-15 OK
