# pyright: strict
"""Example 9: Query Builder -- Two-Table JOIN."""

from __future__ import annotations

from pypika import JoinType, Query, Table  # => co-03: JoinType picks INNER/LEFT/etc as a typed enum, not a keyword string

customer = Table("customer")  # => the "one" side of the join
customer_order = Table("customer_order")  # => the "many" side -- named to avoid the reserved word "order"
# => module-level Table values, reused by every function below -- a builder Table is just a plain Python object


def build_orders_with_customer() -> str:  # => co-03: a two-table join, entirely composed from Table/Field values
    query = (
        Query.from_(customer_order)  # => start the builder tree from the "many" side
        .join(customer, JoinType.inner)  # => explicit INNER join -- PyPika defaults to inner if omitted, this spells it out
        .on(customer.id == customer_order.customer_id)  # => .on() takes an expression object comparing two Fields
        .select(customer_order.id, customer.name, customer_order.total)  # => columns pulled from BOTH tables
    )  # => the tree only becomes SQL text when rendered below -- nothing runs yet
    return str(query)  # => renders the whole composed tree to SQL text on demand


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    sql = build_orders_with_customer()  # => builds then renders the join -- no execution, no connection needed
    print(sql)  # => Output: SELECT "customer_order"."id","customer"."name","customer_order"."total" FROM "customer_order" JOIN "customer" ON "customer"."id"="customer_order"."customer_id"
    expected = 'SELECT "customer_order"."id","customer"."name","customer_order"."total" FROM "customer_order" JOIN "customer" ON "customer"."id"="customer_order"."customer_id"'  # => the fully rendered join, one line
    assert sql == expected  # => confirms PyPika qualified every column with its OWN table name automatically
    # => co-03: the JOIN's shape came entirely from Table/Field VALUES -- never a hand-typed "JOIN ... ON ..." string
    # => .join()/.on() compose the SAME way .where() did in Example 8 -- one consistent builder API for every clause
    print("ex-09 OK")  # => Output: ex-09 OK
