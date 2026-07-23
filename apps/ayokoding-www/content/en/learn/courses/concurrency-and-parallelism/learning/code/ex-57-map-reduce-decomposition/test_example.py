"""Example 57: pytest verification for Map-Reduce Decomposition."""

from example import chunk_list, map_reduce_sum


def test_chunk_list_covers_every_element_with_no_overlap() -> None:
    data = list(range(10))
    chunks = chunk_list(data, 3)
    flattened = [item for chunk in chunks for item in chunk]
    assert flattened == data  # => every element appears exactly once, in original order


def test_map_reduce_sum_matches_the_serial_baseline() -> None:
    data = list(range(1, 1001))
    assert map_reduce_sum(data, 4) == sum(data)  # => split-then-combine matches summing the whole list directly


# => Run: pytest -- Output: 2 passed
