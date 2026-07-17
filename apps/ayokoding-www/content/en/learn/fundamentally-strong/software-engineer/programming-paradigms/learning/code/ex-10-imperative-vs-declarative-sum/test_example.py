"""Example 10: pytest verification for Imperative vs Declarative Sum."""

from example import sum_of_squares_of_evens_declarative, sum_of_squares_of_evens_imperative


def test_both_forms_agree_on_one_through_ten() -> None:
    data = list(range(1, 11))  # => same input as the module-level demo
    imp = sum_of_squares_of_evens_imperative(data)  # => HOW version
    dec = sum_of_squares_of_evens_declarative(data)  # => WHAT version
    assert imp == dec == 220  # => 4 + 16 + 36 + 64 + 100


def test_both_forms_agree_on_an_empty_list() -> None:
    assert sum_of_squares_of_evens_imperative([]) == 0  # => empty input, empty-safe accumulator
    assert sum_of_squares_of_evens_declarative([]) == 0  # => sum() of an empty generator is 0


# => Run: pytest -- Output: 2 passed
