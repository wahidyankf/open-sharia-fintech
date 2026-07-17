"""Example 68: pytest verification for Sequencing Option Computations, Do-Style."""

from example import Nothing, Some, compute


def test_do_style_chain_short_circuits_on_absence() -> None:
    assert compute(100, 4) == Some(500.0)
    assert compute(100, 0) == Nothing()
    assert compute(-100, 4) == Nothing()


# => Run: pytest -- Output: 1 passed
