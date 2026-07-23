# pyright: strict
"""Example 11: Query Builder vs f-string -- Injection Safety."""

from __future__ import annotations  # => enables modern type-hint syntax across this file

from pypika import Field, Query, Table  # => co-05: comparing a Field to a Python value, not splicing text

customer = Table("customer")  # => the table both approaches below query against
ATTACK_INPUT: str = "x' OR '1'='1"  # => a classic SQL-injection payload -- a single quote breaks naive interpolation


def build_with_pypika(name: str) -> str:  # => co-03 + co-05: the builder approach
    query = Query.from_(customer).select(customer.id).where(Field("name") == name)  # => `name` is a bound VALUE, not text
    return str(query)  # => renders the tree -- PyPika escapes the value while rendering the literal


def build_with_fstring(name: str) -> str:  # => the naive, UNSAFE approach -- shown only to contrast, never to use
    return f'SELECT "id" FROM "customer" WHERE "name"=\'{name}\''  # => splices `name` directly into the SQL text


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    safe_sql = build_with_pypika(ATTACK_INPUT)  # => the SAME attack string, run through the builder
    print(safe_sql)  # => Output: SELECT "id" FROM "customer" WHERE "name"='x'' OR ''1''=''1'
    assert safe_sql == "SELECT \"id\" FROM \"customer\" WHERE \"name\"='x'' OR ''1''=''1'"  # => the attack stayed DATA
    # => PyPika DOUBLED every single quote ('' instead of ') -- the payload became one harmless string literal

    unsafe_sql = build_with_fstring(ATTACK_INPUT)  # => the SAME attack string, spliced with an f-string instead
    print(unsafe_sql)  # => Output: SELECT "id" FROM "customer" WHERE "name"='x' OR '1'='1'
    assert unsafe_sql == "SELECT \"id\" FROM \"customer\" WHERE \"name\"='x' OR '1'='1'"  # => the attack became SQL syntax
    # => the quote in ATTACK_INPUT closed the string EARLY -- "OR '1'='1'" now reads as executable SQL, not data
    # => co-05: this is why every raw-SQL example in this topic (Examples 2-6) used %s placeholders, never f-strings
    assert safe_sql != unsafe_sql  # => co-05: identical input, different SQL -- the builder neutralized it, text didn't
    print("ex-11 OK")  # => Output: ex-11 OK
