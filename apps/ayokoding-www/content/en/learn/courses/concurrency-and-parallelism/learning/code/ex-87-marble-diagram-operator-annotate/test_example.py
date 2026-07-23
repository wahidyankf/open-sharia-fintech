"""Example 87: pytest verification for the Annotated Marble Diagram (merge -> map -> debounce)."""

from example import SOURCE_A, SOURCE_B, debounce_marbles, map_marbles, merge_marbles


def test_merge_interleaves_by_tick_without_changing_any_value() -> None:
    merged = merge_marbles(SOURCE_A, SOURCE_B)
    ticks = [tick for tick, _ in merged]
    assert ticks == sorted(ticks)  # => strictly non-decreasing -- merge never reorders by anything but time
    assert {value for _, value in merged} == {"a1", "a2", "a3", "b1", "b2", "b3"}  # => every original value survives


def test_map_changes_values_but_leaves_every_tick_untouched() -> None:
    merged = merge_marbles(SOURCE_A, SOURCE_B)
    mapped = map_marbles(merged, str.upper)
    assert [tick for tick, _ in mapped] == [tick for tick, _ in merged]  # => identical tick sequence, unchanged
    assert [value for _, value in mapped] == [value.upper() for _, value in merged]  # => every value transformed


def test_debounce_keeps_only_marbles_with_enough_trailing_silence() -> None:
    merged = merge_marbles(SOURCE_A, SOURCE_B)
    mapped = map_marbles(merged, str.upper)
    debounced = debounce_marbles(mapped, quiet=2)
    assert debounced == [(5, "A2"), (10, "B3")]  # => exactly the two marbles that had a 2+ tick gap after them
    assert len(debounced) < len(mapped)  # => debounce is strictly lossy -- it always sheds superseded marbles


# => Run: pytest -- Output: 3 passed
