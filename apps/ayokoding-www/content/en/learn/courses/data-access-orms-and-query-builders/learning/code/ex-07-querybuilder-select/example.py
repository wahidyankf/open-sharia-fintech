# pyright: strict
"""Example 7: Query Builder -- SELECT."""

from __future__ import annotations

from pypika import Query, Table  # => co-03: PyPika builds queries as composable Python values, not strings

customer = Table("customer")  # => a Table VALUE -- can be inspected, reused, and combined like any object


def build_select_all() -> str:  # => returns the RENDERED SQL text -- nothing executes here, only builds
    query = Query.from_(customer).select("id", "name", "email")  # => co-03: SELECT list composed from column names
    return str(query)  # => PyPika only renders the builder tree to SQL text when you ask for it


def build_select_columns() -> str:  # => the same table, a NARROWER column list -- same builder API either way
    query = Query.from_(customer).select(customer.id, customer.name)  # => `customer.id` is a Field VALUE, not a string
    return str(query)  # => rendering is always the same final step, regardless of how the tree was built


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    sql_all = build_select_all()  # => builds then renders a SELECT of 3 named columns
    print(sql_all)  # => Output: SELECT "id","name","email" FROM "customer"
    assert sql_all == 'SELECT "id","name","email" FROM "customer"'  # => PyPika double-quotes identifiers by default
    # => co-05: no values are being bound here -- SELECT with a fixed column list has nothing to parameterize

    sql_cols = build_select_columns()  # => builds then renders a SELECT of 2 named columns via Field objects
    print(sql_cols)  # => Output: SELECT "id","name" FROM "customer"
    assert sql_cols == 'SELECT "id","name" FROM "customer"'  # => `customer.id`/`customer.name` render identically to strings
    # => co-03: `customer.id` and the string "id" produced the SAME output -- Field objects are just a typed spelling
    print("ex-07 OK")  # => Output: ex-07 OK
