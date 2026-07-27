"""Example 19: B-Tree Height from Fanout."""

import math  # => stdlib module for the log/ceil formula this example checks itself against

# Tree height grows LOGARITHMICALLY with the key count, in the base of the
# fanout (co-08) -- a high fanout keeps the tree shallow, so a lookup only
# ever touches a handful of pages even over millions of keys. This example
# builds actual bottom-up levels and checks the resulting level count against
# the ceil(log_fanout(N)) formula (illustrative numbers, not vendor constants).

FANOUT: int = 10  # => each internal node groups up to 10 children below it


def build_levels(
    keys: list[int], fanout: int
) -> list[list[int]]:  # => bottom-up: leaf level first
    level: list[int] = keys  # => start at the leaf level -- the raw key list itself
    levels: list[list[int]] = [level]  # => levels[0] is always the leaf level
    while (
        len(level) > 1
    ):  # => keep grouping representatives until one root-level group remains
        level = [
            level[i] for i in range(0, len(level), fanout)
        ]  # => one representative key per group
        levels.append(level)  # => this new, smaller group becomes the next level up
    return levels  # => bottom-to-top: levels[0] is leaves, levels[-1] is the root


keys: list[int] = list(range(100))  # => N = 100 keys
levels = build_levels(
    keys, FANOUT
)  # => actually build the levels, not just compute a formula
level_count = len(
    levels
)  # => leaf level + every internal level up to (and including) the root
internal_levels = math.ceil(
    math.log(len(keys), FANOUT)
)  # => ceil(log_fanout(N)) -- levels ABOVE the leaf
print(level_count)  # => Output: 3
print(internal_levels)  # => Output: 2

assert (
    level_count == internal_levels + 1
)  # => +1 accounts for the leaf level the pure formula excludes
print("ex-19 OK")  # => Output: ex-19 OK
