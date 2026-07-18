# pyright: strict
"""Example 8: Query Builder -- Composed WHERE."""

from __future__ import annotations

from pypika import Field, Query, Table  # => co-03: WHERE predicates are composed as Field expressions

customer = Table("customer")  # => the table every predicate below is built against


def build_active_in_country(country: str, min_age: int) -> str:  # => co-03: two conditions, composed programmatically
    # => `country` and `min_age` are plain Python values -- the CALLER decides the filter, not string surgery
    query = (
        Query.from_(customer)  # => start the builder tree from the customer table
        .select(customer.id, customer.name)  # => the column list, same as Example 7
        .where(Field("country") == country)  # => first predicate -- a Field compared with `==`, not a string
        .where(Field("age") >= min_age)  # => a SECOND .where() call ANDs onto the first -- no manual "AND" text
    )  # => the tree only becomes SQL text when rendered below -- nothing runs yet
    return str(query)  # => renders the whole composed tree to SQL text on demand


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    sql = build_active_in_country("US", 18)  # => country and min_age are ordinary Python arguments, not string parts
    print(sql)  # => Output: SELECT "id","name" FROM "customer" WHERE "country"='US' AND "age">=18
    assert sql == 'SELECT "id","name" FROM "customer" WHERE "country"=\'US\' AND "age">=18'
    # => co-03: two SEPARATE .where() calls composed into one AND-joined clause -- built from values, not concatenation
    # => swapping "US" for another country string requires no string surgery -- just a different function argument
    # => Example 11 shows why this matters: the SAME composition style keeps user input out of the SQL text entirely
    print("ex-08 OK")  # => Output: ex-08 OK
