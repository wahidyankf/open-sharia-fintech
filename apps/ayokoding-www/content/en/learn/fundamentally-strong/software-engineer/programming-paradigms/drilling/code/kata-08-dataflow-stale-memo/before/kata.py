"""Kata 8 (before): dataflow violation -- a memoized node is never invalidated when its input changes."""


class Doubler:
    def __init__(self, source: list[int]) -> None:
        self.source = source
        self._cache: int | None = None  # SMELL: cached once, nothing ever clears it

    def total_doubled(self) -> int:
        if self._cache is None:
            self._cache = sum(n * 2 for n in self.source)
        return self._cache  # BUG: returns the STALE cached value even after `source` has changed


doubler = Doubler([1, 2, 3])
print(doubler.total_doubled())  # correct: 12
doubler.source.append(10)  # dependency changed
print(doubler.total_doubled())  # should be 32, but the stale cache still says 12
