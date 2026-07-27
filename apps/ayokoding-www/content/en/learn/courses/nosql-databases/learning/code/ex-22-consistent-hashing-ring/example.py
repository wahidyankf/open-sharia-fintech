"""Example 22: Consistent Hashing Ring."""  # => co-11: this file's own purpose, doubling as its module __doc__

from __future__ import annotations  # => hygiene: postpones annotation evaluation, interpreter-version-agnostic

import bisect  # => co-11: bisect finds a key's clockwise-nearest node point in O(log N), no linear scan
import hashlib  # => co-11: a stable, deterministic hash, same across every run


def ring_point(label: str) -> int:  # => co-11: maps any string (a node name OR a key) onto the SAME ring space
    """Hash a label onto a fixed-size ring position."""  # => documents the contract, no runtime output
    digest = hashlib.sha256(label.encode("utf-8")).hexdigest()  # => a stable 256-bit digest
    return int(digest, 16) % (2**32)  # => co-11: reduces to a 32-bit ring -- large enough to avoid collisions here


class HashRing:  # => co-11: nodes and keys share ONE ring; a key belongs to the next node clockwise
    def __init__(self, nodes: list[str]) -> None:  # => builds the ring from an initial node list
        self._point_to_node: dict[int, str] = {}  # => co-11: maps a ring position back to the node that owns it
        self._sorted_points: list[int] = []  # => co-11: kept sorted so bisect can find "next point clockwise" fast
        for node in nodes:  # => places every initial node onto the ring
            self.add_node(node)

    def add_node(self, node: str) -> None:  # => co-11: inserts one more node onto the ring, in sorted position
        point = ring_point(node)  # => this node's own fixed position on the ring
        self._point_to_node[point] = node  # => records which node owns this point
        bisect.insort(self._sorted_points, point)  # => co-11: keeps the point list sorted after every insertion

    def node_for_key(self, key: str) -> str:  # => co-11: walks CLOCKWISE from the key's point to the first node found
        point = ring_point(key)  # => this key's own fixed position on the SAME ring space as the nodes
        idx = bisect.bisect_left(self._sorted_points, point)  # => co-11: index of the first node point >= key's point
        if idx == len(self._sorted_points):  # => co-11: past the last point -- wrap around to the ring's start
            idx = 0
        return self._point_to_node[self._sorted_points[idx]]  # => the owning node, found in O(log N)


def main() -> None:  # => entry point -- runs only when this file executes directly, not on import
    ring = HashRing(["node-A", "node-B", "node-C", "node-D"])  # => co-11: 4 nodes on the ring to start
    keys = [f"key-{i}" for i in range(200)]  # => co-11: a large-enough key set to see a stable percentage move
    before = {key: ring.node_for_key(key) for key in keys}  # => co-11: every key's owning node, BEFORE adding node-E

    ring.add_node("node-E")  # => co-11: a 5th node joins -- only keys landing between node-E and its clockwise neighbor move
    after = {key: ring.node_for_key(key) for key in keys}  # => the SAME keys, re-mapped now that node-E exists

    moved = sum(1 for key in keys if before[key] != after[key])  # => co-11: count of keys whose owning node changed
    fraction_moved = moved / len(keys)  # => the observed fraction, to compare against consistent hashing's own promise
    print(f"Keys remapped after adding a 5th node: {moved} of {len(keys)} ({fraction_moved:.1%})")  # => Output line
    # => co-11: consistent hashing's promise is roughly 1/N_new of keys move (here, ~1/5 = 20%) --
    # => NOT all 200 keys, which a naive mod-hash (key_hash % node_count) would have remapped instead
    assert 0.05 <= fraction_moved <= 0.40  # => co-11: a generous band around the theoretical ~20% -- confirms it is NOT "almost all"


if __name__ == "__main__":  # => guards against running main() on `import example`
    main()  # => runs everything above when executed as a script
