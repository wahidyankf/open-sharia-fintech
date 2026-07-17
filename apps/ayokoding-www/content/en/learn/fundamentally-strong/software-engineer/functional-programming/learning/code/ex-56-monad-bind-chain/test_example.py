"""Example 56: pytest verification for bind/flat_map Chaining Result Steps."""

from example import Err, Ok, half, to_positive


def test_bind_chains_and_short_circuits_on_the_first_error() -> None:
    assert Ok(8).bind(half).bind(to_positive) == Ok(4.0)
    assert Ok(7).bind(half).bind(to_positive) == Err("7 is odd")


# => Run: pytest -- Output: 1 passed
