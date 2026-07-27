# Example 73: Naive vs. Community-Aware Sharding. (co-18, co-26)
# A pure-Python simulation extending Example 45's ring, now with a Louvain-style community
# label already known (as if gds.louvain.stream had already run) for the comparison.
NODES: list[int] = list(range(1, 11))
EDGES: list[tuple[int, int]] = [
    (1, 2),
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 1),
    (6, 7),
    (7, 8),
    (8, 9),
    (9, 10),
    (10, 6),
    (5, 6),
]
# => TWO dense 5-node rings (1-5 and 6-10), joined by exactly ONE bridging edge: (5, 6)

# Naive shard: split by id into three contiguous ranges, 1-3 and 8-10 vs 4-7 -- an ID-range split
# that does NOT line up with the graph's two 5-node ring communities, cutting across BOTH rings.
naive_shard = {n: ("A" if (n <= 3 or n >= 8) else "B") for n in NODES}

# Community-aware shard: as if Louvain had ALREADY identified the two rings as separate communities,
# and the shard boundary is drawn to match that community structure exactly -- genuinely DIFFERENT
# from naive_shard above, not a relabeling of the same partition.
community_shard = {n: ("A" if n <= 5 else "B") for n in NODES}


def crossing_edges(
    shard_of: dict[int, str],
) -> list[tuple[int, int]]:  # => shared by both shards
    return [
        e for e in EDGES if shard_of[e[0]] != shard_of[e[1]]
    ]  # => an edge "crosses" iff shards differ


naive_cross = crossing_edges(
    naive_shard
)  # => crossing edges under the naive id-range split
community_cross = crossing_edges(
    community_shard
)  # => crossing edges under the community-aware split
print(
    f"naive shard crossing edges: {len(naive_cross)} -> {naive_cross}"
)  # => prints the naive result
print(
    f"community-aware shard crossing edges: {len(community_cross)} -> {community_cross}"
)
# => prints the community-aware result, for the direct side-by-side comparison
