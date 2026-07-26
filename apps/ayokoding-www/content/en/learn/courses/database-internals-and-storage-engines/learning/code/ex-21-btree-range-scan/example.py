"""Example 21: B-Tree Range Scan via Sibling Links."""

from dataclasses import dataclass  # => a plain, typed record for one leaf node


@dataclass
class Leaf:  # => a leaf node with a NEXT pointer chaining it to its right sibling
    keys: list[int]  # => this leaf's own sorted keys
    next: "Leaf | None" = None  # => the sibling immediately to the right, or None if this is the last leaf


# Sibling-linked leaves let a range scan walk forward leaf-to-leaf without
# ever re-descending from the root (co-10) -- only the STARTING leaf needs a
# root-to-leaf search; every following leaf is reached via `next` alone.


def range_scan(
    start: Leaf, lo: int, hi: int
) -> list[int]:  # => inclusive [lo, hi] range scan
    result: list[int] = []  # => accumulates every matching key, in sorted order
    node: Leaf | None = start  # => begin at the leaf the caller already descended to
    while node is not None:  # => walk sideways via `next`, never back up to the root
        for key in node.keys:  # => scan this leaf's own keys
            if lo <= key <= hi:  # => inclusive bounds check
                result.append(key)
        if (
            node.keys and node.keys[-1] > hi
        ):  # => this leaf's max key already exceeds hi -- stop early
            break
        node = node.next  # => hop sideways to the next leaf -- no root descent needed
    return result  # => a contiguous, sorted run possibly spanning several leaves


leaf_a = Leaf(keys=[10, 20, 30])  # => the first leaf in the chain
leaf_b = Leaf(keys=[40, 50, 60])  # => the second leaf in the chain
leaf_c = Leaf(keys=[70, 80, 90])  # => the third leaf in the chain
leaf_a.next, leaf_b.next = leaf_b, leaf_c  # => chain: a -> b -> c

result = range_scan(leaf_a, 25, 75)  # => starts inside leaf_a, ends inside leaf_c
print(result)  # => Output: [30, 40, 50, 60, 70]

assert result == [
    30,
    40,
    50,
    60,
    70,
]  # => a contiguous sorted run spanning THREE separate leaf nodes
# => the scan never had to climb back up to leaf_a's parent to reach leaf_b or leaf_c
print("ex-21 OK")  # => Output: ex-21 OK
