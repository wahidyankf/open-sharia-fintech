"""Example 13: pytest verification for Combine Two Predicates With OR."""

from example import Or, col


def test_or_wraps_both_branches_in_parens() -> None:
    pred = Or(left=col("a") == 1, right=col("b") == 2)  # => two leaves
    sql, params = pred.compile()  # => splits into text + bound values
    assert sql == "(a = ? OR b = ?)"  # => outer parens present, exactly one " OR "
    assert params == [1, 2]  # => left's value before right's value


def test_or_composes_inside_a_larger_where_clause() -> None:
    pred = Or(left=col("a") == 1, right=col("b") == 2)  # => same OR node
    sql, _ = pred.compile()  # => only the SQL text is checked here
    full = f"col = ? AND {sql}"  # => embeds the parenthesized OR inside a bigger clause
    assert full == "col = ? AND (a = ? OR b = ?)"  # => parens keep AND/OR precedence correct


# => Run: pytest -- Output: 2 passed
