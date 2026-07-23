# learning/code/ex-43-property-idempotent/test_example.py
"""Example 43: Property -- Idempotence."""

from hypothesis import given  # => the property-test decorator: runs the body over MANY generated inputs (co-18)  # fmt: skip
from hypothesis import strategies as st  # => st.integers() DESCRIBES the input space to generate from (co-20)  # fmt: skip


def normalize_sign(
    n: int,
) -> int:  # => the unit under test -- clamps any int to -1, 0, or 1
    if n > 0:  # => positive branch
        return 1  # => clamps ANY positive int down to exactly 1
    if n < 0:  # => negative branch
        return -1  # => clamps ANY negative int down to exactly -1
    return 0  # => exactly zero


@given(st.integers())  # => co-18/co-20: Hypothesis generates HUNDREDS of ints, not just hand-picked ones  # fmt: skip
def test_normalize_sign_is_idempotent(x: int) -> None:  # => x is Hypothesis-generated, not hand-picked  # fmt: skip
    # => IDEMPOTENT means applying the function twice equals applying it once -- a property
    # => that should hold for EVERY integer, not just a few examples chosen by hand (co-18)
    once = normalize_sign(x)  # => act 1: the first application
    twice = normalize_sign(normalize_sign(x))  # => act 2: applying it AGAIN to its own output  # fmt: skip
    assert once == twice  # => the invariant Hypothesis checks across every generated x
