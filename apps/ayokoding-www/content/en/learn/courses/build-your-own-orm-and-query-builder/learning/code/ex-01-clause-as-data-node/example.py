"""Example 1: Clause as Data, Not a String."""  # => docstring names the concept under test

import contextlib  # => guarantees Connection.close() even if the block below raises
import sqlite3  # => the stdlib DB-API driver this entire topic sits on (PEP 249)
from dataclasses import dataclass  # => frozen dataclasses model immutable clause nodes


@dataclass(frozen=True)  # => frozen: a node is a value, never mutated after creation
class ColumnRef:  # => the SIMPLEST possible clause node -- one column reference
    name: str  # => the only piece of state this node carries

    def render(self) -> str:  # => rendering happens LAZILY, on demand -- not at construction
        return self.name  # => turns the node into SQL text only when asked


node = ColumnRef(name="id")  # => builds a NODE, not a string -- node is a ColumnRef object
# => node.name is "id" (type: str); node itself is NOT a string until .render() runs
assert node.name == "id"  # => the raw data is inspectable before any SQL text exists
assert isinstance(node, ColumnRef)  # => confirms node is a data structure, not str
# => rendering is deferred: nothing above produced a single character of SQL text yet

with contextlib.closing(sqlite3.connect(":memory:")) as conn:  # => real local SQLite db
    conn.execute("CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)")
    # => a real table so the rendered node can be proven against a real query
    conn.execute("INSERT INTO users(id, name) VALUES (1, 'Alice')")
    # => one seed row -- id=1, name='Alice'
    conn.commit()  # => makes the seed row visible to the SELECT below
    sql = f"SELECT {node.render()} FROM users"  # => .render() called HERE, lazily
    # => sql is "SELECT id FROM users" -- the node only became text at this exact point
    row = conn.execute(sql).fetchone()  # => runs the rendered SQL against the real db
    print(row)  # => Output: (1,)
    # => proves node.render() produced valid, executable SQL against a real SQLite table
