"""Example 58: pytest verification for Paradigm Cost Table."""

from example import count_lines, count_local_names, evens_squared_declarative, evens_squared_imperative


def test_declarative_version_measures_fewer_lines_and_local_names() -> None:
    imperative_lines = count_lines(evens_squared_imperative)  # => real measurement, not a guess
    declarative_lines = count_lines(evens_squared_declarative)  # => real measurement of the other version
    assert declarative_lines < imperative_lines  # => the concrete metric this example's claim rests on

    imperative_names = count_local_names(evens_squared_imperative)
    declarative_names = count_local_names(evens_squared_declarative)
    assert declarative_names < imperative_names  # => declarative never introduces a named accumulator


def test_both_measured_versions_are_still_behaviorally_equivalent() -> None:
    nums = [1, 2, 3, 4, 5, 6]  # => a cost comparison is meaningless if the versions disagree
    assert evens_squared_imperative(nums) == evens_squared_declarative(nums) == [4, 16, 36]


# => Run: pytest -- Output: 2 passed
