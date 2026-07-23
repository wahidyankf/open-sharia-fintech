"""Example 36: Prolog-in-Python (Unification + Backtracking)."""

from collections.abc import Iterator  # => grandparent() below is a generator, typed as an Iterator

Fact = tuple[str, str]  # => a (parent, child) fact, mirroring example 19's family data
facts: list[Fact] = [  # => the FACTS -- raw data, no rule about grandparents anywhere in this list
    ("alice", "bob"),  # => alice is bob's parent
    ("bob", "carol"),  # => bob is carol's parent
    ("carol", "dave"),  # => carol is dave's parent
]  # => the same three-generation family as example 19, this time queried via search, not a comprehension


def parent(x: str, y: str) -> bool:  # => the base relation: is (x, y) a stored fact? (unification step)
    return (x, y) in facts  # => "unifying" x and y against every stored fact


def grandparent(x: str) -> Iterator[str]:  # => the RULE, expressed as a search over intermediate variables
    for _px, y in facts:  # => try binding Y to every fact's child (a backtracking choice point)
        if _px != x:  # => this choice point only matters when x is actually the parent in this fact
            continue  # => BACKTRACK: this binding of Y didn't unify with parent(x, Y) -- try the next one
        for py, z in facts:  # => a NESTED choice point: try binding Z to every fact's child
            if py != y:  # => does this fact's parent match the Y we just bound?
                continue  # => BACKTRACK again: try the next candidate fact
            yield z  # => both parent(x, Y) and parent(Y, Z) unified -- z is a valid answer


results = list(grandparent("alice"))  # => search: alice -> bob (bind Y) -> bob -> carol (bind Z)
# => draining the generator forces the backtracking search to actually run to completion
print(results)  # => must match example 19's comprehension-based answer
# => Output: ['carol']
