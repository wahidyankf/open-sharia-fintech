"""Example 6: pytest verification for Branch a Partial Query."""

from example import Query


def test_branches_share_the_trunk_but_diverge_independently() -> None:
    trunk = Query(table="orders").where("region = 'west'")  # => shared partial query
    left = trunk.where("status = 'open'")  # => first branch
    right = trunk.where("status = 'closed'")  # => second, independent branch
    assert left.wheres[0] == right.wheres[0] == "region = 'west'"  # => both inherit the trunk
    assert left.wheres[-1] != right.wheres[-1]  # => each branch's own tip differs


def test_trunk_is_never_mutated_by_either_branch() -> None:
    trunk = Query(table="orders").where("region = 'west'")  # => one-filter trunk
    trunk.where("status = 'open'")  # => branch, but result discarded on purpose
    trunk.where("status = 'closed'")  # => second branch, also discarded
    assert trunk.wheres == ("region = 'west'",)  # => trunk still has exactly one filter


# => Run: pytest -- Output: 2 passed
