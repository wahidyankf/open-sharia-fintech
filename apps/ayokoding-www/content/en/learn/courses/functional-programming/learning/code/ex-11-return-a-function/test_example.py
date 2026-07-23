"""Example 11: pytest verification for A Function Returning a Closure."""

from example import multiplier


def test_returned_closures_remember_their_own_n() -> None:
    times_three = multiplier(3)
    times_five = multiplier(5)
    assert times_three(4) == 12
    assert times_five(4) == 20
    assert multiplier(3)(4) == 12  # => calling the returned function immediately


# => Run: pytest -- Output: 1 passed
