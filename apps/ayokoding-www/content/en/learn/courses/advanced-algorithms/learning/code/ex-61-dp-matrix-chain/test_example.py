"""Example 61: pytest verification for Matrix-Chain Multiplication Order."""

from example import matrix_chain_min_cost


def test_known_clrs_chain_example() -> None:
    dims = [30, 35, 15, 5, 10, 20, 25]
    assert matrix_chain_min_cost(dims) == 15125


def test_single_matrix_has_zero_cost() -> None:
    assert matrix_chain_min_cost([5, 10]) == 0


def test_two_matrices_have_exactly_one_possible_order() -> None:
    assert matrix_chain_min_cost([2, 3, 4]) == 24  # => 2*3*4, the only possible order


# => Run: pytest -- Output: 3 passed
