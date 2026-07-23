"""Example 19: Logic Family Facts."""

# => FACTS: raw (parent, child) pairs -- nothing here says "grandparent" anywhere
parent_facts: set[tuple[str, str]] = {
    ("alice", "bob"),  # => alice is bob's parent
    ("bob", "carol"),  # => bob is carol's parent
    ("carol", "dave"),  # => carol is dave's parent
}


def query_grandparent(person: str, facts: set[tuple[str, str]]) -> list[str]:  # => the RULE, as a function
    # => grandparent(X, Z) :- parent(X, Y), parent(Y, Z).  -- a rule composed from two facts
    return [
        z  # => the value the query resolves to -- a grandchild name, never a stored fact
        for (x, y1) in facts  # => find every fact where `person` is the parent
        if x == person  # => keep only facts whose parent side matches the query's `person`
        for (y2, z) in facts  # => then find every fact where THAT child is itself a parent
        if y2 == y1  # => keep only facts whose parent side matches the child found above
        # => z is inferred to be a grandchild of `person` -- it is never stored as a fact anywhere
    ]


print(query_grandparent("alice", parent_facts))  # => alice -> bob -> carol: alice is carol's grandparent
# => Output: ['carol']
print(query_grandparent("bob", parent_facts))  # => bob -> carol -> dave: bob is dave's grandparent
# => Output: ['dave']
print(("alice", "carol") in parent_facts)  # => confirms "grandparent" was never a stored fact
# => Output: False
