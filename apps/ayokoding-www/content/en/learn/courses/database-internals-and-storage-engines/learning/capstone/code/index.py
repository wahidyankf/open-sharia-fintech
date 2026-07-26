"""Capstone Step 2: a B+-tree-style index over pages.py's page ids.

Time/space complexity (n = keys, L = leaf capacity, a small constant):

- ``insert``: O(n / L) -- a linear leaf scan (this course's simplified,
  non-height-balanced leaf chain, in the spirit of Example 43's bulk-vs-
  incremental comparison) plus an O(L) sorted insert within one leaf.
- ``lookup``: O(n / L) worst case -- one linear pass over the leaf chain.
- ``range_scan``: O(n / L + k) -- the same linear pass, plus O(k) for the k
  keys actually inside the requested range.
"""

from __future__ import annotations

import bisect
from dataclasses import dataclass, field

LEAF_CAPACITY = (
    4  # => each leaf holds at most this many (key, page_id) entries before splitting
)


@dataclass
class BTreeIndex:  # => co-07: values (page ids) live only in the leaves, exactly like a real B+-tree
    leaves: list[list[tuple[int, int]]] = field(
        default_factory=list[list[tuple[int, int]]]
    )  # => sorted leaves

    def insert(
        self, key: int, page_id: int
    ) -> None:  # => co-09-style leaf insert + split on overflow
        if not self.leaves:  # => the very first key this index has ever seen
            self.leaves.append([(key, page_id)])
            return
        leaf_index = self._find_leaf(key)  # => which leaf this key belongs in
        leaf = self.leaves[leaf_index]
        existing = next(
            (i for i, (k, _) in enumerate(leaf) if k == key), None
        )  # => already indexed?
        if (
            existing is not None
        ):  # => co-27-style update: a key maps to exactly ONE pointer, never two
            leaf[existing] = (
                key,
                page_id,
            )  # => overwrite the pointer in place -- no duplicate entry
            return  # => an in-place update never overflows a leaf, so there is nothing left to split
        bisect.insort(
            leaf, (key, page_id)
        )  # => a genuinely NEW key -- keeps the leaf sorted by key
        if (
            len(leaf) > LEAF_CAPACITY
        ):  # => the leaf overflowed -- split it, like Example 44's B-tree
            mid = (
                len(leaf) // 2
            )  # => roughly half the entries on each side of the split
            self.leaves[leaf_index] = leaf[:mid]  # => left half stays at this position
            self.leaves.insert(
                leaf_index + 1, leaf[mid:]
            )  # => right half becomes a brand-new leaf

    def _find_leaf(
        self, key: int
    ) -> int:  # => co-10: leaves are kept in key order, front to back
        leaf_index = 0  # => defaults to the first leaf if key is smaller than every leaf's first key
        for i, leaf in enumerate(self.leaves):  # => walk leaves left to right
            if (
                leaf and key < leaf[0][0]
            ):  # => key belongs BEFORE this leaf -- stop at the previous one
                break
            leaf_index = (
                i  # => keep tracking the rightmost leaf whose start is still <= key
            )
        return (
            leaf_index  # => the leaf `insert`/`lookup`/`range_scan` should examine next
        )

    def lookup(
        self, key: int
    ) -> int | None:  # => co-07: a point lookup, returning the key's page_id
        for leaf in (
            self.leaves
        ):  # => a linear scan (this course's simplified leaf chain, not height-log(n))
            for (
                candidate_key,
                page_id,
            ) in leaf:  # => each leaf's entries are already sorted by key
                if (
                    candidate_key == key
                ):  # => an exact match -- this is the page the key lives on
                    return page_id
        return None  # => the key does not exist anywhere in the index

    def range_scan(
        self, low: int, high: int
    ) -> list[tuple[int, int]]:  # => co-10: sibling-linked leaf scan
        matches: list[
            tuple[int, int]
        ] = []  # => every (key, page_id) pair inside [low, high]
        for leaf in (
            self.leaves
        ):  # => walking leaves in order is what makes the RESULT already sorted
            for (
                candidate_key,
                page_id,
            ) in leaf:  # => co-10: no need to re-descend from the root per leaf
                if (
                    low <= candidate_key <= high
                ):  # => within the requested range, inclusive on both ends
                    matches.append(
                        (candidate_key, page_id)
                    )  # => collected in leaf (and thus key) order
        return (
            matches  # => already sorted, since leaves themselves are kept in key order
        )


def demo() -> (
    None
):  # => a genuine, runnable walkthrough of point lookups and a range scan
    index = BTreeIndex()  # => a fresh, empty index
    for key in [
        5,
        1,
        9,
        3,
        7,
        2,
        8,
        4,
        6,
    ]:  # => insert out of order -- the index sorts as it goes
        index.insert(
            key, page_id=key * 10
        )  # => an illustrative mapping: key 5 lives on page 50, etc.
    print(index.lookup(7))  # => a point lookup for an existing key
    print(index.lookup(99))  # => a point lookup for a key that was never inserted
    print(
        index.range_scan(3, 6)
    )  # => every (key, page_id) pair with 3 <= key <= 6, in sorted order


if (
    __name__ == "__main__"
):  # => only runs the demo when this file is executed directly, not on import
    demo()
