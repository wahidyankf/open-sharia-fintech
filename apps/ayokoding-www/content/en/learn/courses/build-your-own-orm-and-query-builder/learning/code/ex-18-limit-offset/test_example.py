"""Example 18: pytest verification for LIMIT and OFFSET."""

from example import Select


def test_limit_and_offset_both_bind_as_placeholders() -> None:
    query = Select(table="items").limit(5).offset(10)  # => both set
    sql, params = query.compile()  # => splits into text + bound values
    assert sql == "SELECT * FROM items LIMIT ? OFFSET ?"  # => two placeholders, in order
    assert params == [5, 10]  # => limit's value before offset's value


def test_limit_without_offset_omits_offset_clause() -> None:
    query = Select(table="items").limit(5)  # => only limit set, no offset
    sql, params = query.compile()  # => splits into text + bound values
    assert sql == "SELECT * FROM items LIMIT ?"  # => no "OFFSET" text at all
    assert params == [5]  # => exactly one bound value


# => Run: pytest -- Output: 2 passed
