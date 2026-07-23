"""Kata 4 (before): union() attaches the raw nodes instead of their ROOTS, orphaning an earlier link."""


class UnionFind:
    def __init__(self, n: int) -> None:
        self.parent = list(range(n))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        self.parent[a] = (
            b  # BUG: overwrites parent[a] directly, ignoring find(a) -- can orphan an old link
        )


uf = UnionFind(3)
uf.union(0, 1)  # 0 and 1 are now one group
uf.union(0, 2)  # intent: merge {0, 1} and {2} into one group of all three
print(
    uf.find(0) == uf.find(1)
)  # expected True -- 0 and 1 were explicitly unioned, but the link is now lost
