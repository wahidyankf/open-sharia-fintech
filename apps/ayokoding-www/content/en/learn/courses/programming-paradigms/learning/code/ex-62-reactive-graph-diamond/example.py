"""Example 62: Reactive Graph Diamond."""

from collections.abc import Callable  # => types every no-argument recompute rule stored below


class Computed:  # => a derived signal that tracks its own recursion depth for correct recompute ordering
    def __init__(self, compute: Callable[[], int], depth: int) -> None:  # => constructor seeds value and depth
        self._compute = compute  # => this node's own recompute rule
        self.value = compute()  # => computed once immediately
        self.depth = depth  # => diamond nodes at a deeper level recompute AFTER their shallower dependencies
        self.dependents: list["Computed"] = []  # => nodes that read THIS node's value
        self.recompute_count = 0  # => proves the diamond's shared node recomputes exactly once per update

    def recompute(self) -> None:  # => re-run this node's rule and bump its recompute counter
        self.value = self._compute()  # => re-run the formula and refresh the cached value
        self.recompute_count += 1  # => bumps once per call -- proves how many times this node actually ran


class Signal:  # => a reactive source; writing it schedules every transitive dependent EXACTLY once
    def __init__(self, initial: int) -> None:  # => constructor seeds the starting value
        self._value = initial  # => the current value, hidden behind get()/write() below
        self.dependents: list[Computed] = []  # => the Computed nodes that read this signal directly

    def get(self) -> int:  # => read the current value
        return self._value  # => a plain read -- getting never triggers propagation

    def write(self, value: int) -> None:  # => write a new value and propagate through the whole graph
        self._value = value  # => update this signal's own value first

        by_id: dict[int, Computed] = {}  # => collect every transitively-dependent node, keyed by identity
        frontier: list[Computed] = list(self.dependents)  # => start from this signal's direct dependents
        while frontier:  # => BFS outward through the dependency graph
            node = frontier.pop(0)  # => dequeue the next node to visit, FIFO order
            if id(node) not in by_id:  # => a diamond node reached via two paths is only ADDED once
                by_id[id(node)] = node  # => identity-keyed, so the same object is never collected twice
                frontier.extend(node.dependents)  # => keep walking further downstream

        # => recompute in depth order -- every shallower dependency is refreshed before anything deeper
        # => reads it, so a diamond's bottom node never reads a stale value from either branch
        for node in sorted(by_id.values(), key=lambda n: n.depth):  # => shallow depths recompute first
            node.recompute()  # => runs at most ONCE per node per write(), regardless of incoming edge count


a = Signal(1)  # => the single source at the top of the diamond
b = Computed(lambda: a.get() + 1, depth=1)  # => b <- a (left branch)
c = Computed(lambda: a.get() + 2, depth=1)  # => c <- a (right branch)
d = Computed(lambda: b.value + c.value, depth=2)  # => d <- b, c (the diamond's bottom, joins both branches)
a.dependents.extend([b, c])  # => wire a's direct dependents
b.dependents.append(d)  # => wire d as a dependent of b
c.dependents.append(d)  # => wire d as a dependent of c

a.write(10)  # => ONE write at the top of the diamond
print(d.value)  # => b=11, c=12, d=11+12=23
# => Output: 23
print(d.recompute_count)  # => d must recompute EXACTLY ONCE per update, not once per incoming edge (2)
# => Output: 1
