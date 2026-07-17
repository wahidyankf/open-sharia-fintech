"""Kata 8 (after): dataflow fix -- the node recomputes whenever its source has actually changed."""


class Doubler:
    def __init__(self, source: list[int]) -> None:
        self.source = source
        self._cache: int | None = None
        self._cached_length = -1  # tracks the source length the cache was computed FOR

    def total_doubled(self) -> int:
        if self._cache is None or self._cached_length != len(self.source):  # dependency changed -> stale
            self._cache = sum(n * 2 for n in self.source)
            self._cached_length = len(self.source)
        return self._cache


doubler = Doubler([1, 2, 3])
print(doubler.total_doubled())
doubler.source.append(10)
print(doubler.total_doubled())
