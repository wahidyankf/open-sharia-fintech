"""Example 32: pytest verification for Stateful Closure Counter vs. Pure Fold."""

from example import count_pure, make_counter


def test_closure_state_and_pure_fold_agree_on_the_final_count() -> None:
    counter = make_counter()
    for _ in range(3):
        counter()
    assert counter() == 4  # => state lives IN the closure, mutated across calls
    assert count_pure(4) == 4  # => the SAME count, computed with zero mutable state


# => Run: pytest -- Output: 1 passed
