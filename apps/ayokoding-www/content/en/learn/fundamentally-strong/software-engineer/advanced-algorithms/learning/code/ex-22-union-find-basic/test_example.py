"""Example 22: pytest verification for Basic Union-Find."""

from example import UnionFind


def test_union_merges_transitively() -> None:
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    assert uf.connected(0, 2) is True  # => transitively merged via node 1


def test_disjoint_groups_stay_disjoint() -> None:
    uf = UnionFind(4)
    uf.union(0, 1)
    uf.union(2, 3)
    assert uf.connected(0, 2) is False  # => two separate unions never merged


def test_repeated_union_is_a_harmless_no_op() -> None:
    uf = UnionFind(3)
    uf.union(0, 1)
    uf.union(0, 1)  # => unioning an already-merged pair changes nothing
    assert uf.connected(0, 1) is True


# => Run: pytest -- Output: 3 passed
