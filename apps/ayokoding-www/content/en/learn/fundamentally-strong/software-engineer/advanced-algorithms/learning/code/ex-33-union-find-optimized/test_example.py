"""Example 33: pytest verification for Optimized Union-Find."""

from example import OptimizedUnionFind


def test_path_compression_keeps_trees_shallow_after_a_worst_case_chain() -> None:
    n = 500
    uf = OptimizedUnionFind(n)
    for i in range(n - 1):
        uf.union(i, i + 1)  # => the worst possible union order for a naive union-find
    for x in range(n):
        uf.find(x)  # => compresses every path
    for x in range(n):  # => re-checks: every element's parent should now be near-root
        assert uf.parent[x] == uf.find(x) or uf.parent[x] == uf.parent[uf.find(x)]


def test_connectivity_after_optimized_unions_matches_expectations() -> None:
    uf = OptimizedUnionFind(6)
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(1, 2)  # => merges {0,1} and {2,3} into one group of 4
    assert uf.find(0) == uf.find(3)  # => transitively connected
    assert uf.find(0) != uf.find(4)  # => 4 and 5 remain their own singleton groups
    assert uf.find(4) != uf.find(5)


# => Run: pytest -- Output: 2 passed
