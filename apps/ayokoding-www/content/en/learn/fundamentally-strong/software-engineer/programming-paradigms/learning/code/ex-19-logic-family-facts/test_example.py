"""Example 19: pytest verification for Logic Family Facts."""

from example import query_grandparent


def test_grandparent_is_inferred_not_stored() -> None:
    facts = {("alice", "bob"), ("bob", "carol"), ("carol", "dave")}  # => same three facts as the demo
    assert query_grandparent("alice", facts) == ["carol"]  # => inferred via two composed facts
    assert ("alice", "carol") not in facts  # => never directly stored anywhere


def test_a_childless_leaf_has_no_grandchildren() -> None:
    facts = {("alice", "bob"), ("bob", "carol"), ("carol", "dave")}  # => same fact set
    assert query_grandparent("dave", facts) == []  # => dave has no children in these facts at all


# => Run: pytest -- Output: 2 passed
