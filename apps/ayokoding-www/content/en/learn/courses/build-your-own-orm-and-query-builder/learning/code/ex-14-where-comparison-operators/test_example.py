"""Example 14: pytest verification for Lt, Gt, Ne, and In."""

from example import col


def test_lt_and_gt_compile_correctly() -> None:
    lt_sql, lt_params = (col("age") < 18).compile()  # => Lt
    gt_sql, gt_params = (col("age") > 65).compile()  # => Gt
    assert (lt_sql, lt_params) == ("age < ?", [18])  # => strict less-than
    assert (gt_sql, gt_params) == ("age > ?", [65])  # => strict greater-than


def test_in_compiles_one_placeholder_per_value() -> None:
    sql, params = col("id").in_(5, 6, 7).compile()  # => three-value membership check
    assert sql == "id IN (?, ?, ?)"  # => one "?" per value, comma-separated
    assert params == [5, 6, 7]  # => call order preserved in the params list


# => Run: pytest -- Output: 2 passed
