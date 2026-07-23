"""Example 22: pytest verification for State Fault Line Demo."""

import example
from example import total_immutable


def test_immutable_fold_needs_no_shared_state_at_all() -> None:
    before = example.running_total  # => snapshot the module global before this test touches anything
    result = total_immutable([1, 2, 3, 4])  # => a completely separate computation via the fold
    assert result == 10  # => 1+2+3+4
    assert example.running_total == before  # => the fold never touched the global -- proves isolation


def test_mutable_global_version_matches_the_immutable_fold() -> None:
    from example import add_mutable

    example.running_total = 0  # => reset the shared global explicitly for this test's own run
    for n in (5, 15):  # => drive the mutable version with a fresh sequence
        add_mutable(n)
    assert example.running_total == 20  # => 5 + 15
    assert example.running_total == total_immutable([5, 15])  # => both styles agree on the same total


# => Run: pytest -- Output: 2 passed
