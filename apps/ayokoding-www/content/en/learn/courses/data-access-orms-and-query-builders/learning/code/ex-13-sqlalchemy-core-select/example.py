# pyright: strict
"""Example 13: SQLAlchemy Core -- select()."""

from __future__ import annotations

import os  # => reads connection settings from the environment

from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, select, text  # => co-03: Core's builder

SQLA_URL: str = os.environ.get(  # => the SQLAlchemy dialect+driver URL, distinct from a plain DB-API DSN
    "SQLA_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/orm_by_example"
)  # => override SQLA_URL in the environment to point at a different Postgres instance

metadata = MetaData()  # => co-04: registers every Core Table defined against it
product = Table(  # => the Core Table this example's select() statement queries
    "product",
    metadata,
    Column("id", Integer, primary_key=True),  # => auto-incrementing primary key
    Column("name", String, nullable=False),  # => product name -- required
    Column("price_cents", Integer, nullable=False),  # => cents, not a float, to avoid rounding drift (co-05 spirit)
)


def build_and_run() -> tuple[str, list[tuple[int, str]]]:  # => returns BOTH the emitted SQL text and the fetched rows
    engine = create_engine(SQLA_URL)  # => a Core engine -- manages the connection pool for every statement below
    with engine.begin() as conn:  # => begin(): auto-commits on a clean exit, auto-rolls-back on an exception
        conn.execute(text("DROP SCHEMA public CASCADE"))  # => wipes EVERY table -- fully isolated from other examples
        conn.execute(text("CREATE SCHEMA public"))  # => a blank public schema to build the fresh Table into
    metadata.create_all(engine)  # => issues CREATE TABLE product from the Table object above
    stmt = select(product.c.id, product.c.name).where(product.c.price_cents > 1000)  # => co-03: a Core select() construct
    # => `product.c.id` accesses a Column by name -- `.c` is Core's column collection on every Table
    # => `stmt` is still just a builder tree here -- nothing has executed against Postgres yet
    compiled = stmt.compile(engine, compile_kwargs={"literal_binds": True})  # => renders WITH bound values inlined, for display
    # => literal_binds=True is a DISPLAY-ONLY convenience -- the actual execute() below still binds parameters (co-05)
    with engine.begin() as conn:  # => a second transaction: seed 2 rows, then run the select from above
        conn.execute(product.insert().values(name="Widget", price_cents=999))  # => below the $10.00 threshold
        conn.execute(product.insert().values(name="Gadget", price_cents=1999))  # => above the $10.00 threshold
        result = conn.execute(stmt)  # => co-05: the DRIVER binds price_cents=1000 as a real parameter, not literal text
        rows = [(int(r[0]), str(r[1])) for r in result.fetchall()]  # => normalize Row objects to plain tuples
    return str(compiled), rows  # => the display-only SQL text, plus the actually-fetched rows


if __name__ == "__main__":  # => module entry point -- only runs when executed directly, not on import
    sql_text, rows = build_and_run()  # => builds, creates schema, seeds 2 rows, and runs the filtered select once
    print(sql_text)  # => Output: SELECT product.id, product.name  FROM product  WHERE product.price_cents > 1000
    # => compile() prints on 3 lines (SELECT / FROM / WHERE) -- SQLAlchemy's default multi-line pretty-printing
    print(rows)  # => Output: [(2, 'Gadget')]
    assert "product.price_cents > 1000" in sql_text  # => confirms the WHERE clause compiled as expected
    assert rows == [(2, "Gadget")]  # => only Gadget clears the threshold -- Widget was correctly filtered out
    # => co-03 + co-05: Core BUILDS the statement tree; the engine still binds parameters when it actually executes
    # => co-04: this IS SQLAlchemy's own builder, contrasted with PyPika (Example 7-11) -- both compose queries as data
    print("ex-13 OK")  # => Output: ex-13 OK
