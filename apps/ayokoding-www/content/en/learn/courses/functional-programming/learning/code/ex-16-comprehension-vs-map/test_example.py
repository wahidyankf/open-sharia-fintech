"""Example 16: pytest verification for A Comprehension Matching map() and filter()."""


def test_comprehension_matches_map_filter() -> None:
    nums = list(range(1, 11))
    via_map_filter = list(map(lambda n: n * n, filter(lambda n: n % 2 == 0, nums)))
    via_comprehension = [n * n for n in nums if n % 2 == 0]
    assert via_map_filter == via_comprehension


# => Run: pytest -- Output: 1 passed
