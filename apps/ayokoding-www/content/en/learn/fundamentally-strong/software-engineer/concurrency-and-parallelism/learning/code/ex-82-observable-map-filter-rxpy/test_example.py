"""Example 82: pytest verification for `reactivex` `map` + `filter` Pipelines."""

from example import build_pipeline


def test_only_transformed_matching_items_reach_the_observer() -> None:
    collected, completed_flag = build_pipeline()
    expected = [n * n for n in range(10) if (n * n) % 2 == 0]
    assert collected == expected  # => squared, then filtered to even values only
    assert completed_flag == [True]  # => on_completed fired exactly once


# => Run: pytest -- Output: 1 passed
