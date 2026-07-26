# Example 45: Graph Sharding and the Edge Cut. (co-18)
# A small, pure-Python simulation (no live database needed) -- models a naive ID-range shard
# split and counts how many edges end up crossing the shard boundary.
NODES: list[int] = list(range(1, 11))  # => 10 nodes, ids 1 through 10
EDGES: list[tuple[int, int]] = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (10, 1),
]
# => a RING: every node connects to its neighbor, and node 10 wraps back to node 1

# Naive shard split: nodes 1-5 go to shard A, nodes 6-10 go to shard B -- pure ID-range.
shard_of: dict[int, str] = {n: ("A" if n <= 5 else "B") for n in NODES}

crossing = [e for e in EDGES if shard_of[e[0]] != shard_of[e[1]]]
# => an edge "crosses" if its two endpoints land in DIFFERENT shards -- co-18's edge cut
print(f"total edges: {len(EDGES)}")
print(f"crossing edges: {len(crossing)} -> {crossing}")
