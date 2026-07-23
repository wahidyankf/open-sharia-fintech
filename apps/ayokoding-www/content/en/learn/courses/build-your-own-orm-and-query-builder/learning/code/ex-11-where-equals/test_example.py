"""Example 11: pytest verification for col("age") == 30."""

from example import Select, col


def test_eq_predicate_compiles_to_placeholder() -> None:
    query = Select(table="users").where(col("age") == 30)  # => equality predicate
    sql, params = query.compile()  # => splits SQL text from bound params
    assert sql == "SELECT * FROM users WHERE age = ?"  # => literal 30 never inlined
    assert params == [30]  # => value travels in the params list


def test_different_column_and_value_compile_correctly() -> None:
    query = Select(table="orders").where(col("status") == "open")  # => string value this time
    sql, params = query.compile()  # => splits SQL text from bound params
    assert sql == "SELECT * FROM orders WHERE status = ?"  # => same shape, different column
    assert params == ["open"]  # => the string travels as a bound param, not quoted in SQL


# => Run: pytest -- Output: 2 passed
