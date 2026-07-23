"""Example 26: pytest verification for a Fully Type-Annotated Builder Chain."""

from example import Select


def test_typed_chain_compiles_to_expected_sql_and_params() -> None:
    chain = Select(table="orders").select("id").where_id(3)  # => same typed chain shape
    sql, params = chain.compile()  # => tuple[str, list[Any]], per the declared return type
    assert sql == "SELECT id FROM orders WHERE id = ?"  # => both fluent steps took effect
    assert params == [3]  # => the narrowed int landed in the typed params list


# => Run: pytest -- Output: 1 passed
