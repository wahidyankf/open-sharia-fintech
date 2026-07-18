"""Example 28: Metadata Drives a SELECT's Column List."""  # => this concept

import contextlib  # => guarantees Connection.close() even if the block below raises
import dataclasses  # => frozen dataclasses model immutable metadata records
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)


@dataclasses.dataclass(frozen=True)  # => co-09: a single registered column
class Column:  # => holds just a name -- enough to drive a SELECT's column list
    name: str  # => the column's name, in registration order


@dataclasses.dataclass(frozen=True)  # => co-09: the shared metadata record
class TableMeta:  # => a table's registered columns, nothing else needed here
    name: str  # => the table name
    columns: tuple[Column, ...]  # => ordered columns -- registration order, never re-sorted


def select_all_columns(meta: TableMeta) -> str:  # => co-04: builds SELECT from metadata, not a hand-typed list
    col_list = ", ".join(c.name for c in meta.columns)  # => joins in REGISTRATION order
    return f"SELECT {col_list} FROM {meta.name}"  # => co-09: metadata is the ONE source of truth here


users_meta = TableMeta(  # => registered once, columns declared in a deliberate order
    name="users",  # => table name
    columns=(Column(name="id"), Column(name="name"), Column(name="email")),  # => id, name, email -- in order
)  # => nothing about this metadata mentions SQL text yet
sql = select_all_columns(users_meta)  # => the ONLY place metadata turns into SQL text
assert sql == "SELECT id, name, email FROM users"  # => order matches registration exactly

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, email TEXT)")  # => real table
    conn.execute("INSERT INTO users(id, name, email) VALUES (1, 'Alice', 'alice@example.com')")  # => one row
    conn.commit()  # => makes the seed row visible
    row = conn.execute(sql).fetchone()  # => runs the metadata-derived SELECT for real
    print(row)  # => Output: (1, 'Alice', 'alice@example.com')
