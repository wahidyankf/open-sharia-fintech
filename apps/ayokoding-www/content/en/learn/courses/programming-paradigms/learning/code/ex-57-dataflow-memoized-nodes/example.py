"""Example 57: Dataflow Memoized Nodes."""

from collections.abc import Callable


class Node:  # => a dataflow graph node that caches its output and tracks whether it's stale
    def __init__(self, compute: Callable[[], int], *deps: "Node") -> None:
        self._compute = compute  # => this node's own recompute rule
        self._deps = deps  # => the nodes this node depends on
        self._dirty = True  # => starts dirty -- nothing has been computed yet
        self._cache: int | None = None  # => the memoized result, once computed
        self.compute_count = 0  # => counts ACTUAL recomputations -- proves memoization is working

    def invalidate(self) -> None:  # => mark this node (and implicitly its dependents) as needing recompute
        self._dirty = True  # => the cache is no longer trustworthy

    def value(self) -> int:  # => read the node's value, recomputing ONLY if dirty
        if self._dirty:  # => only recompute when something actually changed
            self._cache = self._compute()  # => run the rule
            self.compute_count += 1  # => record that a real recomputation happened
            self._dirty = False  # => the cache is fresh again
        return self._cache  # type: ignore[return-value]  # => guaranteed set after the branch above


source = Node(lambda: 5)  # => a source node with no dependencies
unrelated = Node(lambda: 100)  # => a SECOND, unrelated source node -- its own subtree
derived = Node(lambda: source.value() * 2, source)  # => depends only on `source`, NOT on `unrelated`

print(derived.value(), derived.compute_count)  # => first read: computes once
# => Output: 10 1
print(derived.value(), derived.compute_count)  # => second read: cache hit, no recompute
# => Output: 10 1

unrelated.invalidate()  # => invalidate the UNRELATED subtree only
print(derived.value(), derived.compute_count)  # => derived's own cache is untouched -- still 1, not 2
# => Output: 10 1
