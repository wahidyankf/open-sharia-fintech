"""Example 80: pytest verification for A Property-Based Test of an Invariant."""

import random

from example import Percentage


def test_no_randomized_input_reaches_an_invalid_state() -> None:
    rng: random.Random = random.Random(
        1234
    )  # => a different, still-fixed seed for reproducibility
    for _ in range(500):
        candidate: float = rng.uniform(-50, 150)
        try:
            p: Percentage = Percentage(candidate)
        except ValueError:
            continue  # => rejection is the correct outcome for an out-of-range candidate
        assert (
            0 <= p.value <= 100
        )  # => any SUCCESSFULLY constructed instance must satisfy the invariant


# => Run: pytest -- Output: 1 passed
