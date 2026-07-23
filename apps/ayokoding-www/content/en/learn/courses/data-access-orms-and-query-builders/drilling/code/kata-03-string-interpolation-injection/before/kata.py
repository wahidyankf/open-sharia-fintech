# pyright: strict
"""Kata 3 (before): an f-string-interpolated WHERE clause lets a crafted name return every row."""

from __future__ import annotations

import os

import psycopg

PG_DSN: str = os.environ.get("PG_DSN", "postgresql://postgres:postgres@localhost:5432/orm_by_example")


if __name__ == "__main__":
    with psycopg.connect(PG_DSN, autocommit=True) as conn:
        conn.execute("DROP SCHEMA public CASCADE")
        conn.execute("CREATE SCHEMA public")
        conn.execute("CREATE TABLE customer(id SERIAL PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL)")
        conn.execute(
            "INSERT INTO customer(name, email) VALUES (%s, %s), (%s, %s)",
            ("Ada", "ada@example.com", "Grace", "secret@example.com"),
        )

    # intent: look up ONE customer by a name typed into a search box
    untrusted_input = "Ada' OR '1'='1"  # => a name that was never actually seeded -- crafted to always be true
    with psycopg.connect(PG_DSN) as conn:
        # BUG: the untrusted value is spliced directly into the SQL TEXT via an f-string -- pyright still
        # accepts this as a LiteralString (every PIECE of the f-string is itself a literal), which is
        # EXACTLY why the type checker cannot catch this bug: the type system only proves "not built from
        # unknown runtime data," never "safe to interpolate untrusted VALUES into," a narrower guarantee
        sql_text = f"SELECT id, name, email FROM customer WHERE name = '{untrusted_input}'"
        rows = conn.execute(sql_text).fetchall()  # => the crafted quote breaks OUT of the intended string literal
    print(f"rows_returned={len(rows)}")  # => Output: rows_returned=2 -- BOTH customers, including Grace's secret email
    print(f"emails={[r[2] for r in rows]}")  # => Output: emails=['ada@example.com', 'secret@example.com']
