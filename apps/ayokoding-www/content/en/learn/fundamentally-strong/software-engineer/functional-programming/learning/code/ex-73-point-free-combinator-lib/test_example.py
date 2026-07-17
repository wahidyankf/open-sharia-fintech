"""Example 73: pytest verification for A Small Point-Free Combinator Library."""

from example import const, flip, pipe, subtract


def _add_one(x: int) -> int:
    return x + 1


def _double(x: int) -> int:
    return x * 2


def test_pipe_const_and_flip_compose_correctly() -> None:
    transform = pipe(_add_one, _double)
    assert transform(3) == 8

    always_five = const(5)
    assert always_five(1, 2, 3) == 5

    flipped_subtract = flip(subtract)
    assert flipped_subtract(10, 3) == -7


# => Run: pytest -- Output: 1 passed
