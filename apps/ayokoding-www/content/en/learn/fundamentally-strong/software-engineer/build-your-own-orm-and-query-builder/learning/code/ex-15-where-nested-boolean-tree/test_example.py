"""Example 15: pytest verification for a Nested Boolean Tree."""

from example import And, Or, col


def test_nested_tree_parenthesizes_only_the_or() -> None:
    tree = And(left=col("a") == 1, right=Or(left=col("b") == 2, right=col("c") == 3))
    sql, params = tree.compile()  # => one recursive compile() walk
    assert sql == "a = ? AND (b = ? OR c = ?)"  # => AND bare, OR parenthesized
    assert params == [1, 2, 3]  # => depth-first, left-to-right


def test_deeper_nesting_still_compiles_correctly() -> None:
    inner = Or(left=col("x") == 1, right=col("y") == 2)  # => innermost OR
    outer = And(left=inner, right=col("z") == 3)  # => OR nested on the LEFT this time
    sql, params = outer.compile()  # => walks OR first, then the remaining leaf
    assert sql == "(x = ? OR y = ?) AND z = ?"  # => parens travel with the OR, wherever it sits
    assert params == [1, 2, 3]  # => still strictly left-to-right


# => Run: pytest -- Output: 2 passed
