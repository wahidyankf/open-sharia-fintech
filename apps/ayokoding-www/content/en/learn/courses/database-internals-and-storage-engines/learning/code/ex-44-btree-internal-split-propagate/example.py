"""Example 44: Force B-Tree Splits Up to the Root."""
# A B-tree only grows taller by splitting a FULL root (co-09) -- every other split stays local.

import bisect  # => stdlib binary-search helper for sorted-list insertion


class BTreeNode:  # => a single B-tree node -- either an internal node or a leaf
    def __init__(
        self, leaf: bool = True
    ) -> None:  # => leaf=True until proven otherwise
        self.keys: list[
            int
        ] = []  # => this node's own separator/data keys, always kept sorted
        self.children: list[
            "BTreeNode"
        ] = []  # => empty for leaves, len(keys)+1 for internal nodes
        self.leaf: bool = leaf  # => whether this node has no children at all


class BTree:  # => a minimal B-tree with proactive split-on-the-way-down insertion (co-09)
    def __init__(
        self, t: int
    ) -> None:  # => t is the minimum degree -- max keys per node is 2t-1
        self.root: BTreeNode = BTreeNode(leaf=True)  # => starts as a single empty leaf
        self.t: int = t  # => stored for use by split/insert below

    def height(
        self,
    ) -> int:  # => counts edges from root down to a leaf (all leaves are equidistant)
        node, h = self.root, 0  # => start at the root with height 0
        while not node.leaf:  # => descend the leftmost path until a leaf is reached
            node = node.children[
                0
            ]  # => step down one level, always via the first child
            h += 1  # => one more edge crossed
        return h  # => the tree's current height, in edges from root to any leaf

    def insert(
        self, key: int
    ) -> None:  # => the public entry point -- handles a full root specially
        root = self.root  # => the current root, before any possible split
        if (
            len(root.keys) == 2 * self.t - 1
        ):  # => the root itself is full -- MUST split before inserting
            new_root = BTreeNode(
                leaf=False
            )  # => a brand-new root, one level taller than before
            new_root.children.append(
                root
            )  # => the old root becomes the new root's only child, for now
            self._split_child(
                new_root, 0
            )  # => splits it in two, promoting a median key up
            self.root = (
                new_root  # => the tree's height has now increased by exactly one
            )
        self._insert_nonfull(
            self.root, key
        )  # => descend and insert, splitting full children on the way

    def _split_child(
        self, parent: BTreeNode, i: int
    ) -> None:  # => splits parent.children[i] in two
        t = self.t  # => the minimum degree, cached locally for readability below
        child = parent.children[i]  # => the full node being split
        new_node = BTreeNode(
            leaf=child.leaf
        )  # => the right half -- same leaf-ness as the original
        mid_key = child.keys[t - 1]  # => the median key -- it moves UP into the parent
        new_node.keys = child.keys[
            t:
        ]  # => the right half of the keys goes to the new sibling
        child.keys = child.keys[
            : t - 1
        ]  # => the original node keeps only its left half
        if not child.leaf:  # => internal nodes must also split their children pointers
            new_node.children = child.children[
                t:
            ]  # => right-half children follow their keys
            child.children = child.children[:t]  # => left-half children stay behind
        parent.children.insert(
            i + 1, new_node
        )  # => the new sibling takes its place beside the original
        parent.keys.insert(
            i, mid_key
        )  # => the median key becomes a new separator in the parent

    def _insert_nonfull(
        self, node: BTreeNode, key: int
    ) -> None:  # => assumes node is never full itself
        if (
            node.leaf
        ):  # => base case -- leaves just get the key inserted in sorted order
            bisect.insort(
                node.keys, key
            )  # => keeps the leaf's keys sorted after the insert
            return  # => nothing further to do once a leaf has absorbed the key
        i = len(node.keys) - 1  # => find which child subtree the key belongs under
        while (
            i >= 0 and key < node.keys[i]
        ):  # => walk right-to-left until the right slot is found
            i -= 1  # => keep moving left while the key is smaller than this separator
        i += 1  # => i now indexes the correct child to descend into
        if (
            len(node.children[i].keys) == 2 * self.t - 1
        ):  # => that child is full -- split it FIRST
            self._split_child(
                node, i
            )  # => proactively split before descending, never after
            if (
                key > node.keys[i]
            ):  # => the split may shift which child the key now belongs under
                i += 1  # => the key now belongs in the newly created right sibling instead
        self._insert_nonfull(
            node.children[i], key
        )  # => recurse into the now-guaranteed-non-full child


tree = BTree(
    t=2
)  # => t=2 means max 3 keys per node, forcing splits quickly for this example
for key in range(
    1, 9
):  # => insert keys 1 through 8 -- enough to fill the root once already
    tree.insert(key)  # => each insert may cascade zero or more splits below the root
height_before = tree.height()  # => height BEFORE the key that forces a root split
print(height_before)  # => Output: 1

tree.insert(9)  # => this ninth key overflows the (now full) root, forcing a root split
height_after = tree.height()  # => height AFTER the forced root split
print(height_after)  # => Output: 2
print(len(tree.root.children))  # => Output: 2

assert (
    height_after == height_before + 1
)  # => the root split grew the tree by exactly one level
assert (
    len(tree.root.children) == 2
)  # => a freshly split root always starts with exactly two children
print("ex-44 OK")  # => Output: ex-44 OK
