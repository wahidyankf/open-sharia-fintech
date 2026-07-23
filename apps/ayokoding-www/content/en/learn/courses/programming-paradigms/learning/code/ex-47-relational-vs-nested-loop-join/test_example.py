"""Example 47: pytest verification for Relational vs Nested-Loop Join."""

from example import join_via_nested_loop, join_via_sql


def test_sql_and_nested_loop_joins_produce_identical_rows() -> None:
    customers = [(1, "alice"), (2, "bob")]  # => same fixtures as the module-level demo
    orders = [(101, 1, "widget"), (102, 2, "gadget"), (103, 1, "gizmo")]
    assert join_via_sql(customers, orders) == join_via_nested_loop(customers, orders)


def test_an_order_with_no_matching_customer_is_dropped_by_both_joins() -> None:
    customers = [(1, "alice")]  # => only customer 1 exists
    orders = [(101, 1, "widget"), (102, 99, "orphan")]  # => order 102 references a nonexistent customer
    sql_rows = join_via_sql(customers, orders)  # => an INNER JOIN drops unmatched orders
    loop_rows = join_via_nested_loop(customers, orders)  # => the nested loop's `break` also drops it
    assert sql_rows == loop_rows == [("alice", "widget")]  # => both agree: the orphan order vanishes


# => Run: pytest -- Output: 2 passed
