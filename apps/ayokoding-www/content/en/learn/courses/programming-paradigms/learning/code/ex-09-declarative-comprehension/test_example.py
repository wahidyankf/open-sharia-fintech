"""Example 9: pytest verification for Declarative Comprehension."""

from example import evens_squared_declarative, evens_squared_imperative


def test_both_forms_produce_the_identical_list() -> None:
    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # => same input the module-level demo uses
    assert evens_squared_imperative(nums) == evens_squared_declarative(nums) == [4, 16, 36, 64, 100]


def test_both_forms_handle_an_all_odd_input_identically() -> None:
    nums = [1, 3, 5]  # => no evens at all -- edge case
    assert evens_squared_imperative(nums) == evens_squared_declarative(nums) == []


# => Run: pytest -- Output: 2 passed
