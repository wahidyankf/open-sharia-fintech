"""Example 13: pytest verification for Stable vs Unstable Sorting."""

from example import selection_sort_by_key, stable_sort_by_key


def test_stable_sort_preserves_input_order_of_equal_keys() -> None:
    data: list[tuple[int, str]] = [(2, "x"), (1, "y"), (2, "z")]
    result = stable_sort_by_key(data)
    assert result == [(1, "y"), (2, "x"), (2, "z")]  # => "x" stays before "z"


def test_both_sorts_agree_on_the_final_key_order() -> None:
    data: list[tuple[int, str]] = [(3, "p"), (1, "q"), (2, "r")]
    stable_keys = [key for key, _ in stable_sort_by_key(data)]
    unstable_keys = [key for key, _ in selection_sort_by_key(data)]
    assert stable_keys == unstable_keys == [1, 2, 3]  # => key order always agrees


# => Run: pytest -- Output: 2 passed
