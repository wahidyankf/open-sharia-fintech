"""Example 25: pytest verification for the Doubling Dynamic Array."""

from example import DynamicArray


def test_all_appended_values_are_stored_in_order() -> None:
    arr = DynamicArray()
    for v in [10, 20, 30]:
        arr.append(v)
    assert arr.size == 3
    assert [arr.data[i] for i in range(arr.size)] == [10, 20, 30]


def test_amortized_copy_count_stays_bounded_as_n_grows() -> None:
    small = DynamicArray()
    for i in range(100):
        small.append(i)
    large = DynamicArray()
    for i in range(10_000):
        large.append(i)
    small_ratio = small.total_copies / 100
    large_ratio = large.total_copies / 10_000
    assert large_ratio < 2.0  # => a 100x bigger n does NOT proportionally grow copies
    assert small_ratio < 2.0


# => Run: pytest -- Output: 2 passed
