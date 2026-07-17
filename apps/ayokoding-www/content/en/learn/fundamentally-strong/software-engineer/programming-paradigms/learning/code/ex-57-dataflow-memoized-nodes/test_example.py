"""Example 57: pytest verification for Dataflow Memoized Nodes."""

from example import Node


def test_repeated_reads_do_not_recompute_an_unchanged_node() -> None:
    node = Node(lambda: 42)  # => fresh node, isolated from the module-level demo
    node.value()  # => first read: real computation
    node.value()  # => second read: should be a cache hit
    node.value()  # => third read: should also be a cache hit
    assert node.compute_count == 1  # => exactly one real recomputation across three reads


def test_invalidating_an_unrelated_subtree_never_recomputes_this_node() -> None:
    source = Node(lambda: 5)  # => fresh source
    other = Node(lambda: 1)  # => a completely separate, unrelated node
    derived = Node(lambda: source.value() + 1, source)  # => depends only on `source`
    derived.value()  # => compute once
    other.invalidate()  # => invalidate the unrelated node
    derived.value()  # => read again
    assert derived.compute_count == 1  # => still just one recompute -- the unchanged subtree was skipped


# => Run: pytest -- Output: 2 passed
