"""Example 67: pytest verification for An Expression AST as an ADT With a match Evaluator."""

from example import Add, Mul, Num, evaluate


def test_evaluator_respects_precedence_baked_into_the_tree_shape() -> None:
    expr = Add(Num(2), Mul(Num(3), Num(4)))
    assert evaluate(expr) == 14.0


# => Run: pytest -- Output: 1 passed
