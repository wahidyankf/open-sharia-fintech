"""Example 72: pytest verification for the three monad laws on Result."""

from example import Ok, add_ten, half, unit


def test_all_three_monad_laws_hold() -> None:
    assert unit(8).bind(half) == half(8)  # => left identity
    assert Ok(8).bind(unit) == Ok(8)  # => right identity
    assert Ok(8).bind(half).bind(add_ten) == Ok(8).bind(
        lambda x: half(x).bind(add_ten)
    )  # => associativity


# => Run: pytest -- Output: 1 passed
