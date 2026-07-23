"""Example 79: pytest verification for Deadlock-Free Dining Philosophers."""

from example import MEALS_PER_PHILOSOPHER, PHILOSOPHER_COUNT, run_dinner


def test_every_philosopher_eats_without_deadlocking() -> None:
    meals_eaten = run_dinner()
    assert meals_eaten == [MEALS_PER_PHILOSOPHER] * PHILOSOPHER_COUNT  # => every philosopher ate, fully, no hang


# => Run: pytest -- Output: 1 passed
