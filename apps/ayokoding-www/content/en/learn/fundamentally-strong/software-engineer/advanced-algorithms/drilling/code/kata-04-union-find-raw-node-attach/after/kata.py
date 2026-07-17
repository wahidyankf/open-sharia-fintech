"""Kata 4 (after): union() finds and attaches the ROOTS, so an earlier link is never orphaned."""


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        root_a, root_b = (
            self.find(a),
            self.find(b),
        )  # => resolves to CURRENT roots before attaching
        if root_a != root_b:
            self.parent[root_a] = root_b


uf = UnionFind(3)
uf.union(0, 1)
uf.union(0, 2)
print(uf.find(0) == uf.find(1))
print(uf.find(1) == uf.find(2))  # the whole group of three is now correctly connected
