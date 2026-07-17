"""Example 58: pytest verification for Property-Testing Purity Without a Third-Party Library."""

import random

from example import normalize_score


def test_purity_holds_across_many_generated_inputs() -> None:
    random.seed(
        99
    )  # => a different fixed seed than example.py, still fully reproducible
    inputs = [random.randint(-1000, 1000) for _ in range(500)]
    first_pass = [normalize_score(x) for x in inputs]
    second_pass = [normalize_score(x) for x in inputs]
    assert first_pass == second_pass


# => Run: pytest -- Output: 1 passed
