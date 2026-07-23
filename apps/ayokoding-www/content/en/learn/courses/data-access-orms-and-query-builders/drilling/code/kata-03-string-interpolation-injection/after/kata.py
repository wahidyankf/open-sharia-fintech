# pyright: strict
"""Kata 3 (after): a %s placeholder keeps the untrusted value OUT of the SQL text entirely."""

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

    untrusted_input = "Ada' OR '1'='1"  # => the SAME crafted string -- the fix does not depend on cleaning the input
    with psycopg.connect(PG_DSN) as conn:
        # THE FIX: %s is a placeholder -- the driver sends the value as DATA, on a separate wire from the SQL text,
        # so the quote inside untrusted_input can never be interpreted as SQL syntax at all
        rows = conn.execute("SELECT id, name, email FROM customer WHERE name = %s", (untrusted_input,)).fetchall()
    print(f"rows_returned={len(rows)}")  # => Output: rows_returned=0 -- no customer is literally named "Ada' OR '1'='1"
    print(f"emails={[r[2] for r in rows]}")  # => Output: emails=[] -- Grace's email was never at risk
