"""Example 19: pytest verification for B-Tree Height from Fanout."""

import math

from example import FANOUT, build_levels


def test_level_count_matches_the_fanout_formula() -> None:
    keys = list(range(1000))
    levels = build_levels(keys, FANOUT)
    expected = math.ceil(math.log(len(keys), FANOUT))
    assert len(levels) == expected + 1  # => +1 for the leaf level the formula excludes


def test_higher_fanout_yields_a_shallower_tree() -> None:
    keys = list(range(1000))
    shallow = build_levels(keys, fanout=100)
    deep = build_levels(keys, fanout=2)
    assert len(shallow) < len(
        deep
    )  # => a higher fanout keeps the tree shallower for the SAME key count


# => Run: pytest -- Output: 2 passed
