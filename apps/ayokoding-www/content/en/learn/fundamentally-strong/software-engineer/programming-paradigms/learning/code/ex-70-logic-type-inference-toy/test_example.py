"""Example 70: pytest verification for Logic Type-Inference Toy."""

import pytest

from example import Add, BoolLit, If, IntLit, infer_type


def test_add_of_two_ints_infers_int() -> None:
    assert infer_type(Add(IntLit(1), IntLit(2))) == "int"  # => the Add rule's base case


def test_if_with_matching_branch_types_infers_that_type() -> None:
    expr = If(BoolLit(False), IntLit(1), IntLit(2))  # => both branches are int
    assert infer_type(expr) == "int"


def test_mismatched_branch_types_raise_a_type_error() -> None:
    bad_expr = If(BoolLit(True), IntLit(1), BoolLit(False))  # => branches disagree: int vs bool
    with pytest.raises(TypeError):
        infer_type(bad_expr)


# => Run: pytest -- Output: 3 passed
