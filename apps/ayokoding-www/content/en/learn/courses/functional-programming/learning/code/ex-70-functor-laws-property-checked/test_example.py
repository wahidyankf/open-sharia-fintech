"""Example 70: pytest verification for Property-Checking the Functor Identity and Composition Laws."""

import random

from example import Box, check_composition_law, check_identity_law


def test_both_functor_laws_hold_across_many_generated_boxes() -> None:
    random.seed(7)
    boxes = [Box(random.randint(-500, 500)) for _ in range(100)]
    assert all(check_identity_law(b) for b in boxes)
    assert all(check_composition_law(b) for b in boxes)


# => Run: pytest -- Output: 1 passed
