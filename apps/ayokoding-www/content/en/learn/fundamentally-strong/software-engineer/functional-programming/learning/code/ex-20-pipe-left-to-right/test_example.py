"""Example 20: pytest verification for A Left-to-Right pipe Helper."""

from example import add_one, double, pipe


def test_pipe_matches_nested_calls() -> None:
    assert pipe(3, add_one, double) == double(add_one(3)) == 8


# => Run: pytest -- Output: 1 passed
