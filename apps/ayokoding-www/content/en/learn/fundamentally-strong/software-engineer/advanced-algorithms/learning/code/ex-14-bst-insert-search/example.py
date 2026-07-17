"""Example 14: Unbalanced BST -- Insert, Search, and the Inorder-Is-Sorted Invariant."""

# A binary search tree's defining invariant (co-12): every left subtree holds
# only SMALLER values, every right subtree only LARGER ones -- which is
# exactly what makes an inorder traversal always visit values in sorted order.
from __future__ import annotations  # => lets Node reference "Node | None" cleanly


class Node:  # => a single BST node -- value plus left/right child references
    def __init__(self, value: int) -> None:  # => constructs a leaf node
        self.value = value  # => this node's key
        self.left: Node | None = None  # => smaller subtree, absent until inserted
        self.right: Node | None = None  # => larger subtree, absent until inserted


def insert(root: Node | None, value: int) -> Node:  # => returns the (possibly new) root
    if root is None:  # => base case: an empty subtree becomes a new leaf
        return Node(value)  # => this value has no tree yet -- it IS the tree now
    if value < root.value:  # => belongs in the left (smaller-values) subtree
        root.left = insert(root.left, value)  # => recurses left, reattaches the result
    elif value > root.value:  # => belongs in the right (larger-values) subtree
        root.right = insert(root.right, value)  # => recurses right, reattaches result
    return root  # => duplicates (value == root.value) are silently ignored here


def search(root: Node | None, value: int) -> bool:  # => True if value exists in the BST
    if root is None:  # => fell off the tree without finding value
        return False  # => value is not present
    if value == root.value:  # => found it at this node
        return True  # => confirms presence
    if value < root.value:  # => only the LEFT subtree could contain smaller values
        return search(root.left, value)  # => recurses left only
    return search(root.right, value)  # => recurses right only


def inorder(  # => classic left-node-right recursive traversal
    root: Node | None,  # => the subtree to walk -- None yields an empty list
) -> list[int]:  # => left, node, right -- yields sorted order
    if root is None:  # => an empty subtree contributes nothing
        return []  # => base case
    return inorder(root.left) + [root.value] + inorder(root.right)  # => sorted merge


tree_root: Node | None = None  # => starts as an empty tree
for v in [5, 2, 8, 1, 3, 7, 9]:  # => inserted in an arbitrary, unsorted order
    tree_root = insert(tree_root, v)  # => rebinds root in case the tree was empty

traversal = inorder(tree_root)  # => walks left-node-right
print(traversal)  # => Output: [1, 2, 3, 5, 7, 8, 9]
print(search(tree_root, 7))  # => Output: True
print(search(tree_root, 4))  # => Output: False

assert traversal == sorted(  # => opens the self-comparison against Python's own sort
    traversal  # => re-sorts the SAME list -- a no-op if the BST invariant held
)  # => confirms the BST invariant: inorder is always sorted
assert search(tree_root, 7) is True  # => confirms a present value is found
assert search(tree_root, 4) is False  # => confirms an absent value is correctly missed
print("ex-14 OK")  # => Output: ex-14 OK
