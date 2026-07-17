"""Example 60: Mini Logic Engine (Rules + Queries)."""

from collections.abc import Iterator  # => query_edge() and query_path() are lazy, typed as Iterator

Fact = tuple[str, str, str]  # => (relation, subject, object) -- e.g. ("edge", "a", "b")


class LogicEngine:  # => a small backtracking engine: stored facts plus derived rules
    def __init__(self) -> None:  # => constructor starts with an empty fact base
        self.facts: set[Fact] = set()  # => the base facts, asserted directly

    def assert_fact(self, relation: str, subject: str, obj: str) -> None:  # => add a base fact
        self.facts.add((relation, subject, obj))  # => stores the raw fact, no rule evaluated yet

    def query_edge(self, subject: str) -> Iterator[str]:  # => base relation: direct edges only
        for relation, s, o in self.facts:  # => scan every stored fact
            if relation == "edge" and s == subject:  # => unify against the "edge" relation
                yield o  # => a direct hop

    def query_path(self, subject: str, _seen: frozenset[str] | None = None) -> Iterator[str]:  # => the RULE, resolved via recursive search
        # => RULE: path(X, Z) :- edge(X, Z).  path(X, Z) :- edge(X, Y), path(Y, Z).  (transitive closure)
        seen = _seen or frozenset()  # => guards against infinite recursion on a cyclic fact base
        for direct in self.query_edge(subject):  # => base case: every direct edge is a path
            if direct not in seen:  # => BACKTRACKING guard: don't revisit a node already on this path
                yield direct  # => yield the direct hop itself
                yield from self.query_path(direct, seen | {subject})  # => recurse: extend the path further


engine = LogicEngine()  # => build a small graph as facts
engine.assert_fact("edge", "a", "b")  # => a -> b
engine.assert_fact("edge", "b", "c")  # => b -> c
engine.assert_fact("edge", "c", "d")  # => c -> d
engine.assert_fact("edge", "d", "a")  # => d -> a: a cycle, exercises the backtracking guard

closure = sorted(set(engine.query_path("a")))  # => the transitive closure from "a"
print(closure)  # => a reaches b, c, d; the guard stops the d->a branch since "a" is already in `seen`
# => Output: ['b', 'c', 'd']
