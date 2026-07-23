"""Example 76: pytest verification for the Subset-Sum-to-Partition Reduction."""

from example import can_partition, reduce_subset_sum_to_partition, subset_sum_possible


def test_reduction_preserves_a_yes_instance() -> None:
    items = [3, 7, 2, 9, 5]
    target = 5  # => the single-element subset {5} sums to 5
    assert subset_sum_possible(items, target) is True
    assert can_partition(reduce_subset_sum_to_partition(items, target)) is True


def test_reduction_preserves_a_no_instance() -> None:
    items = [3, 7, 2, 9, 5]
    unreachable_target = 4  # => no subset of {3, 7, 2, 9, 5} sums to 4
    assert subset_sum_possible(items, unreachable_target) is False
    assert (
        can_partition(reduce_subset_sum_to_partition(items, unreachable_target))
        is False
    )


def test_reduced_instance_always_has_exactly_one_more_element() -> None:
    items = [2, 2, 4, 6]
    for target in range(sum(items) // 2 + 1):
        reduced = reduce_subset_sum_to_partition(items, target)
        assert len(reduced) == len(items) + 1


# => Run: pytest -- Output: 3 passed
